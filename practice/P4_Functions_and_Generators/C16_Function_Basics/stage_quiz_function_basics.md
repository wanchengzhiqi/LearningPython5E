# C16 Function Basics 阶段测验

<!-- quiz-validator: total=100 -->

本卷用于验收 P4_Functions_and_Generators / C16_Function_Basics。
C16 是 P4 的 PART opener；正式主线已经完成，本卷只检查 C16 的必学核心与必要
补救。总分 100 分。

生命周期关卡核验：权威启动模板未安排 C16 测验前 capstone；路线图中的小型纯函数
实验和 P4 函数管线均只是候选，不构成本卷之前的必经项目。

## 冻结命题蓝图

考察范围：

- def 执行、函数对象创建、定义名绑定、别名和容器引用；
- 函数对象、调用表达式、函数体执行与结果对象；
- 调用入口的引用绑定、共享可变对象修改与局部名字重新绑定；
- 显式返回值、裸 return、正常执行到末尾、不可达代码与异常路径；
- 返回对象、展示或日志、参数对象修改和受控 I/O 的合同分层；
- 函数作为一等对象的基础观察，以及 docstring、callable、签名、Signature.bind
  和注解所能提供的有限证据；
- 用本地化数据设计返回合同清晰、展示职责独立的小型函数。

明确排除：

- C17 的完整 LEGB、global、nonlocal、嵌套作用域与闭包；
- C18 的完整参数匹配、positional-only、keyword-only、可变默认值、*args 和
  **kwargs；
- C19 的高阶函数架构、装饰器、递归专题和系统注解设计；
- C20 的 yield、生成器函数和暂停帧；
- C21 的基准测试、性能陷阱与优化；
- frame、字节码、描述符实现、静态类型检查器细节；
- 数据库、真实文件、网络、CLI、GUI 写入，未排期 capstone 和 P4 全阶段综合。

| 分区 | 主题 | 题型 | 分值 |
| --- | --- | --- | ---: |
| A | def、函数对象与名字绑定 | 概念分类、代码预测 | 16 |
| B | 调用与返回时间线 | 事件轨迹、对象关系 | 18 |
| C | 返回路径、不可达代码与异常 | 路径分析、控制流追踪 | 22 |
| D | 返回合同与副作用分层 | 代码预测、工程审查 | 20 |
| E | docstring、签名、注解与有限证据 | 运行观察、证据边界 | 14 |
| F | 小型合同驱动设计 | 本地化应用题 | 10 |
| **合计** |  | **11 题** | **100** |

难度略高于当前舒适区，主要体现在多步对象身份、调用顺序、异常前副作用和证明范围
的联合追踪；不依赖对象地址、无序容器偶然显示或完整异常消息制造难度。

## 作答说明

1. 请保留稳定题号、分值标记和 HTML 注释，只在每题的
   answer:start / answer:end 之间作答。
2. 精确输出题先写逐行输出，再解释定义、绑定、调用、对象修改、返回或异常的顺序。
3. 概念与工程题应明确区分名字、对象、调用表达式、返回对象、展示文本和外部效果。
4. 可以使用 Python 3.14.5 的最小实验核对，但请先保留自己的推理，并说明实验能与
   不能证明什么。
5. 除非题目明确要求，不要引入 C17-C21 的高级机制。

---

<!-- quiz-section: id=A score=16 -->
## A. def、函数对象与名字绑定（16 分）

本区检查“执行 def”和“调用函数”是否仍被严格分开，并把难度提高到：定义名
重新绑定后，既有别名与容器槽位仍可保留旧函数对象。

<!-- quiz-question: id=A1 score=6 -->
### A1. 定义、绑定、调用与结果对象（6 分）

阅读下面的代码，但先不要运行：

~~~python
def normalize_key(key):
    return key.strip().lower()


alias = normalize_key
registry = {"normalize": normalize_key}
result = alias(" MENU.Start ")
~~~

回答：

1. 按“执行 def → 创建对象 → 名字绑定 → 建立别名/容器引用 → 调用 → 函数体
   → return → 调用者绑定”的顺序，说明这段代码发生了什么。
2. 分别指出下列各项代表函数对象引用、保存同一函数对象的名字或容器槽位、
   调用表达式，以及调用结果对象中的哪一类：

   ~~~text
   normalize_key
   alias
   registry["normalize"]
   alias(" MENU.Start ")
   result
   ~~~

3. 判断下面三个命题，并说明理由：

   ~~~text
   alias is normalize_key
   registry["normalize"] is normalize_key
   normalize_key is result
   ~~~

4. 用一句话说明这里为什么可以称函数为“一等对象”的基础观察，以及为什么这还
   不等于已经学习高阶函数设计。

评分关注：完整时间线 2 分；五项分类 2 分；三个身份判断 1.5 分；范围边界 0.5 分。

#### 你的作答

<!-- answer:start -->

### 1. 完整时间线

1. 控制流执行 `def normalize_key(...)`。此时执行的是函数定义语句，不是函数体中的 `return`。

2. 本次 `def` 创建一个用户定义函数对象，记为 **F**。

3. 当前命名空间中的名字 `normalize_key` 绑定 F：

   ```text
   normalize_key ──► F
   ```

4. `alias = normalize_key` 读取 F，再让 `alias` 绑定同一个 F；没有复制，也没有调用。

5. `registry = {"normalize": normalize_key}` 把同一个 F 保存为字典键 `"normalize"` 对应的值。所以现有：

   ```text
   normalize_key          ──► F
   alias                  ──► F
   registry["normalize"]  ──► F
   ```

6. 求值 `alias(" MENU.Start ")` 时，先得到调用目标 F，再得到字符串实参 `" MENU.Start "`。

7. 进入函数体后，形参 `key` 绑定该字符串对象。参数绑定不会默认复制对象。

8. `key.strip()` 产生 `"MENU.Start"`，再由 `lower()` 产生 `"menu.start"`。

9. `return` 将字符串对象 `"menu.start"` 作为正常返回对象交给调用者。

10. 右侧调用正常完成后，名字 `result` 才绑定该返回对象：

    ```text
    result ──► "menu.start"
    ```

### 2. 五项分类

| 项目                    | 分类                                                |
| ----------------------- | --------------------------------------------------- |
| `normalize_key`         | 名字；求值时得到函数对象 F                          |
| `alias`                 | 保存同一函数对象 F 的另一个名字                     |
| `registry["normalize"]` | 保存同一函数对象 F 的容器槽位；取项表达式求值得到 F |
| `alias(" MENU.Start ")` | 函数调用表达式；正常完成时其值为 `"menu.start"`     |
| `result`                | 调用后绑定结果字符串 `"menu.start"` 的名字          |

### 3. 身份判断

```python
alias is normalize_key
```

为 `True`，因为两边都是 F。

```python
registry["normalize"] is normalize_key
```

为 `True`，因为字典槽位保存的也是 F。

```python
normalize_key is result
```

为 `False`，因为左边是函数对象 F，右边是字符串结果对象。

