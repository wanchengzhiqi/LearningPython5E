# P4 / C20 — Comprehensions Revisited and Generators
## 正式测验（作答版）

- **学习阶段：** `P4_Functions_and_Generators / C20_Comprehensions_Revisited_and_Generators`
- **章节角色：** `normal`；当前章节在本卷作答与验收前仍为 `OPEN`
- **语义基线：** **Python 3.14.5**（以语言规定为准；不依赖 CPython 内部实现）
- **总题数：** 11 题；**基础总分：100 分**
- **作答状态：** 未作答 / 待提交

---

## 0. 答题与判分规则（必读）

1. **每题所有小问均须作答。** 在对应的 `【Qxx 答题区】` 与 `【Qxx 答题区结束】` 之间填写答案；允许使用代码块、时间线、表格。请保留题干、原始代码和所有答题区标记，便于逐题核验。
2. **先写可观察结果，再解释原因。** 对 `print`、返回值、事件列表、异常类型、对象 `is` 关系和实际已消费范围，给出明确答案；仅描述“大概惰性执行”不足以获得对应分值。
3. **时间与对象必须分清。** 严格区分函数对象、generator object、产出对象；创建、启动、`yield` 暂停、恢复、正常耗尽和异常终止；名字重新绑定与共享可变对象修改。
4. **异常要标明发生位置。** 若异常被题中 `try/except` 捕获，说明捕获情况和后续执行；若涉及赋值右侧失败，说明左侧绑定是否完成。题中不要求完整 traceback 或实现相关的报错消息，只要求规定的异常类别和语义。
5. **独立题目、独立命名空间。** Q01—Q11 均视为在全新 Python 3.14.5 模块命名空间中执行；未特别说明时，代码从上到下顺序执行，没有其他线程、其他消费者或隐藏操作。**输出按执行顺序解释；不能依赖 set 的打印顺序或对象地址。**
6. **正常程序行为不得自行“修复”。** 题中如果故意出现一次性 iterator 共用、重复 key、延迟异常等情况，请按原代码推导。只有题目明确要求修改时才提供替代代码。
7. **允许本地运行自检，但必须给出解释。** 答题重点是可迁移的语言模型；如果在本机运行，请核对 `.venv-py314`、`sys.version` 与 `sys.executable`。没有强制运行、截图、上传历史项目工件的要求。
8. **严格限定考查范围。** 本卷只覆盖 C20 六项必学核心及必要精度辨析：不考 `send/throw/close` 完整协议、异步、性能基准、复杂资源发布框架、数据库事务、字节码或内部 frame。
9. **评分：** 严格按每题分值与小问要求逐项给分；只给对输出但未解释关键机制者不能取得相应解释分。所有题目采用明确的 Python 3.14.5 正常语义，不以代码风格好坏替代正确性判断。

### 分值与必学目标映射

| 题号 | 核心主题 | 分值 |
|---|---|---:|
| Q01 | generator function/object，启动、暂停与恢复 | 8 |
| Q02 | 独立局部状态与共享可变对象 | 9 |
| Q03 | `return`、`StopIteration.value`、异常终止 | 9 |
| Q04 | list comprehension 的顺序与作用域 | 9 |
| Q05 | dict/set comprehension、重复与求值副作用 | 10 |
| Q06 | generator expression 创建与外部名字读取时点 | 9 |
| Q07 | `any()` 短路、剩余 iterator 与消费时点 | 9 |
| Q08 | 最小 `yield from` 顺序委托 | 10 |
| Q09 | 几类写法的工程选择 | 10 |
| Q10 | 流式管线、延迟异常及物化失败 | 9 |
| Q11 | 共享上游、浅层产出与数据所有权 | 8 |
| **合计** | **六项必学核心** | **100** |

---

## Q01（8 分）生成器对象创建、启动、暂停与恢复

阅读以下完整代码：

```python
events = []


def produce(seed):
    events.append(("start", seed))
    local = seed
    yield local
    local += 5
    events.append(("resume", local))
    yield local
    events.append(("end", local))


g = produce(2)

print("A", events)
print("B", iter(g) is g)
print("C", next(g))
print("D", events)
print("E", next(g))
print("F", list(g))
print("G", list(g))
print("H", events)
```

