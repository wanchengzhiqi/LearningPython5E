#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/10

import importlib.abc

from myimporter.utils.setup_loggers import setup_logging
from myimporter.utils.trace import trace, TraceScope, is_enabled
from myimporter.utils.settings import MYIMPORTER_DEBUG_ENVAR_NAME, MYIMPORTER_TRACE_ENVAR_NAME, FINDER_CUSTOMFINDER_FIND_SPEC_EXCLUDED_MODULES

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)


def get_real_caller():
    try:
        import inspect

        stack = inspect.stack()
        for frame in stack[2:]:
            module = inspect.getmodule(frame[0])
            if module and module.__name__ != __name__:
                return f"{module.__name__}:{frame.function}:{frame.lineno}"
    except Exception as e:
        logger.error(f"[GetRealCaller] Error while inspecting stack: {e}")
        return "unknown"


class CustomFinder(importlib.abc.MetaPathFinder):
    def __init__(self, providers):
        self.providers = providers
        self._cache = {}

    def find_spec(self, fullname, path=None, target=None):
        import sys

        if is_enabled(MYIMPORTER_TRACE_ENVAR_NAME):
            trace(f"import request from: {fullname} (which is from {get_real_caller()})", MYIMPORTER_TRACE_ENVAR_NAME)

        # 首先检查sys.modules，避免重复加载已经存在的模块，这也是Python导入系统的标准行为
        if fullname in sys.modules:
            logger.debug(f"[CustomFinder] Module {fullname} already in sys.modules, skipping CustomFinder")
            return None

        # 检查内置模块，内置模块不应该由CustomFinder处理，这也是Python导入系统的标准行为
        root_name = fullname.partition('.')[0]
        if fullname in sys.builtin_module_names or root_name in FINDER_CUSTOMFINDER_FIND_SPEC_EXCLUDED_MODULES:
            logger.warning(f"[CustomFinder] Module {fullname} is a built-in module, skipping CustomFinder")
            return None

        # 检查缓存，避免重复搜索已经找到的模块，这也是一个性能优化措施
        if fullname in self._cache:
            logger.debug(f"[CustomFinder] Module {fullname} found in cache")
            return self._cache[fullname]

        with TraceScope(f"Finding module {fullname}", MYIMPORTER_TRACE_ENVAR_NAME):
            for provider in self.providers:
                try:
                    spec = provider.find(fullname, search_paths=path)
                    if spec is not None:
                        # 记录模块是否具有位置属性，这对于调试和错误处理非常有用
                        self.has_location = hasattr(spec, 'origin') and spec.origin is not None
                        self._cache[fullname] = spec
                        return spec
                except Exception as e:
                    logger.error(f"[CustomFinder] Error in provider {provider} while finding module {fullname}: {e}")
                    continue

        logger.debug(f"[CustomFinder] Module {fullname} not found by any provider, will leave it to python's default import system")
        return None

    def invalidate_caches(self):
        self._cache.clear()
