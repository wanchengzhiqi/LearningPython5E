# C13 while and for Loops

本目录正式推进 `P3_Statements_and_Syntax / C13_while_and_for_Loops`。

本章以 `docs/C13_WHILE_AND_FOR_LOOPS_STARTUP_TEMPLATE.md` 的“实践目标”为正式入口，
把 C12 的条件控制流模型推进到重复执行、跳过、提前终止和安全遍历。
`projects/P3_Statements_and_Syntax/prompt_template_manager/` 只作为真实代码背景，
本目录脚本不会打开、迁移或修改它的 SQLite 数据库。

## 核心分析链

```text
while 条件表达式每轮重新求值
    -> 得到对象
    -> 对象接受真值测试
    -> 为真则执行循环体，为假则正常结束
    -> 循环体必须能改变退出条件，否则可能无限循环

for 先取得可迭代对象
    -> 每轮取出下一个元素对象
    -> 循环变量重新绑定到该元素对象
    -> 执行循环体
    -> 可迭代对象耗尽则正常结束

break    -> 提前终止最近一层循环，并跳过循环 else
continue -> 跳过本轮剩余语句，进入下一轮判断或迭代
else     -> 循环没有被 break 提前终止时执行
```

## 使用方式

先停在每个 `[Predict]`，预测循环次数、变量绑定、输出顺序、容器变化和
循环 `else` 是否执行，再运行脚本。

```powershell
.\.venv-py314\Scripts\Activate.ps1
python --version

python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\01_while_condition_rechecks_and_exit_state.py
python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\02_sentinel_loop_break_and_continue.py
python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\03_loop_else_normal_vs_break.py
python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\04_for_iterables_and_variable_binding.py
python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\05_range_enumerate_zip_selection.py
python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\06_mutating_while_iterating_risks.py
python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\07_localization_resource_scan_loop_pipeline.py
python practice\P3_Statements_and_Syntax\C13_while_and_for_Loops\08_prompt_manager_loop_reading_walkthrough.py
```

## 正式实验地图

1. `01_while_condition_rechecks_and_exit_state.py`：`while` 条件每轮重新求值、循环体改变退出状态。
2. `02_sentinel_loop_break_and_continue.py`：`while True`、哨兵值、`break` 和 `continue`。
3. `03_loop_else_normal_vs_break.py`：循环 `else` 在正常耗尽与 `break` 下的差异。
4. `04_for_iterables_and_variable_binding.py`：字符串、列表、字典、集合、文件行和变量绑定。
5. `05_range_enumerate_zip_selection.py`：直接遍历、`range()`、`enumerate()`、`zip()` 的选型。
6. `06_mutating_while_iterating_risks.py`：边遍历边修改列表或字典的风险与安全替代。
7. `07_localization_resource_scan_loop_pipeline.py`：本地化资源扫描、跳过、收集、阻断和结构化报告。
8. `08_prompt_manager_loop_reading_walkthrough.py`：结合 `prompt_template_manager` 的真实循环阅读实验。

## 每次预测的固定问题

1. `while` 条件每轮是否重新求值？循环体改变了哪个退出状态？
2. `for` 从可迭代对象中取出了哪个元素对象？
3. 循环变量是重新绑定，还是元素对象被复制？
4. `continue` 跳过了哪些语句？
5. `break` 终止了哪一层循环？
6. 循环 `else` 是否执行，原因是什么？
7. 遍历时修改容器结构是否安全？
8. 函数应该返回结构化数据，还是在循环里直接输出或写文件？
