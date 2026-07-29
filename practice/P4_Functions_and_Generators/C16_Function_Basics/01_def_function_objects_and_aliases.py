r"""
Function objects, definition names, aliases, and calls.

Run:
    python practice\P4_Functions_and_Generators\C16_Function_Basics\01_def_function_objects_and_aliases.py
"""


def format_key(key):
    print(f"body effect -> formatting {key!r}")
    return key.strip().lower()


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Executing def creates a function object")
    predict("Has format_key's body run merely because the function exists?")
    print("type(format_key).__name__ ->", type(format_key).__name__)
    print("callable(format_key) ->", callable(format_key))
    print("format_key.__name__ ->", format_key.__name__)
    print("Observation: no 'body effect' line has appeared yet.")

    section("2. Other names and containers can hold the same function object")
    predict("Do alias and registry create copies of the function object?")
    alias = format_key
    registry = {"format": format_key}
    print("alias is format_key ->", alias is format_key)
    print("registry['format'] is format_key ->", registry["format"] is format_key)
    print("Rule: assignment stores another reference; it does not call or copy.")

    section("3. Parentheses perform a call and produce a result object")
    predict("Which line first executes the function body?")
    result = alias(" MENU.Start ")
    print("result ->", result)
    print("type(result).__name__ ->", type(result).__name__)
    print("format_key is result ->", format_key is result)
    print("Rule: function, function alias, call expression, and result differ.")

    section("4. First-class observation stays limited in C16")
    predict("Does storing a function in a dictionary require callback design?")
    selected = registry["format"]
    selected_result = selected(" MENU.Quit ")
    print("selected is format_key ->", selected is format_key)
    print("selected result ->", selected_result)
    print("Boundary: C16 observes storage and calling, not higher-order design.")


if __name__ == "__main__":
    main()
