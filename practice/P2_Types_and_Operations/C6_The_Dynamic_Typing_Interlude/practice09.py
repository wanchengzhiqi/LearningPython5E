#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/4


def total_length(items):
    total = 0
    for item in items:
        total += len(item)
    return total


def get_name(user):
    return user['name']
