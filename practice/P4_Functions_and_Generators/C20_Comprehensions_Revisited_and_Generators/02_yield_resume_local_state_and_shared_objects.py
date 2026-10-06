"""Pause/resume, independent local bindings, and shared yielded references.

Run with .venv-py314/Scripts/python.exe -X utf8 and this file's path.
Events store immutable observations, not references to a changing record.
"""


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def track(label, record, events):
    count = 0
    events.append((label, "start"))
    while count < 2:
        count += 1
        events.append((label, "yield", count, record["text"]))
        yield record
        events.append((label, "resume", count, record["text"]))
    events.append((label, "end", count))


def main():
    section("1. Two calls have independent count bindings")
    events = []
    source = {"text": "Start"}
    original = source
    left = track("A", source, events)
    right = track("B", source, events)
    assert left is not right and events == []
    first = next(left)
    assert first is original
    assert events == [("A", "start"), ("A", "yield", 1, "Start")]
    print("A paused after first yield ->", tuple(events))

    section("2. A paused generator retains references, not a deep snapshot")
    first["text"] = "Begin"
    source = {"text": "Detached"}
    from_right = next(right)
    assert from_right is first is original
    assert from_right is not source
    again = next(left)
    assert again is first
    assert events[-2:] == [
        ("A", "resume", 1, "Begin"), ("A", "yield", 2, "Begin")
    ]
    print("both generators yield original ->", from_right is again is original)
    print("external rebound source ->", source)
    print("saved first item now ->", first)
    print("timeline ->", tuple(events))

    section("3. After the last yield, one more advance observes the end")
    assert ("A", "end", 2) not in events
    assert list(left) == []
    remaining_right = list(right)
    assert len(remaining_right) == 1
    assert remaining_right[0] is original
    # Extract only yield events: start/end entries have different lengths.
    counts = [(event[0], event[2]) for event in events if event[1] == "yield"]
    assert counts == [("A", 1), ("B", 1), ("A", 2), ("B", 2)]
    assert events[-1] == ("B", "end", 2)
    print("per-call counts ->", counts)
    print("completed timeline ->", tuple(events))
    print("Boundary: independent execution state does not isolate shared data.")
    print("OK: pause/resume, local state, sharing, and final advancement")


if __name__ == "__main__":
    main()
