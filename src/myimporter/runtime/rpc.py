#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/23

import json
import socket


def send_json(sock, payload):
    data = json.dumps(payload).encode('utf-8')
    length = len(data)
    sock.sendall(length.to_bytes(4, byteorder='big') + data)


def recv_json(sock):
    header = sock.recv(4)
    if not header:
        raise ConnectionError("No data received from socket.")
    size = int.from_bytes(header, byteorder='big')
    chunks = []
    remaining = size
    while remaining > 0:
        chunk = sock.recv(min(4096, remaining))
        if not chunk:
            raise ConnectionError("Socket connection closed while receiving data.")
        chunks.append(chunk)
        remaining -= len(chunk)
    return json.loads(b''.join(chunks).decode('utf-8'))
