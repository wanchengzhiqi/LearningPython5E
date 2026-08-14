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

   ```python no-compile
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

   ```python no-compile
   records.append("x")
   ```

   只是读取名字 `records` 得到列表，再修改列表对象；它不会因为列表可变就把 `records` 自动判定为当前函数的局部名字。

   反之：

   ```python no-compile
   records = []
   ```

   是对普通名字 `records` 的绑定操作，即使右侧对象是可变列表，也应按名字绑定规则判断作用域。

   因此准确表述应是：**对象可变性决定某些对象能否被原地修改，但不决定裸名字的作用域分类。**

3. **错误。**

   ```python no-compile
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

   ```python no-compile
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

精确输出为：

```text
('module shadow', 2)
```

### 1. 裸名字 `len` 在哪里停止

在 `report()` 内：

```python no-compile
return len, builtins.len(entries)
```

第一个 `len` 是普通裸名字读取。

查找过程为：

```text
L：report 的局部作用域没有 len
E：没有外层函数作用域
G：当前模块存在 len ──> "module shadow"   ← 命中
B：不再继续
```

因此第一个返回值是字符串：

```python
"module shadow"
```

名字解析采用较近的绑定优先；在模块 G 层已经找到同名绑定后，就不会为了寻找“可调用的那个 `len`”而继续到 B 层。Python 不会根据对象类型是否合适来跳过已经成功解析出的绑定。

### 2. `builtins.len(entries)` 的精确机制

它**不等于**“让裸名字 `len` 绕过 G 层继续执行 B 层查找”。

这个表达式应拆成两步：

第一步，读取裸名字：

```python
builtins
```

`import builtins` 已在当前模块的全局命名空间中建立名字 `builtins` 到该模块对象的绑定，所以这里通过普通名字解析取得 `builtins` 模块对象。

第二步：

```python
builtins.len
```

点号后的 `len` 是对已经取得的模块对象执行**属性访问**，不是再次对裸名字 `len` 做 LEGB 查找。

因此：

```python
builtins.len(entries)
```

取得 `builtins` 模块的 `len` 属性，即内置长度函数，并对：

```python
("menu.start", "menu.quit")
```

求长度，得到 `2`。

### 3. 本题的 global 属于哪个命名空间

本题所说的模块 global 是**定义这些代码的当前模块自己的全局命名空间**。

其中至少包含：

```text
builtins ──> builtins 模块对象
len      ──> "module shadow"
report   ──> 函数对象
```

它不是跨整个 Python 程序、跨所有模块共享的“统一全局名字池”。其他模块各自拥有自己的模块全局命名空间；跨模块若共享对象，是通过导入和引用形成的对象关系，而不是所有模块天然共用同一个 global 命名空间。

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

全部精确输出为：

```text
error False UnboundLocalError
error True UnboundLocalError
module 10
events ['start:False', 'start:True']
```

### 1. 为什么 `counter` 在整个 `update` 中都是局部名字

函数体中存在：

```python
counter = 20
```

它是对普通名字 `counter` 的绑定操作，并且函数中没有：

```python
global counter
```

或：

```python no-compile
nonlocal counter
```

因此 Python 根据整个 `update` 代码块进行名字分类时，会把 `counter` 判定为该函数的局部名字。这个分类对整个函数代码块生效，不会因为赋值语句写在 `if flag:` 分支中，就只在 `flag is True` 时才把名字视为局部。

模块中虽然已有：

```python
counter = 10
```

但那是另一个命名空间中的同名绑定。

---

### 2. 两次调用首先失败在哪里，为什么都到不了条件分支

每次调用 `update(flag)` 时，第一条函数体语句都是：

```python
events.append(f"start:{flag}")
```

它会先成功执行。

下一条是：

```python
before = counter
```

赋值语句会先求值右侧表达式 `counter`。此处 `counter` 已经被静态分类为当前 `update` 调用的局部名字，但直到这一时刻，本次调用还没有执行过：

```python
counter = 20
```

所以局部 `counter` 尚未绑定值。

因此异常发生在：

```python no-compile
before = counter
         ^^^^^^^
```

准确说，是右侧局部名字 `counter` 的读取处引发：

```text
UnboundLocalError
```

这发生在：

```python no-compile
if flag:
```

之前，所以无论实参是 `False` 还是 `True`，两次调用都根本无法执行到条件判断，更不可能执行分支里的 `counter = 20`。

外层表达式：

```python
print("return", flag, update(flag))
```

在真正调用 `print` 前必须先求值所有实参；`update(flag)` 求值时已经抛出异常，因此没有任何以 `return` 开头的行被打印。

异常被相应的 `except` 捕获，于是输出：

```text
error False UnboundLocalError
error True UnboundLocalError
```

---

### 3. 异常前已经发生的副作用与没有执行的语句

#### `flag == False` 的第一次调用

已经完成：

```python
events.append("start:False")
```

所以模块名字 `events` 所指的列表从：

```python
[]
```

变为：

```python
["start:False"]
```

随后在 `before = counter` 的右侧读取处异常。

没有执行：

```python no-compile
before = ...
if flag:
    ...
