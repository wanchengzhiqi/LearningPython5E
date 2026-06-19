#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/16
# C11-06: expression statements, REPL echo, and print()

print("=== Experiment 1: expression statements in script ===")

1 + 2
"hello"
len("abc")

print("If you see this line only, the naked expressions above did not auto-display.")


print("\n=== Experiment 2: explicit output ===")

print(1 + 2)
print("hello")
print(len("abc"))


print("\n=== Experiment 3: side effect expression statement ===")

items = ["en", "ja"]

items.append("zh")

print("items =", items)


print("\n=== Experiment 4: append return value ===")

items = ["en", "ja"]

returned = items.append("zh")

print("items =", items)
print("returned =", returned)


print("\n=== Experiment 5: print return value ===")

result = print("This line is produced by print().")

print("result =", result)


print("\n=== Experiment 6: repr-style inspection ===")

text = "Start\nExit"

print("str style:")
print(text)

print("repr style:")
print(repr(text))


print("\n=== Experiment 7: sep and end ===")

print("menu.start", "en", "Start")
print("menu.start", "en", "Start", sep=",")
print("Loading", end="...")
print("done")


print("\n=== Experiment 8: print to file ===")

with open("c11_06_report.txt", "w", encoding="utf-8") as f:
    print("Missing keys:", file=f)
    print("menu.start", file=f)
    print("settings.audio", file=f)

print("Report file written: c11_06_report.txt")
