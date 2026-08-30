r"""
Loop late binding and bounded default, factory, and partial comparisons.

Run:
    python practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\04_late_binding_fixes_and_partial_references.py
"""

from functools import partial


def make_labeler(locale):
    def label(key):
        return f"{locale}:{key}"

    return label


def render_label(locale, key):
    return f"{locale}:{key}"


def make_config_labeler(config):
    def label(key):
        return render_label(config["locale"], key)

    return label


def render_from_config(config, key):
    return render_label(config["locale"], key)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    locales = ("en-US", "ja-JP", "fr-FR")

    section("1. Loop-created functions can read one name later")
    predict("Do the three functions remember three independent locale values?")
    late_rules = []
    for locale in locales:
        def label(key):
            return f"{locale}:{key}"

        late_rules.append(label)
    print("results ->", tuple(rule("menu.start") for rule in late_rules))
    print("first and second are distinct functions ->", late_rules[0] is not late_rules[1])
    print(
        "Rule: the functions are distinct objects, but their free name locale "
        "is read when each function is called."
    )

    section("2. A default parameter can save each iteration's object reference")
    predict("Which locale object does each saved_locale default supply later?")
    default_rules = []
    for locale in locales:
        def label(key, saved_locale=locale):
            return f"{saved_locale}:{key}"

        default_rules.append(label)
    print("results ->", tuple(rule("menu.start") for rule in default_rules))
    print("caller can override saved default ->", default_rules[0]("menu.start", "ko-KR"))
    print(
        "Rule: each def execution evaluates its default expression and stores "
        "that object on the new function; the parameter remains overridable."
    )

    section("3. A factory call creates a separate enclosing binding each time")
    predict("Does each make_labeler call isolate one locale binding?")
    factory_rules = tuple(make_labeler(locale) for locale in locales)
    print("results ->", tuple(rule("menu.start") for rule in factory_rules))
    print(
        "Rule: each factory call creates a new locale binding that its returned "
        "function can read later."
    )

    section("4. partial fixes arguments but none of these tools deep-copy objects")
    predict("What does partial save, and what happens if a saved dict is mutated?")
    partial_rules = tuple(partial(render_label, locale) for locale in locales)
    print("partial results ->", tuple(rule("menu.start") for rule in partial_rules))

    shared_config = {"locale": "en-US"}

    def default_config_rule(key, saved_config=shared_config):
        return render_from_config(saved_config, key)

    factory_config_rule = make_config_labeler(shared_config)
    partial_config_rule = partial(render_from_config, shared_config)
    shared_config["locale"] = "ja-JP"
    print(
        "after shared dict mutation ->",
        (
            default_config_rule("menu.quit"),
            factory_config_rule("menu.quit"),
            partial_config_rule("menu.quit"),
        ),
    )
    print(
        "Boundary: defaults, closures, and partial save object references; none "
        "of them automatically shallow-copies or deep-copies a mutable object."
    )


if __name__ == "__main__":
    main()
