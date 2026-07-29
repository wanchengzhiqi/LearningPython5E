r"""
Explicit return values, None paths, unreachable code, and exceptions.

Run:
    python practice\P4_Functions_and_Generators\C16_Function_Basics\03_return_paths_none_and_exceptions.py
"""


def explicit_value(text):
    return text.strip()


def bare_return(stop_early):
    if stop_early:
        return
    return "continued"


def implicit_none(timeline):
    timeline.append("body reached its final statement")


def classify_text(text):
    if text is None:
        raise ValueError("text is required")
    if text == "":
        return "empty"
    if text.isspace():
        return "blank"
    return "ready"


def early_exit(timeline):
    timeline.append("before return")
    return "done"
    timeline.append("unreachable after return")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Explicit, bare, and implicit return paths")
    predict("Which calls produce a non-None object?")
    timeline = []
    print("explicit value ->", explicit_value(" Start "))
    print("bare return ->", bare_return(True))
    print("bare non-early path ->", bare_return(False))
    implicit_result = implicit_none(timeline)
    print("implicit result ->", implicit_result)
    print("implicit result is None ->", implicit_result is None)
    print("timeline ->", timeline)
    print("Rule: bare return and fall-through both return None normally.")

    section("2. One function can have multiple reachable return paths")
    predict("Which path handles empty, whitespace-only, and ordinary text?")
    for sample in ("", "   ", "menu.start"):
        print(f"classify_text({sample!r}) ->", classify_text(sample))
    print("Rule: only the path actually reached determines this call's result.")

    section("3. return ends the current function-body path")
    predict("Will the statement after return append another event?")
    exit_timeline = []
    exit_result = early_exit(exit_timeline)
    print("exit result ->", exit_result)
    print("exit timeline ->", exit_timeline)
    print("Rule: source can exist after return without being reached.")

    section("4. Raising an exception is not returning None")
    predict("Does the assignment complete when classify_text raises?")
    unchanged = object()
    result = unchanged
    try:
        result = classify_text(None)
    except ValueError as error:
        print("exception type ->", type(error).__name__)
    print("result binding unchanged ->", result is unchanged)
    print(
        "Rule: an exception that propagates out of the function exits that call "
        "abnormally; it does not produce an implicit None result."
    )


if __name__ == "__main__":
    main()
