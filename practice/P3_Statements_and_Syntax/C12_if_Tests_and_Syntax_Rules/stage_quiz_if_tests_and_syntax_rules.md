# Stage Quiz: if Tests and Syntax Rules

本测验用于当前小阶段：**条件判断、真值测试与语法规则：短路求值、比较链和控制流选择**。

它不只考 `if` 的写法，而是考你是否能把 C10/C11 已经稳定掌握的“表达式求值 vs 语句执行”“对象本体 vs 显示形式”“名字绑定 vs 对象修改”模型，继续压到 C12 的条件控制流里：条件表达式先如何求值，`if` 如何对结果做真值测试，`and` / `or` 如何短路并返回操作数对象，比较链如何避免重复求值，`if / elif / else` 如何选择代码块，以及 `match` 在结构化分派中的适用边界。

总分：100 分。

答题规则：

1. 第一遍不要运行代码，先写预测、求值顺序、返回对象、分支选择、副作用是否发生和理由。
2. 第二遍可以用当前日常学习环境 Python `3.14.5` 验证，并标注“验证前预测”和“验证后修正”。
3. 每道代码题尽量按这条链解释：表达式是否求值、对象通过什么规则参与真值测试、`and` / `or` 返回哪个操作数、`not` / 比较 / 成员测试返回什么、控制流进入哪个代码块、副作用是否发生。
4. 本卷不包含参考答案。你作答后交给我审批，我会保留你的原答案并追加批改记录。
5. 若你认为题目本身有歧义，可以直接指出；这也属于本阶段能力的一部分。

---

## A. 概念边界：条件、真值测试、短路与控制流（15 分）

### A1. `if x` 是否等于 `x == True`（5 分）

逐条判断下面说法是否准确；若不准确，请改写成更精确的说法。

```tex
1. if x: 的意思就是 if x == True:。
2. bool(x) 得到的布尔对象和 x 本身是同一个对象。
3. 非空列表一定为真，即使它里面装的是假值元素。
4. 自定义对象如果没有 __bool__ 和 __len__，默认在真值测试中为真。
5. 条件表达式 x if cond else y 是一种语句，因为它也包含 if。
```

要求至少说明：

1. 对象本体、真值测试结果、相等性比较三者的区别；
2. 容器真值测试是否递归检查内部所有元素；
3. 条件表达式和 `if` 语句的职责边界。

答题区：

```tex
验证前预测：

1. 不准确。更精确的说法是：
if x: 的意思不是 if x == True:，而是对对象 x 做真值测试。if x 关心的是 bool(x) 的真值结果；而 x == True 关心的是 x 与 True 的“值”相等性比较结果。也就是说，二者语义不同。
例如：
x = []
bool(x)      -> False
x == True    -> False

x = [1]
bool(x)      -> True
x == True    -> False
综上，不难判断出，if x: 不能理解成 if x == True:。
2. 不准确。更精确的说法是：
bool(x) 得到的是布尔对象 True 或 False，它和 x 本身通常不是同一个对象。x 是原始对象，例如列表、字符串、字典、自定义对象等；而 bool(x) 是对 x 做真值测试后产生的布尔结果。
例如：
x = ["issue"]
x 本身是 list 对象；
bool(x) 则是 bool 对象 True。

对象本体、真值测试结果、相等性比较三者的不同：
- 对象本体：x 实际引用的对象，例如 []、[""]、"0"、某个自定义实例；
- 真值测试结果：bool(x) 得到的 True 或 False；
- 相等性比较：x == True 或 x == False 的比较结果。

所以说，只有当 x 本身已经是 True 或 False 时，bool(x) 才会返回对应的布尔单例对象；但这不能推广成“bool(x) 和 x 总是同一个对象”。
3. 准确。对于内置列表来说，非空列表在真值测试中为真，即使它内部装的是假值元素。容器真值测试看的是容器本身是否为空，不会递归检查内部所有元素的真假。比如 [""] 中的 "" 本身是假值，但列表 [""] 有一个元素，所以列表本身是真值。
4. 准确。普通自定义对象如果既没有定义 __bool__()，也没有定义 __len__()，那么默认在真值测试中为真。除非类通过 __bool__() 返回 False，或者在没有 __bool__() 时通过 __len__() 返回 0。
5. 不准确。更精确的说法是：
条件表达式 x if cond else y 是表达式，不是语句。不是因为源码中含有 if 就代表一定是一条 if 语句！条件表达式会产生一个值，且可以出现在赋值右侧、函数实参、return 后面等表达式位置。例如：status = "ok" if passed else "failed"。而 if 语句是控制流语句，用来选择执行哪个代码块，例如：
if passed:
    status = "ok"
else:
    status = "failed"

条件表达式和 if 语句的职责边界：
- 条件表达式：适合简单二选一地产生值；
- if 语句：适合组织代码块、处理多步骤逻辑和副作用。

验证后修正：

无须修正。
```

### A2. `and` / `or` / `not` 的返回值边界（5 分）

解释下面四个表达式分别返回什么类型的对象，并指出哪些表达式保证返回 `bool`。

```python
[] or "fallback"
["issue"] and "abort"
not []
not ["issue"]
```

要求至少说明：

1. `and` / `or` 为什么不是统一返回 `True` 或 `False`；
2. `not` 为什么一定返回布尔对象；
3. 如果这些表达式放进 `if` 条件位置，`if` 会进一步做什么。

答题区：

```tex
验证前预测：

1. [] or "fallback"
首先注意到：[] 是空列表，其真值为 False。而 or 的规则是：“左侧为真则返回左侧操作数；左侧为假则返回右侧操作数。”，所以：[] or "fallback" 显然返回 "fallback"！即第一个表达式返回的是字符串类型的对象，并且不保证返回 bool。
2. ["issue"] and "abort"
首先注意到：["issue"] 是非空列表，其真值为 True。而 and 的规则是：“左侧为假则返回左侧操作数；左侧为真则返回右侧操作数。”，所以：["issue"] and "abort" 显然返回 "abort"！即第二个表达式返回的是字符串类型对象，也不保证返回 bool。
3. not []
在这里，[] 是空列表，其真值为 False。而 not 会先对操作数做真值测试，再返回相反的布尔对象。所以：not [] 返回 True！即第三个表达式返回的是布尔类型对象，并且保证能返回 bool。
4. not ["issue"]
在这里，["issue"] 是非空列表，其真值为 True，在 not 取反后返回 False。所以有：not ["issue"] 返回 False！即第四个表达式返回的是布尔类型的对象，并且也保证返回 bool。

综上，总结：
and / or 不是统一返回 True 或 False。它们用（左侧操作数对象的）真值测试结果来决定短路路径，但最终返回某个操作数对象本身。

not 一定返回 bool。这是因为 not 的语义就是“对真值结果取反”，最终结果只能是 True 或 False。

如果这些表达式放进 if 条件位置，if 会对整个表达式的结果再做真值测试。
例如：
if [] or "fallback":
    ...
在这里，[] or "fallback" 按前面的分析会先返回字符串 "fallback"；然后 if 又对 "fallback" 做真值测试；因为非空字符串为真，所以控制流会进入 if 的代码块。

验证后修正：

无须修正。
```

