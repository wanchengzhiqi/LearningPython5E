#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/3

a = [1, 2]
b = a
c = [1, 2]

print(a == b)  # True
print(a is b)  # True
print(a == c)  # True
print(a is c)  # False

b.append(3)

print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]
print(c)  # [1, 2]

b = c
b.append(4)

print(a)  # [1, 2, 3]
print(b)  # [1, 2, 4]
print(c)  # [1, 2, 4]
