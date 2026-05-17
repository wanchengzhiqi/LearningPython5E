"""
List object identity: list literals, name binding, equality, and display.

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\01_list_object_identity.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_binding(name, value):
    print(f"{name:<14} type={type(value).__name__:<6} id={id(value)} repr={value!r}")


def show_list_elements(name, values):
    print(f"{name}: outer id={id(values)} len={len(values)} repr={values!r}")
    for index, item in enumerate(values):
        print(f"  [{index}] type={type(item).__name__:<6} id={id(item)} repr={item!r}")


def main():
    section("1. A list literal creates one mutable container object")
    predict("Do two equal-looking list literals create the same list object?")
    items = ["menu.start", "item.potion", "dialog.warning"]
    same_contents = ["menu.start", "item.potion", "dialog.warning"]
    show_binding("items", items)
    show_binding("same_contents", same_contents)
    print("items == same_contents ->", items == same_contents)
    print("items is same_contents ->", items is same_contents)
    print("Rule: == asks about value equality; is asks about object identity.")

    section("2. Assignment binds another name; it does not copy the list")
    predict("After alias.append(...), which name sees the new element?")
    alias = items
    show_binding("items", items)
    show_binding("alias", alias)
    print("alias is items before append ->", alias is items)
    append_result = alias.append("system.quit")
    print("append_result ->", append_result)
    show_binding("items", items)
    show_binding("alias", alias)
    print("alias is items after append ->", alias is items)
    print("Rule: append mutates the shared list object and returns None.")

    section("3. Container display uses element repr-style text")
    predict("Does a list containing a newline store backslash-n or a real newline?")
    text_items = ["Line 1\nLine 2", "C:\\game\\text.txt", ""]
    show_list_elements("text_items", text_items)
    print("print(text_items) ->", text_items)
    print("print(text_items[0]) ->")
    print(text_items[0])
    print("Rule: list display uses repr(element); the element object itself is unchanged.")

    section("4. A list stores references to element objects")
    predict("If the same inner list is stored twice, how many inner list objects exist?")
    tag_bucket = ["ui"]
    rows = [tag_bucket, tag_bucket]
    show_list_elements("rows", rows)
    rows[0].append("reviewed")
    print("After rows[0].append('reviewed'):")
    show_list_elements("rows", rows)
    print("rows[0] is rows[1] ->", rows[0] is rows[1])
    print("Rule: the outer list has two slots, but both slots can reference one object.")


if __name__ == "__main__":
    main()
