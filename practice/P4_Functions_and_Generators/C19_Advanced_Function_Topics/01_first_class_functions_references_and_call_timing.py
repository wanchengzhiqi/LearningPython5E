r"""
First-class function objects, references, and delayed call timing.

Run:
    python practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\01_first_class_functions_references_and_call_timing.py
"""


call_events = []


def normalize_key(key):
    call_events.append("normalize_key")
    return key.strip().casefold()


def keep_callable(rule):
    call_events.append("keep_callable")
    return rule


def apply_rule(rule, value):
    call_events.append("apply_rule:before")
    result = rule(value)
    call_events.append("apply_rule:after")
    return result


def no_arguments():
    return "ready"


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Aliases and container slots can reference one function object")
    predict("Does saving normalize_key in more places execute its body?")
    alias = normalize_key
    registry = {"normalize": normalize_key}
    pipeline = [normalize_key]
    print("alias is original ->", alias is normalize_key)
    print("registry slot is original ->", registry["normalize"] is normalize_key)
    print("pipeline slot is original ->", pipeline[0] is normalize_key)
    print("events after saving references ->", tuple(call_events))
    print("Rule: extra names and slots add references; they do not call the function.")

    section("2. A higher-order function can accept and return a callable")
    predict("Does keep_callable call the rule that it returns?")
    selected = keep_callable(registry["normalize"])
    print("returned object is original ->", selected is normalize_key)
    print("events after returning callable ->", tuple(call_events))
    print(
        "Rule: accepting, saving, or returning a function object is separate "
        "from invoking it."
    )

    section("3. Parentheses begin the later call and its body effects")
    predict("Which events appear only when apply_rule invokes selected?")
    result = apply_rule(selected, " Menu.Start ")
    print("result ->", result)
    print("events after actual call ->", tuple(call_events))
    print(
        "Rule: apply_rule first receives a function object, then selected(value) "
        "performs the actual call."
    )

    section("4. callable() does not prove a compatible call contract")
    predict("Can a callable that accepts no arguments be used as a text rule?")
    call_events.clear()
    print("no_arguments is callable ->", callable(no_arguments))
    try:
        apply_rule(no_arguments, "menu.quit")
    except TypeError as error:
        print("exception type ->", type(error).__name__)
    print("events before rejection ->", tuple(call_events))
    print(
        "Boundary: callable() does not prove accepted arguments, return values, "
        "exceptions, side effects, or business behavior."
    )


if __name__ == "__main__":
    main()
