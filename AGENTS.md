# AGENTS.md

## Project Context

本项目是用户 Python 基础学习旅程的长期具象化项目，而不是一个已经完成定型的单一应用。项目主要参考《Learning Python 5th Edition》，会持续积累学习笔记、章节练习脚本、手工测试模块、阶段性实践成果，以及后续可能出现的自动化测试和更复杂的实践项目。

当前项目中，`myimporter` 是一个重要的阶段性实践成果，但不代表项目边界的全部。随着学习推进，项目结构、实验内容和实践成果都会继续扩展，旧的实践项目也可能继续完善。

## Repository Structure

- `notes/`：中文学习笔记，按书籍部分和章节组织，包含截图资源。
- `practice/`：学习过程中的章节练习脚本、实验脚本和数据文件。
- `src/myimporter/`：当前主要实践成果，自定义导入器与插件运行时系统。
- `src/plugins/`：`myimporter` 的示例插件和测试模块。
- `tests/`：目前更偏手工实验脚本，不应默认视为成熟自动化测试套件。
- `web_ui/`：基于 Flask 的插件管理 Web UI。
- `cli.py`：通过 socket 与运行时服务交互的命令行入口。
- `runtime_service.py`：插件运行时 TCP 服务入口。
- `README.md`：面向人类读者的项目介绍、运行入口和注意事项。
- `requirements.txt`：当前运行时代码实际使用的第三方依赖。

## Current Core Implementation

`myimporter` 当前包含两条核心能力线：

1. 自定义导入机制：
   - `src/myimporter/install.py` 提供 `install()` / `uninstall()`。
   - `src/myimporter/core/finder.py` 实现自定义 `MetaPathFinder`。
   - `src/myimporter/core/loader.py` 实现自定义 `SourceLoader`。
   - `src/myimporter/core/providers.py` 提供文件系统和环境变量路径查找。
   - `src/myimporter/core/path_manager.py` 负责路径规范化和管理。

2. 插件运行时：
   - `src/myimporter/runtime/plugin_manager.py` 负责插件发现、加载、激活、停用、重载、远程安装和子进程运行。
   - `src/myimporter/runtime/registry.py` 维护插件状态、实例、权限、指标和错误信息。
   - `src/myimporter/runtime/dependency.py` 负责插件依赖排序。
   - `src/myimporter/runtime/plugin_worker.py` 是子进程插件执行器。
   - `src/myimporter/runtime/rpc.py` 使用长度头加 JSON 的 socket RPC 协议。

## Development Guidelines

- 默认把本项目视为用户 Python 基础学习旅程的长期记录与实践场，而不是单一功能仓库。处理问题时要区分学习笔记、章节脚本、手工实验、实践成果和可能逐渐成熟的工程模块。
- 修改学习脚本时保持章节目录结构，不要把练习脚本重构成统一应用，除非用户明确要求。
- 修改 `myimporter` 时优先保持现有分层：`core/`、`runtime/`、`utils/`。
- 不要擅自修改带有全局配置、常量、运行模式、路径、环境变量或系统行为含义的文件，例如 `settings.py`，也不要擅自修改影响范围深远的核心文件。若认为这类文件确有修改必要，应先向用户说明修改原因、影响范围和建议方案，并等待用户指示后再行动。
- 涉及插件运行时改动时，同时检查 `plugin_manager.py`、`registry.py`、`plugin_worker.py`、`rpc.py` 的状态流是否一致。
- 新增插件应放入 `src/plugins/<plugin_name>/`，包含 `manifest.json` 和带 `Plugin` 类的入口模块。
- 运行验证前注意当前环境未必安装 `pytest`，不能假设 `python -m pytest` 可用。
- 编辑中文笔记、中文注释或其他中文内容时保持 UTF-8 编码，并尽量小范围修改。当前在 Windows 命令提示符或 PowerShell 中看到中文乱码，通常是终端默认编码不是 UTF-8 导致的显示问题，不应据此判断源文件内容已经损坏；除非用户明确要求，不要为了“修复乱码”而批量重写中文内容。
- 当前项目有全局 `sitecustomize.py` 参与 Python 启动过程，看到启动日志时不要误判为项目内测试输出。

## Git Automation Boundary

- Git hygiene automation may stage, commit, and push files that are clearly tied to the LearningPython5E learning journey, even when they are currently untracked. This includes learning notes and note assets, practice scripts and supporting data, stage README files, mini-project source files and resources, stage quiz files, learning profile files, learning-profile-derived snapshot images, and personal practice scripts in the project path that are strongly related to the current learning topic.
- The project `tests/` directory is a hard exclusion for Git hygiene automation. Do not stage, unstage, commit, delete, move, edit, clean up, or otherwise operate on files under `tests/`. If a `tests/` path is already staged, leave it exactly as-is and use explicit pathspecs to commit only authorized learning-theme files. Stop only if Git cannot avoid including or touching `tests/` while making the learning-artifact commit.
- Generated/cache/temporary/IDE files such as `__pycache__/`, `.pyc`, temp files, `.venv/`, and `.idea/` remain ignored unless the user explicitly says otherwise.

## Runtime Notes

常见入口：

```powershell
python runtime_service.py
python cli.py list
python cli.py reload plugin_a
python web_ui\web_ui.py
```

默认运行参数目前集中在 `src/myimporter/utils/settings.py` 中，包括：

- 运行时服务：`127.0.0.1:5000`
- Web UI：`127.0.0.1:8000`
- 插件 RPC：从 `9000` 附近分配端口
- 模式语义：`safe_mod`、`runtime_mod`、`dev_mod`

这些模式和配置影响范围较大，修改前应先和用户确认。

## Dependencies

`requirements.txt` 当前记录运行时代码实际使用的第三方依赖：

- `Flask`
- `requests`
- `coloredlogs`

当前没有把 `pytest` 写入依赖文件，因为 `tests/` 还不是稳定的自动化测试套件。后续如果测试自动化逐步成熟，再补充测试依赖和统一测试命令。

## Testing Notes

当前 `tests/` 中的内容更像学习和手工验证脚本，不是稳定的自动化测试套件。

已知情况：

- 代码实际使用了 `Flask`、`requests`、`coloredlogs`。
- 当前环境曾验证 Python 版本为 `3.9.13`。
- 当前环境曾出现 `python -m pytest -q` 失败，原因为未安装 `pytest`。
- `tests/test_for_myimporter.py` 会调用 `src.myimporter.install()`，并尝试导入外部路径中的模块，不能默认作为普通 pytest 测试运行。

## Known Cautions

- `settings.py` 中存在硬编码绝对路径，当前项目明显绑定在 `D:\MySoftwareDownload\PythonPractice\LearningPython5E`。
- `README.md` 现在记录项目介绍、目录结构、常见运行入口、插件约定、测试说明和注意事项。
- `requirements.txt` 现在记录当前运行时代码实际使用的第三方依赖，但不包含尚未稳定化的测试工具依赖。
- `PluginRegistry.to_dict()` 中的 `provides` 当前存在演示性质的硬编码查询。
- 远程插件安装功能依赖占位哈希 `expected_sha256_hash_here`，目前不应视为可直接用于生产的完整功能。
- PowerShell 或命令提示符中的中文乱码优先按终端编码显示问题处理，不要贸然批量改写源文件。
