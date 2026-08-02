# C16 函数契约卡定稿

适用脚本：`p3_localization_quality_gate_c16_run_gate.py`

基线报告：`p3_localization_report.json`

> 本工件记录当前实现的真实合同。它不是对未来版本的永久保证；
> 若实现或业务规则变化，契约卡与验证器应同步更新。

## 总体职责图

```text
normalize_key ─────────┐
                       ├── make_issue ───────┐
extract_placeholders ──┘                    │
                                            ▼
build_entries ───────────────────── validate_entries
      ▲                                     ▲
      └────────────── run_gate ─────────────┘
                         │
                         ▼
                       report
                    ┌────┴────┐
                    ▼         ▼
              print_report  save_report
                    └────┬────┘
                         ▼
                       main
```

---

## 1. `normalize_key(key)`

**主要职责**  
去除本地化键首尾空白，并将其转换为小写。

**输入与最小接口**  
`key` 支持 `strip()`；其返回对象支持 `lower()`。当前项目正式输入为 `str`。

**正常返回**  
`key.strip().lower()` 的结果对象。

**输入修改**  
无显式原地修改；对当前字符串输入不修改原对象。

**显示、日志、外部 I/O**  
无。

**异常**  
所需方法缺失或方法调用失败时，异常向外传播。

**非职责**  
不检查前缀、重复键或空键；不创建问题记录。

---

## 2. `extract_placeholders(text)`

**主要职责**  
按从左到右顺序提取由左花括号开始、随后第一个右花括号结束的 token。

**正常返回**  
新 `list`；保留出现顺序与重复次数。

**输入修改与副作用**  
不修改当前字符串输入；无显示、日志或文件 I/O。

**当前边界**  
未闭合的左花括号会使剩余文本作为一个 token 返回；孤立右花括号被忽略；不实现完整 Python 格式字符串语法。

**非职责**  
不比较源文与译文，不判定占位符是否业务合法。

---

## 3. `build_entries(keys, sources, translations, enabled_flags)`

**主要职责**  
把四组平行数据列组合为带 1 起始行号的统一条目列表。

**输入与消费**  
四个输入均需可迭代；调用会推进它们。`zip(..., strict=True)` 要求长度一致。

**正常返回**  
新 `list`，元素为包含 `line`、`key`、`source`、`translation`、`enabled` 的新字典。

**输入修改**  
不对当前列表输入做显式原地修改。

**异常**  
长度不一致时抛出 `ValueError`；迭代过程中的异常继续传播。

**非职责**  
不规范化字段，不验证质量规则，不执行 I/O。

---

## 4. `make_issue(level, code, entry, message)`

**主要职责**  
按统一结构创建一条问题记录。

**输入最低要求**  
`entry` 支持 `entry["line"]` 和 `entry["key"]`；键可由 `normalize_key()` 处理。

**正常返回**  
新字典：`level`、`code`、`line`、规范化 `key`、`message`。

**输入修改与副作用**  
不修改当前条目字典；无显示、日志或文件 I/O。

**非职责**  
不判断是否违规，不把记录追加到问题列表。

---

## 5. `validate_entries(entries, config)`

**主要职责**  
执行当前质量规则，返回摘要和排序后的结构化问题列表。

**输入与最低接口**  
`entries` 必须可迭代且支持 `len()`；普通生成器不满足当前完整合同。每个条目支持所需字段访问。`config` 提供 `allowed_prefixes` 与包含 `ERROR`、`WARNING` 的 `error_levels`。

**正常返回**

```python
{
    "summary": {
        "input_count": ...,
        "processed_count": ...,
        "skipped_count": ...,
        "error_count": ...,
        "warning_count": ...,
        "passed": ...,
    },
    "issues": [...],
}
```

**输入修改**  
对当前列表、条目字典和配置字典不做显式原地修改。

**消费**  
完整遍历 `entries` 一次，最后读取 `len(entries)`。

**直接副作用**  
无显示、日志和文件 I/O。

**当前规则边界**  
禁用条目完全跳过；空译文产生问题后 `continue`；占位符比较保留重复次数但忽略顺序；问题按 `(line, level, code)` 排序。

---

## 6. `print_report(report)`

**主要职责**  
把结构化报告写成人读终端文本。

**正常返回**  
`None`。无问题分支执行裸 `return`，仍正常返回 `None`。

**显示输出**  
向标准输出写入 Python/解释器诊断、摘要和问题明细。

**输入修改与外部 I/O**  
不修改当前报告；无文件写入。标准输出本身属于副作用。

**部分失败**  
格式化或输出中途异常时，标准输出可能已有部分文本。

---

## 7. `save_report(report, filename)`

**主要职责**  
以 UTF-8 JSON 覆盖写入结构化报告。

**正常返回**  
`None`。

**文件合同**  
`ensure_ascii=False`、`indent=2`；当前实现不主动追加文件末尾换行。

**输入修改**  
不修改当前报告对象。

**异常与部分失败**  
序列化、权限、路径或文件系统异常继续传播；覆盖写入失败可能留下空文件或部分文件。

**非职责**  
不打印成功消息，不执行验证，不决定门禁是否通过。

---

## 8. `run_gate(keys, sources, translations, enabled_flags, config)`

**主要职责**  
组合 `build_entries()` 与 `validate_entries()`，交付结构化报告。

**正常返回**  
基于输入生成的报告字典。

**直接副作用**  
不打印、不保存文件。对当前普通列表与字典没有观察到内容修改。

**消费与异常**  
通过 `build_entries()` 消费四组输入；下游异常继续传播。

**准确表述**  
它是当前项目中的数据处理边界，但不应被绝对化为“对任意自定义对象都严格纯”。

---

## 9. `main()`

**主要职责**  
使用模块默认常量运行完整命令式工作流。

**运行轨迹**  
`run_gate()` → `print_report()` → `save_report()`。

**正常返回**  
运行到末尾，隐式返回 `None`。

**副作用**  
打印报告，并在当前工作目录覆盖写入 `p3_localization_report.json`。

**异常与部分失败**  
下游异常继续传播；保存失败前报告通常已经打印。

**入口关系**  
只有在 `__name__ == "__main__"` 时被自动调用；普通导入只创建对象和绑定，不自动运行门禁。

---

## 基线业务结果

```text
input_count      = 6
processed_count  = 5
skipped_count    = 1
error_count      = 3
warning_count    = 0
passed           = False
```

问题顺序：

1. `line=2 / missing_translation`
2. `line=3 / duplicate_key`
3. `line=4 / placeholder_mismatch`

## 当前保留而未修正的边界

- 畸形花括号的占位符提取行为；
- `validate_entries()` 对普通生成器不兼容；
- `error_levels` 必须包含 `ERROR` 和 `WARNING`；
- 问题级别按字符串排序；
- 输出路径相对于当前工作目录；
- 保存失败没有原子替换保证；
- `main()` 不返回报告或命令行退出码；
- 函数尚未系统添加类型注解。

这些事项若以后调整，应作为独立行为变更，而不是混入本轮结构验收。
