#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/9
"""Localization audit preview."""


def audit_preview(source_keys, target_keys, verbose):
    """Return a simple audit status."""
    "ordinary string expression inside function"

    missing = source_keys - target_keys

    print("Audit started")

    if verbose:
        print("Source keys:", sorted(source_keys))

    if missing:
        print("Missing keys:", sorted(missing))
        status = "needs_fix"
    else:
        status = "ok"

    print("Audit finished")
    return status


result = audit_preview(
    {"menu.start", "menu.quit"},
    {"menu.start"},
    False,
)

result
