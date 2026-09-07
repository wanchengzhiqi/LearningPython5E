#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/7

import sys


def countdown_recursive(n):
    print("recursive:", n)

    if n == 0:
        return

    countdown_recursive(n - 1)


def countdown_iterative(n):
    while True:
        print("iterative:", n)

        if n == 0:
            return

        n -= 1


def sum_tail_recursive(n, total=0):
    if n == 0:
        return total

    return sum_tail_recursive(
        n - 1,
        total + n,
    )


def sum_iterative(n):
    total = 0

    while n > 0:
        total += n
        n -= 1

    return total


print(
    "recursion limit:",
    sys.getrecursionlimit(),
)

print("\n=== recursive countdown ===")
countdown_recursive(3)

print("\n=== iterative countdown ===")
countdown_iterative(3)

print("\n=== tail recursion ===")
print(sum_tail_recursive(10))

print("\n=== iteration ===")
print(sum_iterative(10))
