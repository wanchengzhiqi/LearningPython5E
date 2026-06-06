r"""
Game localization resource auditor.

This project intentionally keeps Python's core object model visible:

    JSON text files
        -> file objects opened with UTF-8
        -> Python dict mappings and key counters
        -> set/list/namedtuple issue analysis
        -> text report or JSON report

Run:
    python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py
    python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --observe
    python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --format json
"""

import argparse
import csv
import json
import re
import string
import sys
from collections import Counter, namedtuple
from pathlib import Path


Issue = namedtuple("Issue", "severity code key message source target detail")
GlossaryTerm = namedtuple("GlossaryTerm", "source target note")
Resource = namedtuple("Resource", "label path text pairs mapping duplicate_counts")

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / "data" / "source_en.json"
DEFAULT_TARGET = HERE / "data" / "target_zh.json"
DEFAULT_GLOSSARY = HERE / "data" / "glossary.csv"

FORMATTER = string.Formatter()
PERCENT_CONVERSIONS = set("diouxXeEfFgGcrsa")
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


class JsonObjectPairs(list):
    """Marker list used by json.loads(object_pairs_hook=...) to keep duplicate keys observable."""


def build_parser():
    parser = argparse.ArgumentParser(
        description="Audit game localization JSON resources with visible Python object boundaries."
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="source-language JSON resource file")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="target-language JSON resource file")
    parser.add_argument(
        "--glossary",
        help="optional CSV glossary file; defaults to bundled data/glossary.csv when present",
    )
    parser.add_argument("--max-length", type=int, default=42, help="maximum target text length before warning")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="report output format")
    parser.add_argument("--output", help="optional report output path")
    parser.add_argument("--observe", action="store_true", help="include object-model observations")
    return parser


def read_text_file(path, encoding="utf-8"):
    with open(path, "r", encoding=encoding) as file:
        return file.read()


def load_json_resource(path_text, label):
    path = Path(path_text)
    text = read_text_file(path, encoding="utf-8-sig")
    parsed = json.loads(text, object_pairs_hook=JsonObjectPairs)
    if not isinstance(parsed, JsonObjectPairs):
        raise ValueError(f"{label} JSON must be an object mapping keys to strings")

    pairs = []
    for index, pair in enumerate(parsed):
        if len(pair) != 2:
            raise ValueError(f"{label} JSON item {index} is not a key/value pair")
        key, value = pair
        if not isinstance(key, str):
            raise ValueError(f"{label} JSON key at item {index} is not a string")
        if not isinstance(value, str):
            raise ValueError(f"{label} JSON value for {key!r} must be a string")
        pairs.append((key, value))

    mapping = {}
    for key, value in pairs:
        mapping[key] = value

    duplicate_counts = Counter(key for key, _ in pairs)
    return Resource(label, path, text, pairs, mapping, duplicate_counts)


def resolve_glossary_path(path_text):
    if path_text:
        path = Path(path_text)
        if not path.exists():
            raise FileNotFoundError(f"glossary CSV does not exist: {path}")
        return path

    if DEFAULT_GLOSSARY.exists():
        return DEFAULT_GLOSSARY

    return None


def load_glossary(path):
    if path is None:
        return []

    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("glossary CSV must include a header row")
        required = {"source", "target"}
        missing = sorted(required - set(reader.fieldnames))
        if missing:
            raise ValueError(f"glossary CSV missing required column(s): {', '.join(missing)}")
        terms = []
        for row in reader:
            source = (row.get("source") or "").strip()
            target = (row.get("target") or "").strip()
            note = (row.get("note") or "").strip()
            if source and target:
                terms.append(GlossaryTerm(source, target, note))
        return terms


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


def format_fields(text):
    fields = []
    errors = []

    def marker(field_name, format_spec, conversion):
        name = "{}" if field_name == "" else field_name
        if conversion:
            name = f"{name}!{conversion}"
        if format_spec:
            name = f"{name}:{format_spec}"
        return name

    def collect(source):
        try:
            for _, field_name, format_spec, conversion in FORMATTER.parse(source):
                if field_name is not None:
                    fields.append(marker(field_name, format_spec, conversion))
                if format_spec:
                    collect(format_spec)
        except ValueError as error:
            errors.append(str(error))

    collect(text)
    return fields, errors


def placeholder_signature(text):
    format_names, format_errors = format_fields(text)
    percent_names = percent_placeholders(text)
    return {
        "format": Counter(format_names),
        "percent": Counter(percent_names),
        "errors": format_errors,
    }


def make_issue(severity, code, key, message, source="", target="", detail=None):
    return Issue(severity, code, key, message, source, target, detail or {})


def duplicate_values(resource, key):
    return [value for pair_key, value in resource.pairs if pair_key == key]


def duplicate_issues(resource):
    issues = []
    for key, count in sorted(resource.duplicate_counts.items()):
        if count > 1:
            values = duplicate_values(resource, key)
            issues.append(
                make_issue(
                    "error",
                    f"duplicate_{resource.label}_key",
                    key,
                    f"{resource.label} JSON object contains the same key {count} times; Python dict keeps the last value.",
                    detail={
                        "count": count,
                        "pair_values": values,
                        "kept_value": resource.mapping[key],
                    },
                )
            )
    return issues


