r"""
Signatures, interpreter evidence, official references, and minimum experiments.

Run:
    python practice\P3_Statements_and_Syntax\C15_The_Documentation_Interlude\04_signature_version_and_contract_checks.py
"""

import inspect
import itertools
import platform
import sys


BATCHED_DOCS = "https://docs.python.org/3/library/itertools.html#itertools.batched"


def normalize_text(text: str, *, strip: bool = True, upper: bool = False) -> str:
    """Return text after the explicitly selected normalization operations."""

    if not isinstance(text, str):
        raise TypeError("text must be str")
    result = text.strip() if strip else text
    return result.upper() if upper else result


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Record the active runtime before comparing version-sensitive claims")
    predict("Which interpreter and implementation are producing this evidence?")
    print("sys.executable ->", sys.executable)
    print("version tuple ->", tuple(sys.version_info[:3]))
    print("implementation ->", platform.python_implementation())
    print("full version ->", sys.version.splitlines()[0])

    section("2. A signature describes call shape, not the whole behavior contract")
    predict("Which arguments are keyword-only, and which exception is possible?")
    signature = inspect.signature(normalize_text)
    bound = signature.bind(" hp ", upper=True)
    print("signature ->", signature)
    print("bound arguments ->", dict(bound.arguments))
    print("docstring ->", inspect.getdoc(normalize_text))
    print("representative result ->", normalize_text(" hp ", upper=True))
    try:
        normalize_text(15)
    except TypeError as exc:
        print("invalid input exception ->", type(exc).__name__)
    print("Rule: read parameters, returns, exceptions, side effects, and version scope.")

    section("3. Cross-check a version-sensitive standard-library API")
    predict("What does strict=True do with an incomplete final batch?")
    print("itertools.batched signature ->", inspect.signature(itertools.batched))
    print("official docs ->", BATCHED_DOCS)
    print(
        "strict=False result ->",
        list(itertools.batched("ABCDE", 2, strict=False)),
    )
    try:
        list(itertools.batched("ABCDE", 2, strict=True))
    except ValueError as exc:
        print("strict=True exception ->", type(exc).__name__)
    print("Rule: the docs state a contract; the active runtime checks current behavior.")

    section("4. Runtime introspection also has limits")
    predict("Can inspect.getsource() always recover source for a built-in object?")
    try:
        inspect.getsource(itertools.batched)
    except (OSError, TypeError) as exc:
        print("getsource unavailable ->", type(exc).__name__)
    else:
        print("getsource unavailable ->", False)
    fields = (
        "object type",
        "signature",
        "parameter semantics",
        "return value",
        "exceptions",
        "side effects",
        "version changes",
        "implementation notes",
    )
    print("contract checklist ->", fields)
    print("Rule: no single introspection tool replaces the public documentation.")


if __name__ == "__main__":
    main()
