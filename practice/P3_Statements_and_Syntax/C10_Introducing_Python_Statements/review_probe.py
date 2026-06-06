#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/6

resources = [
    {"id": "menu_start", "text": "Start"},
    {"id": "menu_exit", "text": "Exit"},
    {"id": "dialog_001", "text": ""},
]

print("resource count:", len(resources))

missing_ids = []

for resource in resources:
    text = resource["text"]

    if text == "":
        missing_ids.append(resource["id"])
        print("missing:", repr(resource["id"]))

print("missing ids:", missing_ids)

append_result = missing_ids.append("summary_marker")

print("append result:", append_result)
print("missing ids:", missing_ids)

"script finished"
print("done")
