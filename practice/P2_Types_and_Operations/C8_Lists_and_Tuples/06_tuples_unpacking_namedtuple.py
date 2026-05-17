"""
Tuples, commas, immutability boundaries, unpacking, *args, and namedtuple.

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\06_tuples_unpacking_namedtuple.py
"""

from collections import namedtuple


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(name, value):
    print(f"{name:<18} type={type(value).__name__:<12} id={id(value)} repr={value!r}")


def split_key(key):
    namespace, name = key.split(".", 1)
    return namespace, name


def describe_args(*args):
    print("*args type ->", type(args).__name__)
    print("*args repr ->", args)
    return args


def main():
    section("1. The comma creates a tuple; parentheses only group")
    predict("Which expressions below create tuples?")
    value = (1)
    single = (1,)
    no_parens = "menu.start", "Start", "Start Game"
    empty = ()
    show("value", value)
    show("single", single)
    show("no_parens", no_parens)
    show("empty", empty)
    print("Rule: (1) is just grouped integer 1; (1,) is a one-element tuple.")

    section("2. Tuple immutability means tuple slots cannot be replaced")
    predict("Can a list stored inside a tuple still be mutated?")
    record = ("menu.start", "Start", "Start Game", ["ui"])
    show("record before", record)
    try:
        record[1] = "Begin"
    except TypeError as error:
        print("record[1] = 'Begin' -> TypeError:", error)
    record[3].append("reviewed")
    show("record after", record)
    print("Rule: the tuple still stores the same list reference; the list object changed.")

    section("3. Sequence unpacking binds names to elements")
    predict("What objects do key, source, translation, and tags bind to?")
    key, source, translation, tags = record
    show("key", key)
    show("source", source)
    show("translation", translation)
    show("tags", tags)
    print("tags is record[3] ->", tags is record[3])

    section("4. Extended unpacking collects into a new list")
    predict("Is middle a tuple or a list?")
    first, *middle, last = ["start", "load", "settings", "quit"]
    show("first", first)
    show("middle", middle)
    show("last", last)
    print("Rule: in assignment, the starred target collects items into a list.")

    section("5. Multiple return values are usually one tuple object")
    predict("What does split_key return before unpacking?")
    result = split_key("item.potion")
    show("result", result)
    namespace, name = result
    show("namespace", namespace)
    show("name", name)
    print("Rule: return namespace, name returns a tuple that can be unpacked.")

    section("6. *args collects positional arguments into a tuple")
    predict("What type is args inside describe_args?")
    args = describe_args("menu.start", "item.potion", "dialog.warning")
    show("args returned", args)

    section("7. namedtuple gives names to tuple positions")
    predict("Does namedtuple make the record mutable?")
    LocalizedRecord = namedtuple("LocalizedRecord", "key source translation tags")
    item = LocalizedRecord("item.potion", "Potion", "Potion", ("item", "shop"))
    show("item", item)
    print("item.key ->", item.key)
    print("item[0] ->", item[0])
    changed = item._replace(translation="HP Potion")
    show("changed", changed)
    show("item", item)
    print("Rule: _replace returns a new namedtuple; it does not mutate the old one.")


if __name__ == "__main__":
    main()
