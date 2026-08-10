<!-- quiz-validator: total=100 -->
# C17 Scopes 阶段测验：名字解析与闭包入口

本卷对应 `P4_Functions_and_Generators / C17_Scopes`，章节角色为
`normal`。课程范围与节奏的唯一权威入口是
`docs/C17_SCOPES_STARTUP_TEMPLATE.md`。

## 冻结命题蓝图

### 考察范围

- 名字、绑定、命名空间、作用域和名字查找的区别。
- LEGB 读取顺序、遮蔽、模块全局边界与 builtins 回退。
- 函数代码块的局部名字分类、运行期绑定状态、分支路径与
  `UnboundLocalError`。
- `global` 与 `nonlocal` 改变绑定目标的精确语义。
- 跨作用域重新绑定与对已找到共享对象进行原地修改的区别。
- 嵌套函数、free name 与最小闭包入口，包括共享对象身份和不同外层调用。
- `locals()` / `globals()` 的有限运行期观察与证据边界。
- 隐式模块配置和显式依赖传递之间的工程取舍。

### 明确排除

- 不考 `__closure__`、cell、符号表、字节码或闭包内部实现。
- 不考循环闭包晚绑定、回调、高阶函数组合、递归、lambda 或系统注解。
- 不考完整参数匹配、生成器、基准或 P4 综合陷阱。
- 不运行或考查 `prompt_template_manager`、SQLite、CRUD、CLI 或 GUI。
- 不要求通过写入 `locals()` / `globals()` 完成动态作用域技巧。

### 分区与分值

| 分区 | 题型与重点 | 题号 | 分值 |
| --- | --- | --- | ---: |
| A | 概念解释与规则边界 | A1-A2 | 14 |
| B | LEGB、遮蔽与精确输出 | B1-B2 | 18 |
| C | 局部分类、异常与控制流轨迹 | C1-C2 | 20 |
| D | `global` / `nonlocal`、修改与重绑 | D1-D2 | 20 |
| E | 闭包入口与命名空间观察 | E1-E2 | 14 |
| F | 本地化配置工程应用 | F1 | 14 |
| **合计** | **6 个分区，11 题** | **A1-F1** | **100** |

### 稳定题号与评分映射

| 题号 | 分值 | 主要证据 |
| --- | ---: | --- |
| A1 | 7 | 区分名字、绑定、命名空间、作用域与查找 |
| A2 | 7 | 区分读取规则、绑定目标和对象属性 |
| B1 | 9 | 追踪 enclosing、global 与 builtin 读取 |
| B2 | 9 | 解释模块遮蔽与显式 builtin 访问 |
| C1 | 10 | 定位 `UnboundLocalError` 与异常前副作用 |
| C2 | 10 | 区分静态局部分类和分支上的运行期绑定 |
| D1 | 10 | 追踪模块绑定替换、旧对象修改与身份 |
| D2 | 10 | 追踪最近 enclosing 绑定与共享列表修改 |
| E1 | 8 | 判断闭包、共享对象身份与独立外层调用 |
| E2 | 6 | 限制 `locals()` / `globals()` 的证明范围 |
| F1 | 14 | 用显式依赖重构小型本地化配置函数 |

难度略高于单点预测的舒适区，重点是组合追踪和精确边界，而不是引入相邻章节内容。
所有运行期结论以 Python 3.14.5 为当前验证环境。

## 作答说明

1. 把答案写在每题对应的 `answer:start` 与 `answer:end` 之间。
2. 预测题应给出精确输出；若有异常，还要写明异常类型、发生语句和异常前已完成效果。
3. 解释题应区分名字与对象、读取与绑定、重新绑定与原地修改、语言语义与当前观察。
4. 可以运行代码辅助验证，但答案仍需说明推理链，不能只粘贴输出。
5. 未要求修改仓库中的正式脚本；设计题只需在答题区给出代码和说明。

---

<!-- quiz-section: id=A score=14 -->
## A. 概念解释与规则边界（14 分）

<!-- quiz-question: id=A1 score=7 -->
### A1（7 分）

阅读下面代码，但本题重点不是背诵输出，而是建立名字—作用域—对象关系：

