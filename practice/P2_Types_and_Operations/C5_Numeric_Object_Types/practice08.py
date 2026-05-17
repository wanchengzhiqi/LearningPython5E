#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/7

import cmath

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

z = 3 + 4j
print(z.real, z.imag, abs(z))
print(cmath.sqrt(-1))

money = Decimal("19.995")
print(money.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

print(Fraction("0.1") + Fraction("0.2"))
print(Fraction(1, 3) + Fraction(1, 6))

a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)
print(a & b)
print(a ^ b)

scores = [80, 55, 90, 40]
print(sum(score >= 60 for score in scores))
