#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/11

X = 99


def setX(new):  # Accessor make external changes explicit
    global X  # And can manage access in a single place
    X = new
