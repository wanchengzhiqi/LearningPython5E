#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/16


class Plugin:
    name = 'plugin_b'
    version = "1.1"

    def activate(self):
        print(f"Activating {self.name}")

    def deactivate(self):
        print(f"Deactivating {self.name}")
