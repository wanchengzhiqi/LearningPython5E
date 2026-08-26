import inspect
import sys

print("PYTHON:", sys.version)
print("=" * 60)


def export(
    source,
    /,
    target,
    mode="json",
    *fields,
    encoding="utf-8",
    strict,
    **options,
):
    print(
        source,
        target,
        mode,
        fields,
        encoding,
        strict,
        options,
    )


print("signature:", inspect.signature(export))
for name, kind in [
    ("source", "positional-only"),
    ("target", "positional-or-keyword"),
    ("mode", "positional-or-keyword"),
    ("fields", "var-positional"),
    ("encoding", "keyword-only"),
    ("strict", "keyword-only"),
    ("options", "var-keyword"),
]:
    p = inspect.signature(export).parameters[name]
    print(f"{name:10} kind={p.kind.name:22} default={p.default!r}")
print("=" * 60)

calls = {
    1: 'export("a.csv", "b.json", strict=True)',
    2: 'export("a.csv", target="b.json", strict=True)',
    3: 'export(source="a.csv", target="b.json", strict=True)',
    4: 'export("a.csv", "b.json", "text", "speaker", strict=True)',
    5: 'export("a.csv", "b.json", target="other.json", strict=True)',
    6: 'export("a.csv", "b.json", strict=True, pretty=True)',
}

for n in range(1, 7):
    code = calls[n]
    print(f"--- call {n}: {code}")
    try:
        result = eval(code, {"export": export})
        print(f"    => 合法")
    except Exception as e:
        print(f"    => 非法 | {type(e).__name__}: {e}")
