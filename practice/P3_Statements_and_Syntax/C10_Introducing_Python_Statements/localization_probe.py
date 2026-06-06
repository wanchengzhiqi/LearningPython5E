#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/5

resources = [
    {"id": "menu_start", "text": "Start"},
    {"id": "menu_exit", "text": "Exit"},
]

print("loaded:", len(resources))

result = resources.append({"id": "dialog_001", "text": ""})

print("append returned:", result)
print("resources:", resources)

dry_run = True

if dry_run:
    print("Preview only, no files changed.")

print("done")