**作答要求：**

1. 给出 A—H 八次 `print` 的**准确输出**，保留打印时的 Python 值表示。（4 分）
2. 分清 `produce`、`g`、两次 `yield` 所产出的值分别属于什么对象/角色；说明调用 `produce(2)` 时是否已经执行 `events.append(...)`。（2 分）
3. 解释 `local` 是否在两次 `next()` 之间重新初始化；解释 F、G 为什么都得到该结果，以及 `("end", ...)` 在何时写入。（2 分）

**【Q01 答题区】**

（在此填写答案）

**【Q01 答题区结束】**

---

## Q02（9 分）不同生成器对象的局部绑定与共享引用

```python
shared = {"n": 0}


def count(label, state):
    own = 0
    while own < 2:
        own += 1
        state["n"] += 1
        yield (label, own, state["n"])


a = count("A", shared)
b = count("B", shared)

print("I", a is b)
print("II", next(a))
print("III", next(b))
print("IV", next(a))
print("V", shared)
print("VI", next(b))
print("VII", list(a), list(b))
```

**作答要求：**

1. 给出 I—VII 的准确输出。（5 分）
2. 用对象与绑定模型解释：为什么 `a`、`b` 的 `own` 不会互相覆盖，但 `state["n"]` 的变化会被双方看见？（3 分）
3. 说明这里的“生成器执行状态独立”**不能**推出什么关于输入可变对象的结论。（1 分）

**【Q02 答题区】**

（在此填写答案）

**【Q02 答题区结束】**

---

## Q03（9 分）产出值、终止值与错误的 `StopIteration`

```python
def finished():
    yield "item"
    return "receipt"


g = finished()
print("A", next(g))
try:
    next(g)
except StopIteration as exc:
    print("B", exc.value)
print("C", next(g, "END"))
print("D", list(finished()))


def wrong():
    yield "item"
    raise StopIteration("manual")


h = wrong()
print("E", next(h))
try:
    next(h)
except Exception as exc:
    print("F", type(exc).__name__)
```

**作答要求：**

1. 给出 A—F 的准确输出。（4 分）
2. 区分 `yield "item"` 与 `return "receipt"` 的作用；为什么 `list(finished())` 不含 `"receipt"`？（2 分）
3. 解释 `wrong()` 的终止方式、捕获的异常类别，以及为什么不应把 `raise StopIteration` 用作生成器内部的常规 `return` 替代品。（2 分）
4. 假设 `finished()` 中的 `return "receipt"` 被删掉，让函数自然结束，正常耗尽时 `StopIteration.value` 应是什么？（1 分）

**【Q03 答题区】**

（在此填写答案）

**【Q03 答题区结束】**

---

## Q04（9 分）List comprehension 的执行顺序与局部作用域

```python
events = []
x = "outside"


def mark(v):
    events.append(("mark", v))
    return v + 1


result = [
    mark(a * b)
    for a in (1, 2)
    for b in (10, 20)
    if a * b >= 20
]

print("A", result)
print("B", events)
print("C", x)

try:
    print("D", a)
except NameError as exc:
    print("D", type(exc).__name__)
```

**作答要求：**

1. 给出 A—D 的准确输出。（4 分）
2. 列出全部 `(a, b)` 候选组合及各组合的 `if` 结果；明确 `mark()` 实际调用顺序。（3 分）
3. 解释推导式目标变量 `a` 为什么没有成为外层可用绑定；并指出该表达式最终创建的结果对象类别。（2 分）

**【Q04 答题区】**

（在此填写答案）

**【Q04 答题区结束】**

---

## Q05（10 分）Dict/set comprehension：key/value 求值、重复覆盖与副作用

```python
events = []


def make_key(n):
    events.append(("key", n))
    return "dup" if n < 3 else "other"


def make_value(n):
    events.append(("value", n))
    return n * 10


mapping = {
    make_key(n): make_value(n)
    for n in (1, 2, 3)
}

unique = {
    make_value(n)
    for n in (1, 2, 2)
}

print("A", mapping)
print("B", unique == {10, 20})
print("C", events)
```

**作答要求：**

