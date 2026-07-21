r"""
Read-only documentation walk through the real prompt_template_manager project.

This script imports prompt_store definitions, reads UTF-8 source and README
text, and calls only pure helpers. It does not open, initialize, migrate, or
modify the SQLite database.

Run:
    python practice\P3_Statements_and_Syntax\C15_The_Documentation_Interlude\05_prompt_manager_documentation_walkthrough.py
"""

import inspect
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_MANAGER_DIR = (
    REPO_ROOT / "projects" / "P3_Statements_and_Syntax" / "prompt_template_manager"
)
sys.path.insert(0, str(PROMPT_MANAGER_DIR))

import prompt_store  # noqa: E402


PURE_TARGETS = (
    "resolve_db_path",
    "normalized_content_hash",
    "parse_tags",
    "tags_from_json",
)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def markdown_headings(path):
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("#")
    ]


def function_observation(name):
    obj = getattr(prompt_store, name)
    source_line = inspect.getsourcelines(obj)[1]
    return {
        "name": name,
        "signature": str(inspect.signature(obj)),
        "has_docstring": inspect.getdoc(obj) is not None,
        "source_line": source_line,
    }


def main():
    database_path = prompt_store.DEFAULT_DB_PATH
    database_existed_before = database_path.exists()

    section("1. Project README and module docstring answer different questions")
    predict("Which source is broad project guidance, and which is module metadata?")
    readme_path = PROMPT_MANAGER_DIR / "README.md"
    print("README heading sample ->", markdown_headings(readme_path)[:6])
    print("prompt_store.__doc__ ->", prompt_store.__doc__)
    print("module source ->", Path(prompt_store.__file__).name)

    section("2. Inspect selected public call shapes without calling database APIs")
    predict("Which selected functions have local docstrings as well as signatures?")
    for name in PURE_TARGETS:
        print("observation ->", function_observation(name))
    print(
        "Rule: a visible signature or name does not prove a complete documented "
        "public contract."
    )

    section("3. Call only pure helpers with synthetic values")
    predict("Do these helper calls need or create a SQLite connection?")
    print("parse_tags ->", prompt_store.parse_tags(" docs, C15, docs, contract "))
    print(
        "tags_from_json ->",
        prompt_store.tags_from_json('["documentation", 15, null]'),
    )
    print(
        "normalized hash prefix ->",
        prompt_store.normalized_content_hash("  C15 docs\r\n")[:12],
    )
    print("resolved default path ->", prompt_store.resolve_db_path())

    section("4. Verify the persistence boundary stayed untouched")
    predict("Did importing definitions and calling pure helpers create the database?")
    database_existed_after = database_path.exists()
    print("database existed before ->", database_existed_before)
    print("database exists after ->", database_existed_after)
    print("existence state unchanged ->", database_existed_before == database_existed_after)
    print(
        "Safety: connect, initialize_database, CRUD, CLI, and GUI entry points "
        "were not called."
    )


if __name__ == "__main__":
    main()
