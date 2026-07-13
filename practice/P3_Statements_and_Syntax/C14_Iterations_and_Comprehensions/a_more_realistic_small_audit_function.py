#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/10


def audit_translations(source, target):
    stats = {
        "source_total": 0,
        "target_total": 0,
        "missing": 0,
        "empty": 0,
        "extra": 0,
    }

    issues = []

    stats["source_total"] = len(source)
    stats["target_total"] = len(target)

    for key in source:
        if key not in target:
            stats["missing"] += 1
            issues.append({
                "key": key,
                "type": "missing_key",
                "message": "key exists in source but not in target",
            })
            continue

        if target[key] == "":
            stats["empty"] += 1
            issues.append({
                "key": key,
                "type": "empty_translation",
                "message": "target translation is empty",
            })

    for key in target:
        if key not in source:
            stats["extra"] += 1
            issues.append({
                "key": key,
                "type": "extra_key",
                "message": "key exists in target but not in source",
            })

    return {
        "completed": True,
        "stats": stats,
        "issues": issues,
    }


source = {
    "ui.start": "Start",
    "ui.exit": "Exit",
    "ui.save": "Save",
    "ui.load": "Load",
}

target = {
    "ui.start": "开始",
    "ui.exit": "退出",
    "ui.save": "",
    "ui.debug": "调试",
}

report = audit_translations(source, target)

print(report)
