# Python Learning Roadmap

更新时间：2026-08-27

## 1. 定位

这是一份可动态调整的 Python 学习路线图，不是对《Learning Python 5th
Edition》目录的机械复刻。

参考书仍然提供可靠的语言主线，但它主要面向 Python 3.3 时代的初学者。
当前路线需要同时考虑：

- 当前已经建立 Python `3.14.5` 日常学习环境，并保留 Python `3.9.13`
  历史回归环境；
- 已经通过 `P2_Types_and_Operations` 收束验收；
- 已形成对象模型驱动的学习方法；
- 需要逐渐补齐现代 Python 工程实践；
- 需要服务于未来 Python、C++、Java 和 AI 方向的长期成长。

## 2. 路线原则

1. **保留语言主干，不照搬旧目录。**
   书籍章节编号继续作为来源索引，但教学单元可以合并、拆分、前置或补充。
2. **继续使用对象模型解释路线。**
   每个新主题继续追问：创建了什么对象、名字绑定到哪里、协议如何工作、
   哪些变化发生在内存对象、文件、网络或进程边界。
3. **保持“概念 -> 小实验 -> 按需阶段项目 -> 测验 -> 笔记”的闭环。**
4. **工程化能力逐步加入。**
   不等读完整本书后才接触测试、类型标注、虚拟环境、打包、日志和并发。
5. **抽象必须有真实需求。**
   教学脚本可以保留重复实现作为阶段快照。只有出现至少两个独立调用方、
   行为契约稳定且能被验证时，才考虑把共享逻辑提取到仓库级 `src/`。

## 3. 环境现代化检查点

Python `3.9` 已结束官方支持，而 Windows 官方下载页当前列出的最新稳定
Python 3 版本是 Python `3.14.5`。
在正式开始 `P3` 前，已经单独安排并执行环境迁移检查：

1. 保留现有 Python `3.9.13` 环境，便于回看历史实验；
2. 已并行安装 Python `3.14.5` 并新建 `.venv-py314`；
3. 已用 `localization_resource_auditor` 和 `myimporter_system` 完成代表性命令行
   回归验证；
4. 暂不复制全局 `sitecustomize.py`，也不修改持久化 PATH；
5. 用户决定暂缓 PyCharm 升级；项目 SDK 已指向 `.venv-py314`，但 PyCharm
   `2023.3.5` 会显示为 `Python 3.10`，IDE 集成能力仍需用实际运行结果验证。

环境迁移是独立任务，不应和新章节第一批语法练习混在一起执行。
具体盘点、决策点和回归清单见
[`PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`](PYTHON_ENVIRONMENT_MIGRATION_PLAN.md)。

## 4. 定制后的主路线

| 路线顺序 | 大阶段 | 参考书来源 | 定制重点 | 推荐阶段成果 |
| --- | --- | --- | --- | --- |
| 1 | `P3_Statements_and_Syntax` | 原 P3，C10-C15 | 语句、表达式、赋值、条件、循环、迭代、推导式；补充 `match`；把文档工具融入日常，不把 C15 只当孤立章节 | 可配置的本地化批处理工作流 |
| 2 | `P4_Functions_and_Generators` | 原 P4，C16-C21 | 函数对象、LEGB、参数绑定、闭包、递归、函数注解、迭代器、生成器、性能测量；装饰器只做预告 | 将审计流程拆分成可组合函数管线 |
| 3 | `P5_Modules_and_Packages` | 原 P5，C22-C25 | 模块对象、命名空间、`__name__`、导入、包、相对导入、`sys.path`；补充 `venv`、`pip`、`pyproject.toml` 基础与可复用代码归属 | 把稳定能力整理成可导入包 |
| 4 | `P7_Exceptions_and_Tools` | 原 P7，C33-C36，前置学习 | 异常对象、抛出与捕获、异常链、资源释放、上下文管理器；补充 `unittest`、日志和失败路径设计 | 为既有工具建立可验证错误边界 |
| 5 | `P6_Classes_and_OOP` | 原 P6，C26-C32 | 类与实例、属性查找、组合与继承、真实领域建模、运算符重载；补充 `dataclass`、ABC 和协议意识 | 面向对象重构一个真实领域模型 |
| 6 | `PX1_Modern_Python_Engineering` | 现代补充阶段 | 类型标注、静态检查思维、测试组织、依赖管理、打包、配置、日志、CLI 设计、代码质量工具 | 一个可安装、可测试、可维护的小型包 |
| 7 | `P8_Advanced_Topics` | 原 P8，C37-C40 | Unicode/bytes 进阶回访、属性管理、描述符、装饰器、元类；全部学习，但控制深度，强调适用边界 | 对既有项目做高级机制观察与小范围应用 |
| 8 | `PX2_Concurrency_and_IO` | 现代补充阶段 | `subprocess`、线程、进程、`concurrent.futures`、`asyncio`、socket、网络 I/O、竞态与序列化边界 | 扩展并解释 `myimporter_system` 的进程与 RPC 边界 |
| 9 | `PX3_Professionalization_Capstone` | 综合阶段 | 架构、测试、类型、文档、发布、性能、错误处理、安全边界和跨语言视野 | 一个面向真实使用场景的完整 Python 项目 |

