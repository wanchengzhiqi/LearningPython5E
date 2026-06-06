#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/6

resources = [
    {"id": "menu_start", "text": "Start"},
    {"id": "dialog_001", "text": "Line 1\nLine 2"},
]

print("resource count:", len(resources))

first_text = resources[0]["text"]
second_text = resources[1]["text"]

first_text
repr(second_text)

print(first_text)
print(second_text)
print(repr(second_text))

result = resources.append({"id": "menu_exit", "text": "Exit"})

print("append result:", result)
print("resource count:", len(resources))