events.append("done")
return before, counter
```

其中 `before` 也没有成功建立绑定，因为赋值语句右侧求值已经失败。

#### `flag == True` 的第二次调用

先成功执行：

```python
events.append("start:True")
```

同一个模块列表进一步变成：

```python
["start:False", "start:True"]
```

然后同样在：

```python
before = counter
```

处抛出 `UnboundLocalError`。

因此即使实参为 `True`，也完全没有机会执行：

```python
counter = 20
```

以及后续 `"done"` 追加和 `return`。

异常不会自动回滚异常发生前已经成功完成的列表修改。

---

### 4. 为什么模块 `counter` 与 `events` 最终状态不同

模块全局名字：

```python
counter
```

始终仍绑定到整数 `10`。函数中的 `counter = 20` 本来就是局部绑定目标，而且两次调用都还没执行到它，所以模块级 `counter` 从未被重新绑定。

因此：

```text
module 10
```

而 `events` 的情况不同。函数中没有给普通名字 `events` 赋值；表达式：

```python
events.append(...)
```

读取模块全局名字 `events` 找到同一个列表对象，再调用列表方法原地修改该对象。

两次异常前都成功完成了一次追加，所以最终模块列表为：

```python
["start:False", "start:True"]
```

故最后输出：

```text
events ['start:False', 'start:True']
```

这正体现了：

```text
函数异常退出
≠
此前已经完成的对象修改自动回滚
```

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

精确输出为：

```text
True ['scan']
False UnboundLocalError
['module']
```

### 1. 为什么两个控制流路径中 `result` 都属于局部名字

函数体中存在：

```python
result = []
```

这是对普通名字 `result` 的绑定操作，并且没有 `global result` 或 `nonlocal result` 声明。

因此编译/作用域分析针对整个 `collect` 代码块，把 `result` 统一分类为当前函数的局部名字。该分类由代码块文本决定，不会根据某次调用的 `flag` 值重新决定。

也就是说：

```text
flag == True  → result 是局部名字
flag == False → result 仍然是局部名字
```

区别只在于运行时是否真的执行过建立局部绑定的语句。

---

### 2. `True` 路径与 `False` 路径的运行期绑定状态

#### `collect(True)`

执行：

```python
if flag:
    result = []
```

条件成立，于是先创建新列表对象，并在本次调用的局部命名空间中建立：

```text
result ──> []
```

接着：

```python
result.append("scan")
```

读取已经存在的局部绑定，找到这个列表并原地追加，得到：

```python
["scan"]
```

随后返回该列表，所以外层打印：

```text
True ['scan']
```

#### `collect(False)`

条件不成立，因此：

```python
result = []
```

没有执行。

然而 `result` 仍然已经被分类为当前函数的局部名字。执行到：

```python
result.append("scan")
```

时，Python 首先必须读取局部名字 `result` 才能进行属性访问 `.append`；但本次调用尚未建立这个局部绑定，因此在读取 `result` 时抛出：

```text
UnboundLocalError
```

外层捕获后输出：

```text
False UnboundLocalError
```

---

### 3. 为什么模块同名列表不能挽救 `False` 路径

模块中确实有：

```python
result = ["module"]
```

但当前 `collect` 代码块已经把 `result` 确定为局部名字。运行时遇到“局部名字尚未绑定”时，不会把它当作一次普通的 L 层未命中然后退回模块 G 层。

因此模块 `result` 不会成为后备值。

最终模块名字仍绑定到原列表：

```python
["module"]
```

所以最后：

```python
print(result)
```

输出：

```text
['module']
```

---

### 4. 为什么“列表可变”既不能决定分类，也不能保证方法调用成功

对象可变性与名字作用域分类是两个问题。

`result = []` 是否使 `result` 成为局部名字，关键是它是一个**普通名字绑定目标**，而不是因为列表是可变类型。

反过来：

```python
result.append("scan")
```

的确是要修改列表对象，而不是重新绑定名字 `result`；但在调用 `.append` 之前，程序必须先成功读取名字 `result` 得到一个列表对象。

在 `False` 路径中，失败正发生在这个前置步骤：

```text
读取局部 result
→ 尚未绑定
→ UnboundLocalError
→ 根本没有机会取得列表对象，更没有机会调用 append
```

所以“对象可变”既不能决定局部名字分类，也不能保证任何方法调用一定能发生。

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

五行输出依次为：

```text
['initial', 'before-reset']
['replacement']
False
True
['replacement']
```

### 关系变化与执行轨迹

先把初始模块列表记作 **旧列表 L1**：

```text
模块全局：
audit_events ──> L1 ["initial"]
```

调用：

```python
reset(("replacement",))
```

后进入函数。

#### 第一步：`global audit_events`

```python
global audit_events
```

声明当前 `reset` 代码块中的裸名字 `audit_events` 使用定义模块的全局绑定。它本身不会创建列表、复制列表，也不会修改列表。

#### 第二步：`previous = audit_events`

右侧读取全局名字：

```text
audit_events ──> L1
```

然后在本次 `reset` 调用中建立局部名字：

```text
previous ──> L1
```

此时：

```text
模块 audit_events ─┐
                   ├──> L1 ["initial"]