~~~python
catalog = {"menu.start": "Start"}


def inspect(resource):
    local_alias = resource
    return local_alias


returned = inspect(catalog)
~~~

请完成以下说明：

1. 分别列出模块作用域和 `inspect` 本次调用的局部作用域中，与这段代码有关的名字绑定。
2. 结合代码解释“名字”“绑定”“命名空间”“作用域”“名字查找”各指什么；不要把五者写成同义词。
3. 判断 `returned is catalog` 的结果，并说明形参绑定、局部命名空间和字典对象之间的关系。特别说明：调用函数是否复制了调用方命名空间或复制了字典对象。

<!-- answer:start -->

### 1. 模块作用域与本次函数调用中的名字绑定

执行完整段代码后，与题目直接相关的模块级名字绑定可以写成：

```text
模块全局命名空间
├─ catalog  ──> 字典对象 D：{"menu.start": "Start"}
├─ inspect  ──> 函数对象
└─ returned ──> 同一个字典对象 D
```

执行 `inspect(catalog)` 的那一次调用中，局部名字绑定为：

```text
inspect 本次调用的局部命名空间
├─ resource    ──> 字典对象 D
└─ local_alias ──> 同一个字典对象 D
```

其中，`resource` 是形参名字。调用 `inspect(catalog)` 时，先求值实参表达式 `catalog`，得到模块名字 `catalog` 当前绑定的字典对象 D，然后在这一次 `inspect` 调用的局部环境中，让形参名字 `resource` 绑定到 D。

随后执行：

```python
local_alias = resource
```

右侧读取局部名字 `resource`，仍得到 D；左侧在当前函数调用的局部命名空间中建立名字 `local_alias` 到 D 的绑定。

函数返回 `local_alias` 所指对象 D 后，模块层执行：

```python
returned = inspect(catalog)
```

于是模块名字 `returned` 也绑定到 D。

---

### 2. 五个概念的精确区别

#### name（名字）

名字是程序文本中用于引用对象的标识符，例如本题的：

```text
catalog
inspect
returned
resource
local_alias
```

名字不是对象本身，也不是“装对象的盒子”。同一个对象可以同时被多个名字引用；同一个名字也可以在以后重新绑定到其他对象。

#### binding（绑定）

绑定是在某个命名空间中建立“名字 → 对象”的关联。

例如：

```python
catalog = {"menu.start": "Start"}
```

建立模块名字 `catalog` 到字典对象 D 的绑定。

而函数调用时：

```text
resource ──> D
```

则是本次函数调用局部命名空间中的另一个绑定。

重新绑定名字与修改对象本身必须分开。例如：

```python
catalog = {}
```

会重新绑定名字 `catalog`；而：

```python
catalog["menu.quit"] = "Quit"
```

是在读取 `catalog` 找到字典后修改该字典对象，不是在重新绑定名字 `catalog`。

#### namespace（命名空间）

命名空间是维护一组“名字 → 对象”绑定关系的环境。

本题至少涉及两个不同的命名空间：

1. 当前模块的全局命名空间；
2. `inspect` 这一次函数调用的局部命名空间。

它们可以拥有不同名字，却让这些名字指向同一个对象。

#### scope（作用域）

作用域描述源码中的名字可见范围以及一个裸名字在该范围内应从哪些环境解析。

它不是存放对象的容器。比如 `resource` 和 `local_alias` 是 `inspect` 的局部名字；它们的作用域由函数代码块决定，但二者所指的字典对象并不因此获得“局部对象”这一语言属性。

#### name lookup / resolution（名字查找 / 名字解析）

名字查找发生在读取一个裸名字时，Python 根据当前代码块的作用域规则寻找相应绑定。

例如函数中的：

```python
local_alias = resource
```

右侧 `resource` 是一次名字读取。它在当前函数的局部作用域中就找到形参绑定，因此无需继续向外查找。

注意，名字读取规则不能与赋值目标判定混为一谈：左侧 `local_alias` 不是先按 LEGB 搜索一个已有 `local_alias`，而是在没有 `global` / `nonlocal` 声明时作为当前函数的局部绑定目标。

---

