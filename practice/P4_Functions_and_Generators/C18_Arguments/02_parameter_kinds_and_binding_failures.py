r"""
Five parameter kinds and common argument-binding TypeError paths.

Run:
    python practice\P4_Functions_and_Generators\C18_Arguments\02_parameter_kinds_and_binding_failures.py
"""


strict_body_events = []


def bind_matrix(record_id, /, locale="en-US", *tags, dry_run, **metadata):
    return {
        "record_id": record_id,
        "locale": locale,
        "tags": tags,
        "dry_run": dry_run,
        "metadata": metadata,
    }


def strict_entry(key, locale="en-US", *, dry_run):
    strict_body_events.append((key, locale, dry_run))
    return f"{locale}:{key}"


def positional_identity(record_id, /):
    return record_id


def show_error(label, error):
    print(f"{label} -> {type(error).__name__}")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. One signature can expose all five parameter kinds")
    predict("Which objects do the extra positional and keyword inputs become?")
    bound = bind_matrix(
        "prompt-001",
        "ja-JP",
        "menu",
        "reviewed",
        dry_run=True,
        source="memory",
        priority=2,
    )
    print("record id ->", bound["record_id"])
    print("locale ->", bound["locale"])
    print("collected tags ->", bound["tags"])
    print("keyword-only dry_run ->", bound["dry_run"])
    print("collected metadata ->", bound["metadata"])
    print(
        "Rule: positional-only, positional-or-keyword, var-positional, "
        "keyword-only, and var-keyword parameters have distinct roles."
    )

    section("2. Missing, duplicate, unknown, and excessive inputs are rejected")
    predict("Can any rejected call enter strict_entry's body?")
    try:
        strict_entry(dry_run=True)
    except TypeError as error:
        show_error("missing required key", error)

    try:
        strict_entry("menu.start", key="menu.quit", dry_run=True)
    except TypeError as error:
        show_error("duplicate key assignment", error)

    try:
        strict_entry("menu.start", dry_run=True, verbose=True)
    except TypeError as error:
        show_error("unknown keyword", error)

    try:
        strict_entry("menu.start", "ja-JP", False, dry_run=True)
    except TypeError as error:
        show_error("too many positional arguments", error)

    print("strict body entries ->", tuple(strict_body_events))
    print("Rule: matching failures raise TypeError before the target body runs.")

    section("3. A positional-only parameter cannot be supplied by keyword")
    predict("Does the matching parameter name make keyword use valid?")
    print("positional call ->", positional_identity("prompt-002"))
    try:
        positional_identity(record_id="prompt-002")
    except TypeError as error:
        show_error("positional-only supplied by keyword", error)
    print(
        "Rule: the slash marks parameters to its left as positional-only; "
        "their spelling does not authorize keyword binding."
    )

    section("4. Stable evidence should not depend on full error wording")
    predict("What part of these failures is safe to compare across versions?")
    print("stable exception class ->", TypeError.__name__)
    print(
        "Boundary: exact TypeError messages may vary; the argument shape, "
        "rejected stage, body-entry state, and exception class are the focus."
    )


if __name__ == "__main__":
    main()
