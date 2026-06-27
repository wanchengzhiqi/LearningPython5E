#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/25


def is_failure(result, strict):
    status = result["status"]

    if status == "ok":
        return False

    if status in {"invalid", "missing"}:
        return True

    if strict and status in {"empty", "blank"}:
        return True

    return False


def write_report_line(line):
    print(f"WRITE: {line}")


def handle_result(result, *, strict, dry_run, verbose):
    failed = is_failure(result, strict)

    level = "ERROR" if failed else "INFO"
    key = result.get("key", "<NO KEY>")
    line = f"[{level}] {key}: {result['status']} - {result['reason']}"

    if verbose:
        print(line)

    if dry_run:
        return {
            "action": "skip_write",
            "line": line,
            "failed": failed,
        }

    write_report_line(line)

    return {
        "action": "written",
        "line": line,
        "failed": failed,
    }


result_empty = {
    "status": "empty",
    "reason": "zh_CN is empty",
    "key": "menu.load",
}

result_missing = {
    "status": "missing",
    "reason": "missing language: zh_CN",
    "key": "menu.start",
}

result_ok = {
    "status": "ok",
    "reason": "translation exists",
    "key": "menu.new_game",
}

print("case 1")
print(handle_result(result_empty, strict=False, dry_run=True, verbose=True))

print("case 2")
print(handle_result(result_empty, strict=True, dry_run=True, verbose=True))

print("case 3")
print(handle_result(result_missing, strict=False, dry_run=False, verbose=False))

print("case 4")
print(handle_result(result_ok, strict=True, dry_run=False, verbose=True))
