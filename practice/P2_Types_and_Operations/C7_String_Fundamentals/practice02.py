#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/12

samples = [
    "A\nB",
    "A\\nB",
    "",
    " ",
    "hello\tworld",
    "中文\nEnglish",
]

for s in samples:
    print("对象正常输出:")
    print(s)

    print("repr显示:")
    print(repr(s))

    print("放进列表:")
    print([s])

    print("str长度:", len(str(s)))
    print("repr长度:", len(repr(s)))
    print("-" * 30)
