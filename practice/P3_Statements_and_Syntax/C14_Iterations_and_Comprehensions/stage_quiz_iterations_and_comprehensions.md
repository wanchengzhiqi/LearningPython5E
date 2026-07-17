# Stage Quiz: Iterations and Comprehensions

本测验用于当前小阶段：**迭代协议、一次性消费、推导式、惰性求值与工程边界**。

它不要求把所有循环改写得更短，而是检查你能否准确判断：哪个对象提供迭代器，哪个对象记录消费进度，何时发生求值，消费者会推进到哪里，以及简单过滤/投影与复杂扫描报告分别适合什么写法。

总分：100 分。

## 测验覆盖边界

本卷计分范围来自 C14 启动模板的必修主线：

1. iterable、iterator、`iter()`、`next()`、`StopIteration` 与 `for` 背后的协议；
2. 可重复遍历容器与 file、zip、map、filter、生成器表达式等一次性对象；
3. 文件式对象的共享位置与 EOF 契约；
4. 列表、集合、字典推导式及生成器表达式的过滤、转换、嵌套顺序和作用域；
5. 惰性/急切求值、短路消费、重复消费与物化边界；
6. 稳定报告、字典碰撞、`zip()` 对齐与多消费者风险；
7. 本地化资源处理中推导式与显式循环的工程选择。

`iter(callable, sentinel)`、`tee()`、`islice()`、`takewhile()`、`dropwhile()`、`groupby()`、`pairwise()` 和 `batched()` 属于本会话中的可选延伸，本卷不把这些 API 的专属行为列入计分范围。

答题规则：

1. 第一遍不要运行代码，先写完整输出顺序、对象状态、消费位置和理由。
2. 第二遍可以使用当前日常学习环境 Python `3.14.5` 验证，并保留“验证前预测”和“验证后修正”。
3. 代码题优先按这条链解释：表达式何时求值；谁调用 `iter()`；谁调用 `next()`；当前元素是否通过过滤；消费者何时停止；源容器和迭代器最后各是什么状态。
4. 不要只写“因为它是惰性的”；要说明惰性行为由哪个消费者、哪一次索取触发。
5. 本卷不包含参考答案。若认为题目有歧义，可以明确指出并说明采用的解释。
6. 作答后我会保留你的原答案，并在文件末尾追加逐题批改记录。

---

## A. 概念边界：可迭代对象、迭代器与求值模型（15 分）

### A1. 说法纠偏（8 分）

逐条判断下面说法是否准确；若不准确，请改写成更精确的说法。

```tex
1. 所有 iterable 都同时是 iterator，因此都可以直接传给 next()。
2. 对列表调用 iter(items) 时，返回值一定就是 items 自身。
3. next(iterator) 在耗尽时返回 None，所以 None 不能作为正常元素。
4. for 循环会反复调用 next()，并把 StopIteration 当成正常结束信号处理。
5. 列表推导式和生成器表达式都在创建时完成全部计算，只是括号不同。
6. 推导式隔离内部循环变量，因此推导式不可能修改外部对象。
7. bool(generator) 可以可靠判断生成器是否还剩元素。
8. 直接遍历字典默认产出 key；sorted(some_set) 返回新列表，不会修改原集合。
```

要求至少准确说明：

1. iterable 与 iterator 的关系；
2. `None` 数据与 `StopIteration` 的区别；
3. 推导式作用域隔离的是名字绑定还是对象副作用；
4. 为什么生成器对象的真值不是通用的空检测接口。

答题区：

验证前预测：

1. **不准确。** iterable（可迭代对象）表示 `iter(obj)` 能取得一个迭代器；iterator（迭代器）则是实际保存遍历进度、能由 `next()` 逐项取值的对象。所有合格迭代器都同时是 iterable，因为 `iter(iterator)` 应返回其自身；但列表、元组、字符串、`range`、字典视图等 iterable 自身通常不是 iterator，不能直接交给 `next()`。

   更精确地改写为：

   > 所有 iterator 都是 iterable；并非所有 iterable 都是 iterator。对普通 iterable 应先通过 `iter(obj)` 取得迭代器，再对该迭代器调用 `next()`。

2. **不准确。** 对列表调用 `iter(items)` 通常返回一个新的 `list_iterator`，而不是列表自身，所以：

   ```python
   iter(items) is items
   ```

   为 `False`。多次调用 `iter(items)` 通常会取得彼此独立、从头开始的列表迭代器。

3. **不准确。** 没有为 `next()` 提供默认值时，迭代器耗尽会抛出 `StopIteration`；只有写成：

   ```python
   next(iterator, default)
   ```

   时，耗尽才返回指定的 `default`。`None` 可以完全合法地作为迭代数据，例如迭代 `[None, "HP"]` 时，第一项就是正常数据 `None`。协议结束由 `StopIteration` 表示，而不是由某个普通数据值表示。

4. **准确，但应补充边界。** `for` 会先取得迭代器，然后反复请求下一项；迭代器以 `StopIteration` 表示正常耗尽，`for` 捕获这个协议信号并正常结束。这里的“等价展开”是理解语义的模型，不表示解释器必定逐字执行一段 Python `while/try` 代码。

5. **不准确。** 列表推导式是急切求值：赋值语句结束时，遍历、过滤、转换和列表构造已经完成。生成器表达式创建的是惰性生成器对象；除最左侧 iterable 表达式的求值、对应的迭代器的获取等必要步骤外，逐项循环体通常要等 `next()`、`for`、`list()`、`sum()`、`any()` 等消费者索取元素时才执行。

6. **不准确。** 推导式隔离的是其内部循环目标等**名字绑定**，并不保证没有对象副作用。推导式表达式或过滤条件可以调用会修改外部列表、字典、文件或对象属性的函数。例如：

   ```python
   collected = []
   result = [collected.append(x) for x in range(3)]
   ```

   推导式内部的循环变量不会泄漏，但外部 `collected` 已被修改；同时 `result` 还是无意义的 `[None, None, None]`。因此“作用域隔离”和“无副作用”是两回事。

7. **不准确。** 普通生成器对象没有把“是否还有元素”定义为其真值协议；只要对象存在，`bool(generator)` 通常就是 `True`，即使它尚未开始、已部分消费或已经耗尽。若要知道是否还有下一项，只能尝试消费，例如使用 `next(generator, sentinel)`；但这会推进状态。不存在适用于任意迭代器、既可靠又完全不消费的通用空检测接口。

8. **准确。** 直接遍历字典默认产出 key。`sorted(some_set)` 会消费集合的迭代结果，建立并返回一个新的排序列表，不会原地修改原集合。集合本身的迭代顺序不应用作稳定报告契约，因此对外报告通常显式排序。

验证后修正：

已在当前解释器中用列表、列表迭代器、含 `None` 的迭代器、生成器耗尽状态和集合排序进行了运行验证，结论与验证前预测一致，无需修改。需要保留的限定是：上述结论描述 Python 迭代协议和标准内置对象的正常行为；自定义对象仍可能在 `__iter__()`、`__next__()` 或真值方法中加入非典型副作用。

### A2. 对象分类与重复消费（7 分）

阅读下面的对象创建代码：

```python
from io import StringIO

items = ["HP", "MP"]
list_iterator = iter(items)
zipped = zip(["ui.hp", "ui.mp"], ["Health", "Mana"])
mapped = map(str.upper, ["hp", "mp"])
filtered = filter(str.strip, ["HP", "   ", "MP"])
generated = (text.strip() for text in [" HP ", " MP "])
stream = StringIO("HP\nMP\n")
```

