#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/7

from decimal import Decimal, ROUND_HALF_UP

price = Decimal("19.99")
quantity = 3
tax_rate = Decimal("0.075")

subtotal = price * quantity
tax = (subtotal * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
total = subtotal + tax

print(subtotal)  # 59.97
print(tax)       # 4.50
print(total)     # 64.47
