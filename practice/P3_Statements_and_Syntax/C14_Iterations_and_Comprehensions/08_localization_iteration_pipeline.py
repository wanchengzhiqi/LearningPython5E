r"""
Localization resource iteration pipeline with comprehensions and explicit loops.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\08_localization_iteration_pipeline.py
"""

import re


PLACEHOLDER_RE = re.compile(r"\{[a-z_]+\}")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def placeholders(text):
    return set(PLACEHOLDER_RE.findall(text or ""))


def audit_records(records, required_keys):
    report = {
        "completed": True,
        "stats": {"read": 0, "enabled": 0, "valid": 0, "disabled": 0},
        "issues": [],
        "valid_records": [],
    }

    enabled_keys = set()
    for record in records:
        report["stats"]["read"] += 1
        key = record["key"]

        if not record.get("enabled", True):
            report["stats"]["disabled"] += 1
            continue

        report["stats"]["enabled"] += 1
        enabled_keys.add(key)

        if "target" not in record:
            report["completed"] = False
            report["issues"].append({"key": key, "kind": "missing-target"})
            continue

        target = record["target"]
        if target == "":
            report["issues"].append({"key": key, "kind": "empty-target"})
            continue

        source_ph = placeholders(record["source"])
        target_ph = placeholders(target)
        if source_ph != target_ph:
            report["issues"].append(
                {
                    "key": key,
                    "kind": "placeholder-mismatch",
                    "missing": sorted(source_ph - target_ph),
                    "extra": sorted(target_ph - source_ph),
                }
            )
            continue

        report["stats"]["valid"] += 1
        report["valid_records"].append({"key": key, "target": target})

    for missing_key in sorted(required_keys - enabled_keys):
        report["issues"].append({"key": missing_key, "kind": "missing-enabled-key"})

    return report


def main():
    records = [
        {"key": "menu.start", "source": "Start {player}", "target": "Start {player}"},
        {"key": "menu.debug", "source": "Debug", "target": "Debug", "enabled": False},
        {"key": "menu.options", "source": "Options", "target": ""},
        {"key": "menu.score", "source": "Score {points}", "target": "Score"},
        {"key": "menu.quit", "source": "Quit"},
    ]
    required_keys = {"menu.start", "menu.options", "menu.score", "menu.quit", "menu.credits"}

    section("1. Simple filtering and projection are good comprehension jobs")
    predict("Which records are enabled, and which keys do they expose?")
    enabled_records = [record for record in records if record.get("enabled", True)]
    enabled_keys = [record["key"] for record in enabled_records]
    present_key_set = {record["key"] for record in enabled_records}
    print("enabled_keys ->", enabled_keys)
    print("stable present keys ->", sorted(present_key_set))
    print("missing required keys ->", sorted(required_keys - present_key_set))

    section("2. Multi-step auditing stays clearer as an explicit loop")
    predict("Which issues are ordinary, and which one marks completed=False?")
    report = audit_records(records, required_keys)
    print("completed ->", report["completed"])
    print("stats ->", report["stats"])
    print("issues ->", report["issues"])
    print("valid_records ->", report["valid_records"])

    section("3. Comprehensions can summarize an already structured report")
    predict("What compact issue lines should a human review see?")
    issue_lines = [
        f"{issue['key']}:{issue['kind']}"
        for issue in sorted(report["issues"], key=lambda item: (item["key"], item["kind"]))
    ]
    print("issue_lines ->", issue_lines)

    section("4. any() is useful after issue objects already exist")
    predict("Will any() inspect every issue after it finds missing-target?")
    has_missing_target = any(issue["kind"] == "missing-target" for issue in report["issues"])
    has_placeholder_mismatch = any(
        issue["kind"] == "placeholder-mismatch" for issue in report["issues"]
    )
    print("has_missing_target ->", has_missing_target)
    print("has_placeholder_mismatch ->", has_placeholder_mismatch)
    print("Rule: build explicit data first; then use comprehensions for clean summaries.")


if __name__ == "__main__":
    main()
