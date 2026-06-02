# Localization Resource Auditor

`localization_resource_auditor` 是 Types and Operations 大阶段的综合实践项目。它不是生产级本地化平台，而是一个可复盘的标准库 CLI 工具，用来把字典、列表、元组 / `namedtuple`、集合、`Counter`、文件对象、JSON、CSV、字符串和数字统计放进同一个工程场景中观察。

默认运行会读取 `data/source_en.json`、`data/target_zh.json` 和 `data/glossary.csv`。
JSON 资源文件按 `utf-8-sig` 读取，因此普通 UTF-8 与带 UTF-8 BOM 的导出文件都可处理。

```powershell
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --observe
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --format json
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --format json --observe
```

指定外部文件：

```powershell
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --source path\to\source.json --target path\to\target.json --glossary path\to\glossary.csv --max-length 42
python projects\P2_Types_and_Operations\localization_resource_auditor\localization_auditor.py --format json --output report.json
```

如果显式传入的 `--glossary` 路径不存在，程序会报错，而不是静默当成“没有术语表”。如果不传 `--glossary`，程序会优先使用项目自带的 `data/glossary.csv`；若该默认文件不存在，则按无术语表运行。

学习目标：

- `dict` 保存资源 key 到文本的映射。
- `Counter` 检查 JSON object 中重复出现的 key。
- `set` 做缺失 key、额外 key、共同 key 的差异计算。
- `list` 保存可排序、可过滤的问题记录。
- `namedtuple` 表示稳定的 issue 和术语记录。
- `csv.DictReader` 把 CSV 文本行转成带字段名的行映射。
- `open(..., encoding="utf-8")` 明确文本文件的编码边界。
- JSON 输出前把内部对象模型转换成 `dict/list/str/int/bool/None`。
- `--observe` 输出对象边界观察：JSON pair 列表如何折叠成 dict、重复 key 如何保留最后值、`str` 长度与 UTF-8 字节长度如何不同。

重点纠偏：

- JSON object 文本不是 Python dict；解析后才得到新的 Python 映射对象。
- 字典查找 key 不是靠 `is`，而是靠 `hash()` 与 `==`。
- 字典浅拷贝只复制外层映射，内部可变值对象仍可能共享。
- `--format json` 输出的是机器可读结构；如果混入普通说明文字，就会破坏下游工具读取。
- JSON object 中重复 key 不会被普通 `dict` 保留下来；本项目先用 `object_pairs_hook` 保留 pair 列表，再显式展示“折叠前 values”和“折叠后 kept value”。
- CSV 单元格是文本字段，不会自动保留 Python 的 `list` / `dict` 结构；需要嵌套结构时优先输出 JSON report。
