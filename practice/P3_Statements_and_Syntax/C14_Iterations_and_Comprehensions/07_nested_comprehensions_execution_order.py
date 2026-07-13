r"""
Nested comprehensions and their equivalent explicit loop order.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\07_nested_comprehensions_execution_order.py
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
    return set(PLACEHOLDER_RE.findall(text))


def build_pairs_with_loop(locales, keys):
    pairs = []
    for locale in locales:
        for key in keys:
            pairs.append((locale, key))
    return pairs


def build_placeholder_report(records):
    report = []
    for record in records:
        source_ph = placeholders(record["source"])
        target_ph = placeholders(record["target"])
        if source_ph != target_ph:
            report.append(
                {
                    "key": record["key"],
                    "missing": sorted(source_ph - target_ph),
                    "extra": sorted(target_ph - source_ph),
                }
            )
    return report


def main():
    locales = ["zh_CN", "ja_JP"]
    required_keys = ["menu.start", "menu.quit", "menu.options"]
    available = {
        "zh_CN": {"menu.start", "menu.quit"},
        "ja_JP": {"menu.start", "menu.options"},
    }
    records = [
        {"key": "menu.start", "source": "Start {player}", "target": "Start {player}"},
        {"key": "menu.score", "source": "Score {points}", "target": "Score"},
        {"key": "menu.rank", "source": "Rank", "target": "Rank {rank}"},
    ]

    section("1. Nested comprehension order matches nested for-loop order")
    predict("Which loop is outer, locale or key?")
    loop_pairs = build_pairs_with_loop(locales, required_keys)
    comprehension_pairs = [(locale, key) for locale in locales for key in required_keys]
    print("loop pairs          ->", loop_pairs)
    print("comprehension pairs ->", comprehension_pairs)
    print("same order ->", loop_pairs == comprehension_pairs)
    print("Rule: read nested comprehension clauses from left to right.")

    section("2. The trailing if filters the innermost produced item")
    predict("Which locale/key pairs are missing from available?")
    missing_pairs = [
        (locale, key)
        for locale in locales
        for key in required_keys
        if key not in available[locale]
    ]
    print("missing_pairs ->", missing_pairs)

    section("3. Flatten nested data when the result stays simple")
    predict("Which placeholders appear in each source string?")
    placeholder_pairs = [
        (record["key"], placeholder)
        for record in records
        for placeholder in sorted(placeholders(record["source"]))
    ]
    print("placeholder_pairs ->", placeholder_pairs)

    section("4. Keep a loop when the report needs named intermediate states")
    predict("Which records have missing or extra placeholders?")
    dense_mismatch_keys = [
        record["key"]
        for record in records
        if placeholders(record["source"]) != placeholders(record["target"])
    ]
    explicit_report = build_placeholder_report(records)
    print("dense mismatch keys ->", dense_mismatch_keys)
    print("explicit report ->", explicit_report)
    print("Rule: nested comprehensions are fine for flat projections, not every audit.")


if __name__ == "__main__":
    main()