### A3. `if / elif / else`、多个独立 `if` 与 `match`（5 分）

回答下面问题：

```tex
1. if / elif / else 链最多执行几个代码块？后续 elif 条件一定会求值吗？
2. 多个独立 if 和 if / elif / else 的主要差异是什么？
3. pass 与注释在空代码块中有什么区别？
4. match / case 是不是 C / Java 风格 switch？是否自动 fall-through？
5. case {"key": key} 中右侧的 key 通常是在比较已有变量，还是捕获绑定？
```

答题区：

```tex
验证前预测：

1. if / elif / else 链最多执行一个代码块。Python 会从上到下求值条件，遇到第一个真值条件后，执行对应代码块，然后整个 if 语句结束。后续 elif 条件不一定会求值；如果前面的 if 或某个 elif 已经命中，后续 elif 条件不会再求值。
2. 多个独立 if 和 if / elif / else 的主要差异是：
- 多个独立 if：每个 if 都会单独检查，可能有多个代码块执行；
- if / elif / else：互斥分支链，最多只有一个代码块执行。

多个独立 if 适合“收集所有满足条件的问题”。而 if / elif / else 适合“选择一个最终动作或一个最终分类”。
3. pass 与注释在空代码块中的区别：
pass 是一条真正的 Python 语句，表示什么也不做，但能合法占据代码块位置；
注释不是语句，解析时会被忽略，也不能充当代码块内容。
4. match / case 不是 C / Java 风格 switch。它是结构化模式匹配，不只是简单的值分派。而且 Python 的 match 也不会自动 fall-through；一个 case 命中并执行后，整个 match 语句结束，不会继续执行后续 case。
5. case {"key": key} 中右侧的 key 通常是捕获绑定，而不是在比较已有变量。意即，如果 subject 是一个 mapping，并且存在 "key" 这个键，就把 subject["key"] 的值绑定到名字 key。如果要比较已有变量，通常需要使用 guard，例如：

case {"key": value} if value == expected_key:
    ...

验证后修正：

无须修正。
```

---

## B. 真值协议：内置对象、自定义对象与错误边界（15 分）

预测完整输出，并解释每个对象通过什么规则参与真值测试。

```python
class LocalizedEntries:
    def __init__(self, entries):
        self.entries = entries

    def __len__(self):
        print("LocalizedEntries.__len__")
        return len(self.entries)


class StrictLocalizedEntries(LocalizedEntries):
    def __bool__(self):
        print("StrictLocalizedEntries.__bool__")
        return bool(self.entries) and all("text" in item for item in self.entries)


class BrokenFlag:
    def __bool__(self):
        print("BrokenFlag.__bool__")
        return 1


values = [
    [],
    [""],
    "",
    "0",
    None,
    LocalizedEntries([]),
    LocalizedEntries([{"key": "menu.start"}]),
    StrictLocalizedEntries([{"key": "menu.start"}]),
    StrictLocalizedEntries([{"key": "menu.start", "text": "Start"}]),
]

for value in values:
    print(type(value).__name__, bool(value))

try:
    print(bool(BrokenFlag()))
except Exception as exc:
    print(type(exc).__name__)
```

要求至少说明：

1. `LocalizedEntries` 为什么调用 `__len__()`；
2. `StrictLocalizedEntries` 为什么不会退回去调用继承来的 `__len__()`；
3. `[""]` 与 `""` 的真值为什么不同；
4. `BrokenFlag.__bool__()` 返回 `1` 为什么不是合法返回值。

答题区：

