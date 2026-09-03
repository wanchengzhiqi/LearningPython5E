#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/1

import inspect


def make_default_handlers(labels):
    handlers = []

    for label in labels:
        handlers.append(
            lambda saved=label: saved
        )

    return handlers


def make_one_handler(label):
    def handler():
        return label

    return handler


def make_factory_handlers(labels):
    handlers = []

    for label in labels:
        handlers.append(
            make_one_handler(label)
        )

    return handlers


labels = ("UI", "SYSTEM", "NPC")

defaults = make_default_handlers(labels)
closures = make_factory_handlers(labels)


print("results:")

for default_handler, closure_handler in zip(
    defaults,
    closures,
):
    print(
        default_handler(),
        closure_handler(),
    )


print("\ndefault technique:")

for handler in defaults:
    print(
        "signature:",
        inspect.signature(handler),
        "defaults:",
        handler.__defaults__,
        "freevars:",
        handler.__code__.co_freevars,
        "closure:",
        handler.__closure__,
    )


print("\nfactory technique:")

for handler in closures:
    print(
        "signature:",
        inspect.signature(handler),
        "defaults:",
        handler.__defaults__,
        "freevars:",
        handler.__code__.co_freevars,
        "closure value:",
        handler.__closure__[0].cell_contents,
    )
