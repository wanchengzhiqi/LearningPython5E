def bind_matrix(record_id, /, locale="en-US", *tags, dry_run, **metadata):
    return {
        "record_id": record_id,
        "locale": locale,
        "tags": tags,
        "dry_run": dry_run,
        "metadata": metadata,
    }


print("=== try to pass dry_run positionally ===")
try:
    result = bind_matrix(
        "prompt-002",
        "fr-FR",
        "dialog",
        False,          # 想给 dry_run 的位置参数
        reviewer="qa",
    )
    print("result:", result)
except TypeError as e:
    print(f"{type(e).__name__}: {e}")

print()

print("=== only three positionals ===")
try:
    result = bind_matrix(
        "prompt-002",
        "fr-FR",
        "dialog",
        reviewer="qa",
    )
    print("result:", result)
except TypeError as e:
    print(f"{type(e).__name__}: {e}")

print()

print("=== dry_run keyword + no extra positional ===")
result = bind_matrix(
    "prompt-002",
    dry_run=True,
)
print("result:", result)
