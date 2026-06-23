r"""
Boolean short-circuit evaluation and operand return values.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\02_short_circuit_operand_results.py
"""

TRACE = []


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def visit(label, value):
    TRACE.append(label)
    print(f"  evaluated {label!r} -> {value!r}")
    return value


def forbidden(label):
    raise RuntimeError(f"{label} should have been skipped")


def main():
    section("1. and returns the first falsy operand or the final operand")
    predict("Will a falsy left operand evaluate the right expression?")
    left = []
    right = ["menu.start"]
    TRACE.clear()
    result = visit("left", left) and visit("right", right)
    print("result ->", result)
    print("result is left ->", result is left)
    print("trace ->", TRACE)

    predict("If the left operand is truthy, which object is returned?")
    truthy_left = ["ready"]
    TRACE.clear()
    result = visit("truthy_left", truthy_left) and visit("right", right)
    print("result ->", result)
    print("result is right ->", result is right)
    print("trace ->", TRACE)

    section("2. or returns the first truthy operand or the final operand")
    predict("Will a truthy primary value evaluate the fallback?")
    primary = {"mode": "cached"}
    fallback = {"mode": "generated"}
    TRACE.clear()
    result = visit("primary", primary) or visit("fallback", fallback)
    print("result ->", result)
    print("result is primary ->", result is primary)
    print("trace ->", TRACE)

    predict("What happens when the primary value is falsy?")
    empty_primary = {}
    TRACE.clear()
    result = visit("empty_primary", empty_primary) or visit("fallback", fallback)
    print("result ->", result)
    print("result is fallback ->", result is fallback)
    print("trace ->", TRACE)

    section("3. Short-circuiting can skip calls, side effects, and exceptions")
    predict("Will either forbidden() call run?")
    safe_or = "available" or forbidden("or-right")
    safe_and = "" and forbidden("and-right")
    print("safe_or ->", safe_or)
    print("safe_and ->", safe_and)
    print("No exception means both right-side calls were skipped.")

    section("4. A longer chain stops as soon as its result is known")
    predict("Which labels will appear in TRACE?")
    TRACE.clear()
    result = (
        visit("config", {"strict": True})
        and visit("missing_keys", ["menu.quit"])
        and visit("report_mode", "json")
    )
    print("result ->", result)
    print("trace ->", TRACE)

    TRACE.clear()
    result = (
        visit("config", {"strict": True})
        and visit("missing_keys", [])
        and visit("report_mode", "json")
    )
    print("result with empty missing_keys ->", result)
    print("trace ->", TRACE)

    section("5. not always returns a bool object")
    predict("How does not differ from and/or?")
    for value in ([], ["menu.start"], "", "ready", None):
        result = not value
        print(
            f"value={value!r:<20} result={result!r:<5} "
            f"type={type(result).__name__}"
        )
    print("Rule: and/or select operands; not produces True or False.")


if __name__ == "__main__":
    main()
