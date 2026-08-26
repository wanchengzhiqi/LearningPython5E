import inspect


def bind_matrix(record_id, /, locale="en-US", *tags, dry_run, **metadata):
    return {
        "record_id": record_id,
        "locale": locale,
        "tags": tags,
        "dry_run": dry_run,
        "metadata": metadata,
    }


def positional_identity(record_id, /):
    return record_id


print("=== call 1: bind_matrix ===")
print("signature:", inspect.signature(bind_matrix))
try:
    result = bind_matrix(
        "prompt-004",
        dry_run=True,
        record_id="external-alias",
    )
    print("SUCCESS")
    print("result:", result)
except TypeError as e:
    print("FAILED")
    print(f"{type(e).__name__}: {e}")

print()
print("=== call 2: positional_identity ===")
print("signature:", inspect.signature(positional_identity))
try:
    result = positional_identity(record_id="prompt-004")
    print("SUCCESS")
    print("result:", result)
except TypeError as e:
    print("FAILED")
    print(f"{type(e).__name__}: {e}")
