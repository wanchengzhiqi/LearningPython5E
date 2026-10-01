#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/28

tests = (
    [1, [2, [3, 4], 5], 6, [7, 8]],      # Mixed nesting => 36
    [1, [2, [3, [4, [5]]]]],             # Right-heavy nesting => 15
    [[[[[1], 2], 3], 4], 5]              # Left-heavy nesting => 15
)


def tester(sumtree, trace=True):
    for test in tests:
        print(sumtree(test, trace))


def sumtree(L, trace=False):
    tot = 0
    for x in L:                                 # For each item at this level
        if isinstance(x, int):
            tot += x                            # Add numbers directly
            if trace: print(x, end=', ')
        else:
            tot += sumtree(x, trace)            # Recur for sublists
    return tot


def sumtree_queue(L, trace=False):                     # Breadth-first, explicit queue
    tot = 0
    items = list(L)                              # Start with copy of top level
    while items:
        front = items.pop(0)                     # Fetch/delete front item
        if isinstance(front, int):
            tot += front                         # Add numbers directly
            if trace: print(front, end=', ')
        else:
            items.extend(front)                  # <== Append all in nested list
    return tot


def sumtree_stack(L, trace=False):                     # Depth-first, explicit stack
    tot = 0
    items = list(L)                              # Start with copy of top level
    while items:
        front = items.pop(0)                     # Fetch/delete front item
        if isinstance(front, int):
            tot += front                         # Add numbers directly
            if trace: print(front, end=', ')
        else:
            items[:0] = front                    # <== Prepend all in nested list
    return tot


if __name__ == '__main__':
    tester(sumtree)
    print("=" * 36)
    tester(sumtree_queue)
    print("=" * 36)
    tester(sumtree_stack)
