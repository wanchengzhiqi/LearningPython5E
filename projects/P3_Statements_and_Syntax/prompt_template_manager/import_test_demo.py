#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Import prompt snippets from a stable sample source as database snapshots."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from prompt_store import PROJECT_DIR, REPO_ROOT, content_hash, import_blocks, resolve_db_path


DEFAULT_SOURCE = PROJECT_DIR / "sample_data" / "prompt_templates_demo.py"
LEGACY_TEST_DEMO_SOURCE = REPO_ROOT / "tests" / "test_demo.py"
DEFAULT_HEADER_LINES = 3


@dataclass(frozen=True)
class PromptBlock:
    title: str
    category: str
    content: str
    tags: list[str]
    source_file: str
    source_block_index: int
    source_start_line: int
    source_end_line: int
    source_hash: str

    def as_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "tags": self.tags,
            "source_file": self.source_file,
            "source_block_index": self.source_block_index,
            "source_start_line": self.source_start_line,
            "source_end_line": self.source_end_line,
            "source_hash": self.source_hash,
        }


def strip_comment_marker(line: str) -> str:
    if not line.startswith("#"):
        return line.rstrip()
    body = line[1:]
    if body.startswith(" "):
        body = body[1:]
    return body.rstrip()


def title_from_content(content: str, max_length: int = 46) -> str:
    first_line = next((line.strip() for line in content.splitlines() if line.strip()), "")
    if len(first_line) <= max_length:
        return first_line
    return first_line[: max_length - 1] + "..."


def categorize(
    content: str,
    source_block_index: int,
    *,
    source_tag: str = "prompt_template_sample",
) -> tuple[str, list[str]]:
    tags = ["imported", source_tag]
    if source_block_index == 1 and content.startswith("以下是待处理"):
        return "source_note", tags + ["说明"]
    if "改善该脚本" in content and "review" in content:
        return "script_improvement_request", tags + ["脚本", "review"]
    if "尾声" in content:
        return "stage_status_question", tags + ["学习阶段"]
    if "生成一份当前小阶段学习末的考卷" in content:
        return "quiz_generation_request", tags + ["阶段测验"]
    if "代码审查" in content and ("审批" in content or "批改" in content):
        return "quiz_review_request", tags + ["阶段测验", "批改"]
    if "生成一份当前小阶段学习的笔记内容" in content:
        return "notes_consolidation_request", tags + ["笔记"]
    if "是否需要补充至笔记文件" in content:
        return "notes_followup_request", tags + ["笔记", "followup"]
    if "启动模板" in content:
        return "startup_template_request", tags + ["启动模板"]
    if "Activate.ps1" in content or "deactivate" in content:
        return "environment_commands", tags + ["环境"]
    if "$global-memory-audit" in content:
        return "memory_audit_request", tags + ["memory"]
    if "自动化任务" in content and "memory.md" in content:
        return "automation_memory_audit_request", tags + ["automation", "memory"]
    if "数学试题" in content:
        return "reasoning_exam_request", tags + ["推理"]
    return "prompt", tags


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.expanduser().resolve() == right.expanduser().resolve()
    except OSError:
        return False


def source_tag_for_path(path: Path) -> str:
    if same_path(path, DEFAULT_SOURCE):
        return "prompt_template_sample"
    if same_path(path, LEGACY_TEST_DEMO_SOURCE):
        return "test_demo"
    return "custom_source"


def default_skip_header_lines(path: Path) -> int:
    if same_path(path, DEFAULT_SOURCE) or same_path(path, LEGACY_TEST_DEMO_SOURCE):
        return DEFAULT_HEADER_LINES
    return 0


