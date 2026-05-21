#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/19

import copy

original = [
    ["MENU_START", ["ui"]],
    ["MENU_EXIT", ["ui", "todo"]],
]

via_slice = original[:]
via_list = list(original)
via_copy = copy.copy(original)
via_deep = copy.deepcopy(original)

original[0][1].append("checked")
print(via_slice, via_list, via_copy, via_deep, sep='\n')