请分别说明 `items`、`list_iterator`、`zipped`、`mapped`、`filtered`、`generated` 和 `stream`：

1. 它是 iterable、iterator，还是二者兼具；
2. `iter(obj) is obj` 通常是 `True` 还是 `False`；
3. 连续两次对同一个对象执行 `list(obj)`，通常能否得到两份完整内容；
4. `stream.seek(0)` 为什么属于文件 API 的额外能力，而不是通用迭代协议的重置操作。

答题区：

验证前预测：

| 对象            | 协议角色                      | `iter(obj) is obj` | 连续两次 `list(obj)`                                         | 说明                                                         |
| --------------- | ----------------------------- | -----------------: | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `items`         | iterable，但自身不是 iterator |            `False` | 两次通常都得到 `["HP", "MP"]`                                | 列表每次可创建新的独立列表迭代器；`list(items)` 遍历的是临时迭代器，不会耗尽列表本身。 |
| `list_iterator` | iterable 与 iterator 兼具     |             `True` | 第一次得到 `["HP", "MP"]`，第二次得到 `[]`                   | 消费位置保存在同一个列表迭代器中；第一次 `list()` 将其完整耗尽。 |
| `zipped`        | iterable 与 iterator 兼具     |             `True` | 第一次得到 `[("ui.hp", "Health"), ("ui.mp", "Mana")]`，第二次得到 `[]` | `zip()` 返回惰性迭代器，按位置并行取得各输入的下一项。       |
| `mapped`        | iterable 与 iterator 兼具     |             `True` | 第一次得到 `["HP", "MP"]`，第二次得到 `[]`                   | `map()` 返回迭代器；只有消费者索取时才调用 `str.upper`。     |
| `filtered`      | iterable 与 iterator 兼具     |             `True` | 第一次得到 `["HP", "MP"]`，第二次得到 `[]`                   | `filter()` 返回迭代器；`str.strip("   ")` 的结果为空字符串，真值为假，因此空白项被过滤。它产出的是原始元素，而不是谓词的返回值。 |
| `generated`     | iterable 与 iterator 兼具     |             `True` | 第一次得到 `["HP", "MP"]`，第二次得到 `[]`                   | 生成器表达式创建生成器迭代器，逐项执行 `text.strip()`，消费后不能从同一对象重新开始。 |
| `stream`        | iterable 与 iterator 兼具     |      通常为 `True` | 第一次得到 `["HP\n", "MP\n"]`，第二次得到 `[]`               | `StringIO` 是文本流和文件式迭代器，迭代时按行读取；读操作共享一个当前流位置。 |

各对象创建后均尚未被消费，因此上表“第一次”的内容都从各自开头开始。

`stream.seek(0)` 是流对象额外提供的随机访问能力：它把该 `StringIO` 的流位置改回开头。通用迭代协议只规定 `iter()`、`next()` 和 `StopIteration` 等行为，并没有 `reset()`、`rewind()` 或 `seek()`。普通生成器、`zip`、`map` 和 `filter` 对象没有统一的重置操作；因此不能因为某些文件式对象可 `seek(0)`，就推导出所有迭代器都能重置。

还应区分：

- “同一迭代器按当前位置向前消费”是迭代协议层的模型；
- “底层对象是否允许重新定位”是具体 API 的额外能力；
- 即使文件可 `seek()`，也必须由调用者显式执行，耗尽后的再次 `iter(stream)` 不会自动回到开头。

验证后修正：

运行验证结果与上表一致。`StringIO("HP\nMP\n")` 初始位置在缓冲区开头；第一次 `list(stream)` 读取两行并到达 EOF，第二次为空；执行 `stream.seek(0)` 后才可再次从 `"HP\n"` 开始。

---

## B. 协议与流位置：逐项消费、默认值和 EOF（18 分）

### B1. 独立迭代器、真实 `None` 与剩余状态（9 分）

预测八行输出，并说明每一步后 `a`、`b` 和 `items` 的状态。

```python
items = [None, "HP", "MP"]
a = iter(items)
b = iter(items)

print(iter(a) is a)
print(a is b)
print(next(a, "END"))
print(next(a, "END"))
print(next(b, "END"))
print(list(a))
print(next(a, "END"))
print(items)
```

要求至少说明：

1. 两个迭代器是否共享消费位置；
2. 第一项 `None` 为什么不是结束信号；
3. `list(a)` 从哪里开始收集；
4. 为什么源列表不应描述为“被耗尽”。

答题区：

验证前预测：

完整八行输出为：

```tex
True
False
None
HP
None
['MP']
END
[None, 'HP', 'MP']
```

逐步状态如下：

1. `a = iter(items)` 和 `b = iter(items)` 分别创建两个独立的 `list_iterator`。二者都引用同一个底层列表，但各自保存自己的遍历索引。

2. `print(iter(a) is a)` 输出 `True`。`a` 已经是迭代器，其 `iter()` 返回自身。此时：
   - `a` 剩余：`None, "HP", "MP"`；
   - `b` 剩余：`None, "HP", "MP"`；
   - `items` 内容未变。

3. `print(a is b)` 输出 `False`。`a`、`b` 是两个不同迭代器，因此不共享消费位置。

4. `print(next(a, "END"))` 输出 `None`。这是列表中的真实第一项，不是结束信号。调用后：
   - `a` 剩余：`"HP", "MP"`；
   - `b` 仍剩余：`None, "HP", "MP"`。

5. 第二次 `next(a, "END")` 输出 `HP`。此后：
   - `a` 剩余：`"MP"`；
   - `b` 未受影响。

6. `next(b, "END")` 输出 `None`。`b` 才开始消费自己的第一项。此后：
   - `b` 剩余：`"HP", "MP"`；
   - `a` 仍只剩 `"MP"`。

7. `list(a)` 从 **a 的当前消费位置** 开始完整消费，而不是从源列表开头开始，因此收集 `["MP"]`，并把 `a` 完整耗尽。

8. 耗尽后再调用 `next(a, "END")`，由于提供了默认值，输出 `END`；若未提供默认值，则会抛出 `StopIteration`。

9. 最后 `items` 仍为 `[None, "HP", "MP"]`。迭代只推进 `a` 和 `b` 各自保存的遍历索引，没有删除或修改列表元素。所以准确说法是“迭代器被耗尽”，而不是“源列表被耗尽”。

验证后修正：

运行结果与预测完全一致，无需修正。额外确认：真实数据 `None` 会原样返回；只有迭代器的 `__next__()` 抛出 `StopIteration`，或 `next(iterator, default)` 在耗尽时返回 default，才表示没有下一项。

### B2. `StringIO` 的共享游标与两种 EOF 契约（9 分）

预测完整输出：

```python
from io import StringIO

stream = StringIO("HP\nMP\nSP\n")

print(repr(next(stream)))
print(repr(stream.readline()))
print(list(stream))
print(next(stream, "END"))
print(repr(stream.readline()))

stream.seek(0)
print(repr(next(stream)))
```

要求至少说明：

1. `next()`、`readline()` 和 `list(stream)` 是否共享同一个位置；
2. 为什么迭代协议耗尽与 `readline()` 到 EOF 的结果不同；
3. `seek(0)` 改变了什么；
4. 为什么 `seek(0)` 不推翻“一次性向前消费”的通用迭代器模型。

