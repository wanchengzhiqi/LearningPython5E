# Python Environment Migration Plan

更新时间：2026-06-03

## 1. 目的

这份文档用于规划 `LearningPython5E` 从 Python `3.9.13` 向受支持版本的
迁移。迁移目标不是覆盖旧环境，而是建立一条可回滚、可验证的并行升级路径。

当前仍处于跨阶段治理期。正式开始 `P3_Statements_and_Syntax` 前，先完成
环境现代化，可以避免把解释器差异、IDE 差异和新章节学习混在同一轮排错中。

## 2. 官方版本状态

截至 2026-06-03：

- Python `3.9` 已于 2025-10-31 结束官方支持；
- Python `3.14` 处于 bugfix 维护阶段；
- Windows 官方下载页列出的最新稳定 Python 3 版本为 `3.14.5`，发布日期为
  2026-05-10；
- Windows 官方下载页列出的最新 Python install manager 为 `26.2`，发布日期为
  2026-05-11；
- Python `3.15` 仍处于 prerelease 阶段，不适合作为当前学习仓库的默认环境。

官方来源：

- [Status of Python versions](https://devguide.python.org/versions/)
- [Python Releases for Windows](https://www.python.org/downloads/windows/)

## 3. 当前环境盘点

### 3.1 解释器

当前命令行默认解释器：

```text
Python 3.9.13
D:\MySoftwareDownload\Python\Python39\python.exe
```

当前为 64 位 Windows 与 64 位 Python 进程。

现有 Python `3.9.13` 仍可以正常通过 `python` 命令使用，但它不在 Windows
Python Launcher 的可发现列表中。

2026-06-03 已并行安装：

```text
Python 3.14.5
D:\MySoftwareDownload\Python\Python314\python.exe
```

新安装器同时更新了全局 `py launcher`。当前：

- `py -0p` 可以发现 Python `3.14`；
- `py` 与 `py -3.14` 指向 Python `3.14.5`；
- `python` 仍指向旧 Python `3.9.13`，因为没有修改持久化 `PATH`。

### 3.2 项目虚拟环境

现有虚拟环境：

```text
D:\MySoftwareDownload\PythonPractice\LearningPython5E\.venv
```

它基于：

```text
D:\MySoftwareDownload\Python\Python39\python.exe
```

现有 `.venv` 应暂时保留，作为 Python `3.9.13` 历史回归环境。不要覆盖、原地
升级或批量删除它。

2026-06-03 已新建并行虚拟环境：

```text
D:\MySoftwareDownload\PythonPractice\LearningPython5E\.venv-py314
```

它基于 Python `3.14.5`，只安装项目声明依赖及其传递依赖，没有无差别复制旧
`.venv`。新环境确认不包含历史残留 `requests`。

### 3.3 PyCharm

当前项目 `.idea/misc.xml` 指向：

```text
Python 3.10 (LearningPython5E)
```

当前机器 PATH 中可见的 IDE 路径是：

```text
D:\MySoftwareDownload\PyCharm 2023.3.5\bin
```

PyCharm `2023.3` 的官方说明重点支持 Python `3.12` 特性。不要未经验证就假设
它能完整理解 Python `3.14` 的新语法、调试协议和代码分析能力。

截至 2026-06-03，JetBrains 官方页面列出的当前版本为 PyCharm `2026.1`。
迁移时应升级现有 PyCharm `2023.3.5`，而不是继续把旧 IDE 作为 Python
`3.14.5` 的默认开发环境。

如果采用 Python `3.14.5`，建议先把 PyCharm 升级到支持现代 Python 版本的
新版本，再在 IDE 中手工切换项目解释器。

用户已于 2026-06-03 明确决定暂不升级 PyCharm。2026-06-04 已在 PyCharm 中
把项目 SDK 切换到现有虚拟环境：

```text
D:\MySoftwareDownload\PythonPractice\LearningPython5E\.venv-py314\Scripts\python.exe
```

需要注意：PyCharm `2023.3.5` 会把该 SDK 显示为
`Python 3.10 (LearningPython5E)`，这与命令行验证出的实际解释器版本
Python `3.14.5` 不一致。判断真实解释器时，应以 `sys.version`、
`sys.executable` 和实际运行结果为准；仍不把该旧 IDE 对 Python `3.14` 的
代码分析、调试协议和新语法支持视为完整验证。

官方来源：

- [What's New in PyCharm 2023.3](https://www.jetbrains.com/pycharm/whatsnew/2023-3/)
- [What's New in PyCharm 2026.1](https://www.jetbrains.com/pycharm/whatsnew/)
- [PyCharm installation guide](https://www.jetbrains.com/help/pycharm/installation-guide.html)
- [Configure a Python interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)

### 3.4 环境变量

当前 Codex 进程中可见：

```text
ENABLE_MYIMPORTER=0
PYTHONPATH=<repo>;<repo>\practice;<repo>\src;<repo>\projects;
MY_MODULE_PATHS=<repo>;<repo>\practice;<repo>\projects;<repo>\src;...
```

这些变量没有写入用户级或机器级环境变量。它们属于当前进程环境，不应被直接
当作新环境的永久配置模板。

根目录 `src/` 目前只是仓库级公共包的预留位置。迁移时要继续保持这个边界，
不要因为历史环境变量仍包含 `<repo>\src` 就误认为它已经有公共包职责。

## 4. 推荐决策

### 默认建议

采用并行迁移：

1. 保留 Python `3.9.13` 与当前 `.venv`；
2. 升级 PyCharm；
3. 并行安装 Python `3.14.5` 64 位；
4. 用 Python `3.14.5` 新建独立虚拟环境，例如 `.venv-py314`；
5. 只按项目声明安装依赖；
6. 执行本文件中的回归清单；
7. 回归通过后，在 PyCharm 中把项目 SDK 切换到新虚拟环境；
8. 保留旧环境一段时间，供历史脚本回看和差异实验使用。

### 为什么不原地覆盖

- Python `3.9.13` 是既有学习记录的历史基线；
- `.venv` 绑定基础解释器，不适合视为可跨大版本平移的目录；
- 全局 `sitecustomize.py` 属于解释器级行为，新解释器应先保持干净；
- 并行环境可以把“安装失败”“依赖兼容”“项目回归”“IDE 切换”拆开验证。

### 安装方式

Windows 官方页提供 Python install manager 和 64 位 Windows installer。

对于当前学习仓库，两种方式都可以。若希望保持现有的显式路径风格，可以使用
官方 64 位 installer，把 Python `3.14.5` 并行安装到新的独立目录。不要覆盖
`D:\MySoftwareDownload\Python\Python39`。

## 5. 依赖策略

`localization_resource_auditor` 只使用标准库，不需要第三方依赖。

`myimporter_system` 当前声明：

```text
Flask
coloredlogs
```

代码扫描确认：当前系统不再导入 `requests`。旧 `.venv` 中的 `requests` 是
历史残留，不应无差别复制到新环境。

新环境应按项目声明安装：

```powershell
<new-python> -m venv .venv-py314
.\.venv-py314\Scripts\python.exe -m pip install --upgrade pip
.\.venv-py314\Scripts\python.exe -m pip install -r projects\P1_Getting_Started\myimporter_system\requirements.txt
```

仓库 `.gitignore` 已通过 `.venv-py*/` 规则忽略并行版本化虚拟环境，例如
`.venv-py314/`。

## 6. 全局 sitecustomize 边界

旧解释器中的全局文件：

```text
D:\MySoftwareDownload\Python\Python39\Lib\site-packages\sitecustomize.py
```

当前它和项目模板 SHA-256 一致：

```text
23B3D1524F7A8DFA40001E7B042CDC40F7F7D9300DDF0669B59F623F81E24736
```

模板位置：

```text
projects\P1_Getting_Started\myimporter_system\src\myimporter\sitecustomize_template.py
```

迁移原则：

1. 新 Python `3.14.5` 初始环境不要复制全局 `sitecustomize.py`；
2. 先验证普通解释器、虚拟环境和两个阶段项目；
3. 只有确实需要全局 opt-in bootstrap 时，再把可追溯模板复制到新解释器；
4. 复制后验证默认静默；
5. 再显式设置 `ENABLE_MYIMPORTER=1`、`MYIMPORTER_SOURCE_ROOT` 和
   `MY_MODULE_PATHS`，验证 opt-in 行为。

## 7. Python 3.9 历史基线

以下检查已在 2026-06-02 使用现有 `.venv` 通过。

### 7.1 核心语法与阶段项目

- `py_compile`：通过；
- `localization_resource_auditor --format json | python -m json.tool`：通过；
- `Flask`、`requests`、`coloredlogs` 导入：通过。

### 7.2 myimporter 安装器

- `safe_mod -> runtime_mod -> safe_mod`：通过；
- 安装后 finder 位于 `sys.meta_path`：通过；
- 卸载后 finder 清理：通过。

### 7.3 RuntimeService、CLI 和 worker

临时端口生命周期验证：

- `list`：通过；
- `status plugin_b`：通过；
- `plugin_a` 以 `inprocess` 模式激活：通过；
- `plugin_b` 以 `subprocess` 模式激活：通过；
- `shutdown`：通过；
- 服务退出后没有新增 Python PID 残留：通过。

### 7.4 Web UI

在线 RuntimeService 下：

- `/`：`200`；
- `/api/plugins`：`200`；
- `/api/plugins/reload/plugin_a`：`200`；
- `/api/plugins/install`：`501`，符合“远程安装明确禁用”的设计。

### 7.5 全局 sitecustomize

- 全局文件和项目模板 SHA-256 一致：通过；
- 默认启动保持静默：通过；
- 默认不会自动导入 `myimporter`：通过。

## 8. Python 3.14 回归清单

安装新解释器并创建新虚拟环境后，按顺序验证：

1. `python --version` 与解释器路径；
2. `sys.executable`、`sys.prefix`、`sys.base_prefix`；
3. `py_compile`；
4. `localization_resource_auditor --format json | python -m json.tool`；
5. `myimporter` 安装器模式切换；
6. RuntimeService、CLI、worker 临时端口生命周期；
7. Web UI 在线路由；
8. worker 解释器是否来自新虚拟环境；
9. 默认没有全局 `sitecustomize.py` 时是否正常；
10. 如需 opt-in bootstrap，再单独复制模板并验证默认静默与显式启用；
11. 在 PyCharm 中切换 SDK，并运行一条章节脚本与两个阶段项目；
12. 记录 Python `3.9.13` 与 `3.14.5` 的差异。

### 8.1 2026-06-03 命令行回归结果

已通过：

1. 新解释器版本、路径、`sys.executable`、`sys.prefix` 与 `sys.base_prefix`；
2. `.venv-py314` 已由 `.gitignore` 的 `.venv-py*/` 规则忽略；
3. `pip check`；
4. `localization_resource_auditor --format json | python -m json.tool`；
5. `myimporter` 的 `safe_mod -> runtime_mod -> safe_mod` 切换、finder 插入与清理；
6. RuntimeService、CLI、worker 临时端口生命周期；
7. CLI 的 `list`、`status plugin_b` 与 `shutdown`；
8. `plugin_a` 以 `inprocess` 模式激活；
9. `plugin_b` 以 `subprocess` 模式激活；
10. `plugin_b` worker 明确由 `.venv-py314\Scripts\python.exe` 启动；
11. Web UI 的 `/`、`/api/plugins` 与 `/api/plugins/reload/plugin_a` 返回 `200`；
12. Web UI 的 `/api/plugins/install` 返回预期中的 `501`；
13. 服务关闭后无残留 Python 进程；
14. 新解释器与新虚拟环境默认都没有加载 `sitecustomize` 或 `myimporter`；
15. 一条 C9 章节脚本可正常运行。

Python `3.14` 同时暴露出 Windows 路径示例中的无效转义序列警告。已把
`localization_auditor.py` 和六个 C9 教学脚本的模块文档字符串改为原始字符串，
随后重新通过定向 `py_compile`。

尚未执行：

1. PyCharm IDE 内代表性脚本回归；
2. 为新解释器复制全局 `sitecustomize.py`，因为当前没有必要；
3. 修改持久化 `PATH`，因为当前并行状态已经满足验证需求。

## 9. 需要人工确认后再执行的事项

以下操作会改变机器级开发环境，不应静默执行：

1. 是否升级 PyCharm：用户已决定暂缓；
2. 安装方式：已使用官方 64 位 installer；
3. Python `3.14.5` 的安装目录：已采用 `D:\MySoftwareDownload\Python\Python314`；
4. 新虚拟环境名称：已采用 `.venv-py314`；
5. PyCharm 项目 SDK：已指向 `.venv-py314\Scripts\python.exe`，但 PyCharm
   `2023.3.5` 显示标签不准确；
6. 是否在回归完成后为新解释器安装全局 `sitecustomize.py`；
7. 是否调整持久化 PATH。

## 10. 当前结论

Python `3.14.5` 并行安装、新虚拟环境创建和命令行回归已经完成。

当前保留一个有意为之的过渡状态：

- `python` 命令仍指向旧 Python `3.9.13`；
- `py` 与 `py -3.14` 指向新 Python `3.14.5`；
- `.venv` 保留为历史回归环境；
- `.venv-py314` 是已经通过命令行回归的新环境；
- 新解释器没有复制全局 `sitecustomize.py`；
- PyCharm `2023.3.5` 暂不升级；项目 SDK 已指向 `.venv-py314`，但 UI 标签
  显示为 `Python 3.10 (LearningPython5E)`，不应把该标签当作真实解释器版本；
- 持久化 `PATH` 暂不修改。

后续只需要单独决定：

1. 何时升级 PyCharm，并重新验证 Python `3.14` IDE 支持；
2. 是否在 PyCharm 内跑一组代表性脚本回归；
3. 是否确实需要为新解释器安装 opt-in `sitecustomize.py`；
4. 是否要让持久化 `PATH` 中的 `python` 命令转向新解释器。

## 11. 日常使用约定

后续仓库学习默认使用 `.venv-py314`。进入新的 PowerShell 会话后，在仓库根
目录运行：

```powershell
.\.venv-py314\Scripts\Activate.ps1
python --version
```

预期输出版本为 Python `3.14.5`。激活后，普通 `python` 与 `python -m pip`
都会落入 `.venv-py314`。离开时运行：

```powershell
deactivate
```

如果不希望激活环境，也可以显式调用：

```powershell
.\.venv-py314\Scripts\python.exe <script>
```

注意：

- 未激活虚拟环境时，裸 `python` 仍指向旧 Python `3.9.13`；
- `py -3.14` 启动的是 Python `3.14.5` 基础解释器，不会自动进入
  `.venv-py314`；
- PyCharm 项目 SDK 已指向 `.venv-py314\Scripts\python.exe`，但旧 IDE 可能
  显示为 `Python 3.10`；如需确认，运行 `import sys` 后查看 `sys.version`
  和 `sys.executable`；
- 旧 Python `3.9.13` 与旧 `.venv` 只作为历史回归基线；
- 新 Python `3.14.5` 和 `.venv-py314` 不需要全局 `sitecustomize.py`；
- 只有未来明确需要全局 opt-in bootstrap 时，才单独评估复制模板。
