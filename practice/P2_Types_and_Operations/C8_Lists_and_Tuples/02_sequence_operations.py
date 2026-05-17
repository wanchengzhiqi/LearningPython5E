"""
Sequence operations on lists: indexing, slicing, concatenation, repetition, and +=.

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\02_sequence_operations.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(name, value):
    print(f"{name:<16} id={id(value)} type={type(value).__name__:<5} repr={value!r}")


def main():
    section("1. Indexing retrieves an existing element reference")
    predict("Does items[0] create a new list or retrieve one element?")
    items = ["start", "load", "quit", "credits"]
    first = items[0]
    last = items[-1]
    show("items", items)
    show("first", first)
    show("last", last)
    print("items[0] == 'start' ->", items[0] == "start")
    print("Rule: indexing reads one element; it does not create a new outer list.")

    section("2. Slicing reads a range and creates a new outer list")
    predict("Is items[:] the same list object as items?")
    middle = items[1:3]
    whole = items[:]
    show("items", items)
    show("middle", middle)
    show("whole", whole)
    print("whole == items ->", whole == items)
    print("whole is items ->", whole is items)
    print("Rule: list slicing creates a new outer list when used as an expression.")

    section("3. + and * create new list objects")
    predict("Does items + ['settings'] modify items?")
    combined = items + ["settings"]
    repeated = ["empty"] * 3
    show("items", items)
    show("combined", combined)
    show("repeated", repeated)
    print("combined is items ->", combined is items)
    print("Rule: + and * return new lists; the original list remains bound to items.")

    section("4. += on a list usually mutates the list object in place")
    predict("Will observer see the elements added through items += ...?")
    observer = items
    show("items before", items)
    show("observer before", observer)
    items += ["settings", "gallery"]
    show("items after", items)
    show("observer after", observer)
    print("observer is items ->", observer is items)
    print("Rule: list += extends the existing list, so aliases see the change.")

    section("5. += on a string cannot mutate the string object")
    predict("Does old_text change after text += '!'?")
    text = "Localization"
    old_text = text
    show("text before", text)
    show("old_text", old_text)
    text += "!"
    show("text after", text)
    show("old_text", old_text)
    print("text is old_text ->", text is old_text)
    print("Rule: strings are immutable; text is rebound to a different string object.")


if __name__ == "__main__":
    main()