```tex
验证前预测：

完整输出为：
list False
list True
str False
str True
NoneType False
LocalizedEntries.__len__
LocalizedEntries False
LocalizedEntries.__len__
LocalizedEntries True
StrictLocalizedEntries.__bool__
StrictLocalizedEntries False
StrictLocalizedEntries.__bool__
StrictLocalizedEntries True
BrokenFlag.__bool__
TypeError

逐项解释：
1. []
value 是空列表。而空列表是典型的假值。所以有：
type(value).__name__ -> "list"
bool(value) -> False
输出：
list False
2. [""]
value 是非空列表，而非空列表是真值。虽然内部元素 "" 是假值，但列表本身因为有一个元素所以不为空。列表真值测试看的是列表是否为空，不递归检查内部所有元素的真假。所以有：
type(value).__name__ -> "list"
bool(value) -> True
输出：
list True
3. ""
value 是空字符串。而空字符串是典型的假值。所以有：
type(value).__name__ -> "str"
bool(value) -> False
输出：
str False
4. "0"
value 是非空字符串。即使内容看起来像数字零，字符串本身非空，所以是真值。也就有：
type(value).__name__ -> "str"
bool(value) -> True
输出：
str True
5. None
None 也是很典型的假值。所以有：
type(value).__name__ -> "NoneType"
bool(value) -> False
输出：
NoneType False
6. LocalizedEntries([])
LocalizedEntries 这个自定义类本身没有定义 __bool__()，但定义了 __len__()。所以 bool(value) 求值时会调用自定义对象所继承的 __len__()。又因为 self.entries 是 []，len(self.entries) 为 0，所以对象真值为 False。也就有输出：
LocalizedEntries.__len__
LocalizedEntries False
7. LocalizedEntries([{"key": "menu.start"}])
同样没有 __bool__()，所以调用 __len__()。而此时的 self.entries 是一个包含 1 个元素的列表，len(self.entries) 为 1。所以对象真值为 True。也就有输出：
LocalizedEntries.__len__
LocalizedEntries True
8. StrictLocalizedEntries([{"key": "menu.start"}])
StrictLocalizedEntries 这个自定义类本身定义了 __bool__()。只要类有 __bool__()，真值测试优先使用 __bool__()，不会退回去调用继承来的 __len__()。依据源码可知 __bool__ 返回：bool(self.entries) and all("text" in item for item in self.entries)。因为 self.entries 是非空列表，所以 bool(self.entries) 为 True。但其中唯一的 item 是 {"key": "menu.start"}，没有 "text" 键。所以 all(...) 为 False。也就是说，最终真值测试的结果是 False（因为 True and False -> False），所以有输出：
StrictLocalizedEntries.__bool__
StrictLocalizedEntries False
9. StrictLocalizedEntries([{"key": "menu.start", "text": "Start"}])
同样优先调用 __bool__()，不会调用 __len__()。这次的 self.entries 依然指向非空列表，所以 bool(self.entries) 为 True。和上一个 value 不同的是，唯一 item 中有 "text" 键，所以这次的 all(...) 为 True。也就是说，最终真值测试的结果是 True（因为 True and True -> True），所以有输出：
StrictLocalizedEntries.__bool__
StrictLocalizedEntries True
10. BrokenFlag()
依据源码不难判断，bool(BrokenFlag()) 会调用 BrokenFlag.__bool__()。但 __bool__() 返回的是整数 1。而在 Python 中，__bool__() 必须返回真正的 bool 对象，即 True 或 False！返回 int 属于协议错误，所以真值测试的过程中必然抛出 TypeError。try / except 捕获异常后输出异常类型名：TypeError。

综上，总结：
1. LocalizedEntries 之所以调用 __len__() 是因为它没有定义 __bool__()，但定义了 __len__()。
2. StrictLocalizedEntries 不会退回调用继承来的 __len__()，因为 __bool__() 优先级更高。
3. [""] 与 "" 的真值不同：
   - "" 是空字符串，是假值；
   - [""] 是非空列表，是真值。
4. BrokenFlag.__bool__() 返回 1 不合法，因为 __bool__() 必须返回 bool 作为真值测试的结果，而不是“可被真值测试的对象”。

验证后修正：

无须修正。
```

---

## C. 短路求值：操作数返回、默认值陷阱与副作用（15 分）

预测完整输出，并解释哪些函数调用发生、哪些被短路跳过。

```python
def mark(name, value):
    print("mark", name)
    return value


missing_keys = mark("missing", [])
empty_text_keys = mark("empty", ["menu.start"])
strict = True
user_path = ""
default_path = "audit.txt"

issue = missing_keys or empty_text_keys
should_abort = strict and issue
path_bad = user_path or default_path
path_precise = default_path if user_path is None else user_path

print("issue =", issue, type(issue).__name__)
print("should_abort =", should_abort, type(should_abort).__name__)
print("path_bad =", repr(path_bad))
print("path_precise =", repr(path_precise))

message = mark("abort", "stop") if should_abort else mark("ok", "continue")
print("message =", message)

print(mark("left", "") and mark("right", "unused"))
print(mark("primary", "report") or mark("fallback", "unused"))
```

要求至少说明：

1. `issue` 和 `should_abort` 是不是 `bool`；
2. `path_bad` 与 `path_precise` 为什么不同；
3. `mark("ok", "continue")`、`mark("right", "unused")`、`mark("fallback", "unused")` 是否会调用；
4. `print(mark("left", "") and ...)` 最终输出什么显示形式。

答题区：

```tex
验证前预测：

完整输出为：
mark missing
mark empty
issue = ['menu.start'] list
should_abort = ['menu.start'] list
path_bad = 'audit.txt'
path_precise = ''
mark abort
message = stop
mark left

mark primary
report

注意：
在 mark left 后面有一个空白输出行，因为表达式 mark("left", "") and mark("right", "unused") 最终返回空字符串 ""，而 print("") 会打印一个空行。

逐项解释：
1. 初始赋值阶段
missing_keys = mark("missing", [])
这条赋值语句执行时首先调用 mark("missing", [])：输出mark missing并返回 []，然后名字 missing_keys 绑定在返回的空列表对象 [] 上。
empty_text_keys = mark("empty", ["menu.start"])
这条赋值语句执行时首先调用 mark("empty", ["menu.start"])：输出mark empty并返回 ["menu.start"]，然后名字 empty_text_keys 绑定在返回的列表对象 ["menu.start"] 上。
2. issue 对应的代码部分是：
issue = missing_keys or empty_text_keys
其中，missing_keys 指向空列表 []，是假值。即 or 左侧为假，所以 missing_keys or empty_text_keys 求值时直接返回右侧操作数对象 empty_text_keys，也就是列表对象 ["menu.start"]。因此，名字 issue 绑定在列表对象 ["menu.start"] 上。
3. should_abort 对应的代码部分是：
should_abort = strict and issue
其中，strict 绑定的是 True，自然是真值。因为 and 左侧为真，所以 strict and issue 求值时直接返回右侧操作数对象 issue，也就是列表对象 ["menu.start"]。因此，名字 should_abort 绑定在列表对象 ["menu.start"] 上。
4. path_bad 与 path_precise 对应的代码部分是：
user_path = ""
default_path = "audit.txt"

path_bad = user_path or default_path
path_precise = default_path if user_path is None else user_path
user_path 绑定的是空字符串 ""，是典型的假值。因为 or 左侧为假，所以 user_path or default_path 求值时直接返回右侧操作数对象 default_path，也就是字符串对象 "audit.txt"。因此，名字 path_bad 绑定在字符串对象 "audit.txt" 上；
user_path 绑定的是空字符串 ""，显然对于条件 user_path is None，条件位置的表达式求值结果为 False。所以对于整个条件表达式 default_path if user_path is None else user_path 来说，将会进入 `else` 分支并返回 user_path 绑定的对象，即空字符串对象 ""！因此，名字 path_precise 绑定在字符串对象 "" 上。
5. message 对应的代码部分是：
message = mark("abort", "stop") if should_abort else mark("ok", "continue")
由前述可知，should_abort 指向 ["menu.start"] 这个非空列表，是真值。所以条件表达式只求值真值分支：即求值 mark("abort", "stop")，将会输出mark abort并返回字符串对象 "stop"，最终，名字 message 绑定到了 "stop" 上，并且 mark("ok", "continue") 不会调用，因为条件表达式未选中的分支不会求值。
6. print(mark("left", "") and mark("right", "unused"))
先求值左侧操作数：mark("left", "")，将会输出mark left并返回空字符串对象 ""，由于空字符串是典型的假值，而 and 左侧为假时直接返回左侧操作数，不求值右侧。所以，mark("right", "unused") 不会调用，并且由于整个表达式返回 "" 会导致紧跟在mark left之后的输出变成一条空行（print("") 会打印一个空行）。
7. print(mark("primary", "report") or mark("fallback", "unused"))
先求值左侧操作数：mark("primary", "report")，将会输出mark primary并返回字符串对象 "report"，由于非空字符串是真值，而 or 左侧为真时直接返回左侧操作数，不求值右侧。所以，mark("fallback", "unused") 不会调用。

对于重点问题的回答：
1. issue 和 should_abort 都不是 bool，都是 list 对象：
   issue -> ["menu.start"]
   should_abort -> ["menu.start"]
2. path_bad 与 path_precise 不同，是因为 path_bad 使用 or 默认值技巧，把空字符串 "" 当成假值替换成 "audit.txt"；path_precise 只在 user_path is None 为真时才使用默认值，所以保留了 ""。
3. 以下调用不会发生（详见上面的分析）：
   mark("ok", "continue")
   mark("right", "unused")
   mark("fallback", "unused")
4. print(mark("left", "") and ...) 最终输出空字符串的显示效果，也就是一个空行；不是 False，也不是 None。

验证后修正：

无须修正。
```

