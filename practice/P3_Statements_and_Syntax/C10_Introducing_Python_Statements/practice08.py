#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/10
"""C10 checkpoint."""

print("module start")


def make_status(debug):
    """Return status."""
    "ordinary string"

    events = []
    print(events.append("entered"))

    if debug:
        events.append("debug")
        return "debug"

    events.append("normal")
    print(events)
    return "normal"


print("after def")

status = make_status(False)

status
