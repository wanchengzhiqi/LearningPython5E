#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/16

import sys
import socket

from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.utils.settings import HOST, PORT, MYIMPORTER_DEBUG_ENVAR_NAME, MYIMPORTER_MODE, MYIMPORTER_CURRENT_MODE

logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)

if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
    import src.myimporter
    src.myimporter.install(mod=MYIMPORTER_MODE[1])
    logger.warning(f"[CLI] is switching myimporter to {MYIMPORTER_MODE[1]}.")

cmd = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'list'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send(cmd.encode())

print(client.recv(4096).decode())

client.close()