### 为什么调整顺序

- **异常阶段前置到 OOP 之前**：从函数和模块开始，程序已经需要清晰处理失败
  路径。异常、上下文管理器、测试和日志不应拖到类之后才系统学习。
- **Unicode 改为进阶回访**：`P2` 已经系统掌握 `str`、`bytes`、编码和文件边界。
  `P8` 不应从头重复，而应深入规范化、文件系统边界和复杂文本问题。
- **现代工程与并发单独补充**：旧书目录不足以覆盖今天的 Python 工程基线。
- **元类必须学，但不追求滥用**：目标是理解框架和高级库的机制，而不是把元类
  当作日常首选工具。

## 5. 已完成大阶段：P3 章级路线与收束结论

`P3_Statements_and_Syntax` 已于 2026-07-26 完成最终收束。它没有退化成简单
语法背诵，而是把此前的对象模型迁移到“程序如何决定下一步执行什么”，并在 C15
进一步形成证据驱动的代码调查与自查方法。

学习会话继续保持章节级粒度：每个新会话只正式推进一个 `CHAPTER`。`PART`
和相邻章节用于提供路线背景；当前章节验收后，再为下一个章节生成启动模板并
另开会话。

| 小阶段 | 参考书来源 | 学习重点 |
| --- | --- | --- |
| `C10_Introducing_Python_Statements` | 原 C10 | 表达式与语句、缩进块、执行顺序、对象模型在语句层的延续 |
| `C11_Assignments_Expressions_and_Prints` | 原 C11 | 各类赋值、解包、增强赋值、链式赋值、表达式语句、输出流；继续区分原地修改与重新绑定 |
| `C12_if_Tests_and_Syntax_Rules` | 原 C12 | 真值测试、布尔短路、条件表达式、语法规则；补充 `match` 的适用边界 |
| `C13_while_and_for_Loops` | 原 C13 | `while`、`for`、`break`、`continue`、`else`、循环变量绑定、修改迭代对象的风险 |
| `C14_Iterations_and_Comprehensions` | 原 C14 | 可迭代对象、迭代器、生成器预告、推导式作用域、惰性与急切求值 |
| `C15_The_Documentation_Interlude` | 原 C15 | `help()`、`dir()`、文档字符串、官方文档检索；章节角色为 `PART closer`，作为 P3 收束专题整合 |

P3 阶段项目建议曾沿用游戏本地化语境：实现一个可配置的批处理工作流，用条件、
循环、迭代和推导式组织资源筛选、规则执行和摘要输出。它可以调用既有项目，
但不要为了复用而提前制造抽象层。

最终关卡结论是：该建议始终只是候选方向，从未被排期为 C15 的强制 pre-quiz
capstone。C15 实际按 `mainline -> stage quiz` 完成；
`prompt_template_manager` 继续作为 P3 支持性工程背景，不被事后追认为 capstone。
这是 P3 的历史完成结论，后续不得因为 C15 是 `PART closer` 而补造项目关卡。

## 6. 当前大阶段：P4 章级路线

`P4_Functions_and_Generators` 是 P3 收束后的当前大阶段。用户当初提供的 P3-P8
目录摘录已保存到
[`LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`](LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md)；
该文件只负责来源追溯，本路线图仍是定制课程的权威记录。

