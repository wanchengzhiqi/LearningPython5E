# C17 Scopes Startup Template

下面的内容用于新开会话，正式进入
`P4_Functions_and_Generators / C17_Scopes`。C17 是 P4 的 `normal` 章节；新会话
只正式推进 C17，不重启 C16，也不提前展开 C18-C21。

```text
<Subject>
当前新开会话的启动模板（可复用）：作用域：LEGB、名字解析与闭包入口
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

C16 最终证据：
- 阶段测验 A1-F1 共 `11 / 11` 题逐题审批完成，稳定得分 `99.75 / 100`；
- 当前能力判断保持为“中级入门前段已经稳固，函数基础达到优秀”，没有新增证据要求
  改分或改变判断；
- C16 已完成 preparation、有限正式主线、测验生成、作答、逐题批改、学习画像同步、
  阶段末笔记和最终收束；
- C16 没有排期 pre-quiz capstone；路线图中的函数管线或实验候选没有被事后追认为
  已完成关卡；
- 实体书问答和后续专题属于 optional follow-up，未发生也不影响 C16 closed；
- 阶段笔记已写入 `notes/P4_Functions_and_Generators.md`，本章工件与考卷保留在
  `practice/P4_Functions_and_Generators/C16_Function_Basics/`。

P4 章级路线背景：
1. `C16_Function_Basics`（已关闭，`PART opener`）
2. `C17_Scopes`（当前章节，`normal`）
3. `C18_Arguments`（normal）
4. `C19_Advanced_Function_Topics`（normal）
5. `C20_Comprehensions_Revisited_and_Generators`（normal）
6. `C21_Benchmarking_and_Function_Pitfalls`（`PART closer`）

当前小阶段：`C17_Scopes`

正式标题：名字解析与闭包入口

章节角色：`normal`

角色依据：
- `docs/PYTHON_LEARNING_ROADMAP.md` 的 P4 章级路线明确把 C16 定位为
  `PART opener`、C17 定位为 `normal`、C21 定位为 `PART closer`；
- 来源索引按 C16 -> C17 -> C18 排列，C17 位于已经关闭的 opener C16 与后续参数
  章节 C18 之间；
- C17 承接 C16 的函数调用与本次调用局部状态，为 C18 的参数名字和 C19 的闭包/
  回调建立名字解析模型；
- 本章既不打开新的 PART，也不关闭 P4，因此该角色来自持久路线和相邻依赖，而不是
  仅凭章节编号猜测。

本章计划关卡：
`preparation -> mainline -> quiz_authoring -> quiz_answering -> quiz_review -> stage_note -> final_closeout`

当前 capstone 状态：**未安排**。

路线图中的“作用域追踪器或不依赖全局可变状态的配置函数”仍只是阶段检查点候选，
不是 C17 已排期的 pre-quiz capstone。C17 默认主线出口为：
`mainline 100% -> stage quiz`。只有本模板被明确更新或用户以后明确改变范围，才可以
插入 capstone 关卡。

---

【我当前的位置】
✔ 已掌握：
- 能按“执行 `def` -> 创建函数对象并绑定名字 -> 调用 -> 本次调用的局部状态 ->
  正常返回/异常 -> 调用者继续”追踪对象和控制流；
- 能区分函数对象、别名、调用表达式、返回对象、调用方赋值、共享对象原地修改和
  形参局部重新绑定；
- 能区分返回对象、显示、输出流写入、外部持久化和异常前部分效果，并理解异常不会
  自动回滚已经完成的副作用；
- 能限制 `callable()`、签名、`Signature.bind()`、docstring、注解和一次运行实验
  各自的证明强度；
- 已稳定掌握对象身份与值相等、对象修改与名字重新绑定等前置模型；
- 能主动指出题干、代码与证明范围之间的细小冲突，并用当前解释器做最小验证。

❗ 不确定 / 模糊：
- C16 的“本次调用局部名字”尚未扩展成完整名字解析规则；需要系统建立 LEGB 模型；
- 需要区分“读取一个名字时到哪里查找”和“赋值语句把名字绑定到哪个作用域”两套
  相关但不相同的规则；
- 需要解释为什么函数体中稍后出现赋值，可能让前面的同名读取触发
  `UnboundLocalError`，即使模块层存在同名对象；
- 需要系统区分 local、enclosing、global、builtins 名字以及遮蔽；
- 需要精确理解 `global` 与 `nonlocal` 改变的是名字绑定目标，不是把对象本身变成
  “全局对象”或“非局部对象”；
- 需要建立嵌套函数、free name 与闭包的入口模型，但完整闭包设计、晚绑定和高阶
  组合留给 C19；
- 需要谨慎观察 `locals()`、`globals()` 等命名空间映射，不把当前实现观察提升成
  任意场景都可可靠写回的合同。

❌ 卡住的问题：
- 暂无阻止进入 C17 的核心问题；
- C16 测验中的唯一轻微扣分是把 `StringIO` 的内容/位置语义外推给所有输出接收者；
  另有“字符串处理结果不等于无条件保证全新对象身份”的非扣分提醒。这两项作为证据
  精度纪律保留，不扩张成 C17 额外主线；
- 完整参数匹配、高阶函数与闭包晚绑定、生成器和基准尚未系统学习，是 C18-C21 的
  正常路线状态，不是 C17 的待补作业。

---

【当前小阶段目标】
📘 学习目标：
- 建立名字、绑定、命名空间和作用域之间的精确关系；
- 解释读取名字时的 LEGB 查找顺序，以及 local、enclosing、global、builtins 每一层
  的来源与遮蔽边界；
- 解释函数代码块如何判定局部名字，并能追踪 `UnboundLocalError` 的真实发生路径；
- 区分名字查找、名字重新绑定和对已找到对象的原地修改；
- 解释模块全局名字、内置名字和同名遮蔽，不把“全局”误写成跨模块普遍共享；
- 精确使用 `global` 和 `nonlocal`，说明它们分别改变哪个作用域中的绑定目标；
- 建立嵌套函数、enclosing/free name 和闭包保存外层绑定的入口模型；
- 把作用域模型迁移到工程设计：优先显式传递依赖，谨慎使用隐式全局可变状态，并为
  命名空间观察保留证据边界。

🧠 理解深度：
- 保底：能按 LEGB 判断一个读取表达式会从哪一层获得名字，并识别常见遮蔽；
- 进阶：能把局部名字判定、运行时绑定状态和 `UnboundLocalError` 放进完整执行轨迹，
  正确解释 `global` / `nonlocal`；
- 最好：能对嵌套函数和共享可变对象画出名字—作用域—对象关系图，并据此选择显式
  依赖传递、返回值、对象修改或受控非局部状态；
- normal 章节要求：只完成 C17 的名字解析主线，不承担 P4 开篇或收束职责。

C17 有限主线：

必学核心：
1. 名字、绑定、命名空间、作用域和名字查找不是同一个概念；
2. 函数局部名字判定、读取与绑定顺序，以及 `UnboundLocalError`；
3. LEGB：local、enclosing、global、builtins 的查找与遮蔽；
4. 模块全局名字、内置名字与“全局只属于当前模块”的边界；
5. `global`：把当前代码块中的相应名字绑定指向模块全局命名空间；
6. `nonlocal`：把当前代码块中的相应名字绑定指向最近的外层函数作用域；
7. 跨作用域重新绑定与共享对象原地修改的区别；
8. 嵌套函数、free name 与闭包入口，以及运行期命名空间观察的有限证据。

必要补救：
- 不把局部命名空间说成调用方命名空间或实参对象的复制；
- 不把名字的 LEGB 查找规则和赋值目标的作用域判定混成一条规则；
- 不用对象是否可变来解释一个名字为什么被判定为局部；
- 不把 `UnboundLocalError` 简化成“全局名字不存在”；
- 不把 `global` / `nonlocal` 说成改变对象的归属、类型或可变性；
- 不因能够修改模块层可变对象，就误认为任何情况都需要或已经使用 `global`；
- 不把 `locals()` / `globals()` 映射的当前观察提升成稳定的任意写回接口。

可选拓展：
- 函数的 `__closure__`、cell 对象和更底层的符号表/字节码观察；
- 更复杂的闭包状态、晚绑定陷阱和回调设计；
- 额外真实项目源码走查。

可选拓展不影响主线完成度，也不能反向增加阶段测验必考范围。完整参数绑定属于 C18；
闭包晚绑定、高阶函数、递归和系统注解属于 C19；生成器属于 C20；基准和 P4 综合陷阱
属于 C21。

🛠 实践目标：
- preparation 阶段只在 `practice/P4_Functions_and_Generators/C17_Scopes/` 下建立
  C17 README 与计划内、彼此独立的可运行实验；本模板生成时不预先创建这些工件；
- 实验应覆盖 LEGB 与遮蔽、局部名字判定和 `UnboundLocalError`、模块全局名字、
  `global`、`nonlocal`、跨作用域修改对象与重新绑定名字、嵌套函数/free name/闭包
  入口，以及有限命名空间观察；
- 使用 `.venv-py314` 执行 `py_compile`、代表性运行和 Markdown 检查；
- 真实工程背景只用于解释适用边界：`prompt_template_manager` 最多静态观察模块常量和
  函数读取模块名字；C16 的合同卡或 `run_gate` 材料最多作为函数/模块边界背景；
- `prompt_template_manager` 当前源码不能被硬包装成完整 `global` / `nonlocal` 教材；
  显式作用域机制应优先使用自包含合成实验；
- 不连接、初始化、迁移或修改 SQLite，不运行 CRUD、CLI 或 GUI；不让任何相邻项目
  或辅助工件替代本模板、扩大必学范围或升级为 capstone；
- 本章后期阶段测验只覆盖 C17 必学核心与必要补救；阶段末笔记继续追加到 P4 笔记，
  不在 preparation 中抢跑；
- 不创建 P4 capstone，不创建 C18-C21 练习文件，不操作 `tests/`。

---

【你回答时的要求】
- 新会话开始前完整重读磁盘中的全局和项目 `AGENTS.md`，确认 sandbox-helper 编辑
  规避路径、弹窗停机规则、禁止操作和 `tests/` 硬排除；
- 读取本模板、`docs/PYTHON_LEARNING_ROADMAP.md`、
  `docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`、
  `notes/Python_Learning_Profile.md`、`notes/P4_Functions_and_Generators.md`、C16 本章
  README 与阶段测验批改记录；
- 本模板是 C17 课程范围、必学结果和节奏的唯一权威入口；路线图和画像负责背景与
  难度校准，同主题脚本、项目和来源摘录只能作为运行锚点、风格参考或完成证据；
- 先核实 C17 的 `normal` 角色，再做 preparation；只推进当前 CHAPTER；
- preparation 轮只创建并验证计划内 C17 学习工件，不在同一轮顺带开始正式主线；
- 正式主线采用最新版 stepwise teaching mode：每一步必须是一节内容完整的小课，
  教学是主体，深度同时依据主题难度和当前表现调整；
- 维护“必学核心 / 必要补救 / 可选拓展”的有限地图；只以前两者决定下一关卡，不因
  好奇追问或工程背景无限扩张完成分母；
- 选答题只在有定位价值时使用，并明确可跳过、不影响继续；跳过后在下一主课前主动
  给出最小必要收束，不要求补答，也不把跳过视为掌握不足；
- 仅在有定位价值的主线检查点显示 `主线学习进度：约 N%`；若同一步还有预告和选答
  题，顺序必须是完整教学 -> 进度 -> 下一主题预告 -> 选答题；
- preparation、测验、批改、笔记、最终收束和启动模板生成阶段不显示主线进度；
- required core 与必要补救达到关卡后，默认进入阶段测验；只有当前权威模板被更新
  或用户明确排期 capstone，才插入该关卡；
- 对细小但会模糊边界的偏差也要显式纠正，持续区分名字/对象、查找/绑定、作用域/
  生命周期、重新绑定/原地修改、语言语义/当前实现观察；
- 核心例子优先使用嵌套函数、配置读取、本地化记录、日志和小型纯函数；可运行实验
  使用 Python `3.14.5`，验证稳定语义而不是偶然显示格式；
- 不在 C17 系统教授完整参数匹配、闭包晚绑定与高阶组合、递归专题、生成器或基准；
  这些按路线分别留给 C18-C21；
- 上下文压缩前按最新版生命周期协议生成续作检查点，保留章节角色、phase、有限主线
  游标、选答状态、关卡、下一原子动作、安全规则、验证证据和 dirty-worktree 事实；
- C17 最终收束时只生成 C18 的下一章启动模板并建议另开会话，不在同一会话开始 C18；
- 文件编辑必须遵循当前 `AGENTS.md` 的 sandbox-helper 规避路径；若出现弹窗、
  `orchestrator_helper_launch_canceled`、`ShellExecuteExW` 或错误 1223，立即停机；
- 不使用被禁止的本地图片查看路径，不操作 `tests/`，不未经明确授权同步用户级
  Codex memory。

---

【补充】
- 当前操作系统：Windows 11；
- 当前项目路径：`D:\MySoftwareDownload\PythonPractice\LearningPython5E`；
- 当前日常学习环境：仓库根目录 `.venv-py314`，实际解释器 Python `3.14.5`；
- 未激活环境时裸 `python` 仍可能指向历史 Python `3.9.13`，环境判断以
  `sys.version` 和 `sys.executable` 为准；
- 当前路线权威：`docs/PYTHON_LEARNING_ROADMAP.md`；
- 当前章节权威：`docs/C17_SCOPES_STARTUP_TEMPLATE.md`；
- 来源索引：`docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`，只作追溯；
- 当前学习画像：`notes/Python_Learning_Profile.md`；
- P4 阶段笔记：`notes/P4_Functions_and_Generators.md`；
- C16 关闭证据：`practice/P4_Functions_and_Generators/C16_Function_Basics/README.md`
  与 `stage_quiz_function_basics.md`；
- 学习风格：重视本质、对象与名字、执行轨迹、证据来源、可运行实验、显式纠偏、工程
  边界和可复盘工件，质量与理解深度优先于速度。
</Contents>
```
