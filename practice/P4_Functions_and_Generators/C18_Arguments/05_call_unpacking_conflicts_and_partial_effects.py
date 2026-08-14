r"""
Call-side * and ** unpacking, conflicts, and effects before rejection.

Run:
    python practice\P4_Functions_and_Generators\C18_Arguments\05_call_unpacking_conflicts_and_partial_effects.py
"""


unpack_events = []


def positional_source():
    unpack_events.append("positional source")
    return ("menu.start", "ja-JP")


def keyword_source():
    unpack_events.append("keyword source")
    return {"dry_run": True}


def evaluate_keyword(label, value):
    unpack_events.append(label)
    return value


def conflicting_keyword_source():
    unpack_events.append("conflicting keyword source")
    return {"dry_run": False}


def audit_entry(key, locale, *, dry_run):
    unpack_events.append("body")
    return {
        "key": key,
        "locale": locale,
        "dry_run": dry_run,
    }


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Call-side * and ** unpack sources before matching")
    predict("In what order are the two source expressions and body observed?")
    result = audit_entry(*positional_source(), **keyword_source())
    print("event order ->", tuple(unpack_events))
    print("result ->", result)
    print(
        "Rule: * supplies positional items and ** supplies string-keyed "
        "keyword items to the call being assembled."
    )

    section("2. One parameter cannot receive both positional and keyword values")
    predict("Will a duplicate locale assignment enter audit_entry's body?")
    unpack_events.clear()
    try:
        audit_entry(
            *positional_source(),
            locale=evaluate_keyword("explicit locale", "fr-FR"),
            dry_run=True,
        )
    except TypeError as error:
        print("exception type ->", type(error).__name__)
    print("events before rejection ->", tuple(unpack_events))
    print("body entered ->", "body" in unpack_events)
    print(
        "Rule: the unpacked second positional item and explicit locale keyword "
        "target the same parameter, so matching rejects the call."
    )

    section("3. Duplicate keywords across explicit input and **mapping reject the call")
    predict("Are mapping-source effects undone when duplicate dry_run is found?")
    unpack_events.clear()
    try:
        audit_entry(
            "dialog.ok",
            "en-US",
            dry_run=evaluate_keyword("explicit dry_run", True),
            **conflicting_keyword_source(),
        )
    except TypeError as error:
        print("exception type ->", type(error).__name__)
    print("events before rejection ->", tuple(unpack_events))
    print("body entered ->", "body" in unpack_events)
    print(
        "Rule: evaluated argument sources keep their completed effects even "
        "though duplicate keyword assembly fails before body entry."
    )

    section("4. Collection and unpacking are opposite call boundaries")
    predict("Does call-side ** create a **kwargs parameter in the target?")
    print("target accepts arbitrary keywords ->", False)
    print("successful keyword source keys ->", tuple(keyword_source()))
    print(
        "Boundary: call-side unpacking supplies inputs; definition-side "
        "*args/**kwargs decides whether and how surplus inputs are collected."
    )


if __name__ == "__main__":
    main()
