#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/6

import math

print("== vs is")
a = 1000
b = int("1000")
print(a == b)
print(a is b)

print("small int cache")
x = 10
y = 10
print(x == y)
print(x is y)

print("chained comparison")
age = 20
print(18 <= age <= 60)
print(1 < 2 > 1)
print(1 == 1.0 == True)

print("float comparison")
v = 0.1 + 0.2
print(v)
print(v == 0.3)
print(math.isclose(v, 0.3))

print("bool counting")
scores = [80, 55, 90, 40]
passed_count = sum(score >= 60 for score in scores)
print(passed_count)
