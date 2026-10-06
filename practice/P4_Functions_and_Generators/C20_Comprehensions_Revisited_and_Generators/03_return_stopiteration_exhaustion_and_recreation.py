"""Yielded values, termination values, exhaustion, and fresh calls.

Run with .venv-py314/Scripts/python.exe -X utf8 and this file's path.
Use return inside generators, not a manual raise StopIteration.
"""


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def with_summary(events):
    events.append("start")
    yield "menu.start"
    events.append("return")
    return {"produced": 1}


def natural_end():
    yield "natural"


def bare_return():
    yield "bare"
    return


def observe_end(stream):
    try:
        next(stream)
    except StopIteration as error:
        print("exception ->", type(error).__name__, "; value ->", error.value)
        return error.value
    raise AssertionError("expected termination, but an item was yielded")


def main():
    section("1. yield suspends; return ends this execution")
    events = []
    stream = with_summary(events)
    item = next(stream)
    assert item == "menu.start"
    assert events == ["start"]
    print("last data item ->", item, "; events ->", tuple(events))
    summary = observe_end(stream)
    assert summary == {"produced": 1}
    assert events == ["start", "return"]
    assert observe_end(stream) is None
    assert list(stream) == []
    print("Rule: the original return value is not replayed after exhaustion.")

    section("2. for consumes data items and handles normal termination")
    loop_events = []
    delivered = []
    for item in with_summary(loop_events):
        delivered.append(item)
    assert delivered == ["menu.start"]
    assert loop_events == ["start", "return"]
    print("for delivered ->", delivered)
    print("The summary dictionary is not an extra yielded item.")

    section("3. Natural ending and bare return both terminate with None")
    for factory in (natural_end, bare_return):
        current = factory()
        print("data ->", next(current))
        assert observe_end(current) is None

    section("4. Reusing the object differs from calling the producer again")
    fresh = with_summary(events)
    assert fresh is not stream
    assert list(fresh) == ["menu.start"]
    assert events == ["start", "return", "start", "return"]
    print("fresh is old ->", fresh is stream)
    print("events after fresh call and consumption ->", tuple(events))
    print("Boundary: a fresh call does not promise to recreate external sources.")
    print("OK: return values, consumer behavior, exhaustion, and recreation")


if __name__ == "__main__":
    main()
