#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/31

# 练习：将字符串写入文件
with open("myfile.txt", "w", encoding="utf-8") as f:
    f.write("Hello file world!\n")
