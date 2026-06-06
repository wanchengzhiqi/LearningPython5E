r"""
Core type synthesis for the end of Types and Operations.

Run:
    python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\06_core_type_synthesis.py
"""

import json
from pathlib import Path


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def can_hash(value):
    try:
        hash(value)
        return True
    except TypeError:
        return False


def show_row(name, value, role):
    print(
        f"{name:<10} type={type(value).__name__:<12} "
        f"len={len(value) if hasattr(value, '__len__') else 'n/a':<3} "
        f"hashable={can_hash(value)!s:<5} repr={value!r} role={role}"
    )


def main():
    section("1. Core object types are chosen by behavior, not by habit")
    predict("Which objects are mutable, ordered, hashable, or file-boundary tools?")
    rows = [
        ("int", 42, "numeric count, score, length limit"),
        ("str", "menu.start", "text, key, display, JSON string"),
        ("list", ["menu.start", "menu.quit"], "ordered mutable work collection"),
        ("tuple", ("menu.start", "Start"), "stable positional record"),
        ("dict", {"menu.start": "Start"}, "mapping from key to value"),
        ("set", {"menu.start", "menu.quit"}, "membership and difference checks"),
    ]
    for name, value, role in rows:
        show_row(name, value, role)
    print("Rule: choose a type by operation needs: order, mutation, lookup, uniqueness, boundary.")

    section("2. JSON supports only a smaller data model than Python")
    predict("Can every Python object be directly serialized as JSON?")
    payload = {
        "keys": ["menu.start", "menu.quit"],
        "unique_keys": {"menu.start", "menu.quit"},
        "record": ("menu.start", "Start"),
    }
    try:
        json.dumps(payload)
    except TypeError as error:
        print("json.dumps(payload) -> TypeError:", error)
    serializable_payload = {
        "keys": payload["keys"],
        "unique_keys": sorted(payload["unique_keys"]),
        "record": list(payload["record"]),
    }
    print("json.dumps(serializable_payload) ->", json.dumps(serializable_payload, ensure_ascii=False))
    print("Rule: convert set, namedtuple, custom objects, and other internals before JSON output.")

    section("3. File objects are handles to external data, not the data itself")
    predict("Is a file object the same thing as the path or the text inside the file?")
    path = Path(__file__)
    with path.open("r", encoding="utf-8") as file:
        first_line = file.readline()
        print("path type ->", type(path).__name__, "repr ->", repr(str(path)))
        print("file type ->", type(file).__name__, "closed ->", file.closed)
        print("first_line type ->", type(first_line).__name__, "repr ->", repr(first_line))
    print("file closed after with ->", file.closed)
    print("Rule: path, file object, text content, and bytes content are separate layers.")


if __name__ == "__main__":
    main()
