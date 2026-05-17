#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/3

a = [1, 2]
b = a
c = a.copy()

b.append(3)
c.append(4)

print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]
print(c)  # [1, 2, 4]
print(a is b)  # True
print(a is c)  # False
print(a == c)  # False

x = 'py'
y = x

y += 'thon'

print(x)  # 'py'
print(y)  # 'python'
print(x is y)  # False
