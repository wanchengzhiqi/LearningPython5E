#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/26

L = list(map(lambda x: 2 ** x, range(7)))

X = 5

if 2 ** X in L:
    print("at index", L.index(2 ** X))
else:
    print(X, "not found")
