# Stage Quiz: Assignments, Expressions, and Prints

本测验用于当前小阶段：**赋值、表达式语句与输出：名字绑定、原地修改和 `print()` 边界**。

它不只考赋值语法，而是考你是否能把 C10 的“表达式求值 vs 语句执行”模型压到 C11 的具体代码里：右侧表达式何时求值，左侧目标改变什么，增强赋值什么时候原地修改，表达式语句结果是否被丢弃，`print()` 到底返回什么、写到哪里。

总分：100 分。

答题规则：

1. 第一遍不要运行代码，先写预测、对象身份变化、返回值、副作用和理由。
2. 第二遍可以用当前日常学习环境 Python `3.14.5` 验证，并标注“验证前预测”和“验证后修正”。
3. 每道代码题尽量按这条链解释：右侧表达式求值、左侧赋值目标处理、名字绑定变化、对象本体是否被修改、表达式结果是否被丢弃、输出流是否被写入。
4. 本卷不包含参考答案。你作答后交给我审批，我会保留你的原答案并追加批改记录。
5. 若你认为题目本身有歧义，可以直接指出；这也属于本阶段能力的一部分。

---

## A. 概念边界：表达式、语句、返回值与副作用（15 分）

### A1. 赋值语句有没有返回值（5 分）

解释下面两行代码分别包含哪些表达式，哪一行是赋值语句。重点说明为什么不能说“赋值语句返回右侧表达式的值”。

```python
title = "menu.start".upper()
"menu.quit".upper()
```

要求至少说明：

1. 右侧表达式求值得到什么对象；
2. `title = ...` 执行后改变了什么；
3. 第二行在脚本文件中是否会自动显示；
4. 如果在 REPL 中输入第二行，为什么可能看到回显。

答题区：

```text
验证前预测：

第一行：
title = "menu.start".upper()
这一整行是赋值语句，不是表达式。它包含右侧的函数/方法调用表达式："menu.start".upper()，右侧表达式先求值。"menu.start" 是字符串对象，.upper() 方法调用会返回一个新的字符串对象："MENU.START"，然后赋值语句左侧的名字 title 被绑定到这个新字符串对象。所以第一行的执行效果是：title 绑定到 "MENU.START"。但不能说 title = "menu.start".upper() 这个赋值语句“返回了”"MENU.START"。普通赋值语句是语句，不是表达式；它有执行效果，但不能作为表达式产生一个可继续使用的求值结果。
第二行：
"menu.quit".upper()
这一行是表达式语句。它包含一个方法调用表达式："menu.quit".upper()，表达式求值得到新的字符串对象："MENU.QUIT"。如果这行写在 .py 脚本文件中，表达式确实会被求值，但求值结果没有被绑定、没有被传给 print、也没有写入任何输出流，所以通常不会自动显示。如果在 REPL / Python Console 中输入第二行，交互式解释器会对非 None 的表达式求值结果进行回显，通常显示它的 repr 形式，所以可能看到：'MENU.QUIT'

验证后修正：

无需修正。关键结论是：
1. 右侧表达式 "menu.start".upper() 求值得到字符串对象 "MENU.START"；
2. title = ... 改变的是当前命名空间中名字 title 的绑定；
3. 第二行在脚本中通常不会自动显示；
4. 第二行在 REPL 中可能显示，是交互式环境的回显机制，不是表达式自身的输出副作用。
```

### A2. 返回值与副作用分离（5 分）

预测输出，并解释 `append()`、`sorted()`、`print()` 三者的返回值和副作用边界。

```python
items = []

a = items.append("menu.start")
b = sorted(items)
c = print(items)

print(a)
print(b)
print(c)
print(items)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. items = []
右侧 [] 创建一个新的空列表对象，名字 items 绑定到该列表对象。
2. a = items.append("menu.start")
右侧表达式 items.append("menu.start") 先求值。items.append(...) 的主要作用是副作用：原地修改 items 绑定的列表对象，把 "menu.start" 追加进去。此时 items 绑定的列表对象变成：["menu.start"]，但 list.append() 的返回值是 None。所以 a 绑定到 None。
3. b = sorted(items)
sorted(items) 会读取 items 中的元素，返回一个新的排序后的列表对象。它不会原地修改 items。因为 items 目前只有一个元素，所以 sorted(items) 返回：["menu.start"]。于是 b 绑定到这个新列表对象。
4. c = print(items)
print(items) 会把 items 的字符串表示写入默认输出流 sys.stdout，产生输出副作用：['menu.start']。但 print() 返回 None。所以 c 绑定到 None。
接下来：
print(a) 输出 None
print(b) 输出 ['menu.start']
print(c) 输出 None
print(items) 输出 ['menu.start']
因此完整输出为：
['menu.start']
None
['menu.start']
None
['menu.start']

验证后修正：

无需修正。边界总结：
append()：
- 副作用：原地修改列表；
- 返回值：None。

sorted()：
- 副作用：通常没有修改原列表；
- 返回值：新的排序列表。

print()：
- 副作用：文本写入某个文件流；
- 返回值：None。
```

### A3. 工程表述纠偏（5 分）

逐条判断下面说法是否准确；若不准确，请改写成更精确的说法。

```text
1. x = expr 会返回 expr 的值。
2. print("ok") 的值就是屏幕上出现的 ok。
3. items.append(x) 会返回修改后的 items。
4. 脚本里的裸表达式没显示，所以它没有被求值。
5. 表达式语句只要没有保存结果，就一定没有副作用。
```

答题区：

```text
验证前预测：

1. x = expr 会返回 expr 的值。
不准确。更精确的说法：
x = expr 是赋值语句，不是表达式。它会先求值右侧表达式 expr，得到某个对象，然后让左侧赋值目标 x 绑定到这个对象。普通赋值语句有执行效果，但不能说它“返回 expr 的值”。
2. print("ok") 的值就是屏幕上出现的 ok。
不准确。更精确的说法：
print("ok") 是函数调用表达式。它的副作用是把 "ok" 写入默认输出流 sys.stdout，通常显示在屏幕上；但这个调用表达式的返回值是 None。因此，屏幕上出现的 ok 是输出副作用，不是 print("ok") 的返回值。
3. items.append(x) 会返回修改后的 items。
不准确。更精确的说法：
items.append(x) 求值的副作用是原地修改 items 绑定的列表对象，把 x 追加进去；但 list.append() 的返回值是 None，不是修改后的列表。
4. 脚本里的裸表达式没显示，所以它没有被求值。
不准确。更精确的说法：
脚本里的裸表达式作为表达式语句仍然会被求值，只是求值结果通常不会自动显示。如果表达式有副作用，副作用仍然会发生。
5. 表达式语句只要没有保存结果，就一定没有副作用。
不准确。更精确的说法：
表达式语句即使没有保存求值结果，也可能有副作用。例如 items.append(x) 会修改列表，print(x) 会写入输出流，logger.warning(...) 会记录日志。是否有副作用取决于表达式求值过程中做了什么，而不是结果有没有被保存。

验证后修正：

无需修正。
```

