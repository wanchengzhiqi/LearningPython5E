#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/7

MODE = "idle"
SHARED = []


def make_worker(label):
    count = 0
    records = []

    def work(value):
        nonlocal count
        global MODE

        count += 1
        MODE = label

        records.append(value)
        SHARED.append((label, value))

        local_records = records + ["local"]

        return {
            "count": count,
            "records": list(records),
            "local_records": local_records,
        }

    def inspect():
        return count, list(records)

    return work, inspect


work_a, inspect_a = make_worker("A")
work_b, inspect_b = make_worker("B")

assert work_a(1) == {
    "count": 1,
    "records": [1],
    "local_records": [1, "local"],
}

assert work_a(2) == {
    "count": 2,
    "records": [1, 2],
    "local_records": [1, 2, "local"],
}

assert work_b(3) == {
    "count": 1,
    "records": [3],
    "local_records": [3, "local"],
}

assert inspect_a() == (2, [1, 2])
assert inspect_b() == (1, [3])

assert MODE == "B"
assert SHARED == [
    ("A", 1),
    ("A", 2),
    ("B", 3),
]

print("checks passed")
