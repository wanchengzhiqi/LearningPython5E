# C5 Numeric Object Types

本目录用于当前小阶段：Python 数值对象类型的系统学习。

建议使用方式：

1. 先读每个 `section()` 的标题和 `predict()` 提示，不急着运行。
2. 在心里或笔记里写下你预测的结果、结果类型和理由。
3. 再运行脚本验证实际输出。
4. 最后回到源码，解释“为什么是这个结果”，尤其要解释对象类型、运算符语义和边界情况。

运行示例：

```powershell
python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\01_int_float_basics.py
```

阶段综合小工具：

```powershell
python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\mini_project_numeric_toolkit.py
```

它不是一个完整业务系统，而是一个“数值对象实验台”。运行后重点观察：

- `0x2d`、`b"\x2d"[0]`、`ord("-")` 分别处在源码整数表示、字节值、Unicode 码位三层语义中。
- `round()`、`format()`、`math.floor()`、`math.trunc()`、`int()` 对正负浮点数的处理差异。
- 金额计算为什么拒绝已有 `float`，并用 `Decimal(...).quantize(...)` 明确最终小数位。
- `Fraction(0.1)` 为什么暴露的是已有浮点对象的真实二进制近似值。
- 权限位为什么要求原子权限是非零且不重叠的单个二进制位。
- `set` 如何服务本地化 key 的缺失项、额外项和完成率检查。
- 字符串长度、UTF-8 字节数、Unicode 码位和 bytes 迭代结果为什么不是同一件事。

学习主线：

- `01_int_float_basics.py`：整数、浮点数、进制字面量、除法边界。
- `02_decimal_fraction.py`：固定精度十进制数和有理分数。
- `03_complex_bool.py`：复数、布尔值与整数的关系。
- `04_sets.py`：集合对象、集合代数和去重场景。
- `05_bitwise_flags.py`：位运算、权限位、标志位。
- `mini_project_numeric_toolkit.py`：阶段综合小工具，整合进制、显示/取整、金额、比例、权限位、集合和字符编码观察。

阶段验收：

- 能解释 `int` 的任意精度和 `float` 的二进制近似语义。
- 能解释 `/`、`//`、`%`、`divmod()` 的关系，尤其是负数参与时的结果。
- 能把二进制、八进制、十六进制看作“整数对象的不同源码/显示形式”，而不是不同种类的数。
- 能说明什么时候选择 `float`、`Decimal`、`Fraction`，并知道从已有 `float` 构造 `Decimal` 或 `Fraction` 的陷阱。
- 能说明 `bool` 是 `int` 的子类，但在工程代码中主要表达真假语义。
- 能使用 `set` 做去重、差集、交集、并集、对称差集，并知道集合没有位置顺序。
- 能把位运算解释成“对整数的二进制位进行组合、检测、移除和切换”。
- 能读懂并运行综合小工具，理解它如何服务本地化 key 检查、覆盖率统计、权限标志和字符编码观察。

阶段提醒：

- 数字对象大多不可变，计算通常产生新对象。
- `float` 适合近似计算，不适合精确金额。
- `Decimal` 适合十进制定点语义，但要避免从已有 `float` 直接构造。
- `Fraction` 适合理解比例、精确有理数和验证浮点误差来源。
- `bool` 是 `int` 的子类，但工程上不要把二者随意混用。
- `set` 是集合类型，不是序列：无顺序语义，不支持按位置索引。
- 位运算本质上是在二进制位层面组合、检测、移除状态。
- `~x` 不是“把显示出来的几位取反”，而是基于 Python 整数模型满足 `~x == -x - 1`。
