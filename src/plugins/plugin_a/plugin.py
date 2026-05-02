#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/15


class Plugin:
    name = "plugin_a"
    version = "1.1"

    def activate(self):
        print(f"{self.name} activated")

    def deactivate(self):
        print(f"{self.name} deactivated")

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version
        }
