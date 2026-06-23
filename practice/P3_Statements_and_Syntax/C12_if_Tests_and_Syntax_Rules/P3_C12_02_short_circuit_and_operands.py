"""C12-02: short-circuit evaluation and operand return values."""

TRACE = []


def section(title):
    print("\n" + "=" * 68)
    print(title)


def visit(label, value):
    TRACE.append(label)
    print(f"  evaluated {label!r} -> {value!r}")
    return value


def explode():
    raise RuntimeError("this expression should have been short-circuited")


def main():
    section("1. and returns an operand")
    print("[Predict] Does a falsy left operand evaluate the right side?")
    left = []
    right = ["menu.start"]
    TRACE.clear()
    result = visit("left", left) and visit("right", right)
    print("result ->", result, "result is left ->", result is left)
    print("trace ->", TRACE)

    TRACE.clear()
    result = visit("truthy left", "ready") and visit("right", right)
    print("result ->", result, "result is right ->", result is right)
    print("trace ->", TRACE)

    section("2. or returns an operand")
    print("[Predict] Does a truthy primary evaluate the fallback?")
    primary = "cached report"
    fallback = "generated report"
    TRACE.clear()
    result = visit("primary", primary) or visit("fallback", fallback)
    print("result ->", result, "result is primary ->", result is primary)
    print("trace ->", TRACE)

    TRACE.clear()
    result = visit("empty primary", "") or visit("fallback", fallback)
    print("result ->", result, "result is fallback ->", result is fallback)
    print("trace ->", TRACE)

    section("3. Calls, effects, and exceptions can be skipped")
    print("[Predict] Will either explode() call run?")
    first = "available" or explode()
    second = "" and explode()
    print("first ->", first)
    print("second ->", second)
    print("No exception: neither right-side expression was evaluated.")

    section("4. not always returns bool")
    for value in ([], ["menu.start"], "", "ready"):
        result = not value
        print(f"value={value!r:<20} result={result!r:<5} type={type(result).__name__}")
    print("and/or return operands; not returns True or False.")


if __name__ == "__main__":
    main()
