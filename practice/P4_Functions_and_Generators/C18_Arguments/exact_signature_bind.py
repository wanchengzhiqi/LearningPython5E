import inspect
import sys

print("PYTHON:", sys.version)
print("=" * 50)


def package(
    source,
    /,
    target,
    mode="full",
    *files,
    encoding="utf-8",
    strict,
    **options,
):
    pass


sig = inspect.signature(package)
print("signature:", sig)
print("=" * 50)

bound = sig.bind(
    "source.csv",
    "target.json",
    "dialogue",
    "ui",
    strict=True,
    pretty=True,
)

print("after bind, arguments:")
print(bound.arguments)

bound.apply_defaults()

print("after apply_defaults, arguments:")
print(bound.arguments)
print("args  :", bound.args)
print("kwargs:", bound.kwargs)
