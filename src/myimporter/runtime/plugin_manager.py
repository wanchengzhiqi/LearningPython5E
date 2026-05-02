#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/15

import os
import sys
import importlib
import json
import requests
import zipfile
import hashlib
import time
import subprocess
import socket

from src.myimporter.runtime.registry import PluginRegistry, PluginState
from src.myimporter.runtime.dependency import DependencyResolver
from src.myimporter.runtime.rpc import send_json, recv_json
from src.myimporter.utils.trace import trace
from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.utils.settings import MYIMPORTER_MODE, MYIMPORTER_CURRENT_MODE, PLUGINMANAGER_DEFAULT_PLUGIN_PATHS, MYIMPORTER_DEBUG_ENVAR_NAME, MYIMPORTER_TRACE_ENVAR_NAME, PLUGINMANAGER_REMOTE_PLUGIN_EXPECTED_HASH, PLUGIN_DEFAULT_EXECUTION_MODE, PLUGIN_RPC_HOST, PLUGIN_RPC_BASE_PORT, PLUGIN_WORKER_PYTHON

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)
trace_env_name = MYIMPORTER_TRACE_ENVAR_NAME


def verify_plugin(file_path, expected_hash):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_hash


class PluginManager:
    def __init__(self, plugin_paths):
        self.plugin_paths = plugin_paths
        self.registry = PluginRegistry()

    # 分配RPC端口，根据当前注册表中插件的数量和插件名称的哈希值计算一个唯一的端口号，确保每个插件都有一个独立的RPC端口用于通信，端口号的计算方式是基于一个预定义的基础端口号加上当前注册表中插件数量的偏移量和插件名称哈希值的模运算结果，以避免端口冲突和确保端口号在合理范围内
    def _allocate_port(self, name):
        return PLUGIN_RPC_BASE_PORT + len(self.registry.all()) + hash(name) % 1000

    # 发现插件，扫描指定的插件路径，寻找包含manifest.json文件的目录，解析manifest.json文件中的元信息，并将插件注册到插件注册表中，注册时使用插件名称、元信息和插件目录路径作为参数，如果没有找到manifest.json文件或者解析失败，则记录相应的日志并跳过该插件
    def discover(self):
        for base in self.plugin_paths:
            trace(f"scanning for plugins in: {base}", trace_env_name)
            for name in os.listdir(base):
                plugin_dir = os.path.join(base, name)
                manifest_path = os.path.join(plugin_dir, 'manifest.json')
                # print(f'checking manifest: {manifest_path}')

                if not os.path.isfile(manifest_path):
                    logger.warning(f"[PluginManager] No manifest.json found for plugin {name} in {plugin_dir}, skipping.")
                    continue

                with open(manifest_path, 'r', encoding='utf-8') as f:
                    try:
                        meta = json.load(f)
                    except json.JSONDecodeError as e:
                        logger.error(f"[PluginManager] failed to parse manifest.json for plugin {name} in {plugin_dir}: {e}")
                        continue

                self.registry.register(name, meta, plugin_dir)
                logger.info(f"[PluginManager] discovered plugin: {name}")

    # 加载所有插件，首先使用依赖解析器解析插件之间的依赖关系，确定加载顺序，然后按照解析出的顺序逐个加载插件，如果在加载过程中发生任何异常，则记录错误日志并抛出异常
    def load_all(self):
        resolver = DependencyResolver(self.registry)
        order = resolver.resolve()
        logger.info(f"[PluginManager] loading plugins in order: {order}")

        for name in order:
            trace(f"loading plugin: {name}", trace_env_name)
            self._load(name)

    # 加载单个插件（在当前进程中），根据插件名称从注册表中获取插件信息，构建模块名称并使用importlib导入模块，获取模块中的Plugin类并实例化，然后将实例存储回注册表中，如果在加载过程中发生任何异常，则记录错误日志并抛出异常
    def _load_inprocess(self, name):
        start = time.time()

        try:
            plugin_info = self.registry.get(name)

            # TODO: apply sandbox permissions for in-process plugins if needed, currently we just log the permissions without real sandbox implementation, which can be added in the future based on specific requirements and security considerations
            # permissions = plugin_info.get('permissions', {})
            # self._apply_sandbox(permissions)
            #
            # logger.info(f"[PluginManager] applying sandbox permissions for plugin {name}")

            entry = plugin_info['meta']['entry']
            module_name = f"{name}.{entry}"

            trace(f"loading in-process: {module_name}", trace_env_name)

            module = importlib.import_module(module_name)
            plugin_class = getattr(module, 'Plugin', None)
            instance = plugin_class()
            self.registry.set_instance(name, instance=instance)
            logger.info(f"[PluginManager] loaded plugin in-process: {name}")

            self.registry._plugins[name]['metrics']['load_time'] = time.time() - start
            logger.info(f"[PluginManager] Plugin {name} has been recorded load(in-process) time successfully.")
        except Exception as e:
            logger.error(f"[PluginManager] failed to load plugin in-process: {e}")
            self.registry.set_error(name, 'loading_errors', str(e))
            logger.info(f"[PluginManager] Plugin {name} has been recorded loading(in-process) error successfully.")

    # 加载单个插件（在子进程中），根据插件名称从注册表中获取插件信息，构建模块名称并使用importlib导入模块，获取模块中的Plugin类并实例化，然后将实例存储回注册表中，如果在加载过程中发生任何异常，则记录错误日志并抛出异常
    def _load_subprocess(self, name):
        start = time.time()

        plugin_info = self.registry.get(name)
        entry = plugin_info['meta']['entry']
        module_name = f"{name}.{entry}"

        host = PLUGIN_RPC_HOST
        port = self._allocate_port(name)
        logger.debug(f"[PluginManager] allocated RPC host {host} and port {port} for plugin {name}")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        worker_path = os.path.join(os.path.dirname(__file__), 'plugin_worker.py')

        trace(f"starting plugin worker subprocess for: {module_name} with command: {PLUGIN_WORKER_PYTHON} {worker_path} {host} {port} {module_name}", trace_env_name)
        proc = subprocess.Popen([PLUGIN_WORKER_PYTHON, worker_path, host, str(port), module_name])

        conn, _ = server.accept()
        ready = recv_json(conn)

        if ready.get('status') != 'ready':
            logger.error(f"[PluginManager] Plugin worker for {name} failed to start properly.")
            raise RuntimeError(f"Plugin worker for {name} failed to start properly: {ready}")

        try:
            runtime_info = {
                "instance_id": None,
                "instance_object": None,
                "execution_mode": PLUGIN_DEFAULT_EXECUTION_MODE,
                "process_pid": proc.pid,
                "rpc_host": host,
                "rpc_port": port,
                "rpc_conn": conn,
                "rpc_process": proc
            }

            self.registry.set_instance(name, runtime_info=runtime_info)
            logger.info(f"[PluginManager] loaded plugin in subprocess: {name}")
            self.registry._plugins[name]['metrics']['load_time'] = time.time() - start
            logger.info(f"[PluginManager] Plugin {name} has been recorded load(subprocess) time successfully.")
        except Exception as e:
            logger.error(f"[PluginManager] failed to load plugin in subprocess: {e}")
            self.registry.set_error(name, 'loading_errors', str(e))
            logger.info(f"[PluginManager] Plugin {name} has been recorded loading(subprocess) error successfully.")

    # 加载单个插件，根据插件名称从注册表中获取插件信息，检查插件的权限设置，如果允许在子进程中执行则调用_load_subprocess方法加载插件，否则调用_load_inprocess方法加载插件，如果在加载过程中发生任何异常，则记录错误日志并抛出异常
    def _load(self, name):
        plugin_info = self.registry.get(name)
        if not plugin_info:
            logger.error(f"[PluginManager] Plugin {name} not found.")
            raise ValueError(f"Plugin {name} not found.")

        execution_mode = plugin_info.get('permissions', {}).get('subprocess', True)

        if execution_mode:
            logger.info(f"[PluginManager] loading plugin {name} in subprocess mode due to its permissions.")
            self._load_subprocess(name)
        else:
            logger.info(f"[PluginManager] loading plugin {name} in in-process mode due to its permissions.")
            self._load_inprocess(name)

    # 检查插件是否可以被激活，根据插件名称从注册表中获取插件状态，如果状态是loaded并且实例存在，则返回True，否则返回False
    def can_activate(self, name):
        state = self.registry.get_state(name)
        return state == PluginState.LOADED and self.registry.has_instance(name)

    # 检查插件是否可以被停用，根据插件名称从注册表中获取插件状态，如果状态是active并且实例存在，则返回True，否则返回False
    def can_deactivate(self, name):
        state = self.registry.get_state(name)
        return state == PluginState.ACTIVE and self.registry.has_instance(name)

    # 进行RPC调用，根据插件名称从注册表中获取插件信息，检查插件是否在子进程模式下运行，如果是则使用RPC连接发送命令并等待响应，如果不是则记录错误日志并抛出异常
    def _rpc_call(self, name, cmd):
        plugin_info = self.registry.get(name)
        if not plugin_info:
            logger.error(f"[PluginManager] Plugin {name} not found for RPC call.")
            raise ValueError(f"Plugin {name} not found.")

        runtime_info = plugin_info.get('instance')
        if not runtime_info or runtime_info.get('execution_mode') != 'subprocess':
            logger.error(f"[PluginManager] Plugin {name} is not running in subprocess mode for RPC call.")
            raise RuntimeError(f"Plugin {name} is not running in subprocess mode for RPC call.")

        conn = runtime_info.get('rpc_conn')
        if not conn:
            logger.error(f"[PluginManager] No RPC connection found for plugin {name}.")
            raise RuntimeError(f"No RPC connection found for plugin {name}.")

        send_json(conn, {'cmd': cmd})
        response = recv_json(conn)
        return response

    # 激活所有插件，遍历注册表中的所有插件信息，对于每个插件，如果实例存在并且具有activate方法，则调用该方法激活插件，并将插件状态更新为active，如果没有activate方法，则记录警告日志并跳过激活，如果在激活过程中发生任何异常，则记录错误日志并将插件状态更新为failed
    def activate_all(self):
        for name, info in self.registry.all().items():
            try:
                instance = self.registry.get_instance_object(name)
                # print(f'checking instance for plugin {name}: {instance}')
                if instance and hasattr(instance, 'activate'):
                    start = time.time()
                    trace(f"activating plugin: {name}", trace_env_name)
                    instance.activate()
                    self.registry.activate(name)
                    logger.info(f"[PluginManager] activated plugin: {name}")
                    self.registry._plugins[name]['metrics']['activate_time'] = time.time() - start
                    logger.info(f"[PluginManager] Plugin {name} has been recorded activate time successfully.")
                else:
                    logger.warning(f"[PluginManager] Plugin {name} has no activate method or has not been loaded, activation failed.")
            except Exception as e:
                logger.error(f"[PluginManager] failed to activate plugin {name}: {e}")
                self.registry.set_error(name, 'activating_errors', str(e))
                logger.info(f"[PluginManager] Plugin {name} has been recorded activating error successfully.")
                self.registry.fail(name)
                logger.info(f"[PluginManager] Plugin {name} has marked as failed due to activation error.")

    # 激活单个插件，根据插件名称从注册表中获取插件信息，如果实例存在并且具有activate方法，则调用该方法激活插件，并将插件状态更新为active，如果没有activate方法，则记录警告日志并跳过激活，如果在激活过程中发生任何异常，则记录错误日志并将插件状态更新为failed
    def activate_plugin(self, name):
        plugin_info = self.registry.get(name)
        if not plugin_info:
            logger.error(f"[PluginManager] Plugin {name} not found for activation.")
            raise ValueError(f"Plugin {name} not found.")

        state = self.registry.get_state(name)
        if not self.can_activate(name):
            if state == PluginState.ACTIVE:
                logger.error(f"[PluginManager] Plugin {name} is already active.")
                raise RuntimeError(f"Plugin {name} is already active.")
            if state == PluginState.FAILED:
                logger.error(f"[PluginManager] Plugin {name} is in failed state! Reload it first.")
                raise RuntimeError(f"Plugin {name} is in failed state! Reload it first.")
            if state == PluginState.DISCOVERED:
                logger.error(f"[PluginManager] Plugin {name} is not loaded yet! Load/Reload it first.")
                raise RuntimeError(f"Plugin {name} is not loaded yet! Load/Reload it first.")
            if not self.registry.has_instance(name):
                logger.error(f"[PluginManager] Plugin {name} has no live instance! Load/Reload it first.")
                raise RuntimeError(f"Plugin {name} has no live instance! Load/Reload it first.")

        instance_info = self.registry.get(name).get('instance')
        execution_mode = instance_info.get('execution_mode', PLUGIN_DEFAULT_EXECUTION_MODE)

        start = time.time()
        if execution_mode == 'subprocess':
            trace(f"activating plugin in subprocess: {name}", trace_env_name)
            response = self._rpc_call(name, 'activate')
            if response.get('status') == 'fatal error':
                logger.error(f"[PluginManager] failed to activate plugin {name} in subprocess: {response.get('message')}")
                raise RuntimeError(f"Failed to activate plugin {name} in subprocess: {response.get('message')}")
            elif response.get('status') == 'error':
                logger.error(f"[PluginManager] failed to activate plugin {name} in subprocess: {response.get('message')}")
                self.registry.set_error(name, 'activating_errors', response.get('message'))
                logger.info(f"[PluginManager] Plugin {name} has been recorded activating(subprocess) error successfully.")
                self.registry.fail(name)
                logger.info(f"[PluginManager] Plugin {name} has marked as failed due to activation(subprocess) error.")
                return
        else:
            trace(f"activating plugin in-process: {name}", trace_env_name)
            instance = self.registry.get_instance_object(name)
            if hasattr(instance, 'activate'):
                try:
                    instance.activate()
                except Exception as e:
                    logger.error(f"[PluginManager] failed to activate plugin {name} in-process: {e}")
                    self.registry.set_error(name, 'activating_errors', str(e))
                    logger.info(f"[PluginManager] Plugin {name} has been recorded activating(in-process) error successfully.")
                    self.registry.fail(name)
                    logger.info(f"[PluginManager] Plugin {name} has marked as failed due to activation(in-process) error.")
                    return
            else:
                logger.error(f"[PluginManager] Plugin {name} has no activate method, activation(in-process) failed.")
                raise ValueError(f"Plugin {name} has no activate method, activation(in-process) failed.")
        try:
            self.registry.activate(name)
            logger.info(f"[PluginManager] activated plugin in {execution_mode}: {name}")
            self.registry._plugins[name]['metrics']['activate_time'] = time.time() - start
            logger.info(f"[PluginManager] Plugin {name} has been recorded activate({execution_mode}) time successfully.")
            self.registry.clear_error(name)
            logger.info(f"[PluginManager] Plugin {name} in {execution_mode} has been cleared all error messages successfully.")
        except Exception as e:
            logger.error(f"[PluginManager] failed to activate plugin {name} in {execution_mode}: {e}")
            self.registry.set_error(name, 'activating_errors', str(e))
            logger.info(f"[PluginManager] Plugin {name} has been recorded activating({execution_mode}) error successfully.")
            self.registry.fail(name)
            logger.info(f"[PluginManager] Plugin {name} has marked as failed due to activation({execution_mode}) error.")

    # 停用单个插件，根据插件名称从注册表中获取插件信息，如果实例存在并且具有deactivate方法，则调用该方法停用插件，并将插件状态更新为loaded，如果没有deactivate方法，则记录警告日志并跳过停用，如果在停用过程中发生任何异常，则记录错误日志并将插件状态更新为failed
    def deactivate_plugin(self, name):
        plugin_info = self.registry.get(name)
        if not plugin_info:
            logger.error(f"[PluginManager] Plugin {name} not found for deactivation.")
            raise ValueError(f"Plugin {name} not found.")

        state = self.registry.get_state(name)
        if not self.can_deactivate(name):
            if state == PluginState.DISCOVERED:
                logger.error(f"[PluginManager] Plugin {name} is not loaded yet! Load/Reload it first.")
                raise RuntimeError(f"Plugin {name} is not loaded yet! Load/Reload it first.")
            if state == PluginState.LOADED:
                logger.error(f"[PluginManager] Plugin {name} is not active yet! Activate it first.")
                raise RuntimeError(f"Plugin {name} is not active yet! Activate it first.")
            if state == PluginState.FAILED:
                logger.error(f"[PluginManager] Plugin {name} is in failed state! Reload it first.")
                raise RuntimeError(f"Plugin {name} is in failed state! Reload it first.")
            if state != PluginState.ACTIVE:
                logger.error(f"[PluginManager] Plugin {name} is not active! Current state: {state}.")
                raise RuntimeError(f"Plugin {name} is not active! Current state: {state}.")
            if not self.registry.has_instance(name):
                logger.error(f"[PluginManager] Plugin {name} has no live instance! Load/Reload it first.")
                raise RuntimeError(f"Plugin {name} has no live instance! Load/Reload it first.")

        instance_info = self.registry.get(name).get('instance')
        execution_mode = instance_info.get('execution_mode', PLUGIN_DEFAULT_EXECUTION_MODE)

        if execution_mode == 'subprocess':
            trace(f"deactivating plugin in subprocess: {name}", trace_env_name)
            response = self._rpc_call(name, 'deactivate')
            if response.get('status') == 'fatal error':
                logger.error(f"[PluginManager] failed to deactivate plugin {name} in subprocess: {response.get('message')}")
                raise RuntimeError(f"Failed to deactivate plugin {name} in subprocess: {response.get('message')}")
            elif response.get('status') == 'error':
                logger.error(f"[PluginManager] failed to deactivate plugin {name} in subprocess: {response.get('message')}")
                self.registry.set_error(name, 'deactivating_errors', response.get('message'))
                logger.info(f"[PluginManager] Plugin {name} has been recorded deactivating(subprocess) error successfully.")
                self.registry.fail(name)
                logger.info(f"[PluginManager] Plugin {name} has marked as failed due to deactivation(subprocess) error.")
                return
        else:
            trace(f"deactivating plugin in-process: {name}", trace_env_name)
            instance = self.registry.get_instance_object(name)
            if hasattr(instance, 'deactivate'):
                try:
                    instance.deactivate()
                except Exception as e:
                    logger.error(f"[PluginManager] failed to deactivate plugin {name} in-process: {e}")
                    self.registry.set_error(name, 'deactivating_errors', str(e))
                    logger.info(f"[PluginManager] Plugin {name} has been recorded deactivating(in-process) error successfully.")
                    self.registry.fail(name)
                    logger.info(f"[PluginManager] Plugin {name} has marked as failed due to deactivation(in-process) error.")
                    return
            else:
                logger.error(f"[PluginManager] Plugin {name} has no deactivate method, deactivation(in-process) failed.")
                raise ValueError(f"Plugin {name} has no deactivate method, deactivation(in-process) failed.")
        try:
            self.registry.deactivate(name)
            logger.info(f"[PluginManager] deactivated plugin in {execution_mode}: {name}")
        except Exception as e:
            logger.error(f"[PluginManager] failed to deactivate plugin {name} in {execution_mode}: {e}")
            self.registry.set_error(name, 'deactivating_errors', str(e))
            logger.info(f"[PluginManager] Plugin {name} has been recorded deactivating({execution_mode}) error successfully.")
            self.registry.fail(name)
            logger.info(f"[PluginManager] Plugin {name} has marked as failed due to deactivation({execution_mode}) error.")

    # 重新加载插件，根据插件名称从注册表中获取插件信息，构建模块名称并使用importlib重新加载模块，获取模块中的Plugin类并实例化，然后将实例存储回注册表中，如果在重新加载过程中发生任何异常，则记录错误日志并抛出异常
    def reload_plugin(self, name):
        # if name not in self.registry.all():
        #     logger.error(f"[PluginManager] Plugin {name} not found for reload.")
        #     raise ValueError(f"Plugin {name} not found.")

        plugin_info = self.registry.get(name)
        if not plugin_info:
            logger.error(f"[PluginManager] Plugin {name} not found for reload.")
            raise ValueError(f"Plugin {name} not found.")

        module_name = f"{name}.{plugin_info['meta']['entry']}"
        instance_info = self.registry.get(name).get('instance')
        execution_mode = instance_info.get('execution_mode', PLUGIN_DEFAULT_EXECUTION_MODE)
        was_active = (self.registry.get_state(name) == PluginState.ACTIVE)

        # 在重新加载之前先停用插件，如果插件当前处于active状态并且具有deactivate方法，则调用该方法停用插件，以确保在重新加载过程中不会有旧的实例在运行，避免潜在的资源冲突和不一致问题
        if self.can_deactivate(name):
            trace(f"deactivating the active plugin before reload: {name}", trace_env_name)
            self.deactivate_plugin(name)

        if execution_mode == 'subprocess':
            trace(f"reloading plugin in subprocess: {name}", trace_env_name)
            response = self._rpc_call(name, 'reload')
            if response.get('status') == 'fatal error':
                logger.error(f"[PluginManager] failed to reload plugin {name} in subprocess: {response.get('message')}")
                raise RuntimeError(f"Failed to reload plugin {name} in subprocess: {response.get('message')}")
            elif response.get('status') == 'error':
                logger.error(f"[PluginManager] failed to reload plugin {name} in subprocess: {response.get('message')}")
                self.registry.set_error(name, 'loading_errors', response.get('message'))
                logger.info(f"[PluginManager] Plugin {name} has been recorded loading(subprocess) error successfully.")
                self.registry.fail(name)
                logger.info(f"[PluginManager] Plugin {name} has marked as failed due to loading(subprocess) error.")
                return
            self.registry.deactivate(name)  # 重新加载后状态会自动变为loaded，这里确保状态正确
        else:
            try:
                trace(f"reloading plugin in-process: {module_name}", trace_env_name)
                module = importlib.import_module(module_name) if module_name not in sys.modules else sys.modules[module_name]
                importlib.reload(module)

                plugin_class = getattr(module, 'Plugin', None)
                instance = plugin_class()
                self.registry.set_instance(name, instance=instance)  # 更新实例后状态会自动变为loaded
            except Exception as e:
                logger.error(f"[PluginManager] failed to reload plugin {name} in-process: {e}")
                self.registry.set_error(name, 'loading_errors', str(e))
                logger.info(f"[PluginManager] Plugin {name} has been recorded (re)loading(in-process) error successfully.")
                return
        logger.info(f"[PluginManager] reloaded plugin in {execution_mode}: {name}")

        # 重新加载后如果之前是active状态，则尝试重新激活插件，如果在激活过程中发生任何异常，则记录错误日志并将插件状态更新为failed
        if was_active:
            trace(f"reactivating the plugin was active after reload: {name}", trace_env_name)
            self.activate_plugin(name)

    # 安装远程插件，接受一个URL参数，下载该URL指向的ZIP文件到本地临时目录，然后解压缩到插件目录中，最后调用discover方法重新扫描插件目录以发现新安装的插件，如果在下载、解压或扫描过程中发生任何异常，则记录错误日志并抛出异常
    def install_remote_plugin(self, url):
        # 远程安装功能只能在特定的模式下使用，如果当前模式不允许远程安装，则记录错误日志并抛出异常
        if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
            logger.error(f"[PluginManager] can only install remote plugins in {MYIMPORTER_MODE[1]}")
            raise RuntimeError(f"Remote install is only allowed in {MYIMPORTER_MODE[1]}.")

        trace(f"installing remote plugin from: {url}", trace_env_name)

        file_name = url.split('/')[-1]
        download_path = os.path.join('temp', file_name)
        os.makedirs('temp', exist_ok=True)

        # 下载ZIP文件
        logger.debug(f"[PluginManager] downloading plugin from {url} to {download_path}")
        try:
            r = requests.get(url)
            with open(download_path, 'wb') as f:
                f.write(r.content)
        except Exception as e:
            logger.error(f"[PluginManager] failed to download plugin from {url}: {e}")
            raise

        # 验证下载的文件完整性（这里需要预先知道文件的SHA256哈希值）
        if not verify_plugin(download_path, expected_hash=PLUGINMANAGER_REMOTE_PLUGIN_EXPECTED_HASH):
            logger.error(f"[PluginManager] Downloaded plugin from {url} failed integrity check.")
            raise ValueError("Downloaded plugin failed integrity check.")

        # 解压缩到插件目录
        logger.debug(f"[PluginManager] extracting plugin from {download_path} to {PLUGINMANAGER_DEFAULT_PLUGIN_PATHS[0]}")
        try:
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(*PLUGINMANAGER_DEFAULT_PLUGIN_PATHS)
        except Exception as e:
            logger.error(f"[PluginManager] failed to extract plugin from {download_path}: {e}")
            raise

        logger.info(f"[PluginManager] installed remote plugin from: {url}")

        # 重新扫描插件目录以发现新安装的插件
        self.discover()

    # 应用沙箱权限，根据插件的权限设置，动态修改Python的内置函数和标准库函数，以限制插件对文件系统、网络、子进程等资源的访问，如果插件没有相应的权限，则在访问这些资源时抛出PermissionError异常
    def _apply_sandbox(self, permissions):
        import builtins

        if not permissions.get('filesystem', True):
            logger.error(f"[PluginManager] The current processing plugin is denied access to filesystem. Any attempt to access filesystem will raise PermissionError.")
            builtins.open = lambda *args, **kwargs: (_ for _ in ()).throw(PermissionError("Filesystem access is denied."))

        if not permissions.get('subprocess', False):
            import subprocess
            logger.error(f"[PluginManager] The current processing plugin is denied access to subprocess. Any attempt to access subprocess will raise PermissionError.")
            subprocess.Popen = lambda *args, **kwargs: (_ for _ in ()).throw(PermissionError("Subprocess access is denied."))
