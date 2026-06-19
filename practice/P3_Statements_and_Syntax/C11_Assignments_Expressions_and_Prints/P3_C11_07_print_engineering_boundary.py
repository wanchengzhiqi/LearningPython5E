#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/16
# C11-07: print engineering boundary

import sys
import logging


print("=== Experiment 1: print return value ===")

result = print("Hello from print().")
print("result =", result)


print("\n=== Experiment 2: sep ===")

print("menu.start", "en", "Start")
print("menu.start", "en", "Start", sep=",")
print("menu.start", "en", "Start", sep=" | ")


print("\n=== Experiment 3: end ===")

print("A")
print("B")

print("A", end="")
print("B")

print("Checking files", end="... ")
print("done")


print("\n=== Experiment 4: stdout and stderr ===")

print("This is a normal message on stdout.")
print("This is a warning message on stderr.", file=sys.stderr)


print("\n=== Experiment 5: str-style and repr-style inspection ===")

text = "Start\nExit"

print("str style:")
print(text)

print("repr style:")
print(repr(text))


print("\n=== Experiment 6: print to file ===")

with open("c11_07_report.txt", "w", encoding="utf-8") as f:
    print("Localization audit report", file=f)
    print("=========================", file=f)
    print("Missing keys:", file=f)
    print("menu.start", file=f)
    print("settings.audio", file=f)

print("Wrote c11_07_report.txt")


print("\n=== Experiment 7: print(file=f) vs file.write() ===")

with open("c11_07_write_demo.txt", "w", encoding="utf-8") as f:
    print("A", file=f)
    print("B", file=f)
    f.write("C")
    f.write("D")
    f.write("\n")

print("Wrote c11_07_write_demo.txt")


print("\n=== Experiment 8: minimal logging preview ===")

logging.basicConfig(
    filename="c11_07_app.log",
    level=logging.INFO,
    encoding="utf-8",
)

logging.info("Localization audit started.")
logging.info("Loaded sample localization data.")
logging.warning("Missing key detected: menu.start")

print("Wrote c11_07_app.log")
