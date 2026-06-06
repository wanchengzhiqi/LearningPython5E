r"""
Expressions, expression statements, return values, and side effects.

Run:
    python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\01_expressions_statements_and_side_effects.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_binding(name, value):
    print(f"{name:<18} type={type(value).__name__:<10} id={id(value)} repr={value!r}")


def main():
    section("1. An expression is evaluated to produce a value object")
    predict("Does 'menu.' + 'start' create a str object, print text, or both?")
    menu_key = "menu." + "start"
    show_binding("menu_key", menu_key)
    print("Rule: the expression produced a str object; printing is a separate action.")

    section("2. An expression statement can discard the expression value")
    predict("Will the next expression statement auto-display MENU.START in a script?")
    "menu.start".upper()
    print("No automatic echo appeared above.")
    print("Rule: a script executes the expression statement, then discards its value.")

    section("3. A function call expression can return a value and cause side effects")
    predict("What is the return value of print('visible output')?")
    result = print("visible output from print()")
    show_binding("result", result)
    print("Rule: print() wrote text to stdout as a side effect and returned None.")

    section("4. A method call can mutate an object while returning None")
    predict("After keys.append('menu.quit'), what changed: the list or the return value?")
    keys = ["menu.start"]
    append_result = keys.append("menu.quit")
    show_binding("append_result", append_result)
    show_binding("keys", keys)
    print("Rule: list.append() mutates the list object and returns None.")

    section("5. A value-producing expression may have no external side effect")
    predict("Does sorted(keys) mutate keys, or return a new list?")
    sorted_keys = sorted(keys)
    show_binding("keys", keys)
    show_binding("sorted_keys", sorted_keys)
    print("keys is sorted_keys ->", keys is sorted_keys)
    print("Rule: return value, mutation, and output are three separate questions.")


if __name__ == "__main__":
    main()