def parse_prompt_source(
    source_path: str | Path = DEFAULT_SOURCE,
    *,
    skip_header_lines: int | None = None,
) -> list[PromptBlock]:
    """Parse effective comment blocks from a prompt source file.

    Built-in and legacy sources skip their three metadata lines by default.
    Custom sources start at line 1 unless skip_header_lines is explicitly set.
    Blank physical lines separate blocks; each block is stored as a snapshot value.
    """

    path = Path(source_path)
    source_tag = source_tag_for_path(path)
    if skip_header_lines is None:
        skip_header_lines = default_skip_header_lines(path)
    if skip_header_lines < 0:
        raise ValueError("skip_header_lines cannot be negative")
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    raw_blocks: list[tuple[int, int, list[str]]] = []
    current: list[str] = []
    start_line: int | None = None
    end_line: int | None = None

    def flush() -> None:
        nonlocal current, start_line, end_line
        if current and start_line is not None and end_line is not None:
            raw_blocks.append((start_line, end_line, current))
        current = []
        start_line = None
        end_line = None

    for line_no, line in enumerate(lines, start=1):
        if line_no <= skip_header_lines:
            continue
        if not line.strip():
            flush()
            continue
        if not line.startswith("#"):
            flush()
            continue
        if start_line is None:
            start_line = line_no
        end_line = line_no
        current.append(strip_comment_marker(line))
    flush()

    blocks: list[PromptBlock] = []
    for index, (start, end, block_lines) in enumerate(raw_blocks, start=1):
        content = "\n".join(block_lines).strip()
        if not content:
            continue
        category, tags = categorize(content, index, source_tag=source_tag)
        blocks.append(
            PromptBlock(
                title=title_from_content(content),
                category=category,
                content=content,
                tags=tags,
                source_file=str(path),
                source_block_index=index,
                source_start_line=start,
                source_end_line=end,
                source_hash=content_hash(content),
            )
        )
    return blocks


def parse_test_demo(
    source_path: str | Path = DEFAULT_SOURCE,
    *,
    skip_header_lines: int | None = None,
) -> list[PromptBlock]:
    """Compatibility wrapper for the historical import_test_demo module name.

    Historical test_demo-shaped files have three metadata lines, so this wrapper
    preserves that default even when the caller passes a custom source path.
    """

    if skip_header_lines is None:
        skip_header_lines = DEFAULT_HEADER_LINES
    return parse_prompt_source(source_path, skip_header_lines=skip_header_lines)


def import_prompt_source(
    *,
    db_path: str | Path | None = None,
    source_path: str | Path = DEFAULT_SOURCE,
    skip_header_lines: int | None = None,
) -> dict[str, object]:
    blocks = [
        block.as_dict()
        for block in parse_prompt_source(
            source_path,
            skip_header_lines=skip_header_lines,
        )
    ]
    return import_blocks(blocks, db_path=db_path)


def import_test_demo(
    *,
    db_path: str | Path | None = None,
    source_path: str | Path = DEFAULT_SOURCE,
    skip_header_lines: int | None = None,
) -> dict[str, object]:
    """Compatibility wrapper; default source is now the project-owned sample."""

    if skip_header_lines is None:
        skip_header_lines = DEFAULT_HEADER_LINES
    return import_prompt_source(
        db_path=db_path,
        source_path=source_path,
        skip_header_lines=skip_header_lines,
    )


def resolve_cli_source(args: argparse.Namespace) -> Path:
    if args.legacy_test_demo:
        return LEGACY_TEST_DEMO_SOURCE
    if args.source:
        return Path(args.source)
    return DEFAULT_SOURCE


def non_negative_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or a positive integer")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import prompt source blocks into SQLite.")
    parser.add_argument("--db", default=None, help="SQLite database path.")
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--source",
        default=None,
        help="Source UTF-8 file path. Defaults to the project-owned sample data.",
    )
    source_group.add_argument(
        "--legacy-test-demo",
        action="store_true",
        help="Read the legacy tests/test_demo.py source once, without writing it.",
    )
    parser.add_argument(
        "--skip-header-lines",
        type=non_negative_int,
        default=None,
        help=(
            "Override source header lines to skip. Defaults: built-in and legacy "
            "sources skip 3 lines; custom --source files skip 0 lines."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source_path = resolve_cli_source(args)
    try:
        result = import_prompt_source(
            db_path=args.db,
            source_path=source_path,
            skip_header_lines=args.skip_header_lines,
        )
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"Import failed: {exc}", file=sys.stderr)
        return 1
    print(f"Database: {resolve_db_path(args.db)}")
    print(f"Source: {source_path}")
    print(f"Imported: {len(result['imported'])}")
    print(f"Skipped: {len(result['skipped'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
