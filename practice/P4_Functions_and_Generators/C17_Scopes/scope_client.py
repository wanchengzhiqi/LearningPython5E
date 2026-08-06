#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/5

import scope_source

LABEL = "client"
label = "client module"


def caller():
    label = "caller local"
    return scope_source.read_label()


print(caller())
print(scope_source.read_label.__module__)
print(
    scope_source.read_label.__globals__
    is scope_source.__dict__
)

print(scope_source.read_label())
scope_source.label = "changed by client"
print(scope_source.read_label())

print(scope_source.inspect_global())
print(scope_source.inspect_global.__globals__ is scope_source.__dict__)
