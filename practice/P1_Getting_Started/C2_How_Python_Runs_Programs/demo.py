#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/2

import dis


def add(a, b):
    return a + b


def square_list(nums):
    return [i * i for i in nums]


x = add(2, 3)
print(f"The result of adding 2 and 3 is: {x}")

dis.dis(add)
dis.dis(square_list)

print(add.__code__)
print(add.__code__.co_code)
