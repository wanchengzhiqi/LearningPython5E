r"""
Closure environments, shared state, and isolation between factory calls.

Run:
    python practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\03_closure_environments_sharing_and_factory_isolation.py
"""


def make_tracker(label):
    count = 0
    history = []

    def record(key):
        nonlocal count
        count += 1
        entry = f"{label}:{count}:{key}"
        history.append(entry)
        return entry

    def snapshot():
        return count, tuple(history), history

    return record, snapshot, history


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Returned functions can still read enclosing bindings")
    predict("Can record_menu use label after make_tracker has returned?")
    record_menu, snapshot_menu, external_history = make_tracker("menu")
    print("first record ->", record_menu("start"))
    print("snapshot ->", snapshot_menu()[:2])
    print(
        "Rule: the returned function keeps access to the enclosing bindings "
        "needed by its body."
    )

    section("2. Closures from one factory call can share one environment")
    predict("Do record_menu and snapshot_menu observe the same count and history?")
    print("second record ->", record_menu("quit"))
    count, history_values, observed_history = snapshot_menu()
    print("count ->", count)
    print("history values ->", history_values)
    print("snapshot history is external history ->", observed_history is external_history)
    print(
        "Rule: the two inner functions share bindings created by the same "
        "make_tracker call."
    )

    section("3. A different factory call creates an isolated environment")
    predict("Does a settings tracker continue the menu tracker's count?")
    record_settings, snapshot_settings, settings_history = make_tracker("settings")
    print("settings record ->", record_settings("audio"))
    print("settings snapshot ->", snapshot_settings()[:2])
    print("menu snapshot remains ->", snapshot_menu()[:2])
    print("history objects are distinct ->", settings_history is not external_history)
    print(
        "Rule: a new factory call normally creates new enclosing bindings and "
        "new objects made during that call."
    )

    section("4. A closure is not an automatic value snapshot or deep copy")
    predict("Will mutating the exposed history list be visible through the closure?")
    external_history.append("external:manual")
    print("menu snapshot after external mutation ->", snapshot_menu()[:2])
    print("same history object ->", snapshot_menu()[2] is external_history)
    print(
        "Boundary: the closure keeps access to bindings; if a binding refers "
        "to a mutable object, aliases can observe mutations of that same object."
    )


if __name__ == "__main__":
    main()
