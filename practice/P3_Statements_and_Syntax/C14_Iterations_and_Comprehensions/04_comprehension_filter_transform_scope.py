r"""
List comprehensions: filtering, transformation, and scope boundaries.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\04_comprehension_filter_transform_scope.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def active_labels_with_loop(records):
    labels = []
    for record in records:
        if record.get("enabled", True):
            labels.append(f"{record['key']} -> {record['target']}")
    return labels


def active_labels_with_comprehension(records):
    return [
        f"{record['key']} -> {record['target']}"
        for record in records
        if record.get("enabled", True)
    ]


def main():
    records = [
        {"key": "menu.start", "target": "Start", "enabled": True},
        {"key": "menu.debug", "target": "Debug", "enabled": False},
        {"key": "menu.options", "target": "", "enabled": True},
        {"key": "menu.quit", "target": "Quit", "enabled": True},
    ]

    section("1. A simple filter/projection can become a list comprehension")
    predict("Which enabled records will appear in the final labels?")
    loop_result = active_labels_with_loop(records)
    comprehension_result = active_labels_with_comprehension(records)
    print("loop result          ->", loop_result)
    print("comprehension result ->", comprehension_result)
    print("same result ->", loop_result == comprehension_result)

    section("2. The filter condition is part of the business meaning")
    predict("Does if record.get('target') keep an empty target string?")
    truthy_targets = [record["target"] for record in records if record.get("target")]
    supplied_targets = [record["target"] for record in records if "target" in record]
    print("truthy targets   ->", truthy_targets)
    print("supplied targets ->", supplied_targets)
    print("Correction: empty string may be a real quality issue, not absent data.")

    section("3. List comprehensions are eager")
    predict("Is the result already a list object before we print it?")
    key_lengths = [(record["key"], len(record["key"])) for record in records]
    print("key_lengths ->", key_lengths)
    print("type ->", type(key_lengths).__name__)

    section("4. Comprehension variables do not leak out of the comprehension")
    predict("Which loop variable remains visible after an ordinary for loop?")
    for loop_record in records[:1]:
        pass
    print("ordinary for loop_record ->", loop_record["key"])

    _ = [comp_record["key"] for comp_record in records]
    try:
        print("comprehension comp_record ->", comp_record)  # noqa: F821
    except NameError as exc:
        print("comprehension comp_record ->", type(exc).__name__)
    print("Rule: do not rely on a comprehension variable after the expression ends.")

    section("5. Keep explicit loops when the work has several meanings")
    predict("Which version makes the empty target issue easier to audit?")
    issues = []
    labels = []
    for record in records:
        if not record.get("enabled", True):
            continue
        if record["target"] == "":
            issues.append({"key": record["key"], "kind": "empty-target"})
            continue
        labels.append(f"{record['key']} -> {record['target']}")
    print("labels ->", labels)
    print("issues ->", issues)
    print("Rule: a comprehension is best for one clear projection, not hidden auditing.")


if __name__ == "__main__":
    main()
