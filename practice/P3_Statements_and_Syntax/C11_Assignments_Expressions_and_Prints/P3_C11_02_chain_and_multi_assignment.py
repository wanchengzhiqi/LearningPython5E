#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/15
# C11-02: chain assignment and shared mutable objects

print("=== Experiment 1: chain assignment with immutable object ===")

a = b = 100
a = 200

print("a =", a)
print("b =", b)
print("a is b:", a is b)


print("\n=== Experiment 2: chain assignment with mutable object ===")

x = y = []

x.append("menu.start")

print("x =", x)
print("y =", y)
print("x is y:", x is y)


print("\n=== Experiment 3: separate list objects ===")

p = []
q = []

p.append("settings.audio")

print("p =", p)
print("q =", q)
print("p is q:", p is q)


print("\n=== Experiment 4: multiple assignment ===")

left = "L"
right = "R"

left, right = right, left

print("left =", left)
print("right =", right)


print("\n=== Experiment 5: localization bug simulation ===")

missing_en = missing_ja = missing_zh = []

missing_en.append("menu.start")
missing_ja.append("settings.audio")

print("EN:", missing_en)
print("JA:", missing_ja)
print("ZH:", missing_zh)


print("\n=== Experiment 6: correct localization structure ===")

missing = {
    "en": [],
    "ja": [],
    "zh": [],
}

missing["en"].append("menu.start")
missing["ja"].append("settings.audio")

print("missing =", missing)


print("\n=== Experiment 7: nested list trap ===")

grid = [[0] * 3] * 3
grid[0][0] = 1

print("grid =", grid)


print("\n=== Experiment 8: correct nested list ===")

safe_grid = [[0] * 3 for _ in range(3)]
safe_grid[0][0] = 1

print("safe_grid =", safe_grid)
