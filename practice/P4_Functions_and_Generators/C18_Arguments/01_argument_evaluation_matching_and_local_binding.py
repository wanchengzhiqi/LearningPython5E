r"""
Argument evaluation, call matching, and per-call local parameter bindings.

Run:
    python practice\P4_Functions_and_Generators\C18_Arguments\01_argument_evaluation_matching_and_local_binding.py
"""


call_events = []


def resolve_builder():
    call_events.append("target")
    return build_entry


def evaluate(label, value):
    call_events.append(f"argument:{label}")
    return value


def build_entry(key, *, locale, options):
    call_events.append("body")
    current_locals = locals()
    parameter_names = tuple(
        name for name in ("key", "locale", "options") if name in current_locals
    )
    return {
        "label": f"{locale}:{key.strip().lower()}",
        "options": options,
        "parameter_names": parameter_names,
    }


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. The call target and argument expressions are evaluated first")
    predict("Which events occur before the function body begins?")
    shared_options = {"normalize": True}
    result = resolve_builder()(
        evaluate("key", " Menu.Start "),
        locale=evaluate("locale", "ja-JP"),
        options=evaluate("options", shared_options),
    )
    print("event order ->", tuple(call_events))
    print("result label ->", result["label"])
    print("Rule: target and argument expressions are evaluated before body entry.")

    section("2. Successful matching creates this call's local parameter bindings")
    predict("Did the call copy shared_options into a new dictionary?")
    print("selected local parameter names ->", result["parameter_names"])
    print("bound options is caller object ->", result["options"] is shared_options)
    print(
        "Rule: parameters are local names for this call; binding them does "
        "not copy the argument objects."
    )

    section("3. Matching failure prevents body entry but keeps earlier effects")
    predict("Are argument-evaluation events rolled back after TypeError?")
    call_events.clear()
    try:
        resolve_builder()(
            evaluate("key", "menu.quit"),
            locale=evaluate("locale", "en-US"),
            options=evaluate("options", shared_options),
            unknown=evaluate("unknown", True),
        )
    except TypeError as error:
        print("exception type ->", type(error).__name__)
    print("events before rejection ->", tuple(call_events))
    print("body entered ->", "body" in call_events)
    print(
        "Rule: all shown expressions produced effects, then matching rejected "
        "the call before local parameter bindings and body execution."
    )

    section("4. Call progress must be described by its actual completed stage")
    predict("Does 'the call started' prove that parameter binding completed?")
    print("successful call reached body ->", result["label"] == "ja-JP:menu.start")
    print("rejected call reached body ->", "body" in call_events)
    print(
        "Boundary: target evaluation, argument evaluation, matching, local "
        "binding, and body entry are separate checkpoints."
    )


if __name__ == "__main__":
    main()
