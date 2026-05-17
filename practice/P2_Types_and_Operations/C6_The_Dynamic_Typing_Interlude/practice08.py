#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/4


def show_count(x):
    print(len(x))


show_count('abc')  # 3
show_count([1, 2, 3])  # 3
show_count({'a': 1, 'b': 2})  # 2


def first_item(items):
    return items[0]


print(first_item([10, 20]))  # 10
print(first_item('python'))  # 'p'
