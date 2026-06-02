#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/16


class Plugin:
    name = 'plugin_b'
    version = "1.2"

    def __init__(self):
        self.active = False

    def activate(self):
        self.active = True
        print(f"Activating {self.name}")

    def deactivate(self):
        self.active = False
        print(f"Deactivating {self.name}")

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "active": self.active
        }