---

## B. 赋值目标、链式赋值与解包（18 分）

### B1. 链式赋值与共享对象（6 分）

预测输出，并说明哪些名字绑定到同一个对象，哪一步是原地修改。

```python
source = target = []
snapshot = source

source.append("menu.start")
target = target + ["menu.quit"]

print(source)
print(target)
print(snapshot)
print(source is snapshot)
print(source is target)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. source = target = []
右侧 [] 只求值一次，创建一个新的空列表对象。名字 source 和 target 都绑定到这个同一个列表对象。
2. snapshot = source
右侧 source 求值得到当前绑定的列表对象。snapshot 也绑定到同一个列表对象。此时：source、target、snapshot 三个名字都绑定同一个列表对象 []。
3. source.append("menu.start")
source.append(...) 通过名字 source 找到这个共享列表对象，并原地修改它。此时同一个列表对象变成：["menu.start"]。因为 source、target、snapshot 仍然绑定同一个对象，所以三者观察到的对象内容都变了。
4. target = target + ["menu.quit"]
右侧 target + ["menu.quit"] 先求值。target 当前绑定的旧列表内容是 ["menu.start"]。列表加法会创建一个新列表：["menu.start", "menu.quit"]，然后左侧名字 target 被重新绑定到这个新列表对象。注意：这一步没有修改旧列表对象，而是让 target 改绑到新列表。source 和 snapshot 仍然绑定旧列表对象 ["menu.start"]。
所以输出为：
['menu.start']
['menu.start', 'menu.quit']
['menu.start']
True
False

验证后修正：

无需修正。对象关系：
source 和 snapshot 最终仍绑定同一个旧列表对象；
target 最终绑定到由 target + ["menu.quit"] 产生的新列表对象。
原地修改发生在：
source.append("menu.start")
重新绑定发生在：
target = target + ["menu.quit"]
```

### B2. 右侧先求值与安全交换（6 分）

预测输出，并解释为什么 `left, right = right, left` 不会先覆盖其中一个名字。

```python
left = ["source"]
right = ["target"]

left, right = right, left
left.append("checked")

print(left)
print(right)
```

继续回答：下面这行代码会发生什么？为什么？

```python
a, b = ["menu.start"]
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. left = ["source"]
创建列表对象 ["source"]，left 绑定它。
2. right = ["target"]
创建另一个列表对象 ["target"]，right 绑定它。
3. left, right = right, left
这是解包赋值。右侧先整体求值。赋值之前：left 绑定 ["source"]；right 绑定 ["target"]，右侧 right, left 先求值，得到类似：(["target"], ["source"])，然后左侧目标按位置绑定：left 绑定原来 right 指向的列表 ["target"]；right 绑定原来 left 指向的列表 ["source"]，所以不会先覆盖其中一个名字，因为右侧在任何左侧绑定改变之前已经完整求值。
4. left.append("checked")
此时 left 绑定的是原来的 right 指向的 ["target"] 列表。append 原地修改该列表，变成：["target", "checked"]。right 绑定的是另一个列表 ["source"]，不受影响。
所以输出为：
['target', 'checked']
['source']
继续回答：
a, b = ["menu.start"]这行代码会在执行阶段报错：ValueError: not enough values to unpack 原因是：左侧有两个普通目标 a 和 b，没有星号目标；右侧列表 ["menu.start"] 只有一个元素。解包赋值要求右侧可迭代对象产生的元素数量与左侧目标数量完全匹配。因此在这里，右侧元素太少，无法给 b 提供值。

验证后修正：

无需修正。
```

### B3. 星号解包、嵌套解包与共享内部对象（6 分）

预测输出，并说明 `tags` 是否是新列表，`rest` 是否是新列表，二者共享的对象层级有什么不同。

```python
entry = ("menu.start", ("Start Game", "开始游戏"), ["ui", "main"])

key, (source_text, target_text), tags = entry
head, *rest = entry

tags.append("checked")
rest.append("extra")

print(key)
print(source_text, target_text)
print(entry)
print(rest)
print(entry[2] is tags)
print(rest[-1])
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. entry = ("menu.start", ("Start Game", "开始游戏"), ["ui", "main"])
entry 绑定到一个三元素元组：
(
    "menu.start",
    ("Start Game", "开始游戏"),
    ["ui", "main"]
)
要注意的是：元组的第三个元素是一个可变列表对象。
2. key, (source_text, target_text), tags = entry
右侧 entry 求值得到该元组对象。左侧按结构解包：key 绑定 "menu.start"；(source_text, target_text) 继续解包第二个元素 ("Start Game", "开始游戏")：source_text 绑定 "Start Game"；target_text 绑定 "开始游戏"；tags 绑定 entry 第三个元素，也就是列表对象 ["ui", "main"]。注意：tags 不是新列表，它绑定的是 entry[2] 里那个已有列表对象。
3. head, *rest = entry
右侧 entry 再次被解包。head 绑定 entry 的第一个元素 "menu.start"；rest 作为星号目标，收集剩余两个顶层元素，生成一个新的列表：
[
    ("Start Game", "开始游戏"),
    ["ui", "main"]
]
注意：rest 这个外层列表是新列表。但 rest[1] 引用的是 entry[2] 中同一个内部列表对象，不是复制出来的新内部列表。
4. tags.append("checked")
tags 绑定 entry[2] 的列表对象，所以 append 原地修改这个列表。entry 的第三个元素仍然是同一个列表对象，但内容变成：["ui", "main", "checked"]，因此 entry 现在表现为：("menu.start", ("Start Game", "开始游戏"), ["ui", "main", "checked"])。同时 rest[1] 也会看到这个内部列表的变化。
5. rest.append("extra")
rest 是星号解包生成的新列表。对 rest 追加 "extra" 只修改 rest 这个新列表本身，不会改变 entry 的顶层结构。
最终输出：
menu.start
Start Game 开始游戏
('menu.start', ('Start Game', '开始游戏'), ['ui', 'main', 'checked'])
[('Start Game', '开始游戏'), ['ui', 'main', 'checked'], 'extra']：
True
extra

验证后修正：

无需修正。重点：
tags 不是新列表，它绑定 entry[2] 的原内部列表对象；
rest 是新列表；
但 rest 的第二个元素和 entry[2] 共享同一个内部列表对象。
```

---

## C. 属性、下标、切片赋值与对象协议（15 分）

### C1. 赋值左侧不一定是名字（5 分）

预测输出，并分别说明三条赋值语句改变的是名字绑定、对象属性，还是容器内容。

