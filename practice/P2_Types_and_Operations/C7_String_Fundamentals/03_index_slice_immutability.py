"""
String indexing, slicing, negative indexes, step, and immutability.

Run:
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\03_index_slice_immutability.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(title, value):
    print(f"{title:<30} -> {value!r} ({type(value).__name__})")


def explain_slice(text, start, stop, step=None):
    current_slice = slice(start, stop, step)
    normalized = current_slice.indices(len(text))
    result = text[current_slice]
    print(f"text[{start}:{stop}:{step}] -> {result!r:<12} normalized={normalized}")


def main():
    text = "Python"

    section("1. Indexing returns a one-character str")
    predict("What are text[0], text[-1], and their types?")
    show("text", text)
    show("text[0]", text[0])
    show("text[-1]", text[-1])
    show("type(text[0])", type(text[0]))
    print("Rule: indexing a str returns another str whose length is 1.")

    section("2. Slicing describes a range, not a single item access")
    predict("Before running, draw the boundaries around P y t h o n.")
    explain_slice(text, 0, 2)
    explain_slice(text, 2, 5)
    explain_slice(text, None, 3)
    explain_slice(text, 3, None)
    explain_slice(text, None, None)
    explain_slice(text, 99, 200)
    print("Rule: out-of-range slicing is allowed; out-of-range indexing is not.")
    try:
        print(text[99])
    except IndexError as exc:
        print("text[99] ->", type(exc).__name__, str(exc))

    section("3. Empty slices are normal results")
    predict("Which of these slices produce an empty string?")
    explain_slice(text, 3, 3)
    explain_slice(text, 4, 2)
    explain_slice(text, -2, 1)
    print("Rule: with a positive step, start at or to the right of stop gives ''.")

    section("4. Step and reverse slicing")
    predict("What does text[::-1] produce, and why?")
    explain_slice(text, None, None, 2)
    explain_slice(text, 1, None, 2)
    explain_slice(text, None, None, -1)
    explain_slice(text, 4, 1, -1)
    explain_slice(text, None, None, -2)

    section("5. Strings are immutable; apparent modification creates a new object")
    predict("Can text[0] = 'J' modify the existing string object?")
    try:
        text[0] = "J"
    except TypeError as exc:
        print("text[0] = 'J' ->", type(exc).__name__, str(exc))
    new_text = "J" + text[1:]
    show("text", text)
    show("new_text", new_text)
    print("text is new_text ->", text is new_text)
    print("Rule: build a new string, then bind a name to that new object.")

    section("6. Full slicing of immutable strings may reuse the same object")
    predict("Is text[:] guaranteed to be a different object?")
    full = text[:]
    show("full", full)
    print("full == text ->", full == text)
    print("full is text ->", full is text)
    print("Learning rule: equality matters here; object reuse is an implementation optimization.")


if __name__ == "__main__":
    main()
