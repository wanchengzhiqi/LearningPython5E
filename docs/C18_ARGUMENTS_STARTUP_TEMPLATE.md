# C18 Arguments Startup Template

下面的内容用于新开会话，正式进入
`P4_Functions_and_Generators / C18_Arguments`。C18 是 P4 的 `normal` 章节；新会话
只正式推进 C18，不重启 C17，也不提前展开 C19-C21。

```text
<Subject>
当前新开会话的启动模板（可复用）：参数：调用合同、参数绑定与默认值边界
</Subject>

<Contents>
【阶段名称】
当前大阶段：学习 Python 的函数与生成器（Functions and Generators）

已完成的大阶段：
1. `P1_Getting_Started`（已完成）
2. `P2_Types_and_Operations`（已完成并通过收束验收）
3. `P3_Statements_and_Syntax`（C10-C15 已完成最终收束）

P4 已完成的小阶段：
1. `C16_Function_Basics`（`PART opener`，已完成最终收束）
2. `C17_Scopes`（`normal`，已完成最终收束）

C17 最终证据：
- 阶段测验 A1-F1 共 `11 / 11` 题逐题审批完成，稳定得分 `99.25 / 100`；
- 当前能力判断保持为“中级入门前段继续稳固，C17 作用域主干达到优秀，能够用
  名字—作用域—对象—控制流四层模型审查小型函数状态与配置边界”；
- C17 preparation、有限正式主线、阶段测验、逐题审批、学习画像同步、阶段末笔记、
  optional follow-up 审核和最终收束均已完成；
- C17 没有排期 pre-quiz capstone，路线图中的作用域追踪器或配置函数候选没有被
  事后追认为已完成关卡；
- 阶段末笔记及耐久 follow-up 补充已写入
  `notes/P4_Functions_and_Generators.md`；后续问答没有新增证据要求改变既定分数或
  能力判断；
- 本章工件与考卷保留在
  `practice/P4_Functions_and_Generators/C17_Scopes/`。

P4 章级路线背景：
1. `C16_Function_Basics`（已关闭，`PART opener`）
2. `C17_Scopes`（已关闭，`normal`）
3. `C18_Arguments`（当前章节，`normal`）
4. `C19_Advanced_Function_Topics`（`normal`）
5. `C20_Comprehensions_Revisited_and_Generators`（`normal`）
6. `C21_Benchmarking_and_Function_Pitfalls`（`PART closer`）

当前小阶段：`C18_Arguments`

正式标题：调用合同与参数绑定

章节角色：`normal`

角色依据：
- `docs/PYTHON_LEARNING_ROADMAP.md` 的 P4 章级路线明确把 C16 定位为
  `PART opener`、C18 定位为 `normal`、C21 定位为 `PART closer`；
- 来源索引按 C17 -> C18 -> C19 排列，C18 位于已经关闭的作用域章节与后续高级
  函数专题之间；
- C18 承接 C16 的调用时间线、C17 的局部名字与绑定模型、P2 的可变性和 C11 的
  解包模型，为 C19 的高阶函数合同与 C20 的可组合管线建立稳定接口；
- 本章既不打开新的 PART，也不关闭 P4，因此该角色来自持久路线和相邻依赖，而不是
  仅凭章节编号猜测。

本章计划关卡：
`preparation -> mainline -> quiz_authoring -> quiz_answering -> quiz_review -> stage_note -> final_closeout`

当前 capstone 状态：**未安排**。

路线图中的“带 keyword-only 控制项的本地化审计函数与参数绑定矩阵”仍只是阶段
检查点候选；P4 的“可组合函数管线 + 可复现实验/基准报告”也仍是候选成果。它们都
不是 C18 已排期的 pre-quiz capstone。C18 默认主线出口为：
`mainline 100% -> stage quiz`。只有本模板被明确更新或用户以后明确改变范围，才可
插入 capstone 关卡。

---

【我当前的位置】
✔ 已掌握：
- 能按“执行 `def` -> 创建函数对象并绑定名字 -> 调用 -> 本次调用的局部状态 ->
  正常返回/异常 -> 调用者继续”追踪对象和控制流；
- 能区分函数对象、调用表达式、调用结果、形参局部重新绑定和传入可变对象的原地
  修改；
- 能把名字、绑定、命名空间、作用域和查找拆开，按真实词法结构追踪 LEGB、局部
  分类、运行期是否已绑定及 `UnboundLocalError`；
- 能精确说明 `global` / `nonlocal` 的绑定目标，并区分跨作用域重绑与共享对象
  修改；
- 能限制签名、`Signature.bind()`、注解、`locals()` / `globals()` 和单次实验
  各自的证明范围；
- 能用显式参数和结构化返回让配置选择、输入依赖及副作用归属更可见。

❗ 不确定 / 模糊：
- 需要系统区分调用端实参表达式、函数定义中的形参，以及成功调用后建立的局部参数
  绑定；
- 需要按完整顺序追踪“调用目标与实参求值 -> `*` / `**` 输入展开与装配 ->
  按签名匹配 -> 建立形参绑定 -> 执行函数体”，并区分各阶段的异常和已发生副作用；
- 需要系统掌握 positional-only、positional-or-keyword、var-positional、
  keyword-only 和 var-keyword 五类参数及其排列边界；
- 需要精确解释位置参数、关键字参数、缺失参数、重复赋值、未知关键字和过多位置
  实参何时触发 `TypeError`；
- 需要区分定义端 `*args` / `**kwargs` 的收集与调用端 `*iterable` /
  `**mapping` 的解包；
- 需要系统理解默认表达式的求值时机、函数对象保存的默认对象、调用时省略实参的
  绑定，以及可变默认值为何跨调用共享状态；
- 需要用 `/` 和 `*` 表达 positional-only / keyword-only API 意图，并判断它们
  何时提高调用合同清晰度；
- C17 optional follow-up 已接触默认值固定对象引用和循环闭包晚绑定的入口，但这不
  等于 C18 参数系统已经掌握；循环回调与系统闭包设计仍留给 C19。

❌ 卡住的问题：
- 暂无阻止进入 C18 的核心问题；
- C17 测验的三个轻微精修点不是主干缺失，但应迁移到参数过程：调用已经开始不等于
  绑定已完成；参数绑定必须对应真实名字；对象本身没有“属于某个参数”的作用域属性；
- 完整高阶函数、lambda、闭包晚绑定、递归和系统注解属于 C19，生成器属于 C20，
  基准与 P4 综合陷阱属于 C21；这些尚未学习是正常路线状态，不是 C18 的待补作业。

---

【当前小阶段目标】
📘 学习目标：
- 区分实参、形参、实参表达式求值、调用匹配和函数体中的局部参数绑定；
- 建立调用时间线：先求值调用目标与实参表达式并处理解包，再按签名匹配；只有匹配
  成功，才建立本次调用的形参绑定并执行函数体；
- 掌握位置参数、关键字参数及五类参数的匹配规则、排列约束和主要失败路径；
- 掌握默认表达式的定义时求值、函数对象保存默认对象、调用时使用默认值的机制；
- 用对象身份、修改与重绑模型解释可变默认值陷阱，并选择按调用创建新对象的修复；
- 区分定义端 `*args` / `**kwargs` 收集与调用端 `*` / `**` 解包；
- 掌握 `/` positional-only 和 `*` keyword-only 的现代函数签名；
- 用参数合同设计小型显式接口，并限制 `inspect.signature()` /
  `Signature.bind()` 的证据强度。

🧠 理解深度：
- 保底：能写出并调用包含位置、关键字、默认值、`*args` 与 `**kwargs` 的函数，
  正确判断常见绑定结果和 `TypeError`；
- 进阶：能按“实参求值 -> 展开 -> 匹配 -> 建立局部绑定 -> 函数体”追踪对象、
  控制流和失败阶段，并解释默认对象的生命周期；
- 最好：能使用 positional-only / keyword-only 设计清晰接口，区分调用形状、
  运行期行为和业务合同，并为可变输入、默认状态及转发边界建立可验证规则；
- normal 章节要求：只完成 C18 的参数绑定主线，不承担 P4 开篇或收束职责。

C18 有限主线：

必学核心：
1. 实参与形参、实参表达式求值和本次调用局部绑定；
2. 参数种类、签名排列及 positional-only / keyword-only 边界；
3. 位置/关键字匹配，以及缺失、重复、未知和过量实参的失败路径；
4. 默认表达式的求值时机、默认对象存储和省略实参时的绑定；
5. 可变默认值的共享原因、风险和按调用创建状态的修复；
6. 定义端 `*args` / `**kwargs` 收集及其获得的对象结构；
7. 调用端 `*iterable` / `**mapping` 解包、求值顺序和冲突边界；
8. 参数绑定矩阵、API 合同设计，以及签名观察工具的有限证据。

必要补救：
- 不把“调用表达式已经开始求值”说成“所有形参绑定已经完成”；
- 实参表达式求值失败时，不能描述成已经进入被调函数体；匹配失败时也不执行函数体；
- 记录失败前已经发生的实参表达式副作用，不把 `TypeError` 说成自动回滚；
- 不把参数绑定解释成复制实参对象，也不把对象说成“局部对象”或“属于形参”；
- 不把调用者局部作用域当成被调函数的 enclosing 层；形参是本次调用的 local 名字；
- 不把可变默认值问题解释成 `global` / `nonlocal`，而应追踪定义时保存并跨调用
  复用的默认对象；
- 不把 `*args` / `**kwargs` 的定义端收集与调用端解包混成同一个动作；
- 不把 `Signature.bind()` 成功提升为函数体、类型、异常、副作用或业务合同成功。

可选拓展：
- `__defaults__`、`__kwdefaults__`、`inspect.Parameter` 和
  `Signature.bind_partial()` 的进一步观察；
- 当 `None` 本身是合法业务值时，使用专用 sentinel 区分“未提供”；
- 多组 `*` / `**` 展开的复杂求值与错误顺序；
- 小型参数转发函数的额外观察。

可选拓展不影响主线完成度，也不能反向增加阶段测验必考范围。完整高阶函数、lambda、
循环闭包晚绑定、递归、`functools.partial` 的系统设计和函数注解属于 C19；生成器
属于 C20；基准和 P4 综合陷阱属于 C21。

🛠 实践目标：
- preparation 阶段只在 `practice/P4_Functions_and_Generators/C18_Arguments/`
  下建立 C18 README 与计划内、彼此独立的正式编号实验；本模板生成时不预先创建
  这些工件；
- 实验应有限覆盖：
  1. 实参求值、调用匹配与形参局部绑定；
  2. 位置/关键字参数及常见 `TypeError`；
  3. 默认值和可变默认值；
  4. `*args` / `**kwargs` 定义端收集；
  5. `*` / `**` 调用端解包、冲突和失败前效果；
  6. positional-only、keyword-only 与有限签名观察；
- 使用 `.venv-py314` 执行 `py_compile`、代表性运行和 Markdown 检查；
- 可以只读、静态参考
  `projects/P3_Statements_and_Syntax/prompt_template_manager/` 中真实签名，例如
  `prompt_store.py` 的 `list_records(*, ...)`、`add_record(*, ...)`、
  `update_record(record_id, *, ...)`，`prompt_manager_cli.py` 的
  `print_record(record, *, show_content=True)`，以及 `import_test_demo.py` 的
  `parse_prompt_source(source_path=..., *, skip_header_lines=None)`；
- 工程背景只用于观察参数合同和 API 取舍，不导入或运行会连接、初始化、迁移、查询
  或修改 SQLite 的函数，不执行 CRUD、CLI 或 GUI，不修改该项目，也不让它替代
  自包含实验、当前模板或扩大 C18 必学范围；
- 本章后期阶段测验只覆盖 C18 必学核心与必要补救；阶段末笔记继续追加到 P4 笔记，
  不在 preparation 中抢跑；
- 不创建 P4 capstone，不创建 C19-C21 练习文件，不操作 `tests/`。

---

【你回答时的要求】
- 新会话开始前完整重读磁盘中的全局和项目 `AGENTS.md`，确认当前安全边界、允许
  编辑路径、禁止操作、sandbox-helper 编辑规避路径、弹窗停机规则和 `tests/`
  硬排除；
- 读取本模板、`docs/PYTHON_LEARNING_ROADMAP.md`、
  `docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`、
  `notes/Python_Learning_Profile.md`、`notes/P4_Functions_and_Generators.md`、
  C17 README 与阶段测验批改记录；
- 本模板是 C18 课程范围、必学结果和节奏的唯一权威入口；路线图和画像负责背景与
  难度校准，同主题脚本、项目和来源摘录只能作为运行锚点、风格参考或完成证据；
- 先核实 C18 的 `normal` 角色，再做 preparation；只推进当前 CHAPTER；
- preparation 轮只创建并验证计划内 C18 学习工件，不在同一轮顺带开始正式主线；
- 正式主线采用最新版 stepwise teaching mode：每一步必须是一节内容完整的小课，
  教学是主体，深度同时依据主题难度和当前表现调整；
- 维护“必学核心 / 必要补救 / 可选拓展”的有限地图；只以前两者决定下一关卡，不因
  好奇追问、相邻项目或真实工程签名无限扩张完成分母；
- 选答题只在有定位价值时使用，并明确可跳过、不影响继续；跳过后在下一主课前主动
  给出最小必要收束，不要求补答，也不把跳过视为掌握不足；
- 仅在有定位价值的主线检查点显示 `主线学习进度：约 N%`；若同一步还有预告和
  选答题，顺序必须是完整教学 -> 进度 -> 下一主题预告 -> 选答题；
- preparation、测验、批改、笔记、最终收束和启动模板生成阶段不显示主线进度；
- required core 与必要补救达到关卡后，默认进入阶段测验；只有当前权威模板被更新
  或用户明确排期 capstone，才插入该关卡；
- 对细小但会模糊边界的偏差也要显式纠正，持续区分实参/形参、表达式求值/绑定完成、
  收集/解包、对象传递/对象复制、调用形状/函数行为、语言合同/当前实验；
- 核心例子优先使用本地化记录、配置选项、日志控制项、JSON/CSV 路径和小型纯函数；
  可运行实验使用 Python `3.14.5`，验证稳定语义而不是偶然显示格式；
- 不在 C18 系统教授高阶函数、lambda、循环闭包晚绑定、递归、函数注解、生成器或
  基准；这些按路线分别留给 C19-C21；
- 上下文压缩前按最新版生命周期协议生成续作检查点，保留章节角色、phase、有限主线
  游标、选答状态、关卡、下一原子动作、安全规则、验证证据和 dirty-worktree 事实；
- C18 最终收束时只生成 C19 的下一章启动模板并建议另开会话，不在同一会话开始 C19；
- 禁止使用内置 `apply_patch`、Edit 或 Write；需要编辑时必须遵循磁盘最新
  `AGENTS.md`，使用既定的 Base64 传输、`.venv-py314` Python subprocess 和官方
  本地 patch engine；本地 patch engine 缺失或失败时立即停止，不得切换到被禁路径；
- 若出现 `codex-windows-sandbox-setup.exe` 弹窗，或工具结果包含
  `orchestrator_helper_launch_canceled`、`ShellExecuteExW`、错误 `1223`，
  立即停止后续工具调用，记录时间和触发操作，等待用户关闭或确认；
- 不使用 `view_image` 查看本地图片，不批量删除文件，不操作 `tests/`，不清理
  无关 dirty worktree，不未经明确授权同步用户级 Codex memory。

---

【补充】
- 当前操作系统：Windows 11；
- 当前项目路径：`D:\MySoftwareDownload\PythonPractice\LearningPython5E`；
- 当前日常学习环境：仓库根目录 `.venv-py314`，实际解释器 Python `3.14.5`；
- 未激活环境时裸 `python` 仍可能指向历史 Python `3.9.13`，环境判断以
  `sys.version` 和 `sys.executable` 为准；
- 当前路线权威：`docs/PYTHON_LEARNING_ROADMAP.md`；
- 当前章节权威：`docs/C18_ARGUMENTS_STARTUP_TEMPLATE.md`；
- 来源索引：`docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`，只作追溯；
- 当前学习画像：`notes/Python_Learning_Profile.md`；
- P4 阶段笔记：`notes/P4_Functions_and_Generators.md`；
- C17 关闭证据：`practice/P4_Functions_and_Generators/C17_Scopes/README.md`
  与 `stage_quiz_scopes.md`；
- 可选工程背景：
  `projects/P3_Statements_and_Syntax/prompt_template_manager/`，仅限受控静态观察；
- 学习风格：重视本质、对象与名字、参数绑定时间线、控制流、证据来源、可运行实验、
  显式纠偏、工程边界和可复盘工件，质量与理解深度优先于速度。
</Contents>
```
