#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/28


def normalize_spaces(text):
    print("normalize_spaces: CALLED")
    return " ".join(text.split())


def upper_text(text):
    print("upper_text: CALLED")
    return text.upper()


def apply_rule(text, rule):
    print("apply_rule: begin")
    print("rule is:", rule.__name__)
    result = rule(text)
    print("apply_rule: end")
    return result


rules = {
    "normalize": normalize_spaces,
    "upper": upper_text,
}


print("=== registration complete ===")

selected = rules["normalize"]

print("=== selected ===")

result = apply_rule("  Start   Game  ", selected)

print("=== final ===")
print(result)
