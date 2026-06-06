# C10 Introducing Python Statements

本目录用于当前小阶段：Python 语句导论：表达式、语句、代码块与执行顺序。

这一章的重点不是背语法表，而是把 P2 已经建立的对象模型推进到语句层：

```text
源码片段
    -> 表达式求值，得到对象或产生副作用
    -> 语句执行，组织一步程序动作
    -> 缩进代码块表达语法归属
    -> 控制流决定某些代码块是否进入
    -> 程序按可解释的顺序影响内存对象、输出流和外部文件
```

建议使用方式：

1. 先读每个 `section()` 的标题和 `[Predict]` 提示，不急着运行。
2. 在心里写出预测：这里是表达式求值，还是语句执行？有没有副作用？
3. 再运行脚本验证实际输出。
4. 最后回到源码，用“表达式的值 / 副作用 / 语句执行 / 代码块归属 / 控制流进入条件”重新解释一遍。

运行示例：

```powershell
.\.venv-py314\Scripts\Activate.ps1
python --version
python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\01_expressions_statements_and_side_effects.py
python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\02_script_vs_interactive_echo.py
python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\03_logical_lines_and_blocks.py
python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\04_order_and_control_flow_preview.py
```

学习主线：

- `01_expressions_statements_and_side_effects.py`：表达式、表达式语句、返回值和副作用。
- `02_script_vs_interactive_echo.py`：脚本执行、交互式回显、`print()` 输出与返回值。
- `03_logical_lines_and_blocks.py`：物理行、逻辑行、括号续行、反斜杠续行、分号和缩进块。
- `04_order_and_control_flow_preview.py`：顶层顺序执行，以及控制流是否进入代码块的最小预告。

关键纠偏：

- 表达式会被求值并产生一个值；不要把这句话扩展成“所有语句都有返回值”。
- 函数调用是表达式；函数调用可能既有返回值，也有副作用。
- `print(value)` 的副作用是向输出流写文本；它的返回值通常是 `None`。
- 脚本里的表达式语句不会自动回显结果；交互式环境会显示非 `None` 表达式值。
- 物理换行不一定结束逻辑行；括号内可以隐式续行。
- 缩进不是代码美化，而是 Python 源码语法结构。
- 缩进代码块不是运行时容器对象；控制流进入代码块时，里面的语句才会执行。

阶段验收：

- 能区分表达式求值与语句执行。
- 能说明表达式的值和副作用不是一回事。
- 能解释 `print()` 输出和 `print()` 返回值的区别。
- 能解释脚本执行与交互式回显的差异。
- 能读懂物理行、逻辑行、括号续行、反斜杠续行和分号。
- 能说明缩进代码块表达语法归属，不是运行时对象。
- 能预测顶层语句顺序执行，以及简单控制流是否进入某个代码块。