### 4. 一等对象与范围边界

函数可像其他对象一样被名字引用、赋给别名、存入容器并取出调用，所以这是函数作为“一等对象”的基础观察；但这里只观察了对象可保存和可传递的性质，尚未进入系统的高阶函数设计、函数组合或回调架构。

<!-- answer:end -->

<!-- quiz-question: id=A2 score=10 -->
### A2. 重新定义后的别名、容器与调用顺序（10 分）

预测下面五行 print 的精确输出：

~~~python
events = []


def label():
    events.append("v1")
    return "v1"


old = label
registry = {"saved": label}


def label():
    events.append("v2")
    return "v2"


print(old is label)
print(registry["saved"] is old)
print(old.__name__ == label.__name__)
print(old(), label(), registry["saved"]())
print(events)
~~~

除输出外，还须说明：

1. 两个 def 语句分别创建了几个函数对象；第二个 def 改变了哪个名字的绑定。
2. 为什么 old 和 registry["saved"] 没有随 label 一起变成新函数。
3. 三次调用按什么顺序执行，events 为什么得到相应内容。
4. 为什么两个不同函数对象的 __name__ 仍然可以相等；元数据相等为什么不等于
   对象身份相同。

评分关注：五行输出 4 分；对象创建与重新绑定 2 分；别名/容器引用 2 分；调用顺序
和元数据边界 2 分。

#### 你的作答

<!-- answer:start -->

### 精确输出

```text
False
True
True
v1 v2 v1
['v1', 'v2', 'v1']
```

### 对象创建与重新绑定

第一次 `def label()` 创建函数对象 **F1**，名字 `label` 绑定 F1。随后：

```text
old                ──► F1
registry["saved"]  ──► F1
label              ──► F1
```

第二次同名 `def label()` 又创建一个新函数对象 **F2**，并只把名字 `label` 改绑为 F2：

```text
old                ──► F1
registry["saved"]  ──► F1
label              ──► F2
```

所以两条 `def` 各创建一个函数对象，共两个。第二条 `def` 改变的是名字 `label` 的绑定，不会追溯修改 `old` 或字典槽位。

因此：

- `old is label` 比较 F1 与 F2，输出 `False`；
- `registry["saved"] is old` 比较 F1 与 F1，输出 `True`。

### 调用顺序与 `events`

`print(old(), label(), registry["saved"]())` 的三个实参从左到右求值：

1. `old()` 调用 F1，追加 `"v1"`，返回 `"v1"`；
2. `label()` 调用 F2，追加 `"v2"`，返回 `"v2"`；
3. `registry["saved"]()` 调用 F1，追加 `"v1"`，返回 `"v1"`；
4. 外层 `print` 输出 `v1 v2 v1`。

因此最终：

```python
events == ["v1", "v2", "v1"]
```

### 元数据相等与身份不同

两个函数对象都来自名为 `label` 的定义，所以它们各自的 `__name__` 初始值都是字符串 `"label"`，故：

```python
old.__name__ == label.__name__
```

为 `True`。

但 `__name__` 只是元数据。两个不同对象完全可以携带相等的元数据；对象身份必须用 `is` 判断，元数据相等不能推出对象相同。

<!-- answer:end -->

---

<!-- quiz-section: id=B score=18 -->
## B. 调用与返回时间线（18 分）

本区沿着一次真实调用追踪对象和控制流。只使用 C16 的基本调用入口模型：
形参绑定对象引用，不展开 C18 的完整参数匹配规则。

<!-- quiz-question: id=B1 score=10 -->
### B1. 调用者—函数体—return—调用者事件轨迹（10 分）

预测三行精确输出，并写出完整事件顺序：

~~~python
def normalize_key(key, timeline):
    timeline.append("body: entered")
    normalized = key.strip().lower()
    timeline.append(f"body: normalized={normalized!r}")
    timeline.append("body: before return")
    return normalized
    timeline.append("body: unreachable")


timeline = ["caller: before call"]
source = " MENU.Start "
result = normalize_key(source, timeline)
timeline.append("caller: after call")

print(repr(source))
print(result)
print(timeline)
~~~

说明：

1. 执行 def 时为什么没有向 timeline 追加任何内容。
2. 调用表达式求值时，source 所指字符串对象如何进入形参 key；这一步是否默认
   复制该对象。
3. 局部名字 normalized 与调用者名字 result 是否是同一个名字；return 实际
   交给调用者的是什么。
4. 为什么调用者的 "caller: after call" 只能在正常返回后追加，而 return 后面的
   函数体语句不可达。
5. source 为什么保持原字符串；不要把字符串方法产生新结果说成原地修改。

评分关注：三行输出与事件顺序 4 分；定义/调用时机 2 分；入口绑定与返回对象 2 分；
不可达代码和不可变对象边界 2 分。

#### 你的作答

<!-- answer:start -->

### 精确输出

```text
' MENU.Start '
menu.start
['caller: before call', 'body: entered', "body: normalized='menu.start'", 'body: before return', 'caller: after call']
```

### 完整事件顺序

1. 执行 `def normalize_key(...)` 时创建函数对象并绑定名字，函数体不执行，因此不会向 `timeline` 追加内容。

2. `timeline` 绑定列表 T，初始含 `"caller: before call"`；`source` 绑定原字符串 S，即 `" MENU.Start "`。

3. 求值 `normalize_key(source, timeline)` 时，实参表达式分别得到 S 和 T。

4. 进入调用后，形参 `key` 绑定 S，形参 `timeline` 绑定 T。参数绑定不会自动复制对象。

5. `timeline.append("body: entered")` 修改共享列表 T。

6. `key.strip().lower()` 产生新字符串 N，即 `"menu.start"`；局部名字 `normalized` 绑定 N。原字符串 S 未被原地修改。

7. 接着向 T 依次追加：

   ```text
   body: normalized='menu.start'
   body: before return
   ```

8. `return normalized` 将 N 交给调用者。局部名字 `normalized` 与调用者名字 `result` 不是同一个名字；调用正常完成后，`result` 才绑定 N。

9. `return` 立即结束本次调用，因此 `timeline.append("body: unreachable")` 在该路径不可达。

10. 调用正常返回并完成 `result` 绑定后，调用者才执行 `timeline.append("caller: after call")`。

所以：

- `source` 仍绑定原字符串，`repr(source)` 输出 `' MENU.Start '`；
- `result` 绑定返回字符串，输出 `menu.start`；
- 时间线按题示顺序排列。

本题涉及的字符串方法都产生新结果，不能描述为对 `source` 的原地修改。

<!-- answer:end -->

<!-- quiz-question: id=B2 score=8 -->
### B2. 共享修改与局部重新绑定（8 分）

预测三行精确输出：

~~~python
def update_records(items, trace):
    original = items
    items.append("body")
    trace.append(items is original)

    items = ["local"]
    trace.append(items)
    items.append("tail")

    return original


records = ["caller"]
trace = []
result = update_records(records, trace)

print(records)
print(result is records)
print(trace)
~~~

