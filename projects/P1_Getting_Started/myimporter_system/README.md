# myimporter System

`myimporter_system` 是 `P1_Getting_Started` 大阶段持续演进的综合实践成果。
它不是生产级插件框架，而是一个用于理解 Python 导入机制、插件发现、
依赖排序、运行时服务、进程边界和 socket JSON RPC 的可复盘项目。

## 目录结构

```text
myimporter_system/
  cli.py
  runtime_service.py
  requirements.txt
  plugins/
    plugin_a/
    plugin_b/
  src/
    myimporter/
      core/
      runtime/
      utils/
  web_ui/
    web_ui.py
    templates/
```

- `src/myimporter/`：可导入的核心包。
- `plugins/`：示例插件及其 `manifest.json`。
- `runtime_service.py`：唯一的插件运行时服务。
- `cli.py`：通过 socket 与运行时服务交互的命令行客户端。
- `web_ui/`：通过 RuntimeService 管理插件的 Flask 客户端。
- `requirements.txt`：本项目需要的第三方依赖。

## 环境准备

在仓库根目录运行：

```powershell
.\.venv-py314\Scripts\Activate.ps1
python -m pip install -r projects\P1_Getting_Started\myimporter_system\requirements.txt
```

后续示例默认已经激活 `.venv-py314`。不要把依赖误装入保留作历史回归的旧
Python `3.9.13` 或旧 `.venv`。

## 推荐用法

先启动运行时服务：

```powershell
python projects\P1_Getting_Started\myimporter_system\runtime_service.py
```

在另一个终端中使用 CLI：

```powershell
python projects\P1_Getting_Started\myimporter_system\cli.py list
python projects\P1_Getting_Started\myimporter_system\cli.py status plugin_b
python projects\P1_Getting_Started\myimporter_system\cli.py reload plugin_a
python projects\P1_Getting_Started\myimporter_system\cli.py deactivate plugin_b
python projects\P1_Getting_Started\myimporter_system\cli.py activate plugin_b
python projects\P1_Getting_Started\myimporter_system\cli.py shutdown
```

启动 Web UI：

```powershell
python projects\P1_Getting_Started\myimporter_system\web_ui\web_ui.py
```

默认访问地址为 `http://127.0.0.1:8000`。Web UI 和 CLI 都是
RuntimeService 的客户端；使用前应先启动 RuntimeService。

## 直接使用导入器

```powershell
$env:PYTHONPATH="projects\P1_Getting_Started\myimporter_system\src"
python -c "import myimporter; from myimporter.utils.settings import MYIMPORTER_MODE; myimporter.install(mod=MYIMPORTER_MODE[1]); import plugin_a.plugin; print(plugin_a.plugin.Plugin); myimporter.uninstall()"
```

模式语义：

- `safe_mod`：移除 finder 并清空托管路径。
- `runtime_mod`：使用项目默认路径。
- `dev_mod`：在默认路径上追加 `MY_MODULE_PATHS`。

## 配置覆盖

- `MYIMPORTER_ROOT_DIRECTORY`：自定义导入器根搜索目录。
- `MYIMPORTER_PLUGIN_PATHS`：插件搜索目录列表。
- `MYIMPORTER_RUNTIME_HOST`、`MYIMPORTER_RUNTIME_PORT`：运行时服务地址。
- `MYIMPORTER_WEB_UI_HOST`、`MYIMPORTER_WEB_UI_PORT`：Web UI 地址。
- `MYIMPORTER_PLUGIN_RPC_HOST`、`MYIMPORTER_PLUGIN_RPC_TIMEOUT`：worker RPC 参数。
- `MYIMPORTER_WORKER_PYTHON`：worker 使用的 Python 解释器。
- `MYIMPORTER_DEFAULT_EXECUTION_MODE`：默认插件执行位置。
- `MY_MODULE_PATHS`：`dev_mod` 的附加模块目录。

插件清单中的 `execution_mode` 表示插件位于当前进程还是 worker 子进程；
`permissions.subprocess` 表示插件自身是否有权创建子进程。两者不是同一件事。

## 全局 sitecustomize

`src/myimporter/sitecustomize_template.py` 是可选的全局启动钩子模板。默认
启动 Python 时保持静默。显式启用时，需要让全局解释器知道本项目源码位置：

```powershell
$env:ENABLE_MYIMPORTER="1"
$env:MYIMPORTER_SOURCE_ROOT="D:\path\to\LearningPython5E\projects\P1_Getting_Started\myimporter_system\src"
$env:MY_MODULE_PATHS="D:\path\to\extra\modules"
python
```

当前 Python `3.14.5` 与 `.venv-py314` 不需要安装该全局钩子。项目入口已经
能够显式运行系统；只有未来确实需要全局 opt-in bootstrap 时才单独评估复制。

## 当前限制

- 权限字段仍是元数据，不构成安全边界。
- worker 子进程提高故障隔离程度，但不是安全沙箱。
- RPC 尚未加入认证和加密，只适合本机学习环境。
- RuntimeService 当前串行处理请求。
- 状态和指标只保存在内存中。
- 远程插件安装入口明确禁用，尚未补齐认证、完整性校验、URL 策略、
  ZIP 路径穿越防护和资源上限。
