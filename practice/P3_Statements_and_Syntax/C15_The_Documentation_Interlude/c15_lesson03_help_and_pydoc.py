#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/20

import pydoc
import sys
from contextlib import redirect_stdout
from io import StringIO


def normalize_key(text, *, keep_case=False):
    """Normalize one localization key.

    Leading and trailing whitespace is removed.
    The result is lowercased unless keep_case is true.
    """

    text = text.strip()

    if not keep_case:
        text = text.lower()

    return text


print("=== Environment ===")
print("version:", sys.version)
print("executable:", sys.executable)
print("implementation:", sys.implementation.name)

print("\n=== Raw __doc__ ===")
raw_doc = normalize_key.__doc__

print("type:", type(raw_doc))
print("repr:", repr(raw_doc))

print("\n=== Captured help() ===")
help_buffer = StringIO()

with redirect_stdout(help_buffer):
    help_result = help(normalize_key)

help_text = help_buffer.getvalue()

print("return value:", repr(help_result))
print("return type:", type(help_result))
print("captured type:", type(help_text))
print("captured non-empty:", bool(help_text))
print(
    "contains function name:",
    "normalize_key" in help_text,
)
print(
    "contains parameter:",
    "keep_case" in help_text,
)
print(
    "contains doc summary:",
    "Normalize one localization key." in help_text,
)

print("\n=== pydoc.render_doc() ===")
rendered_text = pydoc.render_doc(
    normalize_key,
    renderer=pydoc.plaintext,
)

print("return type:", type(rendered_text))
print("non-empty:", bool(rendered_text))
print(
    "contains function name:",
    "normalize_key" in rendered_text,
)
print(
    "contains parameter:",
    "keep_case" in rendered_text,
)
print(
    "contains doc summary:",
    "Normalize one localization key." in rendered_text,
)

print("\n=== Two documentation layers ===")
print("raw doc length:", len(raw_doc))
print("help text length:", len(help_text))
print("rendered text length:", len(rendered_text))

print(
    "help equals raw doc:",
    help_text == raw_doc,
)
print(
    "rendered equals raw doc:",
    rendered_text == raw_doc,
)

print("\n=== Object behavior ===")
print(normalize_key("  UI.MENU.START  "))
print(
    normalize_key(
        "  UI.Menu.Start  ",
        keep_case=True,
    )
)
