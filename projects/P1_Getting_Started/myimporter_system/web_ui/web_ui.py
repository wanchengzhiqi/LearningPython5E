#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from flask import Flask, jsonify, render_template

from myimporter.runtime.rpc import recv_json, send_json
from myimporter.utils.settings import (
    HOST,
    PLUGIN_RPC_TIMEOUT,
    PORT,
    WEB_UI_HOST,
    WEB_UI_PORT,
    WEB_UI_ROUTE_RULES,
)

app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent / "templates"))


def runtime_request(payload):
    with socket.create_connection((HOST, PORT), timeout=PLUGIN_RPC_TIMEOUT) as client:
        client.settimeout(PLUGIN_RPC_TIMEOUT)
        send_json(client, payload)
        return recv_json(client)


def runtime_response(payload):
    try:
        response = runtime_request(payload)
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 502

    status_code = 200 if response.get("status") == "ok" else 400
    return jsonify(response), status_code


@app.route(WEB_UI_ROUTE_RULES["templates"])
def dashboard():
    return render_template("dashboard.html")


@app.route(WEB_UI_ROUTE_RULES["list"], methods=["GET"])
def list_plugins():
    try:
        response = runtime_request({"command": "list"})
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 502

    if response.get("status") != "ok":
        return jsonify(response), 400
    return jsonify(response["data"])


@app.route(WEB_UI_ROUTE_RULES["reload"], methods=["POST"])
def reload_plugin(name):
    return runtime_response({"command": "reload", "name": name})


@app.route(WEB_UI_ROUTE_RULES["activate"], methods=["POST"])
def activate_plugin(name):
    return runtime_response({"command": "activate", "name": name})


@app.route(WEB_UI_ROUTE_RULES["deactivate"], methods=["POST"])
def deactivate_plugin(name):
    return runtime_response({"command": "deactivate", "name": name})


@app.route(WEB_UI_ROUTE_RULES["install"], methods=["POST"])
def install_plugin():
    return (
        jsonify(
            {
                "status": "error",
                "message": "Remote plugin installation is intentionally disabled.",
            }
        ),
        501,
    )


if __name__ == "__main__":
    app.run(host=WEB_UI_HOST, port=WEB_UI_PORT)
