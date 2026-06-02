#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/15

from myimporter.utils.settings import PLUGINREGISTRY_PLUGIN_STATE


class PluginState:
    DISCOVERED = PLUGINREGISTRY_PLUGIN_STATE.get('discovered')
    LOADED = PLUGINREGISTRY_PLUGIN_STATE.get('loaded')
    ACTIVE = PLUGINREGISTRY_PLUGIN_STATE.get('active')
    FAILED = PLUGINREGISTRY_PLUGIN_STATE.get('failed')


class PluginRegistry:
    def __init__(self):
        self._plugins = {}

    def register(self, name, meta, path):
        if name in self._plugins:
            return False

        self._plugins[name] = {
            'meta': meta,
            'path': path,
            'instance': None,
            'state': PluginState.DISCOVERED,
            'permissions': meta.get('permissions', {}),
            'metrics': {
                'load_time': None,
                'activate_time': None,
                'error': {'activating_errors': [], 'deactivating_errors': [], 'loading_errors': []},
            }
        }
        return True

    def set_instance(self, name, instance=None, runtime_info=None):
        if name not in self._plugins:
            return

        if runtime_info is not None:
            self._plugins[name]['instance'] = runtime_info
        else:
            self._plugins[name]['instance'] = {
                "instance_id": id(instance),
                "instance_object": instance,
                "execution_mode": "inprocess",
                "process_pid": None,
                "rpc_host": None,
                "rpc_port": None
            }
        self._plugins[name]['state'] = PluginState.LOADED

    def activate(self, name):
        if self.has_instance(name):
            self._plugins[name]['state'] = PluginState.ACTIVE

    def deactivate(self, name):
        if self.has_instance(name):
            self._plugins[name]['state'] = PluginState.LOADED

    def fail(self, name):
        if name in self._plugins:
            self._plugins[name]['state'] = PluginState.FAILED

    def clear_instance(self, name):
        if name in self._plugins:
            self._plugins[name]['instance'] = None
            self._plugins[name]['state'] = PluginState.DISCOVERED

    def set_error(self, name, error_type, error_msg):
        if name in self._plugins:
            self._plugins[name]['metrics']['error'][error_type].append(error_msg)

    def clear_error(self, name):
        if name in self._plugins:
            for _ in self._plugins[name]['metrics']['error'].values():
                _.clear()

    def get(self, name):
        return self._plugins.get(name)

    def all(self):
        return self._plugins

    def get_state(self, name):
        plugin = self.get(name)
        if plugin:
            return plugin['state']
        return None

    def has_instance(self, name):
        plugin = self.get(name)
        return bool(plugin and plugin['instance'] is not None)

    def get_instance_object(self, name):
        plugin = self.get(name)
        if not self.has_instance(name):
            return None
        return plugin['instance'].get('instance_object')

    def to_dict(self):
        result = {}
        for name, info in self._plugins.items():
            instance_info = info['instance']

            if instance_info is None:
                instance_repr = None
            elif instance_info.get('execution_mode') == 'subprocess':
                instance_repr = {
                    "execution_mode": instance_info.get('execution_mode'),
                    "process_pid": instance_info.get('process_pid'),
                    "rpc_host": instance_info.get('rpc_host'),
                    "rpc_port": instance_info.get('rpc_port')
                }
            else:
                obj = instance_info['instance_object']
                instance_repr = obj.to_dict() if hasattr(obj, 'to_dict') else obj.__class__.__name__

            result[name] = {
                "meta": info['meta'],
                "path": info['path'],
                "instance": instance_repr,
                "state": info['state'],
                "permissions": info['permissions'],
                "provides": info['meta'].get('provides', []),
                "metrics": info['metrics']
            }
        return result

    def get_dependencies(self, name):
        plugin = self.get(name)
        if plugin:
            return plugin['meta'].get('depends', [])
        return []

    def get_providers(self, capability):
        return [
            name for name, info in self._plugins.items()
            if capability in info['meta'].get('provides', [])
        ]
