#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/19

records = [
    ("MENU_START", "Start Game", "开始游戏", ("ui",)),
    ("MENU_EXIT", "Exit", "", ("ui", "todo")),
    ("DIALOG_001", "Hello\nthere", "你好\n啊", ("dialog",)),
    ("ITEM_POTION", "Potion {count}", "药水", ("item",)),
    ("MENU_START", "Start", "开始", ("ui", "duplicate")),
]

keys = [record[0] for record in records]

missing_translations = [
    record
    for record in records
    if record[2] == ""
]

texts_with_newline = [
    record
    for record in records
    if "\n" in record[1] or "\n" in record[2]
]

long_sources = [
    record
    for record in records
    if len(record[1]) > 10
]

print("keys:", keys)
print("missing:", missing_translations)
print("newline:", texts_with_newline)
print("long sources:", long_sources)
print("records:", records)
