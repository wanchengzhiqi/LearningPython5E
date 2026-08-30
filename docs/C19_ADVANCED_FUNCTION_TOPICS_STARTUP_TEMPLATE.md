# C19 Advanced Function Topics Startup Template

下面的内容用于新开会话，正式进入
`P4_Functions_and_Generators / C19_Advanced_Function_Topics`。C19 是 P4 的
`normal` 章节；新会话只正式推进 C19，不重启 C18，也不提前展开 C20-C21。

```text
<Subject>
当前新开会话的启动模板（可复用）：高级函数主题：组合、闭包、递归与注解
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
3. `C18_Arguments`（`normal`，已完成最终收束）

C18 最终证据：
- 阶段测验 A1-F1 共 `11 / 11` 题逐题审批完成，稳定得分 `99.25 / 100`；
- 既定能力判断保持为“中级入门前段已经稳固，C18 参数与调用合同主干达到优秀”，
  本次最终收束没有新增学习证据，因此没有改变分数或能力判断；
- C18 preparation、有限正式主线、测验生成、作答、逐题批改、学习画像同步、
  阶段末笔记和最终收束均已完成；
- C18 没有排期 pre-quiz capstone；参数绑定矩阵、本地化审计函数和 P4 函数管线
  候选均未被事后追认为已完成关卡；
- 实体书问答与后续专题属于 optional follow-up，没有发生也不影响 C18 关闭；
- C18 阶段末笔记已写入 `notes/P4_Functions_and_Generators.md`，本章工件和
  考卷保留在 `practice/P4_Functions_and_Generators/C18_Arguments/`。

P4 章级路线背景：
1. `C16_Function_Basics`（已关闭，`PART opener`）
2. `C17_Scopes`（已关闭，`normal`）
3. `C18_Arguments`（已关闭，`normal`）
4. `C19_Advanced_Function_Topics`（当前章节，`normal`）
5. `C20_Comprehensions_Revisited_and_Generators`（`normal`）
6. `C21_Benchmarking_and_Function_Pitfalls`（`PART closer`）

当前小阶段：`C19_Advanced_Function_Topics`

正式标题：组合、闭包、递归与注解

章节角色：`normal`

角色依据：
- `docs/PYTHON_LEARNING_ROADMAP.md` 的 P4 路线明确把 C16 定位为
  `PART opener`、C19 定位为 `normal`、C21 定位为 `PART closer`；
- 来源索引按 C18 -> C19 -> C20 排列，C19 位于已关闭的参数章节与后续生成器章节
  之间；
- C19 综合 C16 的函数对象与调用、C17 的作用域与闭包入口、C18 的参数合同，
  并为 C20 的生产者函数和 C21 的函数陷阱复盘建立组合基础；
- 本章既不打开新的 PART，也不关闭 P4；角色来自持久路线和相邻依赖，不是仅凭
  编号或标题猜测。

本章计划关卡：
`preparation -> mainline -> quiz_authoring -> quiz_answering -> quiz_review -> stage_note -> final_closeout`

当前 capstone 状态：**未安排**。

路线图中的“可组合规则注册表或本地化转换函数管线”只是阶段检查点候选，不是
C19 已排期的 pre-quiz capstone。C19 默认主线出口为：
`mainline 100% -> stage quiz`。只有本模板被明确更新或用户以后明确改变范围，
才可插入 capstone 关卡。

---

【我当前的位置】
✔ 已掌握：
- 能区分函数对象、函数名字与别名、调用表达式、返回对象和调用方后续绑定；
- 能按“`def` 执行—函数对象—名字绑定—调用—函数体—正常返回/异常”追踪
  控制流，并限制单次实验、签名和 `bind()` 的证据强度；
- 能按真实词法结构追踪 LEGB、free name、`global` / `nonlocal`、共享对象修改
  和跨作用域重绑，已经建立最小闭包入口；
- 能追踪五类参数、调用端装配、签名匹配、初始局部绑定、函数体执行、默认对象、
  收集/解包和异常前部分效果；
- 能用 positional-only、keyword-only 和封闭关键字合同设计小型显式 API；
- 能把名字/容器槽位与对象、对象身份与相等、原地修改与重新绑定分开描述。

❗ 不确定 / 模糊：
- C16 只建立了一等函数对象的基础观察，尚未系统学习把函数作为实参、返回值、
  回调和分派表成员来组合行为；
- C17 只建立闭包入口，尚未系统学习闭包读取 enclosing 绑定的时机、循环晚绑定、
  同一环境共享与不同工厂调用隔离；
- 需要比较默认参数、每轮工厂调用和 `functools.partial` 固定对象引用的不同合同，
  并明确它们都不自动深拷贝可变对象；
- 需要建立递归的基线条件、递归步骤、进展量与终止模型，并区分每次调用的独立局部
  绑定和可能共享的实参对象；
- 需要限定 `lambda` 的单表达式性质、适用范围，以及它与 `def` 共享的参数、
  作用域和晚绑定规则；
- 需要在 Python 3.14.5 下观察参数/返回注解和 `Callable` 基础，持续区分元数据
  意图、调用形状与运行期强制。

❌ 卡住的问题：
- 暂无阻止进入 C19 的核心问题；未系统学习高阶函数、闭包晚绑定、递归、lambda
  和注解是正常路线状态，不是补考或能力倒退；
- C18 的三项轻微精修应迁移到 C19：不要把回调注册和稍后调用压成“同时”，引用图
  坚持“名字/槽位 -> 对象”，每次调用的初始参数绑定与函数体内后续重绑分开记录；
- 呈现签名、注解、`Callable`、注册成功或一次真实调用都不能独自证明完整业务合同；
- 生成器属于 C20，基准与 P4 综合陷阱属于 C21，装饰器系统设计属于 P8/C39；
  这些不是 C19 的待补作业。

---

【当前小阶段目标】
📘 学习目标：
- 说明函数是一等对象，能把函数对象绑定给别名、放入容器、作为实参传入并作为
  返回值交给调用者，同时区分“传入函数对象”和“立即调用函数”；
- 建立有限高阶函数合同：接受函数、返回函数、注册回调、稍后调用、字典分派和
  简单转换管线，并追踪参数、返回、异常与副作用；
- 从 C17 的 free name 入口推进到完整闭包模型，解释 enclosing 绑定的持续可访问性、
  同一环境共享、不同工厂调用隔离和循环晚绑定；
- 比较晚绑定的常见修复：默认参数保存当时对象引用、每轮工厂调用建立独立
  enclosing 绑定；`functools.partial` 只作有限对照；
- 建立递归基线：基线条件、递归步骤、进展量、终止、每次调用的局部绑定和共享
  对象边界；能与显式循环作语义比较，但不进入性能基准；
- 掌握 `lambda` 是单表达式函数对象，能判断短小局部回调/排序键与多步骤业务逻辑
  的适用边界，并说明它没有特殊的“自动捕获值”语义；
- 观察参数/返回注解和 `Callable` 基础，把它们解释为有限元数据与设计意图，
  不当成 Python 自动执行的运行期类型强制；
- 用可组合规则、回调或转换管线设计小型工程接口，并保持证据强度与结论强度匹配。

🧠 理解深度：
- 保底：能识别函数对象被保存、传递、返回与调用的不同时间点；能写出有明确基线的
  简单递归，并正确解释 lambda 与注解的基本边界；
- 进阶：能画出闭包/回调的名字—对象—时间线，预测循环晚绑定，比较两种核心修复，
  并追踪递归调用的局部状态与异常传播；
- 最好：能设计小型分派表或转换管线，清楚写出回调形状、返回/异常/副作用合同，
  并限制注解、`Callable`、签名观察和单次运行的证据范围；
- normal 章节要求：只完成 C19 的高级函数有限主线，不承担 P4 开篇或收束职责。

C19 有限主线：

必学核心：
1. 函数的一等对象性质：别名、容器引用、作为实参和返回值，以及调用时机；
2. 高阶函数、回调、分派表与简单可组合转换管线；
3. 闭包环境、free name、共享与隔离，以及循环创建函数后的晚绑定；
4. 默认参数与每轮工厂调用两种核心晚绑定修复及其对象引用边界；
5. 递归的基线条件、递归步骤、进展量、终止和逐次调用状态；
6. lambda 的单表达式边界、适用范围及与 `def` 共享的语义；
7. 参数/返回注解、`__annotations__` 与 `Callable` 的有限元数据/形状证据；
8. 小型高阶 API 的参数、返回、异常、副作用和验证合同。

必要补救：
- 区分保存/注册函数对象和真正调用函数；容器里有 callable 不等于函数体已经执行；
- 不把闭包说成深拷贝外层值；应追踪内部函数对 enclosing 绑定的访问时机；
- 不把循环晚绑定说成 lambda 专属问题，也不把默认参数修复说成万能快照；
- 按阶段分开回调注册、外层函数返回、稍后调用、free name 读取和调用方结果绑定；
- 引用图统一从名字、容器槽位或闭包环境中的绑定指向函数/数据对象；
- 每次高阶或递归调用先记录初始参数绑定，再记录函数体内创建、修改与重绑；
- 不把注解、`Callable`、签名或 `callable()` 提升为类型、返回、异常、副作用或
  业务规则已经满足；
- 递归必须同时说明基线与每一步如何接近基线，不把“代码能继续调用自己”当成终止
  证明。

可选拓展：
- `__closure__` / cell 的有限观察；
- `functools.partial` 与更复杂签名表现；
- 当前解释器的递归深度限制观察；
- 更丰富的函数组合工具；
- 装饰器只作“接收并返回 callable”的入口预告。

可选拓展不影响主线完成度，也不能反向增加阶段测验必考范围。装饰器系统实现留给
P8/C39；生成器、`yield` 与暂停/恢复留给 C20；`timeit`、性能比较和 P4 综合
陷阱留给 C21；泛型、`ParamSpec`、Protocol、静态类型检查器和完整类型工程留给
PX1。

🛠 实践目标：
- preparation 阶段只在
  `practice/P4_Functions_and_Generators/C19_Advanced_Function_Topics/` 下建立
  C19 README 与计划内、彼此独立的正式编号实验；本模板生成时不预先创建这些工件；
- 建议用六个自包含实验有限覆盖：
  1. 一等函数、别名、容器引用与调用时机；
  2. 高阶转换、回调、分派表和简单组合；
  3. 闭包环境、共享状态与不同工厂调用；
  4. 循环晚绑定及默认参数/工厂/`partial` 对照；
  5. 递归基线、进展量、局部绑定与共享对象；
  6. lambda、参数/返回注解、`Callable` 与证据边界；
- 使用 `.venv-py314` 执行 `py_compile`、代表性运行和 Markdown 检查；
- 可以只读、静态参考
  `projects/P3_Statements_and_Syntax/prompt_template_manager/` 的真实函数对象边界：
  `prompt_manager_cli.py` 中 `set_defaults(func=command_...)` 与
  `args.func(args)`，以及 `prompt_manager_gui.py` 中 `command=self.some_method`、
  `command=lambda: ...` 和 `bind(..., lambda ...)`；
- 工程背景只用于观察函数对象、延迟调用、分派和有限 lambda；不得运行 GUI，
  不得导入或执行会连接、初始化、迁移、查询或修改 SQLite 的路径，不执行 CRUD、
  CLI 或 self-check，不进入 Tkinter/OOP/argparse 教学，也不修改该项目；
- 真实项目不完整覆盖闭包晚绑定、递归和 `Callable`，正式证据必须来自自包含实验；
- 本章后期阶段测验只覆盖 C19 必学核心与必要补救；阶段末笔记继续追加到 P4 笔记，
  不在 preparation 中抢跑；
- 不创建 C19 capstone，不创建 C20-C21 练习文件，不操作 `tests/`。

---

【你回答时的要求】
- 新会话开始前完整重读磁盘中的全局和项目 `AGENTS.md`，确认当前安全边界、允许
  编辑路径、禁止操作、sandbox-helper 编辑规避路径、弹窗停机规则和 `tests/`
  硬排除；
- 读取本模板、`docs/PYTHON_LEARNING_ROADMAP.md`、
  `docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`、
  `notes/Python_Learning_Profile.md`、`notes/P4_Functions_and_Generators.md`、
  C18 README 与阶段测验批改记录；
- 本模板是 C19 课程范围、必学结果和节奏的唯一权威入口；路线图和画像负责背景与
  难度校准，同主题脚本、项目和来源摘录只能作为运行锚点、风格参考或完成证据；
- 先核实 C19 的 `normal` 角色，再做 preparation；只推进当前 CHAPTER；
- preparation 轮只创建并验证计划内 C19 学习工件，不在同一轮顺带开始正式主线；
- 正式主线采用最新版 stepwise teaching mode：每一步必须是一节内容完整的小课，
  教学是主体，练习只作支持；深度同时依据主题难度和实际表现调整；
- 建立并维护“必学核心 / 必要补救 / 可选拓展”的有限地图；只以前两者决定下一
  关卡，不因真实项目、工具细节、好奇追问或可选函数式工具无限扩张完成分母；
- 已稳定的 C16-C18 基础可压缩；闭包晚绑定、递归轨迹和注解证据边界应按难度
  展开，遇到误解时缩小概念跳跃并增加可运行轨迹，而不是只增加题目；
- 选答题只在有定位价值时使用，并明确可跳过、不影响继续；若跳过，下一主课前主动
  给出最小必要收束，不要求补答，也不把跳过视为掌握不足；
- 仅在有定位价值的主线检查点显示 `主线学习进度：约 N%`；若同一步还有预告和
  选答题，顺序必须是完整教学 -> 进度 -> 下一主题预告 -> 选答题；
- preparation、测验、批改、笔记、最终收束和启动模板生成阶段不显示主线进度；
- required core 与必要补救达到关卡后，默认进入阶段测验；路线图候选不构成
  capstone，只有本模板被明确更新或用户明确排期才插入该关卡；
- 对细小但会模糊边界的偏差也要显式纠正，持续区分函数对象/函数调用、注册/执行、
  enclosing 绑定/值快照、默认参数保存引用/深拷贝、递归调用帧/共享实参对象、
  注解元数据/运行期强制、呈现合同/真实行为；
- 核心例子优先使用本地化转换规则、分派表、排序键、回调、配置解析和小型纯函数；
  可运行实验使用 Python `3.14.5`，验证稳定语义而不是偶然显示或实现细节；
- 不在 C19 系统教授装饰器、生成器、性能基准、完整静态类型系统、Tkinter/OOP、
  模块打包或异常专题；这些按路线留给后续章节或阶段；
- 上下文压缩前按最新版生命周期协议生成续作检查点，保留章节角色、phase、有限
  主线游标、选答状态、关卡、下一原子动作、安全规则、验证证据和 dirty-worktree
  事实；
- C19 最终收束时只生成 C20 的下一章启动模板并建议另开会话，不在同一会话开始
  C20；
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
- 当前章节权威：`docs/C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md`；
- 来源索引：`docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`，只作追溯；
- 当前学习画像：`notes/Python_Learning_Profile.md`；
- P4 阶段笔记：`notes/P4_Functions_and_Generators.md`；
- C18 关闭证据：`practice/P4_Functions_and_Generators/C18_Arguments/README.md`
  与 `stage_quiz_arguments.md`；
- 可选工程背景：
  `projects/P3_Statements_and_Syntax/prompt_template_manager/`，仅限受控静态观察；
- 学习风格：重视本质、名字与对象、调用时间线、闭包环境、递归进展、证据来源、
  可运行实验、显式纠偏、工程边界和可复盘工件，质量与理解深度优先于速度。
</Contents>
```
