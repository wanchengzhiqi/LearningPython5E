#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/6

READ = 1 << 0
WRITE = 1 << 1
EXECUTE = 1 << 2

flags = 0
flags |= READ
flags |= WRITE

print(f"flags: {flags:03b}")
print("read:", bool(flags & READ))
print("execute:", bool(flags & EXECUTE))

flags &= ~WRITE
print(f"remove write: {flags:03b}")

flags ^= EXECUTE
print(f"toggle execute: {flags:03b}")

byte = 0xAB
print(f"byte: {byte:08b}")
print(f"high: {byte >> 4:X}")
print(f"low: {byte & 0x0F:X}")

x = 5
print(~x)
print(f"{(~x) & 0xff:08b}")
