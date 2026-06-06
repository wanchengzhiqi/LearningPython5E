r"""
Dict methods, view objects, and method return values.

Run:
    python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\03_methods_views_and_returns.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_mapping(name, mapping):
    print(f"{name}: id={id(mapping)} len={len(mapping)} repr={mapping!r}")


def main():
    section("1. get() reads without creating a new key")
    predict("Does d.get('missing', []) mutate the dict?")
    issues_by_key = {"menu.start": ["too long"]}
    result = issues_by_key.get("menu.quit", [])
    show_mapping("issues_by_key", issues_by_key)
    print("result ->", result)
    print("'menu.quit' in issues_by_key ->", "menu.quit" in issues_by_key)
    print("Rule: get() returns a value or default; it does not insert the default.")

    section("2. setdefault() can insert and returns the stored value object")
    predict("After setdefault(...).append(...), what object changed?")
    bucket = issues_by_key.setdefault("menu.quit", [])
    append_result = bucket.append("missing translation")
    show_mapping("issues_by_key", issues_by_key)
    print("bucket ->", bucket)
    print("append_result ->", append_result)
    print("issues_by_key['menu.quit'] is bucket ->", issues_by_key["menu.quit"] is bucket)
    print("Rule: setdefault may mutate the dict, then returns the actual stored value.")

    section("3. update() mutates the dict and returns None")
    predict("What does update_result contain?")
    patch = {"menu.options": "Options", "menu.start": "Begin"}
    resources = {"menu.start": "Start", "menu.quit": "Quit"}
    update_result = resources.update(patch)
    show_mapping("resources", resources)
    print("update_result ->", update_result)
    print("Rule: update() modifies the target mapping; the return value is None.")

    section("4. pop() mutates the dict and returns the removed value")
    predict("What is returned by pop() when the key exists or is missing with a default?")
    removed = resources.pop("menu.quit")
    missing = resources.pop("menu.missing", "<not found>")
    show_mapping("resources", resources)
    print("removed ->", removed)
    print("missing ->", missing)
    print("Rule: pop() is both a mutation and a value-producing operation.")

    section("5. keys(), values(), and items() are live views, not list snapshots")
    predict("Will key_view change after adding a new key?")
    key_view = resources.keys()
    item_view = resources.items()
    key_snapshot = list(resources.keys())
    print("before key_view ->", key_view)
    print("before item_view ->", item_view)
    print("before key_snapshot ->", key_snapshot)
    resources["system.exit"] = "Exit"
    print("after key_view ->", key_view)
    print("after item_view ->", item_view)
    print("after key_snapshot ->", key_snapshot)
    print("Rule: a view tracks the dict; list(...) creates a separate snapshot.")


if __name__ == "__main__":
    main()
