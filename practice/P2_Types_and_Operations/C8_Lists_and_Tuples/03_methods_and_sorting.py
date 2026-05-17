"""
List methods and sorting: return values versus mutated objects.

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\03_methods_and_sorting.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(name, value):
    print(f"{name:<18} id={id(value)} type={type(value).__name__:<8} repr={value!r}")


def main():
    section("1. append and extend mutate the target list and return None")
    predict("What value should you store from items.append('quit')?")
    items = ["start", "load"]
    show("items before", items)
    append_result = items.append("quit")
    extend_result = items.extend(["settings", "credits"])
    show("append_result", append_result)
    show("extend_result", extend_result)
    show("items after", items)
    print("Rule: do not write items = items.append(x); you would bind items to None.")

    section("2. insert, remove, reverse, and clear are also in-place operations")
    predict("Which operations return useful values, and which return None?")
    menu = ["start", "debug", "load", "quit"]
    insert_result = menu.insert(1, "settings")
    remove_result = menu.remove("debug")
    reverse_result = menu.reverse()
    show("menu", menu)
    show("insert_result", insert_result)
    show("remove_result", remove_result)
    show("reverse_result", reverse_result)
    popped = menu.pop()
    show("popped", popped)
    show("menu after pop", menu)
    print("Rule: pop returns the removed element; most mutating methods return None.")

    section("3. sort mutates the list; sorted creates a new list")
    predict("Does records.sort(...) create a new sorted list?")
    records = [
        ("item.potion", 5),
        ("menu.start", 1),
        ("dialog.warning", 20),
    ]
    observer = records
    show("records before", records)
    sort_result = records.sort(key=lambda record: record[1])
    show("sort_result", sort_result)
    show("records after", records)
    show("observer", observer)
    print("observer is records ->", observer is records)

    by_key = sorted(records, key=lambda record: record[0])
    show("by_key", by_key)
    show("records final", records)
    print("by_key is records ->", by_key is records)
    print("Rule: list.sort() is in-place; sorted(iterable) returns a new list.")

    section("4. Sorting strings is display-independent")
    predict("Does sorting change the string objects inside the list?")
    labels = ["line\\ntext", "alpha", "Quest"]
    before_ids = [id(label) for label in labels]
    labels.sort(key=str.casefold)
    after_ids = [id(label) for label in labels]
    show("labels", labels)
    print("ids before sort ->", before_ids)
    print("ids after sort  ->", after_ids)
    print("Rule: sorting reorders references in the list; it does not rewrite strings.")


if __name__ == "__main__":
    main()
