```python
def find_entry(entries, key):
    normalized_key = key.strip().lower()

    for entry in entries:
        if entry["key"].strip().lower() == normalized_key:
            return entry

    return None
```

| 维度             | 合同                                                         |
| ---------------- | ------------------------------------------------------------ |
| 输入             | 可迭代的记录集合，以及支持 `strip().lower()` 的键对象        |
| 正常返回         | 找到时返回匹配的记录对象；未找到时返回 `None`                |
| 异常             | 记录缺少 `"key"` 时可能出现 `KeyError`；对象不支持所需操作时可能出现相关异常 |
| 显示输出         | 无                                                           |
| 外部 I/O         | 无                                                           |
| 是否修改传入对象 | 当前代码不执行原地修改                                       |
| 路径稳定性       | 所有正常路径均明确返回：记录对象或 `None`                    |
