#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/5

LABEL = "source"
label = "source module"


def read_label():
    return label


def inspect_global():
    return globals()["LABEL"]
