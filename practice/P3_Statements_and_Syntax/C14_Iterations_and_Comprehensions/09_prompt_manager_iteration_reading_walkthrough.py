r"""
Read-only C14 iteration experiments with prompt_template_manager helpers and source.

This script imports pure helpers from prompt_store.py and reads source text. It does
not open, initialize, migrate, or modify the SQLite database.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\09_prompt_manager_iteration_reading_walkthrough.py
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_MANAGER_DIR = (
    REPO_ROOT / "projects" / "P3_Statements_and_Syntax" / "prompt_template_manager"
)
sys.path.insert(0, str(PROMPT_MANAGER_DIR))

from prompt_store import (  # noqa: E402
    normalized_content_hash,
    parse_tags,
    tags_from_json,
)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def source_iteration_lines(limit=10):
    path = PROMPT_MANAGER_DIR / "prompt_store.py"
    lines = path.read_text(encoding="utf-8").splitlines()
    interesting = [
        (line_no, line.strip())
        for line_no, line in enumerate(lines, start=1)
        if looks_like_iteration_code(line.strip())
    ]
    return interesting[:limit]


def looks_like_iteration_code(stripped):
    if stripped.startswith(('"""', "'''", "#")):
        return False
    if stripped.startswith(("for ", "while ")):
        return True
    if stripped.startswith(("return [", "return {")):
        return " for " in stripped
    return " for " in stripped and (" in " in stripped or stripped.startswith("f\""))


def duplicate_content_groups(records):
    """Teaching replica of the explicit grouping style in validate_database_integrity."""

    content_hashes = {}
    for record in records:
        digest = normalized_content_hash(record["content"])
        content_hashes.setdefault(digest, []).append(record["id"])
    return [ids for ids in content_hashes.values() if len(ids) > 1]


def main():
    section("1. Read real source lines that use iteration")
    predict("Which real lines use for, while, or a comprehension?")
    for line_no, text in source_iteration_lines():
        print(f"{line_no}: {text}")

    section("2. parse_tags preserves first-seen order with an explicit loop")
    predict("Can a set comprehension replace parse_tags without changing meaning?")
    raw_tags = " imported, C14, imported, iterator, "
    split_values = raw_tags.split(",")
    stripped_values = [value.strip() for value in split_values]
    non_empty_values = [value for value in stripped_values if value]
    sorted_unique_values = sorted({value for value in non_empty_values})
    print("stripped values ->", stripped_values)
    print("non-empty values ->", non_empty_values)
    print("sorted unique values ->", sorted_unique_values)
    print("parse_tags(raw_tags) ->", parse_tags(raw_tags))
    print("Correction: a set loses first-seen order; parse_tags needs its explicit loop.")

    section("3. tags_from_json is a clean projection")
    predict("What type does each JSON element become?")
    parsed_tags = tags_from_json('["active", 14, null]')
    print("tags_from_json ->", parsed_tags)
    print("types ->", [type(tag).__name__ for tag in parsed_tags])

    section("4. Fake records let us practice projections without opening the database")
    predict("Which active, unlocked titles are selected?")
    records = [
        {
            "id": 1,
            "title": "C14 startup",
            "category": "startup_template_request",
            "content": "Read the C14 startup template.",
            "tags_json": '["C14", "iteration"]',
            "status": "active",
            "is_locked": False,
        },
        {
            "id": 2,
            "title": "C13 closeout",
            "category": "stage_note",
            "content": "C13 closeout note",
            "tags_json": '["C13", "loops"]',
            "status": "active",
            "is_locked": True,
        },
        {
            "id": 3,
            "title": "Duplicate content demo",
            "category": "stage_note",
            "content": "C13 closeout note",
            "tags_json": '["duplicate"]',
            "status": "deleted",
            "is_locked": False,
        },
    ]
    editable_titles = [
        record["title"]
        for record in records
        if record["status"] == "active" and not record["is_locked"]
    ]
    tags_by_id = {record["id"]: tags_from_json(record["tags_json"]) for record in records}
    print("editable_titles ->", editable_titles)
    print("tags_by_id ->", tags_by_id)

    section("5. Hash grouping remains clearer as an explicit loop")
    predict("Which record ids share identical normalized content?")
    print("duplicate content groups ->", duplicate_content_groups(records))
    print("Safety: no SQLite connection was opened or modified.")


if __name__ == "__main__":
    main()
