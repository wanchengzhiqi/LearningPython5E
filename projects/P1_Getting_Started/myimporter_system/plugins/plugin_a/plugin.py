#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/15


class Plugin:
    name = "plugin_a"
    version = "1.2"

    def __init__(self):
        self.active = False

    def activate(self):
        self.active = True
        print(f"{self.name} activated")

    def deactivate(self):
        self.active = False
        print(f"{self.name} deactivated")

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "active": self.active
        }
