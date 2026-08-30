r"""
Higher-order transforms, delayed callbacks, dispatch, and simple composition.

Run:
    python practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\02_higher_order_callbacks_dispatch_and_composition.py
"""


rule_events = []
callback_events = []


def strip_text(text):
    rule_events.append("rule:strip_text")
    return text.strip()


def normalize_case(text):
    rule_events.append("rule:normalize_case")
    return text.casefold()


def add_locale_prefix(text):
    rule_events.append("rule:add_locale_prefix")
    return f"ja-JP:{text}"


def reject_empty(text):
    rule_events.append("rule:reject_empty")
    if not text:
        raise ValueError("empty text")
    return text


def record_success(result):
    callback_events.append(f"success:{result}")


def apply_transform(text, rule):
    return rule(text)


def register_rule(registry, name, rule, events):
    registry[name] = rule
    events.append(f"registered:{name}")


def dispatch(registry, name, text, events):
    events.append(f"dispatch:{name}")
    return registry[name](text)


def run_pipeline(text, rules, *, on_success, events):
    current = text
    for rule in rules:
        events.append(f"before:{rule.__name__}")
        current = rule(current)
        events.append(f"after:{rule.__name__}")
    on_success(current)
    return current


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. A higher-order function receives behavior through an argument")
    predict("When does the supplied strip_text function actually run?")
    rule_events.clear()
    transformed = apply_transform(" Menu.Start ", strip_text)
    print("result ->", transformed)
    print("rule events ->", tuple(rule_events))
    print(
        "Rule: apply_transform accepts a function object, and rule(text) is the "
        "separate invocation point."
    )

    section("2. Registration and later dictionary dispatch are separate stages")
    predict("Does placing a rule in the registry execute the rule body?")
    registry = {}
    dispatch_events = []
    rule_events.clear()
    register_rule(registry, "normalize", normalize_case, dispatch_events)
    print("events after registration ->", tuple(dispatch_events))
    print("rule events after registration ->", tuple(rule_events))
    dispatched = dispatch(registry, "normalize", "Menu.Quit", dispatch_events)
    print("dispatch result ->", dispatched)
    print("events after dispatch ->", tuple(dispatch_events))
    print("rule events after dispatch ->", tuple(rule_events))
    print("Rule: a registry slot saves a callable; dispatch performs the later call.")

    section("3. Uniform call contracts allow a small transformation pipeline")
    predict("In which order do the three rules and success callback run?")
    pipeline_events = []
    rule_events.clear()
    callback_events.clear()
    pipeline = (strip_text, normalize_case, add_locale_prefix)
    result = run_pipeline(
        " Menu.Options ",
        pipeline,
        on_success=record_success,
        events=pipeline_events,
    )
    print("result ->", result)
    print("pipeline events ->", tuple(pipeline_events))
    print("rule events ->", tuple(rule_events))
    print("callback events ->", tuple(callback_events))
    print(
        "Rule: composition is reliable only when each step's accepted input, "
        "return object, exception, and side-effect contract is explicit."
    )

    section("4. A failing rule keeps earlier effects and skips later callbacks")
    predict("Which events remain when reject_empty raises ValueError?")
    pipeline_events.clear()
    rule_events.clear()
    callback_events.clear()
    try:
        run_pipeline(
            "   ",
            (strip_text, reject_empty, add_locale_prefix),
            on_success=record_success,
            events=pipeline_events,
        )
    except ValueError as error:
        print("exception type ->", type(error).__name__)
    print("pipeline events ->", tuple(pipeline_events))
    print("rule events ->", tuple(rule_events))
    print("callback events ->", tuple(callback_events))
    print(
        "Boundary: a callback's registration does not guarantee that it will "
        "run, and an exception does not roll back earlier rule effects."
    )


if __name__ == "__main__":
    main()
