"""Generator functions, created objects, and first body execution.

Run from the repository root with .venv-py314/Scripts/python.exe -X utf8
and this file's path. Uses only synthetic memory data and stdout.
"""


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def argument(record, events):
    events.append("argument:evaluated")
    return record


def produce(record, events):
    events.append("body:start")
    yield record
    events.append("body:after-yield")


def main():
    section("1. Argument evaluation and binding precede body execution")
    events = []
    record = {"key": "menu.start"}
    factory = produce
    stream = factory(argument(record, events), events)
    assert factory is produce
    assert stream is not factory
    assert iter(stream) is stream
    assert events == ["argument:evaluated"]
    print("factory is produce ->", factory is produce)
    print("iter(stream) is stream ->", iter(stream) is stream)
    print("after creation ->", tuple(events))

    section("2. next() starts the body and yield hands out an object")
    item = next(stream)
    assert item is record
    assert events == ["argument:evaluated", "body:start"]
    print("yielded item is source record ->", item is record)
    print("after first next ->", tuple(events))
    tail = list(stream)
    assert tail == []
    assert events[-1] == "body:after-yield"
    print("tail ->", tail, "; after finishing ->", tuple(events))

    section("3. Missing arguments fail during the call")
    rejected_events = []
    result = "old"
    try:
        result = produce(argument(record, rejected_events))
    except TypeError as error:
        print("call exception ->", type(error).__name__)
    else:
        raise AssertionError("missing events argument must fail")
    assert result == "old"
    assert rejected_events == ["argument:evaluated"]
    print("argument effects remain ->", tuple(rejected_events))
    print("Rule: no generator body ran, but the argument expression did run.")
    print("OK: creation, argument matching, body start, and yielded identity")


if __name__ == "__main__":
    main()
