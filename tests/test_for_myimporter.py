#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/11

import src.myimporter

src.myimporter.install(paths=['E:\\'], mod='dev_mod')

import brian, test_module, module1, sys

print(sys.path)
print('src.myimporter' in sys.modules)
print(test_module.hello())

src.myimporter.uninstall()

import showargs
