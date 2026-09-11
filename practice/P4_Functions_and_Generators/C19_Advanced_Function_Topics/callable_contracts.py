#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/9

from collections.abc import Callable
from inspect import signature


def apply_rule(
    rule: Callable[[str], str],
    text: str,
) -> str:
    return rule(text)


def good(text: str) -> str:
    return text.strip().lower()


def wrong_arity() -> str:
    return "fixed"


def surprising(value: int) -> int:
    return value * 2


rules = [
    good,
    wrong_arity,
    surprising,
]


for rule in rules:
    print(
        "\nRULE:",
        rule.__name__,
    )

    print(
        "callable:",
        callable(rule),
    )

    sig = signature(rule)

    print(
        "signature:",
        sig,
    )

    try:
        bound = sig.bind("START")
    except TypeError as exc:
        print(
            "bind failed:",
            exc,
        )
    else:
        print(
            "bind succeeded:",
            bound.arguments,
        )

    try:
        result = apply_rule(
            rule,
            "START",
        )
    except Exception as exc:
        print(
            "call failed:",
            type(exc).__name__,
            exc,
        )
    else:
        print(
            "call result:",
            repr(result),
            type(result).__name__,
        )
