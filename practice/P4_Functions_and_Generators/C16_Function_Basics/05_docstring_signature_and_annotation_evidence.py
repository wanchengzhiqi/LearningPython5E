r"""
Limited docstring, signature, callable, and annotation evidence.

Run:
    python practice\P4_Functions_and_Generators\C16_Function_Basics\05_docstring_signature_and_annotation_evidence.py
"""

import inspect


def normalize_key(key: str) -> str:
    """Return a stripped, lowercase localization key."""

    return key.strip().lower()


def echo_label(label: str) -> str:
    """Return the supplied object unchanged for an annotation experiment."""

    return label


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. A docstring is metadata, not the business return")
    predict("Are normalize_key.__doc__ and normalize_key(' X ') the same object?")
    business_result = normalize_key(" MENU.Start ")
    print("__doc__ ->", normalize_key.__doc__)
    print("inspect.getdoc() ->", inspect.getdoc(normalize_key))
    print("business result ->", business_result)
    print("Rule: metadata describes a function; calling executes its body.")

    section("2. A signature describes the call shape presented to inspect")
    predict("Does Signature.bind() call normalize_key or validate business types?")
    signature = inspect.signature(normalize_key)
    bound = signature.bind(" MENU.Quit ")
    print("signature ->", signature)
    print("bound arguments ->", dict(bound.arguments))
    print("call performed by bind ->", False)
    print("Rule: binding maps arguments to this Signature; it does not run the body.")

    section("3. Annotations are metadata, not automatic runtime enforcement")
    predict("Will echo_label reject an integer because its annotation says str?")
    unexpected_type_result = echo_label(404)
    print("annotations ->", echo_label.__annotations__)
    print("echo_label(404) ->", unexpected_type_result)
    print("result type ->", type(unexpected_type_result).__name__)
    print("Rule: Python did not enforce the annotation during this call.")

    section("4. Shape evidence cannot guarantee body success")
    predict("Can a value bind successfully and still fail in the function body?")
    integer_binding = signature.bind(404)
    print("integer binding ->", dict(integer_binding.arguments))
    try:
        normalize_key(404)
    except AttributeError as error:
        print("call exception type ->", type(error).__name__)
    print("callable(normalize_key) ->", callable(normalize_key))
    print(
        "Boundary: callable, signatures, and annotations are limited evidence, "
        "not complete behavior contracts."
    )

    section("5. This experiment keeps introspection risk in scope")
    predict("Does safe observation of these ordinary functions prove all objects safe?")
    print("inspected objects defined in this file ->", True)
    print(
        "Safety: runtime introspection of custom objects may execute attribute "
        "protocols; this result does not generalize to untrusted objects."
    )


if __name__ == "__main__":
    main()
