#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/20

import inspect
import sys


def print_signature(obj):
    """Print an object's runtime signature when available."""

    try:
        sig = inspect.signature(obj)
    except (TypeError, ValueError) as exc:
        print(
            "signature unavailable:",
            type(exc).__name__,
            str(exc),
        )
        return None

    print("signature:", sig)

    for parameter in sig.parameters.values():
        print(
            "parameter:",
            parameter.name,
            "| kind:",
            parameter.kind,
            "| default:",
            parameter.default,
        )

    return sig


def traced(label, values):
    """Yield values while reporting each consumption."""

    for value in values:
        print(f"yield {label}: {value!r}")
        yield value


def export_entries(
    entries,
    /,
    *,
    encoding="utf-8",
    strict=False,
):
    """Demonstrate positional-only and keyword-only parameters."""

    print("FUNCTION BODY EXECUTED")

    return {
        "entries": entries,
        "encoding": encoding,
        "strict": strict,
    }


print("=== Environment ===")
print("version:", sys.version)
print("executable:", sys.executable)
print("implementation:", sys.implementation.name)

print("\n=== Runtime signatures ===")

for obj in (
    zip,
    sorted,
    list.sort,
    range,
    len,
    export_entries,
):
    print("\nobject:", obj)
    print_signature(obj)

print("\n=== Signature.bind() ===")
export_sig = inspect.signature(export_entries)

binding_cases = [
    (
        (
            ["menu.start=开始游戏"],
        ),
        {},
    ),
    (
        (
            ["menu.start=开始游戏"],
        ),
        {
            "encoding": "utf-8",
            "strict": True,
        },
    ),
    (
        (),
        {
            "entries": ["menu.start=开始游戏"],
        },
    ),
    (
        (
            ["menu.start=开始游戏"],
            "utf-8",
        ),
        {},
    ),
]

for args, kwargs in binding_cases:
    print("\nargs:", args)
    print("kwargs:", kwargs)

    try:
        bound = export_sig.bind(
            *args,
            **kwargs,
        )
    except TypeError as exc:
        print(
            "binding error:",
            type(exc).__name__,
            str(exc),
        )
    else:
        print("explicit binding:", bound.arguments)
        bound.apply_defaults()
        print("with defaults:", bound.arguments)

print("\n=== zip() laziness and strictness ===")
left = traced(
    "left",
    [1, 2],
)
right = traced(
    "right",
    ["a", "b", "c"],
)

pairs = zip(
    left,
    right,
    strict=True,
)

print("zip created")

collected = []

try:
    for pair in pairs:
        print("pair:", pair)
        collected.append(pair)
except ValueError as exc:
    print(
        "zip error:",
        type(exc).__name__,
        str(exc),
    )

print("collected before failure:", collected)

print("\n=== Default zip truncation ===")
default_pairs = list(
    zip(
        [1, 2],
        ["a", "b", "c"],
    )
)

print(default_pairs)

print("\n=== list.sort() side effect and return ===")
records = [
    ("menu.start", 2),
    ("menu.quit", 1),
    ("menu.options", 2),
]

original_id = id(records)

sort_result = records.sort(
    key=lambda item: item[1],
)

print("sorted records:", records)
print("return value:", repr(sort_result))
print("same outer list:", id(records) == original_id)

print("\n=== sort failure boundary ===")
mixed = [3, "2", 1]

try:
    mixed.sort()
except TypeError as exc:
    print(
        "sort error:",
        type(exc).__name__,
        str(exc),
    )

print("state after failure:", mixed)