答题区：

验证前预测：

完整输出为：

```tex
'HP\n'
'MP\n'
['SP\n']
END
''
'HP\n'
```

消费过程：

1. `next(stream)` 使用文件对象的迭代器接口读取当前行，返回 `"HP\n"`；`repr()` 使换行符显示为 `\n`。流位置移动到第一行之后。

2. `stream.readline()` 从**同一个当前流位置**继续读取当前行，返回 `"MP\n"`，流位置移动到第二行之后。`next()` 和 `readline()` 并没有各自独立的游标。

3. `list(stream)` 从当前位置开始按行完整消费，由于迭代器当前只剩 `"SP\n"`，因此得到：

   ```python
   ["SP\n"]
   ```

   完成后流位置位于 EOF。

4. `next(stream, "END")` 在迭代器已耗尽时返回默认值 `"END"`。如果没有默认值，则由迭代协议抛出 `StopIteration`。

5. `stream.readline()` 在已经位于 EOF 时返回空字符串 `""`，所以 `repr()` 输出 `''`。这是**文件读取 API 的 EOF 契约**，与迭代器通过 `StopIteration` 表示耗尽不同。

6. `stream.seek(0)` 把同一个流对象的当前位置显式设置回缓冲区开头。它没有创建新流，也没有恢复一个通用迭代器快照；只是调用了 `StringIO` 具体支持的定位 API。

7. 重新定位后，`next(stream)` 再次读取第一行，所以输出 `'HP\n'`。

`seek(0)` 不推翻“一次性向前消费”的模型：在没有显式 seek 时，同一 `stream` 的 `next()`、`readline()`、`for` 和 `list(stream)` 都共享并推进同一位置。可 seek 是某些流对象的附加能力，并不是每个 iterator 都具有的协议能力。

验证后修正：

运行验证与预测一致，无需修正。需要特别保留两种 EOF 表达：

- 迭代协议：耗尽时抛出 `StopIteration`，或由带默认值的 `next()` 返回默认值；
- 文本流 `readline()`：流已在 EOF 时返回空字符串 `""`。

---

## C. 推导式：过滤、转换、作用域、集合与字典（20 分）

### C1. 列表推导式的执行顺序与作用域（8 分）

预测完整输出顺序：

```python
text = "OUTER"
raw = [" hp ", "   ", " mp "]


def keep(value):
    print(f"keep({value!r})")
    return bool(value.strip())


def normalize(value):
    print(f"normalize({value!r})")
    return value.strip().upper()


result = [normalize(text) for text in raw if keep(text)]

print(result)
print(repr(text))
print(raw)
```

要求至少说明：

1. 为什么 `keep()` 先于 `normalize()`；
2. 空白元素为什么仍进入 `keep()`，却不进入 `normalize()`；
3. 赋值语句结束时计算是否已经全部完成；
4. 推导式内部 `text` 与外层 `text` 的绑定关系；
5. 写出语义等价的清晰显式循环，并指出循环变量作用域方面的差异。

答题区：

验证前预测：

完整输出顺序为：

```tex
keep(' hp ')
normalize(' hp ')
keep('   ')
keep(' mp ')
normalize(' mp ')
['HP', 'MP']
'OUTER'
[' hp ', '   ', ' mp ']
```

执行顺序按每个输入元素逐项展开：

1. 对 `" hp "`，先执行过滤条件 `keep(text)`：
   - 打印 `keep(' hp ')`；
   - `value.strip()` 为 `"hp"`，真值为真。
     条件通过后才计算结果表达式 `normalize(text)`，打印 `normalize(' hp ')`，产出 `"HP"`。

2. 对 `"   "`，仍然必须调用 `keep()` 才能知道它是否通过：
   - 打印 `keep('   ')`；
   - `strip()` 后为空字符串，条件为假。
     因此不会调用 `normalize()`，也不会向结果列表加入元素。

3. 对 `" mp "`，先打印 `keep(' mp ')`，条件通过后打印 `normalize(' mp ')`，产出 `"MP"`。

这是列表推导式，属于急切容器构造。执行：

```python
result = [...]
```

的赋值语句结束时，所有遍历、过滤、规范化和列表填充已经完成，不会等到后面的 `print(result)` 才计算。

推导式内部的 `text` 是其隐式局部作用域中的循环目标，对它的重新绑定并不会覆盖外层原有绑定：

```python
text = "OUTER"
```

所以后续 `repr(text)` 仍为 `'OUTER'`。至于 `raw` 只是被读取，没有原地修改，内容保持不变。

等价显式循环：

为了保留与原程序相同的外部绑定效果，可使用不同的循环变量名：

```python
result = []

for candidate in raw:
    if keep(candidate):
        result.append(normalize(candidate))
```

它保持相同的调用顺序和结果，并且不会改写外层名字 `text`。

若机械地写成：

```python
result = []

for text in raw:
    if keep(text):
        result.append(normalize(text))
```

则过滤和转换顺序相同，但普通 `for` 不创建块级/推导式局部作用域；循环结束后，外层 `text` 会绑定到最后一项 `" mp "`。因此这只能称为数据处理顺序上的展开，不能称为外部名字绑定效果完全等价。

验证后修正：

运行输出与预测一致，无需修正。

### C2. 集合去重、字典碰撞与稳定报告（6 分）

预测四行输出，并解释顺序与覆盖规则：

```python
records = [
    ("UI.HP", "Health"),
    ("ui.mp", "Mana"),
    ("ui.hp", "HP"),
    ("ui.debug", "   "),
]

nonempty_keys = {
    key.strip().lower()
    for key, text in records
    if text.strip()
}

text_by_key = {
    key.strip().lower(): text.strip()
    for key, text in records
    if text.strip()
}

print(sorted(nonempty_keys))
print(text_by_key)
print(list(text_by_key))
print(sorted(text_by_key.items()))
```

要求至少说明：

1. 哪条记录被过滤；
2. 哪两个 key 规范化后发生碰撞，最终保留哪个值；
3. 覆盖已有 key 是否会移动其插入位置；
4. 为什么结构化报告通常显式排序；
5. 如果重复 key 是数据错误，为什么不能只依赖字典推导式。

答题区：

验证前预测：

四行输出为：

```tex
['ui.hp', 'ui.mp']
{'ui.hp': 'HP', 'ui.mp': 'Mana'}
['ui.hp', 'ui.mp']
[('ui.hp', 'HP'), ('ui.mp', 'Mana')]
```

逐条处理：

1. `("UI.HP", "Health")`
   - `text.strip()` 为 `"Health"`，通过过滤；
   - key 规范化为 `"ui.hp"`；
   - 集合加入 `"ui.hp"`；
   - 字典首次插入 `"ui.hp": "Health"`。

2. `("ui.mp", "Mana")`
   - `text.strip()` 为 `"Mana"`，通过过滤；
   - key 规范化为 `"ui.mp"`；
   - 集合加入 `"ui.mp"`；
   - 字典插入 `"ui.mp": "Mana"`。

3. `("ui.hp", "HP")`
   - `text.strip()` 为 `"HP"`，通过过滤；
   - 规范化 key 仍是 `"ui.hp"`，与第一条发生碰撞；
   - 集合因去重仍只有一个 `"ui.hp"`；
   - 字典中后产生的 value `"HP"` 覆盖此前的 `"Health"`。