1. 给出 A、B、C 的准确输出；**不要按某一种集合打印顺序写出 `unique` 的显示字符串**，B 只需给出布尔输出。（5 分）
2. 对 dict comprehension，逐项说明 `make_key` 与 `make_value` 的调用先后，并说明重复 `"dup"` key 的最终结果。（3 分）
3. 为什么 set comprehension 去重以后，事件中仍会记录两次 `make_value(2)`？结果去重是否意味着之前的表达式求值与副作用被撤销？（2 分）

**【Q05 答题区】**

（在此填写答案）

**【Q05 答题区结束】**

---

## Q06（9 分）Generator expression：最左侧求值与晚读取的外部名字

```python
events = []


def get_source():
    events.append("source-called")
    return [1, 2, 3]


factor = 10
threshold = 1

g = (
    n * factor
    for n in get_source()
    if n > threshold
)

print("A", events)

factor = 5
print("B", next(g))

factor = 7
print("C", list(g))
print("D", list(g))
print("E", events)
```

**作答要求：**

1. 给出 A—E 的准确输出。（4 分）
2. 说明 `get_source()` 在什么时点调用；生成器表达式创建时是否已经把 `n * factor` 的全部结果计算出来？（2 分）
3. 解释两个不同的 `factor` 值分别在什么时点被读取；`threshold` 参与筛选的时点是什么？（2 分）
4. 为什么 D 不会重新生成原始序列？（1 分）

**【Q06 答题区】**

（在此填写答案）

**【Q06 答题区结束】**

---

## Q07（9 分）消费者短路，不等于生产者已经正常耗尽

```python
events = []


def values():
    for value in (0, 2, 3):
        events.append(("before", value))
        yield value
        events.append(("after", value))
    events.append(("done",))


g = values()

print("A", any(g))
print("B", events)
print("C", next(g))
print("D", list(g))
print("E", events)
```

**作答要求：**

1. 给出 A—E 的准确输出。（5 分）
2. 解释 `any(g)` 停止时生成器暂停在哪里；为什么 B 尚未包含 `("after", 2)`？（2 分）
3. 说明 C、D 各自推进了哪些代码，以及 E 中 `("done",)` 代表的执行事实。（2 分）

**【Q07 答题区】**

（在此填写答案）

**【Q07 答题区结束】**

---

## Q08（10 分）最小 `yield from`：顺序委托子迭代

```python
events = []


def child(label, data):
    events.append(("child-start", label))
    for value in data:
        events.append(("child-yield", value))
        yield value
    events.append(("child-end", label))


def outer():
    events.append("outer-start")
    yield "HEADER"
    yield from child("A", (1, 2))
    events.append("between")
    yield from []
    yield "FOOTER"
    events.append("outer-end")


g = outer()
print("A", next(g))
print("B", events)
print("C", next(g))
print("D", next(g))
print("E", next(g))
print("F", list(g))
print("G", events)
```

**作答要求：**

1. 给出 A—G 的准确输出。（5 分）
2. 解释子迭代何时开始、外层何时恢复执行 `"between"`，以及空 iterable 的委托对控制流的影响。（3 分）
3. 对比 `yield from (1, 2)` 与 `yield (1, 2)` 的产出项数和形态；说明 `yield from` 是否自动复制子数据或创建并发任务。（2 分）

**【Q08 答题区】**

（在此填写答案）

**【Q08 答题区结束】**

---

## Q09（10 分）工程选择：根据返回与消费合同选用语言结构

假设输入是内存中有限的本地化记录；除各小问特别规定外，记录均符合预期数据类型。请在每个小问中指出**最自然的主要结构**（`list comprehension`、`set comprehension`、`dict comprehension`、`generator expression + consumer`、`generator function` 或显式 `for`），并简要解释它满足了哪一项合同。允许多个方案都可行，但必须说明为什么你的首选符合要求。

**情形 A（2 分）**：按输入顺序立即返回全部启用记录的 key；允许重复 key；返回对象需要能够反复从头遍历。

**情形 B（1 分）**：只需要唯一的命名空间名称，不要求结果迭代顺序。

**情形 C（2 分）**：构建完整的 `key -> text` 映射。先考虑业务**允许重复 key 后值覆盖**时的最直接结构；再说明若要求“任何重复 key 必须报错”，为什么应改变写法或增加什么检查。