---

## D. 比较、身份、成员测试与比较链（15 分）

预测完整输出，并解释每一行问的是“相等性、身份、成员关系、真值测试、比较链”中的哪一种问题。

```python
record_a = {"key": "menu.start", "text": ""}
record_b = {"key": "menu.start", "text": ""}
records = [record_a]

print(record_a == record_b)
print(record_a is record_b)
print(record_b in records)
print(record_b is records[0])
print(record_a["text"] == "")
print(bool(record_a["text"]))
print(record_a["text"] == False)


def probe(name, value):
    print("probe", name)
    return value


print("chain-1")
print(probe("low", 1) < probe("mid", 3) <= probe("high", 3))

print("chain-2")
print(probe("a", 5) < probe("b", 2) < probe("c", 9))
```

要求至少说明：

1. `record_b in records` 使用相等性还是身份；
2. `record_a["text"] == False` 为什么不是在问空字符串真假；
3. 两条比较链中哪些 `probe(...)` 会调用，哪些不会；
4. 比较链为什么不能简单当成文本替换版的 `and`。

答题区：

```tex
验证前预测：

完整输出为：
True
False
True
False
True
False
False
chain-1
probe low
probe mid
probe high
True
chain-2
probe a
probe b
False

逐行解释：
1. print(record_a == record_b)
record_a 和 record_b 分别绑定到由两个相互独立的字典字面量表达式创建的不同的字典对象，但二者的键值对内容相同。因为 == 比较的是值意义上的相等性，不是身份，而字典的相等性比较默认看键值对是否相等，所以 record_a == record_b 的求值结果是 True。

这一行问的是：相等性。
2. print(record_a is record_b)
首先明确：is 比较对象身份。record_a 和 record_b 绑定的是两个分别创建的字典对象，内容相同但不是同一个对象。所以 record_a is record_b 的求值结果是 False。

这一行问的是：身份。
3. print(record_b in records)
前面已执行：records = [record_a]，也就是说，records 现在指向一个内部槽位只保存了 record_a 引用的列表对象。record_b in records 会检查 records 绑定的对象中是否存在与 record_b 相等的元素。即：列表成员测试使用相等性比较，而不是要求身份相同。由前述已知有：record_b == record_a -> True，所以现有：record_b in records 的求值结果是 True。

这一行问的是：成员关系；成员关系内部使用相等性判断。
4. print(record_b is records[0])
从前面的解释已知：records 现在指向一个内部槽位只保存了 record_a 引用的列表对象；并且record_a 和 record_b 绑定的是两个内容相等但身份不同的字典对象。所以 records[0] 求值结果正是 record_a 指向的字典对象，record_b is records[0] 等价于 record_b is record_a，显然求值结果是 False。

这一行问的是：身份。
5. print(record_a["text"] == "")
不难得到：record_a["text"] 求值结果是空字符串 ""。而 `== ""` 是相等性比较，在这里，用于精确判断 "" 是否等于空字符串。所以，record_a["text"] == "" 的求值结果显然是 True。

这一行问的是：相等性。
6. print(bool(record_a["text"]))
已知 record_a["text"] 求值结果是空字符串 ""。而空字符串在真值测试中为假。所以有：bool(record_a["text"]) 的求值结果为 False。

这一行问的是：真值测试。
7. print(record_a["text"] == False)
这是相等性比较，不是真值测试。record_a["text"] 求值得到的空字符串确实是假值，但空字符串本身并不等于 False。所以，record_a["text"] == False 的求值结果是 False。

这一行问的是：相等性，不是在问空字符串真假。
8. chain-1 部分：
print("chain-1") 求值后输出chain-1，然后控制流抵达这一步：
print(probe("low", 1) < probe("mid", 3) <= probe("high", 3))
这里的执行顺序是：首先进行 probe("low", 1) 的调用，输出probe low并返回 1；接着是对 probe("mid", 3) 的调用，输出probe mid并返回 3；比较 1 < 3，结果 True；因为前半段为真，继续求值后半段；所以继续对 probe("high", 3) 调用，输出probe high并返回 3；比较 3 <= 3，结果 True。由此，整个比较链的结果为 True。
9. chain-2 部分：
print("chain-2") 求值后输出chain-2，然后控制流抵达这一步：
print(probe("a", 5) < probe("b", 2) < probe("c", 9))
这里的执行顺序是：首先进行 probe("a", 5) 的调用，输出probe a并返回 5；接着是对 probe("b", 2) 的调用，输出probe b并返回 2；比较 5 < 2，结果 False。要注意：此时比较链已经失败（整个比较链的结果为 False），因此短路，不再调用后面的 probe("c", 9)。

对于重点问题的回答：
1. record_b in records 使用相等性，不是身份。它会检查 records 中是否有元素与 record_b 相等。
2. record_a["text"] == False 不是在问空字符串的真假。它是在问空字符串对象 "" 是否与布尔对象 False 相等，答案是 False。如果要问真假，应使用 bool(record_a["text"]) 或 if record_a["text"]。
3. 两条比较链中：
chain-1 调用 probe low、probe mid、probe high；
chain-2 调用 probe a、probe b，不调用 probe c。
4. 比较链不能简单当成文本替换版的 and。例如 a < b < c 在逻辑上接近 a < b and b < c，但中间表达式 b 只求值一次。如果简单文本替换，b 可能被求值两次，副作用和性能都不同。

验证后修正：

无须修正。
```