局部 previous     ─┘
```

`previous` 是旧列表的局部别名，并不是副本。

#### 第三步：`previous.append("before-reset")`

先读取局部名字 `previous` 得到 L1，然后调用其 `append` 方法。

这是**原地修改旧列表对象**：

```text
L1 ["initial"]
        ↓
L1 ["initial", "before-reset"]
```

两个名字仍然都指向 L1。

#### 第四步：`audit_events = list(new_events)`

先求值：

```python
list(new_events)
```

根据传入的元组：

```python
("replacement",)
```

创建一个新的列表对象 **L2**：

```python
["replacement"]
```

由于本函数声明了：

```python
global audit_events
```

左侧名字 `audit_events` 的绑定目标是模块全局命名空间。因此模块名字从 L1 **重新绑定**到 L2：

```text
局部 previous      ──> L1 ["initial", "before-reset"]
模块 audit_events  ──> L2 ["replacement"]
```

旧列表 L1 没有因为模块名字改绑而消失或自动清空，因为局部 `previous` 仍引用它。

#### 第五步：返回并建立模块名字 `old`、`current`

```python no-compile
return previous, audit_events
```

返回：

```text
previous    → L1
audit_events→ L2
```

调用方：

```python
old, current = ...
```

最终形成：

```text
old          ──> L1 ["initial", "before-reset"]
current      ──> L2 ["replacement"]
audit_events ──> L2 ["replacement"]
```

于是：

```python
old is audit_events
```

为：

```text
False
```

而：

```python
current is audit_events
```

为：

```text
True
```

---

### 1. `global audit_events` 到底改变什么

它改变的是**当前函数代码块中名字 `audit_events` 的解析与绑定目标**，使该名字指向定义 `reset` 的模块全局命名空间中的绑定。

它不改变 L1 或 L2 的：

- 类型；
- 对象身份；
- 可变性。

列表仍然是普通列表对象。

---

### 2. 为什么 `previous.append(...)` 不需要 `global previous`

`previous` 本来就是 `reset` 本次调用中的局部名字：

```python
previous = audit_events
```

已经合法建立了局部绑定。

随后：

```python
previous.append(...)
```

只是读取这个局部名字并修改它所指的列表对象，没有试图把 `previous` 重新绑定到模块全局命名空间，因此既不需要、也不应该声明 `global previous`。

---

### 3. 为什么 `global` 对整个代码块生效

`global audit_events` 是针对当前代码块的名字分类声明，不是“只修饰下面一条赋值语句”。

因此同一个 `reset` 函数中，对裸名字 `audit_events` 的读取：

```python
previous = audit_events
```

和后面的绑定：

```python
audit_events = list(new_events)
```

都使用模块全局绑定。

这也是为什么不能把它理解成运行到某一行时才临时切换作用域；其作用范围是整个当前代码块中该名字的解析/绑定规则。

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

两行精确输出是：

```text
('outer', 'changed', ['middle'])
module
```

### 1. `change()` 第一次读取 `label` 时使用哪个绑定

作用域结构为：

```text
模块
└─ outer
   └─ middle
      └─ change
```

名字绑定有：

```text
outer：
label ──> "outer"
events ──> []

middle：
label ──> "middle"
```

`change` 中声明：

```python no-compile
nonlocal label
```

因此它寻找词法上最近的、已有同名绑定的外层函数作用域。

最近的就是 `middle`：

```text
middle.label ──> "middle"
```

所以：

```python
events.append(label)
```

中对 `label` 的第一次读取得到：

```text
"middle"
```

---

### 2. `label = "changed"` 最终重新绑定哪里

同一个 `nonlocal label` 声明使：

```python
label = "changed"
```

不在 `change` 自己的局部命名空间建立 `label`，而是重新绑定最近的外层 `middle.label`：

```text
之前：
middle.label ──> "middle"