随后画出或用文字描述两个列表对象与这些名字/槽位之间的关系：

~~~text
调用者中的 records
调用者中的 result
函数体最初的 items
函数体重新绑定后的 items
original
trace[1]
~~~

特别解释：

- items.append("body") 为什么能被调用者观察到；
- items = ["local"] 为什么没有把调用者的 records 改绑到新列表；
- trace.append(items) 保存的是什么，为什么之后的 items.append("tail") 会让
  trace[1] 也显示 "tail"；
- return original 返回的是哪个对象。

评分关注：输出 3 分；原列表的共享修改 2 分；局部重新绑定 1.5 分；trace[1]
引用与返回对象 1.5 分。

#### 你的作答

<!-- answer:start -->

### 精确输出

```text
['caller', 'body']
True
[True, ['local', 'tail']]
```

### 对象关系

设调用者原列表为 **L1**，函数体后来创建的新列表为 **L2**。

调用开始时：

```text
records       ──► L1
items         ──► L1
```

执行 `original = items` 后：

```text
original      ──► L1
```

`items.append("body")` 原地修改 L1。调用者的 `records` 仍引用 L1，所以能够观察到：

```python
["caller", "body"]
```

此时 `items is original` 为 `True`，该布尔对象被保存为 `trace[0]`。

随后：

```python
items = ["local"]
```

创建 L2，只把函数局部名字 `items` 从 L1 改绑到 L2：

```text
records       ──► L1
original      ──► L1
items         ──► L2
```

这不会把调用者名字 `records` 改绑到 L2。

`trace.append(items)` 保存的是对 L2 的引用，不是内容副本：

```text
trace[1]      ──► L2
items         ──► L2
```

所以随后 `items.append("tail")` 修改 L2 时，`trace[1]` 也显示 `"tail"`。

最后 `return original` 返回 L1，调用者名字 `result` 绑定 L1：

| 名字或槽位           | 对象                            |
| -------------------- | ------------------------------- |
| 调用者 `records`     | L1，最终为 `["caller", "body"]` |
| 调用者 `result`      | L1                              |
| 函数体最初的 `items` | L1                              |
| 重新绑定后的 `items` | L2，最终为 `["local", "tail"]`  |
| `original`           | L1                              |
| `trace[1]`           | L2                              |

因此 `result is records` 为 `True`。

<!-- answer:end -->

---

<!-- quiz-section: id=C score=22 -->
## C. 返回路径、不可达代码与异常（22 分）

本区不只问“返回了什么”，还要求判断一次调用是正常返回、提前返回还是异常退出，
以及调用方赋值和异常前副作用分别发生到哪一步。

<!-- quiz-question: id=C1 score=10 -->
### C1. 显式返回、裸返回与正常落到末尾（10 分）

预测下面五行 print 的精确输出：

~~~python
def classify(text, audit):
    audit.append(f"start:{text!r}")

    if text == "":
        return

    if text.isspace():
        return "blank"

    audit.append("ready")
    return text.strip().lower()
    audit.append("unreachable")


def mark_seen(audit):
    audit.append("seen")


audit = []

print(classify("", audit))
print(classify("   ", audit))
print(classify(" MENU.Start ", audit))
print(mark_seen(audit))
print(audit)
~~~

逐次说明四次调用各自走过的路径，并回答：

1. classify("") 的裸 return 与 mark_seen(audit) 正常执行到函数体末尾，有什么共同
   结果，又有什么控制流差异？
2. 仅含空白的字符串是真值对象，为什么本题仍会走 isspace() 分支？
3. 普通文本路径中，哪个对象被 return 交给调用者？
4. "unreachable" 为什么不会进入 audit？源码存在与该次运行路径实际到达应怎样
   区分？
5. 哪些调用正常返回 None？为什么不能据此声称它们“什么都没做”？

评分关注：五行输出 4 分；四条路径 2 分；裸返回/隐式 None 1.5 分；不可达代码
1.5 分；返回对象与副作用边界 1 分。

#### 你的作答

<!-- answer:start -->

### 精确输出

```text
None
blank
menu.start
None
["start:''", "start:'   '", "start:' MENU.Start '", 'ready', 'seen']
```

### 四次调用路径

#### `classify("", audit)`

先追加 `"start:''"`。`text == ""` 为真，执行裸 `return`，提前正常返回 `None`，所以外层打印 `None`。

#### `classify("   ", audit)`

先追加 `"start:'   '"`。这里的字符串虽然非空、在普通真值测试中为真，但本题显式调用 `text.isspace()`；该方法判断“非空且所有字符都是空白字符”，所以结果为真，函数返回 `"blank"`。

#### `classify(" MENU.Start ", audit)`

先追加 `"start:' MENU.Start '"`。它既非空，也不是仅含空白，因此追加 `"ready"`，再将 `text.strip().lower()` 产生的字符串对象 `"menu.start"` 交给调用者。

`return` 立即结束本次调用，所以后面的：

```python
audit.append("unreachable")
```

在该路径不可达，`"unreachable"` 不会进入 `audit`。源码中存在一条语句，不等于某次运行路径实际到达了它。

#### `mark_seen(audit)`

向共享列表追加 `"seen"`，然后函数正常运行到末尾，隐式正常返回 `None`，所以外层打印 `None`。

### 裸返回与隐式 `None`

共同点：两者都属于正常返回，正常返回对象都是 `None`。

区别：

- `classify("")` 通过显式裸 `return` 提前结束；
- `mark_seen()` 执行完函数体后自然落到末尾。

返回 `None` 不能推出“什么都没做”：前者已写入审计记录，后者已追加 `"seen"`，而外层 `print` 也产生了显示效果。

<!-- answer:end -->

<!-- quiz-question: id=C2 score=12 -->
### C2. 异常前副作用与调用方赋值（12 分）

预测下面三行 print 的精确输出：

~~~python
def read_key(record, events):
    events.append("entered")
    record["seen"] = True

    if "key" not in record:
        raise KeyError("key")

    events.append("validated")
    return record["key"].strip().lower()


record = {}
events = []
result = "previous"

try:
    result = read_key(record, events)
except KeyError as error:
    events.append(type(error).__name__)

print(result)
print(record)
print(events)
~~~

必须按求值与控制流顺序解释：

1. 调用进入函数体后，异常发生前已经完成了哪些对象修改。
2. raise 发生后，函数是否产生了正常返回对象；能否把这次调用描述成“隐式返回
   None”。
3. 赋值语句 result = read_key(...) 为什么没有完成对 result 的重新绑定。
4. Python 为什么不会自动撤销 record 和 events 已经发生的修改；except 块又增加了
   哪个效果。
5. 如果初始 record 改为 {"key": " MENU.Quit "}，正常路径会多执行哪些语句，
   result、record 和 events 分别会是什么；这一问只需推导，不必给完整异常消息。

评分关注：三行输出 4 分；异常发生位置与正常返回边界 2.5 分；调用方赋值 2 分；
非事务式副作用 2 分；正常路径对照 1.5 分。

