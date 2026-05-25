"""
Dict copy levels, Counter, defaultdict, and mutable defaults.

Run:
    python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\04_copy_counter_defaultdict.py
"""

import copy
from collections import Counter, defaultdict


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_nested(label, mapping):
    print(f"{label}: outer id={id(mapping)} repr={mapping!r}")
    for key, value in mapping.items():
        print(f"  {key!r}: value id={id(value)} type={type(value).__name__} repr={value!r}")


def main():
    section("1. dict.copy() creates a new outer dict, not new inner values")
    predict("After shallow['tags'].append(...), does original['tags'] change?")
    original = {"key": "menu.start", "tags": ["ui", "menu"]}
    shallow = original.copy()
    shallow["tags"].append("reviewed")
    show_nested("original", original)
    show_nested("shallow", shallow)
    print("original is shallow ->", original is shallow)
    print("original['tags'] is shallow['tags'] ->", original["tags"] is shallow["tags"])
    print("Rule: shallow copy copies the mapping shell, not nested mutable objects.")

    section("2. deepcopy isolates nested mutable objects but may reuse immutable atoms")
    predict("Will deepcopy copy the inner list and the string key value in the same way?")
    deep = copy.deepcopy(original)
    deep["tags"].append("deep-only")
    show_nested("original", original)
    show_nested("deep", deep)
    print("original['tags'] is deep['tags'] ->", original["tags"] is deep["tags"])
    print("original['key'] is deep['key'] ->", original["key"] is deep["key"])
    print("Rule: deepcopy is about isolation of nested mutables; immutable atoms may be shared.")

    section("3. Counter reports duplicates instead of silently removing them")
    predict("Which localization keys appear more than once?")
    keys = ["menu.start", "menu.quit", "menu.start", "debug.empty", "menu.quit"]
    counts = Counter(keys)
    duplicate_keys = {key: count for key, count in counts.items() if count > 1}
    print("keys ->", keys)
    print("counts ->", counts)
    print("duplicate_keys ->", duplicate_keys)
    print("Rule: use Counter when you need to report duplicates, not just remove them.")

    section("4. defaultdict creates missing buckets on access")
    predict("Does grouped['ui'] create a key before append runs?")
    records = [
        ("menu.start", "ui"),
        ("menu.quit", "ui"),
        ("quest.long", "quest"),
    ]
    grouped = defaultdict(list)
    for key, category in records:
        grouped[category].append(key)
    print("grouped ->", dict(grouped))
    print("'missing' in grouped before access ->", "missing" in grouped)
    print("grouped['missing'] ->", grouped["missing"])
    print("'missing' in grouped after access ->", "missing" in grouped)
    print("Rule: defaultdict is useful, but reading a missing key can mutate the mapping.")

    section("5. dict.fromkeys(keys, mutable_value) reuses one value object")
    predict("How many list objects are used as values?")
    rows = dict.fromkeys(["menu.start", "menu.quit", "menu.options"], [])
    rows["menu.start"].append("checked")
    show_nested("rows", rows)
    print("rows['menu.start'] is rows['menu.quit'] ->", rows["menu.start"] is rows["menu.quit"])
    print("Rule: fromkeys uses the same value object for every key; avoid mutable defaults here.")


if __name__ == "__main__":
    main()
