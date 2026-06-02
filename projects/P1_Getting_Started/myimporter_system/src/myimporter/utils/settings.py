#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path


def _integer_setting(name, default):
    try:
        return int(os.getenv(name, default))
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer.") from exc


def _float_setting(name, default):
    try:
        value = float(os.getenv(name, default))
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be a number.") from exc
    if value <= 0:
        raise RuntimeError(f"Environment variable {name} must be greater than zero.")
    return value


def _choice_setting(name, default, choices):
    value = os.getenv(name, default)
    if value not in choices:
        allowed = ", ".join(choices)
        raise RuntimeError(f"Environment variable {name} must be one of: {allowed}.")
    return value


def _path_list_setting(name, default):
    return [path for path in os.getenv(name, default).split(os.pathsep) if path]


PROJECT_ROOT = Path(__file__).resolve().parents[3]

HOST = os.getenv("MYIMPORTER_RUNTIME_HOST", "127.0.0.1")
PORT = _integer_setting("MYIMPORTER_RUNTIME_PORT", "5000")
WEB_UI_HOST = os.getenv("MYIMPORTER_WEB_UI_HOST", "127.0.0.1")
WEB_UI_PORT = _integer_setting("MYIMPORTER_WEB_UI_PORT", "8000")

MYIMPORTER_COLOREDLOGS_FORMAT = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
MYIMPORTER_MODE = ("safe_mod", "runtime_mod", "dev_mod")
MYIMPORTER_CURRENT_MODE = [MYIMPORTER_MODE[0]]
MYIMPORTER_DEBUG_ENVAR_NAME = "MYIMPORTER_DEBUG"
MYIMPORTER_TRACE_ENVAR_NAME = "MYIMPORTER_TRACE"
MYIMPORTER_ENABLE_ENVAR_NAME = "ENABLE_MYIMPORTER"
MYIMPORTER_ENVAR_PROVIDER_ENVAR_NAME = "MY_MODULE_PATHS"
SITECUSTOMIZE_DEBUG_ENVAR_NAME = "SITECUSTOMIZE_DEBUG"

FINDER_CUSTOMFINDER_FIND_SPEC_EXCLUDED_MODULES = (
    "sys", "os", "importlib", "runpy",
    "pkgutil", "inspect", "site", "builtins",
    "pip", "setuptools", "pkg_resources", "email", "http", "urllib", "json", "logging",
)

MYIMPORTER_ROOT_DIRECTORY = os.getenv("MYIMPORTER_ROOT_DIRECTORY", str(PROJECT_ROOT))
PLUGINMANAGER_DEFAULT_PLUGIN_PATHS = _path_list_setting(
    "MYIMPORTER_PLUGIN_PATHS",
    str(PROJECT_ROOT / "plugins"),
)
PLUGINREGISTRY_PLUGIN_STATE = {
    "discovered": "discovered",
    "loaded": "loaded",
    "active": "active",
    "failed": "failed",
}

PLUGIN_EXECUTION_MODES = ("inprocess", "subprocess")
PLUGIN_DEFAULT_EXECUTION_MODE = _choice_setting(
    "MYIMPORTER_DEFAULT_EXECUTION_MODE",
    "subprocess",
    PLUGIN_EXECUTION_MODES,
)
PLUGIN_RPC_HOST = os.getenv("MYIMPORTER_PLUGIN_RPC_HOST", "127.0.0.1")
PLUGIN_RPC_TIMEOUT = _float_setting("MYIMPORTER_PLUGIN_RPC_TIMEOUT", "5.0")
PLUGIN_WORKER_PYTHON = os.getenv("MYIMPORTER_WORKER_PYTHON", sys.executable)

COLOREDLOGS_LEVEL_STYLES_CUSTOMIZED_COLOR_SETS = {
    "debug": {"color": "blue"},
    "info": {"color": "green"},
    "warning": {"color": "yellow"},
    "error": {"color": "red"},
}

WEB_UI_ROUTE_RULES = {
    "templates": "/",
    "list": "/api/plugins",
    "reload": "/api/plugins/reload/<name>",
    "install": "/api/plugins/install",
    "activate": "/api/plugins/activate/<name>",
    "deactivate": "/api/plugins/deactivate/<name>",
}
