r"""
Comparison results, equality, identity, and membership tests.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\03_comparisons_identity_and_membership.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Comparisons produce bool objects")
    predict("What are the result types of ==, !=, <, and in?")
    results = {
        "3 == 3": 3 == 3,
        "3 != 4": 3 != 4,
        "3 < 4": 3 < 4,
        "'ui' in ['ui']": "ui" in ["ui"],
    }
    for expression, result in results.items():
        print(f"{expression:<22} -> {result!r:<5} type={type(result).__name__}")

    section("2. Equality and identity answer different questions")
    predict("Which pair is equal, and which pair names the same list object?")
    left = ["menu.start"]
    equal_but_distinct = ["menu.start"]
    alias = left
    print("left == equal_but_distinct ->", left == equal_but_distinct)
    print("left is equal_but_distinct ->", left is equal_but_distinct)
    print("left == alias ->", left == alias)
    print("left is alias ->", left is alias)
    print("Rule: == asks about equality; is asks about object identity.")

    section("3. Use is for identity sentinels such as None")
    predict("Which tests distinguish None from other falsy values?")
    for value in (None, "", 0, [], False):
        print(
            f"value={value!r:<6} value is None -> {value is None!r:<5} "
            f"not value -> {not value!r}"
        )
    print("Correction: falsy does not mean identical to None or False.")

    section("4. Dict membership tests keys by default")
    predict("Are dict values found by using value in mapping?")
    resources = {
        "menu.start": "Start Game",
        "menu.quit": "Quit",
    }
    print("'menu.start' in resources ->", "menu.start" in resources)
    print("'Start Game' in resources ->", "Start Game" in resources)
    print("'Start Game' in resources.values() ->", "Start Game" in resources.values())
    print("'menu.options' not in resources ->", "menu.options" not in resources)

    section("5. Membership follows the chosen container's protocol")
    predict("How do string, list, and set membership differ in meaning?")
    text = "menu.start"
    ordered_keys = ["menu.start", "menu.quit"]
    allowed_modes = {"text", "json"}
    print("'start' in text ->", "start" in text)
    print("'menu.quit' in ordered_keys ->", "menu.quit" in ordered_keys)
    print("'json' in allowed_modes ->", "json" in allowed_modes)

    section("6. Do not use is for ordinary business-value comparison")
    predict("Which operator expresses the intended locale-code comparison?")
    configured_locale = "".join(["zh", "_CN"])
    expected_locale = "zh_CN"
    print("configured_locale == expected_locale ->", configured_locale == expected_locale)
    print("configured_locale is expected_locale ->", configured_locale is expected_locale)
    print("Rule: business values should normally be compared with ==, not is.")


if __name__ == "__main__":
    main()
