#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/8

GLOBAL_MODE = "idle"
AUDIT_LOG = []


def make_gate(name):
    run_count = 0
    records = []
    temporary = "not captured"

    def run(text):
        nonlocal run_count
        global GLOBAL_MODE

        run_count += 1
        GLOBAL_MODE = f"{name}:{run_count}"

        normalized = text.strip().upper()

        records.append(normalized)
        AUDIT_LOG.append(
            (name, run_count, normalized)
        )

        return {
            "mode": GLOBAL_MODE,
            "count": run_count,
            "records": tuple(records),
        }

    def snapshot():
        return run_count, tuple(records)

    return run, snapshot


run_a, snapshot_a = make_gate("A")
run_b, snapshot_b = make_gate("B")


assert run_a(" one ") == {
    "mode": "A:1",
    "count": 1,
    "records": ("ONE",),
}

assert run_a(" two ") == {
    "mode": "A:2",
    "count": 2,
    "records": ("ONE", "TWO"),
}

assert run_b(" three ") == {
    "mode": "B:1",
    "count": 1,
    "records": ("THREE",),
}

assert snapshot_a() == (
    2,
    ("ONE", "TWO"),
)

assert snapshot_b() == (
    1,
    ("THREE",),
)

assert GLOBAL_MODE == "B:1"

assert AUDIT_LOG == [
    ("A", 1, "ONE"),
    ("A", 2, "TWO"),
    ("B", 1, "THREE"),
]


def closure_cells(func):
    return dict(
        zip(
            func.__code__.co_freevars,
            func.__closure__ or (),
        )
    )


run_a_cells = closure_cells(run_a)
snapshot_a_cells = closure_cells(snapshot_a)

assert (
    run_a_cells["run_count"]
    is snapshot_a_cells["run_count"]
)

assert (
    run_a_cells["records"]
    is snapshot_a_cells["records"]
)

assert "temporary" not in (
    make_gate.__code__.co_cellvars
)

print("checks passed")
