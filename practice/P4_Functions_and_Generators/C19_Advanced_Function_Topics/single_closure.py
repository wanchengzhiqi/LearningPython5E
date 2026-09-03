#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/31


def make_prefixer(prefix):
    def add_prefix(text):
        return prefix + text

    return add_prefix


ui = make_prefixer("[UI] ")

print("result:", ui("Start"))

print("freevars:", ui.__code__.co_freevars)
print("closure:", ui.__closure__)

for name, cell in zip(
    ui.__code__.co_freevars,
    ui.__closure__,
):
    print(
        "binding:",
        name,
        "->",
        repr(cell.cell_contents),
    )

print(
    "outer cellvars:",
    make_prefixer.__code__.co_cellvars,
)
