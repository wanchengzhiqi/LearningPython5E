r"""
C10-C15 self-check framework for closing P3 Statements and Syntax.

Run:
    python practice\P3_Statements_and_Syntax\C15_The_Documentation_Interlude\06_p3_closer_self_check.py
"""


P3_CHECKLIST = (
    (
        "C10",
        "Which expressions are evaluated, which statements execute, and which "
        "effects are output rather than return values?",
    ),
    (
        "C11",
        "Which names or slots are rebound, which objects mutate, and which "
        "aliases can observe the change?",
    ),
    (
        "C12",
        "Which object reaches a condition, how is its truth tested, and which "
        "branches or side effects are skipped?",
    ),
    (
        "C13",
        "How does each iteration change state, and does the loop end normally, "
        "with continue, with break, or with an exception?",
    ),
    (
        "C14",
        "Which object is iterable, which iterator stores progress, which "
        "consumer advances it, and what tail remains?",
    ),
    (
        "C15",
        "Which claim comes from source, metadata, help output, official docs, "
        "a signature, or a current minimum experiment?",
    ),
)


P4_HANDOFF_QUESTIONS = (
    "What object does a def statement create?",
    "How are call arguments bound to parameter names?",
    "Where does Python resolve a name used inside a function?",
    "Which function behaviors belong in a return contract versus side effects?",
)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def audit_snapshot(records, required_keys):
    enabled_records = [
        record for record in records if record.get("enabled", True)
    ]
    enabled_keys = {record["key"] for record in enabled_records}
    text_by_key = {
        record["key"]: record["target"]
        for record in enabled_records
        if record["target"]
    }
    missing_keys = sorted(required_keys - enabled_keys)
    empty_keys = [
        record["key"]
        for record in enabled_records
        if record["target"] == ""
    ]

    if missing_keys:
        action = "review-missing"
    elif empty_keys:
        action = "review-empty"
    else:
        action = "ready"

    return {
        "action": action,
        "enabled_count": len(enabled_records),
        "text_by_key": text_by_key,
        "missing_keys": missing_keys,
        "empty_keys": empty_keys,
    }


def main():
    section("1. One finite question chain covers the completed P3 chapters")
    predict("Which question belongs to each chapter boundary?")
    for chapter, question in P3_CHECKLIST:
        print(f"{chapter} -> {question}")

    section("2. Apply the chain to a small localization flow")
    predict("What action and report objects result without mutating records?")
    records = [
        {"key": "menu.start", "target": "Start"},
        {"key": "menu.quit", "target": ""},
        {"key": "menu.debug", "target": "Debug", "enabled": False},
    ]
    required_keys = {"menu.start", "menu.quit", "menu.options"}
    report = audit_snapshot(records, required_keys)
    print("records after call ->", records)
    print("report ->", report)
    print("report type ->", type(report).__name__)

    section("3. Human-facing output is still separate from the returned report")
    predict("What object does the display call return?")
    display_result = print("human summary ->", report["action"])
    print("display call returned None ->", display_result is None)
    print("Rule: the report remains structured even when a human summary is shown.")

    section("4. C15 closes P3 by preserving questions for the next PART")
    predict("Do these questions begin systematic P4 teaching?")
    for question in P4_HANDOFF_QUESTIONS:
        print("P4 handoff question ->", question)
    print("Boundary: these are entry questions only; their P4 lessons have not begun.")


if __name__ == "__main__":
    main()
