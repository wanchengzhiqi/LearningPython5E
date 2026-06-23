# C12 if Tests and Syntax Rules

本目录正式推进
`P3_Statements_and_Syntax / C12_if_Tests_and_Syntax_Rules`。

本章以
`docs/C12_IF_TESTS_AND_SYNTAX_RULES_STARTUP_TEMPLATE.md` 的“实践目标”为正式
教学入口，并结合
`projects/P3_Statements_and_Syntax/prompt_template_manager/` 的真实条件分支。
项目代码提供工程背景，但不会反过来改变本章顺序。

## 核心分析链

```text
测试表达式先求值
    -> 得到一个对象
    -> 对象按真值协议参与测试
    -> 短路、比较或分支规则决定后续哪些表达式还会求值
    -> if / elif / else 选择代码块
    -> 只有实际求值或实际进入的路径才会产生副作用
```

尤其要守住四条边界：

- `if value:` 不是 `if value == True:`；前者是真值测试，后者先做相等性比较。
- `and` / `or` 通常返回操作数对象，不保证返回 `bool`；`not` 返回 `bool`。
- `==` 判断相等性，`is` 判断身份；普通业务值通常使用 `==`。
- 条件表达式产生一个值，`if` 语句选择一个代码块。

## 使用方式

先停在每个 `[Predict]`，预测求值顺序、结果对象、控制流和副作用，再运行脚本。

```powershell
.\.venv-py314\Scripts\Activate.ps1
python --version

python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\01_truth_testing_objects_and_protocols.py
python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\02_short_circuit_operand_results.py
python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\03_comparisons_identity_and_membership.py
python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\04_comparison_chains_evaluation_order.py
python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\05_if_elif_else_branch_selection.py
python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\06_conditional_expressions_and_readability.py
python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\07_localization_rule_decision_pipeline.py
python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\08_prompt_manager_conditions_and_match_boundaries.py
```

实际解释器应为 Python `3.14.5`。不要用未激活环境时指向 Python `3.9.13`
的裸 `python` 误判当前学习结果。

## 正式实验地图

1. `01_truth_testing_objects_and_protocols.py`
   - 数值、字符串、容器和 `None` 的真值；
   - 对象本体与真值测试结果；
   - `__bool__()`、`__len__()`、优先级和错误边界。

2. `02_short_circuit_operand_results.py`
   - `and` / `or` 返回哪个操作数；
   - 右侧调用、副作用和异常如何被短路；
   - `not` 为什么始终返回 `bool`。

3. `03_comparisons_identity_and_membership.py`
   - 比较表达式的布尔结果；
   - `==` / `!=` 与 `is` / `is not`；
   - 字典、字符串、列表和集合的成员测试。

4. `04_comparison_chains_evaluation_order.py`
   - `low < value <= high` 的求值顺序；
   - 中间表达式只求值一次；
   - 前段比较失败后，后续表达式不会求值。

5. `05_if_elif_else_branch_selection.py`
   - `if` / `elif` / `else` 只选择第一个命中分支；
   - 多个独立 `if` 适合累积规则，`elif` 链适合互斥选择；
   - 冒号、缩进代码块和括号内续行的语法边界。

6. `06_conditional_expressions_and_readability.py`
   - 条件表达式产生一个值，未选分支不会求值；
   - `prompt_manager_gui.py` 中按钮文本和 widget state 的真实写法；
   - 单值选择与多步副作用代码块的可读性边界。

7. `07_localization_rule_decision_pipeline.py`
   - 综合 `strict`、`dry_run`、缺失 key、空译文、输出模式和严重级别；
   - 返回结构化决策，不写文件、不修改调用者输入；
   - 区分条件求值、真值测试、分支选择和外部副作用。

8. `08_prompt_manager_conditions_and_match_boundaries.py`
   - 只读调用 `prompt_store.parse_tags()` 和 `display_state()`；
   - 对照 `prompt_manager_cli.py` 的 `is not None and ...` 条件；
   - 用结构化命令映射说明 `match` 的适用边界和无 fall-through 语义。

目录内已有的 `P3_C12_*.py` 保留为个人练手/测试轨迹，不属于本 README 的正式
教学顺序，也不会作为本章验收依据。

## 每次预测的固定问题

1. 哪些表达式真正被求值，顺序是什么？
2. 每个表达式得到哪个对象？
3. 哪个对象接受了真值测试，调用了什么协议？
4. `and` / `or` 最终选择了哪个操作数对象？
5. 哪些调用、副作用或异常因短路而没有发生？
6. 比较、身份和成员测试是否各司其职？
7. 比较链的中间表达式求值几次？
8. 哪个代码块真正执行，后续 `elif` 条件是否还会求值？
9. 条件表达式是否只负责选择一个清晰的值？
10. `match` 是否真正在匹配结构，而不是机械替代简单 `if`？

## 当前推进状态

这组文件是 C12 的正式实验骨架，不代表 C12 已通过验收。当前应从
`01_truth_testing_objects_and_protocols.py` 开始逐步预测和复盘；完成全部
实验、综合题与阶段测验后，才进入小阶段收束。