#### 你的作答

<!-- answer:start -->

### 精确输出

```text
previous
{'seen': True}
['entered', 'KeyError']
```

### 异常路径顺序

初始：

```text
record ──► {}
events ──► []
result ──► "previous"
```

执行 `result = read_key(record, events)` 时，必须先完整求值右侧调用。

进入函数体后，异常前已经完成：

1. `events.append("entered")`；
2. `record["seen"] = True`。

随后 `"key" not in record` 为真，执行：

```python
raise KeyError("key")
```

函数通过异常路径退出，没有执行 `"validated"` 追加，也没有执行 `return`。因此：

- 本次调用没有正常返回对象；
- 不能描述成“隐式返回 `None`”；
- 右侧调用未正常完成，左侧 `result` 没有改绑，仍是 `"previous"`。

Python 调用不是自动事务。异常只改变控制流，不会撤销已经完成的列表追加或字典赋值。外层 `except` 又执行：

```python
events.append(type(error).__name__)
```

追加 `"KeyError"` 到 `events`。

### 正常路径对照

若初始：

```python
record = {"key": " MENU.Quit "}
```

则：

1. 追加 `"entered"`；
2. 添加 `"seen": True`；
3. 条件为假，不抛异常；
4. 追加 `"validated"`；
5. `record["key"].strip().lower()` 产生 `"menu.quit"`；
6. 函数正常返回，外层赋值完成。

最终：

```python
result == "menu.quit"
record == {"key": " MENU.Quit ", "seen": True}
events == ["entered", "validated"]
```

<!-- answer:end -->

---

<!-- quiz-section: id=D score=20 -->
## D. 返回合同与副作用分层（20 分）

本区把一次函数调用可能产生的结果拆成四个维度：交给调用者的返回对象、
写入输出流的文本、传入可变对象的修改，以及其它受控 I/O 结果。

<!-- quiz-question: id=D1 score=10 -->
### D1. 返回对象、列表修改与 StringIO（10 分）

预测下面三行 print 的精确输出：

~~~python
from io import StringIO


def emit_keys(keys, output):
    original = keys
    keys[:] = [key.strip().lower() for key in keys]

    text = "|".join(keys)
    written = output.write(text)
    display_result = print("done", file=output)

    return {
        "same_object": keys is original,
        "written": written,
        "display_result": display_result,
    }


keys = [" MENU.Start ", "MENU.Quit"]
same_keys = keys
output = StringIO()

report = emit_keys(keys, output)

print(report)
print(same_keys)
print(repr(output.getvalue()))
~~~

除精确输出外，分别标注：

1. report 是哪个 return 语句产生的什么类型对象。
2. 切片赋值先创建了什么、随后修改了哪个既有对象；same_keys 为什么能观察到结果。
3. output.write(text) 的返回对象代表什么，为什么它不是被写入的文本本身。
4. print("done", file=output) 的输出效果和返回对象分别是什么。
5. 为什么缓冲区中分隔文本与 done 之间没有自动换行，而末尾存在换行。
6. StringIO 能证明哪些受控内存效果，为什么它不能证明真实文件或数据库已经持久化。

评分关注：三行输出 4 分；列表身份与修改 2 分；write/print 的返回边界 2 分；
缓冲区与持久化限制 2 分。

#### 你的作答

<!-- answer:start -->

### 精确输出

```text
{'same_object': True, 'written': 20, 'display_result': None}
['menu.start', 'menu.quit']
'menu.start|menu.quitdone\n'
```

### 1. 返回对象

最后的 `return` 先构造一个新 `dict`，再将它交给调用者；调用者名字 `report` 绑定该字典。

### 2. 切片赋值与列表身份

列表推导式先创建新列表：

```python
["menu.start", "menu.quit"]
```

随后：

```python
keys[:] = ...
```

原地修改 `keys` 当前引用的原列表对象，而不是重新绑定局部名字 `keys`。调用前 `keys` 与 `same_keys` 引用同一列表；函数内 `original` 也引用该列表。因此切片赋值后：

```python
keys is original
```

为 `True`，调用者的 `same_keys` 也观察到规范化内容。

### 3. `write` 的返回对象

```python
text == "menu.start|menu.quit"
```

字符数为 `20`。`output.write(text)` 把文本写入 `StringIO`，返回写入的字符数整数 `20`；它返回的不是文本本身，文本保存在缓冲区中。

### 4. `print(..., file=output)`

`print("done", file=output)` 向同一缓冲区写入 `"done\n"`，而 `print` 的正常返回对象是 `None`，所以 `display_result is None`。

### 5. 换行位置

`output.write(text)` 不自动添加换行，因此 `"done"` 紧接在 `"menu.quit"` 后。`print` 默认在末尾追加 `"\n"`，所以最终：

```python
output.getvalue() == "menu.start|menu.quitdone\n"
```

### 6. `StringIO` 的证明范围

它能证明本次运行中对受控内存文本流写入了哪些字符、顺序如何，以及 `write`、`print` 的返回对象。它不能证明真实文件已经刷新或持久化，也不能证明数据库事务提交、网络送达或外部设备写入成功。

<!-- answer:end -->

<!-- quiz-question: id=D2 score=10 -->
### D2. 混合职责函数的有限合同审查（10 分）

某段业务代码写成：

~~~python
def publish(report, output):
    report["published"] = True
    print(report["summary"], file=output)
~~~

调用者随后声称：

~~~text
publish() 返回发布后的报告；
既然信息已经显示，就说明报告已经持久化；
函数没有 return，所以没有产生任何可观察结果。
~~~

完成一次有限合同审查：

1. 在正常执行且 report 含有 "summary" 时，publish() 的实际返回对象是什么？
2. 函数对 report 对象和 output 对象分别产生了什么效果？哪些名字仍指向被修改的
   原 report？
3. 逐条纠正上面三项声称。特别说明“显示”“受控输出流写入”和“真实持久化”为什么
   不能互相替代。
4. 写出一份最小合同表，至少包含：输入要求、返回、可能异常、参数对象修改、I/O
   效果。
5. 在不引入类、装饰器或真实文件的前提下，把职责有限拆成两个函数：

   - with_published(report)：返回带 published=True 的新字典，不修改原字典；
   - display_summary(report, output)：只把 summary 写到 output，并明确返回 None。

   可以写可运行实现，也可以写足够精确的伪代码；若使用普通 Python 围栏，代码必须
   能独立通过语法编译。

评分关注：实际返回与两类效果 3 分；三项纠错 2 分；合同表 2 分；有限职责拆分
3 分。

#### 你的作答

<!-- answer:start -->

### 1. 实际返回

正常执行且 `report` 含 `"summary"` 时，函数运行到末尾，隐式正常返回 `None`，不会返回 `report`。

### 2. 两类效果

- `report["published"] = True` 原地新增或覆盖原字典的 `"published"` 项。调用者中所有仍引用该原字典的名字或容器槽位都能观察到修改。
- `print(report["summary"], file=output)` 把摘要的展示文本和换行写入 `output`，改变输出流状态；它不把展示文本作为 `publish()` 的返回值。

