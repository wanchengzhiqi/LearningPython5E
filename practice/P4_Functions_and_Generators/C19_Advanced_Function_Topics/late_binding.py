#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/31


def make_late_handlers():
    handlers = []

    for label in ("UI", "SYSTEM", "NPC"):
        def handler():
            return label

        handlers.append(handler)

    return handlers


def make_saved_handlers():
    handlers = []

    for label in ("UI", "SYSTEM", "NPC"):
        def handler(saved_label=label):
            return saved_label

        handlers.append(handler)

    return handlers


late = make_late_handlers()
saved = make_saved_handlers()


print("late results:")
for handler in late:
    print(handler())


print("\nsaved results:")
for handler in saved:
    print(handler())


print(
    "\nlate cells shared:",
    late[0].__closure__[0]
    is late[1].__closure__[0]
    is late[2].__closure__[0],
)

print(
    "late freevars:",
    late[0].__code__.co_freevars,
)

print(
    "saved freevars:",
    saved[0].__code__.co_freevars,
)

print(
    "saved defaults:",
    [handler.__defaults__ for handler in saved],
)
