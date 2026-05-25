#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/23


class WeirdDict(dict):
    def __iter__(self):
        return iter(["from_iter"])

    def keys(self):
        return ["from_keys"]


wd = WeirdDict({"a": 1})

print(list(wd))         # ['from_iter']
print(list(wd.keys()))  # ['from_keys']
