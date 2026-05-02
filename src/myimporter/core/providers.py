#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/14

import os
import importlib.util

from src.myimporter.core.loader import CustomLoader
from src.myimporter.utils.trace import trace
from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.utils.settings import MYIMPORTER_DEBUG_ENVAR_NAME, MYIMPORTER_TRACE_ENVAR_NAME, MYIMPORTER_ENVAR_PROVIDER_ENVAR_NAME

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)


class BaseProvider:
    def find(self, fullname):
        raise NotImplementedError("Subclasses must implement the find method.")


class FileSystemProvider(BaseProvider):
    def __init__(self, path_manager):
        self.pm = path_manager

    def find(self, fullname):
        logger.debug(f"[FileSystemProvider] searching: {fullname}")
        parts = fullname.split('.')
        rel_path = os.path.join(*parts)

        for base in self.pm.get_paths():
            trace(f"  trying base: {base}", MYIMPORTER_TRACE_ENVAR_NAME)
            module_path = os.path.join(base, rel_path)

            # 首先检查是否存在 .py 文件
            file_path = module_path + '.py'
            if os.path.isfile(file_path):
                logger.info(f"[FileSystemProvider] found module: {file_path}")
                return importlib.util.spec_from_file_location(fullname, file_path, loader=CustomLoader(path=file_path))

            # 如果没有 .py 文件，检查是否存在一个目录，并且该目录下有 __init__.py 文件
            init_path = os.path.join(module_path, '__init__.py')
            if os.path.isfile(init_path):
                logger.info(f"[FileSystemProvider] found package: {init_path}")
                return importlib.util.spec_from_file_location(fullname, init_path, loader=CustomLoader(path=init_path), submodule_search_locations=[module_path])
        logger.warning(f"[FileSystemProvider] not found: {fullname}")
        return None


def env_provider():
    env_var = os.getenv(MYIMPORTER_ENVAR_PROVIDER_ENVAR_NAME)
    if env_var:
        logger.debug(f"[EnvProvider] found environment variable: {env_var}")
        # print(f'checking environment variable MY_MODULE_PATHS: {env_var.split(os.pathsep)}')
        return env_var.split(os.pathsep)
    logger.error(f"[EnvProvider] No environment variable {MYIMPORTER_ENVAR_PROVIDER_ENVAR_NAME} found.")
    raise ValueError(f"Environment variable {MYIMPORTER_ENVAR_PROVIDER_ENVAR_NAME} is required for env_provider but was not found.")
