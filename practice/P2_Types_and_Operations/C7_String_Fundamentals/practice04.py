#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/12

text = "  Press {key}\\nStart\t "

print(repr(text))
print(repr(text.strip()))
print("{key}" in text)
print("\\n" in text)
print("\n" in text)
print(text.replace("{key}", "Enter"))
print(text.split())
print(text.strip().split("\\n"))
