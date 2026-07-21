#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/19

import sys
from inspect import getattr_static


class LocalizationProxy:
    """Provide localization metadata through dynamic attributes."""

    def __init__(self):
        self._values = {
            "title": "Start Game",
            "language": "en",
        }
        self.cached_state = "ready"

    def __getattr__(self, name):
        print(f"__getattr__ called: {name!r}")

        try:
            return self._values[name]
        except KeyError:
            raise AttributeError(name) from None

    def __dir__(self):
        print("__dir__ called")

        return (
            "title",
            "language",
            "ghost",
        )


class AttributeProbe:
    @property
    def stable(self):
        print("stable property executed")
        return 42

    @property
    def unavailable(self):
        print("unavailable property executed")
        raise AttributeError("value is not ready")

    @property
    def broken(self):
        print("broken property executed")
        raise RuntimeError("backend failed")


def discover_candidate_names(
    obj,
    *,
    include_private=False,
    limit=None,
):
    """Return candidate names reported by dir()."""

    names = dir(obj)

    if not include_private:
        names = [
            name
            for name in names
            if not name.startswith("_")
        ]

    if limit is not None:
        if not isinstance(limit, int):
            raise TypeError("limit must be int or None")

        if limit < 0:
            raise ValueError("limit must be non-negative")

        names = names[:limit]

    return names


print("=== Environment ===")
print("version:", sys.version)
print("executable:", sys.executable)
print("implementation:", sys.implementation.name)

proxy = LocalizationProxy()

print("\n=== Custom dir ===")
proxy_names = dir(proxy)
print("reported names:", proxy_names)

print("\n=== Accessible but omitted ===")
print("cached_state in dir:", "cached_state" in proxy_names)
print("cached_state:", proxy.cached_state)

print("\n=== Dynamic and reported ===")
print("title in dir:", "title" in proxy_names)
print("title:", proxy.title)

print("\n=== Reported but unavailable ===")
print("ghost in dir:", "ghost" in proxy_names)
print("hasattr ghost:", hasattr(proxy, "ghost"))

probe = AttributeProbe()

print("\n=== hasattr executes lookup ===")
print("stable in dir:", "stable" in dir(probe))
print("hasattr stable:", hasattr(probe, "stable"))

print("\n=== AttributeError becomes False ===")
print("hasattr unavailable:", hasattr(probe, "unavailable"))

print("\n=== Other exceptions propagate ===")

try:
    print("hasattr broken:", hasattr(probe, "broken"))
except Exception as exc:
    print("exception:", type(exc).__name__, str(exc))

print("\n=== Static inspection ===")
static_stable = getattr_static(probe, "stable")
print("static type:", type(static_stable))
print("is property:", isinstance(static_stable, property))

print("\n=== Candidate discovery ===")

for obj in (
    [],
    {},
    range(3),
    enumerate(["a", "b"]),
    proxy,
):
    print(
        type(obj).__name__,
        discover_candidate_names(
            obj,
            limit=8,
        ),
    )
