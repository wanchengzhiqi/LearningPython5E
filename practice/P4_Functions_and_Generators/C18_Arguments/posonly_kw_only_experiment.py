def f(record_id, /, **metadata):
    return record_id, metadata


for label, fn in [
    ("only keyword record_id=", lambda: f(record_id="x")),
    ("positional + keyword record_id=", lambda: f("x", record_id="y")),
]:
    try:
        print(label, "->", fn())
    except TypeError as e:
        print(label, "->", f"{type(e).__name__}: {e}")
