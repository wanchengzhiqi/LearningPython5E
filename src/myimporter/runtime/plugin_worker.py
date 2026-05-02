#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/21

import sys
import importlib
import socket
import traceback

from src.myimporter.runtime.rpc import send_json, recv_json
from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.utils.settings import MYIMPORTER_MODE, MYIMPORTER_CURRENT_MODE, MYIMPORTER_DEBUG_ENVAR_NAME

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)

if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
    import src.myimporter
    src.myimporter.install(mod=MYIMPORTER_MODE[1])
    logger.warning(f"[PluginWorker] is switching myimporter to {MYIMPORTER_MODE[1]}.")


class PluginWorker:
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None
        self.instance = None

    def load(self):
        self.module = importlib.import_module(self.module_name)
        plugin_cls = getattr(self.module, 'Plugin', None)
        if plugin_cls is None:
            logger.error(f"No 'Plugin' class found in module {self.module_name}")
            raise RuntimeError(f"No 'Plugin' class found in module {self.module_name}")
        self.instance = plugin_cls()

    def reload(self):
        if self.module is None:
            self.load()
            return f"Module {self.module_name} was not loaded before, it has been loaded now.Try reloading it again if you want."
        self.module = importlib.reload(self.module)
        plugin_cls = getattr(self.module, 'Plugin', None)
        if plugin_cls is None:
            logger.error(f"No 'Plugin' class found in module {self.module_name} after reload")
            raise RuntimeError(f"No 'Plugin' class found in module {self.module_name}")
        self.instance = plugin_cls()

    def activate(self):
        if self.instance is None:
            logger.error(f"Plugin instance is not loaded for module {self.module_name}")
            raise RuntimeError("Plugin instance is not loaded.")
        if hasattr(self.instance, 'activate'):
            try:
                self.instance.activate()
            except Exception as e:
                return str(e)
        else:
            logger.error(f"Plugin instance does not have an 'activate' method for module {self.module_name}")
            raise ValueError(f"Plugin instance does not have an 'activate' method.")

    def deactivate(self):
        if self.instance is None:
            logger.error(f"Plugin instance is not loaded for module {self.module_name}")
            raise RuntimeError("Plugin instance is not loaded.")
        if hasattr(self.instance, 'deactivate'):
            try:
                self.instance.deactivate()
            except Exception as e:
                return str(e)
        else:
            logger.error(f"Plugin instance does not have a 'deactivate' method for module {self.module_name}")
            raise ValueError(f"Plugin instance does not have a 'deactivate' method.")

    def status(self):
        return {
            'module_name': self.module_name,
            'instance_class': self.instance.__class__.__name__ if self.instance else None
        }


def main():
    if len(sys.argv) < 4:
        print("Usage: python plugin_worker.py host port <module_name>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    module_name = sys.argv[3]

    worker = PluginWorker(module_name)
    worker.load()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    send_json(sock, {'status': 'ready', 'module_name': module_name})

    while True:
        req = recv_json(sock)
        cmd = req.get('cmd')

        try:
            if cmd == 'activate':
                result = worker.activate()
                if result:
                    send_json(sock, {'status': 'error', 'message': result})
                else:
                    send_json(sock, {'status': 'ok', 'message': 'activated'})
            elif cmd == 'deactivate':
                result = worker.deactivate()
                if result:
                    send_json(sock, {'status': 'error', 'message': result})
                else:
                    send_json(sock, {'status': 'ok', 'message': 'deactivated'})
            elif cmd == 'reload':
                result = worker.reload()
                if result:
                    send_json(sock, {'status': 'error', 'message': result})
                else:
                    send_json(sock, {'status': 'ok', 'message': 'reloaded'})
            elif cmd == 'status':
                status = worker.status()
                send_json(sock, {'status': 'ok', 'data': status})
            elif cmd == 'shutdown':
                send_json(sock, {'status': 'ok', 'message': 'shutdown'})
                break
            else:
                send_json(sock, {'status': 'error', 'message': f'Unknown command: {cmd}'})
        except Exception as e:
            error_msg = traceback.format_exc()
            send_json(sock, {'status': 'fatal error', 'message': str(e), 'traceback': error_msg})

    sock.close()


if __name__ == '__main__':
    main()
