#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Optional global bootstrap template for myimporter.

Copy this file to the interpreter's site-packages directory as
``sitecustomize.py`` only when a global opt-in bootstrap is desired.
"""

import os
import sys
import warnings

ENABLE_ENV = "ENABLE_MYIMPORTER"
DEBUG_ENV = "SITECUSTOMIZE_DEBUG"
SOURCE_ROOT_ENV = "MYIMPORTER_SOURCE_ROOT"

if os.getenv(ENABLE_ENV) == "1":
    try:
        source_root = os.getenv(SOURCE_ROOT_ENV)
        if source_root and source_root not in sys.path:
            sys.path.insert(0, source_root)

        import myimporter
        from myimporter.utils.settings import MYIMPORTER_MODE

        myimporter.install(mod=MYIMPORTER_MODE[2])
    except Exception as exc:
        warnings.warn(f"myimporter bootstrap failed: {exc}", RuntimeWarning)
        if os.getenv(DEBUG_ENV) == "1":
            import traceback

            traceback.print_exc()
