# Python Learning Roadmap

更新时间：2026-06-03

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
3. **保持“概念 -> 小实验 -> 阶段项目 -> 测验 -> 笔记”的闭环。**
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

## 5. 下一大阶段：P3 细化建议

`P3_Statements_and_Syntax` 是下一步。它不应退化成简单语法背诵，而应把已经
掌握的对象模型迁移到“程序如何决定下一步执行什么”。

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
| `C15_The_Documentation_Interlude` | 原 C15 | `help()`、`dir()`、文档字符串、官方文档检索；作为 P3 收束专题整合 |

P3 阶段项目建议沿用游戏本地化语境：实现一个可配置的批处理工作流，用条件、
循环、迭代和推导式组织资源筛选、规则执行和摘要输出。它可以调用既有项目，
但不要为了复用而提前制造抽象层。

## 6. 跨阶段专题

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

## 7. 动态调整规则

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

## 8. 当前状态

- `P1_Getting_Started`：已完成。
- `P2_Types_and_Operations`：已通过收束验收。
- 跨阶段治理收束期已经完成：历史项目、仓库结构、路线图和 Python `3.14.5`
  命令行迁移已经完成。
- 当前大阶段：`P3_Statements_and_Syntax`，当前小阶段为
  `C10_Introducing_Python_Statements`。
- 环境状态：保留旧 Python `3.9.13` 与 `.venv`；新增 Python `3.14.5` 与
  `.venv-py314`；后续日常学习默认使用 `.venv-py314`；PyCharm 升级暂缓，
  项目 SDK 已指向 `.venv-py314`，但旧 IDE 的版本标签不可信。
- P3 启动模板：已生成并用于启动 `C10_Introducing_Python_Statements`。

## 9. 官方参考

- [Python Developer's Guide: Status of Python versions](https://devguide.python.org/versions/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [`venv`: Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [`typing`: Support for type hints](https://docs.python.org/3/library/typing.html)
- [`unittest`: Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [`asyncio`: Asynchronous I/O](https://docs.python.org/3/library/asyncio.html)
- [PyPA: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
