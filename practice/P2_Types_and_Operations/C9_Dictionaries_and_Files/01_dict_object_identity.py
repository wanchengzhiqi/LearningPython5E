r"""
Dict object identity: literals, binding, key overwrite, and value mutation.

Run:
    python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\01_dict_object_identity.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_binding(name, value):
    print(f"{name:<16} type={type(value).__name__:<8} id={id(value)} repr={value!r}")


def show_mapping(name, mapping):
    print(f"{name}: id={id(mapping)} len={len(mapping)} repr={mapping!r}")
    for key, value in mapping.items():
        print(
            "  key "
            f"type={type(key).__name__:<8} id={id(key)} repr={key!r}"
            " -> value "
            f"type={type(value).__name__:<8} id={id(value)} repr={value!r}"
        )


def main():
    section("1. A dict literal creates one mutable mapping object")
    predict("Do two equal-looking dict literals create the same dict object?")
    source = {"menu.start": "Start", "menu.quit": "Quit"}
    same_contents = {"menu.start": "Start", "menu.quit": "Quit"}
    show_binding("source", source)
    show_binding("same_contents", same_contents)
    print("source == same_contents ->", source == same_contents)
    print("source is same_contents ->", source is same_contents)
    print("Rule: == asks about mapping equality; is asks about object identity.")

    section("2. Assignment binds another name; it does not copy the dict")
    predict("After alias['menu.options'] = 'Options', which name sees the new key?")
    alias = source
    show_binding("source", source)
    show_binding("alias", alias)
    alias["menu.options"] = "Options"
    show_binding("source", source)
    show_binding("alias", alias)
    print("source is alias ->", source is alias)
    print("Rule: assigning a key mutates the shared dict object.")

    section("3. A dict stores references to key objects and value objects")
    predict("If the value is a list, does d[k].append(...) mutate the dict or the list?")
    tags = ["ui", "menu"]
    entry = {"key": "menu.start", "tags": tags}
    show_mapping("entry", entry)
    entry["tags"].append("reviewed")
    print("After entry['tags'].append('reviewed'):")
    show_mapping("entry", entry)
    print("tags ->", tags)
    print("entry['tags'] is tags ->", entry["tags"] is tags)
    print("Rule: the dict still maps 'tags' to the same list; the list object changed.")

    section("4. Rebinding one key is different from mutating the old value object")
    predict("After entry['tags'] = ['final'], what happens to the old list?")
    old_tags = entry["tags"]
    entry["tags"] = ["final"]
    show_mapping("entry", entry)
    print("old_tags ->", old_tags)
    print("entry['tags'] is old_tags ->", entry["tags"] is old_tags)
    print("Rule: d[k] = v changes the mapping slot; it does not edit the old value object.")

    section("5. Assigning an existing key overwrites the value, not the key position")
    predict("Does overwriting 'menu.start' create a second visible key?")
    resources = {}
    resources["menu.start"] = "Start"
    resources["menu.quit"] = "Quit"
    resources["menu.start"] = "Begin"
    show_mapping("resources", resources)
    print("list(resources) ->", list(resources))
    print("Rule: a dict has one entry per equal key; overwriting keeps the insertion position.")


if __name__ == "__main__":
    main()
