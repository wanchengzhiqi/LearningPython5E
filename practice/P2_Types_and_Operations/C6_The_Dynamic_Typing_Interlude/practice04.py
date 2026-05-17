#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/3


def f(a, b):
    a.append(3)
    b = b + [4]
    return a, b


x = [1, 2]
y = [1, 2]

r1, r2 = f(x, y)

print(x)  # [1, 2, 3]
print(y)  # [1, 2]
print(r1)  # [1, 2, 3]
print(r2)  # [1, 2, 4]
print(x is r1)  # True
print(y is r2)  # False


def g(data):
    data['items'].append('new')
    data = {'items': []}
    return data


box = {'items': ['old']}
result = g(box)

print(box)  # {'items': ['old', 'new']}
print(result)  # {'items': []}
print(box is result)  # False
print(box['items'] is result['items'])  # False
