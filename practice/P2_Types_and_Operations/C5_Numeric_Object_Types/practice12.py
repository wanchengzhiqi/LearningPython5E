#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/7

values = [None, False, 0, 0.0, "", [], {}, set(), "hi", [1]]

for value in values:
    print(repr(value), bool(value))

print("hello" and 123)
print("" and 123)
print("hello" or 123)
print("" or 123)

print(any([False, 0, "", "ok"]))
print(all([True, 1, "x"]))
print(any([]))
print(all([]))

x = 1
print(x == True)
print(x is True)
print(bool(x))