4. `("ui.debug", "   ")`
   - `text.strip()` 为空字符串，过滤条件为假，因此这条记录要被过滤；
   - 不进入集合，也不进入字典。

更新已有字典 key 的 value 不等于删除后重新插入，所以 `"ui.hp"` 仍保留第一次插入时的位置；`"ui.mp"` 仍在其后。因此字典和 `list(text_by_key)` 的顺序为 `ui.hp, ui.mp`。

结构化报告之所以通常显式排序，原因包括：

- 集合不承担业务排序契约；
- 输入来源可能改变；
- 稳定排序便于测试、日志比较、JSON diff 和人工复盘；
- 排序把“结果内容”与“偶然的内部/输入顺序”分离。

如果重复 key 是数据错误，不能只依赖字典推导式，因为字典构造会静默保留最后一个 value，丢失碰撞事实、原始行号、先后记录及被覆盖值。此时应使用显式循环，先检测 `if normalized_key in mapping`，再记录结构化 duplicate issue，并根据业务规则决定保留第一次还是最后一次。

验证后修正：

运行输出与预测完全一致，无需修正。

### C3. 嵌套推导式与等价循环（6 分）

预测结果，并写出保持执行顺序一致的显式循环：

```python
groups = [
    ("menu", True, [" hp ", "   "]),
    ("debug", False, [" trace "]),
    ("battle", True, [" mp ", " sp "]),
]

result = [
    f"{section}.{text.strip().lower()}"
    for section, enabled, texts in groups
    if enabled
    for text in texts
    if text.strip()
]

print(result)
```

要求至少说明：

1. 各个 `for` 和 `if` 的真实嵌套顺序；
2. 为什么 `debug` 的内层元素不会被访问；
3. `section`、`enabled`、`texts` 和 `text` 是否泄漏到外层；
4. 什么时候应把这种嵌套推导式改回显式循环。

答题区：

验证前预测：

输出为：

```tex
['menu.hp', 'battle.mp', 'battle.sp']
```

推导式的真实嵌套顺序从左到右读取：

```tex
for section, enabled, texts in groups      # 外层循环
    if enabled                             # 外层过滤
        for text in texts                  # 内层循环
            if text.strip()                # 内层过滤
                计算 f"{section}.{...}"    # 产出结果
```

具体过程：

- `("menu", True, [" hp ", "   "])`：外层过滤通过；内层访问两项，`" hp "` 保留并产出 `"menu.hp"`，纯空白项被过滤。
- `("debug", False, [" trace "])`：外层 `if enabled` 不通过，因此不会进入 `for text in texts`；`" trace "` 根本不会被访问。
- `("battle", True, [" mp ", " sp "])`：外层过滤通过；内层访问两项，两项均通过，依次产出 `"battle.mp"`、`"battle.sp"`。

在 Python 3 中，`section`、`enabled`、`texts` 和 `text` 都是推导式内部的循环目标名字，不会泄漏到外层作用域；若外层原来存在同名变量，也不会被这些循环目标重新绑定。

等价显式循环：

```python
result = []

for section_value, enabled_value, text_values in groups:
    if enabled_value:
        for text_value in text_values:
            if text_value.strip():
                result.append(
                    f"{section_value}.{text_value.strip().lower()}"
                )
```

使用不同变量名可同时保留外层名字绑定效果。若使用与推导式完全同名的普通 `for` 变量，它们会留在当前作用域，作用域副作用不同。

应把嵌套推导式改回显式循环的典型情况有：

- 每条记录可能产生多种 issue；
- 需要日志、统计、异常处理或 `continue`/`break`；
- 需要保存中间值，避免重复执行昂贵转换；
- 嵌套层次继续增加，读者难以快速确认执行顺序；
- 需要调试每层状态或生成结构化审计报告。

验证后修正：

运行结果与预测一致，无需修正。

---

## D. 惰性管道与短路消费者（18 分）

### D1. `filter()`、`map()` 与终端消费者（9 分）

预测完整输出顺序：

```python
def keep(value):
    print(f"keep({value!r})")
    return bool(value.strip())


def normalize(value):
    print(f"normalize({value!r})")
    return value.strip().upper()


raw = [" hp ", "   ", " mp "]
pipeline = map(normalize, filter(keep, raw))

print("A")
print(next(pipeline))
print("B")
print(list(pipeline))
print("C")
print(list(pipeline))
print(raw)
```

要求至少说明：

1. 创建 `pipeline` 时两个函数各调用几次；
2. 第一次 `next()` 为得到一个结果，读取了多少个源元素；
3. `filter()` 产出的是什么，`map()` 产出的又是什么；
4. 第一次 `list()` 为什么只收集剩余结果；
5. 第二次 `list()`、源列表和管道对象分别是什么状态。

答题区：

验证前预测：

完整输出顺序为：

```tex
A
keep(' hp ')
normalize(' hp ')
HP
B
keep('   ')
keep(' mp ')
normalize(' mp ')
['MP']
C
[]
[' hp ', '   ', ' mp ']
```

分析如下：

1. 创建：

   ```python
   pipeline = map(normalize, filter(keep, raw))
   ```

   时，`filter` 和 `map` 迭代器被建立，但没有终端消费者索取元素，所以 `keep()` 和 `normalize()` 都调用 **0 次**。因此先打印 `A`。

2. `next(pipeline)` 是第一次终端索取。`map` 向上游 `filter` 请求一个通过过滤的原始元素；`filter` 从 `raw` 的迭代器读取第一项 `" hp "`，调用 `keep()`：

   - 打印 `keep(' hp ')`；
   - 条件为真；
   - `filter` 产出原始字符串 `" hp "`。

   `map` 获取到它后调用 `normalize()`：

   - 打印 `normalize(' hp ')`；
   - 产出 `"HP"`。

   所以第一次 `next()` 为得到一个结果，只读取了 **1 个源元素**。若开头元素不通过，`filter` 会继续读取更多源元素，直到找到一个通过项或上游耗尽。

3. `filter()` 产出的是通过谓词测试的**原始元素**，不是 `keep()` 返回的布尔值；`map()` 把这些通过测试的源元素转换为 `normalize()` 的返回值并产出。

4. 第一次 `list(pipeline)` 从管道当前状态继续：

   - 空白项进入 `keep()`，但被过滤，不调用 `normalize()`；
   - `" mp "` 通过并规范化为 `"MP"`；
   - 因此只收集剩余结果 `["MP"]`，而不会重新得到 `"HP"`。

5. 到此 `pipeline` 已耗尽。第二次 `list(pipeline)` 返回 `[]`。管道对象本身仍存在，但其内部消费链位于终点。

6. 源列表 `raw` 没有被修改。被推进的是临时列表迭代器、`filter` 和 `map` 的状态，最后仍打印原列表。

验证后修正：

运行输出与预测一致，无需修正。

### D2. `any()` 的短路与生成器剩余状态（9 分）

预测完整输出顺序：

```python
records = [
    {"key": "ui.hp", "target": "Health"},
    {"key": "ui.mp", "target": "Mana"},
    {"key": "ui.sp", "target": "   "},
    {"key": "ui.ok", "target": "OK"},
]


def is_missing(record):
    print(f"check({record['key']})")
    return not record["target"].strip()


checks = (is_missing(record) for record in records)

print(any(checks))
print(list(checks))
print(any(checks))
```

