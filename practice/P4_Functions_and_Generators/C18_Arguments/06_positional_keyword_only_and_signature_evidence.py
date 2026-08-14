r"""
Positional-only, keyword-only, and limited inspect.signature evidence.

Run:
    python practice\P4_Functions_and_Generators\C18_Arguments\06_positional_keyword_only_and_signature_evidence.py
"""

import inspect


body_events = []


def render_record(record_id, /, text, *, locale="en-US", show_content=True):
    body_events.append(record_id)
    normalized = text.strip()
    return {
        "record_id": record_id,
        "label": f"{locale}:{normalized}",
        "show_content": show_content,
    }


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    signature = inspect.signature(render_record)

    section("1. Slash and star express positional-only and keyword-only intent")
    predict("Which parameter kind does each name expose?")
    kinds = tuple(
        (name, parameter.kind.name)
        for name, parameter in signature.parameters.items()
    )
    print("visible signature ->", signature)
    print("parameter kinds ->", kinds)
    print(
        "Rule: record_id is positional-only; locale and show_content are "
        "keyword-only; text is positional-or-keyword."
    )

    section("2. Signature.bind maps a call shape without executing the body")
    predict("Does successful binding append a body event?")
    bound = signature.bind(
        "prompt-001",
        " Start ",
        locale="ja-JP",
        show_content=False,
    )
    print("bound arguments ->", tuple(bound.arguments.items()))
    print("body events after bind ->", tuple(body_events))
    print(
        "Rule: bind validates and maps this call shape; it does not invoke "
        "render_record."
    )

    section("3. A real call enters the body and produces behavior evidence")
    predict("What additional evidence appears only after the actual call?")
    result = render_record(
        "prompt-001",
        " Start ",
        locale="ja-JP",
        show_content=False,
    )
    print("result ->", result)
    print("body events after real call ->", tuple(body_events))
    print("Rule: the real call adds body, result, and observed behavior evidence.")

    section("4. Shape success does not prove body or business success")
    predict("Can an integer bind to text even though the body calls text.strip()?")
    mismatched = signature.bind("prompt-002", 404)
    print("shape with integer bound ->", tuple(mismatched.arguments.items()))
    print("body events unchanged by bind ->", tuple(body_events))
    try:
        render_record("prompt-002", 404)
    except AttributeError as error:
        print("real-call exception type ->", type(error).__name__)
    print("body events after failed real call ->", tuple(body_events))

    try:
        signature.bind(record_id="prompt-003", text="Quit")
    except TypeError as error:
        print("positional-only bind failure ->", type(error).__name__)

    try:
        signature.bind("prompt-004", "Quit", "fr-FR")
    except TypeError as error:
        print("keyword-only bind failure ->", type(error).__name__)

    print(
        "Boundary: visible signatures can be customized, and successful bind "
        "does not prove types, body completion, results, side effects, or the "
        "business contract."
    )


if __name__ == "__main__":
    main()
