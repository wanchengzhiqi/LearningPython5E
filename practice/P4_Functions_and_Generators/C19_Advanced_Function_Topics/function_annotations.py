#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/8

from annotationlib import (
    Format,
    get_annotations,
)
from inspect import signature


def probe(name, value):
    print("EVALUATE:", name)
    return value


def demo(
    value: probe("annotation", int)
    = probe("default", 10),
) -> int:
    print("BODY:", value)
    return value


print("\n=== definition finished ===")


print("\n=== ordinary call ===")

result = demo()

print("result:", result)


print("\n=== string annotations ===")

print(
    get_annotations(
        demo,
        format=Format.STRING,
    )
)


print("\n=== value annotations ===")

print(
    get_annotations(
        demo,
        format=Format.VALUE,
    )
)


print("\n=== direct __annotations__ ===")

print(demo.__annotations__)


print("\n=== signature ===")

print(
    signature(
        demo,
        annotation_format=Format.STRING,
    )
)