```python
class Entry:
    pass

entry = Entry()
record = {"key": "menu.start", "tags": ["ui"]}
keys = ["menu.start", "menu.quit", "menu.options"]

entry.key = record["key"]
record["tags"] = record["tags"] + ["checked"]
keys[1:] = ["menu.settings"]

print(entry.key)
print(record)
print(keys)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. entry = Entry()
创建 Entry 实例对象，名字 entry 绑定到该对象。
2. record = {"key": "menu.start", "tags": ["ui"]}
创建字典对象，名字 record 绑定到该字典。字典中的 "tags" 对应一个列表对象 ["ui"]。
3. keys = ["menu.start", "menu.quit", "menu.options"]
创建列表对象，名字 keys 绑定到该列表。
4. entry.key = record["key"]
右侧 record["key"] 先求值，得到字符串对象 "menu.start"。左侧 entry.key 是属性赋值目标。它不是重新绑定 entry，而是在 entry 绑定的对象上设置属性 key，使 entry.key 绑定到 "menu.start"。改变的是对象属性。
5. record["tags"] = record["tags"] + ["checked"]
右侧先求值：record["tags"] 当前是列表 ["ui"]。record["tags"] + ["checked"] 创建一个新列表：["ui", "checked"]。左侧 record["tags"] 是字典下标赋值目标，它会把 record 这个字典中 "tags" 键对应的值替换为这个新列表。注意：这里不是原地修改旧的 ["ui"] 列表，而是创建新列表并写回字典对应 key。改变的是容器 record 的内容。
6. keys[1:] = ["menu.settings"]
右侧 ["menu.settings"] 创建一个新列表作为可迭代对象。左侧 keys[1:] 是切片赋值目标。它会把 keys 中从下标 1 到末尾的部分：["menu.quit", "menu.options"]，替换为：["menu.settings"]，所以 keys 变成：["menu.start", "menu.settings"]。改变的是列表对象 keys 的内部内容，并且列表长度变短。
最终的输出为：
menu.start
{'key': 'menu.start', 'tags': ['ui', 'checked']}
['menu.start', 'menu.settings']

验证后修正：

无需修正。三条赋值语句（事实上，给定代码中共有六条赋值语句。基于本题背景，我认为题干中的“三条赋值语句”特指代码片段中位置靠后的那三条赋值语句）分别改变：
entry.key = ...
改变对象属性。

record["tags"] = ...
改变字典对象内部某个 key 对应的 value。

keys[1:] = ...
改变列表对象内部一段切片内容。
```

### C2. 下标赋值 vs 修改旧对象（5 分）

预测输出，并说明 `first` 为什么不会跟着 `rows[0] = ...` 重新绑定。

```python
rows = [
    {"key": "menu.start", "tags": ["ui"]},
    {"key": "menu.quit", "tags": ["ui"]},
]

first = rows[0]
snapshot = rows[:]

rows[0]["tags"].append("checked")
rows[0] = {"key": "menu.start", "tags": ["rebound"]}

print(first)
print(snapshot[0])
print(rows[0])
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. rows 绑定到一个列表对象。该列表中有两个字典对象。
2. first = rows[0]
rows[0] 求值得到第一个字典对象：{"key": "menu.start", "tags": ["ui"]}，first 绑定到这个字典对象。
3. snapshot = rows[:]
rows[:] 进行浅拷贝，创建一个新的外层列表对象。但浅拷贝不会复制内部字典对象。因此 snapshot 是新列表，但 snapshot[0] 和 rows[0] 此时绑定同一个第一个字典对象。
4. rows[0]["tags"].append("checked")
先通过 rows[0] 找到第一个字典对象，再通过 ["tags"] 这个键索引找到字典对象中名为 "tags" 的键对应的值：即列表对象 ["ui"]，然后 append 原地修改这个列表，列表变成了：["ui", "checked"]。因为 first 和 snapshot[0] 都绑定同一个第一个字典对象，所以它们都会看到这个内部列表的变化。
5. rows[0] = {"key": "menu.start", "tags": ["rebound"]}
右侧创建一个新字典对象。左侧 rows[0] 是下标赋值目标。整条赋值语句的执行效果是：把 rows 这个列表下标 0 的位置替换成新字典。注意：这一步只是替换 rows[0] 这个列表位置保存的引用，不会让 first 重新绑定。first 仍然绑定原来的旧字典对象。snapshot[0] 也仍然绑定原来的旧字典对象。
所以输出为：
{'key': 'menu.start', 'tags': ['ui', 'checked']}
{'key': 'menu.start', 'tags': ['ui', 'checked']}
{'key': 'menu.start', 'tags': ['rebound']}

验证后修正：

无需修正。first 之所以不会跟着 rows[0] = ... 重新绑定，是因为 first 是一个独立名字，已经绑定到旧字典对象。这里的下标赋值只改变 rows 列表内部下标 0 的位置所保存的引用，不会自动修改其他名字的绑定。
```

### C3. 工程边界题：对象协议可能有副作用（5 分）

下面的类把下标赋值记录到 `history`。预测输出，并说明为什么 `store["menu.start"] = "Start"` 不只是“给变量改值”。

```python
class AuditStore:
    def __init__(self):
        self.data = {}
        self.history = []

    def __setitem__(self, key, value):
        self.history.append(("set", key, value))
        self.data[key] = value


store = AuditStore()
store["menu.start"] = "Start"
store["menu.quit"] = "Quit"

print(store.data)
print(store.history)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. store = AuditStore()
创建 AuditStore 实例对象，名字 store 绑定到该实例对象。实例化过程中特殊方法 __init__ 默认自动调用，给实例对象设置两个属性的值：store.data 绑定到空字典 {}；store.history 绑定到空列表 []。
2. store["menu.start"] = "Start"
左侧不是名字赋值，而是下标赋值目标。对本题的自定义对象来说，下标赋值会调用对象的 __setitem__ 方法。因此会执行：store.__setitem__("menu.start", "Start")。而在 __setitem__ 内部：
self.history.append(("set", key, value))
会把 ("set", "menu.start", "Start") 追加到 history 列表；
self.data[key] = value
会向 data 字典新增键"menu.start"，并将该键引用映射至指向字符串对象 "Start" 的值引用。
3. store["menu.quit"] = "Quit"
同理，会向 history 列表追加：("set", "menu.quit", "Quit")；向 data 字典新增键"menu.quit"，并将该键引用映射至指向字符串对象 "Quit" 的值引用。
最终输出为：
{'menu.start': 'Start', 'menu.quit': 'Quit'}
[('set', 'menu.start', 'Start'), ('set', 'menu.quit', 'Quit')]

验证后修正：

无需修正。store["menu.start"] = "Start" 不只是“给变量改值”。它是对 store 这个对象执行下标赋值，触发该对象类型定义的 __setitem__ 协议逻辑。这个逻辑既修改了 store.data，也修改了 store.history，因此有明确的对象内部副作用。
```

---

## D. 增强赋值：原地修改机会 vs 重新绑定（18 分）

### D1. `+=` 不总是等同于 `x = x + y`（6 分）

