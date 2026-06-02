#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/14

import os

from myimporter.utils.setup_loggers import setup_logging
from myimporter.utils.settings import MYIMPORTER_DEBUG_ENVAR_NAME

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)


class PathManager:
    def __init__(self):
        self._paths = []

    # 添加路径时，确保路径是绝对路径，并且规范化路径格式
    def normalize(self, p):
        if not p:
            logger.warning("[PathManager] Invalid path provided, skipping")
            return None

        p = os.path.expanduser(p)  # 展开用户目录
        p = os.path.expandvars(p)  # 展开环境变量

        # 在Windows上，使用os.path.normpath来规范化路径，处理反斜杠和斜杠的混用问题
        if os.name == 'nt':
            if len(p) >= 2 and p[1] == ':':
                if len(p) == 2 or p[2] != '\\':
                    p = p[:2] + '\\' + p[2:]

        p = os.path.abspath(p)  # 获取绝对路径
        p = os.path.normpath(p)  # 规范化路径，去除冗余的分隔符和上级目录引用
        # p = os.path.normcase(p)  # 在Windows上，规范化路径的大小写
        return p

    # 添加路径时，确保路径是绝对路径，并且规范化路径格式，同时检查路径是否存在并且是一个目录
    def add(self, paths):
        if isinstance(paths, (str, os.PathLike)):
            paths = [paths]

        normalized_paths = []
        for p in paths:
            if not isinstance(p, (str, os.PathLike)):
                raise TypeError(f"Expected a path-like object, got {type(p).__name__}.")

            p = os.fspath(p)
            normalized = self.normalize(p)
            logger.debug(f"[PathManager] normalize: {p} -> {normalized}")
            if normalized and os.path.isdir(normalized):
                normalized_paths.append(normalized)

        self._paths.extend(normalized_paths)

    # 清除所有路径，重置路径列表为空
    def clear(self):
        self._paths.clear()

    # 返回去重后的路径列表，确保路径的唯一性
    def get_paths(self):
        return list(dict.fromkeys(self._paths))