---

## E. 控制流语法：分支选择、缩进归属与条件表达式（20 分）

### E1. 互斥分支链与独立 `if`（8 分）

预测完整输出。

```python
def check(name, result):
    print("check", name)
    return result


missing = ["menu.quit"]
empty = ["menu.start"]
dry_run = True

print("chain")
if check("missing", missing):
    print("abort missing")
elif check("empty", empty):
    print("abort empty")
elif check("dry-run", dry_run):
    print("preview")
else:
    print("write")

print("separate")
if check("missing-2", missing):
    print("collect missing")

if check("empty-2", empty):
    print("collect empty")

if check("dry-run-2", dry_run):
    print("collect dry-run")
```

要求说明：

1. `chain` 部分哪些 `check(...)` 不会调用；
2. `separate` 部分为什么可能输出多个收集结果；
3. 这两种结构分别适合“选择一个最终动作”还是“收集所有命中的问题”。

答题区：

```tex
验证前预测：

完整输出为：
chain
check missing
abort missing
separate
check missing-2
collect missing
check empty-2
collect empty
check dry-run-2
collect dry-run

逐项解释：
1. chain 部分
在进入 if / elif / else 链之前，已执行赋值语句：missing = ["menu.quit"]，所以 missing 绑定的是非空列表，真值为真。再然后求值 print("chain")，产生输出副作用：输出chain。最后控制流进入 if / elif / else 链：
if check("missing", missing):
率先检查 `if` 分支的条件，调用 check("missing", missing)：输出check missing并返回 missing，也就是 ["menu.quit"]。因为非空列表为真，所以控制流只会进入第一个 if 的代码块：求值 print("abort missing")，又产生输出副作用：输出abort missing。因为第一个分支已经命中，后续 elif 条件不再求值。所以以下调用不会发生：
check("empty", empty)
check("dry-run", dry_run)
也就不会输出：
abort empty
preview
write
综上，chain 部分的完整输出如下：
chain
check missing
abort missing
2. separate 部分
先求值 print("separate")，产生输出副作用：输出separate。再往后是三个独立 if，要注意它们不是互斥链。
第一个独立 if：
if check("missing-2", missing):
检查第一个 `if` 分支的条件，调用 check("missing-2", missing)：输出check missing-2并返回 missing，也就是 ["menu.quit"]。因为非空列表为真，所以控制流进入第一个独立 if 的代码块：求值 print("collect missing")，又产生输出副作用：输出collect missing。
第二个独立 if：
if check("empty-2", empty):
检查第二个 `if` 分支的条件，调用 check("empty-2", empty)：输出check empty-2并返回 empty，也就是 ["menu.start"]。因为非空列表为真，所以控制流也会进入第二个独立 if 的代码块：求值 print("collect empty")，又产生输出副作用：输出collect empty。
第三个独立 if：
if check("dry-run-2", dry_run):
检查第三个 `if` 分支的条件，调用 check("dry-run-2", dry_run)：输出check dry-run-2并返回 dry_run，也就是 True。因为 True 为真，所以控制流也会进入第三个独立 if 的代码块：求值 print("collect dry-run")，又产生输出副作用：输出collect dry-run。

对于重点问题的回答：
1. chain 部分不会调用：
check("empty", empty)
check("dry-run", dry_run)
因为第一个 if 条件已经命中，后续 elif 不再求值。
2. separate 部分可能输出多个收集结果，因为三个 if 互相独立，每个条件都会被检查。前一个 if 命中不会阻止后一个 if 继续求值。
3. 两种结构的适用场景：
- if / elif / else 链适合选择一个最终动作，例如 abort missing / abort empty / preview / write 中只能选一个；
- 多个独立 if 适合收集所有命中的问题，例如同时收集 missing、empty、dry-run 等状态。

验证后修正：

无须修正。
```

### E2. 缩进、空代码块与 `pass`（6 分）

下面三段代码分别分析。若不能作为完整脚本正常运行，请指出错误发生在解析/编译前还是运行期。

```python
# 片段 1
enabled = True
has_errors = False

if enabled:
    if has_errors:
        print("blocked")
    else:
        print("ready")
else:
    print("disabled")
```

```python
# 片段 2
enabled = True

if enabled:
    # TODO: implement later
else:
    print("disabled")
```

```python
# 片段 3
enabled = True

if enabled:
    pass
else:
    print("disabled")
print("after")
```

答题区：

```tex
验证前预测：

片段 1 可以正常运行：
enabled = True
has_errors = False

if enabled:
    if has_errors:
        print("blocked")
    else:
        print("ready")
else:
    print("disabled")

由源码易得：enabled 和 has_errors 分别绑定到 True 和 False，所以控制流一定会进入外层 if，不过内层 if 的条件不成立，所以控制流接着进入内层 else 分支，最终求值 print("ready")：产生输出副作用，输出ready。注意：内层 else 与 if has_errors 缩进对齐，所以它属于内层 if；而外层 else 与 if enabled 缩进对齐，所以它属于外层 if。
片段 2 不能作为完整脚本正常运行，错误发生在解析/编译阶段，不是运行期：
enabled = True

if enabled:
    # TODO: implement later
else:
    print("disabled")

由源码易得：enabled 绑定到 True，所以控制流一定会进入 if 分支，问题在于 if enabled: 后面的代码块中只有注释。注释不是 Python 语句，会被解析器忽略，不能构成有效代码块。而 Python 要求 if 后面必须有至少一条真正的语句。因此第二个代码片段在解析/编译阶段就会抛出类似：IndentationError: expected an indented block after 'if' statement... 的异常，根本不会延迟至运行期。
片段 3 可以正常运行：
enabled = True

if enabled:
    pass
else:
    print("disabled")
print("after")

由源码易得：enabled 绑定到 True，所以控制流一定会进入 if 代码块。pass 是一条真正的 Python 语句，表示什么也不做，用来占位。因此这次的 if 代码块合法。执行 pass 后，跳过 else。然后继续执行外层的 print("after")：输出after。

验证后修正：

无须修正。
```

