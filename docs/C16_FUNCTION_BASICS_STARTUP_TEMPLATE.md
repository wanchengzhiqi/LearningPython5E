# C16 Function Basics Startup Template

下面的内容用于新开会话，正式进入
`P4_Functions_and_Generators / C16_Function_Basics`。C16 是 P4 的
`PART opener`；新会话只正式推进 C16，不把整个 P4 变成一次会话任务。

```text
<Subject>
当前新开会话的启动模板（可复用）：函数基础：函数对象、调用、返回与副作用边界
</Subject>

<Contents>
【阶段名称】
当前大阶段：学习 Python 的函数与生成器（Functions and Generators）

已完成的大阶段：
1. `P1_Getting_Started`（已完成）
2. `P2_Types_and_Operations`（已完成并通过收束验收）
3. `P3_Statements_and_Syntax`（C10-C15 已完成最终收束）

P3 最终证据：
- C15 是 P3 的 `PART closer`，阶段测验 11 / 11 题审批完成，建议得分
  `98 / 100`；
- C15 学习画像、阶段末笔记、长期记录职责审计和 P3 -> P4 路线协调均已完成；
- P3 没有排期强制 pre-quiz capstone；候选本地化批处理工作流未被事后追认为
  capstone；
- 实体书问答实际未发生，但 optional follow-up 不是收束关卡。

P4 章级路线背景：
1. `C16_Function_Basics`（当前章节，`PART opener`）
2. `C17_Scopes`（normal）
3. `C18_Arguments`（normal）
4. `C19_Advanced_Function_Topics`（normal）
5. `C20_Comprehensions_Revisited_and_Generators`（normal）
6. `C21_Benchmarking_and_Function_Pitfalls`（`PART closer`）

当前小阶段：`C16_Function_Basics`

章节角色：`PART opener`

角色依据：
- `docs/PYTHON_LEARNING_ROADMAP.md` 已完成 P4 的 C16-C21 章级协调，并把 C16
  明确定位为 P4 开篇；
- 用户提供的来源索引把 `C16_Function_Basics` 放在
  `P4_Functions_and_Generators` 首位；
- C15 的测验、画像和阶段笔记已经留下函数对象、参数绑定、名字解析、返回合同与
  注解边界五类交接问题；
- C16 的函数对象、调用和返回模型是 C17 作用域、C18 参数、C19 高阶函数、C20
  生成器和 C21 函数陷阱的共同依赖根，因此该角色不是仅凭章节编号猜测。

本章计划关卡：
`preparation -> mainline -> quiz_authoring -> quiz_answering -> quiz_review -> stage_note -> final_closeout`

当前 capstone 状态：**未安排**。

P4 的“可组合函数管线 + 可复现实验/基准报告”仍是阶段成果候选，不是 C16 已排期的
pre-quiz capstone。C16 默认主线出口为：`mainline 100% -> stage quiz`。不得因为
C16 是 PART opener 而自动增加项目关卡。

---

【我当前的位置】
✔ 已掌握：
- 当前能力处于“中级入门前段已经稳固”的位置，能用对象、控制流和证据分层独立
  审查小型 Python 数据流程与 API 合同；
- 能稳定区分表达式求值、语句执行、名字绑定、对象修改、返回对象、显示输出和外部
  副作用；
- 已能解释 `def` 语句执行与函数体调用不是同一时刻，但尚未在函数专题中系统展开；
- 能追踪真值、分支、循环退出、迭代器位置、惰性消费和推导式作用域；
- 能区分源码、docstring、对象元数据、人读帮助、签名呈现、官方公开承诺和当前
  实验；
- 遇到题干与源码冲突时，能按真实控制流拒绝错误前提并限定证明强度。

❗ 不确定 / 模糊：
- 需要系统区分函数对象、绑定到函数的名字、调用表达式和调用结果；
- 需要把“执行 `def`”与“调用时执行函数体”放进完整时间线；
- 需要精确解释显式 `return value`、裸 `return`、执行到函数末尾与 `None` 的关系；
- 需要继续区分函数返回值、`print()` 展示、参数对象原地修改、文件/数据库写入等
  不同效果；
- 需要建立实参与形参临时绑定的入口模型，但完整匹配规则留给 C18；
- 需要建立局部名字与调用状态的入口模型，但完整 LEGB 留给 C17；
- 函数注解和 `inspect.signature()` 是元数据/证据，不是 Python 自动执行的业务
  类型验证器；系统注解设计留给 C19。

❌ 卡住的问题：
- 暂无阻止进入 C16 的核心问题；
- C15 暴露的“运行期内省可能执行代码、临时目录不等于严格只读、JSON 文本不等于
  展示、哈希相等不是绝对证明”继续作为工程调查边界保留，但不扩张为 C16 必学主线；
- C17-C21 的作用域、完整参数、高阶函数、生成器和基准主题尚未系统学习，这是正常
  路线状态，不是 C16 的待补作业。

---

【当前小阶段目标】
📘 学习目标：
- 解释 `def` 是可执行语句：它创建函数对象，并把当前定义名绑定到该对象；
- 区分函数对象、函数别名、调用表达式、函数体执行和调用结果；
- 解释调用如何进入函数体，以及一条实际执行路径如何到达或绕过 `return`；
- 区分 `return value`、裸 `return`、无显式 `return` 和抛出异常；
- 把返回对象、打印/日志、参数对象修改和外部 I/O 分成不同合同维度；
- 观察函数是一等对象，可以被赋给其它名字、放入容器或作为对象传递，但不在本章
  提前系统展开高阶函数设计；
- 将 C15 的证据方法迁移到函数基础：从源码、函数对象、`__doc__`、签名和最小实验
  分别回答有限问题。

🧠 理解深度：
- 保底：能写出和调用简单函数，正确说明参数入口、返回值与隐式 `None`；
- 进阶：能按“定义 -> 绑定 -> 调用 -> 函数体 -> return/异常 -> 调用者继续”追踪
  对象与控制流；
- 最好：能为小型函数写清输入、返回、异常和副作用边界，并判断哪些观察来自语言
  语义、当前对象、文档或实验；
- PART opener 要求：承接 P3 的执行/绑定模型并建立 P4 共同词汇，但不把整个 P4
  一次性讲完。

C16 有限主线：

必学核心：
1. `def` 执行、函数对象创建与名字绑定；
2. 函数对象、别名、调用表达式和结果对象；
3. 调用时函数体执行与基本局部状态；
4. 显式/隐式 `return`、不可达路径、异常与调用者控制流；
5. 返回、展示、修改和外部副作用的合同分层；
6. 函数作为一等对象的基础观察，以及签名/docstring/注解的有限证据。

必要补救：
- 不把 `function` 与 `function()` 混为同一对象；
- 不把赋值或参数绑定默认解释成复制对象；
- 不把 `print()`、原地修改或持久化写入称为函数返回值；
- 不把注解、`callable()` 或签名检查提升为调用必然成功的完整合同。

可选拓展：
- `__name__`、`__qualname__`、`__defaults__`、`__annotations__`、`__code__` 等函数
  对象属性的进一步观察；
- 更底层的 frame/字节码细节；
- 额外真实项目源码走查。

可选拓展不影响主线完成度，也不能反向增加阶段测验必考范围。

🛠 实践目标：
- preparation 阶段只在
  `practice/P4_Functions_and_Generators/C16_Function_Basics/` 下建立 C16 README
  与计划内的独立可运行实验；本模板生成时不预先创建这些工件；
- 实验应覆盖函数对象与调用结果、别名绑定、调用/返回时间线、隐式 `None`、多路径
  `return`、返回与副作用分层，以及有限的 docstring/签名/注解观察；
- 使用 `.venv-py314` 执行 `py_compile`、代表性运行和 Markdown 检查；
- 可以把 `prompt_template_manager` 的已确认非持久化 helper 或既有审计函数作为
  只读工程背景，但不得调用数据库连接、初始化、迁移、CRUD、CLI 或 GUI，也不得
  让项目文件替代本模板或扩张 C16 范围；
- 本章后期阶段测验只覆盖 C16 必学核心与必要补救；阶段末笔记按 P4 的职责在届时
  建立或更新，不在 preparation 中抢跑；
- 不创建 P4 capstone，不创建 C17-C21 练习文件，不操作 `tests/`。

---

【你回答时的要求】
- 新会话开始前完整重读磁盘中的全局和项目 `AGENTS.md`，确认 sandbox-helper 编辑
  规避路径、弹窗停机规则、禁止操作和 `tests/` 硬排除；
- 读取本模板、`docs/PYTHON_LEARNING_ROADMAP.md`、
  `docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`、
  `notes/Python_Learning_Profile.md` 和 `notes/P3_Statements_and_Syntax.md`；
- 本模板是 C16 课程范围与节奏的唯一权威入口；路线图和画像负责背景/校准，同主题
  脚本、项目和来源摘录只能作锚点、风格参考或完成证据；
- 先核实 C16 的 `PART opener` 角色，再做 preparation；承接 P3 的最终画像和真实
  风险，但只推进当前 CHAPTER；
- preparation 轮只创建并验证计划内 C16 学习工件，不在同一轮顺带开始正式主线；
- 正式主线采用最新版 stepwise teaching mode：每一步是一节内容完整的小课，教学
  是主体，深度同时依据主题难度和当前表现调整；
- 维护有限主线地图，区分必学核心、必要补救和可选拓展；只以前两者决定下一关卡；
- 选答题只在有定位价值时使用，并明确可跳过、不影响继续；跳过后在下一主课前主动
  给出最小必要收束，不要求补答，也不把跳过视为掌握不足；
- 仅在有定位价值的检查点显示 `主线学习进度：约 N%`；若同一步还有预告和选答题，
  顺序必须是完整教学 -> 进度 -> 下一主题预告 -> 选答题；
- required core 与必要补救达到关卡后，默认进入阶段测验；只有权威路线或用户以后
  明确排期 capstone，才插入该关卡；
- 对细小但会模糊边界的偏差也要显式纠正，持续区分对象/名字、定义/调用、返回/展示、
  重新绑定/原地修改、合同/当前观察；
- 核心例子优先使用函数、日志、JSON/CSV、本地化记录和小型纯函数；可运行实验使用
  Python `3.14.5`，验证稳定语义而不是偶然显示格式；
- 不在 C16 系统教授完整 LEGB、复杂参数绑定、闭包应用、递归专题、生成器或基准；
  这些按路线分别留给 C17-C21；
- 上下文压缩前按最新版生命周期协议生成续作检查点，保留章节角色、phase、有限主线
  游标、选答状态、关卡、下一原子动作、安全规则、验证证据和 dirty-worktree 事实；
- C16 最终收束时只生成 C17 的下一章启动模板并建议另开会话，不在同一会话开始 C17；
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
- 当前章节权威：`docs/C16_FUNCTION_BASICS_STARTUP_TEMPLATE.md`；
- 来源索引：`docs/LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`，只作追溯；
- 当前学习画像：`notes/Python_Learning_Profile.md`；
- P3 收束笔记：`notes/P3_Statements_and_Syntax.md`；
- 学习风格：重视本质、对象与控制流、证据来源、可运行实验、显式纠偏、工程边界
  和可复盘工件，质量与理解深度优先于速度。
</Contents>
```
