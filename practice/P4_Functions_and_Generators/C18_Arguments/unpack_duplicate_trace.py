import sys

trace_events = []


def tracer(frame, event, arg):
    if frame.f_code.co_name == "target":
        trace_events.append((event, frame.f_code.co_name))
    return tracer


def positional_source():
    return ("prompt-008", "en-US")


def mapping_source():
    return {"dry_run": False}


def target(key, locale, *, dry_run):
    pass


sys.settrace(tracer)
try:
    target(
        *positional_source(),
        dry_run=True,
        **mapping_source(),
    )
except TypeError as e:
    print("caught:", type(e).__name__, ":", e)
finally:
    sys.settrace(None)

print("target-related trace events:", trace_events)
