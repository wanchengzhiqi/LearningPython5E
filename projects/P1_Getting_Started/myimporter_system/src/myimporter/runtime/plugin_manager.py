#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import json
import os
import socket
import subprocess
import sys
import time

from myimporter.runtime.dependency import DependencyResolver
from myimporter.runtime.registry import PluginRegistry, PluginState
from myimporter.runtime.rpc import recv_json, send_json
from myimporter.utils.settings import (
    MYIMPORTER_CURRENT_MODE,
    MYIMPORTER_DEBUG_ENVAR_NAME,
    MYIMPORTER_MODE,
    MYIMPORTER_TRACE_ENVAR_NAME,
    PLUGIN_DEFAULT_EXECUTION_MODE,
    PLUGIN_EXECUTION_MODES,
    PLUGIN_RPC_HOST,
    PLUGIN_RPC_TIMEOUT,
    PLUGIN_WORKER_PYTHON,
)
from myimporter.utils.setup_loggers import setup_logging
from myimporter.utils.trace import trace

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)
trace_env_name = MYIMPORTER_TRACE_ENVAR_NAME


class PluginManager:
    def __init__(self, plugin_paths):
        self.plugin_paths = list(plugin_paths)
        self.registry = PluginRegistry()

    @staticmethod
    def _validate_manifest(directory_name, meta):
        if not isinstance(meta, dict):
            raise ValueError("Plugin manifest must contain a JSON object.")

        manifest_name = meta.get("name", directory_name)
        if manifest_name != directory_name:
            raise ValueError(
                f"Manifest name {manifest_name!r} does not match directory {directory_name!r}."
            )

        entry = meta.get("entry")
        if not isinstance(entry, str) or not entry:
            raise ValueError("Plugin manifest requires a non-empty string entry.")
        if not all(part.isidentifier() for part in entry.split(".")):
            raise ValueError(f"Invalid plugin entry: {entry!r}.")

        depends = meta.get("depends", [])
        if not isinstance(depends, list) or not all(isinstance(item, str) for item in depends):
            raise ValueError("Plugin manifest depends must be a list of plugin names.")

        permissions = meta.get("permissions", {})
        if not isinstance(permissions, dict):
            raise ValueError("Plugin manifest permissions must be a JSON object.")

        execution_mode = meta.get("execution_mode", PLUGIN_DEFAULT_EXECUTION_MODE)
        if execution_mode not in PLUGIN_EXECUTION_MODES:
            allowed = ", ".join(PLUGIN_EXECUTION_MODES)
            raise ValueError(f"Plugin execution_mode must be one of: {allowed}.")

    def discover(self):
        for base in self.plugin_paths:
            trace(f"scanning for plugins in: {base}", trace_env_name)
            if not os.path.isdir(base):
                logger.warning(f"[PluginManager] Plugin path does not exist: {base}")
                continue

            for name in sorted(os.listdir(base)):
                plugin_dir = os.path.join(base, name)
                if not os.path.isdir(plugin_dir):
                    continue

                manifest_path = os.path.join(plugin_dir, "manifest.json")
                if not os.path.isfile(manifest_path):
                    continue

                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    self._validate_manifest(name, meta)
                except (OSError, json.JSONDecodeError, ValueError) as exc:
                    logger.error(f"[PluginManager] Invalid manifest {manifest_path}: {exc}")
                    continue

                if self.registry.register(name, meta, plugin_dir):
                    logger.info(f"[PluginManager] discovered plugin: {name}")
                else:
                    logger.debug(f"[PluginManager] plugin already registered: {name}")

    @staticmethod
    def _worker_python():
        return PLUGIN_WORKER_PYTHON

    @staticmethod
    def _terminate_process(proc, wait_first=False):
        if proc is None or proc.poll() is not None:
            return
        if wait_first:
            try:
                proc.wait(timeout=PLUGIN_RPC_TIMEOUT)
                return
            except subprocess.TimeoutExpired:
                pass
        proc.terminate()
        try:
            proc.wait(timeout=PLUGIN_RPC_TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=PLUGIN_RPC_TIMEOUT)

    def load_all(self):
        order = DependencyResolver(self.registry).resolve()
        logger.info(f"[PluginManager] loading plugins in order: {order}")
        for name in order:
            if not self.registry.has_instance(name):
                self._load(name)

    def _load(self, name):
        plugin_info = self.registry.get(name)
        if not plugin_info:
            raise ValueError(f"Plugin {name} not found.")

        execution_mode = plugin_info["meta"].get(
            "execution_mode",
            PLUGIN_DEFAULT_EXECUTION_MODE,
        )
        if execution_mode == "subprocess":
            self._load_subprocess(name)
        else:
            self._load_inprocess(name)

    def _load_inprocess(self, name):
        start = time.time()
        try:
            plugin_info = self.registry.get(name)
            entry = plugin_info["meta"]["entry"]
            module_name = f"{name}.{entry}"
            trace(f"loading in-process: {module_name}", trace_env_name)

            module = importlib.import_module(module_name)
            plugin_class = getattr(module, "Plugin", None)
            if plugin_class is None:
                raise RuntimeError(f"No Plugin class found in module {module_name}.")

            self.registry.set_instance(name, instance=plugin_class())
            self.registry._plugins[name]["metrics"]["load_time"] = time.time() - start
            logger.info(f"[PluginManager] loaded plugin in-process: {name}")
        except Exception as exc:
            self.registry.set_error(name, "loading_errors", str(exc))
            self.registry.fail(name)
            logger.error(f"[PluginManager] failed to load plugin in-process: {exc}")
            raise

    def _load_subprocess(self, name):
        start = time.time()
        plugin_info = self.registry.get(name)
        module_name = f"{name}.{plugin_info['meta']['entry']}"
        worker_path = os.path.join(os.path.dirname(__file__), "plugin_worker.py")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.settimeout(PLUGIN_RPC_TIMEOUT)
        conn = None
        proc = None
        try:
            server.bind((PLUGIN_RPC_HOST, 0))
            server.listen(1)
            host, port = server.getsockname()

            trace(f"starting plugin worker subprocess for: {module_name}", trace_env_name)
            proc = subprocess.Popen(
                [self._worker_python(), worker_path, host, str(port), module_name]
            )

            conn, _ = server.accept()
            conn.settimeout(PLUGIN_RPC_TIMEOUT)
            ready = recv_json(conn)
            if ready.get("status") != "ready":
                raise RuntimeError(f"Plugin worker failed to start: {ready}")

            runtime_info = {
                "instance_id": None,
                "instance_object": None,
                "execution_mode": "subprocess",
                "process_pid": proc.pid,
                "rpc_host": host,
                "rpc_port": port,
                "rpc_conn": conn,
                "rpc_process": proc,
            }
            self.registry.set_instance(name, runtime_info=runtime_info)
            self.registry._plugins[name]["metrics"]["load_time"] = time.time() - start
            logger.info(f"[PluginManager] loaded plugin in subprocess: {name}")
        except Exception as exc:
            if conn is not None:
                conn.close()
            self._terminate_process(proc)
            self.registry.set_error(name, "loading_errors", str(exc))
            self.registry.fail(name)
            logger.error(f"[PluginManager] failed to load plugin in subprocess: {exc}")
            raise
        finally:
            server.close()

    def _rpc_call(self, name, cmd):
        plugin_info = self.registry.get(name)
        runtime_info = plugin_info.get("instance") if plugin_info else None
        if not runtime_info or runtime_info.get("execution_mode") != "subprocess":
            raise RuntimeError(f"Plugin {name} is not running in subprocess mode.")

        conn = runtime_info.get("rpc_conn")
        if conn is None:
            raise RuntimeError(f"No RPC connection found for plugin {name}.")

        send_json(conn, {"cmd": cmd})
        return recv_json(conn)

    def can_activate(self, name):
        return (
            self.registry.get_state(name) == PluginState.LOADED
            and self.registry.has_instance(name)
        )

    def can_deactivate(self, name):
        return (
            self.registry.get_state(name) == PluginState.ACTIVE
            and self.registry.has_instance(name)
        )

    def activate_all(self):
        for name in list(self.registry.all()):
            if not self.can_activate(name):
                continue
            try:
                self.activate_plugin(name)
            except Exception as exc:
                logger.error(f"[PluginManager] failed to activate plugin {name}: {exc}")

    def activate_plugin(self, name):
        if not self.can_activate(name):
            state = self.registry.get_state(name)
            raise RuntimeError(f"Plugin {name} cannot be activated from state {state!r}.")

        start = time.time()
        instance_info = self.registry.get(name)["instance"]
        if instance_info["execution_mode"] == "subprocess":
            response = self._rpc_call(name, "activate")
            if response.get("status") != "ok":
                self.registry.set_error(name, "activating_errors", response.get("message"))
                self.registry.fail(name)
                raise RuntimeError(response.get("message"))
        else:
            instance = self.registry.get_instance_object(name)
            if not hasattr(instance, "activate"):
                raise RuntimeError(f"Plugin {name} has no activate method.")
            try:
                instance.activate()
            except Exception as exc:
                self.registry.set_error(name, "activating_errors", str(exc))
                self.registry.fail(name)
                raise

        self.registry.activate(name)
        self.registry._plugins[name]["metrics"]["activate_time"] = time.time() - start
        self.registry.clear_error(name)
        logger.info(f"[PluginManager] activated plugin: {name}")

    def deactivate_plugin(self, name):
        if not self.can_deactivate(name):
            state = self.registry.get_state(name)
            raise RuntimeError(f"Plugin {name} cannot be deactivated from state {state!r}.")

        instance_info = self.registry.get(name)["instance"]
        if instance_info["execution_mode"] == "subprocess":
            response = self._rpc_call(name, "deactivate")
            if response.get("status") != "ok":
                self.registry.set_error(name, "deactivating_errors", response.get("message"))
                self.registry.fail(name)
                raise RuntimeError(response.get("message"))
        else:
            instance = self.registry.get_instance_object(name)
            if not hasattr(instance, "deactivate"):
                raise RuntimeError(f"Plugin {name} has no deactivate method.")
            try:
                instance.deactivate()
            except Exception as exc:
                self.registry.set_error(name, "deactivating_errors", str(exc))
                self.registry.fail(name)
                raise

        self.registry.deactivate(name)
        logger.info(f"[PluginManager] deactivated plugin: {name}")

    def reload_plugin(self, name):
        plugin_info = self.registry.get(name)
        if not plugin_info:
            raise ValueError(f"Plugin {name} not found.")

        if not self.registry.has_instance(name):
            self._load(name)
            return

        was_active = self.registry.get_state(name) == PluginState.ACTIVE
        if was_active:
            self.deactivate_plugin(name)

        instance_info = self.registry.get(name)["instance"]
        if instance_info["execution_mode"] == "subprocess":
            response = self._rpc_call(name, "reload")
            if response.get("status") != "ok":
                self.registry.set_error(name, "loading_errors", response.get("message"))
                self.registry.fail(name)
                raise RuntimeError(response.get("message"))
            self.registry.deactivate(name)
        else:
            module_name = f"{name}.{plugin_info['meta']['entry']}"
            try:
                module = importlib.import_module(module_name)
                module = importlib.reload(module)
                plugin_class = getattr(module, "Plugin", None)
                if plugin_class is None:
                    raise RuntimeError(f"No Plugin class found in module {module_name}.")
                self.registry.set_instance(name, instance=plugin_class())
            except Exception as exc:
                self.registry.set_error(name, "loading_errors", str(exc))
                self.registry.fail(name)
                raise

        if was_active:
            self.activate_plugin(name)
        logger.info(f"[PluginManager] reloaded plugin: {name}")

    def shutdown_plugin(self, name):
        plugin_info = self.registry.get(name)
        if not plugin_info or not self.registry.has_instance(name):
            return

        if self.can_deactivate(name):
            try:
                self.deactivate_plugin(name)
            except Exception as exc:
                logger.warning(f"[PluginManager] deactivate before shutdown failed: {exc}")

        instance_info = plugin_info["instance"]
        if instance_info["execution_mode"] == "subprocess":
            conn = instance_info.get("rpc_conn")
            proc = instance_info.get("rpc_process")
            try:
                response = self._rpc_call(name, "shutdown")
                if response.get("status") != "ok":
                    logger.warning(f"[PluginManager] worker shutdown response: {response}")
            except Exception as exc:
                logger.warning(f"[PluginManager] worker shutdown failed: {exc}")
            finally:
                if conn is not None:
                    conn.close()
                self._terminate_process(proc, wait_first=True)

        self.registry.clear_instance(name)
        logger.info(f"[PluginManager] shutdown plugin: {name}")

    def shutdown_all(self):
        for name in reversed(list(self.registry.all())):
            self.shutdown_plugin(name)

    def install_remote_plugin(self, url):
        if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
            raise RuntimeError(f"Remote install is only allowed in {MYIMPORTER_MODE[1]}.")
        raise RuntimeError(
            "Remote plugin installation is disabled until archive validation, "
            "integrity policy, and authentication are implemented."
        )

    @staticmethod
    def _apply_sandbox(permissions):
        raise NotImplementedError(
            "The sandbox prototype is intentionally disabled: monkeypatching "
            "process-global functions is not a security boundary."
        )