### 3. `returned is catalog` 与调用时是否复制

结果是：

```python
returned is catalog
# True
```

原因是：

```text
catalog     ─┐
resource    ├──> 同一个字典对象 D
local_alias ┤
returned    ─┘
```

函数调用并没有复制调用方的模块命名空间。`inspect` 只建立了属于本次调用的局部绑定环境，其中形参 `resource` 绑定到实参表达式求值得到的对象。

函数也没有自动复制字典对象。`local_alias = resource` 只是让另一个局部名字绑定到同一字典；`return local_alias` 返回的仍然是同一对象引用。因此最终模块名字 `returned` 与 `catalog` 指向同一个字典对象。

<!-- answer:end -->

<!-- quiz-question: id=A2 score=7 -->
### A2（7 分）

下面四个断言都有概念边界问题。请逐条写出“正确 / 错误”，并把错误断言改写成精确表述：

1. “LEGB 是统一规则，因此 `name = value` 总会先按 L → E → G → B 查找一个已有名字，再决定写到哪里。”
2. “只要函数中操作的是可变对象，相应名字就会被编译器判定为局部名字。”
3. “`global setting` 会把 `setting` 所指对象变成所有模块共享的全局对象，并改变它的可变性。”
4. “`nonlocal label` 会沿运行期调用栈查找任意调用者的局部变量，直到找到 `label`。”

回答时至少明确区分：裸名字读取、绑定目标判定、对象原地修改，以及
`global` / `nonlocal` 各自能够指向的命名空间。

<!-- answer:start -->

1. **错误。**

   `LEGB` 主要描述普通裸名字读取时的解析顺序，不能把它机械套用于普通名字赋值目标。

   对：

   ```python
   name = value
   ```

   Python 会先求值右侧 `value`。若左侧 `name` 是普通标识符，并且当前代码块中没有相应的 `global name` 或 `nonlocal name` 声明，则该名字绑定到当前局部命名空间；不会先按 `L → E → G → B` 搜索同名已有绑定再决定写哪里。

   更精确地说：

   ```text
   裸名字读取
   → 按当前代码块的名字分类和词法作用域解析

   普通名字赋值
   → 默认绑定当前局部名字
   → global 时绑定模块全局名字
   → nonlocal 时绑定最近的匹配外层函数名字
   ```

2. **错误。**

   名字是否被当前函数判定为局部，取决于该代码块是否存在对这个**名字本身**的绑定操作，以及是否有 `global` / `nonlocal` 声明；不能由对象是否可变决定。

   例如：

   ```python
   records.append("x")
   ```

   只是读取名字 `records` 得到列表，再修改列表对象；它不会因为列表可变就把 `records` 自动判定为当前函数的局部名字。

   反之：

   ```python
   records = []
   ```

   是对普通名字 `records` 的绑定操作，即使右侧对象是可变列表，也应按名字绑定规则判断作用域。

   因此准确表述应是：**对象可变性决定某些对象能否被原地修改，但不决定裸名字的作用域分类。**

3. **错误。**

   ```python
   global setting
   ```

   改变的是当前代码块中名字 `setting` 的解析和绑定目标，使其指向**包含该代码块的模块全局命名空间**中的绑定。

   它不会：

   - 把对象变成“所有模块共享的全局对象”；
   - 改变对象类型；
   - 改变对象身份；
   - 改变对象可变性。

   每个模块有自己的全局命名空间。即使多个模块中的名字恰好指向同一个对象，那也是对象引用关系，不是 `global` 把对象提升成了跨模块通用对象。

4. **错误。**

   ```python
   nonlocal label
   ```

   使用的是**词法嵌套关系**，不是运行时调用栈。它会在当前代码块的外层函数作用域中寻找已经存在的同名绑定；如果多个外层函数都绑定了该名字，则选择最近的一层。

   它不会去任意运行时调用者的局部命名空间查找，也不能用来指向模块全局绑定。

   精确对照为：

   ```text
   global name
   → 当前代码块所属模块的全局绑定

   nonlocal name
   → 词法上最近的、已有同名绑定的外层函数作用域

   普通局部赋值
   → 当前代码块的局部绑定

   obj.attr = value / obj[key] = value
   → 先读取 obj，再让找到的对象处理属性/下标修改；
      通常不重新绑定名字 obj
   ```

