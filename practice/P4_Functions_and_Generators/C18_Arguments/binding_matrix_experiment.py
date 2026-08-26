import inspect


def bind_matrix(record_id, /, locale="en-US", *tags, dry_run, **metadata):
    return {
        "record_id": record_id,
        "locale": locale,
        "tags": tags,
        "dry_run": dry_run,
        "metadata": metadata,
    }


sig = inspect.signature(bind_matrix)
print("=== signature ===")
for name, p in sig.parameters.items():
    print(f"{name!r}: kind={p.kind}, default={p.default!r}")

print()

result = bind_matrix(
    "prompt-002",
    "fr-FR",
    "dialog",
    dry_run=False,
    reviewer="qa",
)

print("=== returned binding ===")
for name, value in result.items():
    print(f"{name:10} = {value!r}  (type={type(value).__name__}, id={id(value)})")

print()
print("'/' 是否出现在 signature.parameters:",
      "/" in sig.parameters)
print("'*tags' 之后: ", list(sig.parameters))
