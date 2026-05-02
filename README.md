# LearningPython5E

本项目是一个围绕 Python 基础学习过程持续演进的个人学习与实践仓库。主要参考书目是《Learning Python 5th Edition》。仓库内容不只是一组完成后的程序，而是把学习旅程具象化后的长期记录：包括学习笔记、章节练习脚本、手工测试模块、阶段性实践成果，以及未来可能逐步完善的自动化测试和更多实践项目。

当前最主要的阶段性实践成果是 `myimporter`，它围绕 Python 导入机制、插件发现、插件运行时和进程隔离展开。

## 目录概览

- `notes/`：中文学习笔记，按书籍部分和章节组织，包含截图资源。
- `practice/`：学习过程中的章节练习脚本、实验脚本和数据文件。
- `src/myimporter/`：自定义导入器与插件运行时系统。
- `src/plugins/`：`myimporter` 使用的示例插件和测试模块。
- `tests/`：目前更偏手工实验脚本，不应默认视为成熟自动化测试套件。
- `web_ui/`：基于 Flask 的插件管理 Web UI。
- `cli.py`：通过 socket 与运行时服务交互的命令行入口。
- `runtime_service.py`：插件运行时 TCP 服务入口。

## 当前核心实践：myimporter

`myimporter` 当前包含两条核心能力线：

1. 自定义导入机制
   - 通过 `src.myimporter.install()` / `uninstall()` 安装或移除自定义 finder。
   - 使用 `sys.meta_path`、`MetaPathFinder`、`SourceLoader` 和 provider 机制探索 Python 模块查找与加载过程。
   - 支持默认路径和环境变量路径参与模块查找。

2. 插件运行时
   - 从 `src/plugins/` 发现包含 `manifest.json` 的插件。
   - 根据插件依赖关系进行加载排序。
   - 支持插件加载、激活、停用、重载和状态记录。
   - 支持子进程运行插件，并通过 socket JSON RPC 与插件 worker 通信。
   - 提供 Flask Web UI 查看和管理插件状态。

## 环境准备

当前项目曾在 Python `3.9.13` 环境下运行。建议先创建或启用虚拟环境，再安装依赖：

```powershell
python -m pip install -r requirements.txt
```

当前 `requirements.txt` 只记录运行时代码实际使用到的第三方依赖，不包含尚未稳定化的测试工具依赖。

## 常见运行入口

启动插件运行时服务：

```powershell
python runtime_service.py
```

通过 CLI 与运行时服务交互：

```powershell
python cli.py list
python cli.py reload plugin_a
```

启动 Web UI：

```powershell
python web_ui\web_ui.py
```

Web UI 默认监听 `127.0.0.1:8000`。

## 插件约定

新增插件通常应放在 `src/plugins/<plugin_name>/` 下，并包含：

- `manifest.json`
- 入口模块，例如 `plugin.py`
- 入口模块中的 `Plugin` 类
- 可选的 `activate()`、`deactivate()`、`to_dict()` 方法

现有示例插件：

- `plugin_a`：以进程内模式运行，提供示例能力。
- `plugin_b`：依赖 `plugin_a`，以子进程模式运行。

## 测试说明

当前 `tests/` 目录中的内容更像学习和手工验证脚本，不是稳定的自动化测试套件。

已知情况：

- 当前未把 `pytest` 写入 `requirements.txt`。
- `tests/test_for_myimporter.py` 会调用 `src.myimporter.install()`，并尝试导入外部路径中的模块，不能默认作为普通 pytest 测试运行。
- 后续如果测试逐步自动化，应再补充测试依赖和统一运行方式。

## 注意事项

- `src/myimporter/utils/settings.py` 中包含当前本机项目路径、端口、模式语义和环境变量名等全局配置，改动前应谨慎评估影响。
- 当前 Python 环境可能存在全局 `sitecustomize.py`，启动 Python 时出现相关日志不一定来自项目内部测试。
- Windows 命令提示符或 PowerShell 中的中文乱码通常是终端默认编码不是 UTF-8 导致的显示问题，不应据此判断源文件内容损坏。
- 本项目仍处于学习推进中的“进行时”，不要把现有结构误读为最终形态。