之后：
middle.label ──> "changed"
```

因此 `middle()` 最后：

```python no-compile
return label
```

返回：

```text
"changed"
```

---

### 3. `events` 的查找路径和对象变化

`change` 中没有绑定普通名字 `events`。

查找：

```text
L：change 中无 events
E（最近 middle）：middle 中无 events
E（继续 outer）：outer.events ──> 列表对象 []  ← 命中
```

于是：

```python
events.append(label)
```

先找到 `outer` 创建的列表对象，然后把当时读取到的：

```text
"middle"
```

追加进去。

列表对象从：

```python
[]
```

原地修改为：

```python
["middle"]
```

`events` 这个外层名字本身没有重新绑定。

---

### 4. 为什么 `events.append(...)` 不需要 `nonlocal events`

`nonlocal` 在内层函数要**重新绑定外层普通名字**时才需要。

这里：

```python
events.append(...)
```

只是读取外层名字 `events`，取得列表对象，然后调用其方法原地修改该列表。

没有：

```python
events = ...
```

所以不需要 `nonlocal events`。

如果 `change` 的意图是执行：

```python
events = []
```

并让 `outer.events` 指向新列表，那才需要：

```python no-compile
nonlocal events
```

---

### 5. 为什么 `outer.label` 和模块 `module_label` 都不被改绑

`nonlocal label` 选择最近的匹配外层函数绑定。`middle` 已经有：

```python
label = "middle"
```

因此查找到这里就停止，不会继续越过它去重新绑定：

```text
outer.label ──> "outer"
```

所以 `outer` 最终返回元组第一项仍是：

```text
"outer"
```

此外模块名字叫：

```python
module_label
```

它甚至不是同一个标识符 `label`。并且 `nonlocal` 的目标本来就是外层**函数**作用域，不是模块全局作用域。

所以模块：

```python
module_label = "module"
```

完全不受影响，第二行输出：

```text
module
```

本题中的“最近外层”严格由源码词法嵌套确定，不是沿运行时调用栈任意寻找某个调用者的局部状态。

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

三行精确输出为：

```text
True ['menu', 'updated']
True ['dialog']
False False
```

### 1. 为什么外层调用返回后 `reader1` 仍能读取 `state`

第一次：

```python
reader1, external1 = make_reader("menu")
```

调用时，`make_reader` 的本次局部环境中建立：

```text
label ──> "menu"
state ──> 列表对象 L1 ["menu"]
```

内部函数：

```python
def read():
    return state
```

没有在自身代码块中绑定 `state`，所以 `state` 是从外层函数作用域读取的 free name。

当外层 `make_reader` 返回后，返回的 `read` 函数仍保留对其执行所需要的那个外层 `state` 绑定的访问能力。因此：

```python
reader1()
```

仍能取得 L1。

这里应描述成“闭包使内部函数继续访问所需外层绑定”，而不是说整个调用方命名空间被复制了。

---

### 2. 闭包是否复制了列表

没有。

本题没有浅拷贝，也没有深拷贝列表。

第一次调用结束时：

```text
reader1 访问到的 state ─┐
                         ├──> L1 ["menu"]
external1              ─┘
```

`return read, state` 中的第二项直接返回同一个列表对象。因此：

```python
reader1() is external1
```

为：

```text
True
```

同理，第二次调用得到另一个列表对象 L2：

```text
reader2 访问到的 state ─┐
                         ├──> L2 ["dialog"]
external2              ─┘
```

所以：

```python
reader2() is external2
```

同样为 `True`。

---

### 3. 为什么 `external1.append(...)` 会反映在 `reader1()` 中

执行：

```python
external1.append("updated")
```

读取模块名字 `external1` 得到 L1，然后原地修改 L1：

```text
L1 ["menu"]
     ↓
L1 ["menu", "updated"]
```

因为 `reader1()` 读取到的仍是同一个 L1，而不是列表副本，所以之后：

```python
reader1()
```

返回：

```python
["menu", "updated"]
```

第一行因此为：

```text
True ['menu', 'updated']
```

---

### 4. 两次外层调用之间哪些东西彼此独立

两次：

```python
make_reader("menu")
make_reader("dialog")
```

是两次独立的函数调用，因此各自拥有独立的运行期外层绑定环境。

可以概括为：

```text
第一次调用：
label₁    ──> "menu"
state₁    ──> L1 ["menu", "updated"]
reader1   ──> 第一次调用创建的 read 函数对象
external1 ──> L1

