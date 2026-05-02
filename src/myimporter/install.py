#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/10

import sys
import os

from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.core.finder import CustomFinder
from src.myimporter.core.path_manager import PathManager
from src.myimporter.core.providers import FileSystemProvider, env_provider
from src.myimporter.utils.settings import LP5E_ROOT_DIRECTORY, MYIMPORTER_MODE, MYIMPORTER_CURRENT_MODE, MYIMPORTER_DEBUG_ENVAR_NAME

_finder = None
_path_manager = PathManager()
logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)


def default_paths():
    # 自动定位src\plugins目录，假设当前文件位于src\myimporter目录下
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 构建默认的插件目录路径
    default_plugin_path = os.path.join(parent_dir, 'plugins')
    return [LP5E_ROOT_DIRECTORY, default_plugin_path]


def install(paths=None, mod=MYIMPORTER_MODE[0], priority=0):
    logger.info("[Installer] install called")
    global _finder, _path_manager

    if MYIMPORTER_CURRENT_MODE[0] not in MYIMPORTER_MODE:
        if _finder is not None:
            uninstall()
        else:
            MYIMPORTER_CURRENT_MODE[0] = MYIMPORTER_MODE[0]
        logger.error(f"[Installer] It is strictly forbidden to switch modes by manually modifying the variable MYIMPORTER_CURRENT_MODE in the settings.py file! Otherwise, it may lead to serious consequences!!! The current mode of myimporter has been reset to the default mode: {MYIMPORTER_MODE[0]}")
        return

    if mod not in MYIMPORTER_MODE[1:]:
        if _finder is not None:
            uninstall()
        else:
            MYIMPORTER_CURRENT_MODE[0] = MYIMPORTER_MODE[0]
        logger.info(f"[Installer] myimporter初始化成功...当前模式为 {MYIMPORTER_MODE[0]}")
        return

    if mod == MYIMPORTER_MODE[1] and MYIMPORTER_CURRENT_MODE[0] == MYIMPORTER_MODE[2]:
        uninstall()

    if _finder is None:
        logger.info("[Installer] creating CustomFinder")
        provider = FileSystemProvider(_path_manager)
        _finder = CustomFinder(providers=[provider])
        sys.meta_path.insert(priority, _finder)

        _path_manager.add(default_paths())
        logger.info("[Installer] added default paths")
        MYIMPORTER_CURRENT_MODE[0] = MYIMPORTER_MODE[1]

    if mod == MYIMPORTER_MODE[2] and MYIMPORTER_CURRENT_MODE != mod:
        _path_manager.add(env_provider())
        logger.info("[Installer] added environment variable paths")
        MYIMPORTER_CURRENT_MODE[0] = MYIMPORTER_MODE[2]

    # 如果用户提供了路径参数，则将这些路径添加到PathManager中
    if paths:
        _path_manager.add(paths)
        logger.info("[Installer] added user_provided paths")

    logger.info(f"[Installer] myimporter初始化成功...当前模式为 {mod}")
    logger.info(f"[Installer] paths now: {_path_manager.get_paths()}")


def uninstall():
    logger.info("[Uninstaller] uninstall called")
    global _finder, _path_manager

    if _finder is None:
        MYIMPORTER_CURRENT_MODE[0] = MYIMPORTER_MODE[0]
        logger.warning("[Uninstaller] CustomFinder is not created, nothing to uninstall")
        logger.info(f"[Uninstaller] The current mode of myimporter has been reset to the default mode: {MYIMPORTER_MODE[0]}")
        return

    # 从sys.meta_path中移除CustomFinder实例
    sys.meta_path[:] = [f for f in sys.meta_path if f is not _finder]

    _finder = None
    _path_manager.clear()
    MYIMPORTER_CURRENT_MODE[0] = MYIMPORTER_MODE[0]
    logger.info("[Uninstaller] uninstalled successfully")
    logger.info(f"[Uninstaller] The current mode of myimporter has been reset to the default mode: {MYIMPORTER_MODE[0]}")
