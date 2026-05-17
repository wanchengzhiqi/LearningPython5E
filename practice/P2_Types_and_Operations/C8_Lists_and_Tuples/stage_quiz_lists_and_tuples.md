# Stage Quiz: Lists and Tuples

本测验用于当前小阶段：Python 列表和元组。

从本阶段目标看，你需要检验自己是否能稳定地区分：

- 列表对象 vs 名字绑定
- 原地修改 vs 重新绑定
- 列表方法返回值 vs 被修改的列表对象
- 切片读取 vs 切片赋值
- 浅拷贝 vs 深拷贝
- 容器显示形式 vs 元素对象本体
- 元组不可变 vs 元组内部可变元素
- `==` 相等性 vs `is` 身份
- 列表、元组、字符串作为序列类型的共性与差异

建议答题方式：

1. 第一遍不要运行代码，先写出预测结果、对象身份变化和理由。
2. 第二遍用 Python 3.9.13 验证，并标注“验证前预测”和“验证后修正”。
3. 遇到列表或元组细节，尽量按这些层次解释：源码中写了什么、创建了什么对象、哪些名字绑定到哪些对象、哪一步原地修改、哪一步重新绑定、显示形式为什么这样。
4. 本卷不包含参考答案。你作答后可以把答案发给我审批。

总分：100 分。

---

## A. 对象、绑定与方法返回值（25 分）

### A1. 赋值是否复制列表（6 分）

预测下面代码的输出，并解释 `a`、`b` 是否绑定到同一个列表对象。

```python
a = ["start", "load"]
b = a
b.append("quit")
print(a)
print(b)
print(a is b)
print(a == b)
```

答题区：

```text

```

### A2. 方法返回值陷阱（7 分）

解释下面代码为什么容易写错。`result` 的值是什么？`items` 最后是什么？

```python
items = ["potion"]
result = items.append("ether")
print(result)
print(items)
```

答题区：

```text

```

### A3. `+` 与 `+=` 的边界（7 分）

分别说明下面两段代码中哪个名字发生重新绑定，哪个列表对象被原地修改。

```python
left = ["a"]
watcher = left
combined = left + ["b"]

items = ["a"]
observer = items
items += ["b"]
```

答题区：

```text

```

### A4. `==` 与 `is`（5 分）

解释为什么下面两个判断可能一个为真，一个为假。

```python
x = [1, 2]
y = [1, 2]
print(x == y)
print(x is y)
```

答题区：

```text

```

---

## B. 切片、排序、嵌套列表与拷贝（35 分）

### B1. 切片读取 vs 切片赋值（8 分）

预测输出，并说明哪一步创建新列表，哪一步原地修改旧列表。

```python
items = ["start", "load", "quit"]
part = items[1:]
alias = items
items[1:2] = ["settings", "save"]

print(part)
print(items)
print(alias)
print(alias is items)
```

答题区：

```text

```

### B2. 排序的对象效果（7 分）

预测 `result`、`records`、`by_key` 的关系，并解释 `sort()` 与 `sorted()` 的区别。

```python
records = [("b", 2), ("a", 3), ("c", 1)]
result = records.sort(key=lambda item: item[1])
by_key = sorted(records, key=lambda item: item[0])

print(result)
print(records)
print(by_key)
print(by_key is records)
```

答题区：

```text

```

### B3. 嵌套列表重复陷阱（8 分）

预测输出，并解释 `bad[0] is bad[1]` 为什么重要。

```python
bad = [[0] * 3] * 3
good = [[0] * 3 for _ in range(3)]

bad[0][0] = 99
good[0][0] = 99

print(bad)
print(good)
print(bad[0] is bad[1])
print(good[0] is good[1])
```

答题区：

```text

```

### B4. 浅拷贝与深拷贝（8 分）

解释下面代码中 `shallow` 和 `deep` 的差异。

```python
import copy

original = [["menu.start"], ["item.potion"]]
shallow = original[:]
deep = copy.deepcopy(original)

original[0].append("changed")
original.append(["new.key"])

print(original)
print(shallow)
print(deep)
```

答题区：

```text

```

### B5. 默认参数共享（4 分）

指出下面函数的问题，并写出修正版。

```python
def collect(key, bucket=[]):
    bucket.append(key)
    return bucket
```

答题区：

```text

```

---

## C. 元组、解包与工程边界（25 分）

### C1. 逗号与圆括号（5 分）

分别写出下面表达式的类型和值。

```python
a = (1)
b = (1,)
c = 1, 2, 3
d = ()
```

答题区：

```text

```

### C2. 元组不可变的真实含义（7 分）

预测输出，并说明哪一步不允许，哪一步允许。

```python
record = ("menu.start", "Start", ["ui"])

try:
    record[1] = "Begin"
except TypeError as exc:
    print(type(exc).__name__)

record[2].append("reviewed")
print(record)
```

答题区：

```text

```

### C3. 解包与扩展解包（6 分）

预测各名字绑定到什么对象，并指出 `middle` 的类型。

```python
first, *middle, last = ("start", "load", "settings", "quit")
print(first)
print(middle)
print(last)
print(type(middle).__name__)
```

答题区：

```text

```

### C4. `*args` 与函数多返回值（7 分）

解释下面两处“组包 / 解包”分别发生在哪里。

```python
def split_key(key):
    namespace, name = key.split(".", 1)
    return namespace, name

def observe(*args):
    return args

result = split_key("item.potion")
namespace, name = result
values = observe("menu.start", "item.potion")
```

答题区：

```text

```

---

## D. 游戏本地化记录设计题（15 分）

你要处理若干本地化记录，每条记录包含：

```text
key, source, translation, tags
```

要求：

- 记录集合需要支持追加、删除、排序、过滤。
- 单条记录不希望被随意改动字段。
- 需要检查重复 key、空翻译、真实换行与字面量 `\n` 混淆、占位符是否保留。
- 需要避免共享可变 `tags` 导致的误修改。

请设计你会使用的 Python 数据结构，并说明为什么。可以选择 `list`、`tuple`、`namedtuple`、`dict`、`set`、浅拷贝或深拷贝，但必须解释对象共享和可变性边界。

答题区：

```text

```

---

## 本阶段自查清单

```text
1. 我能解释 a = b 为什么不复制列表对象。
2. 我能解释 append、extend、sort、reverse 为什么返回 None。
3. 我能区分 + 创建新列表，+= 原地扩展列表。
4. 我能区分切片读取和切片赋值。
5. 我能解释 [[0] * 3] * 3 的共享引用问题。
6. 我能解释浅拷贝只复制外层容器。
7. 我能解释元组不可变不等于元组内部所有对象都不可变。
8. 我知道真正创建元组的是逗号。
9. 我知道赋值解包中的 *target 收集为列表，而函数定义中的 *args 收集为元组。
10. 我能把列表和元组用于一个小型本地化记录处理工具。
```
