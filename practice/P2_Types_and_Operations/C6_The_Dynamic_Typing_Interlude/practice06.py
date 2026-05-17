#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/4

a = [1, 2]
b = a

del a

b.append(3)
print(b)  # [1, 2, 3]


def make_list():
    x = [1, 2, 3]
    return x


y = make_list()
print(y)  # [1, 2, 3]


def outer():
    data = []

    def inner(x):
        data.append(x)
        return data

    return inner


f = outer()

print(f.__closure__)  # (<cell at 0x7f8c9c1e5d30: list object at 0x7f8c9c1e5d60>,)
print(f.__closure__[0].cell_contents)  # []

print(f(1))  # [1]
print(f.__closure__[0].cell_contents)  # [1]

print(f(2))  # [1, 2]
print(f.__closure__[0].cell_contents)  # [1, 2]
