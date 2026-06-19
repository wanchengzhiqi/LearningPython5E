#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command-line CRUD entrypoint for the prompt template manager."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from import_test_demo import (
    DEFAULT_SOURCE,
    LEGACY_TEST_DEMO_SOURCE,
    import_prompt_source,
)
from prompt_store import (
    add_record,
    display_state,
    get_record,
    hard_delete_record,
    initialize_database,
    list_records,
    lock_record,
    resolve_db_path,
    restore_record,
    soft_delete_record,
    unlock_record,
    update_record,
)


class CliInputError(ValueError):
    """Raised for user-supplied CLI input that cannot be read or parsed."""


def read_content(args: argparse.Namespace) -> str | None:
    if getattr(args, "content_file", None):
        path = Path(args.content_file)
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise CliInputError(f"cannot read content file {path}: {exc}") from exc
        except UnicodeDecodeError as exc:
            raise CliInputError(f"content file must be UTF-8: {path}: {exc}") from exc
    return getattr(args, "content", None)


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def non_negative_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be zero or a positive integer")
    return parsed


def confirm(message: str, assume_yes: bool = False) -> bool:
    if assume_yes:
        return True
    reply = input(f"{message} 输入 yes 确认：").strip().lower()
    return reply == "yes"


def print_record(record: dict, *, show_content: bool = True) -> None:
    tags = ", ".join(record["tags"])
    print(f"[{record['id']}] {record['title']}")
    print(f"  slug: {record['slug']}")
    print(f"  category: {record['category']}")
    print(f"  state: {display_state(record)}")
    print(f"  tags: {tags}")
    print(f"  updated_at: {record['updated_at']}")
    if record.get("source_file"):
        print(
            "  source: "
            f"{record['source_file']}#{record.get('source_start_line')}-"
            f"{record.get('source_end_line')}"
        )
    if show_content:
        print()
        print(record["content"])


def command_init(args: argparse.Namespace) -> int:
    try:
        path = initialize_database(args.db)
    except ValueError as exc:
        print(f"Init failed: {exc}", file=sys.stderr)
        return 1
    print(f"Initialized database: {path}")
    return 0


def command_import_test_demo(args: argparse.Namespace) -> int:
    source_path = resolve_import_source(args)
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


def resolve_import_source(args: argparse.Namespace) -> Path:
    if args.legacy_test_demo:
        return LEGACY_TEST_DEMO_SOURCE
    if args.source:
        return Path(args.source)
    return DEFAULT_SOURCE


def command_list(args: argparse.Namespace) -> int:
    records = list_records(
        db_path=args.db,
        search=args.search,
        include_deleted=args.include_deleted,
        category=args.category,
        limit=args.limit,
    )
    if not records:
        print("No records found.")
        return 0
    for record in records:
        print(
            f"{record['id']:>3} | {display_state(record):<7} | "
            f"{record['category']:<32} | {record['title']}"
        )
    return 0


def command_show(args: argparse.Namespace) -> int:
    record = get_record(args.id, args.db)
    if record is None:
        print(f"Record not found: {args.id}", file=sys.stderr)
        return 1
    print_record(record)
    return 0


def command_search(args: argparse.Namespace) -> int:
    args.search = args.query
    return command_list(args)


def command_add(args: argparse.Namespace) -> int:
    try:
        content = read_content(args)
        if content is None:
            print("add requires --content or --content-file", file=sys.stderr)
            return 2
        record = add_record(
            db_path=args.db,
            title=args.title,
            category=args.category,
            content=content,
            tags=args.tags,
        )
    except CliInputError as exc:
        print(f"Add failed: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Add failed: {exc}", file=sys.stderr)
        return 1
    print("Added record:")
    print_record(record, show_content=False)
    return 0


def command_update(args: argparse.Namespace) -> int:
    current = get_record(args.id, args.db)
    if current is None:
        print(f"Record not found: {args.id}", file=sys.stderr)
        return 1

    try:
        content = read_content(args)
    except CliInputError as exc:
        print(f"Update failed: {exc}", file=sys.stderr)
        return 2
    changes: list[str] = []
    if args.title is not None and args.title != current["title"]:
        changes.append("title")
    if args.category is not None and args.category != current["category"]:
        changes.append("category")
    if content is not None and content.strip() != current["content"].strip():
        changes.append("content")
    if args.tags is not None:
        changes.append("tags")
    if not changes:
        print("No changes provided.")
        return 0

    print(f"Will update record {args.id}: {', '.join(changes)}")
    if not confirm("This modifies the database.", args.yes):
        print("Cancelled.")
        return 1

    try:
        record = update_record(
            args.id,
            db_path=args.db,
            title=args.title,
            category=args.category,
            content=content,
            tags=args.tags,
        )
    except ValueError as exc:
        print(f"Update failed: {exc}", file=sys.stderr)
        return 1
    print("Updated record:")
    print_record(record, show_content=False)
    return 0


def command_delete(args: argparse.Namespace) -> int:
    record = get_record(args.id, args.db)
    if record is None:
        print(f"Record not found: {args.id}", file=sys.stderr)
        return 1
    print_record(record, show_content=False)
    if not confirm("This soft-deletes the record.", args.yes):
        print("Cancelled.")
        return 1
    try:
        soft_delete_record(args.id, args.db)
    except ValueError as exc:
        print(f"Delete failed: {exc}", file=sys.stderr)
        return 1
    print(f"Soft-deleted record {args.id}.")
    return 0


