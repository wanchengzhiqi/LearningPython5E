# Stage Quiz: Dictionaries and Files

本测验用于当前小阶段：字典和文件：映射、持久化边界与核心类型收束。

这份卷子不只考字典 API 或文件 API，还会考你是否能把对象模型、哈希、映射、文件对象、编码、JSON/CSV、本地化资源审计和核心对象类型复盘放到同一张图里理解。

总分：100 分。

答题规则：

1. 第一遍不要运行代码，先写预测、对象身份变化、返回值和理由。
2. 第二遍可以用 Python 3.9.13 验证，并标注“验证前预测”和“验证后修正”。
3. 每道代码题尽量按这条链解释：源码写了什么、创建了什么对象、名字绑定到哪里、哪一步修改字典、哪一步修改值对象、文件或 JSON 边界在哪里、输出为什么这样显示。
4. 本卷不包含参考答案。你作答后交给我审批，我会保留你的原答案并追加批改记录。
5. 若你认为题目本身有歧义，可以直接指出；这也属于本阶段能力的一部分。

---

## A. 字典对象、绑定和可变值对象（20 分）

### A1. 赋值、别名和键赋值（6 分）

预测输出，并说明 `source`、`alias`、`snapshot` 三个名字分别绑定到什么对象。

```python
source = {"menu.start": "Start"}
alias = source
snapshot = source.copy()

alias["menu.quit"] = "Quit"

print(source)
print(alias)
print(snapshot)
print(source is alias)
print(source is snapshot)
print(source == snapshot)
```

答题区：

```text

```

### A2. 修改字典本体 vs 修改值对象（7 分）

预测输出，并解释每一步到底修改了哪个对象。

```python
tags = ["ui"]
entry = {"key": "menu.start", "tags": tags}

entry["tags"].append("reviewed")
old_tags = entry["tags"]
entry["tags"] = ["final"]

print(tags)
print(old_tags)
print(entry)
print(entry["tags"] is old_tags)
```

答题区：

```text

```

### A3. 键覆盖和插入顺序（7 分）

预测输出，并解释为什么最终没有两个 `menu.start`。

```python
resources = {}
resources["menu.start"] = "Start"
resources["menu.quit"] = "Quit"
resources["menu.start"] = "Begin"

print(resources)
print(list(resources))
print(len(resources))
```

答题区：

```text

```

---

## B. 哈希、相等性和集合关系（20 分）

### B1. `hash()` 与 `==`（8 分）

下面两个对象不是同一个对象，但可能被字典当成同一个键。解释原因。

```python
class Key:
    def __init__(self, text):
        self.text = text

    def __eq__(self, other):
        return isinstance(other, Key) and self.text == other.text

    def __hash__(self):
        return hash(self.text)

a = Key("menu.start")
b = Key("menu.start")
d = {a: "Start"}
d[b] = "Begin"

print(a is b)
print(a == b)
print(len(d))
print(d[a])
print(d[b])
```

答题区：

```text

```

### B2. 可哈希不等于“看起来不可变”（6 分）

哪些能作为字典键？哪些不能？为什么？

```python
keys = [
    "menu.start",
    ("menu", "start"),
    ("menu", ["start"]),
    ["menu", "start"],
]
```

答题区：

```text

```

### B3. `dict.fromkeys()`、`set` 和资源 key 差异（6 分）

解释下面三个结果分别适合什么工程需求。

```python
keys = ["menu.start", "menu.quit", "menu.start", "menu.options"]
source = {"menu.start", "menu.quit", "menu.options"}
target = {"menu.start", "debug.unused"}

list(dict.fromkeys(keys))
source - target
target - source
```

答题区：

```text

```

---

## C. 方法返回值、视图对象和拷贝层级（20 分）

### C1. `get()`、`setdefault()`、`update()`、`pop()`（8 分）

预测输出，并说明每个方法是否修改字典，以及返回什么。

```python
issues = {"menu.start": ["too long"]}

a = issues.get("menu.quit", [])
b = issues.setdefault("menu.quit", [])
b.append("missing")
c = issues.update({"menu.options": ["new"]})
d = issues.pop("menu.start")

print(a)
print(b)
print(c)
print(d)
print(issues)
```

答题区：

```text

```

### C2. 视图对象 vs 列表快照（6 分）

预测输出，并解释 `view` 和 `snapshot` 的区别。

```python
d = {"a": 1, "b": 2}
view = d.keys()
snapshot = list(d.keys())
d["c"] = 3

print(view)
print(snapshot)
```

答题区：

```text

```

### C3. 字典浅拷贝（6 分）

预测输出，并解释为什么 `copy()` 后内部列表仍会共享。

```python
original = {"tags": ["ui"]}
shallow = original.copy()
shallow["tags"].append("reviewed")

print(original)
print(shallow)
print(original is shallow)
print(original["tags"] is shallow["tags"])
```

答题区：

```text

```

---

## D. 文件、文本、字节、JSON/CSV 边界（25 分）

### D1. 路径字符串 vs 文件对象（6 分）

解释下面三层分别是什么：`path`、`f`、`text`。

```python
path = "resource.json"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()
```

答题区：

```text

```

### D2. `str`、`bytes`、编码和解码（6 分）

预测输出类型，并解释边界。

```python
text = "HP药水"
data = text.encode("utf-8")
again = data.decode("utf-8")

print(type(text).__name__, len(text))
print(type(data).__name__, len(data))
print(type(again).__name__, again == text)
```

答题区：

```text

```

### D3. JSON 文本 vs Python dict/list（7 分）

解释下面流程中每一层是什么，不要把 JSON object 和 Python dict 混说。

```python
import json

json_text = '{"menu.start": "Start", "menu.quit": "Quit"}'
data = json.loads(json_text)
report_text = json.dumps(data, ensure_ascii=False, indent=2)
```

答题区：

```text

```

### D4. CSV 表头和 `csv.DictReader`（6 分）

为什么本地化术语表 CSV 通常需要表头？`DictReader` 读出的一行更接近列表、元组还是字典？有什么边界要注意？

答题区：

```text

```

---

## E. 阶段综合项目和核心对象类型收束（15 分）

### E1. 类型选型（8 分）

为“游戏本地化资源审计工具”选择合适对象类型，并解释理由：

| 需求 | 你的选择 | 理由 |
| --- | --- | --- |
| 保存源语言 key 到文本的映射 |  |  |
| 保存所有待报告 issue，并按 key 排序 |  |  |
| 表示单条稳定 issue 记录 |  |  |
| 检查缺失 key、额外 key、共同 key |  |  |
| 统计重复 key |  |  |
| 输出机器可读 JSON 报告 |  |  |

### E2. CLI 控制流（7 分）

不运行代码，预测下面命令的大体行为：它读取哪些文件？输出给人读还是给机器读？`--observe` 会额外展示什么？如果 `--output` 指定文件，写入边界发生在哪里？

```powershell
python projects\localization_resource_auditor\localization_auditor.py --format json --observe --output report.json
```

答题区：

```text

```
