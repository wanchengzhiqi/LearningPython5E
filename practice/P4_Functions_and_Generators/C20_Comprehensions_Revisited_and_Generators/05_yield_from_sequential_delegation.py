"""Minimal yield from: sequential delegation and child termination.

Run with .venv-py314/Scripts/python.exe -X utf8 and this file's path.
No send/throw/close protocol, concurrency, or delegation return-value lesson.
"""


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def child(label, records, events):
    events.append((label, "start"))
    for record in records:
        events.append((label, "yield", record["key"]))
        yield record
        events.append((label, "resume"))
    events.append((label, "end"))


def combined(first, second, events):
    events.append(("outer", "start"))
    yield from child("A", first, events)
    events.append(("outer", "after-A"))
    yield from child("empty", [], events)
    events.append(("outer", "after-empty"))
    yield from child("B", second, events)
    events.append(("outer", "end"))


def main():
    section("1. The outer generator delegates until the first child ends")
    first = [{"key": "menu.start", "text": "Start"}]
    second = [{"key": "menu.quit", "text": "Quit"}]
    events = []
    stream = combined(first, second, events)
    assert events == []
    item_a = next(stream)
    assert item_a is first[0]
    assert events == [
        ("outer", "start"), ("A", "start"), ("A", "yield", "menu.start")
    ]
    print("after first next ->", tuple(events))

    section("2. Delegation passes original references and crosses empty input")
    item_a["text"] = "Begin"
    assert first[0]["text"] == "Begin"
    item_b = next(stream)
    assert item_b is second[0]
    assert events[3:] == [
        ("A", "resume"), ("A", "end"), ("outer", "after-A"),
        ("empty", "start"), ("empty", "end"), ("outer", "after-empty"),
        ("B", "start"), ("B", "yield", "menu.quit"),
    ]
    assert ("outer", "end") not in events
    print("A reference preserved ->", item_a is first[0])
    print("B reference preserved ->", item_b is second[0])
    print("after second next ->", tuple(events))

    section("3. Child B and then the outer body finish on the next advance")
    assert list(stream) == []
    assert events[-3:] == [("B", "resume"), ("B", "end"), ("outer", "end")]
    print("completion ->", tuple(events[-3:]))
    print("Rule: sequential delegation neither copies data nor starts concurrency.")
    print("OK: delegation order, empty child, identity, and ending boundaries")


if __name__ == "__main__":
    main()
