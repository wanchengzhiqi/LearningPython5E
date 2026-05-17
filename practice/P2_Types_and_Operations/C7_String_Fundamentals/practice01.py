#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/11

samples = [
    "A\nB",
    "A\\nB",
    r"A\nB",
    "\x41",
    "\u4e2d",
]

for s in samples:
    print("repr:", repr(s))
    print("str :", str(s))
    print("len :", len(s))
    print("chars:", [repr(ch) for ch in s])
    print("-" * 20)
