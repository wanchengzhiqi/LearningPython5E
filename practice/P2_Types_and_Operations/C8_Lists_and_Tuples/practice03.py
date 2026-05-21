#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/18

items = ["MENU_EXIT", "MENU_START"]

result1 = items.append("MENU_OPTIONS")
print("items:", items)
print("result1:", result1)

result2 = items.sort()
print("items:", items)
print("result2:", result2)

result3 = sorted(items)
print("items:", items)
print("result3:", result3)
