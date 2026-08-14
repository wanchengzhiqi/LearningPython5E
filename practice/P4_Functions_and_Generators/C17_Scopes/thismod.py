#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/11

var = 99  # Global variable == module attribute


def local():
    var = 0  # Change local var


def glob1():
    global var  # Declare global (normal)
    var += 1  # Change global var


def glob2():
    var = 0  # Change local var
    import practice.P4_Functions_and_Generators.C17_Scopes.thismod as thismod  # Import myself
    thismod.var += 1  # Change global var


def glob3():
    var = 0  # Change local var
    import sys  # Import system table
    global_env = sys.modules["practice.P4_Functions_and_Generators.C17_Scopes.thismod"]  # Get module object (or use __name__)
    global_env.var += 1  # Change global var


def test():
    print(var)
    local(); glob1(); glob2(); glob3()
    print(var)
