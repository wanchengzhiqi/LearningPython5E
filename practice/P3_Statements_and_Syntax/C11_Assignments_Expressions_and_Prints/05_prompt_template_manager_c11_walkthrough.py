r"""
C11 concepts observed through the real prompt_template_manager project.

This script imports pure helper functions from:
    projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_store.py

It does not open or modify the SQLite database.

Run:
    python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\05_prompt_template_manager_c11_walkthrough.py
"""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_MANAGER_DIR = (
    REPO_ROOT / "projects" / "P3_Statements_and_Syntax" / "prompt_template_manager"
)
sys.path.insert(0, str(PROMPT_MANAGER_DIR))

from prompt_store import (  # noqa: E402
    display_state,
    normalize_content,
    parse_tags,
    row_to_record,
    tags_to_json,
)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_binding(name, value):
    print(f"{name:<18} type={type(value).__name__:<10} id={id(value)} repr={value!r}")


def build_list_records_like_query(search=None, category=None, include_deleted=False, limit=None):
    """Small teaching replica of prompt_store.list_records query assembly."""

    clauses = []
    params = []
    query = "SELECT * FROM records"

    if not include_deleted:
        clauses.append("status = 'active'")
    if category:
        clauses.append("category = ?")
        params.append(category)
    if search:
        like = f"%{search}%"
        clauses.append("(title LIKE ? OR category LIKE ? OR content LIKE ? OR tags_json LIKE ?)")
        params.extend([like, like, like, like])

    before_query_id = id(query)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY id ASC"
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    return query, params, clauses, before_query_id


def cli_error_line(message, stream):
    return print(f"Update failed: {message}", file=stream)


def main():
    section("1. parse_tags(): local names plus list/set mutation")
    predict("Will duplicated tags be preserved after parse_tags?")
    tags = parse_tags(" imported, 阶段测验, imported，C11 ")
    show_binding("tags", tags)
    print("Rule: parse_tags builds a new list while using a set to track seen values.")

    section("2. row_to_record(): new dict binding and subscript assignment")
    predict("Does row_to_record mutate fake_row, or return a separate record dict?")
    fake_row = {
        "id": 7,
        "slug": "c11-demo-1234567890",
        "title": "C11 prompt",
        "category": "quiz_generation_request",
        "content": "  请生成阶段测验  ",
        "tags_json": tags_to_json(["imported", "C11"]),
        "source_file": (
            "projects/P3_Statements_and_Syntax/prompt_template_manager/"
            "sample_data/prompt_templates_demo.py"
        ),
        "source_hash": "demo-hash",
        "status": "active",
        "is_locked": 0,
        "updated_at": "2026-06-15T00:00:00+00:00",
    }
    record = row_to_record(fake_row)
    show_binding("fake_row", fake_row)
    show_binding("record", record)
    print("record is fake_row ->", record is fake_row)
    print("record['tags'] ->", record["tags"])
    print("fake_row has tags key ->", "tags" in fake_row)
    print("Rule: record = dict(row) creates a new dict; record['tags'] writes into it.")

    section("3. Normalization returns a value; assignment preserves the chosen state")
    predict("Which name keeps the raw content and which name gets the normalized text?")
    raw_content = fake_row["content"]
    normalized_content = normalize_content(raw_content)
    show_binding("raw_content", raw_content)
    show_binding("normalized_content", normalized_content)
    print("raw_content == normalized_content ->", raw_content == normalized_content)
    print("Correction: normalization result must be bound or returned; it is not magic.")

    section("4. list_records-like query assembly: mutation and rebinding together")
    predict("Which IDs stay the same after query assembly?")
    query, params, clauses, before_query_id = build_list_records_like_query(
        search="阶段测验",
        category="quiz_generation_request",
        limit=5,
    )
    show_binding("clauses", clauses)
    show_binding("params", params)
    show_binding("query", query)
    print("query id changed ->", before_query_id != id(query))
    print("Rule: clauses/params are mutated lists; query is a rebound string.")

    section("5. display_state() reads record state but does not print by itself")
    predict("Does display_state(record) output text or return a string?")
    state = display_state(record)
    show_binding("state", state)
    print("Rule: display_state returns a value; print(state) is the output action.")

    section("6. prompt_manager_cli.py pattern: print(..., file=sys.stderr)")
    predict("What does cli_error_line return, and where does the text go?")
    error_stream = StringIO()
    result = cli_error_line("locked record", error_stream)
    show_binding("result", result)
    show_binding("error_stream", error_stream.getvalue())
    print("Rule: file= selects the stream boundary; print() still returns None.")

    section("7. Safety note")
    print("This walkthrough imported helper functions only; no database was opened or changed.")


if __name__ == "__main__":
    main()
