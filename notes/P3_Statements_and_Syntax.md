# P3 Statements and Syntax

本笔记用于 `P3_Statements_and_Syntax`：Python 的语句和语法。

P3 的核心任务不是背语法清单，而是把 P2 已经建立的对象模型迁移到程序执行层：

```text
对象模型：对象、名字、引用、可变性、显示形式、外部边界
    -> 表达式求值：创建、查找、组合或调用对象
    -> 语句执行：把求值结果、名字绑定、副作用和控制流组织成程序动作
    -> 代码块：用源码缩进表达语法归属
    -> 控制流：决定下一步执行哪条语句或哪个代码块
```

## 2026-06-03：C10 语句导论启动

当前小阶段：`C10_Introducing_Python_Statements`。

本章只正式推进语句导论，不提前系统展开 C11-C15。后续赋值、条件、循环、迭代和文档工具会在各自小阶段再展开。

### 本章主线

1. 表达式会求值，产生一个对象作为值；求值过程中也可能产生副作用。
2. 语句是可执行的源码单位，用来组织程序动作；不能把“表达式有值”泛化成“所有语句都有返回值”。
3. 表达式语句会执行表达式。在脚本中，表达式语句的值通常被丢弃；在交互式环境中，非 `None` 的表达式值会被回显。
4. `print(value)` 是函数调用表达式；它的副作用是向输出流写文本，返回值通常是 `None`。
5. 物理行是源码文件里的实际换行；逻辑行才是 Python 解析出的完整语句单位。
6. 括号、方括号和花括号内可以隐式续行；反斜杠可以显式续行，但更脆弱。
7. 分号可以在一个逻辑行里分隔多个简单语句，但通常不推荐。
8. 缩进不是排版装饰，而是 Python 语法结构；缩进代码块不是运行时容器对象。
9. 顶层语句通常按顺序执行；控制流语句会决定某个缩进代码块是否进入。

### 当前易混边界

- `print()` 的输出不是 `print()` 的返回值。
- 交互式回显不是脚本执行的自动行为。
- 表达式的值、表达式求值产生的副作用、表达式语句整体的作用，需要分开说。
- 代码块是源码语法结构，不是列表、字典或其它运行时对象。
- 只看源码书写顺序不够；还要判断控制流是否进入某个代码块。

### 本章练习脚本

- `practice/P3_Statements_and_Syntax/C10_Introducing_Python_Statements/01_expressions_statements_and_side_effects.py`
- `practice/P3_Statements_and_Syntax/C10_Introducing_Python_Statements/02_script_vs_interactive_echo.py`
- `practice/P3_Statements_and_Syntax/C10_Introducing_Python_Statements/03_logical_lines_and_blocks.py`
- `practice/P3_Statements_and_Syntax/C10_Introducing_Python_Statements/04_order_and_control_flow_preview.py`

### 阶段验收观察点

- 能否稳定区分表达式求值与语句执行。
- 能否说明值、返回值、副作用、输出和回显的层级差异。
- 能否判断一段源码中的逻辑行、缩进代码块和执行顺序。
- 能否把 P2 的对象模型自然延伸到 P3：表达式产生或访问对象，语句组织对名字、对象和外部边界的影响。