预测输出，并解释 `a += ...` 与 `b = b + ...` 对别名可见性的差异。

```python
a = ["menu.start"]
alias_a = a
a += ["menu.quit"]

b = ["menu.start"]
alias_b = b
b = b + ["menu.quit"]

print(a)
print(alias_a)
print(a is alias_a)

print(b)
print(alias_b)
print(b is alias_b)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. a = ["menu.start"]
创建列表对象，a 绑定它。
2. alias_a = a
alias_a 也绑定同一个列表对象。
3. a += ["menu.quit"]
右侧 ["menu.quit"] 创建一个新列表。对列表对象来说，+= 通常会调用原地加法逻辑，效果接近 extend，即把右侧可迭代对象中的元素追加到原列表中。所以 a 原来绑定的列表对象被原地修改为：["menu.start", "menu.quit"]。但要注意的是：a 仍然绑定这个原列表对象，alias_a 也绑定这个同一个原列表对象。
4. b = ["menu.start"]
创建另一个列表对象，b 绑定它。
5. alias_b = b
alias_b 也绑定这个列表对象。
6. b = b + ["menu.quit"]
右侧 b + ["menu.quit"] 创建一个新列表对象：["menu.start", "menu.quit"]，然后名字 b 被重新绑定到这个新列表对象。alias_b 仍然绑定旧列表对象：["menu.start"]。
综上，完整输出为：
['menu.start', 'menu.quit']
['menu.start', 'menu.quit']
True
['menu.start', 'menu.quit']
['menu.start']
False

验证后修正：

无需修正。差异：
a += ... 对列表原地修改，别名可见；
b = b + ... 创建新列表并重新绑定 b，别名 alias_b 不受影响。
```

### D2. 不可变对象上的增强赋值（4 分）

预测输出，并说明 `count += 1` 与 `text += "!"` 改变的是对象本体还是名字绑定。

```python
count = 0
old_count = count
count += 1

text = "menu"
old_text = text
text += ".start"

print(count)
print(old_count)
print(count is old_count)

print(text)
print(old_text)
print(text is old_text)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. count = 0
count 绑定到整数对象 0。
2. old_count = count
old_count 也绑定到整数对象 0。
3. count += 1
整数是不可变对象，不能把整数对象 0 原地改成 1。所以 count += 1 会通过二元运算 0 + 1 产生新的整数对象 1，然后让名字 count 重新绑定到 1。old_count 仍然绑定到 0。
4. text = "menu"
text 绑定到字符串对象 "menu"。
5. old_text = text
old_text 也绑定到同一个字符串对象 "menu"。
6. text += ".start"
字符串是不可变对象，不能原地修改。因此 text += ".start" 会通过字符串的拼接运算创建新字符串对象 "menu.start"，然后让 text 重新绑定到这个新字符串对象。old_text 仍然绑定旧字符串 "menu"。
综上，完整输出为：
1
0
False
menu.start
menu
False

验证后修正：

无需修正。结论：
count += 1 改变的是名字 count 的绑定，不是整数对象本体；
text += ".start"（题干中写的是 `text += "!"` ，基于本题背景，我还是改用了代码片段中的源码，尽管二者在这里表达的结论一致） 改变的是名字 text 的绑定，不是字符串对象本体。
```

### D3. tuple 里装 list 的高级边界（4 分）

预测输出，并解释为什么异常发生后内部列表仍然变了。

```python
box = (["menu.start"],)

try:
    box[0] += ["menu.quit"]
except TypeError as exc:
    error = type(exc).__name__

print(box)
print(error)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. box = (["menu.start"],)
box 绑定到一个单元素元组。该元组的第一个元素是列表对象：["menu.start"]。
2. box[0] += ["menu.quit"]
此处的增强赋值大致包含如下阶段：
第一，读取左侧目标 box[0]，得到内部列表对象 ["menu.start"]。
第二，对这个列表执行 += ["menu.quit"]。列表支持原地扩展，因此内部列表先被修改为：["menu.start", "menu.quit"]。
第三，增强赋值还要把运算结果赋回原来的左侧目标 box[0]。
第四，但 box 是元组，元组不支持下标赋值，不能执行 box[0] = ...。
所以第三/第四阶段发生 TypeError。异常被 except TypeError 捕获，并设置：error = "TypeError"。虽然最终报错被捕获，但上述第二阶段中的列表原地修改已经发生了。因此 box 内部的列表已经变了。
所以，输出为：
(['menu.start', 'menu.quit'],)
TypeError

验证后修正：

无需修正。关键结论：
这说明增强赋值不是事务式操作。即使最后“赋回目标”失败，前面已经发生的原地修改副作用仍然可能保留下来。
```

### D4. `dict |= ...`、`set |= ...` 与输出报告状态（4 分）

预测输出，并说明哪些操作是原地修改。

```python
report = {"missing": 1}
alias_report = report
report |= {"extra": 2}

flags = {"missing"}
alias_flags = flags
flags |= {"extra"}

print(report)
print(alias_report)
print(report is alias_report)

print(flags)
print(alias_flags)
print(flags is alias_flags)
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. report = {"missing": 1}
report 绑定到一个字典对象。
2. alias_report = report
alias_report 也绑定同一个字典对象。
3. report |= {"extra": 2}
dict 的 |= 是原地更新字典。它把右侧字典中的键值对合并进 report 绑定的原字典对象。所以原字典变为：{"missing": 1, "extra": 2}。alias_report 也能看到同一个字典对象的变化。
4. flags = {"missing"}
flags 绑定到一个集合对象。
5. alias_flags = flags
alias_flags 也绑定同一个集合对象。
6. flags |= {"extra"}
set 的 |= 是原地更新集合，把右侧集合中的元素加入 flags 绑定的原集合对象。最终集合包含：{"missing", "extra"}。集合显示顺序不保证，所以可能显示为 {'missing', 'extra'}，也可能显示为 {'extra', 'missing'}。alias_flags 也看到同一个集合对象的变化。
综上，完整输出是：
{'missing': 1, 'extra': 2}
{'missing': 1, 'extra': 2}
True
{'missing', 'extra'}（只做集合内部元素保证，不保证显示顺序和预测的一致）
{'missing', 'extra'}（只做集合内部元素保证，不保证显示顺序和预测的一致）
True

验证后修正：

无需修正。原地修改发生在：
report |= {"extra": 2}
flags |= {"extra"}
```

---

## E. `print()`、输出流与表达式语句（16 分）

### E1. `print()` 的返回值和 `StringIO` 输出流（6 分）

预测输出，并说明 `result` 与 `buffer.getvalue()` 分别是什么。

```python
from io import StringIO

buffer = StringIO()
result = print("missing", "menu.quit", sep=": ", end="!\n", file=buffer)

print(result)
print(buffer.getvalue())
```

答题区：