def compare_placeholders(key, source_text, target_text):
    issues = []
    source_sig = placeholder_signature(source_text)
    target_sig = placeholder_signature(target_text)

    for error in source_sig["errors"]:
        issues.append(make_issue("error", "source_format_syntax", key, error, source_text, target_text))
    for error in target_sig["errors"]:
        issues.append(make_issue("error", "target_format_syntax", key, error, source_text, target_text))

    if source_sig["format"] != target_sig["format"]:
        issues.append(
            make_issue(
                "error",
                "format_placeholder_mismatch",
                key,
                "named format placeholders differ between source and target",
                source_text,
                target_text,
                {
                    "source": dict(source_sig["format"]),
                    "target": dict(target_sig["format"]),
                },
            )
        )

    if source_sig["percent"] != target_sig["percent"]:
        issues.append(
            make_issue(
                "error",
                "percent_placeholder_mismatch",
                key,
                "percent-style placeholders differ between source and target",
                source_text,
                target_text,
                {
                    "source": dict(source_sig["percent"]),
                    "target": dict(target_sig["percent"]),
                },
            )
        )

    return issues


def glossary_issues(key, source_text, target_text, glossary_terms):
    issues = []
    for term in glossary_terms:
        if term.source in source_text and term.target not in target_text:
            issues.append(
                make_issue(
                    "warning",
                    "glossary_mismatch",
                    key,
                    f"source contains glossary term {term.source!r}, but target does not contain {term.target!r}",
                    source_text,
                    target_text,
                    {"term_note": term.note},
                )
            )
    return issues


def audit_resources(source, target, glossary_terms, max_length):
    issues = []
    issues.extend(duplicate_issues(source))
    issues.extend(duplicate_issues(target))

    source_keys = set(source.mapping)
    target_keys = set(target.mapping)

    for key in sorted(source_keys - target_keys):
        issues.append(make_issue("error", "missing_target_key", key, "target file is missing this source key"))

    for key in sorted(target_keys - source_keys):
        issues.append(make_issue("warning", "extra_target_key", key, "target file has no matching source key"))

    for key in sorted(source_keys & target_keys):
        source_text = source.mapping[key]
        target_text = target.mapping[key]

        if not target_text.strip():
            issues.append(make_issue("error", "empty_target", key, "target text is empty", source_text, target_text))

        if len(target_text) > max_length:
            issues.append(
                make_issue(
                    "warning",
                    "target_too_long",
                    key,
                    f"target text length {len(target_text)} exceeds limit {max_length}",
                    source_text,
                    target_text,
                    {"length": len(target_text), "max_length": max_length},
                )
            )

        if source_text.count("\n") != target_text.count("\n") or ("\n" in source_text and "\\n" in target_text):
            issues.append(
                make_issue(
                    "warning",
                    "newline_mismatch",
                    key,
                    "source and target do not preserve newline structure",
                    source_text,
                    target_text,
                    {
                        "source_newlines": source_text.count("\n"),
                        "target_newlines": target_text.count("\n"),
                        "target_literal_backslash_n": "\\n" in target_text,
                    },
                )
            )

        issues.extend(compare_placeholders(key, source_text, target_text))
        issues.extend(glossary_issues(key, source_text, target_text, glossary_terms))

    return sorted(issues, key=lambda issue: (SEVERITY_ORDER[issue.severity], issue.key, issue.code))


def issue_to_dict(issue):
    return {
        "severity": issue.severity,
        "code": issue.code,
        "key": issue.key,
        "message": issue.message,
        "source": issue.source,
        "target": issue.target,
        "detail": issue.detail,
    }


def duplicate_summary(resource):
    return {key: count for key, count in sorted(resource.duplicate_counts.items()) if count > 1}


def duplicate_boundary(resource):
    for key, count in sorted(resource.duplicate_counts.items()):
        if count > 1:
            values = duplicate_values(resource, key)
            return {
                "resource": resource.label,
                "key": key,
                "pair_count": count,
                "pair_values_before_dict_collapse": values,
                "mapping_value_after_dict_collapse": resource.mapping[key],
                "mapping_keeps_last_value": resource.mapping[key] == values[-1],
            }
    return None


def text_bytes_demo(target):
    sample_text = target.mapping.get("menu.start", "")
    sample_bytes = sample_text.encode("utf-8")
    return {
        "sample_text": sample_text,
        "str_length": len(sample_text),
        "utf8_byte_length": len(sample_bytes),
        "utf8_bytes_repr": repr(sample_bytes),
    }


