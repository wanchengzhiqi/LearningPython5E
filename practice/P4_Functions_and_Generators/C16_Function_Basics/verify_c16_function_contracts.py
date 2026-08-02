#!/usr/bin/env python
"""Verify the finalized C16 function contracts with the standard library."""

from __future__ import annotations

import contextlib
import importlib.util
import inspect
import io
import json
import os
from pathlib import Path
import py_compile
import tempfile


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "p3_localization_quality_gate_c16_run_gate.py"
BASELINE_PATH = HERE / "p3_localization_report.json"


@contextlib.contextmanager
def working_directory(path: Path):
    """Temporarily change the process working directory."""

    previous = Path.cwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(previous)


def load_module(module_path: Path, cwd: Path):
    """Load one module and capture its import-time streams."""

    spec = importlib.util.spec_from_file_location(
        "c16_contract_module",
        module_path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module spec: {module_path}")

    module = importlib.util.module_from_spec(spec)
    stdout = io.StringIO()
    stderr = io.StringIO()

    with (
        working_directory(cwd),
        contextlib.redirect_stdout(stdout),
        contextlib.redirect_stderr(stderr),
    ):
        spec.loader.exec_module(module)

    return module, stdout.getvalue(), stderr.getvalue()


def assert_function_metadata(module) -> None:
    """Check that the chapter functions exist as documented objects."""

    expected_names = (
        "normalize_key",
        "extract_placeholders",
        "build_entries",
        "make_issue",
        "validate_entries",
        "print_report",
        "save_report",
        "run_gate",
        "main",
    )

    for name in expected_names:
        function = getattr(module, name)

        assert callable(function)
        assert function.__name__ == name
        assert isinstance(function.__doc__, str)
        assert function.__doc__.strip()
        assert isinstance(inspect.signature(function), inspect.Signature)


def assert_normalize_key(module) -> None:
    """Check the normalization return contract."""

    source = " UI.MENU.START "
    result = module.normalize_key(source)

    assert result == "ui.menu.start"
    assert source == " UI.MENU.START "


def assert_extract_placeholders(module) -> None:
    """Check order, duplicates, and current malformed-token behavior."""

    assert module.extract_placeholders("plain") == []
    assert module.extract_placeholders("{name}{count}") == [
        "{name}",
        "{count}",
    ]
    assert module.extract_placeholders("{name}...{name}") == [
        "{name}",
        "{name}",
    ]
    assert module.extract_placeholders("x{abc") == ["{abc"]
    assert module.extract_placeholders("a}b") == []


def assert_build_entries(module) -> None:
    """Check construction, line numbering, and strict length matching."""

    keys = [" k1 ", "k2"]
    sources = ["S1", "S2"]
    translations = ["T1", "T2"]
    enabled_flags = [True, False]

    result = module.build_entries(
        keys,
        sources,
        translations,
        enabled_flags,
    )

    assert result == [
        {
            "line": 1,
            "key": " k1 ",
            "source": "S1",
            "translation": "T1",
            "enabled": True,
        },
        {
            "line": 2,
            "key": "k2",
            "source": "S2",
            "translation": "T2",
            "enabled": False,
        },
    ]

    assert keys == [" k1 ", "k2"]
    assert sources == ["S1", "S2"]
    assert translations == ["T1", "T2"]
    assert enabled_flags == [True, False]

    try:
        module.build_entries(
            ["k1", "k2"],
            ["S1"],
            ["T1", "T2"],
            [True, True],
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "build_entries() must reject unequal column lengths"
        )


def assert_make_issue(module) -> None:
    """Check structured issue construction and key normalization."""

    entry = {
        "line": 7,
        "key": " UI.TEST ",
    }

    result = module.make_issue(
        "ERROR",
        "sample_code",
        entry,
        "Sample message.",
    )

    assert result == {
        "level": "ERROR",
        "code": "sample_code",
        "line": 7,
        "key": "ui.test",
        "message": "Sample message.",
    }

    assert entry == {
        "line": 7,
        "key": " UI.TEST ",
    }


def assert_validate_entries(module, baseline) -> None:
    """Check the core report contract and current input requirements."""

    entries = module.build_entries(
        module.KEYS,
        module.SOURCE_TEXTS,
        module.TRANSLATIONS,
        module.ENABLED_FLAGS,
    )
    entries_before = [dict(entry) for entry in entries]
    config_before = dict(module.CONFIG)

    result = module.validate_entries(
        entries,
        module.CONFIG,
    )

    assert result == baseline
    assert entries == entries_before
    assert module.CONFIG == config_before

    generator = (entry for entry in entries)

    try:
        module.validate_entries(
            generator,
            module.CONFIG,
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Current validate_entries() contract requires len(entries)"
        )


def assert_print_report(module, baseline) -> None:
    """Check display output separately from the None return object."""

    stdout = io.StringIO()

    with contextlib.redirect_stdout(stdout):
        result = module.print_report(baseline)

    text = stdout.getvalue()

    assert result is None
    assert "=== Localization Quality Gate ===" in text
    assert "Input: 6" in text
    assert "Passed: False" in text
    assert "code=missing_translation" in text
    assert "code=duplicate_key" in text
    assert "code=placeholder_mismatch" in text

    empty_report = {
        "summary": {
            "input_count": 0,
            "processed_count": 0,
            "skipped_count": 0,
            "error_count": 0,
            "warning_count": 0,
            "passed": True,
        },
        "issues": [],
    }

    stdout = io.StringIO()

    with contextlib.redirect_stdout(stdout):
        empty_result = module.print_report(empty_report)

    assert empty_result is None
    assert "No issues found." in stdout.getvalue()


def assert_save_report(module, baseline, temp_dir: Path) -> None:
    """Check UTF-8 JSON persistence and the None return object."""

    path = temp_dir / "saved_report.json"
    report_before = json.loads(json.dumps(baseline))

    result = module.save_report(
        baseline,
        path,
    )

    assert result is None
    assert path.exists()
    assert json.loads(path.read_text(encoding="utf-8")) == baseline
    assert baseline == report_before


def assert_run_gate(module, baseline, temp_dir: Path) -> None:
    """Check report generation without direct display or file I/O."""

    keys = list(module.KEYS)
    sources = list(module.SOURCE_TEXTS)
    translations = list(module.TRANSLATIONS)
    enabled_flags = list(module.ENABLED_FLAGS)
    config = dict(module.CONFIG)

    inputs_before = (
        list(keys),
        list(sources),
        list(translations),
        list(enabled_flags),
        dict(config),
    )

    stdout = io.StringIO()
    stderr = io.StringIO()

    with (
        working_directory(temp_dir),
        contextlib.redirect_stdout(stdout),
        contextlib.redirect_stderr(stderr),
    ):
        result = module.run_gate(
            keys,
            sources,
            translations,
            enabled_flags,
            config,
        )

    assert result == baseline
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == ""
    assert not (temp_dir / "p3_localization_report.json").exists()

    assert keys == inputs_before[0]
    assert sources == inputs_before[1]
    assert translations == inputs_before[2]
    assert enabled_flags == inputs_before[3]
    assert config == inputs_before[4]


def assert_main(module, baseline, temp_dir: Path) -> None:
    """Check the command workflow's display, file, and None contracts."""

    stdout = io.StringIO()
    stderr = io.StringIO()

    with (
        working_directory(temp_dir),
        contextlib.redirect_stdout(stdout),
        contextlib.redirect_stderr(stderr),
    ):
        result = module.main()

    assert result is None
    assert stderr.getvalue() == ""
    assert "Input: 6" in stdout.getvalue()
    assert "Passed: False" in stdout.getvalue()

    generated = temp_dir / "p3_localization_report.json"
    assert generated.exists()
    assert json.loads(
        generated.read_text(encoding="utf-8")
    ) == baseline


def main() -> None:
    """Run the complete C16 contract acceptance suite."""

    py_compile.compile(
        str(MODULE_PATH),
        doraise=True,
    )

    baseline = json.loads(
        BASELINE_PATH.read_text(encoding="utf-8")
    )

    with tempfile.TemporaryDirectory() as directory:
        temp_dir = Path(directory)

        module, import_stdout, import_stderr = load_module(
            MODULE_PATH,
            temp_dir,
        )

        assert import_stdout == ""
        assert import_stderr == ""
        assert not (temp_dir / "p3_localization_report.json").exists()

        assert_function_metadata(module)
        assert_normalize_key(module)
        assert_extract_placeholders(module)
        assert_build_entries(module)
        assert_make_issue(module)
        assert_validate_entries(module, baseline)
        assert_print_report(module, baseline)
        assert_save_report(module, baseline, temp_dir)
        assert_run_gate(module, baseline, temp_dir)

        command_dir = temp_dir / "command"
        command_dir.mkdir()
        assert_main(module, baseline, command_dir)

    print("PASS: module import is side-effect controlled")
    print("PASS: nine function objects expose names, docs, and signatures")
    print("PASS: normalize_key() contract")
    print("PASS: extract_placeholders() contract")
    print("PASS: build_entries() contract and strict mismatch error")
    print("PASS: make_issue() contract")
    print("PASS: validate_entries() baseline and current len() boundary")
    print("PASS: print_report() display/None contracts")
    print("PASS: save_report() file/None contracts")
    print("PASS: run_gate() data-return boundary")
    print("PASS: main() command-side-effect/None boundary")


if __name__ == "__main__":
    main()