### 3. 纠正三项声称

1. **“返回发布后的报告”错误。**\
   实际返回 `None`。调用者看到字典变化，是因为共享对象被原地修改。

2. **“显示就证明持久化”错误。**\
   显示只说明文本被写入某个输出流。`StringIO` 仅保存内存文本，终端只负责显示；真实文件、数据库或网络持久化需要额外证据。显示、受控流写入和真实持久化不能互相替代。

3. **“没有 `return` 就没有可观察结果”错误。**\
   没有显式 `return` 只意味着正常到末尾时返回 `None`。本函数仍修改 `report` 并写入 `output`。

### 4. 最小合同表

| 维度          | 合同                                                         |
| ------------- | ------------------------------------------------------------ |
| `report` 输入 | 支持 `report["published"] = True` 和 `report["summary"]`；正常业务输入为含 `"summary"` 的可变映射 |
| `output` 输入 | 与 `print(..., file=...)` 兼容的文本输出对象                 |
| 正常返回      | `None`                                                       |
| 参数修改      | 原地修改 `report`；向 `output` 写入文本                      |
| I/O           | 受控输出流写入，不自动证明持久化                             |
| 可能异常      | 不支持赋值可能 `TypeError`；缺 `"summary"` 通常 `KeyError`；输出关闭或写入失败可能出现 `ValueError`、`TypeError` 或其他 I/O 异常 |
| 部分失败      | 若读取摘要或写流失败，`report["published"] = True` 可能已经保留 |

### 5. 有限职责拆分

```python
def with_published(report):
    """Return a new top-level dictionary marked as published."""

    published_report = dict(report)
    published_report["published"] = True
    return published_report


def display_summary(report, output):
    """Write the report summary and return None."""

    print(report["summary"], file=output)
    return None
```

`with_published()` 返回新的顶层字典，不修改原字典。这里是浅复制；嵌套可变对象仍可能共享，但题目未要求深复制。`display_summary()` 只负责展示，并明确返回 `None`。

<!-- answer:end -->

---

<!-- quiz-section: id=E score=14 -->
## E. docstring、签名、注解与有限证据（14 分）

本区要求把“对象看起来可调用”“实参能绑定到签名”“注解表达了类型意图”和
“函数体对这个具体输入成功执行”分成不同强度的证据。

<!-- quiz-question: id=E1 score=8 -->
### E1. 绑定成功仍不保证函数体成功（8 分）

以本卷指定的 Python 3.14.5 环境为准，预测下面五行输出：

~~~python
import inspect


def normalize_key(key: str) -> str:
    """Return a normalized localization key."""

    return key.strip().lower()


signature = inspect.signature(normalize_key)
bound = signature.bind(404)

print(callable(normalize_key))
print(signature)
print(dict(bound.arguments))
print(normalize_key.__annotations__)

try:
    result = normalize_key(404)
except AttributeError as error:
    print(type(error).__name__)
~~~

随后解释：

1. callable(normalize_key) 为真时，只能证明到什么程度？
2. signature.bind(404) 为什么成功？它是否调用了 normalize_key，是否根据 str
   注解检查了 404？
3. __annotations__ 中的对象属于哪一层元数据；普通调用为什么不会自动实施这些
   类型提示？
4. 真正调用时，形参 key 绑定到什么对象，异常在哪个表达式发生？
5. 该调用是否正常产生返回对象？赋值目标 result 在异常前没有旧绑定；如果 except
   后立即执行 print(result)，为什么会出现新的名字访问错误？
6. 当前脚本只检查自身定义的普通函数。为什么不能把这次安全观察推广成
   “对任意对象运行 inspect 都绝不执行用户代码”？

评分关注：五行输出 3 分；callable/bind/注解边界 2.5 分；函数体异常与调用方赋值
1.5 分；内省风险边界 1 分。

#### 你的作答

<!-- answer:start -->

### 五行精确输出

```text
True
(key: str) -> str
{'key': 404}
{'key': <class 'str'>, 'return': <class 'str'>}
AttributeError
```

### 1. `callable()` 的有限证据

`callable(normalize_key)` 为真，只说明当前对象看起来支持调用协议。它不证明某组实参匹配、函数体成功、调用终止、返回 `str`、没有副作用或满足业务合同。

### 2. `Signature.bind(404)`

签名只有一个必需形参 `key`，位置实参 `404` 能在调用形状上绑定给它，所以 `bind` 成功，并得到：

```python
{"key": 404}
```

`bind` 不调用 `normalize_key`，不执行函数体，也不根据 `str` 注解检查 `404` 的类型；它只验证实参与形参的**结构映射**。

### 3. 注解证据层

`__annotations__` 打印为：

```text
{'key': <class 'str'>, 'return': <class 'str'>}
```

它属于函数对象的注解元数据，表达参数和返回值的类型意图。普通 Python 调用不会自动把这些注解转成运行时类型检查或结果验证。

### 4. 真正调用的异常

调用 `normalize_key(404)` 时，形参 `key` 绑定整数对象 `404`。函数体求值：

```python
key.strip().lower()
```

首先在访问或调用 `key.strip()` 时失败，因为整数没有 `strip` 属性，抛出 `AttributeError`；`lower()` 和 `return` 都不会完成。

### 5. 返回与赋值

该调用异常退出，没有正常返回对象，不能说成返回 `None`。赋值右侧未正常完成，因此名字 `result` 没有获得绑定。`except` 后若立即 `print(result)`，会因名字不存在而抛出 `NameError`。

### 6. 内省风险边界

本题对象是脚本自身定义的普通函数，注解也很简单。这次观察不能推广为“任意对象的 `inspect` 都不会执行用户代码”：任意对象可能自定义属性访问，签名内省可能读取对象提供的特殊属性，而 Python 3.14 的注解可能延迟求值，读取签名或注解时可能执行注解表达式或抛出异常。实验只能证明这个具体对象在这条观察路径中的结果。

<!-- answer:end -->

<!-- quiz-question: id=E2 score=6 -->
### E2. 主张、证据与不能证明的边界（6 分）

为下面六条观察建立“主张—主证据层—能支持什么—不能单独证明什么”简表：

~~~text
① 在源文件的函数体首条语句位置看到文档字符串
② normalize_key.__doc__ 是 str
③ inspect.getdoc(normalize_key) 得到清理后的说明文字
④ callable(normalize_key) 为 True
⑤ inspect.signature(normalize_key) 显示 (key: str) -> str，
   且该 Signature 的 bind(" MENU.Start ") 成功
⑥ Python 3.14.5 中一次实际调用返回 "menu.start"
~~~

要求：

1. 至少区分源码事实、函数对象元数据、内省工具当前观察、调用形状证据和具体运行
   结果。
2. 每项写出至少一个不能由它单独推出的结论。必须覆盖：文档可能漂移、可调用不等于
   调用成功、绑定成功不等于业务类型有效、注解不自动强制、一次成功不能覆盖全部
   输入或未来版本。
