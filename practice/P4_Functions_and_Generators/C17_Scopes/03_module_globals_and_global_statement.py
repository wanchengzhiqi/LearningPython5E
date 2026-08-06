r"""
Module-global bindings, shared-object mutation, and the global statement.

Run:
    python practice\P4_Functions_and_Generators\C17_Scopes\03_module_globals_and_global_statement.py
"""


active_locale = "en-US"
audit_events = []


def read_locale():
    return active_locale


def append_event(event):
    audit_events.append(event)
    return len(audit_events)


def change_locale(new_locale):
    global active_locale
    previous = active_locale
    active_locale = new_locale
    return previous, active_locale


def replace_event_log(new_events):
    global audit_events
    previous = audit_events
    audit_events = list(new_events)
    return previous, audit_events


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Reading a module-global name does not require global")
    predict("Which namespace supplies active_locale to read_locale()?")
    print("read locale ->", read_locale())
    print("active_locale in module globals ->", "active_locale" in globals())
    print("Rule: global here means the namespace of this module.")

    section("2. Mutating a found shared object does not rebind its name")
    predict("Does list.append() require a global declaration?")
    append_result = append_event("scan:start")
    print("returned event count ->", append_result)
    print("module event log ->", audit_events)
    print(
        "Rule: append_event reads audit_events, then mutates the list object; "
        "it does not rebind the module name."
    )

    section("3. global redirects binding operations to the module namespace")
    predict("Which module bindings change in these two calls?")
    previous_locale, current_locale = change_locale("ja-JP")
    old_events, current_events = replace_event_log(["scan:reset"])
    print("locale transition ->", (previous_locale, current_locale))
    print("module locale now ->", active_locale)
    print("old event object ->", old_events)
    print("module event log now ->", audit_events)
    print("module log is returned current object ->", audit_events is current_events)
    print("Rule: global changes the target binding, not the kind of object.")

    section("4. A module global is not a universal cross-module variable")
    predict("Does global make an object belong to every imported module?")
    print("current module name ->", __name__)
    print("selected module-global keys exist ->", all(
        name in globals() for name in ("active_locale", "audit_events")
    ))
    print(
        "Boundary: each module has its own global namespace; cross-module "
        "imports and architecture are not replaced by a global declaration."
    )


if __name__ == "__main__":
    main()
