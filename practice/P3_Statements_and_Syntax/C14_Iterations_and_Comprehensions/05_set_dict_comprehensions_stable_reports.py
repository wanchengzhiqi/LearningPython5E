r"""
Set and dict comprehensions for deduplication, mapping, and stable reports.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\05_set_dict_comprehensions_stable_reports.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def find_duplicate_keys(records):
    seen = set()
    duplicates = []
    for record in records:
        key = record["key"]
        if key in seen:
            duplicates.append(key)
            continue
        seen.add(key)
    return duplicates


def main():
    records = [
        {"key": "menu.start", "target": "Start", "category": "menu", "tags": ["ui", "menu"]},
        {"key": "menu.quit", "target": "Quit", "category": "menu", "tags": ["ui"]},
        {"key": "battle.win", "target": "Victory", "category": "battle", "tags": ["battle", "ui"]},
        {"key": "menu.start", "target": "Begin", "category": "menu", "tags": ["duplicate"]},
    ]
    issues = [
        {"key": "menu.options", "kind": "missing-target"},
        {"key": "battle.win", "kind": "placeholder-mismatch"},
        {"key": "menu.start", "kind": "duplicate-key"},
    ]

    section("1. Set comprehensions deduplicate, but do not preserve business order")
    predict("Which categories and tags remain after deduplication?")
    categories = {record["category"] for record in records}
    tags = {tag for record in records for tag in record["tags"]}
    print("raw category set ->", categories)
    print("stable categories ->", sorted(categories))
    print("stable tags ->", sorted(tags))
    print("Rule: use sorted(...) when a report must be stable and reviewable.")

    section("2. Dict comprehensions map keys to values, but duplicate keys overwrite")
    predict("Which target survives for the duplicated menu.start key?")
    target_by_key = {record["key"]: record["target"] for record in records}
    print("target_by_key ->", target_by_key)
    print("menu.start target ->", target_by_key["menu.start"])
    print("duplicates ->", find_duplicate_keys(records))
    print("Correction: a dict comprehension is not a duplicate-key audit by itself.")

    section("3. Dict comprehensions are good for clean one-to-one projections")
    predict("Which issue summary keeps one compact value per issue key?")
    first_issue_by_key = {issue["key"]: issue["kind"] for issue in issues}
    print("first_issue_by_key ->", first_issue_by_key)
    print("sorted issue keys ->", sorted(first_issue_by_key))

    section("4. Stable issue summaries should make ordering explicit")
    predict("What order should a human review see?")
    stable_issue_lines = [
        f"{issue['key']}:{issue['kind']}"
        for issue in sorted(issues, key=lambda item: (item["key"], item["kind"]))
    ]
    print("stable issue lines ->", stable_issue_lines)
    print("Rule: comprehensions can build reports, but sorting is a separate decision.")


if __name__ == "__main__":
    main()
