#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/20
"""A demonstration module for pydoc imports."""

print("MODULE IMPORT SIDE EFFECT")


def normalize_key(text):
    """Normalize one key."""
    return text.strip().lower()


if __name__ == "__main__":
    print("SCRIPT-ONLY DEMONSTRATION")
