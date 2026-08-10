#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/6

import demo_settings


mode = "worker"


def change_mode(transgress=False):
    if transgress:
        demo_settings.mode = "debug"
    else:
        global mode

        mode = "debug"


change_mode()

print(mode)
print(demo_settings.mode)
