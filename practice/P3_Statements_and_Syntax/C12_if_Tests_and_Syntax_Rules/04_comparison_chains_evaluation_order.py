r"""
Comparison-chain evaluation order and short-circuit behavior.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\04_comparison_chains_evaluation_order.py
"""

TRACE = []


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def measured(label, value):
    TRACE.append(label)
    print(f"  measured({label!r}) -> {value!r}")
    return value


def main():
    section("1. A comparison chain evaluates its middle expression once")
    predict("How many times will measured('value', 7) run?")
    TRACE.clear()
    result = 0 < measured("value", 7) <= 10
    print("result ->", result)
    print("trace ->", TRACE)

    section("2. Repeating source text can repeat an expensive call")
    predict("How many times will the value-producing call run here?")
    TRACE.clear()
    result = (0 < measured("value", 7)) and (measured("value", 7) <= 10)
    print("result ->", result)
    print("trace ->", TRACE)
    print("Correction: a chain is not mere text replacement with the middle repeated.")

    section("3. A failed earlier comparison skips later expressions")
    predict("Will the high-bound expression be evaluated?")
    TRACE.clear()
    result = measured("low", 10) < measured("value", 7) < measured("high", 20)
    print("result ->", result)
    print("trace ->", TRACE)

    section("4. Successful earlier comparisons continue left to right")
    predict("What is the exact evaluation order?")
    TRACE.clear()
    result = (
        measured("low", 0)
        < measured("value", 7)
        <= measured("high", 10)
    )
    print("result ->", result)
    print("trace ->", TRACE)

    section("5. Store a value when clarity matters more than compactness")
    predict("Can an explicit local name preserve one evaluation?")
    TRACE.clear()
    score = measured("score", 85)
    in_warning_band = 40 <= score < 80
    in_error_band = 80 <= score <= 100
    print("in_warning_band ->", in_warning_band)
    print("in_error_band ->", in_error_band)
    print("trace ->", TRACE)
    print("Rule: explicit binding can make reuse and debugging clearer.")


if __name__ == "__main__":
    main()
