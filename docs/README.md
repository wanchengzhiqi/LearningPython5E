# Documentation Index

`docs/` 保存仓库级、跨阶段复用的说明文档。它不是章节笔记目录，也不是某个
综合项目的专属文档目录。

## Current Documents

- [`P3_STATEMENTS_AND_SYNTAX_STARTUP_TEMPLATE.md`](P3_STATEMENTS_AND_SYNTAX_STARTUP_TEMPLATE.md)：
  正式进入 `P3_Statements_and_Syntax` 的新会话启动模板。它从
  `C10_Introducing_Python_Statements` 开始，不是中断恢复锚点。
- [`C11_ASSIGNMENTS_EXPRESSIONS_AND_PRINTS_STARTUP_TEMPLATE.md`](C11_ASSIGNMENTS_EXPRESSIONS_AND_PRINTS_STARTUP_TEMPLATE.md)：
  进入 `P3_Statements_and_Syntax / C11_Assignments_Expressions_and_Prints`
  的新会话启动模板。它基于 C10 阶段小测和阶段笔记生成，只正式推进 C11。
- [`C12_IF_TESTS_AND_SYNTAX_RULES_STARTUP_TEMPLATE.md`](C12_IF_TESTS_AND_SYNTAX_RULES_STARTUP_TEMPLATE.md)：
  进入 `P3_Statements_and_Syntax / C12_if_Tests_and_Syntax_Rules` 的新会话
  启动模板。它基于 C11 阶段测验、阶段笔记和最新学习画像生成，只正式推进 C12。
- [`C13_WHILE_AND_FOR_LOOPS_STARTUP_TEMPLATE.md`](C13_WHILE_AND_FOR_LOOPS_STARTUP_TEMPLATE.md)：
  进入 `P3_Statements_and_Syntax / C13_while_and_for_Loops` 的新会话启动模板。
  它基于 C12 阶段测验、阶段笔记和最新学习画像生成，只正式推进 C13。
- [`C14_ITERATIONS_AND_COMPREHENSIONS_STARTUP_TEMPLATE.md`](C14_ITERATIONS_AND_COMPREHENSIONS_STARTUP_TEMPLATE.md)：
  进入 `P3_Statements_and_Syntax / C14_Iterations_and_Comprehensions` 的新会话
  启动模板。它基于 C13 阶段测验、阶段笔记、收束追问和最新学习画像生成，
  只正式推进 C14。
- [`C15_THE_DOCUMENTATION_INTERLUDE_STARTUP_TEMPLATE.md`](C15_THE_DOCUMENTATION_INTERLUDE_STARTUP_TEMPLATE.md)：
  进入 `P3_Statements_and_Syntax / C15_The_Documentation_Interlude` 的新会话
  启动模板。它承接 C14 的 `99 / 100` 阶段测验与阶段末记录，明确 C15 的
  `PART closer` 角色、有限主线以及阶段项目候选的显式决策关卡，只正式推进 C15。
- [`C16_FUNCTION_BASICS_STARTUP_TEMPLATE.md`](C16_FUNCTION_BASICS_STARTUP_TEMPLATE.md)：
  进入 `P4_Functions_and_Generators / C16_Function_Basics` 的新会话启动模板。
  它承接 P3 最终画像与收束结论，明确 C16 的 `PART opener` 角色，但只正式
  推进 C16，不把整个 P4 变成一次会话任务。
- [`C17_SCOPES_STARTUP_TEMPLATE.md`](C17_SCOPES_STARTUP_TEMPLATE.md)：
  进入 `P4_Functions_and_Generators / C17_Scopes` 的新会话启动模板。它承接
  C16 的 `99.75 / 100` 阶段测验、最终画像与阶段末笔记，明确 C17 的 `normal`
  角色、有限作用域主线和未排期 capstone 边界，只正式推进 C17。
- [`C18_ARGUMENTS_STARTUP_TEMPLATE.md`](C18_ARGUMENTS_STARTUP_TEMPLATE.md)：
  进入 `P4_Functions_and_Generators / C18_Arguments` 的唯一新会话启动模板。
  它承接 C17 的 `99.25 / 100` 稳定测验结论、最终画像与阶段末笔记，明确 C18
  的 `normal` 角色、有限参数绑定主线和未排期 capstone 边界，只正式推进 C18。
- [`LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md`](LEARNING_PYTHON_5E_REMAINING_OUTLINE_SOURCE.md)：
  保存用户提供的 P3-P8 目录来源摘录及其与定制路线的映射说明。它只负责来源
  追溯，不是课程路线权威。
- [`PYTHON_LEARNING_ROADMAP.md`](PYTHON_LEARNING_ROADMAP.md)：可动态调整的
  Python 后续学习路线图。每次跨越大阶段边界，或学习目标发生明显变化时，
  应结合最新学习画像复核。
- [`PYTHON_ENVIRONMENT_MIGRATION_PLAN.md`](PYTHON_ENVIRONMENT_MIGRATION_PLAN.md)：
  从 Python `3.9.13` 并行迁移到 Python `3.14.5` 的盘点、执行记录、日常
  使用边界与回归清单。
- [`REPOSITORY_RESTRUCTURE_PLAN.md`](REPOSITORY_RESTRUCTURE_PLAN.md)：仓库结构
  重构的历史执行记录。它最初用于处理中断恢复，现在保留为目录职责和验证
  基线的来源。

## Suitable Content

适合放入 `docs/`：

- 仓库治理规则与目录职责；
- 跨阶段路线图；
- 重要结构调整记录；
- 跨项目技术决策；
- 环境集成说明。

长任务如果再次遇到上下文压缩或额度边界，可以临时新增恢复锚点；任务完成后
应复核其长期价值，避免让过期续接模板长期占据文档索引。

不适合放入 `docs/`：

- 章节学习笔记：放入 `notes/`；
- 章节练习和预测题：放入 `practice/`；
- 单个综合项目的使用说明：放入项目自己的 `README.md`。
