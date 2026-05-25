#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/25

import json

from collections import Counter, defaultdict

records = [
    {"locale": "en_US", "key": "A", "text": "one"},
    {"locale": "en_US", "key": "A", "text": "duplicate"},
    {"locale": "en_US", "key": "B", "text": "two"},
    {"locale": "zh_CN", "key": "A", "text": ""},
    {"locale": "zh_CN", "key": "C", "text": "三"},
]

issues = defaultdict(list)

source_keys = {r["key"] for r in records if r["locale"] == "en_US"}
target_keys = {r["key"] for r in records if r["locale"] == "zh_CN"}

for key in source_keys - target_keys:
    issues[key].append({"type": "missing_in_target", "locale": "zh_CN"})

for key in target_keys - source_keys:
    issues[key].append({"type": "extra_in_target", "locale": "zh_CN"})

counts = Counter(r["key"] for r in records if r["locale"] == "en_US")
for key, count in counts.items():
    if count > 1:
        issues[key].append({"type": "duplicate_source_key", "count": count})

for r in records:
    if r["locale"] == "zh_CN" and not r["text"]:
        issues[r["key"]].append({"type": "empty_text", "locale": "zh_CN"})

print(dict(issues))

report = {"issues": dict(issues)}
text = json.dumps(report, ensure_ascii=False, indent=2)

print(type(text))
print(text)