### E3. 条件表达式的值选择（6 分）

预测完整输出，并说明未选中的分支是否求值。

```python
def build(label, value):
    print("build", label)
    return value


strict = False
issues = ["empty text"]

severity = "error" if strict and issues else "warning"
message = build("issues", issues) if issues else build("ok", [])
print(severity)
print(message)
```

答题区：

```tex
验证前预测：

完整输出为：
build issues
warning
['empty text']

逐项解释：
首先由初始化赋值可得：strict 和 issues 分别绑定到 False 和 ["empty text"]。
1. severity 对应的代码部分是：
severity = "error" if strict and issues else "warning"
先看条件：strict and issues，因为 strict 指向 False。而 and 在左侧为假时直接返回左侧操作数，即 False，右侧 issues 不需要用于决定返回对象所以没有被求值。所以整个条件表达式的条件结果是假值。所以选择 else 分支，并且未选中的分支 "error" 没有求值。最终，severity 被绑定到了 "warning" 上。
2. message 对应的代码部分是：
message = build("issues", issues) if issues else build("ok", [])
这里的条件是 issues。因为 issues 指向非空列表 ["empty text"]，其真值为真。所以只求值真值分支：build("issues", issues)，会输出build issues并返回 issues，也就是 ["empty text"]，并且未被选中的分支 build("ok", []) 没有被求值。最终，message 被绑定到了 ["empty text"] 上。

验证后修正：

无须修正。
```

---

## F. 工程综合题：本地化审计决策与 `match` 边界（20 分）

### F1. 代码阅读：决策流水线（12 分）

预测完整输出，并解释关键绑定。

```python
def report(label):
    print("report", label)
    return f"report:{label}"


strict = True
dry_run = True
missing_keys = []
empty_text_keys = ["menu.start"]
output_path = ""

blocking = missing_keys or empty_text_keys
severity = "error" if strict and blocking else "warning"
mode = "preview" if dry_run else "write"
path = output_path or "audit.txt"
precise_path = "audit.txt" if output_path is None else output_path

print("blocking =", blocking, type(blocking).__name__)
print("severity =", severity)
print("mode =", mode)
print("path =", repr(path))
print("precise_path =", repr(precise_path))

if strict and missing_keys:
    action = report("abort-missing")
elif strict and empty_text_keys:
    action = report("abort-empty")
elif dry_run:
    action = report("preview")
else:
    action = report("write")

event = {"kind": action, "path": precise_path}

match event:
    case {"kind": "report:abort-missing", "path": p}:
        result = f"missing->{p!r}"
    case {"kind": "report:abort-empty", "path": p}:
        result = f"empty->{p!r}"
    case {"kind": "report:preview"}:
        result = "preview"
    case _:
        result = "other"

print("result =", result)
```

要求至少说明：

1. `blocking` 是 `bool` 还是列表对象；
2. `severity` 与 `mode` 如何求值；
3. `path` 与 `precise_path` 的差异是否体现 `or` 默认值陷阱；
4. `if / elif` 链中哪些 `report(...)` 不会调用；
5. `match` 命中哪个 `case`，`p` 是捕获绑定还是已有变量比较。

答题区：

```tex
验证前预测：

完整输出为：
blocking = ['menu.start'] list
severity = error
mode = preview
path = 'audit.txt'
precise_path = ''
report abort-empty
result = empty->''

逐项解释：
1. blocking 对应的代码部分是：
missing_keys = []
empty_text_keys = ["menu.start"]

blocking = missing_keys or empty_text_keys
因为 missing_keys 指向空列表，是假值。意即 or 左侧为假，所以直接返回右侧操作数 empty_text_keys，也就是 ["menu.start"]。所以最终 blocking 绑定在 ["menu.start"] 上。要注意：blocking 指向的不是 bool 对象，而是 list 对象。
2. severity 对应的代码部分是：
strict = True

severity = "error" if strict and blocking else "warning"
这里的条件是：strict and blocking，因为 strict 指向 True，为真，所以 and 直接返回右侧操作数 blocking，也就是 ["menu.start"]。而非空列表在条件语境中也为真。所以条件表达式选择真值分支："error"。最终 severity 绑定在 "error" 上。注意：strict and blocking 本身返回的不是 bool，而是列表对象 ["menu.start"]。但条件表达式会对这个结果做真值测试。
3. mode 对应的代码部分是：
dry_run = True

mode = "preview" if dry_run else "write"
这里的条件是：dry_run，因为 dry_run 指向 True，为真，所以选择真值分支："preview"。所以最终 mode 绑定在 "preview" 上。
4. path 与 precise_path 对应的代码部分是：
output_path = ""

path = output_path or "audit.txt"
precise_path = "audit.txt" if output_path is None else output_path
由于 output_path 指向的空字符串 "" 是假值，所以 or 返回右侧默认路径："audit.txt"，最终 path 绑定在 "audit.txt" 上；而条件表达式那里的条件判断的是 output_path is None，已知 output_path 指向 ""，而不是 None，所以整个条件表达式会返回原始 output_path，也就是 ""，最终 precise_path 绑定在 "" 上。这里确实体现了 or 默认值陷阱：path 使用 value or default，会把 "" 误当成“没有提供路径”；precise_path 只在 output_path is None 为真时才使用默认值，因此保留了空字符串。
5. if / elif 链代码：
if strict and missing_keys:
    action = report("abort-missing")
elif strict and empty_text_keys:
    action = report("abort-empty")
elif dry_run:
    action = report("preview")
else:
    action = report("write")

第一个 if 分支的条件是：strict and missing_keys。因为 strict 指向 True；而 missing_keys 指向空列表 []，所以 and 左侧为真，直接返回右侧的 []。又因为 [] 为假，所以第一个 if 分支的条件不成立。这意味着 report("abort-missing") 不会调用。
第二个是 elif 分支，其条件是：strict and empty_text_keys。因为 strict 指向 True；而 empty_text_keys 指向非空列表 ["menu.start"]，所以 and 左侧为真，直接返回右侧的 ["menu.start"]。又因为 ["menu.start"] 为真，所以这个 elif 分支命中。这意味着 report("abort-empty") 会调用：输出report abort-empty并返回 "report:abort-empty"，最终 action 绑定到 "report:abort-empty"。后续 elif dry_run 和 else 不会再检查或执行。所以不会调用：report("preview") 和 report("write")。
6. match 部分：
首先执行赋值语句：event = {"kind": action, "path": precise_path}，因为此时有：action 指向 "report:abort-empty"；precise_path 指向 ""，所以最终 event 绑定到字典对象 {"kind": "report:abort-empty", "path": ""} 上。接下来：
match event:
第一个 case：`case {"kind": "report:abort-missing", "path": p}:` 不匹配。因为 event["kind"] 的求值结果是 "report:abort-empty" 而不是 "report:abort-missing"。
第二个 case：`case {"kind": "report:abort-empty", "path": p}:` 匹配成功。注意：这里的 p 是捕获绑定，不是比较已有变量。因此，p 绑定到 event["path"] 的求值结果，也就是 ""。再然后执行赋值语句 `result = f"empty->{p!r}"`，不难得到：result 最终绑定到 "empty->''"。

对于重点问题的回答：
1. blocking 是列表对象 ["menu.start"]，不是 bool。
2. severity 因 strict and blocking 的求值结果在条件语境中为真而得到 "error"；mode 因 dry_run 为 True 而得到 "preview"。
3. path 与 precise_path 的差异体现了 or 默认值陷阱：path 把空字符串替换成默认路径；precise_path 保留空字符串。
4. if / elif 链中不会调用：
   report("abort-missing")；
   report("preview")；
   report("write")，
   只调用 report("abort-empty")。
5. match 命中第二个 case：`case {"kind": "report:abort-empty", "path": p}`。而且 p 是捕获绑定，不是已有变量比较。

验证后修正：

无须修正。
```

