#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/6

n = 255

print("display")
print(bin(n), oct(n), hex(n))
print(f"{n:08b}", f"{n:04x}", f"{n:04X}")

print("parse")
print(int("10", 2))
print(int("10", 10))
print(int("10", 16))
print(int("0xff", 0))

print("bytes")
b = b"\x41\x42\x43"
print(b)
print(list(b))

print("unicode")
s = "你"
print(ord(s))
print(hex(ord(s)))
print(s.encode("utf-8"))
print(list(s.encode("utf-8")))