def object_observations(source, target, glossary_terms, issues):
    key_view = source.mapping.keys()
    key_snapshot = list(source.mapping.keys())
    view_demo = dict(source.mapping)
    view = view_demo.keys()
    before_view = list(view)
    view_demo["__observer.demo__"] = "view changed"
    after_view = list(view)

    shallow_original = {"tags": ["ui", "menu"]}
    shallow_copy = shallow_original.copy()
    shallow_copy["tags"].append("reviewed")

    return {
        "path_object_type": type(source.path).__name__,
        "source_text_type": type(source.text).__name__,
        "source_pair_collection_type": type(source.pairs).__name__,
        "source_pair_count_before_dict_collapse": len(source.pairs),
        "source_mapping_type": type(source.mapping).__name__,
        "source_mapping_count_after_dict_collapse": len(source.mapping),
        "source_key_view_type": type(key_view).__name__,
        "source_key_snapshot_type": type(key_snapshot).__name__,
        "source_key_view_repr": repr(key_view),
        "issue_collection_type": type(issues).__name__,
        "issue_record_type": type(issues[0]).__name__ if issues else None,
        "glossary_collection_type": type(glossary_terms).__name__,
        "view_demo": {
            "before": before_view,
            "after": after_view,
            "snapshot_before_mutation": key_snapshot,
        },
        "shallow_copy_demo": {
            "outer_same_object": shallow_original is shallow_copy,
            "inner_tags_same_object": shallow_original["tags"] is shallow_copy["tags"],
            "original_after_copy_mutation": shallow_original,
            "copy_after_copy_mutation": shallow_copy,
        },
        "duplicate_key_boundaries": [
            boundary
            for boundary in (duplicate_boundary(source), duplicate_boundary(target))
            if boundary is not None
        ],
        "text_vs_bytes_demo": text_bytes_demo(target),
        "json_boundary_note": "json.loads created Python objects from text; json.dumps will create report text from Python objects.",
        "target_mapping_type": type(target.mapping).__name__,
    }


def report_data(source, target, glossary_path, glossary_terms, issues, observe):
    source_keys = set(source.mapping)
    target_keys = set(target.mapping)
    severity_counts = Counter(issue.severity for issue in issues)
    code_counts = Counter(issue.code for issue in issues)
    data = {
        "summary": {
            "source_file": str(source.path),
            "target_file": str(target.path),
            "glossary_file": str(glossary_path) if glossary_path is not None else None,
            "glossary_terms": len(glossary_terms),
            "source_key_count": len(source.mapping),
            "target_key_count": len(target.mapping),
            "common_key_count": len(source_keys & target_keys),
            "missing_target_key_count": len(source_keys - target_keys),
            "extra_target_key_count": len(target_keys - source_keys),
            "issue_count": len(issues),
            "issue_counts_by_severity": dict(sorted(severity_counts.items())),
            "issue_counts_by_code": dict(sorted(code_counts.items())),
            "source_duplicate_keys": duplicate_summary(source),
            "target_duplicate_keys": duplicate_summary(target),
        },
        "issues": [issue_to_dict(issue) for issue in issues],
    }
    if observe:
        data["observations"] = object_observations(source, target, glossary_terms, issues)
    return data


def render_text_report(data):
    summary = data["summary"]
    lines = [
        "Localization Resource Auditor",
        "=" * 72,
        f"source_file             : {summary['source_file']}",
        f"target_file             : {summary['target_file']}",
        f"glossary_file           : {summary['glossary_file']}",
        f"glossary_terms          : {summary['glossary_terms']}",
        f"source_key_count        : {summary['source_key_count']}",
        f"target_key_count        : {summary['target_key_count']}",
        f"common_key_count        : {summary['common_key_count']}",
        f"missing_target_key_count: {summary['missing_target_key_count']}",
        f"extra_target_key_count  : {summary['extra_target_key_count']}",
        f"issue_count             : {summary['issue_count']}",
        f"issue_counts_by_severity: {summary['issue_counts_by_severity']}",
        f"issue_counts_by_code    : {summary['issue_counts_by_code']}",
        "",
        "Issues",
        "-" * 72,
    ]

    if not data["issues"]:
        lines.append("No issues found.")
    else:
        for index, issue in enumerate(data["issues"], 1):
            lines.append(f"{index}. [{issue['severity']}] {issue['code']} :: {issue['key']}")
            lines.append(f"   {issue['message']}")
            if issue["source"] or issue["target"]:
                lines.append(f"   source={issue['source']!r}")
                lines.append(f"   target={issue['target']!r}")
            if issue["detail"]:
                lines.append(f"   detail={issue['detail']!r}")

    if "observations" in data:
        lines.extend(["", "Object Observations", "-" * 72])
        for key, value in data["observations"].items():
            lines.append(f"{key}: {value!r}")

    return "\n".join(lines) + "\n"


def render_json_report(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def run(args):
    source = load_json_resource(args.source, "source")
    target = load_json_resource(args.target, "target")
    glossary_path = resolve_glossary_path(args.glossary)
    glossary_terms = load_glossary(glossary_path)
    issues = audit_resources(source, target, glossary_terms, args.max_length)
    data = report_data(source, target, glossary_path, glossary_terms, issues, args.observe)

    if args.format == "json":
        rendered = render_json_report(data)
    else:
        rendered = render_text_report(data)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"Wrote {args.format} report to {output_path}")
    else:
        print(rendered, end="")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        run(args)
    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
