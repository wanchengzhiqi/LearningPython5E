r"""
Lambda boundaries, function annotations, Callable, and evidence limits.

Run:
    python practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\06_lambda_annotations_callable_and_evidence_limits.py
"""

import inspect
from collections.abc import Callable


TextRule = Callable[[str], str]


def apply_rule(text: str, rule: TextRule) -> str:
    return rule(text)


def normalize_with_def(text: str) -> str:
    normalized = text.strip().casefold()
    return normalized


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. lambda creates a function object with ordinary call behavior")
    predict("Is a lambda expression executed now, or is its body run when called?")
    normalize_with_lambda = lambda text: text.strip().casefold()
    print("lambda is callable ->", callable(normalize_with_lambda))
    print("lambda name ->", normalize_with_lambda.__name__)
    print("lambda signature ->", inspect.signature(normalize_with_lambda))
    print("lambda result ->", normalize_with_lambda(" Menu.Start "))
    print("def result ->", normalize_with_def(" Menu.Start "))
    print(
        "Rule: lambda creates a function object whose single expression runs "
        "when the function is called; it has no special value-capture rule."
    )

    section("2. lambda is useful for a short local key or callback")
    predict("Which record is selected first by the lambda sorting key?")
    records = (
        {"key": "menu.quit", "priority": 20},
        {"key": "menu.start", "priority": 10},
    )
    ordered = sorted(records, key=lambda record: record["priority"])
    print("ordered keys ->", tuple(record["key"] for record in ordered))
    print(
        "Boundary: a short local expression can be clear as lambda; multi-step "
        "validation, branching, or reusable business behavior is clearer as def."
    )

    section("3. Annotations and Callable describe limited design intent")
    predict("What metadata is visible without calling apply_rule?")
    annotations = apply_rule.__annotations__
    print("annotation keys ->", tuple(annotations))
    print("text annotation is str ->", annotations["text"] is str)
    print("rule annotation matches TextRule ->", annotations["rule"] == TextRule)
    print("return annotation is str ->", annotations["return"] is str)
    print("visible signature ->", inspect.signature(apply_rule))
    print(
        "Rule: the annotations describe intended inputs and output; Callable "
        "describes a callable shape for tools and readers."
    )

    section("4. Metadata and callable() do not enforce the runtime contract")
    predict("Will Python reject wrong values before the function bodies run?")
    wrong_return = apply_rule("menu.start", lambda text: 123)
    print("annotated call returned ->", wrong_return)
    print("returned type ->", type(wrong_return).__name__)

    try:
        apply_rule(404, normalize_with_lambda)
    except AttributeError as error:
        print("wrong text exception ->", type(error).__name__)

    wrong_shape = lambda: "ready"
    print("wrong_shape is callable ->", callable(wrong_shape))
    try:
        apply_rule("menu.quit", wrong_shape)
    except TypeError as error:
        print("wrong shape exception ->", type(error).__name__)

    print(
        "Boundary: annotations, Callable, signatures, and callable() do not "
        "prove runtime types, return values, exceptions, side effects, or "
        "business correctness."
    )


if __name__ == "__main__":
    main()
