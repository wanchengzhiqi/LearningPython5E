#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/6

resources = [
    {"id": "menu_start", "text": "Start"},
    {"id": "menu_exit", "text": "Exit"},
    {"id": "dialog_001", "text": ""},
]

missing_text_count = 0

for resource in resources:
    if resource["text"] == "":
        missing_text_count = missing_text_count + 1
        print("missing text:", resource["id"])

print("missing count:", missing_text_count)