第二次调用：
label₂    ──> "dialog"
state₂    ──> L2 ["dialog"]
reader2   ──> 第二次调用创建的 read 函数对象
external2 ──> L2
```

因此：

- `reader1` 与 `reader2` 是不同函数对象；
- 两次外层调用的 `state` 绑定彼此独立；
- L1 与 L2 是不同列表对象；
- `external1 is external2` 为 `False`；
- `reader1() is reader2()` 也为 `False`。

所以第三行输出：

```text
False False
```

本题只需要闭包入口层面的结论：内部函数保留对所需外层绑定的访问；不需要假定或讨论更底层的存储实现。

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

精确输出为：

```text
(('key', 'locale'), True, False, 2)
```

### 1. 调用 `locals()` 时哪些候选名字已经绑定

进入：

```python
observe("ja-JP")
```

时，形参局部名字：

```text
locale ──> "ja-JP"
```

已经建立。

随后：

```python
key = "menu.start"
```

建立：

```text
key ──> "menu.start"
```

接下来执行：

```python
local_view = locals()
```

赋值语句必须先求值右侧 `locals()`，然后才能把返回对象绑定给左侧 `local_view`。

因此就在这一次 `locals()` 调用发生的时点，题目候选：

```text
locale
key
later
```

中已有实际局部绑定的是：

```text
locale
key
```

`later` 尚未执行到：

```python
later = "bound later"
```

所以此时还没有运行期值绑定。

因此后面在保存的 `local_view` 中筛选：

```python
("locale", "key", "later")
```

只会找到 `locale` 和 `key`；排序后得到：

```python
("key", "locale")
```

---

### 2. 为什么 `later` 已经是局部名字，但快照里仍可能没有它

函数体中存在：

```python
later = "bound later"
```

因此从函数代码块的名字分类角度，`later` 是 `observe` 的局部名字。

但：

```text
“这个名字被静态分类为局部”
```

与：

```text
“执行到当前时点已经给它建立了运行期值绑定”
```

不是一回事。

第一次调用 `locals()` 时，执行流程还没有到 `later = ...`，所以它虽然属于该函数的局部名字集合，但当前没有实际值绑定；`locals()` 此时观察到的是当前运行期绑定，而不是“未来会有哪些局部名字”的静态清单。

---

### 3. `"len" in global_view` 为 False 与成功调用 `len(...)` 不矛盾

`global_view = globals()` 得到当前模块的全局命名空间映射。

本题模块代码没有建立模块级名字：

```python
len
```

所以：

```python
"len" in global_view
```

结果是：

```text
False
```

但最后：

```python
len(("menu", "dialog"))
```

是普通裸名字读取。

在函数 L 层、外层函数 E 层和模块 G 层都没有找到 `len` 后，名字解析继续到 builtins 层，在那里找到内置函数 `len`，因此调用成功并返回：

```text
2
```

所以两者分别回答不同问题：

```text
"len" in global_view
→ 当前模块全局命名空间是否有 len 绑定？否

len(...)
→ 按名字解析继续到 builtins 后能否找到 len？能
```

没有矛盾。

---

### 4. 这次观察能证明什么，不能证明什么

本题的运行期观察可以证明：

1. 调用 `locals()` 的那个时点，快照中存在 `locale`、`key` 的局部绑定；
2. 同一时点尚没有 `later` 的运行期值绑定；
3. 模块全局命名空间中存在 `DEFAULT_LOCALE`；
4. 模块全局命名空间中没有名为 `len` 的绑定；
5. `len` 仍可通过更外层的 builtins 环境被解析。

但是不能把它扩张成：

> “函数中的 `locals()` 返回的映射就是函数实际局部存储，因此随意修改该字典就能可靠改变局部名字。”

在 Python 3.14.5 的普通函数这类优化作用域中，`locals()` 返回的是当前局部绑定的一个新字典快照；对该字典做名字绑定修改不会写回实际局部变量，而且后续局部绑定变化也不会自动更新先前保存的快照。

同样，虽然 `globals()` 返回模块全局命名空间映射，本题也只是在做观察；不能据此把动态改写命名空间字典当成普通业务代码的“动态作用域”技巧，更不能根据一个名字出现在 `locals()` / `globals()` 中就推断相应对象在哪里创建、由哪个作用域独占。

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

可以按合同改写为：

```python
DEFAULT_LOCALE = "en-US"


def build_entry(key, locale):
    normalized_key = key.strip().lower()

    return {
        "label": f"{locale}:{normalized_key}",
        "event": f"built:{normalized_key}",
    }


events = []

entry = build_entry(
    " Menu.Start ",
    DEFAULT_LOCALE,
)

events.append(entry["event"])

print(entry["label"])
print(events)
```

精确输出：

```text
en-US:menu.start
['built:menu.start']
```

### 1. 核心函数中的名字绑定

调用：

```python
build_entry(" Menu.Start ", DEFAULT_LOCALE)
```

时，`build_entry` 这一次调用中：

```text
key
locale
normalized_key
```

都属于当前函数调用的局部绑定。

更具体地说：

```text
key
──> 实参表达式 " Menu.Start " 求值得到的字符串对象

locale
──> 调用点读取 DEFAULT_LOCALE 得到的字符串对象 "en-US"