<!-- answer:end -->

---

<!-- quiz-section: id=B score=18 -->
## B. LEGB、遮蔽与精确输出（18 分）

<!-- quiz-question: id=B1 score=9 -->
### B1（9 分）

不运行代码，写出两行精确输出：

~~~python
label = "global"


def make_reader():
    label = "enclosing"

    def read():
        return label, len(("menu", "dialog"))

    return read


reader = make_reader()
label = "changed global"

print(reader())
print(label)
~~~

然后分别为 `read()` 中的两个裸名字读取写出查找路径和命中层级：

- `label`
- `len`

最后解释为什么外层调用已经返回、模块层 `label` 又被重新绑定之后，
`reader()` 仍能得到题中那个 `label` 值。答案只需使用 C17 的 free name /
闭包入口模型，不需要讨论 cell 或其他内部实现。

<!-- answer:start -->

两行精确输出是：

```text
('enclosing', 2)
changed global
```

### `read()` 中 `label` 的查找路径

`read` 自己没有绑定 `label`，因此读取时先检查当前局部层，没有命中；然后进入词法外层函数 `make_reader` 的 enclosing 层：

```text
L：read 本身没有 label
E：make_reader 的 label ──> "enclosing"   ← 命中并停止
G：不会继续
B：不会继续
```

因此 `read()` 返回元组第一项 `"enclosing"`。

### `read()` 中 `len` 的查找路径

`len` 也没有在 `read` 中绑定；`make_reader` 的外层函数作用域中同样没有 `len`；模块中也没有同名绑定，因此最终在 builtins 层命中内置函数：

```text
L：无 len
E：无 len
G：模块中无 len
B：内置 len   ← 命中
```

表达式：

```python
len(("menu", "dialog"))
```

得到整数 `2`。

所以：

```python
reader()
```

返回：

```python
("enclosing", 2)
```

打印时显示：

```text
('enclosing', 2)
```

### 为什么 `make_reader()` 已返回后仍得到 `"enclosing"`

`read` 是定义在 `make_reader` 内部的嵌套函数，并且它使用了外层名字 `label`。当 `make_reader()` 返回 `read` 函数对象后，返回的内部函数仍保留对执行所需外层绑定的访问能力。因此外层调用结束并不意味着该绑定对 `reader` 立即失去可达性。

随后模块层执行：

```python
label = "changed global"
```

只是把**模块全局名字** `label` 重新绑定到字符串 `"changed global"`。它没有修改 `make_reader` 那一次调用中供 `reader` 使用的 enclosing `label` 绑定。

由于 `reader()` 中的 `label` 在 E 层已经命中：

```text
E：label ──> "enclosing"
```

它不会继续查找模块 G 层。因此后续模块级重新绑定不改变 `reader()` 返回的第一项。

最后模块顶层：

```python
print(label)
```

读取的是模块自己的全局名字，所以输出：

```text
changed global
```

<!-- answer:end -->

<!-- quiz-question: id=B2 score=9 -->
### B2（9 分）

预测精确输出，并回答后续问题：

~~~python
import builtins

len = "module shadow"


def report():
    entries = ("menu.start", "menu.quit")
    return len, builtins.len(entries)


print(report())
~~~

1. `report()` 中裸名字 `len` 的 LEGB 查找在哪一层停止？为什么不会继续使用 B 层的内置 `len`？
2. 表达式 `builtins.len(entries)` 是否等于“让裸名字 `len` 跳过模块遮蔽继续执行 B 层查找”？请从先解析名字 `builtins`、再进行属性访问的角度给出精确解释。
3. 这段代码中的“global”属于哪个命名空间？不要把它描述成跨所有模块的通用名字池。

<!-- answer:start -->
<!-- answer:end -->

---

<!-- quiz-section: id=C score=20 -->
## C. 局部分类、异常与控制流轨迹（20 分）

<!-- quiz-question: id=C1 score=10 -->
### C1（10 分）

不运行代码，写出全部精确输出：

