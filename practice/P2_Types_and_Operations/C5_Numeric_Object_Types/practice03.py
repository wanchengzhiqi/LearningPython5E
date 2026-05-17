#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/5

import math

from decimal import Decimal

x = 0.1 + 0.2

print("原始显示:", x)
print("两位小数:", f"{x:.2f}")
print("仍然是原值:", repr(x))
print("直接比较:", x == 0.3)
print("近似比较:", math.isclose(x, 0.3))

n = 255

print("二进制:", f"{n:08b}")
print("八进制:", f"{n:o}")
print("十进制:", f"{n:d}")
print("十六进制:", f"{n:02X}")

money = Decimal("19.99") + Decimal("0.01")
print("Decimal 金额:", money)
