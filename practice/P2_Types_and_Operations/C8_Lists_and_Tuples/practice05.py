#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/19

bad = [[0] * 3] * 3

print(bad)
print([id(row) for row in bad])

bad[0][1] = 9

print(bad)
print([id(row) for row in bad])

good = [[0] * 3 for _ in range(3)]

print(good)
print([id(row) for row in good])

good[0][1] = 9

print(good)