~~~python
counter = 10
events = []


def update(flag):
    events.append(f"start:{flag}")
    before = counter
    if flag:
        counter = 20
    events.append("done")
    return before, counter


for flag in (False, True):
    try:
        print("return", flag, update(flag))
    except UnboundLocalError as error:
        print("error", flag, type(error).__name__)

print("module", counter)
print("events", events)
~~~

然后对 `False` 和 `True` 两次调用分别说明：

1. `counter` 为什么在整个 `update` 代码块中被归类为局部名字；
2. 首个失败语句是哪一条，为什么两个实参都无法执行到条件分支；
3. 异常前哪些对象修改已经发生，哪些语句没有执行；
4. 模块层 `counter` 和 `events` 的最终状态为什么不同。

不能只回答“函数报错所以什么都没改变”；需要沿真实执行顺序区分已完成副作用与未执行操作。

<!-- answer:start -->
<!-- answer:end -->

<!-- quiz-question: id=C2 score=10 -->
### C2（10 分）

预测精确输出：

~~~python
result = ["module"]


def collect(flag):
    if flag:
        result = []
    result.append("scan")
    return result


for flag in (True, False):
    try:
        print(flag, collect(flag))
    except UnboundLocalError as error:
        print(flag, type(error).__name__)

print(result)
~~~

请解释：

- 为什么 `result` 在 `collect` 中对两个控制流路径都属于局部名字；
- `True` 路径在调用 `append` 前具有什么运行期绑定，而 `False` 路径缺少什么；
- 为什么模块层已经存在同名列表仍不能挽救 `False` 路径；
- 为什么“列表是可变对象”既不能决定局部名字分类，也不能保证方法调用一定成功。

<!-- answer:start -->
<!-- answer:end -->

---

<!-- quiz-section: id=D score=20 -->
## D. `global` / `nonlocal`、修改与重绑（20 分）

<!-- quiz-question: id=D1 score=10 -->
### D1（10 分）

预测下面五行输出，并画出“模块名字—旧列表—新列表”的关系变化：

~~~python
audit_events = ["initial"]


def reset(new_events):
    global audit_events
    previous = audit_events
    previous.append("before-reset")
    audit_events = list(new_events)
    return previous, audit_events


old, current = reset(("replacement",))

print(old)
print(current)
print(old is audit_events)
print(current is audit_events)
print(audit_events)
~~~

说明每一步到底是读取名字、创建/绑定局部别名、原地修改旧对象，还是重新绑定模块名字。
同时回答：

1. `global audit_events` 改变的是哪个绑定目标，它是否改变列表对象的类型、身份或可变性？
2. 为什么 `previous.append(...)` 本身不需要 `global previous`？
3. 如果同一函数既读取又重新绑定模块名，`global` 声明为什么对整个代码块的该名字生效，而不是只对赋值语句下一行生效？

<!-- answer:start -->
<!-- answer:end -->

<!-- quiz-question: id=D2 score=10 -->
### D2（10 分）

不运行代码，写出两行精确输出：

~~~python
module_label = "module"


def outer():
    label = "outer"
    events = []

    def middle():
        label = "middle"

        def change():
            nonlocal label
            events.append(label)
            label = "changed"

        change()
        return label

    return label, middle(), events


print(outer())
print(module_label)
~~~

然后分别追踪 `change()` 中：

- 第一次读取 `label` 时采用哪个绑定；
- `label = "changed"` 最终重新绑定哪个词法作用域中的名字；
- `events` 的查找路径、命中层级和列表对象变化；
- 为什么 `events.append(...)` 不需要 `nonlocal events`；
- 为什么 `outer` 自己的 `label` 与模块层 `module_label` 都不被这次
  `nonlocal` 重新绑定。

答案应明确“最近的外层函数绑定”是词法嵌套关系，不是任意调用者的局部状态。

<!-- answer:start -->
<!-- answer:end -->

---

<!-- quiz-section: id=E score=14 -->
## E. 闭包入口与命名空间观察（14 分）

<!-- quiz-question: id=E1 score=8 -->
### E1（8 分）

预测三行精确输出：

