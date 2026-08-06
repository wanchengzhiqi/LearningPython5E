r"""
Free names and the minimal closure entry model.

Run:
    python practice\P4_Functions_and_Generators\C17_Scopes\05_free_names_and_closure_entry.py
"""


def make_key_formatter(prefix):
    normalized_prefix = prefix.strip().lower()

    def format_key(key):
        normalized_key = key.strip().lower()
        return f"{normalized_prefix}.{normalized_key}"

    return format_key


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. An outer call can return its inner function object")
    predict("Does creating the formatter also format a localization key?")
    caller_prefix = " MENU "
    menu_formatter = make_key_formatter(caller_prefix)
    print("formatter is callable ->", callable(menu_formatter))
    print("formatter name ->", menu_formatter.__name__)
    print("caller prefix ->", caller_prefix)
    print("Rule: the outer call returns a function object; no key call happened yet.")

    section("2. A free name can still resolve after the outer call returned")
    predict("Where does format_key obtain normalized_prefix?")
    print("formatted key ->", menu_formatter(" Start "))
    print(
        "Rule: normalized_prefix is not local to format_key or module-global; "
        "the inner function resolves it from its preserved enclosing context."
    )

    section("3. Separate outer calls preserve separate enclosing bindings")
    predict("Will two formatters share one prefix binding?")
    dialog_formatter = make_key_formatter(" DIALOG ")
    print("menu key ->", menu_formatter(" Quit "))
    print("dialog key ->", dialog_formatter(" Confirm "))
    print("menu formatter still uses menu ->", menu_formatter(" Options "))
    print("Rule: each outer call establishes its own enclosing state.")

    section("4. Closure entry stays deliberately narrow in C17")
    predict("Does this experiment teach loop late binding or callback design?")
    caller_prefix = "changed caller binding"
    print("caller prefix rebound ->", caller_prefix)
    print("existing formatter result ->", menu_formatter(" Accessibility "))
    print(
        "Boundary: C17 establishes free-name resolution and persistence only; "
        "late binding, callbacks, and higher-order composition belong to C19."
    )


if __name__ == "__main__":
    main()
