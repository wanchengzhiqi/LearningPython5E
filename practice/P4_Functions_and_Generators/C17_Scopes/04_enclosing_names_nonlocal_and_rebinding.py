r"""
Enclosing names, shared mutation, local shadowing, and nonlocal rebinding.

Run:
    python practice\P4_Functions_and_Generators\C17_Scopes\04_enclosing_names_nonlocal_and_rebinding.py
"""


module_locale = "module locale"


def make_scope_controls(initial_locale):
    locale = initial_locale
    events = []

    def snapshot():
        return locale, tuple(events)

    def append_event(event):
        events.append(event)

    def shadow_locale(new_locale):
        locale = new_locale
        return locale

    def change_locale(new_locale):
        nonlocal locale
        previous = locale
        locale = new_locale
        return previous, locale

    return snapshot, append_event, shadow_locale, change_locale


def nearest_enclosing_demo():
    label = "outer"

    def middle():
        label = "middle"

        def change():
            nonlocal label
            label = "changed middle"

        change()
        return label

    return label, middle()


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    snapshot, append_event, shadow_locale, change_locale = make_scope_controls(
        "en-US"
    )

    section("1. A nested function can read enclosing bindings")
    predict("What state does snapshot() obtain from the outer call?")
    print("initial snapshot ->", snapshot())
    print("module locale ->", module_locale)
    print("Rule: locale and events are resolved in the enclosing function scope.")

    section("2. Mutating an enclosing object does not require nonlocal")
    predict("Does appending to events rebind the enclosing name?")
    append_result = append_event("scan:start")
    print("append result is None ->", append_result is None)
    print("snapshot after append ->", snapshot())
    print("Rule: the list changes; the enclosing name still refers to that list.")

    section("3. Local shadowing and nonlocal rebinding are different")
    predict("Which call changes the locale seen by snapshot()?")
    print("shadow call result ->", shadow_locale("local shadow"))
    print("snapshot after shadow ->", snapshot())
    print("nonlocal transition ->", change_locale("fr-FR"))
    print("snapshot after nonlocal ->", snapshot())
    print("module locale unchanged ->", module_locale)
    print(
        "Rule: shadow_locale binds a local name; nonlocal redirects the "
        "binding operation to the enclosing function scope."
    )

    section("4. nonlocal targets the nearest enclosing function binding")
    predict("Does changing middle.label also change outer.label?")
    outer_label, middle_label = nearest_enclosing_demo()
    print("outer label ->", outer_label)
    print("middle label after nonlocal ->", middle_label)
    print(
        "Boundary: nonlocal does not target the module namespace or change "
        "object ownership; complex closure state belongs to C19."
    )


if __name__ == "__main__":
    main()
