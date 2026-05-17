#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/4

a = [1, 2]
b = a
c = [1, 2]

print(a is b)  # True
print(a == b)  # True
print(a is c)  # False
print(a == c)  # True

b.append(3)

print(a)  # [1, 2, 3]
print(c)  # [1, 2]
print(a == c)  # False

x = None
y = []

print(x is None)  # True
print(y is None)  # False
print(y == None)  # False
print(y == [])  # True
print(y is [])  # False