P4 的共同主线是把 P3 已掌握的执行、绑定、控制流、迭代与证据模型推进到函数
调用边界：

```text
def 执行并创建函数对象
    -> 名字与函数对象绑定
    -> 调用时建立参数与局部状态
    -> 按作用域解析名字
    -> return 把对象交给调用者
    -> 闭包、高阶函数与生成器保存或组合行为
    -> 用合同证据和可重复测量核验设计
```

| 小阶段 | 来源映射 | 章节角色 | 核心定位 |
| --- | --- | --- | --- |
| `C16_Function_Basics` | 原 C16 | `PART opener` | 函数对象、`def`、调用、函数体执行、显式/隐式 `return` 与副作用边界 |
| `C17_Scopes` | 原 C17 | `normal` | LEGB、局部/全局/内置名字、`global` / `nonlocal` 和闭包入口 |
| `C18_Arguments` | 原 C18 | `normal` | 实参与形参绑定、位置/关键字参数、默认值、收集与解包、可变默认值 |
| `C19_Advanced_Function_Topics` | 原 C19 | `normal` | 一等函数、高阶组合、闭包晚绑定、递归、lambda 与函数注解 |
| `C20_Comprehensions_Revisited_and_Generators` | 原 `C20_Comprehensions(Revisited)_and_Generations` | `normal` | 以 C14 为前置，新增生成器函数、`yield`、暂停帧、恢复点与单次消费 |
| `C21_Benchmarking_and_Function_Pitfalls` | 原 C21 | `PART closer` | 可重复基准、函数常见陷阱、P4 综合复核和下一 PART 交接 |

C16 的 `PART opener` 角色不是从编号猜测而来：C15 已明确关闭 P3 并留下函数对象、
参数绑定、名字解析、返回合同和注解边界五类交接问题；来源索引与本路线都把 C16
放在 P4 首位；而 C16 的函数对象与调用模型又是 C17-C21 的共同依赖根。

### 6.1 `C16_Function_Basics`：函数对象、调用与返回

- **定制重点**：`def` 语句执行时创建函数对象并绑定名字；函数对象、调用表达式与
  调用结果不是同一对象；调用才执行函数体；显式 `return value`、裸 `return`、执行
  到末尾得到 `None`；返回对象、`print()`、原地修改和外部 I/O 是不同效果。
- **前后依赖**：承接 C10 的 `def` 时间线、C11 的绑定与输出/返回、C15 的合同证据；
  只建立参数与作用域问题入口，把完整 LEGB 留给 C17、完整参数绑定留给 C18。
- **现代补充**：可观察基本签名、docstring 和注解元数据，但继续强调注解不自动执行
  类型验证；系统注解设计留给 C19。
- **阶段检查点候选**：小型纯函数拆分与调用/返回轨迹实验，不是 P4 capstone。
- **完成状态**：已于 2026-08-03 完成最终收束并标记为 `closed`；阶段测验
  `11 / 11` 题逐题审批完成，稳定得分 `99.75 / 100`。本章没有排期 pre-quiz
  capstone，学习画像与 P4 阶段末笔记均已同步。

### 6.2 `C17_Scopes`：名字解析与闭包入口

- **定制重点**：LEGB、局部/全局/内置名字、嵌套函数、`global`、`nonlocal`、
  `UnboundLocalError`；继续区分名字重新绑定与所指对象的原地修改。
- **前后依赖**：以前一章的函数调用与局部状态为基础，为 C18 参数名字和 C19
  闭包/回调建立名字解析模型。
- **现代补充**：优先显式传递依赖，避免隐式全局可变状态；运行期命名空间观察仍须
  保留 C15 的“内省可能执行代码”边界。
- **阶段检查点候选**：作用域追踪器或不依赖全局可变状态的配置函数。
- **完成状态**：已于 2026-08-12 完成最终收束并标记为 `closed`；阶段测验
  `11 / 11` 题逐题审批完成，稳定得分 `99.25 / 100`。本章没有排期 pre-quiz
  capstone，学习画像与 P4 阶段末笔记均已同步；可选 follow-up 不改变完成分母。

### 6.3 `C18_Arguments`：调用合同与参数绑定

