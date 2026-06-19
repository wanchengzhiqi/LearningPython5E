r"""
Unpacking assignment and assignment targets beyond simple names.

Run:
    python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\02_unpacking_assignment_targets.py
"""

from dataclasses import dataclass


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_binding(name, value):
    print(f"{name:<18} type={type(value).__name__:<10} id={id(value)} repr={value!r}")


@dataclass
class DraftRecord:
    title: str = ""
    category: str = ""


def main():
    section("1. Basic unpacking assigns multiple targets from one right-side object")
    predict("Which names will receive start_line, end_line, and lines?")
    raw_block = (7, 12, ["# prompt one", "# prompt two"])
    start_line, end_line, lines = raw_block
    show_binding("start_line", start_line)
    show_binding("end_line", end_line)
    show_binding("lines", lines)
    print("Rule: the tuple is unpacked; no new copy of lines is made.")

    section("2. Starred unpacking captures the rest as a new list")
    predict("What is the type of middle after first, *middle, last = tokens?")
    tokens = ["title", "category", "tag:imported", "tag:C11", "content"]
    first, *middle, last = tokens
    show_binding("first", first)
    show_binding("middle", middle)
    show_binding("last", last)
    print("middle is tokens[1:-1] ->", middle is tokens[1:-1])
    print("Rule: the starred target receives a new list containing the remaining items.")

    section("3. Nested unpacking follows the target shape")
    predict("Which part of payload becomes title and category?")
    payload = (42, ("C11 startup", "startup_template_request"), ["imported", "template"])
    record_id, (title, category), tags = payload
    show_binding("record_id", record_id)
    show_binding("title", title)
    show_binding("category", category)
    show_binding("tags", tags)

    section("4. Multiple assignment evaluates the right side before rebinding the left")
    predict("Can active and deleted swap without a temporary variable?")
    active = "active"
    deleted = "deleted"
    active, deleted = deleted, active
    show_binding("active", active)
    show_binding("deleted", deleted)
    print("Rule: right-side values are collected before left-side targets are rebound.")

    section("5. Unpacking size mismatches raise errors instead of half-working silently")
    predict("What happens if there are too few or too many values?")
    for source in [("only-title",), ("title", "category", "extra")]:
        try:
            title, category = source
        except ValueError as exc:
            print(f"unpacking {source!r} failed -> {exc}")
    print("Correction: Python does not guess which extra value you meant to ignore.")

    section("6. Assignment targets can be attributes, subscripts, and slices")
    predict("Which operations rebind names, and which mutate existing objects?")
    draft = DraftRecord()
    fields = {"title": "old title", "category": "old category"}
    content_lines = ["header", "old body", "old footer"]

    draft.title = "新建提示模板"
    fields["category"] = "manual"
    content_lines[1:] = ["body line 1", "body line 2"]

    show_binding("draft", draft)
    show_binding("fields", fields)
    show_binding("content_lines", content_lines)
    print("Rule: attribute, subscript, and slice assignment write into target objects.")


if __name__ == "__main__":
    main()