**情形 D（1 分）**：只需要判断是否存在至少一条空白文本；找到第一条即可停止；无需收集全部问题清单。

**情形 E（2 分）**：逐条惰性产出规范化记录；每条有多步骤检查、可能 `continue`，还要在暂停之间保留局部计数状态。

**情形 F（2 分）**：输入可能是**一次性 iterator**；必须在一次完整扫描中同时构造合格映射和完整问题清单，并在普通函数返回时提供最终报告。为什么不宜先 `any()` 消费一部分上游，再用另一个推导式读取同一个上游来构建完整结果？

**【Q09 答题区】**

（在此填写答案）

**【Q09 答题区结束】**

---

## Q10（9 分）流式处理、延迟失败与赋值边界

```python
events = []


def normalize(records):
    for key, raw in records:
        events.append(("read", key))
        if not isinstance(raw, str):
            events.append(("bad", key))
            raise TypeError(key)
        result = (key, raw.strip())
        events.append(("emit", key))
        yield result


records = [
    ("a", " A "),
    ("b", " B "),
    ("c", None),
    ("d", " D "),
]

g = normalize(records)
first = next(g)

try:
    tail = list(g)
except TypeError as exc:
    caught = type(exc).__name__

print("A", first)
print("B", caught)
print("C", events)
print("D", next(g, "END"))
```

**作答要求：**

1. 给出 A—D 的准确输出。（4 分）
2. 在本题独立命名空间中，执行完以上代码后，`tail` 是否成功绑定？`list(g)` 内部是否曾收到记录 `"b"` 的产出？解释两者为何不矛盾。（2 分）
3. 明确哪条输入记录没有被 `normalize()` 读取，哪些事件副作用保留；解释 `next(g, "END")` 与“此前已完整成功扫描”之间是否存在必然推论。（3 分）

**【Q10 答题区】**

（在此填写答案）

**【Q10 答题区结束】**

---

## Q11（8 分）共享上游 iterator、产出新容器与引用所有权

```python
records = [
    {"key": "a", "meta": {"tags": []}},
    {"key": "b", "meta": {"tags": []}},
]


def project(source):
    for record in source:
        yield {
            "key": record["key"],
            "meta": record["meta"],
        }


upstream = iter(records)
p = project(upstream)
q = project(upstream)

x = next(p)
y = next(q)
x["meta"]["tags"].append("changed")

print("A", x["key"], y["key"])
print("B", x is records[0])
print("C", x["meta"] is records[0]["meta"])
print("D", records[0]["meta"]["tags"])
print("E", list(p), list(q))
```

**作答要求：**

1. 给出 A—E 的准确输出。（4 分）
2. 分别解释 `x` 的**外层 dict 身份**与它的**嵌套 `meta` 引用**；为什么修改 `x["meta"]["tags"]` 会影响原始记录？（2 分）
3. 如果需要让 `p`、`q` **各自完整遍历全部原始记录**，应怎样改变上游 iterator 的创建方式？如果还要求输出结果中的可变 `meta` 与原始记录隔离，单纯使用 `dict(record)` 是否足够？给出理由。（2 分）

**【Q11 答题区】**

（在此填写答案）

**【Q11 答题区结束】**

---

## 12. 提交前自检与提交方式

完成后请确保：

- [ ] Q01—Q11 的每个答题区内均已填写答案，全部小问均有回应。
- [ ] 对输出顺序、`events` 顺序、异常时点和共享 iterator 的消费范围有明确描述。
- [ ] 对象身份使用 `is` 的语义推导，不依赖内存地址、`id()` 输出或内部 frame。
- [ ] 没有把调用 generator function 等同于执行函数体，没有把 `yield` 等同于 `return`。
- [ ] 没有将本地化发布框架、协程协议或 benchmark 加入作答范围。

**建议保存文件名：** `comprehensions_revisited_and_generators.md`。

**推荐提交方式：** 直接上传填写后的 Markdown 文件，并说明“这是 C20 正式测验作答版，请按原卷规则逐题严格批改”。无需额外上传 C19、P3 或其它相应的可选工件。