### F2. 小设计题：写出清晰条件而不是聪明面条（8 分）

请设计一个函数或伪代码函数 `decide_audit_action(strict, dry_run, missing_keys, empty_text_keys, output_path)`。

要求：

1. 返回一个结构化字典，例如包含 `action`、`severity`、`mode`、`path`、`issues` 等字段；
2. 如果 `output_path is None` 才使用默认路径；如果 `output_path == ""`，保留空字符串，不要被 `or` 默认值误伤；
3. `strict and missing_keys` 优先级高于 `strict and empty_text_keys`；
4. `dry_run` 只影响 `mode` 或最终写入行为，不应掩盖已有阻断问题；
5. 至少用一处条件表达式，但不要把多条有副作用的逻辑塞进条件表达式；
6. 简要说明你为什么选择 `if / elif`、多个独立 `if` 或 `match`。

答题区：

```tex
验证前设计：

def decide_audit_action(strict, dry_run, missing_keys, empty_text_keys, output_path):
    default_path = "audit.txt"

    path = default_path if output_path is None else output_path
    mode = "preview" if dry_run else "write"

    issues = {
        "missing": missing_keys,
        "empty_text": empty_text_keys,
    }

    has_blocking_issue = bool(missing_keys or empty_text_keys)
    severity = "error" if strict and has_blocking_issue else "warning"

    if strict and missing_keys:
        action = "abort-missing"
        reason = "missing keys block strict audit"
    elif strict and empty_text_keys:
        action = "abort-empty"
        reason = "empty translations block strict audit"
    elif dry_run:
        action = "preview"
        reason = "dry run: preview only"
    else:
        action = "write"
        reason = "write audit report"

    return {
        "action": action,
        "severity": severity,
        "mode": mode,
        "path": path,
        "issues": issues,
        "reason": reason,
        "has_blocking_issue": has_blocking_issue,
    }

设计说明：
1. path 的处理不用 output_path or default_path。原因是 output_path == "" 可能是用户显式传入的路径值或特殊配置，不应该被 or 默认值误伤。因此使用：path = default_path if output_path is None else output_path。这样只有 output_path is None 求值结果是 True 时才使用默认路径；如果 output_path == ""，会保留空字符串。
2. mode 使用条件表达式：mode = "preview" if dry_run else "write"。因为这是简单二选一地产生值，适合使用条件表达式。
3. severity 也使用条件表达式：severity = "error" if strict and has_blocking_issue else "warning"。这里表达的是简单二选一的级别选择。同时要注意：has_blocking_issue 显式转成 bool，是为了让返回字典中的字段类型更稳定。如果直接写 missing_keys or empty_text_keys，结果可能是列表对象，而不是 bool。
4. action 使用 if / elif / else，而不是嵌套条件表达式。原因是：
action 是有优先级的业务决策：
strict and missing_keys 优先级最高；
strict and empty_text_keys 次之；
dry_run 只影响预览或写入模式，不应该掩盖已有阻断问题，
所以最终选择 if / elif / else 更清楚。
5. 之所以这次设计没有使用多个独立 if，是因为 action 是最终动作，应该只选择一个。多个独立 if 适合收集所有问题，但不适合选择唯一最终动作。本函数中 issues 字段已经负责收集问题；action 字段负责选择最终动作。
6. 之所以这里不优先用 match，是因为这里的核心判断不是“匹配一个已有结构的形状”，而是根据 strict、dry_run、missing_keys、empty_text_keys 的组合优先级做决策。因此 if / elif / else 比 match 更直接。match 更适合后续拿已经生成的结构化 event 做分派，例如：
event = {"action": action, "mode": mode}
match event:
    case {"action": "abort-missing"}:
        ...
    case {"action": "preview"}:
        ...
但在这个决策函数内部，if / elif / else 更适合表达优先级。

验证后修正：

无须修正。该设计满足题目要求：
1. 返回结构化字典；
2. output_path is None 求值结果为 True 时才使用默认路径，output_path == "" 时 "" 会被保留；
3. strict and missing_keys 优先级高于 strict and empty_text_keys；
4. dry_run 只影响 mode 或最终非阻断时的动作，不掩盖已有阻断问题；
5. 使用了条件表达式，但没有把多条副作用逻辑塞进条件表达式；
6. 使用 if / elif / else 表达唯一最终动作的优先级，用 issues 字段保留所有问题。
```

---

## Codex 批改记录（逐题审批，2026-06-29）

### 审批结论

建议得分：`100 / 100`。

阶段判断：`P3_Statements_and_Syntax / C12_if_Tests_and_Syntax_Rules` 阶段测验通过。你的答案没有出现会改变运行结果、控制流归属、对象返回值或协议规则判断的实质错误；本次只保留几条术语级精修提醒，作为后续复盘锚点。

