#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from myimporter.runtime.rpc import recv_json, send_json
from myimporter.utils.settings import HOST, PLUGIN_RPC_TIMEOUT, PORT


def parse_args():
    parser = argparse.ArgumentParser(description="Manage the myimporter runtime service.")
    parser.add_argument(
        "command",
        choices=("list", "reload", "activate", "deactivate", "status", "shutdown"),
    )
    parser.add_argument("name", nargs="?")
    args = parser.parse_args()
    if args.command not in ("list", "shutdown") and not args.name:
        parser.error(f"{args.command} requires a plugin name")
    return args


def request_runtime(payload):
    with socket.create_connection((HOST, PORT), timeout=PLUGIN_RPC_TIMEOUT) as client:
        client.settimeout(PLUGIN_RPC_TIMEOUT)
        send_json(client, payload)
        return recv_json(client)


def main():
    args = parse_args()
    payload = {"command": args.command}
    if args.name:
        payload["name"] = args.name

    try:
        response = request_runtime(payload)
    except OSError as exc:
        raise SystemExit(f"Unable to reach runtime service at {HOST}:{PORT}: {exc}")

    print(json.dumps(response, ensure_ascii=False, indent=2))
    return 0 if response.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
