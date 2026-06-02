#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import socket
import sys
import traceback
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from myimporter.runtime.rpc import recv_json, send_json
from myimporter.utils.settings import (
    MYIMPORTER_CURRENT_MODE,
    MYIMPORTER_DEBUG_ENVAR_NAME,
    MYIMPORTER_MODE,
)
from myimporter.utils.setup_loggers import setup_logging

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)

if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
    import myimporter

    myimporter.install(mod=MYIMPORTER_MODE[1])


class PluginWorker:
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None
        self.instance = None
        self.active = False

    def load(self):
        self.module = importlib.import_module(self.module_name)
        plugin_class = getattr(self.module, "Plugin", None)
        if plugin_class is None:
            raise RuntimeError(f"No Plugin class found in module {self.module_name}.")
        self.instance = plugin_class()
        self.active = False

    def reload(self):
        if self.module is None:
            self.load()
            return

        self.module = importlib.reload(self.module)
        plugin_class = getattr(self.module, "Plugin", None)
        if plugin_class is None:
            raise RuntimeError(f"No Plugin class found in module {self.module_name}.")
        self.instance = plugin_class()
        self.active = False

    def activate(self):
        if self.instance is None:
            raise RuntimeError("Plugin instance is not loaded.")
        if not hasattr(self.instance, "activate"):
            raise RuntimeError("Plugin instance has no activate method.")
        self.instance.activate()
        self.active = True

    def deactivate(self):
        if self.instance is None:
            raise RuntimeError("Plugin instance is not loaded.")
        if not hasattr(self.instance, "deactivate"):
            raise RuntimeError("Plugin instance has no deactivate method.")
        self.instance.deactivate()
        self.active = False

    def status(self):
        return {
            "module_name": self.module_name,
            "instance_class": self.instance.__class__.__name__ if self.instance else None,
            "active": self.active,
        }


def handle_request(worker, request):
    command = request.get("cmd")
    if command == "activate":
        worker.activate()
        return {"status": "ok", "message": "activated"}
    if command == "deactivate":
        worker.deactivate()
        return {"status": "ok", "message": "deactivated"}
    if command == "reload":
        worker.reload()
        return {"status": "ok", "message": "reloaded"}
    if command == "status":
        return {"status": "ok", "data": worker.status()}
    if command == "shutdown":
        return {"status": "ok", "message": "shutdown"}
    return {"status": "error", "message": f"Unknown command: {command}"}


def main():
    if len(sys.argv) < 4:
        print("Usage: python plugin_worker.py host port <module_name>")
        return 1

    host = sys.argv[1]
    port = int(sys.argv[2])
    module_name = sys.argv[3]
    worker = PluginWorker(module_name)
    worker.load()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        send_json(sock, {"status": "ready", "module_name": module_name})

        while True:
            request = {}
            try:
                request = recv_json(sock)
                response = handle_request(worker, request)
            except ConnectionError:
                break
            except Exception as exc:
                response = {
                    "status": "error",
                    "message": str(exc),
                    "traceback": traceback.format_exc(),
                }

            send_json(sock, response)
            if request.get("cmd") == "shutdown":
                break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
