#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/10

from collections import Counter
from string import Formatter


_FORMATTER = Formatter()

_SEVERITY_RANK = {
    "fatal": 0,
    "error": 1,
    "warning": 2,
    "info": 3,
}


def parse_target_lines(lines):
    parsed_entries = []
    issues = []

    for line_no, raw_line in enumerate(lines, start=1):
        if "=" not in raw_line:
            issues.append({
                "severity": "error",
                "line": line_no,
                "type": "malformed_line",
                "message": "line does not contain '='",
                "raw": raw_line,
            })
            continue

        key, text = raw_line.split("=", 1)

        parsed_entries.append({
            "line": line_no,
            "key": key,
            "text": text,
            "raw": raw_line,
        })

    return parsed_entries, issues


def build_accepted_target(parsed_entries):
    target = {}
    accepted_entries = []
    duplicate_entries = []

    for entry in parsed_entries:
        key = entry["key"]

        if key in target:
            duplicate_entries.append(entry)
            continue

        target[key] = entry["text"]
        accepted_entries.append(entry)

    return target, accepted_entries, duplicate_entries


def extract_placeholder_signatures(text):
    signatures = []

    try:
        for _, field_name, format_spec, conversion in _FORMATTER.parse(text):
            if field_name is None:
                continue

            signatures.append((
                field_name,
                conversion or "",
                format_spec or "",
            ))

    except ValueError as exc:
        return [], str(exc)

    return signatures, None


def format_placeholder_signature(signature):
    field_name, conversion, format_spec = signature

    result = "{" + field_name

    if conversion:
        result += f"!{conversion}"

    if format_spec:
        result += f":{format_spec}"

    return result + "}"


def compare_placeholders(source_text, target_text):
    source_signatures, source_error = extract_placeholder_signatures(
        source_text
    )
    target_signatures, target_error = extract_placeholder_signatures(
        target_text
    )

    result = {
        "source_parse_error": source_error,
        "target_parse_error": target_error,
        "source_placeholders": sorted(
            format_placeholder_signature(signature)
            for signature in source_signatures
        ),
        "target_placeholders": sorted(
            format_placeholder_signature(signature)
            for signature in target_signatures
        ),
        "missing_placeholders": [],
        "extra_placeholders": [],
        "matches": False,
    }

    if source_error is not None or target_error is not None:
        return result

    source_counts = Counter(source_signatures)
    target_counts = Counter(target_signatures)

    result["missing_placeholders"] = sorted(
        format_placeholder_signature(signature)
        for signature in (
            source_counts - target_counts
        ).elements()
    )

    result["extra_placeholders"] = sorted(
        format_placeholder_signature(signature)
        for signature in (
            target_counts - source_counts
        ).elements()
    )

    result["matches"] = (
        not result["missing_placeholders"]
        and not result["extra_placeholders"]
    )

    return result


def audit_placeholder_contracts(source, target):
    issues = []

    checked_count = 0
    skipped_count = 0
    mismatch_count = 0

    for key, source_text in source.items():
        if key not in target:
            skipped_count += 1
            continue

        target_text = target[key]

        if target_text == "":
            skipped_count += 1
            continue

        comparison = compare_placeholders(
            source_text,
            target_text,
        )

        if comparison["source_parse_error"] is not None:
            skipped_count += 1

            issues.append({
                "severity": "error",
                "key": key,
                "type": "source_placeholder_syntax_error",
                "message": comparison["source_parse_error"],
            })
            continue

        if comparison["target_parse_error"] is not None:
            skipped_count += 1

            issues.append({
                "severity": "error",
                "key": key,
                "type": "target_placeholder_syntax_error",
                "message": comparison["target_parse_error"],
            })
            continue

        checked_count += 1

        if comparison["matches"]:
            continue

        mismatch_count += 1

        issues.append({
            "severity": "error",
            "key": key,
            "type": "placeholder_mismatch",
            "message": (
                "source and target placeholder signatures differ"
            ),
            "source_placeholders": (
                comparison["source_placeholders"]
            ),
            "target_placeholders": (
                comparison["target_placeholders"]
            ),
            "missing_placeholders": (
                comparison["missing_placeholders"]
            ),
            "extra_placeholders": (
                comparison["extra_placeholders"]
            ),
        })

    return {
        "checked_count": checked_count,
        "skipped_count": skipped_count,
        "mismatch_count": mismatch_count,
        "issues": issues,
    }


def build_normalization_plan(accepted_entries):
    return [
        {
            "line": entry["line"],
            "key": entry["key"],
            "action": "strip_outer_whitespace",
            "before": entry["text"],
            "after": entry["text"].strip(),
        }
        for entry in accepted_entries
        if entry["text"] != entry["text"].strip()
    ]


