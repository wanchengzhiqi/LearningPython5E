#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/12

s = "A中\n"

print(len(s))
print(repr(s))
print([hex(ord(ch)) for ch in s])

b = s.encode("utf-8")
print(len(b))
print(b)
print(list(b))
print(b.hex())

s2 = b.decode("utf-8")
print(s2 == s)
print(repr(s2))

a = "\u4e2d"
b = "中"
c = b"\xe4\xb8\xad"

print(a == b)
print(len(a))
print(len(c))
print(c.decode("utf-8") == b)
