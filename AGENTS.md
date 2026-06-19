# AGENTS.md

## Project Context

本仓库是用户 Python 基础学习旅程的长期记录与实践空间，主要参考
《Learning Python 5th Edition》。它会持续积累学习笔记、章节脚本、手工实验、
阶段测验、综合实践成果，以及后续逐步成熟的工程模块。

学习大阶段对应书籍中的 `PART`，例如 `P1_Getting_Started` 和
`P2_Types_and_Operations`。学习小阶段对应章节，例如
`C9_Dictionaries_and_Files`。

## Repository Structure

- `notes/`：中文学习笔记、截图资源和学习画像。
- `practice/<PART>/<CHAPTER>/`：章节练习、实验脚本、样例数据和阶段测验。
- `projects/<PART>/<PROJECT>/`：按学习大阶段归档的综合实践成果。
- `docs/`：仓库治理说明、迁移计划和跨阶段文档。
- `src/`：仓库级公共包的预留位置。只有出现多个独立调用方、稳定接口和
  可验证复用需求时才启用；不要把教学脚本中的重复片段直接搬入这里。
- `tests/`：历史手工实验脚本，不默认视为成熟自动化测试套件。
- `README.md`：面向人类读者的仓库级总览与项目索引。

根目录不设置统一 `requirements.txt`。第三方依赖应由需要它们的项目在自己的
目录中声明。

## Roadmap Governance

- 后续学习路线以 `docs/PYTHON_LEARNING_ROADMAP.md` 为当前仓库级参考。
- 参考书章节是语言主线和来源索引，不是不可调整的课表。允许根据最新学习
  画像、项目需求和现代 Python 工程实践合并、拆分、前置或补充主题。
- 学习会话默认以 `CHAPTER` 为粒度：一个新会话只正式推进一个 `PART` 下的
  一个章节。`PART` 和相邻章节用于提供路线背景；当前章节收束后，为下一个
  章节生成新的启动模板并另开会话。
- 每次跨越大阶段边界，或阶段测验暴露出反复薄弱点时，复核路线图并按需更新。
- 小阶段收束、大阶段收束、路线调整、环境迁移、仓库重构或长期流程规则改变
  后，按职责复核 `README.md`、`AGENTS.md`、`docs/` 索引、路线图、学习画像
  和相关项目文档，避免长期记录漂移。`README.md` 只保留仓库级进度入口和
  读者索引；`AGENTS.md` 只保留持久规则、安全边界、目录职责、环境边界和
  代理工作流，不逐章镜像当前小阶段。用户级 Codex 记忆只在用户明确要求时
  同步。
- `P2_Types_and_Operations` 已通过收束验收，当前学习主线已进入
  `P3_Statements_and_Syntax`。具体小阶段状态、下一章启动模板和阶段测验结果
  以 `docs/PYTHON_LEARNING_ROADMAP.md`、`notes/Python_Learning_Profile.md`
  和 `docs/README.md` 为准。
- Python `3.14.5` 并行安装、`.venv-py314` 创建和命令行回归已经完成。
  旧 Python `3.9.13` 与旧 `.venv` 保留用于历史实验回归。PyCharm 升级暂缓；
  项目 SDK 已指向 `.venv-py314\Scripts\python.exe`，但 PyCharm `2023.3.5`
  会把该 SDK 显示为 `Python 3.10 (LearningPython5E)`。判断实际解释器时以
  `sys.version` 和 `sys.executable` 为准。当前迁移记录和使用边界见
  `docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`。

## Current Capstones

### P1: myimporter_system

路径：`projects/P1_Getting_Started/myimporter_system/`

- `src/myimporter/`：自定义导入器与插件运行时核心包。
- `plugins/`：示例插件和清单文件。
- `runtime_service.py`：插件运行时 TCP 服务入口。
- `cli.py`：通过 socket 与 RuntimeService 交互的命令行入口。
- `web_ui/`：基于 Flask 的插件管理客户端。
- `requirements.txt`：该项目的第三方依赖。

核心分层：

1. 自定义导入机制：
   - `src/myimporter/install.py` 提供 `install()` / `uninstall()`。
   - `src/myimporter/core/finder.py` 实现自定义 `MetaPathFinder`。
   - `src/myimporter/core/loader.py` 实现自定义 `SourceLoader`。
   - `src/myimporter/core/providers.py` 提供文件系统和环境变量路径查找。
   - `src/myimporter/core/path_manager.py` 负责路径规范化和管理。

