"""C12-03: comparisons, chained evaluation, and branch selection."""

TRACE = []


def section(title):
    print("\n" + "=" * 68)
    print(title)


def measured_value():
    TRACE.append("measured_value")
    print("  measured_value() called")
    return 7


def condition(label, result):
    TRACE.append(label)
    print(f"  condition {label!r} -> {result}")
    return result


def independent_checks(severity):
    hits = []
    if severity >= 40:
        hits.append("warning")
    if severity >= 80:
        hits.append("critical")
    return hits


def exclusive_branch(severity):
    if severity >= 80:
        return "critical"
    elif severity >= 40:
        return "warning"
    else:
        return "info"


def main():
    section("1. Equality is not identity")
    print("[Predict] Which names refer to the same list?")
    left = ["menu.start"]
    equal_list = ["menu.start"]
    alias = left
    print("left == equal_list ->", left == equal_list)
    print("left is equal_list ->", left is equal_list)
    print("left is alias ->", left is alias)

    section("2. Membership tests")
    print("[Predict] Does dict membership test keys or values?")
    resources = {"menu.start": "Start", "menu.quit": "Quit"}
    print("'menu.start' in resources ->", "menu.start" in resources)
    print("'Start' in resources ->", "Start" in resources)
    print("'Start' in resources.values() ->", "Start" in resources.values())

    section("3. A comparison chain evaluates its middle once")
    print("[Predict] How many times will measured_value() run?")
    TRACE.clear()
    print("0 < measured_value() < 10 ->", 0 < measured_value() < 10)
    print("trace ->", TRACE)
    TRACE.clear()
    repeated = (0 < measured_value()) and (measured_value() < 10)
    print("repeated-call form ->", repeated)
    print("trace ->", TRACE)

    section("4. Independent if versus if/elif/else")
    print("independent_checks(90) ->", independent_checks(90))
    print("exclusive_branch(90) ->", exclusive_branch(90))

    section("5. A matched branch skips later elif conditions")
    print("[Predict] Will the second condition run?")
    TRACE.clear()
    if condition("first", True):
        selected = "first block"
    elif condition("second", True):
        selected = "second block"
    else:
        selected = "else block"
    print("selected ->", selected)
    print("trace ->", TRACE)


if __name__ == "__main__":
    main()
