#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/15
# C11-01: assignment model

print("=== Experiment 1: right side first ===")

x = 1
y = 2
x, y = y, x

print("x =", x)
print("y =", y)


print("\n=== Experiment 2: rebinding ===")

a = [1, 2, 3]
b = a

a = [4, 5, 6]

print("a =", a)
print("b =", b)


print("\n=== Experiment 3: in-place mutation ===")

items = ["en", "ja"]
same_items = items

returned = items.append("zh")

print("items =", items)
print("same_items =", same_items)
print("returned =", returned)


print("\n=== Experiment 4: print return value ===")

result = print("This line is produced by print().")
print("result =", result)
