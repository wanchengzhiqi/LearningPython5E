# Current Session Continuation Template

下面的内容用于新开会话续接当前尚未完成的跨阶段治理任务。它不是
`P3_Statements_and_Syntax` 的新阶段启动模板。

```text
<Subject>
当前会话续接模板（可复用）：P2 收尾后的跨阶段治理与 Python 环境现代化
</Subject>

<Contents>
【任务性质】
这不是新开学习大阶段的会话。

当前仍处于 `P2_Types_and_Operations` 完成验收后的“跨阶段治理期”。请先接续
当前会话尚未完成的历史遗留项与环境现代化事项。只有这些事项处理妥当，并经
我明确确认后，才进入下一学习大阶段 `P3_Statements_and_Syntax`。

请使用 `$pythonpractice-learning-stage` 的自适应策略：把这次任务视为大阶段
交界处的收尾治理，而不是普通章节推进。

---

【项目路径】
`D:\MySoftwareDownload\PythonPractice\LearningPython5E`

开始工作前，请优先读取：

1. `AGENTS.md`
2. `docs/CROSS_STAGE_TRANSITION_HANDOFF.md`
3. `docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`
4. `docs/PYTHON_LEARNING_ROADMAP.md`
5. `docs/REPOSITORY_RESTRUCTURE_PLAN.md`
6. `notes/Python_Learning_Profile.md`

其中：

- `docs/CROSS_STAGE_TRANSITION_HANDOFF.md` 是压缩失败前写入的恢复锚点；
- `docs/PYTHON_ENVIRONMENT_MIGRATION_PLAN.md` 是当前待执行任务的详细依据；
- `docs/PYTHON_LEARNING_ROADMAP.md` 是可动态调整的后续学习路线；
- `docs/REPOSITORY_RESTRUCTURE_PLAN.md` 是已完成仓库重构的历史记录，不要重新
  执行。

---

【已完成事项】
1. `P1_Getting_Started` 已完成。
2. `P2_Types_and_Operations` 已通过收束验收。
3. `C9_Dictionaries_and_Files` 阶段测验已审批完成，建议得分 `96 / 100`。
4. 已完成 `localization_resource_auditor` 综合项目及其精讲、改良和验证。
5. 已完成旧实践成果 `myimporter_system` 的全面代码审查、两轮改良和验证。
6. 已完成仓库结构重构：
   - 阶段成果归档到 `projects/<PART>/<PROJECT>/`；
   - `myimporter_system` 位于
     `projects/P1_Getting_Started/myimporter_system/`；
   - `localization_resource_auditor` 位于
     `projects/P2_Types_and_Operations/localization_resource_auditor/`；
   - 根目录 README 已改为仓库级总览；
   - 项目专属依赖已归入各自项目目录；
   - 根目录 `src/` 只作为未来仓库级公共包的预留位置。
7. 已建立后续动态学习路线图，并补入现代工程、并发与 I/O 等旧书覆盖不足的
   主题。
8. 已完成 Python 环境迁移评估和 Python `3.9.13` 旧环境回归基线。
9. 已在 `.gitignore` 中加入 `.venv-py*/`，用于忽略未来的并行虚拟环境。

---

【当前待完成事项】
当前首要任务是 Python 环境现代化，但尚未获得我的安装方式确认。

推荐方案：

1. 保留旧 Python `3.9.13`；
2. 保留旧 `.venv` 作为历史回归环境；
3. 并行安装受支持的新版 Python；
4. 推荐候选安装路径：
   `D:\MySoftwareDownload\Python\Python314`
5. 新建并行虚拟环境：
   `.venv-py314`
6. 只按项目声明安装依赖，不要无差别克隆旧 `.venv`；
7. 暂不修改持久化 PATH；
8. 暂不向新解释器复制全局 `sitecustomize.py`；
9. 完成新环境回归后，再由我手工切换或确认 PyCharm SDK。

继续执行前，先向我确认：

1. PyCharm 升级由我手工完成，还是需要你协助？
2. Python 新版本安装由我手工完成，还是允许你下载并启动官方安装程序？
3. 是否继续使用推荐安装路径
   `D:\MySoftwareDownload\Python\Python314`？

重要：新会话恢复时，必须重新浏览 Python 官方来源确认“当前最新稳定版本”。
截至 2026-06-02，已验证的候选版本为 Python `3.14.5`；如果恢复日期更晚，不要
机械沿用这个版本号。

---

【已确认的旧环境事实】
- 默认解释器：
  `D:\MySoftwareDownload\Python\Python39\python.exe`
- 当前版本：Python `3.9.13`
- 当前 `.venv` 基于 Python `3.9.13`
- `py -0p` 当前没有发现已注册解释器
- 当前 PATH 中可见：
  `D:\MySoftwareDownload\PyCharm 2023.3.5\bin`
- 旧解释器全局启动钩子：
  `D:\MySoftwareDownload\Python\Python39\Lib\site-packages\sitecustomize.py`
- 项目内可追溯模板：
  `projects/P1_Getting_Started/myimporter_system/src/myimporter/sitecustomize_template.py`
- 两者在 2026-06-02 验证时 SHA-256 一致：
  `23B3D1524F7A8DFA40001E7B042CDC40F7F7D9300DDF0669B59F623F81E24736`

---

【已通过的 Python 3.9 基线】
不要无故重新扩大审查范围。迁移后以这些结果作为对照：

1. `py_compile` 通过；
2. `localization_resource_auditor --format json | python -m json.tool` 通过；
3. `myimporter` 安装与卸载通过；
4. RuntimeService、CLI、子进程 worker 临时端口生命周期通过；
5. `plugin_a` 以 `inprocess` 模式激活；
6. `plugin_b` 以 `subprocess` 模式激活；
7. CLI 的 `list`、`status plugin_b`、`shutdown` 通过；
8. Web UI 在线接口通过：
   - `/` -> `200`
   - `/api/plugins` -> `200`
   - `/api/plugins/reload/plugin_a` -> `200`
   - `/api/plugins/install` -> `501`，符合明确禁用远程安装的设计
9. 服务关闭后没有残留 Python 进程；
10. 全局 `sitecustomize.py` 默认静默，默认不会自动导入 `myimporter`。

---

【安全边界】
最高优先级：

1. 禁止批量删除文件或目录。
2. 不得使用：
   - `del /s`
   - `rd /s`
   - `rmdir /s`
   - `Remove-Item -Recurse`
   - `rm -rf`
3. 如需删除文件，只能一次删除一个明确路径的文件。
4. 不触碰 `tests/`：
   - 不编辑；
   - 不移动；
   - 不删除；
   - 不暂存；
   - 不取消暂存；
   - 不清理。
5. 不删除旧 Python。
6. 不删除或覆盖旧 `.venv`。
7. 不批量重写 `.idea/`。
8. 新解释器初始环境不要复制全局 `sitecustomize.py`。
9. 不把旧环境全部依赖无差别复制到新环境。
10. 当前工作区已有大量与前序治理任务相关的未暂存改动、移动结果和未跟踪
    文件。不要擅自回滚、清理或提交；先理解现状，再小范围操作。

---

【当前学习画像】
我当前 Python 基础处于：

“准中级入门已经基本坐稳，正在向可独立做小型工程设计的中级入门过渡。”

已稳定：

- 对象、名字绑定、原地修改、重新绑定；
- `is` 与 `==`；
- 数字、字符串、列表、元组、字典、集合、文件对象；
- 浅拷贝、深拷贝与共享引用；
- 哈希、映射、字典视图；
- 路径、文件对象、`str`、`bytes`、编码；
- JSON、CSV、结构化报告；
- 小型 CLI 工具和项目级数据流。

仍需持续精修：

- 相等性与身份的术语精度；
- 内部对象模型、JSON 文本和磁盘字节的分层表达；
- 教学快照中的重复逻辑 vs 值得抽取的稳定公共能力；
- 函数、模块、异常、测试、包组织尚未系统学习。

---

【后续路线提醒】
不要在本次续接会话中直接开启 `P3_Statements_and_Syntax`。

在环境现代化和剩余治理事项处理完成后，再根据：

1. `notes/Python_Learning_Profile.md`
2. `docs/PYTHON_LEARNING_ROADMAP.md`
3. 我后续的明确确认

生成真正的 P3 新开会话启动模板。

---

【回答要求】
- 默认使用中文。
- 不要假定我的理解、题干或推论必然正确；发现细小偏差也要显式纠正。
- 优先讲本质和边界。
- 修改文件前先说明准备做什么。
- 修改后执行小范围、可验证的检查。
- 不要把 `tests/` 当作成熟自动化测试套件。
- 不要因为终端中文乱码就批量重写源文件。
- 不要把当前续接任务误判为 P3 正式开课。
</Contents>
```
