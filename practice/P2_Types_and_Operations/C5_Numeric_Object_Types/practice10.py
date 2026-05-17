#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/7

from fractions import Fraction
from decimal import Decimal

print(Fraction(1, 10) + Fraction(2, 10))
print(Fraction("0.1") + Fraction("0.2"))

print(Fraction(0.1))
print(Fraction(0.1).limit_denominator())

print(Decimal("0.3333"))
print(Fraction(1, 3))

x = Fraction(1, 3)
print(x + 1)
print(x + 0.5)

rate = Fraction(1, 20) + Fraction(3, 100)
print(rate)
print(f"{float(rate):.2%}")