要求至少说明：

1. 第一个 `any()` 在哪条记录处短路；
2. 返回后 `checks` 是否耗尽；
3. `list(checks)` 为什么收集布尔值而不是原始记录；
4. 最后一次 `any(checks)` 为什么得到对应结果；
5. 若先改成列表推导式再交给 `any()`，上游函数调用次数有何变化。

答题区：

验证前预测：

完整输出顺序为：

```tex
check(ui.hp)
check(ui.mp)
check(ui.sp)
True
check(ui.ok)
[False]
False
```

执行过程：

1. `checks` 是生成器表达式，创建时没有调用 `is_missing()`。

2. 第一个 `any(checks)` 逐项索取布尔值：
   - `ui.hp`：打印 `check(ui.hp)`，target 非空，产出 `False`；
   - `ui.mp`：打印 `check(ui.mp)`，target 非空，产出 `False`；
   - `ui.sp`：打印 `check(ui.sp)`，纯空白清理后为空，产出 `True`；
   - `any()` 遇到第一个真值，立即返回 `True`，不会在此时检查 `ui.ok`。

3. 返回后 `checks` **尚未耗尽**。前三条记录已消费，第四条记录仍未请求。

4. `list(checks)` 继续消费生成器。生成器调用 `is_missing(ui.ok)`，打印 `check(ui.ok)`，函数返回 `False`。生成器表达式产出的元素就是这些布尔结果，不是原始 record，因此列表为 `[False]`。为确认结束，`list()` 再次索取，但底层记录迭代器确实已被耗尽。

5. 最后一条 `any(checks)` 面对已耗尽生成器，没有任何元素可检查，这意味着没有任何“为真”的元素，因此返回 `False`，也不再打印 `check(...)`。

若先改成列表推导式：

```python
checks = [is_missing(record) for record in records]
print(any(checks))
```

因为列表构造是急切的，所以四条记录都会在调用 `any()` 之前执行 `is_missing()`。`any()` 虽然仍会在布尔列表中短路，但已经无法节省上游函数调用：`check(ui.ok)` 也必然提前发生。

验证后修正：

运行输出与预测完全一致，无需修正。

---

## E. 对齐、物化与多消费者风险（14 分）

### E1. `zip(strict=True)` 只能检查长度，不能修复语义错位（8 分）

预测 `bad` 和 `good`，并解释差异：

```python
keys = ["ui.hp", "", "ui.mp"]
texts = ["Health", "Mana", ""]

bad = list(zip(
    (key for key in keys if key),
    (text for text in texts if text),
    strict=True,
))

good = [
    (key, text)
    for key, text in zip(keys, texts, strict=True)
    if key and text
]

print(bad)
print(good)
```

要求至少说明：

1. 为什么独立过滤两列会破坏原始行身份；
2. 为什么 `strict=True` 没有发现 `bad` 的语义错误；
3. “先配对，再过滤整条记录”保留了什么契约；
4. `zip(strict=True)` 遇到真实长度不一致时何时抛错，以及为什么它不提供回滚；
5. `keys` 和 `texts` 两个列表是否被修改或耗尽。

答题区：

验证前预测：

输出为：

```tex
[('ui.hp', 'Health'), ('ui.mp', 'Mana')]
[('ui.hp', 'Health')]
```

`bad` 的构造过程：

```python
(key for key in keys if key)
```

独立删除空 key，产出：

```python
"ui.hp", "ui.mp"
```

而：

```python
(text for text in texts if text)
```

独立删除空 text，产出：

```python
"Health", "Mana"
```

随后 `zip(..., strict=True)` 只检查到两列各有两个元素，因此认为长度对齐，产出：

```python
("ui.hp", "Health")
("ui.mp", "Mana")
```

第二个元组在语义上是错位的：原始 `"ui.mp"` 来自第三行，而 `"Mana"` 来自第二行。独立过滤列之后，元素已经失去原始行身份；而 `strict=True` 只能检查两个**过滤后迭代器的长度是否一致**，不能推断元素原来是否来自同一记录。

`good` 先执行：

```python
zip(keys, texts, strict=True)
```

保留原始位置关系：

```python
("ui.hp", "Health")
("", "Mana")
("ui.mp", "")
```

再以 `if key and text` 过滤整条配对记录，因此只有第一条保留。这维持了“同一输出元组中的 key 和 text 必须来自同一原始行”的契约。

若输入真实长度不一致，`zip(strict=True)` 是惰性的：在消费过程中可以先产出若干完整元组，直到某个参数先耗尽、检查到另一个参数仍有元素时才抛出 `ValueError`。它不提供事务或回滚：此前的元素可能已经被上游迭代器取走、回调可能已经执行、调用方也可能已经处理过先前元组。若由 `list(zip(..., strict=True))` 构造列表，异常会使新列表的构造无法完成，但底层迭代器已发生的推进不会自动撤销。

`keys` 和 `texts` 是列表。两次计算只通过各自创建的迭代器读取它们，没有修改列表内容；此外，也不能说列表被耗尽。耗尽的是生成器表达式创建的生成器和 `zip` 的临时迭代器链。

验证后修正：

运行结果与预测一致，无需修正。

### E2. 一个上游生成器被两个下游共享（6 分）

预测输出并修复设计：

```python
records = [
    {"key": "ui.hp", "target": "Health", "enabled": True},
    {"key": "ui.debug", "target": "Debug", "enabled": False},
    {"key": "ui.mp", "target": "Mana", "enabled": True},
]

active = (record for record in records if record["enabled"])
keys = (record["key"] for record in active)
targets = (record["target"] for record in active)

print(list(keys))
print(list(targets))
print(records)
```

要求至少说明：

1. `keys` 和 `targets` 是否拥有独立的上游数据；
2. 为什么先消费 `keys` 会影响 `targets`；
3. 为什么源列表仍然完整；
4. 给出两种清晰修复方案，并比较“先物化 active 记录”与“分别重建管道”的适用条件。

不要求使用 `tee()`。

答题区：

验证前预测：

输出为：

```tex
['ui.hp', 'ui.mp']
[]
[{'key': 'ui.hp', 'target': 'Health', 'enabled': True}, {'key': 'ui.debug', 'target': 'Debug', 'enabled': False}, {'key': 'ui.mp', 'target': 'Mana', 'enabled': True}]
```

首先，`active` 是一个生成器对象。`keys` 和 `targets` 虽然是两个不同的下游生成器，但它们都从**同一个 `active` 对象**取记录，并没有独立上游。

先执行 `list(keys)` 时：

- `keys` 持续向 `active` 请求记录；
- `active` 扫描全部 `records`，过滤掉禁用记录；
- `keys` 依次产出 `"ui.hp"` 和 `"ui.mp"`；
- 为确认结束，`active` 最终被完整耗尽。

随后 `list(targets)` 再向同一个 `active` 请求记录，只能立即遇到 `StopIteration`，因此为空。

源列表 `records` 仍然完整，因为生成器消费只推进遍历位置，没有删除或修改列表中的字典。

修复方案：

### 方案一：先物化启用记录

```python
active_records = [
    record
    for record in records
    if record["enabled"]
]

keys = [
    record["key"]
    for record in active_records
]

targets = [
    record["target"]
    for record in active_records
]

print(keys)
print(targets)
```

结果分别为：

```python
["ui.hp", "ui.mp"]
["Health", "Mana"]
```

