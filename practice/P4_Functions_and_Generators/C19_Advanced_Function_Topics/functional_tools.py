#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/1

from functools import reduce


def normalize(text):
    print("normalize:", repr(text))
    return text.strip().lower()


def non_empty(text):
    print("check:", repr(text))
    return bool(text)


texts = [
    "  START  ",
    "",
    "  OPTIONS  ",
]


print("=== comprehension ===")

comprehension_result = [
    normalize(text)
    for text in texts
    if non_empty(text)
]

print("result:", comprehension_result)


print("\n=== map/filter creation ===")

mapped = map(
    normalize,
    filter(non_empty, texts),
)

print("iterators created")


print("\n=== map/filter consumption ===")

mapped_result = list(mapped)

print("result:", mapped_result)


print("\n=== reduce ===")

numbers = [1, 2, 3, 4]

total = reduce(
    lambda accumulator, item: accumulator + item,
    numbers,
    initial=0,
)

print("total:", total)
