"""
repr(), str(), print(), and interactive echo.

Run:
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\02_repr_str_print.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_display(label, value, do_print=True):
    print(f"label          : {label}")
    print(f"type(value)    : {type(value).__name__}")
    print(f"len(value)     : {len(value)}")
    print(f"str(value)     : {str(value)}")
    print(f"repr(value)    : {repr(value)}")
    print(f"repr(str(...)) : {repr(str(value))}")
    print(f"repr(repr(...)): {repr(repr(value))}")
    if do_print:
        print("print(value)   : ", end="")
        print(value)


def main():
    section("1. A string object and its repr display are not the same layer")
    predict("For s = 'sp\\nm', what are len(s), str(s), repr(s), and print(s)?")
    s = "sp\nm"
    show_display("s = 'sp\\nm'", s)
    print("Core rule: interactive echo usually displays repr(expression_result), not print(expression_result).")

    section("2. repr(s) returns a new str object")
    predict("What happens when the result of repr(s) is echoed again?")
    r = repr(s)
    show_display("r = repr(s)", r)
    print("Important: r's content contains quote characters and a backslash-n pair.")
    print("r == s ->", r == s)
    print("len(s), len(r) ->", len(s), len(r))

    section("3. repr chooses a readable representation, not your original source spelling")
    predict("Will Python remember whether you wrote '\\n', '\\x0a', or '\\u000a'?")
    same_newline_values = [
        ("'\\n'", "\n"),
        ("'\\x0a'", "\x0a"),
        ("'\\u000a'", "\u000a"),
    ]
    for source_form, value in same_newline_values:
        print(f"{source_form:<10} -> repr={repr(value):<8} len={len(value)} ord={ord(value)}")
    print("Rule: the str object stores the resulting character, not the exact literal spelling.")

    section("4. print() writes text and returns None")
    predict("What is the return value of print('hello')?")
    result = print("visible text from print()")
    print("repr(result)  :", repr(result))
    print("type(result)  :", type(result).__name__)
    print("Rule: print() is an output action; the call expression itself evaluates to None.")

    section("5. Non-printable characters are safer to inspect with repr()")
    predict("Why should logs often use !r for debugging strange text?")
    bell_text = "HP\aPotion"
    show_display("bell_text = 'HP\\aPotion'", bell_text, do_print=False)
    print("Debug logging often uses f'{value!r}' so invisible characters stay visible.")


if __name__ == "__main__":
    main()
