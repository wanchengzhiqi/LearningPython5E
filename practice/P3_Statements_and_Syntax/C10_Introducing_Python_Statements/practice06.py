#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/6

resources = [
    {"id": "title", "text": "Adventure"},
    {"id": "subtitle", "text": ""},
]

print("start")

empty_ids = []

for item in resources:
    if item["text"] == "":
        result = empty_ids.append(item["id"])
        print("append returned:", result)

print("empty ids:", empty_ids)

empty_ids
print("end")
