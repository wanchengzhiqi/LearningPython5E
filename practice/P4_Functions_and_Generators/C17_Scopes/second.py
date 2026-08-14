#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/11

import practice.P4_Functions_and_Generators.C17_Scopes.first as first

print(first.X)  # OK: references a name in another file
first.X = 88  # But changing it can be too subtle and implicit
