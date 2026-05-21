#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/18


def show(label, obj):
    print(f"\n{label}")
    print("value:", repr(obj))
    print("id:", id(obj))


items = ["START", "LOAD", "OPTIONS", "EXIT"]
show("1. original items", items)

part = items[1:3]
show("2. part = items[1:3]", part)
show("3. items after slicing", items)

items[1:3] = ["CONTINUE", "SETTINGS", "SAVE"]
show("4. after items[1:3] = [...]", items)

items[::2] = ["A", "B", "C"]
show("5. after items[::2] = ['A', 'B', 'C']", items)