```text
验证前预测：

给定代码逐步分析：
1. buffer = StringIO()
创建一个内存文本流对象，名字 buffer 绑定它。
2. result = print("missing", "menu.quit", sep=": ", end="!\n", file=buffer)
print() 会把两个对象转换为字符串，然后用 sep=": " 连接：missing: menu.quit，再追加 end="!\n"，所以实际写入 buffer 的文本为：missing: menu.quit!\n。注意：这次 print 的输出副作用写入的是 buffer，而不是 sys.stdout，所以此时控制台不会显示 missing: menu.quit!。此外，print() 的返回值是 None，所以 result 绑定到 None。
综上，控制台的可见输出为：
None（注意：此时 print 调用的参数sep、end、file指向默认值！）
missing: menu.quit!（注意：此时 print 调用的参数sep、end、file指向默认值，此外 buffer.getvalue() 求值得到当前内存文本流的所有内容（即一个尾端包含了换行符的字符串对象："missing: menu.quit!\n"），因此，这里的输出实际上会额外多出一行空行！）

验证后修正：

无需修正。说明：
result 是 None；
buffer.getvalue() 是字符串 "missing: menu.quit!\n"。
```

### E2. stdout、stderr 与文件对象边界（4 分）

解释下面三种输出的工程差异。无需预测具体控制台顺序，重点说明“写到哪里”和“返回什么”。

```python
import sys

a = print("human report")
b = print("warning: missing menu.quit", file=sys.stderr)

with open("audit.log", "w", encoding="utf-8") as log:
    c = print("missing: menu.quit", file=log, flush=True)
```

要求至少说明：

1. `a`、`b`、`c` 分别绑定到什么；
2. 三次输出分别写向哪里；
3. `flush=True` 改变了什么，不改变什么；
4. 文件写入有哪些外部副作用风险。

答题区：

```text
验证前预测：

给定代码逐步分析：
1. a = print("human report")
print() 未显式指定 file 参数，因此默认写入 sys.stdout，也就是标准输出流。通常显示在终端或被 stdout 重定向捕获。print() 的返回值是 None，因此：a 绑定到 None。
2. b = print("warning: missing menu.quit", file=sys.stderr)
这次显式指定 file=sys.stderr，因此输出写入标准错误流。工程上，stderr 常用于警告、错误、诊断信息。它可能和 stdout 显示在同一个终端窗口中，但它是不同的流；shell 重定向 stdout 时，stderr 通常不会自动跟随。print() 的返回值仍然是 None，因此：b 绑定到 None。
3. with open("audit.log", "w", encoding="utf-8") as log:
       c = print("missing: menu.quit", file=log, flush=True)
open(...) 打开文本文件 audit.log，编码使用 utf-8。print(..., file=log) 把文本写入这个文件对象 log，而不是 stdout 或 stderr。flush=True 会在本次 print 写入后强制刷新 log 这个目标流的缓冲，使文本流层面的缓冲尽快推出去。它改变的是刷新时机，不改变写入内容，也不改变 print() 的返回值。因此 c 也绑定到 None。
至于文件写入的外部副作用风险包括：
1. 文件可能创建或覆盖已有 audit.log；
2. 路径、权限、磁盘空间、编码等问题可能导致写入失败；
3. flush=True 不等于绝对保证数据已经物理安全落盘，操作系统层面仍可能有缓存；
4. 如果程序异常中止，需要依赖 with 语句正常退出时关闭文件并刷新，严重崩溃或进程被强杀时不能保证所有缓冲内容完整写出。

验证后修正：

无需修正。综上：
a、b、c 都绑定到 None；
三次输出分别写向 stdout、stderr、audit.log 文件对象；
flush=True 只影响目标流的刷新行为，不改变 print() 的返回值和输出的文本内容。
```

### E3. 表达式语句是否有意义（6 分）

逐条判断下面哪些表达式语句在脚本中通常有意义，哪些通常可疑，并说明理由。

```python
missing_keys.append("menu.quit")
sorted(missing_keys)
print("audit finished")
"menu.start".upper()
logger.warning("missing menu.quit")
```

答题区：

```text
验证前预测：

逐条判断：
1. missing_keys.append("menu.quit")
在脚本中通常有意义。理由：这是方法调用表达式语句。虽然 append() 的返回值是 None，且返回值既没有保存也没有被使用，但它有通常作为主要目的的副作用：原地修改 missing_keys 绑定的列表对象，把 "menu.quit" 追加进去。
2. sorted(missing_keys)
在脚本中通常可疑。理由：sorted(missing_keys) 会返回一个新的排序列表，但不会原地修改 missing_keys。如果这个返回值没有被绑定、没有被传给 print、也没有用于其他表达式，那么排序结果会被丢弃。除非故意测试某些异常或性能，否则在脚本中这通常是无意义代码。更合理写法可能是：sorted_keys = sorted(missing_keys)，或者：print(sorted(missing_keys))。
3. print("audit finished")
在脚本中通常有意义。理由：print() 的返回值虽然是 None，且返回值既没有保存也没有被使用，但它的副作用是把 "audit finished" 写入输出流，作为用户可见的运行提示。
4. "menu.start".upper()
在脚本中通常可疑。理由：这个表达式会返回新字符串 "MENU.START"，但字符串方法 upper() 不会修改原字符串。如果返回值没有被保存或输出，结果会被丢弃，通常没有实际意义。更合理写法可能是：upper_key = "menu.start".upper()，或者：print("menu.start".upper())。
5. logger.warning("missing menu.quit")
在脚本中通常有意义。理由：这是日志调用表达式语句。它的业务价值通常在副作用：向 logger 配置的处理器记录一条 warning 级别日志。即使返回值没有保存，日志记录（"missing menu.quit"）也可能写入控制台、文件或其他日志目标。

验证后修正：

无需修正。总结：
有意义：
missing_keys.append("menu.quit")
print("audit finished")
logger.warning("missing menu.quit")

通常可疑：
sorted(missing_keys)
"menu.start".upper()
```

---

## F. 综合代码阅读：本地化审计摘要（18 分）

### F1. 一段完整审计代码的对象变化（10 分）

预测最终状态，并解释每个关键语句改变了什么。

```python
from io import StringIO

source_rows = [
    ("menu.start", "Start Game"),
    ("menu.quit", "Quit"),
    ("menu.options", "Options"),
]

target = {
    "menu.start": "开始游戏",
    "menu.options": "",
}

missing_count = 0
missing_keys = []
empty_keys = []
report = StringIO()

for key, source_text in source_rows:
    target_text = target.get(key)

    if target_text is None:
        missing_count += 1
        missing_keys.append(key)
        print("missing", key, sep=": ", file=report)
    elif target_text == "":
        empty_keys += [key]
        print("empty", key, sep=": ", file=report)

summary = {
    "missing_count": missing_count,
    "missing_keys": missing_keys,
    "empty_keys": empty_keys,
}

printed = print("done", file=report)
visible = missing_keys + empty_keys
```

