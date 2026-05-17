#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/4


def make_box():
    items = []

    def add(x):
        items.append(x)
        return items

    return add


box1 = make_box()
box2 = make_box()

print(box1('a'))  # ['a']
print(box1('b'))  # ['a', 'b']
print(box2('x'))  # ['x']
print(box1('c'))  # ['a', 'b', 'c']
print(box2('y'))  # ['x', 'y']


def make_reader():
    value = 10

    def read():
        return value

    value = 20
    return read


reader = make_reader()
print(reader())  # 20
