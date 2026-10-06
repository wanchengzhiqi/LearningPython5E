"""Finite streaming/materialized localization pipelines and their contracts.

Run with .venv-py314/Scripts/python.exe -X utf8 and this file's path.
Inputs: finite iterables of ordinary dicts with key/text strings and tags lists.
Output dicts are new; tags intentionally aliases each input tags list.
Only synthetic memory is used. Events are observations, not an audit framework.
"""


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def sample_records():
    return [
        {"key": " Menu.Start ", "text": " Start ", "tags": ["ui"]},
        {"key": " Menu.Empty ", "text": "  ", "tags": []},
        {"key": " Menu.Quit ", "text": " Quit ", "tags": ["ui"]},
    ]


def normalize(records, events):
    for record in records:
        events.append(("read", record["key"]))
        if not isinstance(record["key"], str) or not isinstance(record["text"], str):
            raise TypeError("key and text must be strings")
        key = record["key"].strip().casefold()
        events.append(("clean", key))
        yield {"key": key, "text": record["text"].strip(), "tags": record["tags"]}


def nonblank(records, events):
    for record in records:
        events.append(("filter", record["key"]))
        if record["text"]:
            yield record


def streaming(records, events):
    return nonblank(normalize(records, events), events)


def materialized(records, events):
    cleaned = list(normalize(records, events))
    return list(nonblank(cleaned, events))


def keys(records):
    return [record["key"] for record in records]


def read_count(events):
    return sum(event[0] == "read" for event in events)


def main():
    section("1. Equal successful content, different stage timing")
    rows = sample_records()
    stream_events, eager_events = [], []
    stream = streaming(rows, stream_events)
    assert stream_events == []
    streamed = list(stream)
    eager = materialized(rows, eager_events)
    assert streamed == eager
    assert keys(streamed) == ["menu.start", "menu.quit"]
    assert read_count(stream_events) == read_count(eager_events) == 3
    assert stream_events != eager_events
    print("results ->", streamed)
    print("stream events ->", tuple(stream_events))
    print("materialized events ->", tuple(eager_events))
    assert streamed is not eager and streamed[0] is not rows[0]
    assert streamed[0]["tags"] is eager[0]["tags"] is rows[0]["tags"]
    streamed[0]["tags"].append("reviewed")
    assert rows[0]["tags"] == ["ui", "reviewed"]
    print("new record, shared tags ->", rows[0]["tags"])
    print("Boundary: materialization is not deep copying or ownership isolation.")

    section("2. break leaves a retained stream partially consumed")
    events = []
    partial = streaming(rows, events)
    for first in partial:
        break
    assert first["key"] == "menu.start" and read_count(events) == 1
    print("after break ->", tuple(events))
    assert keys(list(partial)) == ["menu.quit"]
    assert read_count(events) == 3 and list(partial) == []
    assert keys(list(streaming(rows, []))) == ["menu.start", "menu.quit"]
    print("remaining output -> ['menu.quit']; same exhausted object -> []")

    section("3. Two pipelines can compete for one upstream cursor")
    upstream = iter(rows)
    events_a, events_b = [], []
    left, right = streaming(upstream, events_a), streaming(upstream, events_b)
    assert next(left)["key"] == "menu.start"
    assert next(right)["key"] == "menu.quit"
    assert list(left) == list(right) == []
    assert read_count(events_a) == 1 and read_count(events_b) == 2
    assert list(streaming(upstream, [])) == []
    assert keys(list(streaming(iter(rows), []))) == ["menu.start", "menu.quit"]
    print("shared cursor read counts ->", read_count(events_a), read_count(events_b))
    print("Rule: replay requires a fresh source cursor or saved materialized data.")

    section("4. Empty input produces no rows and no per-record events")
    events = []
    assert list(streaming([], events)) == materialized([], events) == []
    assert events == []
    print("empty outputs and events -> []")

    section("5. Failure preserves prior consumption and partial effects")
    broken = sample_records()
    broken[1]["text"] = 404
    events = []
    upstream = iter(broken)
    failing = streaming(upstream, events)
    delivered = []
    try:
        for record in failing:
            delivered.append(record)
    except TypeError as error:
        print("stream failure ->", type(error).__name__)
    else:
        raise AssertionError("invalid second text must fail")
    assert keys(delivered) == ["menu.start"]
    assert read_count(events) == 2 and list(failing) == []
    assert next(upstream) is broken[2]
    print("delivered before failure ->", keys(delivered))
    print("failure events ->", tuple(events))

    eager_failure_events = []
    result = "old"
    try:
        result = materialized(broken, eager_failure_events)
    except TypeError as error:
        print("materialization failure ->", type(error).__name__)
    else:
        raise AssertionError("materialized path must reject the same row")
    assert result == "old"
    assert read_count(eager_failure_events) == 2
    assert not any(event[0] == "filter" for event in eager_failure_events)
    print("old assignment retained ->", result)
    print("prior eager effects ->", tuple(eager_failure_events))

    list_events = []
    result = "old"
    try:
        result = list(streaming(broken, list_events))
    except TypeError:
        pass
    else:
        raise AssertionError("list consumption must fail")
    assert result == "old" and read_count(list_events) == 2
    assert ("filter", "menu.start") in list_events
    print("list(stream) fails without assigning its partial result.")
    print("Boundary: effects are not rolled back; no timing/memory benchmark.")
    print("The retained event log itself grows as records are consumed.")
    print("OK: normal, empty, partial, shared, repeated, ownership, failure")


if __name__ == "__main__":
    main()
