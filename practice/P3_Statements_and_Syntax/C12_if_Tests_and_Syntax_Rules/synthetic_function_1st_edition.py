#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/24


def audit_entry(entry, lang):
    if not isinstance(entry, dict):
        return {
            "status": "invalid",
            "reason": "entry is not a dict",
        }

    if not entry:
        return {
            "status": "invalid",
            "reason": "empty entry",
        }

    if "key" not in entry:
        return {
            "status": "invalid",
            "reason": "missing key",
        }

    key = entry["key"]

    if key is None:
        return {
            "status": "invalid",
            "reason": "key is None",
        }

    if not isinstance(key, str):
        return {
            "status": "invalid",
            "reason": "key is not a string",
        }

    if key == "":
        return {
            "status": "invalid",
            "reason": "empty key",
        }

    if key.strip() == "":
        return {
            "status": "invalid",
            "reason": "blank key",
        }

    if not 1 <= len(key) <= 40:
        return {
            "status": "invalid",
            "reason": "key length out of range",
            "key": key,
        }

    if lang not in entry:
        return {
            "status": "missing",
            "reason": f"missing language: {lang}",
            "key": key,
        }

    text = entry[lang]

    if text is None:
        return {
            "status": "invalid",
            "reason": f"{lang} is None",
            "key": key,
        }

    if not isinstance(text, str):
        return {
            "status": "invalid",
            "reason": f"{lang} is not a string",
            "key": key,
        }

    if text == "":
        return {
            "status": "empty",
            "reason": f"{lang} is empty",
            "key": key,
        }

    if text.strip() == "":
        return {
            "status": "blank",
            "reason": f"{lang} is blank",
            "key": key,
        }

    return {
        "status": "ok",
        "reason": "translation exists",
        "key": key,
    }


cases = [
    None,
    {},
    {"zh_CN": "开始游戏"},
    {"key": None, "zh_CN": "开始游戏"},
    {"key": 123, "zh_CN": "开始游戏"},
    {"key": "", "zh_CN": "开始游戏"},
    {"key": "   ", "zh_CN": "开始游戏"},
    {"key": "menu.start.with.a.very.very.very.long.name", "zh_CN": "开始游戏"},
    {"key": "menu.start"},
    {"key": "menu.exit", "zh_CN": None},
    {"key": "menu.option", "zh_CN": 0},
    {"key": "menu.load", "zh_CN": ""},
    {"key": "menu.save", "zh_CN": "   "},
    {"key": "menu.new_game", "zh_CN": "新游戏"},
]

for case in cases:
    result = audit_entry(case, "zh_CN")
    print(result["status"], "-", result["reason"])