适用条件：

- 后续有多个消费者；
- 数据量可接受；
- 需要重复遍历、长度、索引、调试或稳定快照；
- 希望启用过滤只执行一次。

代价是把所有启用记录保存在内存中。

### 方案二：从可重复遍历的源分别重建管道

```python
keys = (
    record["key"]
    for record in records
    if record["enabled"]
)

targets = (
    record["target"]
    for record in records
    if record["enabled"]
)

print(list(keys))
print(list(targets))
```

这里两个生成器分别从列表 `records` 创建自己的迭代器，所以拥有独立上游。

适用条件：

- `records` 已知是列表、元组等可重复遍历对象；
- 重复扫描成本低；
- 不希望物化中间 active 列表。

代价是启用判断执行两遍；若 `records` 是文件、生成器或共享游标，这个方案不成立，第二条管道可能没有数据。

### 方案三：使用 `itertools.tee()` 分叉一次性上游

```python
from itertools import tee

active = (
    record
    for record in records
    if record["enabled"]
)

active_for_keys, active_for_targets = tee(active, 2)

keys = (
    record["key"]
    for record in active_for_keys
)

targets = (
    record["target"]
    for record in active_for_targets
)

print(list(keys))
print(list(targets))
```

`tee(active, 2)` 返回两个逻辑上独立的迭代器。一个分支领先时，`tee` 会缓存尚未被另一分支读取的上游元素，因此两边都能看到相同的 active 记录。

`tee()` 的工程边界：

- 它不会重新执行上游过滤；
- 适合两个分支大致同步消费，或不能重新建立上游而又不想立即完整物化的情况；
- 若一个分支远远领先，缓存可能增长到很大；
- 若一个分支会先完整消费、另一个很久以后才开始，直接 `list()` 往往更清楚；
- 同一 `tee()` 产生的迭代器不应用于并发线程中的无保护同时消费。

验证后修正：

原代码运行结果与预测一致。三种修复方案均能得到完整 keys 和 targets；实际选择取决于上游是否可重复、数据规模、重复计算成本及两个消费者的消费节奏。

---

## F. 工程综合题：本地化资源迭代审计（15 分）

### F1. 设计一个可审计的扫描函数（15 分）

请实现或写出接近真实 Python 的清晰伪代码：

```python
def audit_localization(records, required_placeholders):
    ...
```

输入契约：

1. `records` 是任意 iterable，可能是一次性生成器；每个元素预期为字典。
2. `required_placeholders` 形如 `{"mail.reward": ["{count}"]}`。

返回报告至少包含：

```python
{
    "completed": True,
    "stats": {
        "read": 0,
        "disabled": 0,
        "enabled": 0,
        "valid": 0,
    },
    "issues": [],
    "fatal_error": None,
    "valid_by_key": {},
    "valid_items": [],
}
```

扫描规则：

1. 使用 `enumerate(records, start=1)` 保留原始输入位置；每取得一条记录就增加 `read`。
2. 元素不是字典，或缺少 `key`，属于阻断错误：设置 `completed=False` 和 `fatal_error`，然后停止扫描。
3. `enabled` 默认为 `True`；禁用记录计入 `disabled` 后跳过其余检查。
4. 启用记录计入 `enabled`；key 使用 `strip().lower()` 规范化，target 使用 `strip()` 清洗。
5. 空 target 是普通 issue，记录 `line_no`、规范化 key 和 kind，然后继续下一条。
6. 重复的规范化 key 是普通 issue；保留第一次成功写入的值，不允许静默覆盖。
7. 检查 `required_placeholders` 中要求的字符串；缺失项使用 `sorted(...)` 形成稳定列表，并记录为普通 issue。
8. 通过检查后，把新建的干净结果写入 `valid_by_key`，不要修改或直接复用输入字典。
9. 扫描结束后令 `valid_items = sorted(valid_by_key.items())`，以提供稳定报告视图。
10. 核心函数不 `print()`，只返回结构化报告。

除代码外，请解释：

1. 为什么完整扫描应保留显式 `for`，而不应压成一个字典推导式；
2. 哪个已经结构化、无复杂副作用的后处理步骤可以安全使用推导式或 `sorted()`；
3. 若 `records` 是生成器，函数返回后它通常处于什么状态；若发生阻断错误，未读取尾部又处于什么状态；
4. 统计语句的位置如何决定 `read`、`enabled` 和 `valid` 的统计口径。

答题区：

```python
# 在这里写代码或清晰伪代码

def audit_localization(records, required_placeholders):
    stats = {
        "read": 0,
        "disabled": 0,
        "enabled": 0,
        "valid": 0,
    }

    issues = []
    valid_by_key = {}

    completed = True
    fatal_error = None

    for line_no, record in enumerate(records, start=1):
        # 只要 enumerate 已从上游取得一个元素，就计入 read。
        stats["read"] += 1

        if not isinstance(record, dict):
            completed = False
            fatal_error = {
                "line_no": line_no,
                "kind": "record_not_mapping",
                "message": "record must be a dict",
                "record_type": type(record).__qualname__,
            }
            break

        if "key" not in record:
            completed = False
            fatal_error = {
                "line_no": line_no,
                "kind": "missing_key_field",
                "message": "record is missing required field 'key'",
            }
            break

        # enabled 是可选控制字段，缺省为 True。
        if not record.get("enabled", True):
            stats["disabled"] += 1
            continue

        # 只有通过禁用判断的记录才计入 enabled。
        stats["enabled"] += 1

        key = str(record["key"]).strip().lower()

        raw_target = record.get("target", "")
        target = (
            ""
            if raw_target is None
            else str(raw_target).strip()
        )

        if not target:
            issues.append({
                "line_no": line_no,
                "key": key,
                "kind": "empty_target",
            })
            continue

        # 只与此前“成功写入”的 key 比较。
        if key in valid_by_key:
            issues.append({
                "line_no": line_no,
                "key": key,
                "kind": "duplicate_key",
            })
            continue

        required = required_placeholders.get(key, ())

        missing_placeholders = sorted(
            placeholder
            for placeholder in required
            if placeholder not in target
        )

        if missing_placeholders:
            issues.append({
                "line_no": line_no,
                "key": key,
                "kind": "missing_placeholders",
                "missing": missing_placeholders,
            })
            continue

        # 创建新的干净结果，不修改、也不直接复用输入字典。
        clean_record = {
            "key": key,
            "target": target,
        }

        valid_by_key[key] = clean_record
        stats["valid"] += 1

    valid_items = sorted(valid_by_key.items())

    return {
        "completed": completed,
        "stats": stats,
        "issues": issues,
        "fatal_error": fatal_error,
        "valid_by_key": valid_by_key,
        "valid_items": valid_items,
    }
```

设计说明：

### 1. 为什么核心扫描保留显式 `for`

核心循环同时承担：

- 对任意 iterable 的单次消费；
- 原始输入位置记录；
- `read`、`disabled`、`enabled`、`valid` 四种统计；
- 阻断错误与普通 issue 的分流；
- `break` 和多个 `continue`；
- 重复 key 的“第一次成功写入保留”状态；
- 原始记录到干净结果的构造。

这些行为包含多步状态迁移和失败路径。若压成一个字典推导式，非字典、缺 key、禁用、空 target、重复、占位符缺失和成功写入会被隐藏在复杂表达式或外部副作用中；重复 key 还可能被字典构造静默覆盖。显式循环使每一类记录何时计数、为何停止或跳过都可直接审计。

