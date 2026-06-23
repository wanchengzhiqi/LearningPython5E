"""C12-05: match boundaries with a read-only prompt manager helper."""

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_MANAGER_DIR = (
    REPO_ROOT / "projects" / "P3_Statements_and_Syntax" / "prompt_template_manager"
)
sys.path.insert(0, str(PROMPT_MANAGER_DIR))

from prompt_store import display_state  # noqa: E402


def section(title):
    print("\n" + "=" * 68)
    print(title)


def actions_with_if(record):
    state = display_state(record)
    if state == "deleted":
        return ["restore", "hard-delete"]
    elif state == "locked":
        return ["unlock"]
    else:
        return ["update", "soft-delete", "lock"]


def actions_with_match(record):
    match display_state(record):
        case "deleted":
            return ["restore", "hard-delete"]
        case "locked":
            return ["unlock"]
        case "active":
            return ["update", "soft-delete", "lock"]
        case _:
            return []


def route_command(command):
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
    section("1. Real anchor: prompt_store.display_state()")
    print("[Predict] Which state and action list does each record select?")
    records = [
        {"id": 1, "status": "active", "is_locked": 0},
        {"id": 2, "status": "active", "is_locked": 1},
        {"id": 3, "status": "deleted", "is_locked": 0},
    ]
    for record in records:
        before = record.copy()
        by_if = actions_with_if(record)
        by_match = actions_with_match(record)
        print(
            f"id={record['id']} state={display_state(record):<7} actions={by_if} "
            f"same={by_if == by_match} unchanged={record == before}"
        )

    section("2. Structural patterns are match's stronger use case")
    print("[Predict] Which command shape and guard will match?")
    commands = [
        {"action": "update", "record_id": 7, "confirmed": True},
        {"action": "update", "record_id": 7, "confirmed": False},
        {"action": "search", "query": "  C12  "},
        {"action": "search", "query": "   "},
        {"action": "delete", "record_id": "not-an-int"},
    ]
    for command in commands:
        print(f"{command!r} -> {route_command(command)}")
    print("Cases do not fall through; do not mechanically replace every if chain.")

    section("3. Safety boundary")
    print("Imported helper: prompt_store.display_state")
    print("Database operations used: none")


if __name__ == "__main__":
    main()
