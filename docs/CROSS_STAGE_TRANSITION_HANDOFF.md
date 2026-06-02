# Cross-Stage Transition Handoff

更新时间：2026-06-02

## Purpose

这是一份上下文压缩后的恢复锚点。恢复任务时，先读取本文件，再按需读取它引用
的详细文档。不要从头重复仓库重构或 Python `3.9.13` 基线盘点。

## Current State

- `P1_Getting_Started`：已完成。
- `P2_Types_and_Operations`：已通过收束验收。
- 当前处于跨阶段治理期。
- 下一大阶段：`P3_Statements_and_Syntax`。
- 当前正在处理的事项：Python 环境现代化。

## Completed Work

1. 已完成 `myimporter_system` 全面审查、改良和归档。
2. 已完成仓库结构重构：
   - 阶段成果归入 `projects/<PART>/<PROJECT>/`；
   - 根目录 README 改为仓库级总览；
   - 项目依赖归入项目目录；
   - 根目录 `src/` 仅作为未来仓库级公共包的预留位置。
3. 已建立动态学习路线图：
   - `docs/PYTHON_LEARNING_ROADMAP.md`
4. 已完成 Python 环境迁移评估：
   - `docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`
5. 已更新：
   - `README.md`
   - `AGENTS.md`
   - `notes/Python_Learning_Profile.md`
   - `.gitignore`
   - 用户级 `$pythonpractice-learning-stage` 技能的路线自适应规则
   - 用户级 Codex 记忆增量

## Confirmed Environment Facts

- 当前默认解释器：
  `D:\MySoftwareDownload\Python\Python39\python.exe`
- 当前版本：Python `3.9.13`
- 当前 `.venv` 基于 Python `3.9.13`，应保留作历史回归环境。
- `py -0p` 当前没有发现已注册解释器。
- 当前 PATH 中可见：`D:\MySoftwareDownload\PyCharm 2023.3.5\bin`
- 官方 Windows 页面截至 2026-06-02 列出的最新稳定 Python 3 是
  Python `3.14.5`。

## Python 3.9 Baseline

以下基线已经通过，不要无故重新扩大验证范围：

- `py_compile`
- `localization_resource_auditor --format json`
- `myimporter` 安装与卸载
- RuntimeService、CLI、子进程 worker 生命周期
- Web UI 在线接口
- 全局 `sitecustomize.py` 默认静默
- 服务关闭后无残留 Python 进程

## Pending Decision

等待用户确认是否按推荐方案进入安装执行阶段：

1. 并行安装 Python `3.14.5` 64 位到
   `D:\MySoftwareDownload\Python\Python314`
2. 创建 `.venv-py314`
3. 仅按项目声明安装依赖
4. 暂不修改 PATH
5. 暂不复制全局 `sitecustomize.py`
6. 完成回归后，再手工切换 PyCharm SDK

还需要用户说明：

- PyCharm 升级是否手工完成；
- Python 安装是否手工完成，还是允许 Codex 下载并启动官方安装程序。

## Safety Boundaries

- 不删除旧 Python。
- 不删除或覆盖旧 `.venv`。
- 不批量删除任何文件或目录。
- 不触碰 `tests/`：不编辑、不移动、不删除、不暂存、不取消暂存、不清理。
- 不批量重写 `.idea/`。
- 新解释器初始环境不要复制全局 `sitecustomize.py`。
- 不把旧环境中的全部已安装包无差别复制到新环境。

## Resume Order

恢复后依次执行：

1. 读取本文件。
2. 读取 `docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`。
3. 获取用户对安装方式的确认。
4. 如获授权，执行并行安装和 `.venv-py314` 创建。
5. 按迁移计划中的 Python `3.14` 回归清单验证。

## Detailed References

- `docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`
- `docs/PYTHON_LEARNING_ROADMAP.md`
- `docs/REPOSITORY_RESTRUCTURE_PLAN.md`
- `notes/Python_Learning_Profile.md`