def command_restore(args: argparse.Namespace) -> int:
    try:
        record = restore_record(args.id, args.db)
    except (KeyError, ValueError) as exc:
        print(f"Restore failed: {exc}", file=sys.stderr)
        return 1
    print("Restored record:")
    print_record(record, show_content=False)
    return 0


def command_lock(args: argparse.Namespace) -> int:
    try:
        record = lock_record(args.id, args.db)
    except (KeyError, ValueError) as exc:
        print(f"Lock failed: {exc}", file=sys.stderr)
        return 1
    print("Locked record:")
    print_record(record, show_content=False)
    return 0


def command_unlock(args: argparse.Namespace) -> int:
    try:
        record = unlock_record(args.id, args.db)
    except (KeyError, ValueError) as exc:
        print(f"Unlock failed: {exc}", file=sys.stderr)
        return 1
    print("Unlocked record:")
    print_record(record, show_content=False)
    return 0


def command_hard_delete(args: argparse.Namespace) -> int:
    record = get_record(args.id, args.db)
    if record is None:
        print(f"Record not found: {args.id}", file=sys.stderr)
        return 1
    print_record(record, show_content=False)
    if not confirm("This permanently deletes the soft-deleted record.", args.yes):
        print("Cancelled.")
        return 1
    try:
        deleted = hard_delete_record(args.id, args.db)
    except (KeyError, ValueError) as exc:
        print(f"Hard delete failed: {exc}", file=sys.stderr)
        return 1
    print(f"Permanently deleted record {deleted['id']}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prompt template database manager.")
    parser.add_argument("--db", default=None, help="SQLite database path.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize the database.")
    init_parser.set_defaults(func=command_init)

    import_parser = subparsers.add_parser(
        "import-test-demo",
        help="Import the project-owned prompt sample as database snapshots.",
    )
    source_group = import_parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--source",
        default=None,
        help="Source UTF-8 file path. Defaults to the project-owned sample data.",
    )
    source_group.add_argument(
        "--legacy-test-demo",
        action="store_true",
        help="Read legacy tests/test_demo.py once, without writing it.",
    )
    import_parser.add_argument(
        "--skip-header-lines",
        type=non_negative_int,
        default=None,
        help=(
            "Override source header lines to skip. Defaults: built-in and legacy "
            "sources skip 3 lines; custom --source files skip 0 lines."
        ),
    )
    import_parser.set_defaults(func=command_import_test_demo)

    list_parser = subparsers.add_parser("list", help="List records.")
    list_parser.add_argument("--search", default=None)
    list_parser.add_argument("--category", default=None)
    list_parser.add_argument("--include-deleted", action="store_true")
    list_parser.add_argument("--limit", type=positive_int, default=None)
    list_parser.set_defaults(func=command_list)

    show_parser = subparsers.add_parser("show", help="Show one record.")
    show_parser.add_argument("id", type=int)
    show_parser.set_defaults(func=command_show)

    search_parser = subparsers.add_parser("search", help="Search records.")
    search_parser.add_argument("query")
    search_parser.add_argument("--category", default=None)
    search_parser.add_argument("--include-deleted", action="store_true")
    search_parser.add_argument("--limit", type=positive_int, default=None)
    search_parser.set_defaults(func=command_search)

    add_parser = subparsers.add_parser("add", help="Add a manual record.")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--category", required=True)
    add_parser.add_argument("--content", default=None)
    add_parser.add_argument("--content-file", default=None)
    add_parser.add_argument("--tags", default=None)
    add_parser.set_defaults(func=command_add)

    update_parser = subparsers.add_parser("update", help="Update a record.")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--title", default=None)
    update_parser.add_argument("--category", default=None)
    update_parser.add_argument("--content", default=None)
    update_parser.add_argument("--content-file", default=None)
    update_parser.add_argument("--tags", default=None)
    update_parser.add_argument("--yes", action="store_true")
    update_parser.set_defaults(func=command_update)

    delete_parser = subparsers.add_parser("delete", help="Soft-delete a record.")
    delete_parser.add_argument("id", type=int)
    delete_parser.add_argument("--yes", action="store_true")
    delete_parser.set_defaults(func=command_delete)

    restore_parser = subparsers.add_parser("restore", help="Restore a soft-deleted record.")
    restore_parser.add_argument("id", type=int)
    restore_parser.set_defaults(func=command_restore)

    lock_parser = subparsers.add_parser("lock", help="Lock an active record.")
    lock_parser.add_argument("id", type=int)
    lock_parser.set_defaults(func=command_lock)

    unlock_parser = subparsers.add_parser("unlock", help="Unlock a locked active record.")
    unlock_parser.add_argument("id", type=int)
    unlock_parser.set_defaults(func=command_unlock)

    hard_delete_parser = subparsers.add_parser(
        "hard-delete",
        help="Permanently delete a soft-deleted record.",
    )
    hard_delete_parser.add_argument("id", type=int)
    hard_delete_parser.add_argument("--yes", action="store_true")
    hard_delete_parser.set_defaults(func=command_hard_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"{args.command} failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
