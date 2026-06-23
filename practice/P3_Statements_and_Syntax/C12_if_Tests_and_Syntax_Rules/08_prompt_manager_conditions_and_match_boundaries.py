r"""
C12 conditions observed through the real prompt_template_manager project.

This script imports pure helpers from prompt_store.py. It does not open,
initialize, migrate, or modify the SQLite database.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\08_prompt_manager_conditions_and_match_boundaries.py
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_MANAGER_DIR = (
    REPO_ROOT / "projects" / "P3_Statements_and_Syntax" / "prompt_template_manager"
)
sys.path.insert(0, str(PROMPT_MANAGER_DIR))

from prompt_store import display_state, parse_tags  # noqa: E402


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def detect_changes(current, *, title=None, category=None, content=None, tags=None):
    """Teaching replica of prompt_manager_cli.command_update conditions."""

    changes = []
    if title is not None and title != current["title"]:
        changes.append("title")
    if category is not None and category != current["category"]:
        changes.append("category")
    if content is not None and content.strip() != current["content"].strip():
        changes.append("content")
    if tags is not None:
        changes.append("tags")
    return changes


def actions_for_record(record):
    """Simple value comparisons remain clearer as ordinary if statements."""

    state = display_state(record)
    if state == "deleted":
        return ["restore", "hard-delete"]
    if state == "locked":
        return ["unlock"]
    return ["update", "soft-delete", "lock"]


def route_command(command):
    """Structural mapping patterns are a stronger use case for match."""

    match command:
        case {"action": "update", "record_id": int(record_id), "confirmed": True}:
            return f"update record {record_id}"
        case {"action": "update", "record_id": int(record_id)}:
            return f"confirmation required for record {record_id}"
        case {"action": "search", "query": str(query)} if query.strip():
            return f"search for {query.strip()!r}"
        case {"action": "search"}:
            return "search query is empty"
        case _:
            return "unsupported command shape"


def main():
    section("1. parse_tags() uses short-circuit filtering in real code")
    predict("Which empty or duplicate tag values will be skipped?")
    raw_tags = " imported, , C12, imported，truth-testing "
    tags = parse_tags(raw_tags)
    print("raw_tags ->", raw_tags)
    print("parse_tags(raw_tags) ->", tags)
    print(
        "Real condition: if value and value not in seen. "
        "An empty value short-circuits the membership test."
    )

    section("2. is not None differs from a truth test")
    predict("Does an explicit empty title count as a requested change?")
    current = {
        "title": "C12 startup",
        "category": "startup_template_request",
        "content": "Read the startup template.",
    }
    print("omitted title ->", detect_changes(current, title=None))
    print("explicit empty title ->", detect_changes(current, title=""))
    print("same title ->", detect_changes(current, title="C12 startup"))
    print("Correction: None means absent here; an empty string is still supplied.")

    section("3. display_state() shows early-return branch selection")
    predict("Which action list belongs to each record state?")
    records = [
        {"id": 1, "status": "active", "is_locked": 0},
        {"id": 2, "status": "active", "is_locked": 1},
        {"id": 3, "status": "deleted", "is_locked": 0},
    ]
    for record in records:
        before = record.copy()
        state = display_state(record)
        actions = actions_for_record(record)
        print(
            f"id={record['id']} state={state:<7} actions={actions} "
            f"unchanged={record == before}"
        )

    section("4. Conditional expressions select GUI configuration values")
    predict("Which state string would prompt_manager_gui use?")
    for editable in (True, False):
        widget_state = "normal" if editable else "disabled"
        print(f"editable={editable!r:<5} -> {widget_state}")

    section("5. match is useful when structure is part of the decision")
    predict("Which mapping shape, type pattern, and guard will match?")
    commands = [
        {"action": "update", "record_id": 7, "confirmed": True},
        {"action": "update", "record_id": 7, "confirmed": False},
        {"action": "search", "query": "  C12  "},
        {"action": "search", "query": "   "},
        {"action": "delete", "record_id": "not-an-int"},
    ]
    for command in commands:
        print(f"{command!r} -> {route_command(command)}")

    section("6. match boundary and safety note")
    print("Cases do not fall through.")
    print("Simple state comparisons can remain ordinary if statements.")
    print("Imported helpers: parse_tags and display_state.")
    print("Database operations used: none.")


if __name__ == "__main__":
    main()
