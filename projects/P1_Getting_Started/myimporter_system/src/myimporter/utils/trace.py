#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/15

import os
import threading

# thread-local storage to keep track of the current import stack
_local = threading.local()


def is_enabled(envar_name=None):
    return os.getenv(envar_name) == "1" if envar_name else False


def _get_depth():
    return getattr(_local, 'depth', 0)


def _set_depth(d):
    _local.depth = d


def trace(msg, envar_name=None):
    if not is_enabled(envar_name):
        return

    indent = '  ' * _get_depth()
    print(f'[TRACE]{indent}{msg}')


# Context manager for tracing a block of code
class TraceScope:
    def __init__(self, label, envar_name=None):
        self.label = label
        self.envar_name = envar_name

    def __enter__(self):
        if is_enabled(self.envar_name):
            trace(f'--> {self.label}', self.envar_name)
            _set_depth(_get_depth() + 1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if is_enabled(self.envar_name):
            _set_depth(_get_depth() - 1)
            trace(f'<-- {self.label}', self.envar_name)
