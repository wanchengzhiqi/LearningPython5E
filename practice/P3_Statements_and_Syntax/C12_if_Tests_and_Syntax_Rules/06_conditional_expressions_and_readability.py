r"""
Conditional expressions: selected values, lazy branches, and readability boundaries.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\06_conditional_expressions_and_readability.py
"""

TRACE = []


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def choose(label, value):
    TRACE.append(label)
    print(f"  evaluated branch {label!r}")
    return value


def main():
    section("1. A conditional expression produces one selected value")
    predict("Which branch expression runs when dry_run is True?")
    TRACE.clear()
    dry_run = True
    action = (
        choose("preview", "preview")
        if dry_run
        else choose("write", "write")
    )
    print("action ->", action)
    print("trace ->", TRACE)

    section("2. The unselected expression has no call or side effect")
    predict("Will the write branch append to TRACE?")
    TRACE.clear()
    dry_run = False
    action = (
        choose("preview", {"mode": "preview"})
        if dry_run
        else choose("write", {"mode": "write"})
    )
    print("action ->", action)
    print("trace ->", TRACE)

    section("3. prompt_manager_gui.py uses conditional expressions for values")
    predict("Which widget-state strings are produced?")
    for editable in (True, False):
        state = "normal" if editable else "disabled"
        print(f"editable={editable!r:<5} -> state={state!r}")

    current_record_id = 7
    button_text = "新增" if current_record_id is not None else "保存新增"
    print("button_text ->", button_text)

    section("4. Boolean selection and conditional expressions are distinct")
    predict("What objects can search_text.strip() or None return?")
    for search_text in ("  C12  ", "   "):
        normalized_search = search_text.strip() or None
        print(
            f"search_text={search_text!r:<10} -> "
            f"{normalized_search!r} ({type(normalized_search).__name__})"
        )
    print("or selected an operand; it did not promise a bool result.")

    section("5. Use an if statement when a branch needs multiple actions")
    predict("Why is this clearer than packing effects into one expression?")
    output_mode = "json"
    events = []
    if output_mode == "json":
        serializer = "json.dumps"
        content_type = "application/json"
        events.append("validate JSON-compatible report")
    else:
        serializer = "plain text formatter"
        content_type = "text/plain"
        events.append("format human-readable report")
    print("serializer ->", serializer)
    print("content_type ->", content_type)
    print("events ->", events)

    section("6. Keep conditional expressions small and value-oriented")
    predict("Which use is clearer: selecting a suffix or hiding many effects?")
    suffix = ".json" if output_mode == "json" else ".txt"
    print("selected suffix ->", suffix)
    print(
        "Rule: use a conditional expression for one readable value; "
        "use if blocks for multi-step control flow and side effects."
    )


if __name__ == "__main__":
    main()