normalized_key
──> key.strip().lower() 计算结果 "menu.start"
```

这里的形参绑定不是复制调用方命名空间。它只是在本次函数调用的局部命名空间中建立形参名字到相应实参对象的绑定。

函数随后创建并返回一个普通字典对象：

```python
{
    "label": "en-US:menu.start",
    "event": "built:menu.start",
}
```

准确地说，应当称：

> 本次函数调用中的局部名字和返回对象之间存在相应绑定/引用关系。

不应把这个返回字典称作“只能属于局部作用域的局部对象”。返回后，调用方名字 `entry` 会引用它。

---

### 2. `DEFAULT_LOCALE` 在哪里读取，为什么核心函数不需要 `global`

本例调用代码位于模块顶层：

```python
entry = build_entry(
    " Menu.Start ",
    DEFAULT_LOCALE,
)
```

因此实参表达式 `DEFAULT_LOCALE` 在调用点从当前模块的全局命名空间中读取，得到：

```text
"en-US"
```

该对象随后作为第二个实参传给 `build_entry`，在函数内部绑定给局部形参名字：

```text
locale
```

`build_entry` 的函数体中根本没有读取名字：

```python
DEFAULT_LOCALE
```

它只使用自己的局部形参 `locale`。

因此核心函数既不依赖模块级 `DEFAULT_LOCALE` 名字，也没有任何重新绑定模块全局名字的需求，自然无需 `global`。

实际上，即使函数只是读取一个模块全局名字，通常也不需要 `global`；`global` 的关键作用是改变当前代码块中相应名字的解析/绑定目标，而不是声明“允许读取全局数据”。

---

### 3. 显式依赖为何让配置、测试输入和副作用更可见

原函数：

```python
def build_label(key):
    ...
    audit_events.append(...)
    return f"{DEFAULT_LOCALE}:..."
```

隐藏了两项外部依赖：

1. 配置来自模块名字 `DEFAULT_LOCALE`；
2. 函数会原地修改模块共享列表 `audit_events`。

改写后：

```python no-compile
def build_entry(key, locale):
```

核心计算所需的语言配置通过参数 `locale` 显式进入函数。

这样测试可以直接写：

```python
build_entry(" Menu.Start ", "en-US")
build_entry(" Menu.Start ", "ja-JP")
```

而无需先修改模块全局配置。

同时，函数不再偷偷修改共享列表；它把待记录事件作为普通返回数据：

```python no-compile
"event": "built:menu.start"
```

交给调用方明确决定：

```python
events.append(entry["event"])
```

于是副作用归属从“核心函数隐式修改外部状态”变为：

```text
核心函数：
显式输入 → 计算 → 返回数据

