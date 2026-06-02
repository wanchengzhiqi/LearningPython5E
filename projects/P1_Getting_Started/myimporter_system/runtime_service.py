#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import myimporter
from myimporter.runtime.plugin_manager import PluginManager
from myimporter.runtime.rpc import recv_json, send_json
from myimporter.utils.settings import (
    HOST,
    MYIMPORTER_CURRENT_MODE,
    MYIMPORTER_DEBUG_ENVAR_NAME,
    MYIMPORTER_MODE,
    PLUGINMANAGER_DEFAULT_PLUGIN_PATHS,
    PLUGIN_RPC_TIMEOUT,
    PORT,
)
from myimporter.utils.setup_loggers import setup_logging

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)


class RuntimeService:
    def __init__(self):
        if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
            myimporter.install(mod=MYIMPORTER_MODE[1])

        self.plm = PluginManager(PLUGINMANAGER_DEFAULT_PLUGIN_PATHS)
        self._running = True
        try:
            self.plm.discover()
            self.plm.load_all()
            self.plm.activate_all()
        except Exception:
            self.close()
            raise

    @staticmethod
    def _require_name(request):
        name = request.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("A non-empty plugin name is required.")
        return name

    def handle_request(self, request):
        if not isinstance(request, dict):
            raise ValueError("Request must be a JSON object.")

        command = request.get("command")
        if command == "list":
            return {"status": "ok", "data": self.plm.registry.to_dict()}
        if command == "reload":
            name = self._require_name(request)
            self.plm.reload_plugin(name)
            return {"status": "ok", "message": f"Plugin {name} reloaded."}
        if command == "activate":
            name = self._require_name(request)
            self.plm.activate_plugin(name)
            return {"status": "ok", "message": f"Plugin {name} activated."}
        if command == "deactivate":
            name = self._require_name(request)
            self.plm.deactivate_plugin(name)
            return {"status": "ok", "message": f"Plugin {name} deactivated."}
        if command == "status":
            name = self._require_name(request)
            data = self.plm.registry.to_dict().get(name)
            if data is None:
                raise ValueError(f"Plugin {name} not found.")
            return {"status": "ok", "data": data}
        if command == "shutdown":
            self._running = False
            return {"status": "ok", "message": "Runtime service is shutting down."}
        raise ValueError(f"Unknown command: {command!r}.")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(5)
            server.settimeout(0.5)
            print(f"Runtime service started on {HOST}:{PORT}")

            while self._running:
                try:
                    client, addr = server.accept()
                except socket.timeout:
                    continue
                with client:
                    client.settimeout(PLUGIN_RPC_TIMEOUT)
                    logger.debug(f"[RuntimeService] Connection from {addr}")
                    try:
                        request = recv_json(client)
                        response = self.handle_request(request)
                    except Exception as exc:
                        logger.error(f"[RuntimeService] Request failed: {exc}")
                        response = {"status": "error", "message": str(exc)}
                    try:
                        send_json(client, response)
                    except OSError as exc:
                        logger.warning(f"[RuntimeService] Unable to send response: {exc}")

    def close(self):
        self.plm.shutdown_all()
        myimporter.uninstall()


def main():
    service = RuntimeService()
    try:
        service.start()
    except KeyboardInterrupt:
        print("Runtime service stopped.")
    finally:
        service.close()


if __name__ == "__main__":
    main()