要求至少回答：

1. `missing_count`、`missing_keys`、`empty_keys`、`summary`、`printed`、`visible` 最终是什么；
2. `missing_count += 1` 是原地修改还是重新绑定；
3. `missing_keys.append(key)` 的返回值是否被使用；
4. `empty_keys += [key]` 是否原地修改列表；
5. `report.getvalue()` 应该包含哪些文本；
6. `visible = missing_keys + empty_keys` 是否改变原列表。

答题区：

```text
验证前预测：

代码基础数据创建：
source_rows = [
    ("menu.start", "Start Game"),
    ("menu.quit", "Quit"),
    ("menu.options", "Options"),
]
target = {
    "menu.start": "开始游戏",
    "menu.options": "",
}
初始化变量：
missing_count = 0
missing_keys = []
empty_keys = []
report = StringIO()
循环逐步分析：
第一次循环：通过元组解包赋值得到：key 绑定在 "menu.start"；source_text 绑定在 "Start Game"，接着执行赋值语句：target_text = target.get(key)，因为 target 指向的字典中存在名为 "menu.start" 的键，所以 target_text 绑定在该键对应的值对象上，即："开始游戏"。再然后，后续的 if target_text is None: 和 elif target_text == "": 的“真值测试”均未通过，所以它们各自的代码块均跳过不予执行，所以本轮循环不修改 missing_count、missing_keys、empty_keys，也不向 report 写入内容。
第二次循环：通过元组解包赋值得到：key 绑定在 "menu.quit"；source_text 绑定在 "Quit"，接着执行赋值语句：target_text = target.get(key)，因为 target 指向的字典中没有名为 "menu.quit" 的键，所以 target_text 绑定在 get 返回的 None 对象上。再然后，后续的 if target_text is None: 的“真值测试”通过，所以控制流将进入属于这条 if 语句的代码块，但是 elif 子句的代码块将被跳过不予执行。而在被执行的代码块中：首先执行增强赋值语句 missing_count += 1，missing_count 当前绑定整数 0。整数不可变，所以这里不是原地修改整数对象，而是计算 0 + 1 得到新整数对象 1，然后让 missing_count 重新绑定到 1；接着执行方法调用表达式 missing_keys.append(key)，missing_keys 最初绑定到列表对象 []。append 原地修改该列表，在其尾部加入 "menu.quit"。append 返回 None，但返回值没有被保存，也没有被使用，总之，此时有：missing_keys == ["menu.quit"]；最后执行函数调用表达式 print("missing", key, sep=": ", file=report)，这会向 StringIO 对象 report 写入文本：missing: menu.quit\n，print() 也返回 None，但返回值没有被保存。所以本轮循环不修改 empty_keys。
第三次循环：通过元组解包赋值得到：key 绑定在 "menu.options"；source_text 绑定在 "Options"，接着执行赋值语句：target_text = target.get(key)，因为 target 指向的字典中存在名为 "menu.options" 的键，所以 target_text 绑定在 get 返回的该键对应的值对象上，即：""。再然后，后续的 if target_text is None: 的“真值测试”未通过，但是 elif target_text == "": 的“真值测试”通过了，所以控制流将进入属于这条 elif 子句的代码块，而 if 语句的代码块将被跳过不予执行。在被执行的代码块中：首先执行增强赋值语句 empty_keys += [key]，empty_keys 最初绑定到列表对象 []。对列表使用 += 通常原地扩展原列表，在这里会把 key（"menu.options"） 追加至列表尾部，此时有：empty_keys == ["menu.options"]；最后执行函数调用表达式 print("empty", key, sep=": ", file=report)，这会向 StringIO 对象 report 写入文本：empty: menu.options\n，print() 也返回 None，但返回值没有被保存。所以本轮循环不修改 missing_count 和 missing_keys。
循环结束后：
summary = {
    "missing_count": missing_count,
    "missing_keys": missing_keys,
    "empty_keys": empty_keys,
}
这条普通赋值语句执行时，会先创建一个新字典对象，再让名字 summary 绑定它。字典中的键 "missing_keys" 对应的值是 missing_keys 绑定的那个列表对象；"empty_keys" 对应的值是 empty_keys 绑定的那个列表对象，这里没有复制列表。
继续向后顺序执行：
printed = print("done", file=report)
这条普通赋值语句执行时，会先求值函数 print 的调用表达式，求值过程中产生副作用：向 StringIO 对象 report 写入文本：done\n，最后 print() 返回 None，再将名字 printed 绑定到返回的 None 对象上。
visible = missing_keys + empty_keys
右侧先求值。列表加法会创建一个新列表，内容是 missing_keys 和 empty_keys 的拼接：["menu.quit", "menu.options"]，然后 visible 绑定到这个新列表。注意：这一步不会改变 missing_keys，也不会改变 empty_keys。
综上：
1. 最终状态：
missing_count == 1
missing_keys == ["menu.quit"]
empty_keys == ["menu.options"]
summary == {
    "missing_count": 1,
    "missing_keys": ["menu.quit"],
    "empty_keys": ["menu.options"],
}
printed == None
visible == ["menu.quit", "menu.options"]
2. missing_count += 1 是重新绑定。整数不可变，不能原地修改。missing_count += 1 会产生新整数对象 1，并让名字 missing_count 重新绑定到它。
3. missing_keys.append(key) 的返回值没有被使用。append() 的返回值是 None；本代码只是依赖 append 的副作用，即原地修改 missing_keys 列表。
4. empty_keys += [key] 会原地修改列表。empty_keys 绑定的是列表对象，列表的 += 通常原地扩展该列表。
5. report.getvalue() 的文本内容为："missing: menu.quit\nempty: menu.options\ndone\n"
6. visible = missing_keys + empty_keys 不改变原列表。列表 + 会创建一个新列表并让 visible 绑定到它，不会原地修改 missing_keys 或 empty_keys。

验证后修正：

无需修正。
```

### F2. Bug 审查：返回值和副作用混淆（4 分）

下面代码试图收集缺失 key 并返回报告，但有多个 C11 边界错误。指出至少 4 个问题，并给出修正方向。

```python
def collect_missing(source_keys, target_keys):
    missing = []
    report = []

    for key in source_keys:
        if key not in target_keys:
            missing = missing.append(key)
            report = print("missing:", key)

    return report
```

答题区：

