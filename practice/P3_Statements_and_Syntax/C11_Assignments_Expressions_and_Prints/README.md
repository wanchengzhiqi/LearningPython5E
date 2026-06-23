# C11 Assignments, Expressions, and Prints

本目录正式推进 `P3_Statements_and_Syntax / C11_Assignments_Expressions_and_Prints`。

这一章继续沿用 C10 的核心模型：

```text
右侧表达式先求值
    -> 左侧目标再绑定、写入、解包或触发对象协议
    -> 表达式语句的结果在脚本里通常被丢弃
    -> print() 把文本写到输出流，但返回值仍是 None
```

## 使用方式

建议先读脚本里的 `[Predict]` 提示，在心里写出预测，再运行脚本验证。

```powershell
.\.venv-py314\Scripts\Activate.ps1
python --version
python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\01_assignment_binding_and_aliasing.py
python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\02_unpacking_assignment_targets.py
python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\03_augmented_assignment_mutation_vs_rebinding.py
python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\04_expression_statements_and_print_streams.py
python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\05_prompt_template_manager_c11_walkthrough.py
```

## 学习主线

- `01_assignment_binding_and_aliasing.py`：普通赋值、链式赋值、共享引用，以及 `prompt_store.py` 中 `clauses.append(...)` 和 `query += ...` 的差异。
- `02_unpacking_assignment_targets.py`：序列解包、星号解包、嵌套解包、多目标交换、解包错误、属性/下标/切片赋值。
- `03_augmented_assignment_mutation_vs_rebinding.py`：增强赋值在 `list`、`tuple`、`str`、`set`、`dict` 上的原地修改和重新绑定边界。
- `04_expression_statements_and_print_streams.py`：表达式语句、方法调用副作用、`print()` 返回值、`sep`、`end`、`file`、`flush` 与输出流。
- `05_prompt_template_manager_c11_walkthrough.py`：复用 `projects/P3_Statements_and_Syntax/prompt_template_manager/` 的真实代码场景，把 C11 概念连回当前 P3 支持工具。

以上 5 个脚本是本章的综合概览实验。以 C11 启动模板为唯一正式教学入口、
按小步节奏推进时，还形成了以下逐步学习记录：

- `P3_C11_01_assignment_model.py`：普通赋值、名字绑定、对象修改与重新绑定。
- `P3_C11_02_chain_and_multi_assignment.py`：链式赋值、多目标赋值与共享引用。
- `P3_C11_03_unpacking_assignment.py`：序列解包、星号解包、嵌套解包与失败边界。
- `P3_C11_04_attribute_subscript_slice_assignment.py`：属性、下标、切片赋值目标与对象协议。
- `P3_C11_05_augmented_assignment.py`：增强赋值、别名可见性与非事务式副作用。
- `P3_C11_06_expression_statements_and_print.py`：表达式语句、结果丢弃和 `print()` 返回值。
- `P3_C11_07_print_engineering_boundary.py`：stdout、stderr、文件流、刷新和写入边界。
- `P3_C11_08_localization_audit_review.py`：本地化审计场景下的阶段综合复盘。

阶段测验与逐题批改记录保存在：

- `stage_quiz_assignments_expressions_and_prints.md`：A-F 六部分阶段测验、原始作答、逐题批改、阶段评语与学习画像更新。

建议按 `P3_C11_01` 至 `P3_C11_08` 的顺序复盘；需要快速横向回顾时，再运行
前面的 5 个综合概览脚本。

## 本章必须纠正的混淆点

1. `x = expr` 不是“返回 expr 的值”。赋值语句的效果是让目标绑定或写入右侧对象。
2. `a = b = []` 只创建一个列表对象，两个名字共享它；不是两个独立列表。
3. `a, b = b, a` 会先完成右侧求值，再处理左侧绑定。
4. `+=` 不是永远等同于 `x = x + y`。可变对象可能原地修改，不可变对象通常创建新对象并重新绑定。
5. `items.append(x)` 的返回值是 `None`，列表变化来自原地修改副作用。
6. `print(...)` 的返回值是 `None`；屏幕、`StringIO`、文件或 `stderr` 中的文本是输出副作用。
7. `print(..., file=...)` 改变输出流边界，不改变 `print()` 的返回对象。
8. 属性赋值、下标赋值和切片赋值不只是“变量改值”，它们可能调用对象协议并修改已有对象。

## 与 prompt_template_manager 的真实连接

这些脚本优先复用当前 P3 项目里的真实形态：

- `prompt_store.py` 里的 `record = dict(row)` 是新字典绑定，`record["tags"] = ...` 是下标赋值。
- `prompt_store.py` 里的 `clauses.append(...)`、`params.extend(...)` 修改已有列表对象。
- `prompt_store.py` 里的 `query += " WHERE ..."` 作用在 `str` 上，会创建新字符串并重新绑定 `query`。
- `prompt_manager_cli.py` 里的 `print(..., file=sys.stderr)` 把输出副作用写向错误流，而不是改变 `print()` 返回值。

阶段目标不是背这些语法，而是看到任意一行 C11 范围代码时能问清楚：

```text
右侧表达式产生了什么对象？
左侧目标是名字、属性、下标、切片，还是解包结构？
改变的是名字绑定、对象本体，还是输出流？
有没有多个名字共享同一个可变对象？
返回值和副作用是否被混在一起说了？
```
