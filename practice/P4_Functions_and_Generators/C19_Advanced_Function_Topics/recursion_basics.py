#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/2

import sys


def factorial(n):
    print(
        "ENTER",
        "n =", n,
        "id(n) =", id(n),
    )

    if n == 0:
        print("BASE", n)
        return 1

    sub_result = factorial(n - 1)

    result = n * sub_result

    print(
        "LEAVE",
        "n =", n,
        "sub_result =", sub_result,
        "result =", result,
    )

    return result


print(
    "recursion limit:",
    sys.getrecursionlimit(),
)

answer = factorial(4)

print("answer:", answer)
