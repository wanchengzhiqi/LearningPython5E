#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/3

import copy

a = [[1], [2]]
b = a.copy()

b.append([3])
b[0].append(99)

print(a)  # [[1, 99], [2]]
print(b)  # [[1, 99], [2], [3]]
print(a is b)  # False
print(a[0] is b[0])  # True
print(a[1] is b[1])  # True

a = {'name': 'project',
     'files': ['a.txt', 'b.txt'],
     }

b = copy.deepcopy(a)
b['files'].append('c.txt')

print(a)  # {'name': 'project', 'files': ['a.txt', 'b.txt']}
print(b)  # {'name': 'project', 'files': ['a.txt', 'b.txt', 'c.txt']}
print(a is b)  # False
print(a['files'] is b['files'])  # False
print(a['name'] is b['name'])  # True
