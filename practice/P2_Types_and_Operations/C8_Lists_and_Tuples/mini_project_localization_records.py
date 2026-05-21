"""
Mini project: localization record observer and batch checker.

This stage-end practice tool keeps the object model visible:

    list collection -> tuple/namedtuple record -> element references -> display

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --issues-only
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --input records.json
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --input records.csv --report-json
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --copy-demo
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --shared-tags-demo
"""

import argparse
import copy
import csv
import json
import string
from collections import Counter, namedtuple
from pathlib import Path


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


def normalize_tags(value, index):
    if value is None:
        return ()
    if isinstance(value, str):
        return tuple(tag.strip() for tag in value.split(";") if tag.strip())
    if isinstance(value, (list, tuple)):
        return tuple(str(tag).strip() for tag in value if str(tag).strip())
    raise ValueError(f"record {index}: tags must be a list, tuple, semicolon string, or null")


def normalize_text(value):
    if value is None:
        return ""
    return str(value)


def record_from_mapping(data, index):
    required_fields = ("key", "source", "translation")
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f"record {index}: missing required field(s): {', '.join(missing)}")

    key = normalize_text(data["key"])
    if not key.strip():
        raise ValueError(f"record {index}: key cannot be empty")

    return Record(
        key,
        normalize_text(data["source"]),
        normalize_text(data["translation"]),
        normalize_tags(data.get("tags", ()), index),
    )


def record_from_sequence(data, index):
    if len(data) not in (3, 4):
        raise ValueError(f"record {index}: expected 3 or 4 fields, got {len(data)}")

    key = normalize_text(data[0])
    if not key.strip():
        raise ValueError(f"record {index}: key cannot be empty")

    tags = data[3] if len(data) == 4 else ()
    return Record(
        key,
        normalize_text(data[1]),
        normalize_text(data[2]),
        normalize_tags(tags, index),
    )


def record_from_data(data, index):
    if isinstance(data, dict):
        return record_from_mapping(data, index)
    if isinstance(data, (list, tuple)):
        return record_from_sequence(data, index)
    raise ValueError(f"record {index}: expected an object or list, got {type(data).__name__}")


def load_json_records(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        if "records" not in data:
            raise ValueError("JSON input must be a list or an object with a 'records' list")
        data = data["records"]
    if not isinstance(data, list):
        raise ValueError("JSON input must contain a list of records")
    return [record_from_data(item, index) for index, item in enumerate(data)]


def load_csv_records(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("CSV input must include a header row")
        required_fields = {"key", "source", "translation"}
        missing = sorted(required_fields - set(reader.fieldnames))
        if missing:
            raise ValueError(f"CSV input missing required column(s): {', '.join(missing)}")
        return [record_from_mapping(row, index) for index, row in enumerate(reader)]


def load_records(path_text):
    path = Path(path_text)
    suffix = path.suffix.lower()
    if suffix == ".json":
        return load_json_records(path)
    if suffix == ".csv":
        return load_csv_records(path)
    raise ValueError("input file must use .json or .csv")


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

    def field_marker(field_name, format_spec, conversion):
        marker = "{}" if field_name == "" else field_name
        if conversion:
            marker = f"{marker}!{conversion}"
        if format_spec:
            marker = f"{marker}:{format_spec}"
        return marker

    def collect_fields(source):
        try:
            fields = FORMATTER.parse(source)
            for _, field_name, format_spec, conversion in fields:
                if field_name is not None:
                    names.append(field_marker(field_name, format_spec, conversion))
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


def percent_placeholder_summary(placeholders):
    named = []
    positional = []
    for placeholder in placeholders:
        if placeholder.startswith("%("):
            named.append(placeholder)
        else:
            positional.append(placeholder)
    return {
        "named": placeholder_counts(named),
        "positional": positional,
    }


def placeholder_report(text):
    fields, errors = parse_format_fields(text)
    percent_fields = percent_placeholders(text)
    return {
        "format_fields": fields,
        "format_errors": errors,
        "percent_fields": percent_fields,
        "percent_summary": percent_placeholder_summary(percent_fields),
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

    if source_report["percent_summary"] != translated_report["percent_summary"]:
        issues.append(
            "percent placeholder mismatch: "
            f"source={source_report['percent_summary']} "
            f"translation={translated_report['percent_summary']}"
        )

    return issues


def record_issues(record, max_length):
    issues = []
    if not record.translation.strip():
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


def record_to_dict(record):
    return {
        "key": record.key,
        "source": record.source,
        "translation": record.translation,
        "tags": list(record.tags),
    }


def issue_report_data(records, max_length, source_name):
    problems = issue_report(records, max_length)
    return {
        "source": source_name,
        "max_length": max_length,
        "records_checked": len(records),
        "duplicate_keys": duplicate_keys(records),
        "issue_count": len(problems),
        "issues": [
            {
                "index": index,
                "record": record_to_dict(record),
                "issues": issues,
            }
            for index, record, issues in problems
        ],
    }


def dump_issue_report_json(data, output_path=None):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output_path:
        Path(output_path).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


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


def run_demo(
    max_length,
    sort_by=None,
    issues_only=False,
    input_path=None,
    report_json=False,
    json_output=None,
):
    if input_path:
        records = load_records(input_path)
        source_name = input_path
    else:
        records = demo_records()
        source_name = "built-in demo"

    if sort_by:
        records = sorted_records(records, sort_by)

    if report_json or json_output:
        data = issue_report_data(records, max_length, source_name)
        if json_output:
            dump_issue_report_json(data, json_output)
        if report_json:
            dump_issue_report_json(data)
        return

    if not issues_only:
        section("Localization record collection")
        print_collection(records)
    section("Issue report")
    print_issue_report(records, max_length)
    if issues_only or not records:
        return
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
    parser.add_argument("--issues-only", action="store_true", help="Only print the issue report.")
    parser.add_argument("--input", help="Read records from a .json or .csv file instead of built-in demo data.")
    parser.add_argument("--report-json", action="store_true", help="Print the issue report as structured JSON.")
    parser.add_argument("--json-output", help="Write the structured JSON issue report to this file.")
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
    try:
        run_demo(
            args.max_length,
            args.sort_by,
            args.issues_only,
            args.input,
            args.report_json,
            args.json_output,
        )
    except (OSError, ValueError, csv.Error, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