### 2. 哪些后处理适合推导式或 `sorted()`

已经结构化且无复杂副作用的步骤适合紧凑表达：

```python
missing_placeholders = sorted(
    placeholder
    for placeholder in required
    if placeholder not in target
)
```

这里生成器表达式只做过滤，`sorted()` 负责完整消费并返回稳定列表。

扫描完成后：

```python
valid_items = sorted(valid_by_key.items())
```

也很合适，因为数据已经完成验证和写入，此步骤仅建立按 key 排序的稳定报告视图，不参与错误控制或统计副作用。

### 3. `records` 的消费状态

若 `records` 是生成器：

- 正常完整扫描后，它通常已耗尽；
- 普通 issue 只执行 `continue`，因此不会阻止后续扫描，最终仍会耗尽；
- 遇到非字典或缺少 `key` 的阻断错误时，当前坏元素已经由 `enumerate` 取出并计入 `read`，随后 `break`；生成器中尚未读取的尾部仍保留在其当前状态之后。
- 如果调用者仍持有该生成器引用，可以从未读取尾部继续消费；已经读取的前缀不会回来。

若 `records` 是列表，列表内容不被耗尽或修改；耗尽的是循环内部创建的迭代器。

### 4. 统计语句的位置决定口径

```python
stats["read"] += 1
```

位于取得每个元素后的最前面，因此任何已从上游取出的元素——包括非字典和缺 key 的阻断记录——都计入 `read`。

```python
stats["disabled"] += 1
```

只在 `enabled` 明确为假后执行。禁用记录立即 `continue`，不进入 target、重复或占位符检查。

```python
stats["enabled"] += 1
```

位于禁用分支之后，因此表示进入业务校验流程的记录数；空 target、重复 key 和缺占位符记录都属于 enabled，但不属于 valid。

```python
stats["valid"] += 1
```

只在所有检查通过、干净结果成功写入 `valid_by_key` 后执行。因此它统计的是成功结果数量，而不是仅仅“没有被禁用”的数量。

由于阻断记录在检查 `enabled` 之前停止，发生 fatal error 时不必满足：

```python
read == disabled + enabled
```

但在没有 fatal error、并且每个元素都是含 key 的字典时，应满足：

```python
read == disabled + enabled
valid <= enabled
```

### 5. 重复 key 的精确口径

重复检测基于 `valid_by_key`，因此“重复”表示：

> 当前规范化 key 已经有一个此前通过全部检查并成功写入的结果。

若某 key 的第一次出现因为空 target 或缺占位符而失败，没有写入 `valid_by_key`；后续同 key 的有效记录仍有机会成为第一次成功写入。这符合“保留第一次成功写入的值”的题目契约，而不是机械地保留第一次原始出现。

### 6. 其他边界说明

- 本实现把缺失 `target` 或显式 `target is None` 规范化为空 target，作为普通 issue；这是对题目“空 target 继续扫描”的具体解释。
- `required_placeholders` 的 key 按输入契约直接查询，调用方应使用与规范化 key 一致的形式。
- 核心函数没有 `print()`；调用方可以按 CLI、JSON、测试或日志需求自行呈现报告。
- `issues` 保留扫描顺序和原始 `line_no`；其中占位符缺失列表显式排序。`valid_items` 另行排序，提供稳定成功结果视图。

---

## 作答后提交说明

请直接在每题的“答题区”中作答。你可以保留“验证前预测”和“验证后修正”两段，也可以只写完整推理；如果运行过代码，请标明哪些结论来自验证。

提交后我会按阶段测验批改方式进行逐题审批：保留原答案，在本文件末尾追加 `## Codex 批改记录（逐题审批，YYYY-MM-DD）`，给出建议得分、主要强项、需要精修的边界、是否通过 C14，以及可同步到学习画像与阶段笔记的更新。

---

## Codex 批改记录（逐题审批，2026-07-16）

### 总体审批结论

建议得分：`99 / 100`。

`C14_Iterations_and_Comprehensions` 阶段测验通过。全部输出预测均正确，协议角色、消费位置、急切/惰性求值、推导式执行顺序、短路后的剩余状态、`zip(strict=True)` 的语义边界和综合扫描函数的主干设计也都正确。两处扣分均属于术语和状态描述的轻微精度问题，不是主线概念缺口。

代码验证结果：批改前答卷中的 `43` 个 Python 代码块均通过语法编译；`B1`、`B2`、`C1`、`C2`、`C3`、`D1`、`D2`、`E1`、`E2` 共 `9` 组预测代码的实际输出与答案逐行一致；F1 综合函数通过了正常扫描、禁用记录、空译文、重复 key、占位符缺失和阻断错误后保留生成器尾部等代表性运行验证。

### 审查发现与纠偏

#### 1. C1：显式循环只在数据流上等价，改名并不会获得推导式作用域（扣 0.5 分）

原答案已经正确指出：若普通循环继续使用 `text`，循环结束后外层 `text` 会变成最后一项。需要再收紧的是这句：

> 为了保留与原程序相同的外部绑定效果，可使用不同的循环变量名。

改用 `candidate` 的确保住了原有的 `text == "OUTER"`，但普通 `for` 不会创建块级作用域，所以循环结束后 `candidate` 仍会存在于当前作用域；若此前已有同名 `candidate`，它也会被覆盖。因而更准确的结论是：

- 该显式循环与推导式保持相同的遍历、过滤、转换、调用顺序和 `result`；
- 它保留了题目所观察的外层 `text` 绑定；
- 它仍会新增或重绑定 `candidate`，所以与推导式的完整名字环境并不等价。

若确实要求循环目标也不泄漏，应把显式循环放入单独函数等真实作用域，而不是仅仅更换变量名。

#### 2. F1：阻断性 `break` 后，临时列表迭代器可能只是部分消费（扣 0.5 分）

原答案对生成器的正常耗尽和阻断后保留尾部解释正确，但随后写道：

> 若 `records` 是列表，列表内容不被耗尽或修改；耗尽的是循环内部创建的迭代器。

这句话只适用于**正常完整扫描**。若列表扫描在中途遇到 fatal error 并执行 `break`：

- 列表本身仍完整、可再次遍历；
- `for` 内部创建的列表迭代器只消费到阻断记录，尚未耗尽；
- 因为该临时迭代器没有被外部保存，函数返回后通常只是被丢弃，而不是被继续使用。

因此必须区分“已经耗尽”和“尚有尾部但迭代器不再可达”。如果调用方显式传入并保留的是 `iter(records)`，那么阻断后也可像生成器一样从未读取尾部继续消费。

#### 3. F1：输入类型转换策略需要显式成约（不扣分）

实现使用了：

```python
key = str(record["key"]).strip().lower()
target = "" if raw_target is None else str(raw_target).strip()
```

本卷没有要求把“key/target 值不是字符串”升级为 fatal error，因此这一实现可以接受。但 `str(...)` 会静默接纳 `None`、整数或自定义对象；在真实审计器中，这属于业务策略，不应无声决定。更稳妥的工程选择是二选一并写入契约：严格验证字符串类型并报告问题，或明确允许字符串化并说明可能的信息损失。

#### 4. F1：稳定排序视图不等于深层不可变快照（不扣分）

