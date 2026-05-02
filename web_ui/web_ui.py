#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/4/16

from flask import Flask, request, jsonify, render_template
from src.myimporter.runtime.plugin_manager import PluginManager
from src.myimporter.utils.setup_loggers import setup_logging
from src.myimporter.utils.settings import MYIMPORTER_MODE, MYIMPORTER_CURRENT_MODE, PLUGINMANAGER_DEFAULT_PLUGIN_PATHS, MYIMPORTER_DEBUG_ENVAR_NAME, WEB_UI_PORT, WEB_UI_ROUTE_RULES

app = Flask(__name__)
logger = setup_logging(__name__, MYIMPORTER_DEBUG_ENVAR_NAME)

if MYIMPORTER_CURRENT_MODE[0] != MYIMPORTER_MODE[1]:
    import src.myimporter
    src.myimporter.install(mod=MYIMPORTER_MODE[1])
    logger.warning(f"[WebUI] is switching myimporter to {MYIMPORTER_MODE[1]}.")

plm = PluginManager(PLUGINMANAGER_DEFAULT_PLUGIN_PATHS)
plm.discover()
plm.load_all()
# plm.activate_all()  # 在 Web UI 启动时自动激活所有插件，可以考虑在前置操作完善后取消此操作，改为用户手动激活


@app.route(WEB_UI_ROUTE_RULES.get('templates'))
def dashboard():
    return render_template('dashboard.html')


@app.route(WEB_UI_ROUTE_RULES.get('list'), methods=['GET'])
def list_plugins():
    return jsonify(plm.registry.to_dict())


@app.route(WEB_UI_ROUTE_RULES.get('reload'), methods=['POST'])
def reload_plugin(name):
    try:
        plm.reload_plugin(name)
        return jsonify({"status": "ok", "message": f"Plugin {name} reloaded."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route(WEB_UI_ROUTE_RULES.get('activate'), methods=['POST'])
def activate_plugin(name):
    try:
        plm.activate_plugin(name)
        return jsonify({"status": "ok", "message": f"Plugin {name} activated."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route(WEB_UI_ROUTE_RULES.get('deactivate'), methods=['POST'])
def deactivate_plugin(name):
    try:
        plm.deactivate_plugin(name)
        return jsonify({"status": "ok", "message": f"Plugin {name} deactivated."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route(WEB_UI_ROUTE_RULES.get('install'), methods=['POST'])
def install_plugin():
    try:
        url = request.json.get('url')
        plm.install_remote_plugin(url)
        return jsonify({"status": "ok", "message": f"Plugin installed from {url}."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == '__main__':
    app.run(port=WEB_UI_PORT)
