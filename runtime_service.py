#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/16

import socket
import threading

from src.myimporter.runtime.plugin_manager import PluginManager
from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.utils.settings import MYIMPORTER_MODE, MYIMPORTER_CURRENT_MODE, HOST, PORT, PLUGINMANAGER_DEFAULT_PLUGIN_PATHS, CLI_COMMAND_LINE_ARGUMENTS, MYIMPORTER_DEBUG_ENVAR_NAME

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)

if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
    import src.myimporter
    src.myimporter.install(mod=MYIMPORTER_MODE[1])
    logger.warning(f"[RuntimeService] is switching myimporter to {MYIMPORTER_MODE[1]}.")


class RuntimeService:
    def __init__(self):
        self.plm = PluginManager(PLUGINMANAGER_DEFAULT_PLUGIN_PATHS)
        self.plm.discover()
        self.plm.load_all()
        self.plm.activate_all()

    def handle_command(self, cmd):
        parts = cmd.strip().split()
        if parts[0] not in CLI_COMMAND_LINE_ARGUMENTS[:2]:
            return "Invalid command.Use 'list' or 'reload' to be the second argument."

        if parts[1:]:
            for _ in parts[1:]:
                if _ == CLI_COMMAND_LINE_ARGUMENTS[2]:
                    raise RuntimeError("The --safe mode is not allowed in RuntimeService.RuntimeService is interrupted.")
                elif _ == CLI_COMMAND_LINE_ARGUMENTS[4]:
                    import src.myimporter
                    src.myimporter.install(mod=MYIMPORTER_MODE[2])
                    logger.warning(f"[RuntimeService] is switching myimporter to {MYIMPORTER_MODE[2]}.")
                    break

        if parts[0] == 'reload' and len(parts) > 1:
            self.plm.reload_plugin(parts[1])
            return f"Plugin {parts[1]} reloaded."

        elif parts[0] == 'list':
            # return '\n'.join(f"{name}: {info['state']}" for name, info in self.plm.registry.all().items())
            return str(self.plm.registry.all())
        return "Unknown command."

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"Runtime service started on {HOST}:{PORT}")

        while True:
            if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
                src.myimporter.install(mod=MYIMPORTER_MODE[1])
                logger.warning(f"[RuntimeService] is switching myimporter to {MYIMPORTER_MODE[1]}.")

            client, addr = server.accept()
            print(f"Connection from {addr}")

            data = client.recv(1024).decode()
            result = self.handle_command(data)

            client.send(result.encode())
            client.close()


if __name__ == "__main__":
    service = RuntimeService()
    service.start()
