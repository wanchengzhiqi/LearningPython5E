r"""
Definition-time defaults, saved default objects, and mutable default state.

Run:
    python practice\P4_Functions_and_Generators\C18_Arguments\03_defaults_and_mutable_default_state.py
"""


definition_events = []


def make_default_options():
    definition_events.append("default object created")
    return {"locale": "en-US", "calls": []}


def build_label(key, options=make_default_options()):
    options["calls"].append(key)
    return {
        "label": f"{options['locale']}:{key}",
        "options": options,
    }


def build_label_safely(key, options=None):
    if options is None:
        options = {"locale": "en-US", "calls": []}
    options["calls"].append(key)
    return {
        "label": f"{options['locale']}:{key}",
        "options": options,
    }


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. The default expression ran when the def statement executed")
    predict("How many default objects exist before build_label is called?")
    print("definition events before calls ->", tuple(definition_events))
    saved_default = build_label.__defaults__[0]
    print("saved default is dictionary ->", isinstance(saved_default, dict))
    print(
        "Rule: executing def evaluated make_default_options() and stored the "
        "resulting object on the function object."
    )

    section("2. Omitting the argument reuses the saved mutable default")
    predict("Will two omitted-argument calls observe one calls list?")
    first = build_label("menu.start")
    second = build_label("menu.quit")
    print(
        "first and second options are same object ->",
        first["options"] is second["options"],
    )
    print("result options is saved default ->", second["options"] is saved_default)
    print("shared call history ->", saved_default["calls"])
    print("definition events after calls ->", tuple(definition_events))
    print(
        "Rule: omission binds the parameter to the saved object; it does not "
        "reevaluate the default expression for every call."
    )

    section("3. An explicit argument replaces the default for that call")
    predict("Does an explicit options dictionary mutate the saved default?")
    explicit_options = {"locale": "ja-JP", "calls": []}
    explicit = build_label("dialog.ok", explicit_options)
    print("explicit label ->", explicit["label"])
    print("explicit object preserved ->", explicit["options"] is explicit_options)
    print("explicit call history ->", explicit_options["calls"])
    print("saved default history unchanged ->", saved_default["calls"])
    print("Rule: the caller can bind the parameter to a different object explicitly.")

    section("4. Create mutable state inside each call when isolation is required")
    predict("Will two safe omitted-argument calls receive distinct dictionaries?")
    safe_first = build_label_safely("settings.audio")
    safe_second = build_label_safely("settings.video")
    print(
        "safe options are distinct ->",
        safe_first["options"] is not safe_second["options"],
    )
    print("first safe history ->", safe_first["options"]["calls"])
    print("second safe history ->", safe_second["options"]["calls"])
    print(
        "Boundary: this API reserves None to mean omitted. If None were a "
        "valid business value, a dedicated sentinel would be needed."
    )


if __name__ == "__main__":
    main()
