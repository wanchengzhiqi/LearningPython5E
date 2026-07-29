# Learning Python 5th Edition 剩余目录来源摘录（P3-P8）

更新时间：2026-07-26

## 1. 文档定位

本文保存用户曾提供的《Learning Python 5th Edition》剩余目录摘录，用于追溯
P3-P8 的原始来源名称、层级、顺序和附注。

本文只是**用户提供的来源索引**，不是本仓库的课程路线权威。实际学习顺序、章节
拆分或合并、规范化名称、现代 Python 补充、章节角色和阶段成果，均以
[`PYTHON_LEARNING_ROADMAP.md`](PYTHON_LEARNING_ROADMAP.md) 及当前章节启动模板
为准。

来源追溯：

- 原始附件名称：`temp01.txt`；
- 会话记录：
  `C:\Users\天道酬勤\.codex\sessions\2026\05\22\rollout-2026-05-22T19-58-01-019e4f8c-b3ca-78a1-849c-ed183cedca93.jsonl`；
- 原始完整读取调用：JSONL 第 3007 行；
- 与该调用配对的 `function_call_output`：JSONL 第 3011 行，调用成功；
- 提取边界：从 `P3_Statements_and_Syntax:` 到 `C40_Metaclasses`；
- 完整性核对：6 个 PART、31 个章节，其中 P3/P4/P5/P6/P7/P8 分别为
  6/6/4/7/4/4 个章节。

这里的“完整”只表示与 JSONL 第 3011 行保存的完整读取结果一致；它不声称已经重新
读取或比对当前桌面上的原附件。

## 2. 用户提供的原始摘录

以下内容保留原始名称、注释、层级和顺序。本节不纠正拼写，也不把定制路线反向写入
来源文本。

```text
P3_Statements_and_Syntax:

C10_Introducing_Python_Statements
C11_Assignments_Expressions_and_Prints
C12_if_Tests_and_Syntax_Rules
C13_while_and_for_Loops
C14_Iterations_and_Comprehensions
C15_The_Documentation_Interlude


P4_Functions_and_Generators:

C16_Function_Basics
C17_Scopes
C18_Arguments
C19_Advanced_Function_Topics
C20_Comprehensions(Revisited)_and_Generations
C21_Benchmarking_and_Function_Pitfalls


P5_Modules_and_Packages:

C22_Modules(The Big Picture)
C23_Module_Coding_Basics
C24_Module_Packages
C25_Advanced_Module_Topics


P6_Classes_and_OOP:

C26_OOP(The Big Picture)
C27_Class_Coding_Basics
C28_A_More_Realistic_Example(Note: Dedicate an entire chapter to learning how to apply OOP (Object-Oriented Programming) principles to model the real world)
C29_Class_Coding_Details
C30_Operator_Overloading
C31_Designing_with_Classes
C32_Advanced_Class_Topics


P7_Exceptions_and_Tools:

C33_Exception_Basics
C34_Exception_Coding_Details
C35_Exception_Objects
C36_Designing_with_Exceptions


P8_Advanced_Topics(Note: The content identified as optional by the author of the reference book is considered compulsory for me):

C37_Unicode_and_Byte_Strings
C38_Managed_Attributes
C39_Decorators
C40_Metaclasses
```

## 3. 路线映射与调整记录

本节只解释来源索引与定制路线之间的差异；上面的原始摘录保持不变。

| 来源项 | 路线图采用项 | 映射或调整理由 |
| --- | --- | --- |
| `P3_Statements_and_Syntax` / C10-C15 | 保留已经完成的实际目录名与历史成绩 | P3 已按章完成；不为了重新统一大小写或命名而改写学习轨迹 |
| `P4_Functions_and_Generators` / C16-C19 | 原名保留 | 名称清楚且能与来源索引直接对应 |
| `C20_Comprehensions(Revisited)_and_Generations` | `C20_Comprehensions_Revisited_and_Generators` | 去除不利于目录使用的括号，并以 Python 的 generator 概念明确本章新增核心；“Revisited”保留其承接 C14 的含义 |
| `C21_Benchmarking_and_Function_Pitfalls` | 原名保留，角色明确为 P4 `PART closer` | 既保留来源可识别性，也承担 P4 基准核验、陷阱复盘和下一 PART 交接 |
| 来源中 P6 位于 P7 之前 | 定制路线仍把 P7 异常阶段前置到 P6 OOP 之前 | 从函数和模块开始就需要明确失败路径、资源释放、测试和日志边界；这是顺序调整，不是删除来源章节 |
| `P8_Advanced_Topics` 的括号附注 | C37-C40 继续全部保留为必学来源 | “原书 optional 不自动跳过”的用户意图被保留；具体深度、节奏和现代补充仍可在进入 P8 时调整 |
| `PX1`、`PX2`、`PX3` | 定制路线新增的现代工程、并发与综合阶段 | 旧书来源不足以覆盖今天的类型检查、测试、打包、依赖、日志、并发和发布基线 |
| P5-P8 的其它章节名 | 目前只作为远期来源索引 | 本轮只细化即将进入的 P4，不提前冻结 P5 以后的逐章教学设计 |

## 4. 使用规则

1. 选择下一章时，先读最新学习画像和
   [`PYTHON_LEARNING_ROADMAP.md`](PYTHON_LEARNING_ROADMAP.md)，再用本文核对来源位置。
2. 本文可以证明“用户当初提供了哪些来源条目”，不能证明某章必须按原顺序、原深度
   或原名称教学。
3. 任何新的合并、拆分、顺序调整、现代补充或章节角色变化，都应写入路线图的调整
   理由，而不是静默改写本来源摘录。
4. 一个新会话仍只正式推进一个 `CHAPTER`；PART 和远期条目只提供路线背景。
