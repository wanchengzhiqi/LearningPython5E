r"""
Generator expressions are lazy and are often consumed only once.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\06_generator_expressions_lazy_short_circuit.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def trace_enabled(record):
    print("  check enabled ->", record["key"])
    return record.get("enabled", True)


def trace_empty_target(record):
    print("  check empty target ->", record["key"])
    return record.get("target") == ""


def trace_has_target(record):
    print("  check has target ->", record["key"])
    return bool(record.get("target"))


def main():
    records = [
        {"key": "menu.start", "target": "Start", "enabled": True},
        {"key": "menu.debug", "target": "Debug", "enabled": False},
        {"key": "menu.options", "target": "", "enabled": True},
        {"key": "menu.quit", "target": "Quit", "enabled": True},
    ]

    section("1. List comprehensions run eagerly")
    predict("When will trace_enabled() print its messages?")
    print("before list comprehension")
    enabled_keys = [record["key"] for record in records if trace_enabled(record)]
    print("after list comprehension")
    print("enabled_keys ->", enabled_keys)

    section("2. Generator expressions wait until a consumer asks for items")
    predict("Will creating the generator print anything immediately?")
    generated_keys = (record["key"] for record in records if trace_enabled(record))
    print("generator created ->", generated_keys)
    print("first next ->", next(generated_keys))
    print("remaining ->", list(generated_keys))
    print("remaining again ->", list(generated_keys))
    print("Rule: the generator remembered its progress and is now exhausted.")

    section("3. any() short-circuits as soon as it finds a true value")
    predict("How many records will be checked before an empty target is found?")
    print("any empty target ->", any(trace_empty_target(record) for record in records))

    section("4. all() short-circuits as soon as it finds a false value")
    predict("Does an empty string count as a present target for this predicate?")
    print("all have truthy target ->", all(trace_has_target(record) for record in records))
    print("Correction: truthiness may not match the audit meaning of supplied data.")

    section("5. sum() consumes the whole generator expression")
    predict("How many enabled records are counted, and is the generator reusable?")
    counter = (1 for record in records if trace_enabled(record))
    print("enabled count ->", sum(counter))
    print("sum(counter) again ->", sum(counter))
    print("Rule: collect once if later code needs the same sequence again.")


if __name__ == "__main__":
    main()
