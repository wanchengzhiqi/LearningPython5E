"""
Mini project: localization record observer and batch checker.

This stage-end practice tool keeps the object model visible:

    list collection -> tuple/namedtuple record -> element references -> display

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --issues-only
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --copy-demo
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --shared-tags-demo
"""

import argparse
import copy
import string
from collections import Counter, namedtuple


Record = namedtuple("Record", "key source translation tags")
FORMATTER = string.Formatter()
PERCENT_CONVERSIONS = set("diouxXeEfFgGcrsa")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def demo_records():
    return [
        Record("menu.start", "Start", "Start Game", ("ui", "menu")),
        Record("item.count", "{item} x{count}", "{count} x{item}", ("item", "format")),
        Record("system.percent", "100%% complete", "100%% complete", ("system", "percent")),
        Record("dialog.line", "Line 1\nLine 2", "Line 1\\nLine 2", ("dialog", "newline")),
        Record("debug.empty", "Debug only", "", ("debug",)),
        Record("broken.brace", "Press {key", "Press {key", ("format", "broken")),
        Record("value.width", "Value: {value:{width}}", "Value: {value:{width}}", ("format", "nested")),
        Record(
            "quest.long",
            "Find the lost map before the moon rises.",
            "Find the lost map before the moon rises near the old tower gate.",
            ("quest", "length"),
        ),
        Record("menu.start", "Start", "Begin", ("duplicate",)),
    ]


def print_record(record, index=None):
    prefix = f"[{index}] " if index is not None else ""
    print(f"{prefix}record id={id(record)} type={type(record).__name__}")
    print(f"  key         : {record.key!r}")
    print(f"  source      : {record.source!r}")
    print(f"  translation : {record.translation!r}")
    print(f"  tags        : {record.tags!r} id={id(record.tags)} type={type(record.tags).__name__}")


def print_collection(records):
    print(f"records type={type(records).__name__} id={id(records)} len={len(records)}")
    for index, record in enumerate(records):
        print_record(record, index)


def parse_format_fields(text):
    names = []
    errors = []

    def collect_fields(source):
        try:
            fields = FORMATTER.parse(source)
            for _, field_name, format_spec, _ in fields:
                if field_name is not None:
                    if field_name == "":
                        names.append("{}")
                    else:
                        root_name = field_name.split(".", 1)[0].split("[", 1)[0]
                        names.append(root_name)
                if format_spec:
                    collect_fields(format_spec)
        except ValueError as error:
            errors.append(str(error))

    collect_fields(text)
    return names, errors


def percent_placeholders(text):
    placeholders = []
    index = 0
    while index < len(text):
        if text[index] != "%":
            index += 1
            continue

        start = index
        index += 1

        if index < len(text) and text[index] == "%":
            index += 1
            continue

        if index < len(text) and text[index] == "(":
            close_index = text.find(")", index + 1)
            if close_index == -1:
                index = start + 1
                continue
            index = close_index + 1

        while index < len(text) and text[index] in "#0- +":
            index += 1

        if index < len(text) and text[index] == "*":
            index += 1
        else:
            while index < len(text) and text[index].isdigit():
                index += 1

        if index < len(text) and text[index] == ".":
            index += 1
            if index < len(text) and text[index] == "*":
                index += 1
            else:
                while index < len(text) and text[index].isdigit():
                    index += 1

        if index < len(text) and text[index] in "hlL":
            index += 1

        if index < len(text) and text[index] in PERCENT_CONVERSIONS:
            placeholders.append(text[start : index + 1])
            index += 1
        else:
            index = start + 1

    return placeholders


def placeholder_counts(placeholders):
    return dict(sorted(Counter(placeholders).items()))


def placeholder_report(text):
    fields, errors = parse_format_fields(text)
    return {
        "format_fields": fields,
        "format_errors": errors,
        "percent_fields": percent_placeholders(text),
    }


def duplicate_keys(records):
    counts = Counter(record.key for record in records)
    return sorted(key for key, count in counts.items() if count > 1)


def placeholder_issues(record):
    source_report = placeholder_report(record.source)
    translated_report = placeholder_report(record.translation)
    issues = []

    if source_report["format_errors"] or translated_report["format_errors"]:
        issues.append(
            "format syntax error: "
            f"source={source_report['format_errors']} "
            f"translation={translated_report['format_errors']}"
        )
    elif placeholder_counts(source_report["format_fields"]) != placeholder_counts(
        translated_report["format_fields"]
    ):
        issues.append(
            "format placeholder mismatch: "
            f"source={placeholder_counts(source_report['format_fields'])} "
            f"translation={placeholder_counts(translated_report['format_fields'])}"
        )

    if source_report["percent_fields"] != translated_report["percent_fields"]:
        issues.append(
            "percent placeholder mismatch: "
            f"source={source_report['percent_fields']} "
            f"translation={translated_report['percent_fields']}"
        )

    return issues


