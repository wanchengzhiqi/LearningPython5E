#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from myimporter.core.finder import CustomFinder
from myimporter.core.path_manager import PathManager
from myimporter.core.providers import FileSystemProvider, env_provider
from myimporter.utils.settings import (
    MYIMPORTER_CURRENT_MODE,
    MYIMPORTER_DEBUG_ENVAR_NAME,
    MYIMPORTER_MODE,
    MYIMPORTER_ROOT_DIRECTORY,
    PLUGINMANAGER_DEFAULT_PLUGIN_PATHS,
)
from myimporter.utils.setup_loggers import setup_logging

_finder = None
_path_manager = PathManager()
logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)


def default_paths():
    return [MYIMPORTER_ROOT_DIRECTORY, *PLUGINMANAGER_DEFAULT_PLUGIN_PATHS]


def _finder_priority(default):
    if _finder is not None:
        try:
            return sys.meta_path.index(_finder)
        except ValueError:
            pass
    return default


def _build_candidate(paths, mod):
    candidate_manager = PathManager()
    if _finder is None or (
        MYIMPORTER_CURRENT_MODE[0] == MYIMPORTER_MODE[2]
        and mod == MYIMPORTER_MODE[1]
    ):
        candidate_manager.add(default_paths())
    else:
        candidate_manager.add(_path_manager.get_paths())

    if mod == MYIMPORTER_MODE[2] and MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[2]:
        candidate_manager.add(env_provider())

    if paths:
        candidate_manager.add(paths)

    provider = FileSystemProvider(candidate_manager)
    return candidate_manager, CustomFinder(providers=[provider])


def install(paths=None, mod=MYIMPORTER_MODE[0], priority=0):
    logger.info("[Installer] install called")
    global _finder, _path_manager

    if MYIMPORTER_CURRENT_MODE[0] not in MYIMPORTER_MODE:
        uninstall()
        logger.error(
            "[Installer] Invalid current mode detected. "
            f"The mode has been reset to {MYIMPORTER_MODE[0]}."
        )
        return

    if mod not in MYIMPORTER_MODE:
        raise ValueError(f"Unknown myimporter mode: {mod!r}.")

    if mod == MYIMPORTER_MODE[0]:
        uninstall()
        return

    if not isinstance(priority, int):
        raise TypeError("priority must be an integer.")

    candidate_manager, candidate_finder = _build_candidate(paths, mod)
    priority = _finder_priority(priority)

    if _finder is not None:
        sys.meta_path[:] = [finder for finder in sys.meta_path if finder is not _finder]
    sys.meta_path.insert(priority, candidate_finder)

    _path_manager = candidate_manager
    _finder = candidate_finder
    MYIMPORTER_CURRENT_MODE[0] = mod
    logger.info(f"[Installer] initialized successfully in {mod}")
    logger.info(f"[Installer] paths now: {_path_manager.get_paths()}")


def uninstall():
    logger.info("[Uninstaller] uninstall called")
    global _finder, _path_manager

    if _finder is not None:
        sys.meta_path[:] = [finder for finder in sys.meta_path if finder is not _finder]
        _finder.invalidate_caches()

    _finder = None
    _path_manager.clear()
    MYIMPORTER_CURRENT_MODE[0] = MYIMPORTER_MODE[0]
    logger.info(f"[Uninstaller] reset to {MYIMPORTER_MODE[0]}")