~~~python
def make_reader(label):
    state = [label]

    def read():
        return state

    return read, state


reader1, external1 = make_reader("menu")
reader2, external2 = make_reader("dialog")

external1.append("updated")

print(reader1() is external1, reader1())
print(reader2() is external2, reader2())
print(reader1() is reader2(), external1 is external2)
~~~

请结合名字、绑定和对象身份解释：

1. `reader1` 为什么在 `make_reader` 调用已经返回后仍能读取 `state`；
2. 闭包是否复制、浅拷贝或深拷贝了列表对象；
3. `external1.append(...)` 为什么会出现在 `reader1()` 的结果中；
4. 两次独立的外层调用之间，哪些函数对象、enclosing 绑定和列表对象彼此独立。

本题只考 free name 与闭包入口，不要求讨论晚绑定或闭包内部存储实现。

<!-- answer:start -->
<!-- answer:end -->

<!-- quiz-question: id=E2 score=6 -->
### E2（6 分）

以下结果以本卷声明的 Python 3.14.5 环境为准。预测精确输出：

~~~python
DEFAULT_LOCALE = "en-US"


def observe(locale):
    key = "menu.start"
    local_view = locals()
    global_view = globals()
    later = "bound later"
    return (
        tuple(
            sorted(
                name
                for name in ("locale", "key", "later")
                if name in local_view
            )
        ),
        "DEFAULT_LOCALE" in global_view,
        "len" in global_view,
        len(("menu", "dialog")),
    )


print(observe("ja-JP"))
~~~

然后说明：

1. 调用 `locals()` 的那个时点，三个候选名字中哪些已经具有局部绑定；
2. `later` 即使会被归类为局部名字，为什么该次运行期观察仍可能没有它；
3. `"len" in global_view` 与随后成功调用 `len(...)` 为什么不矛盾；
4. 这一次观察可以证明什么，不能据此把 `locals()` / `globals()` 提升成什么样的通用任意写回合同。

不要通过修改命名空间映射来作答；本题考查的是有限观察及证据强度。

<!-- answer:start -->
<!-- answer:end -->

---

<!-- quiz-section: id=F score=14 -->
## F. 本地化配置工程应用（14 分）

<!-- quiz-question: id=F1 score=14 -->
### F1（14 分）

某个本地化模块最初把配置读取和审计副作用都隐藏在函数内部：

~~~python
DEFAULT_LOCALE = "en-US"
audit_events = []


def build_label(key):
    normalized_key = key.strip().lower()
    audit_events.append(f"built:{normalized_key}")
    return f"{DEFAULT_LOCALE}:{normalized_key}"
~~~

请设计一个仅使用 C17 已学内容的显式依赖版本，满足以下合同：

1. 核心函数命名为 `build_entry(key, locale)`；
2. 函数内部不读取 `DEFAULT_LOCALE`，不修改模块层或 enclosing 层列表，也不使用
   `global` / `nonlocal`；
3. 它把 `key` 执行 `strip().lower()` 后，返回普通字典：

   ~~~python answer-template
   {
       "label": f"{locale}:{normalized_key}",
       "event": f"built:{normalized_key}",
   }
   ~~~

4. 再写一段调用方代码：显式把 `DEFAULT_LOCALE` 传给函数，由调用方自己的
   `events` 列表收集返回的事件，并打印 label 与列表；
5. 对输入 `" Menu.Start "`，调用方最终应能观察到：

   ~~~text
   en-US:menu.start
   ['built:menu.start']
   ~~~

除代码外，还要解释：

- 核心函数中的 `key`、`locale`、`normalized_key` 和返回字典属于哪些本次调用绑定；
- `DEFAULT_LOCALE` 在调用点从哪一层读取，为什么核心函数本身不需要
  `global`；
- 显式依赖如何让配置选择、测试输入和副作用归属更可见；
- 为什么这不等于“所有模块常量都错误”：模块常量可作为受控边界配置，但大写命名是约定，模块名字仍可被重新绑定。

评分关注：可运行且符合合同的代码 7 分；名字/对象/作用域解释 4 分；工程边界说明 3 分。

<!-- answer:start -->
<!-- answer:end -->
