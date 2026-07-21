#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/19

import sys
from contextlib import redirect_stdout
from io import StringIO


"""Localization documentation experiment."""


"An ordinary module-level string expression."


def normalize_key(text):
    """Return a normalized localization key."""

    "An ordinary function-body string expression."
    return text.strip().lower()


def misplaced_docstring(text):
    result = text.strip()

    """This is not the function's docstring."""

    return result


class LocalizationEntry:
    """Represent one localization entry."""

    category = "dialogue"

    "An ordinary class-body string expression."


print("=== Environment ===")
print("version:", sys.version)
print("executable:", sys.executable)
print("implementation:", sys.implementation.name)

print("\n=== __doc__ metadata ===")
print("module:", repr(__doc__))
print("normalize_key:", repr(normalize_key.__doc__))
print("misplaced_docstring:", repr(misplaced_docstring.__doc__))
print("LocalizationEntry:", repr(LocalizationEntry.__doc__))

print("\n=== dir() ===")
names = dir(normalize_key)
print("result type:", type(names))
print("all names are str:", all(isinstance(name, str) for name in names))
print("alphabetically sorted:", names == sorted(names))
print("contains __doc__:", "__doc__" in names)
print("contains __name__:", "__name__" in names)

print("\n=== help() output versus return value ===")
buffer = StringIO()

with redirect_stdout(buffer):
    help_result = help(normalize_key)

help_text = buffer.getvalue()

print("return value:", repr(help_result))
print("return type:", type(help_result))
print("produced output:", bool(help_text))
print("mentions normalize_key:", "normalize_key" in help_text)
print(
    "contains docstring:",
    normalize_key.__doc__ in help_text,
)

print("\n=== Object behavior ===")
print(normalize_key("  UI.MENU.START  "))