def record_issues(record, max_length):
    issues = []
    if record.translation == "":
        issues.append("empty translation")
    if len(record.translation) > max_length:
        issues.append(f"translation too long: {len(record.translation)} > {max_length}")
    if ("\n" in record.source) != ("\n" in record.translation):
        issues.append("real newline mismatch")
    if "\\n" in record.translation and "\n" in record.source:
        issues.append("translation uses literal backslash-n where source has a real newline")
    issues.extend(placeholder_issues(record))
    return issues


def issue_report(records, max_length):
    report = []
    duplicate_key_set = set(duplicate_keys(records))
    for index, record in enumerate(records):
        issues = record_issues(record, max_length)
        if record.key in duplicate_key_set:
            issues.append("duplicate key")
        if issues:
            report.append((index, record, issues))
    return report


def print_issue_report(records, max_length):
    duplicate = duplicate_keys(records)
    print("duplicate keys ->", duplicate)
    problems = issue_report(records, max_length)
    if not problems:
        print("No issues found.")
        return
    for index, record, issues in problems:
        print(f"[{index}] {record.key!r}")
        for issue in issues:
            print(f"  - {issue}")


def sorted_records(records, sort_by):
    if sort_by == "key":
        return sorted(records, key=lambda record: record.key)
    if sort_by == "translation_length":
        return sorted(records, key=lambda record: len(record.translation))
    raise ValueError(f"unknown sort key: {sort_by}")


def run_copy_demo():
    section("Copy demo: shallow copy versus deep copy")
    mutable_tags = ["ui"]
    records = [
        Record("menu.start", "Start", "Start Game", mutable_tags),
        Record("menu.quit", "Quit", "Quit Game", ["ui"]),
    ]
    shallow = records[:]
    deep = copy.deepcopy(records)
    print("Before mutation:")
    print_collection(records)
    print("shallow outer id ->", id(shallow))
    print("deep outer id    ->", id(deep))
    records[0].tags.append("reviewed")
    records.append(Record("menu.options", "Options", "Options", ["ui"]))
    print("After records[0].tags.append(...) and records.append(...):")
    print_collection(records)
    print("shallow:")
    print_collection(shallow)
    print("deep:")
    print_collection(deep)
    print("Rule: the shallow copy has its own outer list, but still shares nested mutable tags.")


def run_shared_tags_demo():
    section("Shared tags demo: tuple record cannot protect a mutable element")
    shared_tags = ["ui"]
    records = [
        Record("menu.start", "Start", "Start Game", shared_tags),
        Record("menu.quit", "Quit", "Quit Game", shared_tags),
    ]
    print("Before mutation:")
    print_collection(records)
    records[0].tags.append("shared-change")
    print("After records[0].tags.append('shared-change'):")
    print_collection(records)
    print("records[0].tags is records[1].tags ->", records[0].tags is records[1].tags)
    print("Rule: namedtuple/tuple freezes slots, not the mutable object stored in a slot.")


def run_demo(max_length, sort_by=None, issues_only=False):
    records = demo_records()
    if sort_by:
        records = sorted_records(records, sort_by)
    if not issues_only:
        section("Localization record collection")
        print_collection(records)
    section("Issue report")
    print_issue_report(records, max_length)
    section("Unpacking one record")
    key, source, translation, tags = records[0]
    print("key         ->", key)
    print("source      ->", source)
    print("translation ->", translation)
    print("tags        ->", tags)
    replaced = records[0]._replace(translation="Begin Game")
    print("records[0]  ->", records[0])
    print("replaced    ->", replaced)
    print("Rule: _replace returns a new record; the original record remains unchanged.")


def build_parser():
    parser = argparse.ArgumentParser(description="Observe and check localization records.")
    parser.add_argument("--issues-only", action="store_true", help="Only print records with issues.")
    parser.add_argument("--copy-demo", action="store_true", help="Show shallow/deep copy behavior.")
    parser.add_argument("--shared-tags-demo", action="store_true", help="Show mutable object inside tuple record.")
    parser.add_argument(
        "--sort-by",
        choices=("key", "translation_length"),
        help="Sort records before reporting.",
    )
    parser.add_argument("--max-length", type=int, default=40, help="Maximum translation length.")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.copy_demo:
        run_copy_demo()
        return
    if args.shared_tags_demo:
        run_shared_tags_demo()
        return
    run_demo(args.max_length, args.sort_by, args.issues_only)


if __name__ == "__main__":
    main()