3. 若要核验 normalize_key(404) 的真实行为，指出最小下一实验，并说明它会观察
   返回、异常还是副作用中的哪些维度。
4. 用一句话总结：元数据与当前观察如何帮助建立合同证据，又为什么都不能替代完整
   业务合同。

评分关注：六项分层 2.5 分；不能证明的边界 2 分；下一实验 1 分；总结 0.5 分。

#### 你的作答

<!-- answer:start -->

### 主张—证据—边界简表

| 项目                                 | 主证据层                 | 能支持什么                                           | 不能单独证明什么                                          |
| ------------------------------------ | ------------------------ | ---------------------------------------------------- | --------------------------------------------------------- |
| ① 源文件函数体首条语句处有文档字符串 | 源码事实                 | 作者在源码中写了预期 docstring                       | 不能证明运行对象仍携带它、文档未被修改或文档与实现一致    |
| ② `normalize_key.__doc__` 是 `str`   | 函数对象当前元数据       | 当前函数对象此刻有字符串文档                         | 不能证明文档准确、函数调用成功、返回类型或无副作用        |
| ③ `inspect.getdoc()` 得到清理文字    | 内省工具当前观察         | 工具当前能取得并清理文档缩进                         | 不能证明原始空白形式，也不能证明文档未漂移或业务正确      |
| ④ `callable(...)` 为 `True`          | 可调用协议的有限运行观察 | 对象当前看起来可调用                                 | 不等于特定调用成功、终止、返回指定类型或满足合同          |
| ⑤ 签名显示并且 `bind(...)` 成功      | 调用形状与注解元数据     | 当前签名有 `key` 形参；该实参可映射到它              | `bind` 不执行函数体、不按注解检查业务类型；注解不自动强制 |
| ⑥ 一次调用返回 `"menu.start"`        | 具体运行结果             | 对该对象、输入、版本和环境，本次调用正常返回该字符串 | 不能覆盖全部输入、全部路径、未来版本或证明绝无副作用      |

必须保持：

- 文档可能漂移；
- 可调用不等于调用成功；
- 绑定成功不等于业务类型有效；
- 注解不自动强制；
- 一次成功不能覆盖其他输入与未来版本。

### 核验 `normalize_key(404)` 的最小实验

```python
try:
    observed = normalize_key(404)
except Exception as error:
    print(type(error).__name__)
else:
    print(repr(observed))
```

当前实现最可能输出：

```text
AttributeError
```

该实验主要观察“是否正常返回”以及“若失败，异常类型是什么”。若要观察标准输出、输入修改或其他副作用，还需分别捕获输出并比较对象状态。

### 总结

元数据、源码和内省观察可逐层帮助建立名称、文档、调用形状与类型意图的合同证据，具体实验能提供某个输入的行为证据，但任何单层证据都不能替代同时涵盖输入、返回、异常、修改、副作用和业务语义的完整合同。

<!-- answer:end -->

---

<!-- quiz-section: id=F score=10 -->
## F. 小型合同驱动设计（10 分）

本区是有限的小型设计题，不是 capstone。目标是把 C16 的对象、返回、异常和
副作用模型迁移到一个可运行的本地化函数边界。

<!-- quiz-question: id=F1 score=10 -->
### F1. 本地化缺失键报告（10 分）

请实现下面三个函数：

~~~python
def normalize_key(key):
    ...


def build_missing_report(source_keys, target_keys):
    ...


def display_missing_report(report, output):
    ...
~~~

功能合同：

1. source_keys 和 target_keys 都按“字符串列表”处理。normalize_key(key) 返回
   去除两端空白并转为小写的新字符串。
2. build_missing_report(source_keys, target_keys)：

   - 不修改两个传入列表；
   - 分别规范化两个列表中的 key；
   - 计算源列表有而目标列表没有的 key；
   - 按字典序排序；
   - 返回下面形状的新字典，不在内部 print，也不写外部资源：

~~~python
{
    "missing_count": 2,
    "missing_keys": ["menu.options", "menu.quit"],
}
~~~

3. display_missing_report(report, output) 按以下格式写入 output，并明确返回 None：

   ~~~text
   missing_count=2
   missing=menu.options
   missing=menu.quit
   ~~~

代表性输入：

~~~python
source_keys = [" MENU.Start ", "Menu.Quit", "menu.options"]
target_keys = ["menu.start"]
~~~

除实现外，还须完成：

1. 给三个函数分别写一张最小合同表，包含输入要求、返回对象、可能异常、是否修改
   参数对象、是否产生输出或其它 I/O。
2. 说明为什么 build_missing_report 返回的新字典、display_missing_report 写入的
   文本和 display_missing_report 的 None 返回值是三个不同对象/效果层次。
3. 使用 StringIO 给出一个最小调用示例，并写出 report 的精确值、两个输入列表调用
   后的值，以及 repr(output.getvalue()) 的精确结果。
4. 如果 source_keys 中出现整数 404，说明异常最可能在哪个函数体表达式发生；不能
   把该失败说成注解自动检查或隐式返回 None。
5. 不要引入类、闭包、复杂参数、生成器、真实文件或数据库。

评分关注：规范化与结构化报告 4 分；独立展示函数 2 分；三个函数的合同说明 2 分；
正常/异常代表性验证 2 分。

#### 你的作答

<!-- answer:start -->

### 可运行实现

```python
def normalize_key(key):
    """Return a stripped, lowercase key."""

    return key.strip().lower()


def build_missing_report(source_keys, target_keys):
    """Return normalized source keys missing from target."""

    normalized_source = {
        normalize_key(key)
        for key in source_keys
    }

    normalized_target = {
        normalize_key(key)
        for key in target_keys
    }

    missing_keys = sorted(
        normalized_source - normalized_target
    )

    return {
        "missing_count": len(missing_keys),
        "missing_keys": missing_keys,
    }


def display_missing_report(report, output):
    """Write the missing-key report and return None."""

    print(
        f'missing_count={report["missing_count"]}',
        file=output,
    )

    for key in report["missing_keys"]:
        print(
            f"missing={key}",
            file=output,
        )

    return None
```

这里把“源有而目标没有”按集合差处理，所以同一规范化键重复出现时只保留一次；随后按字典序排序。

### 三个函数的最小合同

#### `normalize_key(key)`

| 维度     | 合同                                                         |
| -------- | ------------------------------------------------------------ |
| 输入     | 正式输入为 `str`；最低运行要求为支持 `strip()`，且其结果支持 `lower()` |
| 返回     | 去除两端空白并转小写的新字符串                               |
| 异常     | 不兼容对象可能在 `strip()` 或 `lower()` 处出现 `AttributeError`、`TypeError` 或自定义异常 |
| 参数修改 | 对普通字符串不修改原对象                                     |
| 输出/I/O | 无                                                           |

#### `build_missing_report(source_keys, target_keys)`

