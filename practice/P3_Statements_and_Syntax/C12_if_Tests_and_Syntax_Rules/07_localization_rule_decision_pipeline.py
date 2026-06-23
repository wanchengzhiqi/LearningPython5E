r"""
A localization-rule decision pipeline built from C12 condition semantics.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\07_localization_rule_decision_pipeline.py
"""

VALID_OUTPUT_MODES = {"text", "json"}
VALID_SEVERITIES = {"info", "warning", "error"}


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def unique_list(values):
    return list(dict.fromkeys(values))


def decide_report(
    *,
    strict,
    dry_run,
    missing_keys,
    empty_keys,
    output_mode,
    severity,
):
    """Return a structured decision without writing files or mutating inputs."""

    if output_mode not in VALID_OUTPUT_MODES:
        return {
            "status": "invalid",
            "reason": f"unsupported output mode: {output_mode}",
        }
    if severity not in VALID_SEVERITIES:
        return {
            "status": "invalid",
            "reason": f"unsupported severity: {severity}",
        }

    missing = unique_list(missing_keys)
    empty = unique_list(empty_keys)
    has_issues = bool(missing or empty)

    # Both operands below are bool objects, so this particular or expression
    # also returns a bool. That is a fact about these operands, not a general
    # promise made by the or operator.
    is_blocking = severity == "error" or (strict and has_issues)

    if is_blocking:
        status = "blocked"
        next_step = "stop pipeline and request correction"
    elif has_issues:
        status = "review"
        next_step = "emit report and continue"
    else:
        status = "clean"
        next_step = "emit clean summary"

    action = "preview only" if dry_run else "emit report"
    target = "JSON report" if output_mode == "json" else "text report"

    return {
        "status": status,
        "action": action,
        "target": target,
        "next_step": next_step,
        "strict": strict,
        "dry_run": dry_run,
        "severity": severity,
        "missing_keys": missing,
        "empty_keys": empty,
    }


def main():
    section("1. Predict the decision path before reading each result")
    predict("Which cases are blocked, review, clean, or invalid?")
    scenarios = [
        {
            "name": "strict preview with a missing key",
            "strict": True,
            "dry_run": True,
            "missing_keys": ["menu.quit"],
            "empty_keys": [],
            "output_mode": "json",
            "severity": "warning",
        },
        {
            "name": "non-strict write with an empty translation",
            "strict": False,
            "dry_run": False,
            "missing_keys": [],
            "empty_keys": ["menu.start"],
            "output_mode": "text",
            "severity": "warning",
        },
        {
            "name": "clean JSON report",
            "strict": False,
            "dry_run": False,
            "missing_keys": [],
            "empty_keys": [],
            "output_mode": "json",
            "severity": "info",
        },
        {
            "name": "error-severity issue",
            "strict": False,
            "dry_run": False,
            "missing_keys": ["menu.options"],
            "empty_keys": [],
            "output_mode": "text",
            "severity": "error",
        },
        {
            "name": "unsupported XML output",
            "strict": False,
            "dry_run": True,
            "missing_keys": [],
            "empty_keys": [],
            "output_mode": "xml",
            "severity": "info",
        },
    ]

    for scenario in scenarios:
        name = scenario["name"]
        inputs = {
            key: value
            for key, value in scenario.items()
            if key != "name"
        }
        decision = decide_report(**inputs)
        print()
        print(name)
        print("  decision ->", decision)

    section("2. Input lists were not mutated")
    predict("Will deduplication modify the caller's original list?")
    missing_keys = ["menu.quit", "menu.quit"]
    before = missing_keys.copy()
    decision = decide_report(
        strict=False,
        dry_run=True,
        missing_keys=missing_keys,
        empty_keys=[],
        output_mode="json",
        severity="warning",
    )
    print("original ->", missing_keys)
    print("unchanged ->", missing_keys == before)
    print("decision missing_keys ->", decision["missing_keys"])

    section("3. Trace the four layers")
    print("1. Conditions are evaluated.")
    print("2. Their result objects participate in truth testing.")
    print("3. if/elif/else selects exactly one decision block.")
    print("4. This function returns data; it performs no report-writing side effect.")


if __name__ == "__main__":
    main()
