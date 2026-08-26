import sys
print("PYTHON:", sys.version)
print("=" * 50)


def mark(name, value):
    print("mark", name)
    return value


def export(
    source,
    target,
    /,
    *,
    encoding,
    strict,
    **options,
):
    print(
        "BODY",
        source,
        target,
        encoding,
        strict,
        options,
    )


paths = (
    "source.csv",
    "target.json",
)

base = {
    "encoding": "utf-8",
}

extra = {
    "pretty": True,
}

export(
    *mark("PATHS", paths),
    **mark("BASE", base),
    strict=mark("STRICT", True),
    **mark("EXTRA", extra),
)
