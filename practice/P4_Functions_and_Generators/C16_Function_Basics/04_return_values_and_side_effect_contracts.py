r"""
Returned data, display, mutation, and controlled I/O as separate effects.

Run:
    python practice\P4_Functions_and_Generators\C16_Function_Basics\04_return_values_and_side_effect_contracts.py
"""

from io import StringIO


def build_missing_report(source_keys, target_keys):
    missing = sorted(set(source_keys) - set(target_keys))
    return {
        "missing_count": len(missing),
        "missing_keys": missing,
    }


def display_report(report, output):
    print("missing count:", report["missing_count"], file=output)
    for key in report["missing_keys"]:
        print("missing:", key, file=output)


def normalize_tags_in_place(tags):
    tags[:] = [tag.strip().lower() for tag in tags]


def write_summary(report, output):
    text = "missing=" + ",".join(report["missing_keys"])
    return output.write(text)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. A structured return gives program data to the caller")
    predict("Does building the report need to display or persist it?")
    source_keys = {"menu.start", "menu.quit", "menu.options"}
    target_keys = {"menu.start"}
    source_before = source_keys.copy()
    report = build_missing_report(source_keys, target_keys)
    print("report type ->", type(report).__name__)
    print("report ->", report)
    print("source unchanged ->", source_keys == source_before)
    print("Rule: a return contract can stay separate from presentation.")

    section("2. Display output is an effect; its return is still None")
    predict("What object does display_report return after writing text?")
    display_buffer = StringIO()
    display_result = display_report(report, display_buffer)
    print("display result is None ->", display_result is None)
    print("captured display ->", display_buffer.getvalue().splitlines())
    print("Rule: visible or captured text is not the function's return object.")

    section("3. Argument-object mutation is another independent effect")
    predict("Will the caller's alias observe slice assignment inside the call?")
    tags = [" UI ", "Menu", " ACCESSIBILITY "]
    same_list = tags
    mutation_result = normalize_tags_in_place(tags)
    print("mutation result is None ->", mutation_result is None)
    print("same_list is tags ->", same_list is tags)
    print("tags after call ->", tags)
    print("Rule: mutation changes the shared object; it is not a returned report.")

    section("4. An I/O effect and a returned count remain separate")
    predict("Does write_summary return the text or the write count?")
    output_buffer = StringIO()
    written_count = write_summary(report, output_buffer)
    print("returned write count ->", written_count)
    print("buffer content ->", output_buffer.getvalue())
    print(
        "Boundary: StringIO is controlled in-memory I/O, not proof of file or "
        "database persistence behavior."
    )


if __name__ == "__main__":
    main()