| 维度     | 合同                                                         |
| -------- | ------------------------------------------------------------ |
| 输入     | 两个字符串列表；函数完整迭代并规范化其中元素                 |
| 返回     | 新字典，含 `missing_count` 和排序后的新列表 `missing_keys`   |
| 异常     | 输入不可迭代可能 `TypeError`；元素不兼容时传播 `normalize_key()` 的异常；规范化结果需可哈希，本题字符串满足 |
| 参数修改 | 不修改两个输入列表                                           |
| 输出/I/O | 不打印、不写外部资源；主要结果是返回字典                     |

#### `display_missing_report(report, output)`

| 维度     | 合同                                                         |
| -------- | ------------------------------------------------------------ |
| 输入     | `report` 提供 `"missing_count"` 与可迭代的 `"missing_keys"`；`output` 是兼容文本输出流 |
| 返回     | 明确返回 `None`                                              |
| 异常     | 缺字段通常 `KeyError`；输出关闭或写入失败可能产生 `ValueError`、`TypeError` 或其他 I/O 异常 |
| 参数修改 | 不修改报告字段；会改变输出流内容和位置                       |
| 输出/I/O | 写入计数行及每个缺失键一行；不自动证明真实持久化             |

### 三个不同层次

1. `build_missing_report()` 返回的新字典是结构化数据对象；
2. `display_missing_report()` 写入 `output` 的文本是展示副作用；
3. `display_missing_report()` 的返回对象是 `None`。

返回字典不等于已经展示，展示文本不等于函数返回文本，也不等于外部资源已经持久化。

### `StringIO` 示例

```python
from io import StringIO


source_keys = [
    " MENU.Start ",
    "Menu.Quit",
    "menu.options",
]

target_keys = [
    "menu.start",
]

report = build_missing_report(
    source_keys,
    target_keys,
)

output = StringIO()

display_result = display_missing_report(
    report,
    output,
)
```

精确结果：

```python
report == {
    "missing_count": 2,
    "missing_keys": [
        "menu.options",
        "menu.quit",
    ],
}
```

按实际字典显示：

```text
{'missing_count': 2, 'missing_keys': ['menu.options', 'menu.quit']}
```

两个输入列表保持：

```python
source_keys == [
    " MENU.Start ",
    "Menu.Quit",
    "menu.options",
]

target_keys == [
    "menu.start",
]
```

并且：

```python
display_result is None
```

缓冲区精确内容：

```python
output.getvalue() == (
    "missing_count=2\n"
    "missing=menu.options\n"
    "missing=menu.quit\n"
)
```

所以：

```text
repr(output.getvalue())
==
'missing_count=2\nmissing=menu.options\nmissing=menu.quit\n'
```

### 出现整数 `404` 时

若 `source_keys` 中有 `404`，`build_missing_report()` 在规范化源键时调用：

```python
normalize_key(404)
```

进入函数后最可能在：

```python
key.strip()
```

处抛出 `AttributeError`，因为整数没有 `strip` 属性。

这不是注解自动检查，也不是隐式返回 `None`；函数通过异常路径退出，没有正常返回对象，`build_missing_report()` 也不会正常交付报告。两个输入列表不会被本实现原地修改。

<!-- answer:end -->

---

## Codex 批改记录（逐题审批，2026-08-01）

### 覆盖账本

下表先冻结本轮审批覆盖。原答案的文字、代码和作答顺序均保留在原作答区；本记录
只追加审批发现与结论。D2 原答案中的三处 Markdown 行尾双空格仅等价改成
CommonMark 反斜杠硬换行，以通过结构验证，不改变任何作答文字或显示层次。

| 题号 | 分值 | 原答案位置 | 审批状态 | 发现 | 得分 |
| --- | ---: | --- | --- | --- | ---: |
| A1 | 6 | 行 112–184（正文 114–182） | 已审批 | 定义、绑定、调用、返回和身份判断完整准确 | 6 |
| A2 | 10 | 行 229–293（正文 231–291） | 已审批 | 两次定义、重新绑定、旧引用和元数据边界准确 | 10 |
| B1 | 10 | 行 344–389（正文 346–387） | 已审批 | 调用时间线、不可达代码和字符串边界准确 | 10 |
| B2 | 8 | 行 442–515（正文 444–513） | 已审批 | 共享修改、局部改绑、容器引用与返回对象准确 | 8 |
| C1 | 10 | 行 573–622（正文 575–620） | 已审批 | 四条返回路径、`None` 与副作用边界准确 | 10 |
| C2 | 12 | 行 671–743（正文 673–741） | 已审批 | 异常前修改、赋值未完成和正常路径对照准确 | 12 |
| D1 | 10 | 行 802–862（正文 804–860） | 已审批 | 列表修改、两个调用返回值和内存流证据准确 | 10 |
| D2 | 10 | 行 905–959（正文 907–957） | 已审批 | 混合职责审查、失败路径和有限拆分完整 | 10 |
| E1 | 8 | 行 1016–1070（正文 1018–1068） | 已审批 | 五行输出及 `callable`/签名/注解/真实调用分层准确 | 8 |
| E2 | 6 | 行 1103–1147（正文 1105–1145） | 已审批 | 六项证据、反向限制、最小实验和总结完整 | 6 |
| F1 | 10 | 行 1226–1422（正文 1228–1420） | 已审批，轻微扣分 | 通用输出对象的“内容和位置”合同外推过强 | 9.75 |

审批游标：`F1`，共 `11 / 11` 题完成，无遗漏。

### A1 — 6 / 6

完整区分了执行 `def`、创建函数对象、名字与容器槽位保存引用、调用表达式、函数体
执行、`return` 交付对象以及调用者名字绑定。三个 `is` 判断全部正确；“一等对象的
基础观察”也没有被扩大成已掌握高阶函数设计。

### A2 — 10 / 10

五行输出完全正确。两次 `def` 各创建一个函数对象，第二次只改绑当前名字 `label`；
`old` 和 `registry["saved"]` 继续引用 F1。三次调用按实参从左到右求值，且准确说明
了两个不同函数对象可以具有相等的 `__name__`，元数据相等不能推出身份相同。

### B1 — 10 / 10

输出、实参求值、形参绑定、局部名字、返回对象、调用者继续执行和不可达语句均追踪
准确；也没有把字符串方法描述成原地修改。

不扣分精度补充：本题具体输入确实得到另一个结果字符串，但一般合同应说“方法返回
结果字符串且不修改原字符串”，不要进一步外推为语言在所有输入和实现下都保证结果
具有全新的对象身份。

### B2 — 8 / 8

L1/L2 对象图、`append()` 对共享对象的修改、局部名字 `items` 的重新绑定、
`trace[1]` 保存 L2 引用以及 `return original` 返回 L1 全部正确。答案清楚地区分了
名字历史与对象身份。

### C1 — 10 / 10

五行输出和四次调用路径全部正确。裸 `return` 与自然落到函数末尾都正常返回
`None`，但控制流终止位置不同；源码中存在语句不等于当前路径到达该语句，返回
`None` 也不等于调用没有产生副作用。

