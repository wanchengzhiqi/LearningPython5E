r"""
Physical lines, logical lines, semicolons, and indentation blocks.

Run:
    python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\03_logical_lines_and_blocks.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Parentheses allow one logical line to span physical lines")
    predict("Is this list literal one object even though it uses several physical lines?")
    menu_keys = [
        "menu.start",
        "menu.options",
        "menu.quit",
    ]
    print("menu_keys ->", menu_keys)
    print("Rule: brackets, parentheses, and braces allow implicit continuation.")

    section("2. Backslash continuation works, but it is fragile")
    predict("What value does this continued expression produce?")
    total_name_length = len("menu.start") + \
        len("menu.quit")
    print("total_name_length ->", total_name_length)
    print("Rule: prefer parentheses when possible; trailing spaces can break backslashes.")

    section("3. A semicolon can put two simple statements on one logical line")
    predict("Does the semicolon create a tuple, a list, or just separate statements?")
    first_key = "menu.start"; second_key = "menu.quit"
    print("first_key ->", first_key)
    print("second_key ->", second_key)
    print("Rule: semicolons separate simple statements; they do not create containers.")

    section("4. Indentation is syntax, not decoration")
    predict("Will inside_block be created when enter_block is True?")
    enter_block = True
    if enter_block:
        inside_block = ["created by an executed statement"]
        print("The indented block was entered.")
    print("inside_block ->", inside_block)
    print("Rule: the indented suite belongs to the if statement syntactically.")

    section("5. A block is not a runtime container object")
    predict("Will skipped_name exist after a skipped block?")
    enter_block = False
    if enter_block:
        skipped_name = "this assignment did not run"
    print("'skipped_name' in locals() ->", "skipped_name" in locals())
    print("Rule: a block is source structure; names appear only if statements execute.")


if __name__ == "__main__":
    main()
