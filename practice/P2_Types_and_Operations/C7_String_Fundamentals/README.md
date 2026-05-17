# C7 String Fundamentals

本目录用于当前小阶段：Python 字符串基础。

本阶段不要把重点放在“背完所有字符串方法”上，而要先建立一条稳定链路：

```text
源码中的字符串字面量
    -> Python 解析转义序列
    -> 内存中的 str 对象
    -> str() / repr() / print() / 交互式回显
    -> encode() 后的 bytes
    -> 文件、网络、JSON、日志、本地化文本
```

建议使用方式：

1. 先读每个 `section()` 的标题和 `predict()` 提示，不急着运行。
2. 在心里或笔记里写出预测结果、结果类型和理由。
3. 再运行脚本验证实际输出。
4. 最后回到源码，用“源码形式 / 对象本体 / 显示形式 / 字节表示”重新解释一遍。

运行示例：

```powershell
python practice\P2_Types_and_Operations\C7_String_Fundamentals\01_literals_and_escapes.py
python practice\P2_Types_and_Operations\C7_String_Fundamentals\02_repr_str_print.py
python practice\P2_Types_and_Operations\C7_String_Fundamentals\03_index_slice_immutability.py
python practice\P2_Types_and_Operations\C7_String_Fundamentals\04_methods_and_formatting.py
python practice\P2_Types_and_Operations\C7_String_Fundamentals\05_text_bytes_files_json.py
python practice\P2_Types_and_Operations\C7_String_Fundamentals\06_formatting_styles_deep_dive.py
```

阶段综合小工具：

```powershell
python practice\P2_Types_and_Operations\C7_String_Fundamentals\mini_project_string_observer.py
python practice\P2_Types_and_Operations\C7_String_Fundamentals\mini_project_string_observer.py --literal "'HP\nPotion'"
python practice\P2_Types_and_Operations\C7_String_Fundamentals\mini_project_string_observer.py --slice 1:-1:2 "Localization"
```

学习主线：

- `01_literals_and_escapes.py`：字符串字面量、转义序列、原始字符串、三重引号、Unicode 转义。
- `02_repr_str_print.py`：`repr()`、`str()`、`print()`、交互式回显的分层关系。
- `03_index_slice_immutability.py`：字符串作为不可变序列的索引、切片、负索引、步长和重新绑定。
- `04_methods_and_formatting.py`：常用字符串方法、方法返回新对象、格式化生成新字符串。
- `05_text_bytes_files_json.py`：`str` / `bytes` 边界、UTF-8 文件读取、JSON 文本、Windows 路径。
- `06_formatting_styles_deep_dive.py`：专题比较 `%` 表达式、`.format()` 方法和 f-string。
- `mini_project_string_observer.py`：字符串观察工具和本地化文本检查工具。
- `stage_quiz_string_fundamentals.md`：阶段验收题。

关键纠偏：

- `str` 支持序列协议，索引结果是长度为 1 的 `str`；不要把它理解成内存中真的存放一堆单字符字符串对象。
- `repr(s)` 返回的是一个新的 `str` 对象；如果在交互式环境里查看这个返回值，它还会再经过一层回显显示。
- `print()` 会把对象转成文本并写入文本流；终端编码仍可能影响最终显示效果。
- 原始字符串不是绝对原始：不能以单个反斜杠结尾，字符串边界的引号规则仍然存在。
- Unicode 码位、用户看到的字符、UTF-8 字节数不是同一层概念。

阶段验收：

- 能面对任意字符串表达式，说明源码里写了什么、解析后对象是什么、长度是多少、每个字符是什么。
- 能解释交互式回显为什么看起来像源码，但并不等于原始源码。
- 能解释 `str()`、`repr()`、`print()` 的区别，并知道 `print()` 本身返回 `None`。
- 能稳定推导常见切片结果，包括负索引、空切片、反向切片和步长。
- 能说明字符串不可变，所以“修改字符串”通常是创建新字符串并让名字重新绑定。
- 能区分文本和字节：文本处理用 `str`，文件/网络底层边界会遇到 `bytes`，跨边界时显式编码或解码。
- 能用小工具检查游戏本地化文本中的换行、占位符、特殊字符、UTF-8 字节数和缺失 key。
