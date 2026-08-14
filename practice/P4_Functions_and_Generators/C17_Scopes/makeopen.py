#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/12

import builtins


def makeopen(id):
    original = builtins.open

    def custom(*kargs, **pargs):
        print("Custom open call %r:" % id, kargs, pargs)
        return original(*kargs, **pargs)
    builtins.open = custom


class MakeOpen:
    def __init__(self, id):
        self.id = id
        self.original = builtins.open
        builtins.open = self

    def __call__(self, *kargs, **pargs):
        print("Custom open call %r:" % self.id, kargs, pargs)
        return self.original(*kargs, **pargs)