- **定制重点**：实参与形参的临时绑定、位置/关键字参数、默认值、`*args`、
  `**kwargs`、调用端解包、可变对象共享和可变默认值陷阱。
- **前后依赖**：承接 C16 调用、C17 局部作用域、P2 可变性和 C11 解包；为 C19
  高阶函数合同与 C20 可组合管线准备稳定接口。
- **现代补充**：系统加入 `/` positional-only 和 `*` keyword-only；可用
  `Signature.bind()` 辅助观察，但不把呈现签名或绑定成功提升为完整行为保证。
- **阶段检查点候选**：带 keyword-only 控制项的本地化审计函数与参数绑定矩阵。
- **完成状态**：已于 2026-08-27 完成最终收束并标记为 `closed`；阶段测验
  `11 / 11` 题逐题审批完成，稳定得分 `99.25 / 100`。本章没有排期 pre-quiz
  capstone，学习画像与 P4 阶段末笔记均已同步；可选 follow-up 未发生也不改变
  完成分母。
- **下一交接**：唯一下一章为 `C19_Advanced_Function_Topics`，入口为
  [`C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md`](C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md)；
  应另开新会话从 preparation 开始，不在 C18 收束中提前教学。

### 6.4 `C19_Advanced_Function_Topics`：组合、闭包、递归与注解

- **定制重点**：函数是一等对象；回调、分派表、闭包与晚绑定；递归的基线与终止；
  lambda 的有限适用范围；函数注解的元数据性质。
- **前后依赖**：综合 C16-C18，并为 C20 的生产者函数和 C21 的陷阱复盘提供函数
  组合基础。
- **现代补充**：首次系统加入参数/返回注解和 `Callable` 基础，但不把注解当成
  运行期强制；装饰器只作入口预告，系统学习仍留给 P8/C39。
- **阶段检查点候选**：可组合规则注册表或本地化转换函数管线。

### 6.5 `C20_Comprehensions_Revisited_and_Generators`：生成器函数状态

- **定制重点**：不重复 C14 的推导式基础；集中学习生成器函数、`yield`、暂停帧、
  恢复点、局部状态、`return` / `StopIteration`、生成器表达式与生成器函数的差异。
- **前后依赖**：以 C14 的迭代协议和单次消费为直接前置，并综合 C16-C19 的函数、
  作用域与参数模型；为 C21 比较急切/惰性方案准备等价工作负载。
- **现代补充**：`yield from` 作为小型委托机制；`send()` 等协程式接口只列为可选
  拓展，不提前转入异步或并发教学。
- **阶段检查点候选**：流式本地化记录处理管线及其与物化方案的语义对照。

### 6.6 `C21_Benchmarking_and_Function_Pitfalls`：P4 收束

- **定制重点**：`timeit` 与计时基本方法；正确性先于性能；复核可变默认值、晚绑定
  闭包、递归限制、生成器复用、过度抽象和注解误用。
- **前后依赖**：综合整个 P4；只建立模块/包边界的交接问题，不提前系统教授 P5。
- **现代补充**：`time.perf_counter()`、重复测量、代表值、热身与环境记录；明确微基准
  不能无条件外推生产性能，`cProfile` 只作可选入口。
- **阶段成果候选**：“可组合函数管线 + 可复现实验/基准报告”。它当前仍是候选，
  是否成为 C21 的 pre-quiz capstone 必须等权威路线或用户以后明确排期。

P4 仍按一个会话一个 `CHAPTER` 推进。本节只冻结 C16-C21 的章级路由与依赖，不把
整个 P4 变成一次会话任务，也不提前冻结 P5 以后的逐章教学细节。

## 7. 跨阶段专题

这些主题不必等待某一个专属大阶段才首次接触：

| 专题 | 首次系统加入位置 | 后续深化位置 |
| --- | --- | --- |
| 类型标注 | P4 函数注解 | PX1 静态检查与 API 契约 |
| 虚拟环境与依赖 | P5 包与项目组织 | PX1 可安装项目 |
| 测试与日志 | P7 异常和失败路径 | PX1 工程质量 |
| `pathlib`、JSON、CSV | 已在 P2 建立基础 | 后续项目持续使用 |
| `pickle`、`shelve`、`struct` | P2 扩展知识已初步接触 | P8/PX2 按安全与二进制边界深化 |
| 并发与网络 | `myimporter_system` 已有观察素材 | PX2 系统学习 |
| 仓库级公共 `src/` | P5 讨论归属规则 | PX1 有真实复用需求后再启用 |

