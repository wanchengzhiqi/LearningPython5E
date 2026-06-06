r"""
Sequential execution and a minimal control-flow preview.

Run:
    python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\04_order_and_control_flow_preview.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def record(events, label):
    print("running ->", label)
    events.append(label)
    return label.upper()


def run_localization_batch(review_enabled):
    events = []
    record(events, "1 load resource table")
    record(events, "2 parse rule config")

    if review_enabled:
        record(events, "3 run manual review block")

    record(events, "4 write summary report")
    return events


def main():
    section("1. Top-level statements run in order")
    predict("In what order will the first three record() calls run?")
    events = []
    first_return = record(events, "A load source JSON")
    second_return = record(events, "B load target JSON")
    third_return = record(events, "C compare keys")
    print("events ->", events)
    print("returns ->", [first_return, second_return, third_return])
    print("Rule: each expression statement calls record(), then discards its return value.")

    section("2. Control flow can skip an indented block")
    predict("Which event is missing when review_enabled is False?")
    without_review = run_localization_batch(review_enabled=False)
    print("without_review ->", without_review)

    section("3. The same source block can run when control enters it")
    predict("Which event appears when review_enabled is True?")
    with_review = run_localization_batch(review_enabled=True)
    print("with_review ->", with_review)
    print("Rule: source order matters, but control flow decides whether a block executes.")


if __name__ == "__main__":
    main()