```text
验证前预测：

由给定代码片段可得出的 4 个问题是：
问题 1：missing = missing.append(key)
这是错误地把 append() 的返回值当成修改后的列表。missing.append(key) 会原地修改 missing 绑定的列表，但返回 None。因此执行第一次缺失 key 收集时，missing 会被重新绑定为 None。下一次如果再遇到缺失 key，就会尝试 None.append(key)，导致异常抛出： AttributeError。
修正方向：
将这条语句改写成：missing.append(key)，即不要把 append() 的返回值赋回 missing。
问题 2：report = print("missing:", key)
这是错误地把 print() 的返回值当成报告内容。print("missing:", key) 求值的副作用是写入输出流，返回值是 None。因此每次执行缺失 key 的收集时，report 都会被重新绑定为 None，而不是预期的字符串报告或列表报告。
修正方向：
如果要收集报告行，可以写：report.append(f"missing: {key}")。如果要输出给用户，可以写：print("missing:", key)。但不要把 print() 的返回值当业务结果。
问题 3：
当前的函数把“收集数据”和“输出文本”混在一起，而且输出流不可控。print("missing:", key) 默认写向 sys.stdout。调用者无法选择写到文件、StringIO、stderr 或关闭输出。这降低了函数的可复用性和可测试性。
修正方向：
可以增加可选参数 output：
def collect_missing(source_keys, target_keys, output=None):
    ...
如果 output 不为 None，才执行：print("missing:", key, file=output)
问题 4：
函数名 collect_missing 暗示它应该收集缺失项，但 return report 不返回 missing，本意和实现不一致。
修正方向：
函数应返回 missing 或包含 missing 的结构化结果。

验证后修正：

无需修正。
```

### F3. 设计题：返回数据、输出文本、写文件三层分离（4 分）

设计一个函数接口，用于检查本地化缺失 key。要求用文字或伪代码说明：

```text
输入：source_keys、target_keys、可选输出流
输出：给调用者使用的结构化结果
副作用：可选地把人读摘要写到输出流
```

必须说清楚：

1. 哪些变量通过赋值绑定中间结果；
2. 哪些操作会原地修改列表或集合；
3. 函数应该 `return` 什么；
4. 什么时候使用 `print(..., file=...)`；
5. 为什么不要把 `print()` 的返回值当业务结果。

答题区：

```text
验证前设计：

可以设计如下函数接口：
def check_missing_keys(source_keys, target_keys, output=None):
    missing = []

    source_set = set(source_keys)
    target_set = set(target_keys)

    missing_set = source_set - target_set
    missing.extend(sorted(missing_set))

    result = {
        "missing_count": len(missing),
        "missing_keys": missing,
    }

    if output is not None:
        print("Localization missing-key report", file=output)
        print("Missing count:", result["missing_count"], file=output)

        for key in missing:
            print("missing:", key, file=output)

    return result

文字辅助说明：
1. 哪些变量通过赋值绑定中间结果？
missing = []
初始化一个空的用于保存缺失 key 的列表对象，并让名字 missing 绑定它。
source_set = set(source_keys)
创建一个集合对象，用于保存源 key，并让名字 source_set 绑定它。
target_set = set(target_keys)
创建一个集合对象，用于保存目标 key，并让名字 target_set 绑定它。
missing_set = source_set - target_set
通过集合差集运算创建一个新的集合对象，并让 missing_set 绑定它。
result = {...}
创建一个待返回的字典对象，并让 result 绑定它。
2. 哪些操作会原地修改列表或集合？
missing.extend(sorted(missing_set))
只有这一条表达式语句在执行时会原地修改 missing 绑定的列表对象，把缺失 key 追加进去。
在上述设计中：
source_set - target_set
不会原地修改 source_set 或是 target_set，而是创建新集合。
3. 函数应该 return 什么？
函数应该 return 给调用者使用的结构化结果，而不是 return print() 的返回值。
因此设计中 result 绑定的字典对象扮演了函数调用返回值的角色：
{
    "missing_count": len(missing),
    "missing_keys": missing,
}
这样调用者可以继续用于测试、生成 JSON、写 CSV、显示 CLI 摘要或交给其他程序单元处理。
4. 什么时候使用 print(..., file=...)？
只有当调用者传入 output 流对象时，函数才把人类可读摘要写入该流：
if output is not None:
    print(..., file=output)
这样调用者可以选择：
不输出：
result = check_missing_keys(source_keys, target_keys)
输出到控制台：
import sys
result = check_missing_keys(source_keys, target_keys, output=sys.stdout)
输出到内存流：
from io import StringIO
buf = StringIO()
result = check_missing_keys(source_keys, target_keys, output=buf)
输出到文件：
with open("audit.txt", "w", encoding="utf-8") as f:
    result = check_missing_keys(source_keys, target_keys, output=f)
5. 为什么不要把 print() 的返回值当业务结果？
因为 print() 的主要作用是输出副作用，它会把文本写入指定输出流；但它的返回值是 None。如果写：
report = print("missing:", key, file=output)
则 report 得到的是 None，而不是报告字符串。业务结果应该用列表、字典、集合等数据结构保存，然后通过 return 返回；输出文本只是可选副作用，不应该取代结构化返回值。

验证后修正：

无需修正。
```

---

## 作答后提交说明

作答时请直接在每题的“答题区”中填写。你提交后，我会按阶段测验批改规则追加：

- `## Codex 批改记录（逐题审批，YYYY-MM-DD）`
- 建议得分；
- 主要强项；
- 主要修正点；
- 是否通过 `C11_Assignments_Expressions_and_Prints` 小阶段；
- `学习画像更新`，用于同步到 `notes/Python_Learning_Profile.md` 和下一阶段启动模板。

---

## Codex 批改记录（逐题审批，2026-06-19）

### 代码审查结论与主要发现

建议得分：**100 / 100**

阶段判断：**通过 `C11_Assignments_Expressions_and_Prints` 小阶段。**

本次没有发现影响代码行为判断、对象模型、返回值、副作用或工程边界的实质错误。所有预测结果均正确，解释链条完整，D3、E1、F1 等高风险题也已用 Python `3.14.5` 代表性复核通过。

以下是三处**不扣分但建议继续收紧**的术语：

1. C1 中“使 `entry.key` 绑定到字符串”方向正确，但更精确可说：属性赋值把对象引用写入 `entry` 的属性目标，并可能触发 `__setattr__` 协议。属性目标不是当前局部命名空间中的普通名字。
2. E1 中“参数 `sep`、`end`、`file` 指向默认值”建议改成“调用时未显式传入这些参数，因此 `print()` 使用其默认参数值”。“指向”更适合描述对象引用关系。
3. F1 中可进一步区分：`target_text is None` 和 `target_text == ""` 是先求值为布尔结果的条件表达式，随后 `if` / `elif` 对该结果做真值测试。你的运行判断完全正确，只是这层术语还能再细分。

这些都是表达精度建议，不构成概念错误，因此不扣分。

### 分项得分

| 部分 | 得分 |
| --- | ---: |
| A. 概念边界 | 15 / 15 |
| B. 赋值目标、链式赋值与解包 | 18 / 18 |
| C. 属性、下标、切片赋值与对象协议 | 15 / 15 |
| D. 增强赋值 | 18 / 18 |
| E. `print()`、输出流与表达式语句 | 16 / 16 |
| F. 综合代码阅读与设计 | 18 / 18 |
| **总分** | **100 / 100** |

