"""
set: unordered unique collection plus set algebra.

Run:
    python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\04_sets.py
"""


def show(title, value):
    print(f"{title:<36} -> {value!r} ({type(value).__name__})")


def predict(question):
    print(f"[Predict] {question}")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main():
    section("1. set removes duplicates and has no position semantics")
    predict("What remains after duplicates are removed? Can you predict the display order?")
    terms = ["HP", "MP", "HP", "STR", "DEX", "MP"]
    unique_terms = set(terms)
    show("terms", terms)
    show("set(terms)", unique_terms)
    show("sorted(set(terms))", sorted(unique_terms))
    print("A set is not a sequence: do not rely on display order.")

    section("2. set algebra maps directly to real problems")
    predict("Which localization keys are missing, extra, done, or changed on only one side?")
    source_keys = {"menu.start", "menu.exit", "item.potion", "item.elixir"}
    translated_keys = {"menu.start", "item.potion", "unused.debug"}
    show("source_keys - translated_keys", source_keys - translated_keys)
    show("translated_keys - source_keys", translated_keys - source_keys)
    show("source_keys & translated_keys", source_keys & translated_keys)
    show("source_keys | translated_keys", source_keys | translated_keys)
    show("source_keys ^ translated_keys", source_keys ^ translated_keys)

    section("3. mutability and hashability")
    predict("Why can frozenset be an element, but list cannot?")
    show("{1, 2, 3}", {1, 2, 3})
    show("frozenset({1, 2})", frozenset({1, 2}))
    show("{frozenset({1, 2})}", {frozenset({1, 2})})
    show("set([1, True, 1.0])", set([1, True, 1.0]))
    print("Set elements must be hashable. list is mutable, so it cannot be a set element.")
    print("Caution: 1, True, and 1.0 compare equal and share hash behavior, so a set keeps one of them.")

    section("4. Membership checks express intent clearly")
    predict("Is membership testing a clearer intention than chained equality checks?")
    allowed_modes = {"safe_mod", "runtime_mod", "dev_mod"}
    mode = "runtime_mod"
    show("mode in allowed_modes", mode in allowed_modes)
    show("'debug_mod' in allowed_modes", "debug_mod" in allowed_modes)


if __name__ == "__main__":
    main()