### 先给 Findings：需要显式纠正或精修的地方

1. **B 题术语精修，不扣分**：你在解释 `LocalizedEntries([])` 时一处写成“调用自定义对象所继承的 `__len__()`”。在这道题中，`LocalizedEntries` 的 `__len__()` 是本类直接定义的方法，不是继承来的方法；`StrictLocalizedEntries` 才是继承了这个 `__len__()`，但因自身定义了 `__bool__()`，真值测试不会退回去调用继承来的 `__len__()`。你后面的总结已经写对，因此这里只作为措辞修正。
2. **E2 题解析期/运行期措辞精修，不扣分**：你正确指出片段 2 会在解析/编译阶段失败。不过在解释时提到“`enabled` 绑定到 `True`，所以控制流一定会进入 `if` 分支”。严格说，非法脚本在解析/编译成功前没有任何赋值执行，也没有控制流进入；这句话只能作为“如果语法合法时的假设推演”，不能描述真实执行过程。
3. **D 题成员测试补充边界，不扣分**：你说 `record_b in records` 使用相等性而不是身份，这对本阶段教学目标是正确的。更精细地说，序列成员测试不是“必须是同一个对象”；语言语义上会按成员关系规则寻找匹配元素，通常以相等性为核心，具体实现可以对同一对象做快速路径。因此复盘时记住：这里要反对的是“成员测试等于 `is`”，不是说实现永远完全不看身份。

### 逐题审批

| 题目 | 分数 | 审批意见 |
| --- | ---: | --- |
| A1 | 5 / 5 | 完全正确。能稳定区分对象本体、`bool(x)` 的真值结果、`x == True` 的相等性比较；也能说明条件表达式是表达式，不是 `if` 语句。 |
| A2 | 5 / 5 | 完全正确。`and` / `or` 返回操作数对象、`not` 返回布尔对象、`if` 会对整个表达式结果再做真值测试，这三层都说明清楚。 |
| A3 | 5 / 5 | 完全正确。互斥链、独立 `if`、`pass`、注释、`match` 无 fall-through、mapping pattern 捕获绑定都解释到位。 |
| B | 15 / 15 | 输出预测正确，协议优先级正确：先 `__bool__()`，无 `__bool__()` 才看 `__len__()`；错误返回类型直接 `TypeError`，不会把 `__len__()` 当补救路径。仅保留上方“方法来源”措辞精修。 |
| C | 15 / 15 | 完全正确。`issue`、`should_abort` 均为列表对象，`path_bad` 暴露 `or` 默认值陷阱，未选中条件表达式分支和短路右侧调用均不会发生，空字符串经 `print()` 表现为空行。 |
| D | 15 / 15 | 完全正确。相等性、身份、成员关系、真值测试、比较链的输出和求值顺序均正确；比较链中间表达式只求值一次、失败后短路，这一点解释得很好。 |
| E1 | 8 / 8 | 完全正确。能把“选择唯一最终动作”的 `if / elif / else` 和“收集所有命中问题”的多个独立 `if` 分开。 |
| E2 | 6 / 6 | 判断正确。缩进归属、注释不构成代码块、`pass` 是合法语句、语法错误发生在解析/编译阶段均正确；仅保留上方解析期/运行期措辞精修。 |
| E3 | 6 / 6 | 完全正确。条件表达式只求值被选中的分支；`strict and issues` 因左侧假值短路，`build("ok", [])` 不会调用。 |
| F1 | 12 / 12 | 完全正确。`blocking` 是列表对象，`severity` / `mode` / `path` / `precise_path` 的绑定都正确；`report("abort-empty")` 是唯一调用；`match` 命中第二个 case，`p` 是捕获绑定。 |
| F2 | 8 / 8 | 设计达标。结构化返回、精确处理 `None` 与空字符串、阻断优先级、`dry_run` 职责、条件表达式使用边界、`if / elif / else` 与 `match` 的取舍都合理。`has_blocking_issue = bool(...)` 是很好的工程稳定性处理。 |

### 本阶段末评语与能力判断

这份答卷体现出你已经把 C10/C11 的“表达式求值、语句执行、名字绑定、输出副作用”模型，成功迁移到了 C12 的条件控制流：你不再把条件粗略理解成 `True/False` 字面量，而是能追踪“表达式先返回哪个对象，条件位置再如何对该对象做真值测试，控制流最终进入哪个代码块”。

最有价值的进步是：你能在本地化审计语境中主动避开 `value or default` 的默认值陷阱，并把 `if / elif / else` 用于唯一动作选择，把多个独立 `if` 用于问题收集，把 `match` 留给结构化事件分派。这说明你已经开始按“业务语义 + Python 求值规则”一起设计条件，而不是只追求短小写法。

阶段结论：C12 通过，可以进入 C12 收束与下一章 `C13_while_and_for_Loops` 的准备。进入循环阶段时，建议把本章已经压实的短路、真值测试和控制流选择继续迁移到循环退出条件、`break` / `continue`、循环 `else`、循环变量绑定和“遍历时修改容器”的风险上。

## 学习画像更新（审批完成，2026-06-29）

本次已同步更新 `notes/Python_Learning_Profile.md`。可复用到后续笔记和下一章启动模板的画像摘要如下：

- 稳定强项：能稳定解释真值测试协议、`__bool__()` / `__len__()` 优先级、`and` / `or` 返回操作数对象、`not` 返回布尔对象、比较链求值顺序、互斥分支链与独立 `if` 的职责差异、条件表达式与 `if` 语句边界，以及 `match` 的结构化分派边界。
- 工程迁移能力：能把条件控制流放入本地化审计决策中，明确区分阻断问题、预览模式、默认路径、结构化返回和可选副作用。
- 活跃精修点：后续仍要继续保持“解析/编译阶段 vs 运行期控制流”的严格措辞；描述自定义协议方法时要区分本类定义、继承获得和协议优先级。
- 当前水平判断：准中级入门已经坐稳，正在稳定向“可独立完成小型 Python 工程设计的中级入门”推进。
- 下一阶段观察点：`C13_while_and_for_Loops` 中重点观察循环退出条件如何变化、`break` / `continue` 如何转移控制流、循环 `else` 何时执行、循环变量如何绑定，以及遍历过程中修改容器的风险。
