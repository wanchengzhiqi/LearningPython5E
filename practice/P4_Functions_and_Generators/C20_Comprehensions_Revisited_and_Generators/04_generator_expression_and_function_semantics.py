"""A finite comparison of generator expressions and generator functions.

Run with .venv-py314/Scripts/python.exe -X utf8 and this file's path.
Equal results alone do not prove equal evaluation times or effects.
"""


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def source(events):
    events.append("source:called")
    return [" A ", " B "]


def clean(text, events):
    events.append(("clean", text))
    return text.strip().casefold()


def from_source(events):
    events.append("function:start")
    for text in source(events):
        yield clean(text, events)


def scale(items, factor, events):
    events.append("scale:start")
    for item in items:
        yield item * factor


def main():
    section("1. The expression evaluates its leftmost iterable immediately")
    expression_events = []
    function_events = []
    expression = (clean(text, expression_events)
                  for text in source(expression_events))
    function = from_source(function_events)
    assert expression_events == ["source:called"]
    assert function_events == []
    print("expression creation ->", tuple(expression_events))
    print("function creation ->", tuple(function_events))
    expression_result = list(expression)
    function_result = list(function)
    assert expression_result == function_result == ["a", "b"]
    assert function_events[0:2] == ["function:start", "source:called"]
    print("equal results ->", expression_result == function_result)
    print("expression events ->", tuple(expression_events))
    print("function events ->", tuple(function_events))

    section("2. Later name lookup differs from a bound function argument")
    items = [1, 2]
    factor = 2
    item = "outside"
    expression = (item * factor for item in items)
    events = []
    function = scale(items, factor, events)
    factor = 10
    items.append(3)
    assert events == []
    expression_result = list(expression)
    function_result = list(function)
    assert expression_result == [10, 20, 30]
    assert function_result == [2, 4, 6]
    assert item == "outside"
    print("later factor lookup ->", expression_result)
    print("parameter bound at call ->", function_result)
    print("outer item ->", item)
    print("Boundary: both retain access to the original mutable items list.")

    section("3. Invalid leftmost iterable fails at different times")
    try:
        expression = (item for item in None)
    except TypeError as error:
        print("expression creation ->", type(error).__name__)
    else:
        raise AssertionError("None must be rejected as the leftmost iterable")
    events = []
    function = scale(None, 2, events)
    assert events == []
    try:
        next(function)
    except TypeError as error:
        print("function first next ->", type(error).__name__)
    else:
        raise AssertionError("None must be rejected when the body iterates")
    assert events == ["scale:start"]
    print("Rule: function argument expressions still evaluate at call time.")
    print("OK: creation timing, lookup, scope, mutation, and failure timing")


if __name__ == "__main__":
    main()
