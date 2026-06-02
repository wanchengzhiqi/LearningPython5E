#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/23

import json

MAX_RPC_MESSAGE_BYTES = 1024 * 1024


def recv_exact(sock, size):
    chunks = []
    remaining = size
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("Socket connection closed while receiving data.")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b''.join(chunks)


def send_json(sock, payload):
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    length = len(data)
    if length > MAX_RPC_MESSAGE_BYTES:
        raise ValueError(f"RPC payload exceeds {MAX_RPC_MESSAGE_BYTES} bytes.")
    sock.sendall(length.to_bytes(4, byteorder='big') + data)


def recv_json(sock):
    header = recv_exact(sock, 4)
    size = int.from_bytes(header, byteorder='big')
    if size > MAX_RPC_MESSAGE_BYTES:
        raise ValueError(f"RPC payload exceeds {MAX_RPC_MESSAGE_BYTES} bytes.")
    return json.loads(recv_exact(sock, size).decode('utf-8'))