## 8. 动态调整规则

路线图不是冻结合同。出现以下情况时，应复核并按需更新：

1. 一个大阶段结束；
2. 阶段测验暴露出反复出现的薄弱点；
3. 新项目对某个知识点提出真实需求；
4. Python 运行环境升级；
5. 职业目标发生变化；
6. 某个补充专题已经自然融入前置阶段，不再需要单独开设。

每次调整时，先读取：

1. `notes/Python_Learning_Profile.md`
2. 当前阶段测验和批改记录
3. 本路线图
4. 相关项目 README 与代码

然后再决定下一阶段目录、学习深度、练习脚本和综合项目。

完成小阶段收束、大阶段收束、路线调整、环境迁移、仓库重构或长期流程规则
改变后，还应按文档职责审计长期记录，只更新受影响的文件，避免仓库级说明、
路线图、学习画像和项目文档互相漂移。

## 9. 当前状态

- `P1_Getting_Started`：已完成。
- `P2_Types_and_Operations`：已通过收束验收。
- `P3_Statements_and_Syntax`：C10-C15 的正式主线、阶段测验、学习画像、阶段笔记
  和最终收束均已完成；C15 是 P3 的 `PART closer`，阶段测验建议得分
  `98 / 100`。
- P3 capstone 结论：没有排期强制 pre-quiz capstone；路线图中的本地化批处理
  工作流保持候选，`prompt_template_manager` 不被事后追认为 capstone。
- `P4_Functions_and_Generators`：已经正式开始。其 `PART opener`
  `C16_Function_Basics` 的正式主线、阶段测验、逐题审批、学习画像、阶段笔记和
  最终收束均已完成；稳定得分 `99.75 / 100`，生命周期状态为 `closed`。
- C16 capstone 结论：权威启动模板未安排 pre-quiz capstone；小型纯函数拆分、
  函数管线和实验/报告候选均未被事后追认为已完成关卡。
- `C17_Scopes` 的正式主线、阶段测验、`11 / 11` 题逐题审批、学习画像、
  阶段末笔记、可选 follow-up 审核和最终收束均已完成；稳定得分
  `99.25 / 100`，生命周期状态为 `closed`。
- C17 capstone 结论：权威启动模板未安排 pre-quiz capstone；作用域追踪器和配置
  函数候选均未被事后追认为已完成关卡。
- `C18_Arguments` 的正式主线、阶段测验、`11 / 11` 题逐题审批、学习画像、
  阶段末笔记和最终收束均已完成；稳定得分 `99.25 / 100`，生命周期状态为
  `closed`。
- C18 capstone 结论：权威启动模板未安排 pre-quiz capstone；参数绑定矩阵、
  本地化审计函数和 P4 函数管线候选均未被事后追认为已完成关卡。
- 当前交接方向：`C19_Advanced_Function_Topics`，正式标题“组合、闭包、递归与
  注解”，章节角色为 `normal`。唯一下一章入口为
  [`C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md`](C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md)；
  应另开新会话从 preparation 开始，只正式推进 C19。当前模板未安排 pre-quiz
  capstone，路线图中的规则注册表或本地化转换函数管线仍只是候选。
- 环境状态：保留旧 Python `3.9.13` 与 `.venv`；新增 Python `3.14.5` 与
  `.venv-py314`；后续日常学习默认使用 `.venv-py314`；PyCharm 升级暂缓，
  项目 SDK 已指向 `.venv-py314`，但旧 IDE 的版本标签不可信。
- P3 的 C10-C15 与 P4 的 C16-C18 启动模板继续作为历史课程入口保留；它们不替代
  当前 C19 模板，也不因章节关闭而改写为完成报告。

## 10. 官方参考

- [Python Developer's Guide: Status of Python versions](https://devguide.python.org/versions/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [`venv`: Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [`typing`: Support for type hints](https://docs.python.org/3/library/typing.html)
- [`unittest`: Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [`asyncio`: Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
- [PyPA: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
