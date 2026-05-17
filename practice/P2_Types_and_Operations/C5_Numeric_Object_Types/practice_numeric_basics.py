#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/5

from decimal import Decimal
from fractions import Fraction

print(10 == 0b1010 == 0o12 == 0xA)  # True

print(0.1 + 0.2)  # 0.30000000000000004
print(Decimal("0.1") + Decimal("0.2"))  # 0.3
print(Fraction(1, 10) + Fraction(2, 10))  # 3/10

print(True + True)  # 2
print(isinstance(True, int))  # True

x = 10
print(id(x))  # id of the integer object 10
x = x + 1
print(id(x))  # id of the integer object 11, different from 10
