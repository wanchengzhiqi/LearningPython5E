#!/usr/bin/env python
"""Verify the C16 run_gate() refactor without third-party dependencies."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import py_compile
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "p3_localization_quality_gate_c16_run_gate.py"
EXPECTED_REPORT_PATH = HERE / "p3_localization_report.json"


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
    """Import one module from a file path and capture import output."""

    spec = importlib.util.spec_from_file_location(
        "c16_run_gate_under_test",
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


def main() -> None:
    """Run all structural and behavior checks."""

    if not MODULE_PATH.exists():
        raise FileNotFoundError(MODULE_PATH)

    if not EXPECTED_REPORT_PATH.exists():
        raise FileNotFoundError(
            f"Expected baseline report is missing: {EXPECTED_REPORT_PATH}"
        )

    expected_report = json.loads(
        EXPECTED_REPORT_PATH.read_text(encoding="utf-8")
    )

    py_compile.compile(
        str(MODULE_PATH),
        doraise=True,
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
        assert callable(module.run_gate)
        assert callable(module.main)

        keys = list(module.KEYS)
        sources = list(module.SOURCE_TEXTS)
        translations = list(module.TRANSLATIONS)
        enabled_flags = list(module.ENABLED_FLAGS)
        config = dict(module.CONFIG)

        keys_before = list(keys)
        sources_before = list(sources)
        translations_before = list(translations)
        enabled_before = list(enabled_flags)
        config_before = dict(config)

        run_stdout = io.StringIO()
        run_stderr = io.StringIO()

        with (
            contextlib.redirect_stdout(run_stdout),
            contextlib.redirect_stderr(run_stderr),
        ):
            report = module.run_gate(
                keys,
                sources,
                translations,
                enabled_flags,
                config,
            )

        assert run_stdout.getvalue() == ""
        assert run_stderr.getvalue() == ""
        assert report == expected_report

        assert keys == keys_before
        assert sources == sources_before
        assert translations == translations_before
        assert enabled_flags == enabled_before
        assert config == config_before

        completed = subprocess.run(
            [sys.executable, "-S", str(MODULE_PATH)],
            cwd=temp_dir,
            text=True,
            capture_output=True,
            check=False,
        )

        assert completed.returncode == 0
        assert completed.stderr == ""

        generated_path = temp_dir / "p3_localization_report.json"
        assert generated_path.exists()

        generated_report = json.loads(
            generated_path.read_text(encoding="utf-8")
        )
        assert generated_report == expected_report

        expected_fragments = (
            "Input: 6",
            "Processed: 5",
            "Skipped: 1",
            "Errors: 3",
            "Warnings: 0",
            "Passed: False",
            "code=missing_translation",
            "code=duplicate_key",
            "code=placeholder_mismatch",
        )

        for fragment in expected_fragments:
            assert fragment in completed.stdout

    print("PASS: syntax compilation")
    print("PASS: import has no output or report-writing side effect")
    print("PASS: run_gate() returns the baseline structured report")
    print("PASS: run_gate() produces no direct display or file I/O")
    print("PASS: supplied list/config inputs remain equal to their baselines")
    print("PASS: direct execution prints and saves the baseline report")


if __name__ == "__main__":
    main()
