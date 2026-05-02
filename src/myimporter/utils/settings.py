#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/15

HOST = "127.0.0.1"
PORT = 5000
MYIMPORTER_COLOREDLOGS_FORMAT = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
MYIMPORTER_MODE = ("safe_mod", "runtime_mod", "dev_mod")
MYIMPORTER_CURRENT_MODE = [MYIMPORTER_MODE[0]]  # 默认模式为 safe_mod
MYIMPORTER_DEBUG_ENVAR_NAME = "MYIMPORTER_DEBUG"
MYIMPORTER_TRACE_ENVAR_NAME = "MYIMPORTER_TRACE"
MYIMPORTER_ENABLE_ENVAR_NAME = "ENABLE_MYIMPORTER"
MYIMPORTER_ENVAR_PROVIDER_ENVAR_NAME = "MY_MODULE_PATHS"
SITECUSTOMIZE_DEBUG_ENVAR_NAME = "SITECUSTOMIZE_DEBUG"
FINDER_CUSTOMFINDER_FIND_SPEC_EXCLUDED_MODULES = (
            "sys", "os", "importlib", "runpy",
            "pkgutil", "inspect", "site", "builtins",
            "pip", "setuptools", "pkg_resources", "email", "http", "urllib", "json", "logging"
        )
LP5E_ROOT_DIRECTORY = "D:\\MySoftwareDownload\\PythonPractice\\LearningPython5E"
PLUGINMANAGER_DEFAULT_PLUGIN_PATHS = ["D:\\MySoftwareDownload\\PythonPractice\\LearningPython5E\\src\\plugins"]
PLUGINMANAGER_REMOTE_PLUGIN_EXPECTED_HASH = "expected_sha256_hash_here"
PLUGINREGISTRY_PLUGIN_STATE = {"discovered": "discovered", "loaded": "loaded", "active": "active", "failed": "failed"}
PLUGIN_EXECUTION_MODE = ("inprocess", "subprocess")
PLUGIN_DEFAULT_EXECUTION_MODE = PLUGIN_EXECUTION_MODE[1]  # 默认使用 subprocess 模式执行插件，以增强隔离性和安全性
PLUGIN_RPC_HOST = "127.0.0.1"
PLUGIN_RPC_BASE_PORT = 9000
PLUGIN_RPC_TIMEOUT = 5.0
PLUGIN_WORKER_PYTHON = "python"  # 可以根据需要指定具体的 Python 解释器路径
COLOREDLOGS_LEVEL_STYLES_CUSTOMIZED_COLOR_SETS = {
    "debug": {"color": "blue"},
    "info": {"color": "green"},
    "warning": {"color": "yellow"},
    "error": {"color": "red"}
}
CLI_COMMAND_LINE_ARGUMENTS = ("list", "reload", "--safe", "--runtime", "--dev")
WEB_UI_PORT = 8000
WEB_UI_ROUTE_RULES = {"templates": "/", "list": "/api/plugins", "reload": "/api/plugins/reload/<name>", "install": "/api/plugins/install", "activate": "/api/plugins/activate/<name>", "deactivate": "/api/plugins/deactivate/<name>"}
