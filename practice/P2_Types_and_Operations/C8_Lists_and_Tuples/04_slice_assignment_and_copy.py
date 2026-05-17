"""
Slice assignment, rebinding, shallow copy, and deep copy.

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\04_slice_assignment_and_copy.py
"""

import copy


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(name, value):
    print(f"{name:<16} id={id(value)} repr={value!r}")


def show_layers(name, values):
    print(f"{name}: outer id={id(values)} repr={values!r}")
    for index, item in enumerate(values):
        print(f"  [{index}] inner id={id(item)} repr={item!r}")


def main():
    section("1. Slice assignment mutates the existing list")
    predict("Will alias see a slice assignment made through items?")
    items = ["start", "load", "quit"]
    alias = items
    show("items before", items)
    show("alias before", alias)
    items[1:2] = ["settings", "save"]
    show("items after", items)
    show("alias after", alias)
    print("alias is items ->", alias is items)
    print("Rule: items[1:2] = ... changes the list object itself.")

    section("2. Rebinding a name does not mutate the old list")
    predict("After items = ['new'], what does alias still reference?")
    old_items = items
    items = ["new"]
    show("items rebound", items)
    show("old_items", old_items)
    show("alias", alias)
    print("alias is old_items ->", alias is old_items)
    print("items is alias ->", items is alias)
    print("Rule: assignment changes what the name points at; it does not rewrite aliases.")

    section("3. Whole-slice assignment keeps identity but replaces contents")
    predict("Can you replace all list contents without rebinding the name?")
    current = ["a", "b", "c"]
    watcher = current
    show("current before", current)
    current[:] = ["x", "y"]
    show("current after", current)
    show("watcher", watcher)
    print("watcher is current ->", watcher is current)
    print("Rule: current[:] = ... is a clear in-place replacement of contents.")

    section("4. Shallow copies create a new outer list only")
    predict("Which copied lists share the same inner lists?")
    original = [["menu.start"], ["item.potion"]]
    via_slice = original[:]
    via_list = list(original)
    via_copy = copy.copy(original)
    deep = copy.deepcopy(original)
    show_layers("original", original)
    show_layers("via_slice", via_slice)
    show_layers("via_list", via_list)
    show_layers("via_copy", via_copy)
    show_layers("deep", deep)

    original[0].append("shared-change")
    print("After original[0].append('shared-change'):")
    show_layers("original", original)
    show_layers("via_slice", via_slice)
    show_layers("via_list", via_list)
    show_layers("via_copy", via_copy)
    show_layers("deep", deep)
    print("Rule: shallow copy protects the outer container, not nested mutable objects.")


if __name__ == "__main__":
    main()