### A. 概念边界（15 / 15）

#### A1（5 / 5）

正确。你准确拆分了方法调用表达式与赋值语句，明确赋值语句有执行效果但不是产生可继续使用结果的表达式；脚本裸表达式与 REPL 回显也分层清楚。

#### A2（5 / 5）

正确。完整输出、`append()` 原地修改并返回 `None`、`sorted()` 创建新列表、`print()` 写流并返回 `None` 均判断准确。

#### A3（5 / 5）

正确。五个错误表述全部被精确纠正，尤其能明确“结果未保存”与“没有副作用”不是同一件事。

### B. 赋值目标、链式赋值与解包（18 / 18）

#### B1（6 / 6）

正确。你准确追踪了 `source`、`target`、`snapshot` 的共享对象关系，并区分 `append()` 原地修改与列表 `+` 后重新绑定。

#### B2（6 / 6）

正确。右侧整体先求值、左侧再绑定的交换模型解释完整；解包数量不足时的 `ValueError` 也判断准确。补充边界：解包失败发生在左侧目标写入前；若 `a`、`b` 原先已有绑定，它们不会因这次失败而被部分覆盖。

#### B3（6 / 6）

正确。你准确区分 `tags` 直接绑定原内部列表、`rest` 是新外层列表、`rest[1]` 仍共享原内部列表。这已经是稳定的对象层级推理。

### C. 属性、下标、切片赋值与对象协议（15 / 15）

#### C1（5 / 5）

正确。三类目标改变的分别是对象属性、字典表项和列表切片；你还主动指出题干“三条赋值语句”与完整代码中赋值语句总数之间的范围歧义，并采用了合理解释。

#### C2（5 / 5）

正确。浅拷贝只创建新外层列表、旧字典对象仍被 `first` 与 `snapshot[0]` 共享；随后 `rows[0] = ...` 只替换 `rows` 的槽位引用。

#### C3（5 / 5）

正确。你不仅预测了 `data` 与 `history`，还准确指出下标赋值会委托给 `__setitem__`，可能执行任意自定义协议逻辑并产生多重副作用。

### D. 增强赋值（18 / 18）

#### D1（6 / 6）

正确。列表 `+=` 的原地修改机会与列表 `+` 创建新对象后的重新绑定解释准确，别名可见性判断无误。

#### D2（4 / 4）

正确。整数和字符串不可变，因此两次增强赋值都创建结果对象并重新绑定名字。你还主动发现题干文字中的 `text += "!"` 与代码中的 `text += ".start"` 不一致，并以实际代码为准；这是很好的规格审查意识。

#### D3（4 / 4）

正确且解释优秀。你准确给出“读取目标 -> 列表原地增强 -> 尝试写回 tuple 槽位 -> 写回失败”的链条，并指出增强赋值不是事务式操作，先发生的副作用不会自动回滚。

#### D4（4 / 4）

正确。`dict |=` 与 `set |=` 都原地更新，别名继续看到同一对象；你也正确保留了集合显示顺序不保证这一边界。

### E. `print()`、输出流与表达式语句（16 / 16）

#### E1（6 / 6）

正确。`result is None`、`buffer.getvalue() == "missing: menu.quit!\n"` 均准确，并且注意到外层 `print(buffer.getvalue())` 会因字符串自带换行和 `print()` 默认 `end` 再产生一个空行。

#### E2（4 / 4）

正确且工程边界完整。stdout、stderr、文件流、`flush=True`、`with` 关闭、权限、磁盘空间、编码、覆盖风险以及“刷新不等于物理持久化”均有覆盖。

#### E3（6 / 6）

正确。你能根据“返回值是否被使用”和“求值是否有有意义副作用”判断表达式语句，而不是机械地把裸调用都视为无效代码。

### F. 综合代码阅读与设计（18 / 18）

#### F1（10 / 10）

正确。最终对象状态、整数重新绑定、两个列表的原地修改、`print()` 返回值、`StringIO` 内容、`summary` 中共享的列表引用，以及 `visible` 的新列表边界全部解释到位。

#### F2（4 / 4）

正确。你识别了 `append()` 返回值误用、`print()` 返回值误用、数据收集与输出副作用耦合、函数名/返回契约不一致四个问题，并给出了结构化结果与可选输出流的修正方向。

#### F3（4 / 4）

正确且具备工程可用性。接口清楚分开输入、中间对象、结构化返回值和可选输出副作用；集合差集、稳定排序、列表原地扩展及多种输出流用法均合理。

## 本阶段末评语与能力判断

你已经稳定掌握 C11 的主干与关键边界：能从“右侧表达式求值 -> 左侧目标处理”解释名字、属性、下标、切片和解包赋值；能追踪共享引用、浅拷贝和重新绑定；能按对象协议判断增强赋值是否原地修改；也能把表达式结果、方法返回值、输出文本和外部副作用严格分开。

本次满分不是因为只写对了输出，而是因为你的解释能够持续落到对象身份、引用关系、协议调用和工程边界上。尤其是 D3 的非事务式副作用、E2 的多层缓冲风险、F2-F3 的返回数据与输出流解耦，已经超过单纯语法记忆层面。

当前能力判断维持并进一步坐实为：**准中级入门已经基本坐稳，正在稳定向可独立完成小型工程设计的中级入门过渡。** 现在的主要提升空间已不是 C11 主干知识，而是让少数术语在属性协议、条件表达式和参数默认值等位置更加精确。

### 学习画像更新

稳定强项：

- 能稳定区分赋值语句执行效果、表达式值、函数返回值和副作用。
- 能独立分析普通赋值、链式赋值、解包、属性/下标/切片目标和增强赋值。
- 能用对象身份与引用关系解释可变对象别名、浅拷贝、原地修改与重新绑定。
- 能准确解释 `print()` 返回 `None`，并把 stdout、stderr、`StringIO`、文件流、刷新与失败路径分层。
- 能把 C11 模型迁移到本地化审计函数设计，分离结构化返回数据与可选人读输出。
- 能主动发现题干文字与代码不一致或范围有歧义，并以可验证源码为准作出说明。

仍需精修：

- 属性、下标等赋值目标宜描述为“通过对象协议写入引用”，避免完全套用局部名字绑定术语。
- 描述函数默认参数时优先说“调用使用默认值”，少用“参数指向默认值”。
- 后续条件语句中继续区分“条件表达式求值”与“对其结果进行真值测试”。

下一阶段关注：

- `C12_if_Tests_and_Syntax_Rules` 中的真值测试协议。
- `and` / `or` 的短路求值与“返回操作数对象而不保证返回 bool”。
- 比较链的求值顺序、身份比较与相等性比较。
- 条件表达式、`if` 代码块和必要的 `match` 适用边界。

画像同步状态：以上判断已同步到 `notes/Python_Learning_Profile.md`。