2. 插件运行时：
   - `src/myimporter/runtime/plugin_manager.py` 管理插件生命周期和 worker。
   - `src/myimporter/runtime/registry.py` 维护状态、实例、权限、指标和错误。
   - `src/myimporter/runtime/dependency.py` 负责依赖排序。
   - `src/myimporter/runtime/plugin_worker.py` 是子进程执行器。
   - `src/myimporter/runtime/rpc.py` 使用长度头加 JSON 的 socket RPC 协议。

常见入口：

```powershell
python projects\P1_Getting_Started\myimporter_system\runtime_service.py
python projects\P1_Getting_Started\myimporter_system\cli.py list
python projects\P1_Getting_Started\myimporter_system\cli.py reload plugin_a
python projects\P1_Getting_Started\myimporter_system\web_ui\web_ui.py
```

### P2: localization_resource_auditor

路径：`projects/P2_Types_and_Operations/localization_resource_auditor/`

这是 `P2_Types_and_Operations` 的综合实践成果，用于整合字典、列表、元组、
集合、文件对象、JSON、CSV、编码边界和结构化报告。

## Development Guidelines

- 把本仓库视为学习旅程，不要把章节脚本重构成单一应用。
- 教学脚本允许保留重复实现作为学习轨迹。只有至少两个独立调用方需要同一
  稳定契约时，才考虑提取仓库级公共包。
- 修改学习脚本时保持 `practice/<PART>/<CHAPTER>/` 结构。
- 新的阶段综合成果放入 `projects/<PART>/<PROJECT>/`，并提供自己的 README。
- 项目专属依赖放在项目目录中，不要默认提升到仓库根目录。
- 修改 `myimporter_system` 时保持 `core/`、`runtime/`、`utils/` 分层。
- 涉及插件运行时改动时，同时检查 `plugin_manager.py`、`registry.py`、
  `plugin_worker.py` 和 `rpc.py` 的状态流。
- 新增 `myimporter` 示例插件应放入
  `projects/P1_Getting_Started/myimporter_system/plugins/<plugin_name>/`。
- 不要擅自修改带有全局配置、路径、环境变量、模式语义或系统行为含义的文件。
  如确有必要，应先说明原因、影响范围和建议方案，并等待用户授权。
- 当前环境未必安装 `pytest`，不要默认执行 `python -m pytest`。
- 后续日常学习默认先激活仓库根目录下的 `.venv-py314`。未激活虚拟环境时，
  裸 `python` 仍指向旧 Python `3.9.13`，不要误把它当成当前学习环境。
- 编辑中文内容时保持 UTF-8。终端乱码通常是显示问题，不要据此批量重写文件。
- 旧 Python `3.9.13` 有全局 `sitecustomize.py` 参与启动过程，不要误判相关
  日志来源。新 Python `3.14.5` 与 `.venv-py314` 当前保持干净，不要未经授权
  复制全局启动钩子。

## Git Automation Boundary

- Git hygiene automation may stage, commit, and push learning-theme files,
  including notes, assets, practice scripts, project resources, quizzes, and
  learning-profile artifacts.
- `tests/` is a hard exclusion. Do not stage, unstage, commit, delete, move,
  edit, clean up, or otherwise operate on files under `tests/`.
- If a `tests/` path is already staged, leave it exactly as-is and use explicit
  pathspecs for authorized files.
- Generated, cache, temporary, and IDE files such as `__pycache__/`, `.pyc`,
  `.venv/`, and `.idea/` remain ignored unless explicitly authorized.

## Runtime Notes

`myimporter_system` 默认参数集中在其 `src/myimporter/utils/settings.py`：

- RuntimeService：`127.0.0.1:5000`
- Web UI：`127.0.0.1:8000`
- 插件 RPC：监听地址默认为 `127.0.0.1`，端口由操作系统动态分配
- 模式语义：`safe_mod`、`runtime_mod`、`dev_mod`

项目目录根据 `settings.py` 位置动态推导。运行时服务、Web UI、插件目录、
worker 解释器和 RPC 参数支持通过对应的 `MYIMPORTER_*` 环境变量覆盖。

`projects/P1_Getting_Started/myimporter_system/src/myimporter/sitecustomize_template.py`
是全局启动钩子的可追溯模板。全局副本默认静默；显式启用时需要通过
`MYIMPORTER_SOURCE_ROOT` 指向该项目的 `src/` 目录。当前只在旧 Python
`3.9.13` 中保留全局副本；新 Python `3.14.5` 默认不安装该钩子。

## Known Cautions

- `myimporter_system` 的权限字段仍是元数据，不构成安全边界。
- worker 子进程提高故障隔离程度，但不是安全沙箱。
- 远程插件安装入口当前明确禁用。
- PowerShell 或命令提示符中的中文乱码优先按终端编码显示问题处理。
