r"""
Iteration protocol basics: iter(), next(), StopIteration, and next(default).

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\01_iter_next_stopiteration.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def manual_for(iterable):
    """Teaching replica of a simple for loop."""

    iterator = iter(iterable)
    collected = []
    while True:
        try:
            item = next(iterator)
        except StopIteration:
            break
        collected.append(item.upper())
    return collected


def main():
    section("1. A list is iterable, but it is not its own iterator")
    predict("What does iter(keys) return, and is it the same object as keys?")
    keys = ["menu.start", "menu.quit"]
    iterator = iter(keys)
    print("keys ->", keys)
    print("iter(keys) ->", iterator)
    print("keys is iterator ->", keys is iterator)
    print("iter(iterator) is iterator ->", iter(iterator) is iterator)

    section("2. next() consumes one item at a time")
    predict("Which key is returned by each next(iterator) call?")
    print("first  ->", next(iterator))
    print("second ->", next(iterator))
    try:
        print("third  ->", next(iterator))
    except StopIteration as exc:
        print("third  -> StopIteration", type(exc).__name__)
    print("Rule: exhaustion is signaled by StopIteration, not by returning None.")

    section("3. next(iterator, default) separates exhaustion from real None data")
    predict("If None is a real item, which call sees it and which call sees the default?")
    values = iter([None, "menu.options"])
    print("next(values, '<END>') ->", next(values, "<END>"))
    print("next(values, '<END>') ->", next(values, "<END>"))
    print("next(values, '<END>') ->", next(values, "<END>"))
    print("Correction: None can be data; exhaustion is a protocol event.")

    section("4. for uses the same protocol behind the scenes")
    predict("What would a manual while/next loop collect from keys?")
    print("manual_for(keys) ->", manual_for(keys))
    print("list comprehension ->", [key.upper() for key in keys])
    print("Rule: for hides the try/except StopIteration machinery for you.")


if __name__ == "__main__":
    main()
