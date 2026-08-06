# LearningPython5E

本仓库是围绕《Learning Python 5th Edition》持续演进的 Python 学习记录与
实践空间。它不是某一个应用的源码仓库，也不把代码规模更大的项目默认视为
更重要的成果。

## 学习阶段模型

- **大阶段**：对应书籍中的 `PART`，例如 `P1_Getting_Started`、
  `P2_Types_and_Operations`。
- **小阶段**：对应大阶段中的章节，例如
  `P2_Types_and_Operations/C9_Dictionaries_and_Files`。
- **会话粒度**：默认一个新会话只正式推进一个 `CHAPTER`。完成当前章节收束
  后，为下一个章节生成新的启动模板并另开会话。
- **阶段成果**：在一个大阶段接近收束时形成的可复盘项目，统一归档到
  `projects/<PART>/`。

## 目录职责

```text
LearningPython5E/
  notes/
  practice/
  projects/
  docs/
  tests/
  AGENTS.md
  README.md
```

- `notes/`：中文学习笔记、截图资源和学习画像。
- `practice/`：按 `PART` 和章节组织的实验、练习、样例数据与阶段测验。
- `projects/`：按 `PART` 归档的阶段综合实践成果。每个项目自行维护 README、
  资源文件和专属依赖。
- `docs/`：仓库治理说明、迁移计划和需要跨阶段复用的文档。
- `tests/`：历史手工实验脚本。目前不默认视为成熟自动化测试套件。

仓库根目录不再设置统一 `requirements.txt`。学习笔记和标准库练习不需要共享
运行时依赖；确有第三方依赖的阶段成果应在自己的项目目录中声明。

## 日常学习环境

后续学习默认使用 Python `3.14.5` 的仓库级虚拟环境。在仓库根目录进入新的
PowerShell 会话后，先运行：

```powershell
.\.venv-py314\Scripts\Activate.ps1
python --version
```

预期版本为 Python `3.14.5`。完成学习后可以运行 `deactivate` 离开虚拟环境。

当前刻意保留并行状态：未激活虚拟环境时，裸 `python` 仍指向旧 Python
`3.9.13`；`py` 与 `py -3.14` 指向新 Python `3.14.5`。旧 `.venv` 仅作为
历史回归基线，不再作为日常学习环境。详细说明见
[`docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`](docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md)。

## 当前阶段成果

### P1 Getting Started

- [`myimporter_system`](projects/P1_Getting_Started/myimporter_system/README.md)：
  自定义导入器与插件运行时系统，用于观察 `sys.meta_path`、模块加载、插件
  生命周期、依赖排序、子进程边界和 socket JSON RPC。

### P2 Types and Operations

- [`localization_resource_auditor`](projects/P2_Types_and_Operations/localization_resource_auditor/README.md)：
  游戏本地化资源审计 CLI，用于整合字典、集合、列表、元组、文件对象、
  JSON、CSV、编码边界和结构化报告。

### P3 Statements and Syntax

- [`prompt_template_manager`](projects/P3_Statements_and_Syntax/prompt_template_manager/README.md)：
  本地 Prompt 模板数据库 GUI/CLI 工具，用 SQLite 保存 prompt 与说明内容，
  并用 tkinter 提供简单的增删改查界面。

## 学习进度入口

- `P1_Getting_Started`：已完成。
- `P2_Types_and_Operations`：已通过收束验收。
- `P3_Statements_and_Syntax`：C10-C15 已完成最终收束。
- `P4_Functions_and_Generators`：已正式开始；`PART opener`
  `C16_Function_Basics` 已完成最终收束。下一正式入口为 `C17_Scopes`
  （`normal`），应从
  [`docs/C17_SCOPES_STARTUP_TEMPLATE.md`](docs/C17_SCOPES_STARTUP_TEMPLATE.md)
  另开新会话。章级进度、阶段测验状态和新会话启动模板，以
  [`docs/PYTHON_LEARNING_ROADMAP.md`](docs/PYTHON_LEARNING_ROADMAP.md)、
  [`notes/Python_Learning_Profile.md`](notes/Python_Learning_Profile.md) 和
  [`docs/README.md`](docs/README.md) 为准。
- 本 README 只保留仓库级进度入口和阶段成果索引，不逐章镜像当前小阶段，
  以免每次章节收束后频繁漂移。

## 仓库治理

- 文档索引见 [`docs/README.md`](docs/README.md)。
- 后续学习路线见
  [`docs/PYTHON_LEARNING_ROADMAP.md`](docs/PYTHON_LEARNING_ROADMAP.md)。
- Python 环境现代化方案见
  [`docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`](docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md)。
- 仓库结构调整的历史执行记录见
  [`docs/REPOSITORY_RESTRUCTURE_PLAN.md`](docs/REPOSITORY_RESTRUCTURE_PLAN.md)。

Windows 终端中出现中文乱码时，应先考虑终端默认编码问题，不要据此批量重写
源文件。运行 Python 验证后产生的 `__pycache__/` 和 `.pyc` 文件属于忽略项。
