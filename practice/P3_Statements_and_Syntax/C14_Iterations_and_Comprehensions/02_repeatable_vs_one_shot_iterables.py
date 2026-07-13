r"""
Repeatable containers versus one-shot iterator objects.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\02_repeatable_vs_one_shot_iterables.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def describe_iter_identity(name, obj):
    first_iterator = iter(obj)
    second_iterator = iter(obj)
    print(
        f"{name:<18} obj_is_iterator={obj is first_iterator!r:<5} "
        f"two_iters_same={first_iterator is second_iterator!r:<5} "
        f"iterator_type={type(first_iterator).__name__}"
    )


def consume_twice(name, obj):
    print(f"{name:<18} first={list(obj)!r} second={list(obj)!r}")


def main():
    section("1. Containers usually create a fresh iterator each time")
    predict("Which objects are iterable but not themselves iterators?")
    keys = ["menu.start", "menu.quit"]
    mapping = {"menu.start": "Start", "menu.quit": "Quit"}
    unique_modes = {"json", "text"}
    locale = "zh_CN"
    for name, obj in [
        ("list", keys),
        ("dict", mapping),
        ("set", unique_modes),
        ("str", locale),
    ]:
        describe_iter_identity(name, obj)
    print("Rule: repeatable means you can ask for a new iterator again.")

    section("2. Repeatable containers can be consumed twice")
    predict("Will the second list(obj) still contain items?")
    consume_twice("list", keys)
    consume_twice("dict keys", mapping)
    consume_twice("str", locale)
    print("Set order is not a business order, so stable reports should sort it:", sorted(unique_modes))

    section("3. zip, map, filter, and generator expressions are one-shot")
    predict("Which second consumption is empty?")
    zipped = zip(["menu.start", "menu.quit"], ["Start", "Quit"])
    mapped = map(str.upper, ["active", "deleted"])
    filtered = filter(lambda key: key.startswith("menu."), ["menu.start", "debug"])
    generated = (key.upper() for key in ["menu.options", "menu.score"])
    for name, obj in [
        ("zip", zipped),
        ("map", mapped),
        ("filter", filtered),
        ("generator", generated),
    ]:
        describe_iter_identity(name, obj)
        consume_twice(name, obj)
    print("Rule: if you need to reuse one-shot data, collect it intentionally once.")


if __name__ == "__main__":
    main()
