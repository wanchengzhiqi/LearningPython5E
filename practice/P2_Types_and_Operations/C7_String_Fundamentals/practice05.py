#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/12

s = "A\nB"

print(f"{s}")
print(f"{s!r}")
print(f"[{s:>6}]")
print(f"[{s!r:>8}]")

template = "Press {key} to start"
key = "Enter"

print(template)
print(template.format(key=key))
print(f"{template}")
