#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/27

from practice.P4_Functions_and_Generators.C18_Arguments.print3 import print3

print3(1, 2, 3)
print3(1, 2, 3, sep="")
print3(1, 2, 3, sep="...")
print3(1, [2], (3, ), sep="...")

print3(4, 5, 6, sep="", end="")
print3(7, 8, 9)
print3()

import sys

print3(1, 2, 3, sep="??", end=".\n", file=sys.stderr)
