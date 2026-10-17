#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/10/16

from practice.P4_Functions_and_Generators.C20_Comprehensions_Revisited_and_Generators.input_integrity import (
    ROWS,
    EXPECTED,
    audit_with_manifest,
    try_publish_verified,
    make_catalog
)


def altered_source():
    for row in ROWS:
        item = dict(row)

        if item["row_id"] == 0:
            item["text"] = " 不对应的翻译 "

        yield item


catalog = make_catalog()
report = audit_with_manifest(
    altered_source,
    EXPECTED,
)
decision = try_publish_verified(report, catalog)

print(report["status"])
print(report["coverage"]["verified"])
print(report["issues"])
print(report["mapping"]["menu.start"])
print(decision)

report = audit_with_manifest(
    lambda: iter(reversed(ROWS)),
    EXPECTED,
)

print(report["coverage"]["observed_ids"])
print(report["coverage"]["verified"])

incomplete_rows = ROWS[:1]
incomplete_expected = (0,)
report = audit_with_manifest(
    lambda: iter(incomplete_rows),
    incomplete_expected,
)

print(report["status"])
print(report["coverage"]["verified"])
print(report["mapping"])

rows = [
    {
        "row_id": 0,
        "key": "menu.start",
        "text": "开始",
    }
]


def fresh_source():
    yield from rows


g1 = fresh_source()
g2 = fresh_source()
rows[0]["text"] = "修改后的内容"

print(g1 is g2)
print(next(g1)["text"])
print(next(g2)["text"])
