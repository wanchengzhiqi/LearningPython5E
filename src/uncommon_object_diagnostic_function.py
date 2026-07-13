#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/11

from collections.abc import Iterable, Iterator


def iteration_profile(obj):
    profile = {
        "type": type(obj).__qualname__,
        "abc_iterable": isinstance(obj, Iterable),
        "abc_iterator": isinstance(obj, Iterator),
    }

    try:
        iterator = iter(obj)
    except TypeError as exc:
        profile.update({
            "operationally_iterable": False,
            "object_is_iterator": False,
            "iterator_type": None,
            "iter_error": str(exc),
        })
    else:
        profile.update({
            "operationally_iterable": True,
            "object_is_iterator": iterator is obj,
            "iterator_type": type(iterator).__qualname__,
            "iter_error": None,
        })

    return profile
