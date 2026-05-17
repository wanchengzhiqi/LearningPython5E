# C8 Lists and Tuples

本目录用于当前小阶段：Python 列表和元组。

本阶段不要把重点放在“背完所有列表方法”上，而要先建立一条稳定链路：

```text
源码中的容器表达式
    -> Python 创建列表 / 元组对象
    -> 名字绑定到对象
    -> 原地修改对象或重新绑定名字
    -> 容器显示时使用元素的 repr 风格
    -> 文件、JSON、日志、CLI 参数、游戏本地化记录
```

建议使用方式：

1. 先读每个 `section()` 的标题和 `predict()` 提示，不急着运行。
2. 在心里或笔记里写出预测结果、对象身份、返回值和理由。
3. 再运行脚本验证实际输出。
4. 最后回到源码，用“源码形式 / 对象本体 / 名字绑定 / 显示形式 / 共享层级”重新解释一遍。

运行示例：

```powershell
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\01_list_object_identity.py
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\02_sequence_operations.py
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\03_methods_and_sorting.py
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\04_slice_assignment_and_copy.py
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\05_nested_lists_and_shared_references.py
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\06_tuples_unpacking_namedtuple.py
```

阶段综合小工具：

```powershell
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --issues-only
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --copy-demo
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --shared-tags-demo
```

学习主线：

- `01_list_object_identity.py`：列表字面量、对象身份、名字绑定、`==` 与 `is`。
- `02_sequence_operations.py`：索引、切片、拼接、重复、`+` 与 `+=` 的对象效果。
- `03_methods_and_sorting.py`：列表方法返回值、原地修改、`sort()` 与 `sorted()`。
- `04_slice_assignment_and_copy.py`：切片赋值、外层浅拷贝、深拷贝、重新绑定边界。
- `05_nested_lists_and_shared_references.py`：嵌套列表、重复引用陷阱、默认参数共享。
- `06_tuples_unpacking_namedtuple.py`：元组字面量、逗号、不可变边界、解包、`*args`、`namedtuple`。
- `mini_project_localization_records.py`：本地化记录观察与批处理工具。
- `stage_quiz_lists_and_tuples.md`：阶段验收题。

关键纠偏：

- `a = b` 不复制列表对象，只是让两个名字绑定到同一个对象。
- `append()`、`extend()`、`sort()`、`reverse()` 通常返回 `None`，它们修改的是目标列表本体。
- `a + b` 创建新列表；`a += b` 对列表通常原地扩展。
- 列表切片读取会创建新外层列表；切片赋值会原地修改原列表。
- `a[:]`、`list(a)`、`copy.copy(a)` 都是浅拷贝，不会复制内层可变对象。
- `[[0] * 3] * 3` 会重复引用同一个内层列表，不会创建三个独立行。
- 真正创建元组的是逗号，不是圆括号；`(1)` 是整数，`(1,)` 才是单元素元组。
- 元组不可变指元组自身保存的引用不可替换；如果元素对象可变，元素对象仍可能被原地修改。
- 容器显示会使用元素的 `repr()` 风格，但不会改变元素对象本体。

阶段验收：

- 能面对任意列表或元组表达式，说明创建了什么对象、哪些名字绑定到它、是否共享同一对象。
- 能判断某一步是原地修改还是重新绑定。
- 能说清楚列表方法返回值和被修改对象之间的关系。
- 能稳定推导索引、切片、拼接、重复、切片赋值、排序和解包结果。
- 能解释浅拷贝与深拷贝的层级差异。
- 能说明元组不可变的真实边界。
- 能在游戏本地化记录场景中选择列表、元组、`namedtuple`、字符串和字典等结构。
