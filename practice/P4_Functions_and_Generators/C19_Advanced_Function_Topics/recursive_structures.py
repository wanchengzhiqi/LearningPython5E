#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/3


def normalize_tree(node, depth=0):
    print(
        "  " * depth,
        "ENTER:",
        repr(node),
        sep="",
    )

    if isinstance(node, str):
        result = node.strip().lower()

        print(
            "  " * depth,
            "LEAF RETURN:",
            repr(result),
            sep="",
        )

        return result

    if not isinstance(node, list):
        raise TypeError(
            "node must be str or list"
        )

    result = []

    for child in node:
        child_result = normalize_tree(
            child,
            depth + 1,
        )
        result.append(child_result)

    print(
        "  " * depth,
        "LIST RETURN:",
        repr(result),
        sep="",
    )

    return result


tree = [
    " A ",
    [
        " B ",
        " C ",
    ],
]

normalized = normalize_tree(tree)

print("FINAL:", normalized)
