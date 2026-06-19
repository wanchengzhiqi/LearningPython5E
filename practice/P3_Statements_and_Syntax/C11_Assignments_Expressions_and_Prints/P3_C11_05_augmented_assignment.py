#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/16
# C11-05: augmented assignment

print("=== Experiment 1: int += creates new object ===")

x = 10
old_id = id(x)

x += 5

print("x =", x)
print("same object:", old_id == id(x))


print("\n=== Experiment 2: str += creates new object ===")

s = "Py"
alias = s

s += "thon"

print("s =", s)
print("alias =", alias)
print("s is alias:", s is alias)


print("\n=== Experiment 3: list += mutates in place ===")

items = ["en", "ja"]
alias = items

items += ["zh"]

print("items =", items)
print("alias =", alias)
print("items is alias:", items is alias)


print("\n=== Experiment 4: list = list + other creates new list ===")

items = ["en", "ja"]
alias = items

items = items + ["zh"]

print("items =", items)
print("alias =", alias)
print("items is alias:", items is alias)


print("\n=== Experiment 5: append vs extend vs += ===")

items = ["en", "ja"]
items.append(["zh", "ko"])
print("after append:", items)

items = ["en", "ja"]
items.extend(["zh", "ko"])
print("after extend:", items)

items = ["en", "ja"]
items += ["zh", "ko"]
print("after +=:", items)


print("\n=== Experiment 6: dict counter ===")

stats = {
    "missing": 0,
    "duplicated": 0,
    "invalid": 0,
}

stats["missing"] += 1
stats["missing"] += 1
stats["invalid"] += 1

print("stats =", stats)


print("\n=== Experiment 7: set |= mutates in place ===")

tags = {"ui"}
alias = tags

tags |= {"menu", "main"}

print("tags =", tags)
print("alias =", alias)
print("tags is alias:", tags is alias)


print("\n=== Experiment 8: dict |= updates in place ===")

base = {"menu.start": "Start"}
patch = {"menu.exit": "Exit"}

alias = base

base |= patch

print("base =", base)
print("alias =", alias)
print("base is alias:", base is alias)


print("\n=== Experiment 9: nested list with += ===")

rows = [[1], [2], [3]]
alias = rows[0]

rows[0] += [99]

print("rows =", rows)
print("alias =", alias)
print("rows[0] is alias:", rows[0] is alias)


print("\n=== Experiment 10: nested list with = old + new ===")

rows = [[1], [2], [3]]
alias = rows[0]

rows[0] = rows[0] + [99]

print("rows =", rows)
print("alias =", alias)
print("rows[0] is alias:", rows[0] is alias)


print("\n=== Experiment 11: tuple containing mutable list trap ===")

t = ([1, 2],)

try:
    t[0] += [3]
except TypeError as e:
    print("Error:", e)

print("t =", t)