`valid_items = sorted(valid_by_key.items())` 正确满足题目要求。这里的“稳定”主要指创建时的 key 排序稳定；新列表中的 value 仍是 `valid_by_key` 里同一个 `clean_record` 字典对象。后续若原地修改该字典，两处都能观察到变化。若报告需要不可变或隔离快照，还要额外复制或转换 value。

#### 5. F1：重复 key 的口径已明确，业务变化时要换状态模型（不扣分）

答案把 duplicate 定义为“此前已有一次成功写入”，与题目中的“保留第一次成功写入的值”相容，因此本卷接受。若真实需求改为“同一规范化 key 只要在原始输入中第二次出现就报告重复”，则还需要独立的 `seen_keys`；不能只检查 `valid_by_key`，否则第一次无效、第二次有效的同 key 不会被标记为重复。

### 逐题审批

| 题目 | 得分 | 审批意见 |
| --- | ---: | --- |
| A1 | 8 / 8 | 正确。八条说法均判断准确；尤其能区分 iterable/iterator、真实 `None`/`StopIteration`、推导式名字隔离/对象副作用，以及生成器真值/剩余元素检测。对最左侧 iterable 表达式即时求值和自定义对象非典型协议行为的限定也到位。 |
| A2 | 7 / 7 | 正确。七类对象的协议角色、`iter(obj) is obj`、重复 `list()` 的结果和 `StringIO.seek(0)` 的 API 层级全部准确。没有把可定位流的额外能力误推广成通用迭代器重置协议。 |
| B1 | 9 / 9 | 正确。八行输出、两个列表迭代器的独立消费位置、真实 `None`、`list(a)` 从当前位置收集，以及列表不应称为“耗尽”都解释完整。 |
| B2 | 9 / 9 | 正确。`next()`、`readline()`、`list(stream)` 共享流位置，两种 EOF 契约和 `seek(0)` 的定位效果均准确；也正确区分了向前消费模型与具体流 API。 |
| C1 | 7.5 / 8 | 输出、过滤先于转换、急切求值和推导式循环变量不泄漏均正确。小扣分仅针对“改用不同变量名即可保持相同外部绑定效果”的表述：`candidate` 仍会留在普通循环所在作用域。 |
| C2 | 6 / 6 | 正确。空白记录过滤、规范化碰撞、最后值覆盖但不移动首次插入位置、集合/字典排序报告，以及重复 key 需要显式审计的工程结论都准确。 |
| C3 | 6 / 6 | 正确。多层 `for`/`if` 的左到右嵌套顺序、外层过滤阻止内层访问、推导式变量隔离和退回显式循环的判断标准都完整。 |
| D1 | 9 / 9 | 正确。创建管道时函数调用次数为零，第一次 `next()` 的按需索取链、`filter` 产出原元素、`map` 产出转换值，以及两次 `list()` 后的状态都解释到位。 |
| D2 | 9 / 9 | 正确。`any()` 在第三条记录处短路，生成器仍保留第四条，随后 `list()` 收集布尔值，最终空迭代的 `any()` 返回 `False`；与列表推导式的上游调用差异也准确。 |
| E1 | 8 / 8 | 正确。独立过滤两列破坏原始行身份、`strict=True` 只检查消费后的长度对齐、先配对再按整行过滤的契约，以及惰性报错和非事务性推进都说明清楚。 |
| E2 | 6 / 6 | 正确。两个下游共享同一个 `active`，先消费 keys 会耗尽共享上游；物化和重建管道两种必答修复均正确，附加的 `tee()` 方案也准确说明了缓存与步调差边界。 |
| F1 | 14.5 / 15 | 主体实现正确且可运行：统计位置、fatal/issue 分流、禁用短路、规范化、重复保护、占位符稳定排序、干净结果和统一结构化返回都满足契约。小扣分仅针对把 fatal `break` 后的临时列表迭代器也笼统描述为“耗尽”。 |

分项汇总：

| 部分 | 得分 |
| --- | ---: |
| A. 概念边界 | 15 / 15 |
| B. 协议与流位置 | 18 / 18 |
| C. 推导式 | 19.5 / 20 |
| D. 惰性管道与短路 | 18 / 18 |
| E. 对齐、物化与多消费者 | 14 / 14 |
| F. 工程综合题 | 14.5 / 15 |
| **总分** | **99 / 100** |

### 学习画像更新

稳定强项：

- 已能从协议层稳定解释 iterable、iterator、`iter()`、`next()`、`StopIteration` 和 `for` 的协作，而不是只记住表面输出。
- 能精确追踪独立游标、共享上游、文件位置、惰性触发、短路停止、剩余状态和再次消费结果。
- 能稳定区分列表推导式的急切构造、生成器表达式与 `map`/`filter` 的惰性求值，并说明具体由哪次消费者索取触发。
- 能解释推导式隔离的是循环目标名字绑定，不隔离外部可变对象、副作用或底层数据来源。
- 能把 set/dict 推导式、排序、碰撞保护、`zip(strict=True)` 和物化边界迁移到本地化资源报告中。
- 已能独立设计一次扫描任意 iterable 的结构化审计函数，并把统计口径、普通 issue、阻断错误、稳定结果和输入对象保护组织清楚。

仍需精修：

- 说明“等价改写”时要标明等价维度：输出和调用顺序等价，不代表名字作用域、异常路径、对象身份或副作用完全等价。
- 严格区分“已耗尽”“部分消费后停止”“尾部仍在但迭代器已不可达”和“源容器仍可重新提供新迭代器”。
- 在真实工程函数中，把输入类型验证与 `str(...)` 静默转换明确为契约，而不是让实现细节代替业务决定。
- 把“排序稳定视图”与“深层隔离快照”分开；新外层列表不意味着内部可变 value 已复制。

新的能力判断：

你已经稳定通过 P3 的 C10-C14。当前可判断为：**中级入门前段已经建立，能够独立分析并设计小型迭代数据管道，但仍需在完整语言覆盖和工程契约表达上继续积累**。这次答卷已经证明，C14 的知识进入了你原有的对象模型、控制流模型和本地化审计设计，而不是停留在推导式语法记忆上。

下一阶段关注点：

- C15 应重点训练如何借助 `help()`、`dir()`、文档字符串和官方文档验证 API 契约，同时继续区分“工具输出”“函数返回值”“对象元数据”和“当前解释器的实际行为”。
- 阅读文档时继续保留本阶段的验证习惯：先形成可检验假设，再用最小代码确认版本、对象类型、协议行为和边界条件。

### 本阶段末评语与能力判断

这是一份主干近乎全对、而且推理链完整的答卷。你不仅给出了正确结果，还能说明是谁取得迭代器、谁推进消费位置、过滤为何可能读取多个源元素、短路为何留下尾部、物化为何改变重复消费能力，以及为什么复杂审计不应为了简短而压进推导式。F1 尤其说明你已经能把迭代协议落实为可审计的工程控制流。

本次暴露的两点都很“后半程”：不是不会写，而是需要继续约束术语覆盖范围。普通循环换名后仍有名字残留；中途 `break` 的迭代器也不等于耗尽。能够把这些状态继续说准，你的解释就会从“结论可靠”进一步走向“契约可靠”。

审批结论：**C14 阶段测验通过，可以进入本小阶段的收束记录同步；在阶段笔记、相关长期文档职责复核和 C15 新会话启动模板完成前，不把整个 C14 收束流程误写成已经全部结束。**