### C2 — 12 / 12

异常发生前的列表追加和字典修改、异常退出没有正常返回对象、右侧调用未完成导致
`result` 不改绑，以及异常不会自动回滚既有副作用，均解释准确；正常路径对照也完全
正确。

不扣分措辞补充：“异常只改变控制流”若脱离本题会过宽。更严密的说法是：异常中断
当前正常控制流并开始传播，传播过程中还可能发生栈展开和 `finally` 等动作，但它不会
自动撤销已经完成的对象修改或 I/O。

### D1 — 10 / 10

三行输出、列表推导式创建新列表、切片赋值修改原列表、`write()` 返回字符数、
`print()` 返回 `None`、缓冲区换行位置和持久化限制全部正确。

不扣分证据补充：`output.getvalue()` 直接证明的是当前内存流内容；`written` 和
`display_result` 才分别记录 `write()` 与 `print()` 的返回对象。整段程序的不同观察
共同支持这些结论，不能把所有证明能力都归给缓冲区本身。

### D2 — 10 / 10

实际返回、共享字典修改、输出流写入、三项错误声称、可能异常和部分失败均分析准确。
两个拆分函数可运行，`dict(report)` 是顶层浅复制这一限制也主动写明。

不扣分用词补充：`display_summary()` 的直接合同是“向调用者提供的输出对象写入摘要
文本”。当目标是 `StringIO`、文件或其它接收器时，这不必然等于用户界面已经发生
“显示”；答案前文已经正确区分，仅末句用词稍宽。

### E1 — 8 / 8

Python 3.14.5 下五行输出全部正确，并严格区分了 `callable()`、
`Signature.bind()`、注解元数据和真实函数体执行的证据强度。异常退出不产生正常
返回对象，调用方的 `result` 也不会获得绑定。

不扣分精度补充：求值 `key.strip()` 时先查找整数对象的 `strip` 属性；`404` 没有该
属性，所以在属性查找阶段抛出 `AttributeError`，`strip()` 调用本身尚未发生，
`lower()` 更未执行。

### E2 — 6 / 6

六项观察的证据层、每项不能单独证明的范围、最小下一实验和合同总结均完整。⑤还可
进一步拆成三个并列层次：`inspect.signature()` 是内省工具当前观察，签名中的注解是
类型意图元数据，`Signature.bind()` 成功是调用形状映射证据。

不扣分措辞补充：对题目给定实现、整数 `404` 和指定解释器，最小实验确定打印
`AttributeError`；这里不需要用“最可能”降低结论强度。一次实验的外推范围有限，
不等于该次具体结果本身不确定。

### F1 — 9.75 / 10

三个函数的职责分离清楚：规范化、集合差、排序、结构化返回、独立输出和显式
`None` 均符合题面。代表性报告、输入列表保持不变、缓冲区精确文本以及整数 `404`
的异常位置均已通过运行核验。

扣 `0.25` 分：合同表中“会改变输出流内容和位置”对本题的 `StringIO` 成立，但不能
提升为任意兼容 `print(..., file=output)` 对象的共同合同。通用表述应为：函数按顺序
向 `output` 发起文本写入并产生由该对象定义的可观察副作用；是否具有可回读内容、
当前位置、刷新或持久化语义取决于具体输出对象。连续多次 `print()` 也不是事务，后续
写入失败不会自动撤销此前成功写入的行。

不重复扣分的边界：正式输入合同仍是 `str` 和字符串列表；额外的鸭子类型兼容性不能
自动扩大业务合同。题目中的“新字符串”应理解为规范化后的字符串结果，不应额外推出
其身份必定不同于输入对象。

### 结构与客观验证记录

使用环境：

```text
CPython 3.14.5
D:\MySoftwareDownload\PythonPractice\LearningPython5E\.venv-py314\Scripts\python.exe
```

针对性运行已覆盖 A1、A2、B1、B2、C1、C2、D1、D2、E1 和 F1：所有精确输出、
身份关系、异常类型、赋值状态、输入列表保持不变与 `StringIO` 内容均和以上审批一致。
E2 的最小实验也确认给定调用确定产生 `AttributeError`。全卷共有 `6` 个分区、`11`
道题、`11` 个非空原作答区，题目分值与分区分值都合计 `100`，且没有遗留
`QUIZ_FILL` 占位符。

### 分区与总分复核

| 分区 | 满分 | 得分 |
| --- | ---: | ---: |
| A | 16 | 16 |
| B | 18 | 18 |
| C | 22 | 22 |
| D | 20 | 20 |
| E | 14 | 14 |
| F | 10 | 9.75 |
| **总分** | **100** | **99.75** |

建议得分：`99.75 / 100`。所有逐题得分、分区小计、总分和扣分说明已复核一致。

### 本阶段末评语与能力判断

`C16_Function_Basics` 阶段测验通过。你已经稳定建立 P4 的函数基础共同词汇：能够按
“`def` 执行—函数对象—名字绑定—调用—函数体—正常返回/异常—调用者继续”追踪
对象和控制流；能够严格区分重新绑定与原地修改、返回对象与显示/I/O、正常返回
`None` 与异常退出、元数据与真实行为证据；并能把这些边界迁移到小型合同驱动设计。

当前能力继续判断为：**中级入门前段已经稳固，函数基础达到优秀，已经具备进入
C17 作用域主题所需的对象与控制流底座**。这不表示已经系统掌握完整 LEGB、复杂
参数匹配、高阶函数、生成器或基准主题；这些仍按后续章节推进。

本次审批完成且学习画像同步后，生命周期进入 `stage_note`；C16 尚未执行阶段笔记与
最终收束。

### 学习画像更新

可复用于 C16 阶段笔记与后续启动模板的稳定证据：

- **稳定强项**：能精确区分函数对象、名字/容器引用、调用表达式、返回对象和调用方
  绑定；能追踪显式/隐式返回、不可达代码、异常传播、异常前副作用和赋值未完成。
- **合同与工程迁移**：能把结构化返回、参数对象修改、输出流写入和外部持久化拆成
  不同维度，并写出包含输入、返回、异常、修改、I/O 与部分失败的有限合同。
- **证据分层**：能正确限制 `callable()`、签名、`bind()`、docstring、注解和一次
  运行实验的证明强度，不把注解提升为自动运行期类型检查。
- **当前精修点**：描述通用输出对象时只承诺调用协议和已观察效果，不把
  `StringIO` 的可回读内容/位置语义外推到所有接收器；描述字符串处理结果时也不
  无条件承诺全新对象身份。
- **水平判断**：中级入门前段已稳固；C16 建议得分 `99.75 / 100`，函数基础达到
  优秀，P4 的语言主线和工程合同边界已经建立。
- **下一阶段风险**：进入 C17 时继续区分局部名字、调用状态和名字解析规则，不把
  当前调用入口模型提前扩大成完整 LEGB；继续保留异常不自动回滚、输出不等于
  持久化、元数据不等于完整行为合同等边界。
