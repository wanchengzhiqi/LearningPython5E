#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/7

import math
import random
import statistics as stats

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

print(abs(3 + 4j))

print(pow(2, 10, 1000))

scores = [80, 55, 90, 40]
print(sum(score >= 60 for score in scores))

names = ["Tom", "Elizabeth", "Ada"]
print(max(names, key=len))

x = 0.1 + 0.2
print(x == 0.3)
print(math.isclose(x, 0.3))

nan = math.nan
print(nan == nan)
print(math.isnan(nan))

money = Decimal("19.995")
print(money.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

print(Fraction("0.1") + Fraction("0.2"))

items = [1, 2, 3]
random.shuffle(items)
print(items)

print(stats.mean([10, 20, 30, 40]))