调用方：
选择配置 → 调用 → 决定是否把 event 写入自己的 events
```

这使依赖来源、测试输入以及谁负责修改列表都更容易从代码表面看出。

---

### 4. 为什么这不表示“所有模块常量都错误”

本题的重构目标是使**会影响一次业务计算结果的配置选择**显式进入核心函数，而不是制定“禁止模块常量”的机械规则。

模块级：

```python
DEFAULT_LOCALE = "en-US"
```

仍然可以作为应用边界处的默认配置。调用方可以合理地从模块全局读取它，再显式传给核心函数：

```python
build_entry(key, DEFAULT_LOCALE)
```

这样既保留了统一默认值，又让核心函数本身不隐藏该依赖。

另外，大写名字：

```python
DEFAULT_LOCALE
```

只是 Python 工程中的“按约定视为常量”的命名习惯，并不是语言层面的不可重新绑定保证。

从 Python 名字绑定语义看，模块名仍然可以以后执行：

```python
DEFAULT_LOCALE = "ja-JP"
```

而重新绑定到其他对象。

所以合理边界是：

```text
模块常量可以作为受控的默认配置/边界配置；
核心业务函数是否显式接收它，应根据依赖可见性、测试性和变化需求判断；
大写命名是工程约定，不会把普通模块名字变成语言层面的只读常量。
```

<!-- answer:end -->

---

## Codex 批改记录（逐题审批，2026-08-10）

### 覆盖账本

下表冻结本轮逐题审批覆盖。原答案的文字、代码、Markdown 标记和作答顺序均保留在
原作答区；本记录只追加审批发现与结论。

| 题号 | 分值 | 原答案位置 | 审批状态 | 发现 | 得分 |
| --- | ---: | --- | --- | --- | ---: |
| A1 | 7 | 行 98–244（正文 99–243） | 已审批 | 五个概念、两层命名空间及对象身份关系完整准确 | 7 |
| A2 | 7 | 行 259–351（正文 260–350） | 已审批 | 四项错误断言均被精确纠正；函数代码块与模块顶层的绑定边界作不扣分补充 | 7 |
| B1 | 9 | 行 392–483（正文 393–482） | 已审批 | 两行输出、LEGB 路径和闭包入口解释准确 | 9 |
| B2 | 9 | 行 508–593（正文 509–592） | 已审批 | 模块遮蔽、builtins 名字解析与属性访问区分准确 | 9 |
| C1 | 10 | 行 638–857（正文 639–856） | 已审批，轻微扣分 | 把“赋值语句已开始但左侧绑定未完成”局部写成该语句没有执行 | 9.75 |
| C2 | 10 | 行 891–1046（正文 892–1045） | 已审批 | 静态局部分类与两条路径的运行期绑定状态准确 | 10 |
| D1 | 10 | 行 1086–1303（正文 1087–1302） | 已审批 | 旧/新列表身份、原地修改和模块名重绑准确 | 10 |
| D2 | 10 | 行 1347–1556（正文 1348–1555） | 已审批 | 最近 enclosing 绑定、共享列表修改及词法边界准确 | 10 |
| E1 | 8 | 行 1597–1766（正文 1598–1765） | 已审批 | 闭包不复制列表，两次外层调用相互独立 | 8 |
| E2 | 6 | 行 1808–1985（正文 1809–1984） | 已审批，轻微扣分 | 本例没有 E 层，实际读取路径应为 L → G → B | 5.75 |
| F1 | 14 | 行 2041–2266（正文 2042–2265） | 已审批，轻微扣分 | 返回字典没有先绑定给函数局部名字，原表述略混淆名字绑定与对象创建 | 13.75 |

审批游标：`F1`，共 `11 / 11` 题完成，无遗漏。

### A1 — 7 / 7

模块名字 `catalog`、`inspect`、`returned` 与本次调用局部名字 `resource`、
`local_alias` 的绑定均列全；名字、绑定、命名空间、作用域和名字查找五者分离
准确。`returned is catalog` 为 `True`，形参和局部别名只建立新绑定，不复制
调用方命名空间或字典对象。

### A2 — 7 / 7

四条断言均正确判错并修正：裸名字读取、简单名字绑定目标与对象原地修改不是同一
机制；`global` 指向当前代码块所属模块的全局绑定，`nonlocal` 按词法嵌套选择
最近的已有外层函数绑定，二者都不改变对象类型、身份或可变性。

不扣分精度补充：“普通名字赋值默认绑定当前局部名字”在本题应明确理解为函数代码块
语境；模块顶层的普通名字赋值建立模块全局绑定。该补充不扩张到本章未考查的其它
代码块规则。

### B1 — 9 / 9

精确输出为 `('enclosing', 2)` 和 `changed global`；`label` 在 E 层命中，
`len` 在 B 层命中。返回的内部函数在外层调用结束后仍能访问执行所需的 enclosing
绑定；模块 `label` 后续重新绑定只改变 G 层，不影响已经在 E 层解析的名字。

### B2 — 9 / 9

输出 `('module shadow', 2)` 正确。裸名字 `len` 在 G 层命中后停止，Python
不会因该对象不可调用而继续到 B 层。`builtins.len` 则是先解析模块全局名字
`builtins`，再对所得模块对象进行属性访问，并非让裸名字 `len` 绕过遮蔽。

### C1 — 9.75 / 10

四行输出、局部名字分类、两次异常位置、异常前两次列表追加、模块 `counter` 保持
`10` 以及异常不回滚既有副作用均正确。

扣 `0.25` 分：答案在“没有执行”的列表中包含 `before = counter`，但该赋值语句
实际上已经进入并开始执行；失败发生在求值右侧局部名字 `counter` 时。没有完成的
是左侧 `before` 的绑定；真正完全未执行的是后续 `if`、`events.append("done")`
和 `return`。答案其它位置已经定位到右侧读取，因此这里只作轻微扣分。

### C2 — 10 / 10

输出 `True ['scan']`、`False UnboundLocalError`、`['module']` 全部正确。
同一个函数代码块中 `result` 对两条路径都被分类为局部名字；`True` 路径先建立
局部绑定，`False` 路径读取尚未绑定的局部名字时失败且不会退回模块同名绑定。
对象可变性既不决定名字分类，也不能绕过调用方法之前的名字读取。

### D1 — 10 / 10

五行输出和 L1/L2 对象图完全正确。`previous` 是指向旧列表 L1 的局部别名，
`append` 原地修改 L1；`global audit_events` 使后续简单赋值重新绑定模块名字
到新列表 L2，但不改变任何列表对象的类型、身份或可变性。该声明对整个函数代码块中
相应名字的读取和绑定生效。

### D2 — 10 / 10

输出 `('outer', 'changed', ['middle'])` 与 `module` 正确。`nonlocal label`
命中词法上最近的 `middle.label`；`events` 经过两个 enclosing 层找到
`outer.events`，随后只原地修改列表。答案准确排除了任意运行期调用者和模块全局
作为 `nonlocal` 目标的错误模型。

### E1 — 8 / 8

三行输出、对象身份和两次独立外层调用的关系均正确。闭包保留对执行所需外层
`state` 绑定的访问，没有复制、浅拷贝或深拷贝列表；`external1` 修改的正是
`reader1()` 返回的同一列表。两次调用分别创建不同内部函数对象、enclosing 绑定
环境和列表对象。

### E2 — 5.75 / 6

输出 `(('key', 'locale'), True, False, 2)` 正确；静态局部分类、调用
`locals()` 时的运行期绑定、保存快照中没有后来绑定的 `later`，以及
`globals()` 不包含 builtins 名字的解释主体准确。

扣 `0.25` 分：`observe` 直接定义在模块层，本例不存在 enclosing 函数作用域，
所以 `len` 的实际查找路径是 L → G → B，而不是“L、E、G 都未命中”。B 是最终
命中的 builtins 层，不应描述成一个实际存在的外层函数环境。

不重复扣分的边界补充：Python 3.14 优化函数中的 `locals()` 返回当前绑定的新字典
快照，不能作为可靠写回接口；`globals()` 返回实际模块全局命名空间映射，写入它
可以影响模块绑定，但这仍不是动态作用域，也不应被提升为可对任意作用域通用写回的
业务接口。

### F1 — 13.75 / 14

可运行代码完全满足合同：核心函数只使用显式参数，返回普通字典，不读取模块配置、
不修改外部列表，也不使用 `global` / `nonlocal`；调用方显式选择默认配置并拥有
事件列表，精确输出符合题面。显式依赖、可测试性、副作用归属和模块常量约定的工程
说明也准确。

扣 `0.25` 分：答案称“本次函数调用中的局部名字和返回对象之间存在相应绑定/引用
关系”，但该字典字面量没有在 `build_entry` 中绑定给任何局部名字。它是在求值
`return` 表达式时创建并直接交给调用者的对象；正常返回后，调用方名字 `entry`
才绑定该字典。作用域分类适用于名字，不是对象的“归属”属性。

### 结构与客观验证记录

使用环境：

```text
CPython 3.14.5
D:\MySoftwareDownload\PythonPractice\LearningPython5E\.venv-py314\Scripts\python.exe
```

针对性运行覆盖 A1、B1、B2、C1、C2、D1、D2、E1、E2 和 F1：所有精确输出、
异常类型、异常前副作用、最终模块状态和对象身份均与以上审批一致。A2 依据语言规则
逐项审查。全卷共有 `6` 个分区、`11` 道题、`11` 个非空原作答区、零个
`QUIZ_FILL` 占位符。

为保留原作答内容并完成结构验证，本轮只给 `16` 个不能脱离上下文独立编译的代码
开栏增加 `no-compile` 元数据，并清除文本围栏中 `3` 个空白行的行尾空格；没有
改动任何答案文字、代码字符或作答顺序，这些纯格式调整不计入得分。

### 分区与总分复核

| 分区 | 满分 | 得分 |
| --- | ---: | ---: |
| A | 14 | 14 |
| B | 18 | 18 |
| C | 20 | 19.75 |
| D | 20 | 20 |
| E | 14 | 13.75 |
| F | 14 | 13.75 |
| **总分** | **100** | **99.25** |

建议得分：`99.25 / 100`。三处扣分各为 `0.25`，合计 `0.75`；逐题得分、
分区小计和总分已复核一致。

### 本阶段末评语与能力判断

`C17_Scopes` 阶段测验通过。你已经稳定建立名字、绑定、命名空间、作用域和查找的
分层模型，能够追踪 LEGB、局部名字分类与运行期绑定、`UnboundLocalError`、
`global` / `nonlocal`、重新绑定与原地修改、异常前副作用、闭包共享对象身份和
有限命名空间观察，并能将它们迁移到显式依赖设计。

当前能力继续判断为：**中级入门前段已经稳固，C17 作用域主干达到优秀，能够用名字—
作用域—对象—控制流四层模型审查小型函数状态与配置边界**。本次三处扣分都是精确
表达层面的轻微边界，不构成主干补救缺口；但仍应继续区分语句开始执行与绑定完成、
实际存在的词法层级，以及对象创建与名字绑定。

该结论只证明 C17 的 free name 与最小闭包入口已经掌握，不外推为 C19 的闭包晚绑定、
高阶组合或高级闭包状态设计已经完成。审批与画像同步完成后，生命周期进入
`stage_note`；本章尚未执行阶段末笔记或最终收束。

### 学习画像更新

可复用于 C17 阶段笔记与后续启动模板的稳定证据：

- **稳定强项**：能精确区分名字、绑定、命名空间、作用域与查找；能按真实词法结构
  追踪 LEGB、遮蔽、局部名字分类、运行期是否已绑定和 `UnboundLocalError`。
- **对象与状态模型**：能稳定区分跨作用域重新绑定与共享对象原地修改，追踪
  `global` / `nonlocal` 的绑定目标、异常前副作用、闭包共享对象身份和两次外层
  调用的独立状态。
- **证据与工程迁移**：能限制 `locals()` / `globals()` 观察的证明范围，并用
  显式参数和结构化返回把配置选择与副作用归属移到可见边界。
- **当前精修点**：赋值语句开始执行不等于左侧绑定已经完成；不存在 enclosing 函数
  时不要机械写出 E 层；对象可在 `return` 表达式中创建并返回而从未绑定给函数局部
  名字。继续区分优化函数的 `locals()` 快照与实际模块 `globals()` 映射。
- **水平判断**：中级入门前段继续稳固；C17 建议得分 `99.25 / 100`，作用域主干
  达到优秀，未发现反复核心误区。
- **下一阶段风险**：C18 应把本章名字解析模型迁移到实参与形参绑定、位置/关键字
  参数、默认值、收集/解包与可变默认值；不要把一次成功绑定提升为完整函数行为合同，
  也不要因 C17 成绩优秀而提前合并 C19 的高级闭包主题。
