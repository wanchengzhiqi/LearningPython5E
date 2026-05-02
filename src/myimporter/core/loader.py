#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/10

import importlib.abc

from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.utils.settings import MYIMPORTER_DEBUG_ENVAR_NAME

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)


class CustomLoader(importlib.abc.SourceLoader):
    def __init__(self, path):
        self.path = path

    # SourceLoader requires get_filename and get_data methods to be implemented
    def get_filename(self, fullname):
        logger.debug(f"[CustomLoader] getting filename for module: {fullname}, path: {self.path}")
        return self.path

    def get_data(self, path):
        logger.debug(f"[CustomLoader] loading data from path: {path}")
        with open(path, 'rb') as f:
            return f.read()

    # 可选：实现 path_stats 方法以提供文件的修改时间和大小等信息
    def path_stats(self, path):
        logger.debug(f"[CustomLoader] getting stats for path: {path}")
        import os
        stat = os.stat(path)
        return {'mtime': stat.st_mtime, 'size': stat.st_size}
