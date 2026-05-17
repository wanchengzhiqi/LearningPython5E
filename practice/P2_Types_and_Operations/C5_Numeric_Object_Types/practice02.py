#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/5

pairs = [
    (9, 2),
    (-9, 2),
    (9, -2),
    (-9, -2),
    ]

for a, b in pairs:
    print(f"{a} / {b} = {a / b}")
    print(f"{a} // {b} = {a // b}")
    print(f"{a} % {b} = {a % b}")
    print(f"divmod({a}, {b}) = {divmod(a, b)}")
    print(f"check: {a} == ({a} // {b}) * {b} + ({a} % {b}) -> {a == (a // b) * b + (a % b)}")
    print()
