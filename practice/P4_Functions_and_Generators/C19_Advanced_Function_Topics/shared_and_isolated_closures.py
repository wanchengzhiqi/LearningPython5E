#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/31


def make_score(initial):
    score = initial

    def read():
        return score

    def add(delta):
        nonlocal score
        score += delta
        return score

    return read, add


read1, add1 = make_score(10)
read2, add2 = make_score(100)

print(
    "same invocation:",
    read1.__closure__[0]
    is add1.__closure__[0],
)

print(
    "different invocation:",
    read1.__closure__[0]
    is read2.__closure__[0],
)

print("read1:", read1())
print("read2:", read2())

add1(5)

print("read1 after add1:", read1())
print("read2 after add1:", read2())
