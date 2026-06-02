# C9 Dictionaries and Files

本目录用于当前小阶段：字典和文件：映射、持久化边界与核心类型收束。

本阶段不要把重点放在“背完所有字典方法”和“记住 open 参数表”上，而要先建立两条稳定链路：

```text
源码中的 dict 表达式
    -> Python 创建可变映射对象
    -> 键对象和值对象以引用形式保存在映射中
    -> hash() 与 == 共同决定键查找和去重
    -> 原地修改字典、替换某个键的值、修改值对象本体
    -> JSON object、配置、本地化资源表、结构化报告
```

```text
路径字符串 / Path 对象
    -> open() 返回文件对象
    -> 文件对象按模式读写字节或文本
    -> encoding 在 bytes 和 str 之间做转换
    -> json/csv 模块把文本转成 Python 对象，或把对象转回文本
```

建议使用方式：

1. 先读每个 `section()` 的标题和 `predict()` 提示，不急着运行。
2. 在心里或笔记里写出预测结果、对象身份、返回值和理由。
3. 再运行脚本验证实际输出。
4. 最后回到源码，用“源码形式 / 对象本体 / 名字绑定 / 显示形式 / 文件边界 / 序列化边界”重新解释一遍。

运行示例：

```powershell
python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\01_dict_object_identity.py
python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\02_hash_equality_keys.py
python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\03_methods_views_and_returns.py
python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\04_copy_counter_defaultdict.py
python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\05_files_text_bytes_json_csv.py
python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\06_core_type_synthesis.py
```

阶段综合项目：

```powershell
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --observe
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --format json
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --source projects\P2_Types_and_Operations\localization_resource_auditor\data\source_en.json --target projects\P2_Types_and_Operations\localization_resource_auditor\data\target_zh.json --glossary projects\P2_Types_and_Operations\localization_resource_auditor\data\glossary.csv --max-length 42
```

学习主线：

- `01_dict_object_identity.py`：字典字面量、对象身份、名字绑定、键覆盖、修改字典本体 vs 修改值对象。
- `02_hash_equality_keys.py`：可哈希要求、`hash()`、`==`、键去重、`dict.fromkeys()`、集合差异。
- `03_methods_views_and_returns.py`：`get()`、`setdefault()`、`update()`、`pop()`、视图对象和返回值。
- `04_copy_counter_defaultdict.py`：浅拷贝、深拷贝、`Counter`、`defaultdict`、`dict.fromkeys()` 可变默认值陷阱。
- `05_files_text_bytes_json_csv.py`：路径、文件对象、文本/字节、编码、JSON/CSV 边界。
- `06_core_type_synthesis.py`：数字、字符串、列表、元组、字典、集合、文件对象的横向收束。
- `stage_quiz_dictionaries_and_files.md`：阶段验收题。

关键纠偏：

- 字典保存的是键对象和值对象的引用；键查找不是靠 `is`，而是先用 `hash()` 定位，再用 `==` 判断是否同一个逻辑键。
- “不可变对象通常可哈希”只是入门近似，不是严格规则；例如包含列表的元组不可哈希。
- `d[k] = v` 修改的是字典这个映射对象；`d[k].append(...)` 修改的是字典中某个值对象本体。
- 字典视图对象不是列表快照；`keys()`、`values()`、`items()` 会反映字典后续变化。
- `update()`、`setdefault()` 等方法的返回值和它们对字典对象造成的变化是两件事。
- 路径字符串不是文件对象；`open()` 返回的文件对象才是读写接口。
- JSON 文本不是 Python dict；`json.loads()` / `json.load()` 会解析文本并创建新的 Python 对象结构。

阶段验收：

- 能解释字典键为什么必须可哈希，以及 `hash()` 与 `==` 如何共同影响键查找和去重。
- 能判断某一步是在修改字典本体、替换某个键的值，还是修改字典中保存的可变值对象。
- 能解释字典视图对象和列表快照的区别。
- 能说明字典浅拷贝与深拷贝的层级差异。
- 能把路径、文件对象、文本、字节、编码、JSON/CSV、内存对象分层说明。
- 能在游戏本地化资源审计项目中合理选择 `dict`、`list`、`tuple` / `namedtuple`、`set`、`Counter`、`defaultdict` 和文件对象。