def issue_sort_key(issue):
    line = issue.get("line")

    return (
        _SEVERITY_RANK.get(
            issue.get("severity", "info"),
            99,
        ),
        issue.get("type", ""),
        line is None,
        line or 0,
        issue.get("key", ""),
        issue.get("message", ""),
    )


def audit_localization(source, target_lines):
    parsed_entries, parse_issues = parse_target_lines(
        target_lines
    )

    target, accepted_entries, duplicate_entries = (
        build_accepted_target(parsed_entries)
    )

    missing_keys = sorted(
        key
        for key in source
        if key not in target
    )

    source_matched_empty_keys = sorted(
        key
        for key in source
        if key in target and target[key] == ""
    )

    extra_keys = sorted(
        key
        for key in target
        if key not in source
    )

    extra_empty_keys = sorted(
        key
        for key in extra_keys
        if target[key] == ""
    )

    placeholder_audit = audit_placeholder_contracts(
        source,
        target,
    )

    normalization_plan = build_normalization_plan(
        accepted_entries
    )

    issues = list(parse_issues)

    for entry in duplicate_entries:
        issues.append({
            "severity": "error",
            "line": entry["line"],
            "key": entry["key"],
            "type": "duplicate_key",
            "message": (
                "duplicate entry was ignored; "
                "first occurrence was retained"
            ),
            "raw": entry["raw"],
        })

    for key in missing_keys:
        issues.append({
            "severity": "error",
            "key": key,
            "type": "missing_key",
            "message": (
                "key exists in source "
                "but not in accepted target"
            ),
        })

    for key in source_matched_empty_keys:
        issues.append({
            "severity": "error",
            "key": key,
            "type": "source_matched_empty_translation",
            "message": (
                "source key exists in accepted target, "
                "but its translation is empty"
            ),
        })

    for key in extra_keys:
        issues.append({
            "severity": "warning",
            "key": key,
            "type": "extra_key",
            "message": (
                "key exists in accepted target "
                "but not in source"
            ),
        })

    issues.extend(placeholder_audit["issues"])

    issues = sorted(
        issues,
        key=issue_sort_key,
    )

    quality_passed = not any(
        issue["severity"] in {"fatal", "error"}
        for issue in issues
    )

    stats = {
        "source_key_total": len(source),
        "raw_line_total": len(target_lines),
        "parsed_pair_total": len(parsed_entries),
        "accepted_target_total": len(target),

        "malformed_line_count": len(parse_issues),
        "duplicate_entry_count": len(duplicate_entries),
        "missing_key_count": len(missing_keys),

        "source_matched_empty_key_count": len(
            source_matched_empty_keys
        ),

        "extra_key_count": len(extra_keys),
        "extra_empty_key_count": len(extra_empty_keys),

        "placeholder_checked_key_count": (
            placeholder_audit["checked_count"]
        ),

        "placeholder_skipped_key_count": (
            placeholder_audit["skipped_count"]
        ),

        "placeholder_mismatch_key_count": (
            placeholder_audit["mismatch_count"]
        ),

        "planned_normalization_count": len(
            normalization_plan
        ),
    }

    return {
        "completed": True,
        "quality_passed": quality_passed,
        "stats": stats,
        "missing_keys": missing_keys,
        "source_matched_empty_keys": (
            source_matched_empty_keys
        ),
        "extra_keys": extra_keys,
        "extra_empty_keys": extra_empty_keys,
        "normalization_plan": normalization_plan,
        "issues": issues,
    }


def render_dry_run_summary(report):
    print("[DRY-RUN] No source files were modified.")

    print(
        "Result:",
        "PASS" if report["quality_passed"] else "FAIL",
    )

    print("Issues:", len(report["issues"]))

    print(
        "Planned normalizations:",
        report["stats"]["planned_normalization_count"],
    )

    for action in report["normalization_plan"]:
        print(
            f'  line {action["line"]}: '
            f'{action["key"]} -> '
            f'{action["action"]}: '
            f'{action["before"]!r} '
            f'=> {action["after"]!r}'
        )


source = {
    "ui.start": "Start",
    "ui.exit": "Exit",
    "ui.save": "Save",
    "ui.load": "Load",
    "ui.welcome": "Welcome {player}",
    "ui.score": "{player} scored {score:d}",
}

target_lines = [
    "ui.start=开始",
    "ui.exit= 退出 ",
    "bad line without separator",
    "ui.save=",
    "ui.start=启动",
    "ui.debug=调试",
    "ui.welcome=欢迎 {name}",
    "ui.score={player} 得分 {score}",
]

report = audit_localization(
    source,
    target_lines,
)

render_dry_run_summary(report)

print(report["stats"])

for issue in report["issues"]:
    print(issue)
