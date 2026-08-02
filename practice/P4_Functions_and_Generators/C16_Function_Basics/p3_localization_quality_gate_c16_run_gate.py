#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/29
"""Validate a small game-localization resource set.

This module is the integrated practice for
P3_Statements_and_Syntax / C15_The_Documentation_Interlude.
"""

import json
import sys


CONFIG = {
    "allowed_prefixes": ("ui.",),
    "error_levels": ("ERROR", "WARNING"),
}


KEYS = [
    " UI.MENU.START ",
    "ui.menu.quit",
    "ui.menu.start",
    "ui.inventory.count",
    "ui.debug.hidden",
    "ui.profile.name",
]


SOURCE_TEXTS = [
    "Start Game",
    "Quit Game",
    "Start Game",
    "You have {count} items.",
    "Debug",
    "Welcome, {name}!",
]


TRANSLATIONS = [
    "开始游戏",
    "",
    "开始",
    "你有 {amount} 件物品。",
    "调试",
    "欢迎，{name}！",
]


ENABLED_FLAGS = [
    True,
    True,
    True,
    True,
    False,
    True,
]


def normalize_key(key):
    """Return a normalized localization key."""

    return key.strip().lower()


def extract_placeholders(text):
    """Return placeholder tokens in left-to-right order."""

    placeholders = []
    position = 0

    while position < len(text):
        open_index = text.find(
            "{",
            position,
        )

        if open_index == -1:
            break

        close_index = text.find(
            "}",
            open_index + 1,
        )

        if close_index == -1:
            placeholders.append(
                text[open_index:]
            )
            break

        placeholders.append(
            text[
                open_index:close_index + 1
            ]
        )

        position = close_index + 1

    return placeholders


def build_entries(
    keys,
    sources,
    translations,
    enabled_flags,
):
    """Build entry dictionaries from parallel input columns."""

    rows = zip(
        keys,
        sources,
        translations,
        enabled_flags,
        strict=True,
    )

    return [
        {
            "line": line_number,
            "key": key,
            "source": source,
            "translation": translation,
            "enabled": enabled,
        }
        for line_number, (
            key,
            source,
            translation,
            enabled,
        ) in enumerate(
            rows,
            start=1,
        )
    ]


def make_issue(
    level,
    code,
    entry,
    message,
):
    """Return one structured issue record."""

    return {
        "level": level,
        "code": code,
        "line": entry["line"],
        "key": normalize_key(
            entry["key"]
        ),
        "message": message,
    }


def validate_entries(
    entries,
    config,
):
    """Validate entries and return a structured report."""

    issues = []
    seen_keys = set()

    processed_count = 0
    skipped_count = 0

    for entry in entries:
        if not entry["enabled"]:
            skipped_count += 1
            continue

        processed_count += 1

        key = normalize_key(
            entry["key"]
        )

        source = entry[
            "source"
        ].strip()

        translation = entry[
            "translation"
        ].strip()

        if not key:
            issues.append(
                make_issue(
                    "ERROR",
                    "empty_key",
                    entry,
                    "The normalized key is empty.",
                )
            )

        elif not key.startswith(
            config["allowed_prefixes"]
        ):
            issues.append(
                make_issue(
                    "ERROR",
                    "invalid_prefix",
                    entry,
                    (
                        "Key must start with "
                        f"{config['allowed_prefixes']!r}."
                    ),
                )
            )

        if key in seen_keys:
            issues.append(
                make_issue(
                    "ERROR",
                    "duplicate_key",
                    entry,
                    (
                        "The normalized key "
                        "has already appeared."
                    ),
                )
            )
        else:
            seen_keys.add(key)

        if not source:
            issues.append(
                make_issue(
                    "ERROR",
                    "missing_source",
                    entry,
                    "Source text is empty.",
                )
            )

        if not translation:
            issues.append(
                make_issue(
                    "ERROR",
                    "missing_translation",
                    entry,
                    "Translation text is empty.",
                )
            )

            continue

        source_placeholders = sorted(
            extract_placeholders(source)
        )

        translation_placeholders = sorted(
            extract_placeholders(
                translation
            )
        )

        if (
            source_placeholders
            != translation_placeholders
        ):
            issues.append(
                make_issue(
                    "ERROR",
                    "placeholder_mismatch",
                    entry,
                    (
                        "Source placeholders "
                        f"{source_placeholders!r} "
                        "do not match translation "
                        "placeholders "
                        f"{translation_placeholders!r}."
                    ),
                )
            )

        if source == translation:
            issues.append(
                make_issue(
                    "WARNING",
                    "unchanged_translation",
                    entry,
                    (
                        "Translation is identical "
                        "to source text."
                    ),
                )
            )

    counts = {
        level: sum(
            1
            for issue in issues
            if issue["level"] == level
        )
        for level in config[
            "error_levels"
        ]
    }

    sorted_issues = sorted(
        issues,
        key=lambda issue: (
            issue["line"],
            issue["level"],
            issue["code"],
        ),
    )

    return {
        "summary": {
            "input_count": len(entries),
            "processed_count": (
                processed_count
            ),
            "skipped_count": skipped_count,
            "error_count": counts[
                "ERROR"
            ],
            "warning_count": counts[
                "WARNING"
            ],
            "passed": (
                counts["ERROR"] == 0
            ),
        },
        "issues": sorted_issues,
    }


def print_report(report):
    """Print a human-readable report."""

    summary = report["summary"]

    print("=== Localization Quality Gate ===")
    print(
        "Python:",
        sys.version,
    )
    print(
        "Executable:",
        sys.executable,
    )

    print()
    print("Input:", summary["input_count"])
    print(
        "Processed:",
        summary["processed_count"],
    )
    print(
        "Skipped:",
        summary["skipped_count"],
    )
    print(
        "Errors:",
        summary["error_count"],
    )
    print(
        "Warnings:",
        summary["warning_count"],
    )
    print(
        "Passed:",
        summary["passed"],
    )

    print()
    print("=== Issues ===")

    if not report["issues"]:
        print("No issues found.")
        return

    for issue in report["issues"]:
        print(
            f'{issue["level"]} '
            f'line={issue["line"]} '
            f'key={issue["key"]!r} '
            f'code={issue["code"]}'
        )

        print(
            " ",
            issue["message"],
        )


def save_report(
    report,
    filename,
):
    """Save the structured report as UTF-8 JSON."""

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as report_file:
        json.dump(
            report,
            report_file,
            ensure_ascii=False,
            indent=2,
        )


def run_gate(
    keys,
    sources,
    translations,
    enabled_flags,
    config,
):
    """Build and validate entries, then return a structured report."""

    entries = build_entries(
        keys,
        sources,
        translations,
        enabled_flags,
    )

    return validate_entries(
        entries,
        config,
    )


def main():
    """Run the localization quality-gate command workflow."""

    report = run_gate(
        KEYS,
        SOURCE_TEXTS,
        TRANSLATIONS,
        ENABLED_FLAGS,
        CONFIG,
    )

    print_report(report)

    save_report(
        report,
        "p3_localization_report.json",
    )


if __name__ == "__main__":
    main()
