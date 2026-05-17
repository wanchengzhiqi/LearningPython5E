#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/7

source = {"start", "exit", "save", "load"}
translated = {"start", "exit", "load", "debug"}

print("missing:", source - translated)
print("extra:", translated - source)
print("common:", source & translated)
print("all:", source | translated)

permissions = {"read", "write"}
print("read" in permissions)

required = {"read", "execute"}
print("has all:", required <= permissions)
print("has any:", bool(required & permissions))

print({1, 1.0, True})
print(len({1, 1.0, True}))
