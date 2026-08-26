<!-- quiz-validator: total=100 -->

# C18 Arguments 阶段测验：调用合同与参数绑定

本卷对应 `P4_Functions_and_Generators / C18_Arguments`，章节角色为
`normal`。课程范围与节奏的唯一权威入口是
`docs/C18_ARGUMENTS_STARTUP_TEMPLATE.md`。

## 冻结命题蓝图

### 考察范围

- 实参表达式求值、调用端装配、签名匹配、局部形参绑定与函数体入口的完整时间线。
- positional-only、positional-or-keyword、var-positional、keyword-only 和
  var-keyword 五类参数，以及缺失、重复、未知和过量输入的失败边界。
- 默认表达式的定义时求值、函数对象保存默认对象、省略实参和显式实参的绑定。
- 可变默认对象的跨调用共享、对象身份、原地修改与按调用创建状态的修复。
- 定义端 `*args` / `**kwargs` 收集与调用端 `*iterable` /
  `**mapping` 解包，包括浅层引用关系、冲突与失败前效果。
- `/` 与 `*` 表达的 API 意图，以及 `inspect.signature()` /
  `Signature.bind()` 的有限证据。
- 用显式参数合同设计一个小型、纯内存的本地化记录接口。

### 明确排除

- 不考高阶函数、lambda、系统闭包晚绑定、递归、`functools.partial` 或系统注解。
- 不考生成器、基准测试、P4 综合陷阱或 C19-C21 的正式内容。
- 不考 `inspect.Parameter` 深入机制、`Signature.bind_partial()`、多组星号的
  复杂交错顺序，或 `None` 也是合法值时的专用 sentinel 设计。
- 不运行或考查 `prompt_template_manager`、SQLite、CRUD、CLI 或 GUI。
- 不按某个 Python 小版本的完整 `TypeError` 文案评分；重点是失败形状、阶段、
  异常类型、函数体入口和已完成效果。

### 分区与分值

| 分区 | 题型与重点 | 题号 | 分值 |
| --- | --- | --- | ---: |
| A | 概念解释与调用时间线 | A1-A2 | 14 |
| B | 参数种类、绑定矩阵与失败边界 | B1-B2 | 18 |
| C | 默认值、对象身份与可变状态 | C1-C2 | 18 |
| D | 定义端收集、调用端解包与部分效果 | D1-D2 | 20 |
| E | 签名观察、绑定记录与证据强度 | E1-E2 | 14 |
| F | 本地化记录 API 工程设计 | F1 | 16 |
| **合计** | **6 个分区，11 题** | **A1-F1** | **100** |

### 稳定题号与评分映射

| 题号 | 分值 | 主要证据 |
| --- | ---: | --- |
| A1 | 7 | 区分实参、形参、局部绑定与对象复制 |
| A2 | 7 | 追踪求值失败、匹配失败和函数体入口 |
| B1 | 10 | 识别五类参数并写出成功绑定结果 |
| B2 | 8 | 分类缺失、重复、未知、过量与 positional-only 失败 |
| C1 | 10 | 追踪默认对象创建时机、身份与跨调用修改 |
| C2 | 8 | 修复可变默认状态并限定显式实参边界 |
| D1 | 10 | 区分收集容器与内部共享对象 |
| D2 | 10 | 追踪解包、关键字冲突和失败前效果 |
| E1 | 8 | 区分 `Signature.bind()` 与实际调用证据 |
| E2 | 6 | 限制签名观察、形状成功和业务合同结论 |
| F1 | 16 | 设计显式、安全且可解释的参数合同 |

难度略高于单点预测的舒适区，重点是组合追踪、阶段定位和证据边界，不引入相邻章节
的新主线。所有运行期结论以 Python 3.14.5 为当前验证环境。

## 作答说明

1. 把答案写在每题对应的 `answer:start` 与 `answer:end` 之间。
2. 预测题应写精确输出；若发生异常，还要说明异常类型、失败阶段、函数体是否进入及
   异常前已经完成的效果。
3. 绑定题应区分“调用端对象已经求值”“调用形状已经装配”“签名匹配成功”和
   “目标函数局部形参已经绑定”。
4. 对象题应区分名字重新绑定、对象原地修改、外层容器和内部共享对象。
5. 可以运行代码辅助验证，但答案仍需给出推理链，不能只粘贴输出。
6. 设计题只需在答题区写代码与合同说明，不要求修改仓库正式脚本。

---

<!-- quiz-section: id=A score=14 -->
## A. 概念解释与调用时间线（14 分）

<!-- quiz-question: id=A1 score=7 -->
### A1（7 分）

阅读代码：

~~~python
shared_options = {"normalize": True}


def prepare_key(key, options):
    local_options = options
    normalized = key.strip().lower()
    return normalized, local_options


result_key, result_options = prepare_key(" Menu.Start ", shared_options)
~~~

完成以下说明：

1. 指出调用点的两个实参表达式、函数定义中的两个形参，以及本次成功调用中建立的
   局部形参绑定。
2. 列出 `prepare_key` 本次调用结束前与题目直接相关的三个局部名字绑定，并说明
   调用者名字 `shared_options` 是否属于该函数的 enclosing 作用域。
3. 判断 `result_options is shared_options`，并精确解释形参绑定是否复制了调用方
   命名空间、字典对象或字典内容。
4. 说明为什么“`options` 是局部形参”不能推出它绑定的字典是“只属于函数局部
   作用域的局部对象”。

<!-- answer:start -->

### 1. 实参表达式、形参与本次调用的局部形参绑定

调用点：

```python
prepare_key(" Menu.Start ", shared_options)
```

有两个实参表达式：

1. 字面量表达式 `" Menu.Start "`；
2. 名字表达式 `shared_options`。

它们先在调用端求值，分别得到：

- 字符串对象 `" Menu.Start "`；
- 模块名字 `shared_options` 当时所绑定的字典对象 `{"normalize": True}`。

函数定义：

```python
def prepare_key(key, options):
```

中的两个形参是 `key` 和 `options`。参数匹配成功后，本次调用建立的局部形参绑定为：

```text
key     -> " Menu.Start "
options -> shared_options 当时所绑定的那个字典对象
```

这里的“绑定”是让本次函数调用的局部名字引用求值得到的对象；既不是复制调用方名字，也不是自动复制对象。

### 2. 本次调用结束前的局部名字与作用域关系

第 1 小问已经给出了两个形参绑定。若按照题目要求“不重复列出所有形参，而列出与后续执行直接相关的三个局部绑定”，可以写为：

```text
options       -> shared_options 所引用的原字典
local_options -> 与 options 相同的原字典
normalized    -> "menu.start"
```

其中：

```python
local_options = options
```

只是新建了一个局部名字 `local_options`，让它成为同一字典对象的别名；没有复制字典。

而：

```python
normalized = key.strip().lower()
```

对字符串处理后，让局部名字 `normalized` 绑定到结果字符串 `"menu.start"`。

若把本次函数帧中的**全部**直接局部名字都列出，则还应包括第 1 小问已经列出的形参 `key`，因此完整集合实际是：

```text
key           -> " Menu.Start "
options       -> 原字典
local_options -> 原字典
normalized    -> "menu.start"
```

调用者名字 `shared_options` **不属于 `prepare_key` 的 enclosing 作用域**。`prepare_key` 定义在模块层；调用者在调用点求值 `shared_options` 后，把所得对象作为实参交给调用机制。Python 使用词法作用域，调用者的局部/全局环境不会因为“调用了某函数”就成为该函数的 E（enclosing）层。

### 3. 对象身份与是否发生复制

结果为：

```python
result_options is shared_options  # True
```

原因是：

```text
shared_options ─────────────┐
                            v
                     {"normalize": True}
                            ^
                            |
本次调用的 options ----------┤
本次调用的 local_options ----┘
```

`prepare_key` 返回的第二项是 `local_options` 所引用的同一个字典对象，因此外部名字 `result_options` 最终也绑定到这个对象。

形参绑定没有复制：

- 调用方命名空间；
- `shared_options` 这个调用方名字；
- 字典对象；
- 字典内部的键和值。

它只是把**已经求值得到的字典对象**绑定给本次调用的局部形参 `options`；随后 `local_options = options` 又创建了另一个指向同一对象的局部绑定。

### 4. 为什么不能推出“局部对象”

“`options` 是局部形参”描述的是**名字绑定所在的局部命名空间**，不是对象的所有权属性。

同一个字典同时可以被：

```text
模块名字 shared_options
局部形参 options
局部名字 local_options
调用结束后的名字 result_options
```

引用。因此准确说法是：

> `options` 是本次 `prepare_key` 调用中的局部名字，它绑定到一个也被函数外部名字引用的字典对象。

不能从名字的局部性推导出“对象只属于函数局部作用域”“对象在函数内部创建”或“对象不存在其他别名”。

<!-- answer:end -->

<!-- quiz-question: id=A2 score=7 -->
### A2（7 分）

预测两段代码各自打印的事件列表，并分别定位失败阶段：

~~~python
events = []


def evaluate_target():
    events.append("target")
    return build_entry


def evaluate(label, value):
    events.append(label)
    return value


def fail_locale():
    events.append("locale:fail")
    raise ValueError("locale unavailable")


def build_entry(key, *, locale):
    events.append("body")
    return f"{locale}:{key}"


try:
    evaluate_target()(
        evaluate("key", "menu.start"),
        locale=fail_locale(),
        unknown=evaluate("unknown", True),
    )
except ValueError:
    events.append("caught:ValueError")

print(events)

events.clear()

try:
    evaluate_target()(
        evaluate("key", "menu.quit"),
        locale=evaluate("locale", "en-US"),
        unknown=evaluate("unknown", True),
    )
except TypeError:
    events.append("caught:TypeError")

print(events)
~~~

对每次调用分别回答：

1. 哪些调用目标或实参表达式完成了求值，哪些没有轮到求值？
2. 是否开始或完成了调用输入装配与签名匹配？
3. `build_entry` 的局部形参绑定和函数帧是否建立，函数体是否进入？
4. 为什么捕获异常不会回滚较早追加到 `events` 的内容？

<!-- answer:start -->

第一段和第二段必须分开追踪，因为它们分别在**实参表达式求值阶段**和**参数匹配阶段**失败。

### 第一段调用

最终打印：

```text
['target', 'key', 'locale:fail', 'caught:ValueError']
```

执行轨迹如下：

1. 先求值调用目标：

   ```python
   evaluate_target()
   ```

   它向 `events` 追加：

   ```text
   "target"
   ```

   并返回函数对象 `build_entry`。

2. 开始从左到右求值实参表达式。第一个位置实参：

   ```python
   evaluate("key", "menu.start")
   ```

   成功执行，追加：

   ```text
   "key"
   ```

   并得到字符串对象 `"menu.start"`。

3. 接着求值关键字 `locale` 的值表达式：

   ```python
   fail_locale()
   ```

   它先追加：

   ```text
   "locale:fail"
   ```

   然后抛出 `ValueError`。

4. 由于求值已经异常中断，后面的：

   ```python
   evaluate("unknown", True)
   ```

   **根本没有轮到求值**，所以 `"unknown"` 不会出现在列表中。

5. 外层 `except ValueError` 捕获异常，再追加：

   ```text
   "caught:ValueError"
   ```

因此，第一段中：

- 调用目标求值已完成；
- 第一个实参表达式已完成；
- `locale` 的值表达式开始执行但以异常结束；
- `unknown` 的值表达式没有执行；
- 完整调用输入没有形成；
- 没有进入针对 `build_entry` 的完整签名匹配；
- 没有建立 `build_entry` 的函数帧和局部形参绑定；
- `build_entry` 函数体没有进入，所以 `"body"` 不会追加。

失败阶段是：

> **实参表达式求值阶段**，具体是在 `fail_locale()` 内抛出 `ValueError`。

---

### 第二段调用

最终打印：

```text
['target', 'key', 'locale', 'unknown', 'caught:TypeError']
```

执行轨迹：

1. `evaluate_target()` 执行，追加：

   ```text
   "target"
   ```

   得到函数对象 `build_entry`。

2. 位置实参：

   ```python
   evaluate("key", "menu.quit")
   ```

   成功，追加 `"key"`，得到 `"menu.quit"`。

3. `locale` 的值表达式：

   ```python
   evaluate("locale", "en-US")
   ```

   成功，追加 `"locale"`，得到 `"en-US"`。

4. `unknown` 的值表达式：

   ```python
   evaluate("unknown", True)
   ```

   也成功，追加 `"unknown"`，得到 `True`。

5. 至此，调用端已经得到并装配出概念上的输入：

   ```text
   positional: "menu.quit"
   keyword:    locale="en-US"
   keyword:    unknown=True
   ```

6. 目标签名是：

   ```python
   def build_entry(key, *, locale):
   ```

   - `"menu.quit"` 可以绑定 `key`；
   - `locale="en-US"` 可以绑定 keyword-only 形参 `locale`；
   - `unknown=True` 没有对应形参，而且目标没有 `**kwargs`。

   因而**签名匹配失败**，抛出 `TypeError`。

7. 外层捕获后追加 `"caught:TypeError"`。

第二段中所有实参表达式都已成功求值，调用输入也已形成；失败发生在：

> **目标签名的参数匹配阶段**。

因为匹配没有整体成功，所以不会建立一个可进入 `build_entry` 函数体的成功调用帧/完整局部形参绑定，`"body"` 不会追加。

---

### 为什么捕获异常不会回滚较早效果

`events.append(...)` 是在异常发生之前已经完成的列表原地修改。普通 Python 异常处理不会自动提供事务式回滚：

```text
已经 append 的项目
    ↓
对象状态已经改变
    ↓
后续抛异常 / 被 except 捕获
    ↓
不会自动撤销先前修改
```

所以第一段已经留下 `"target"`、`"key"`、`"locale:fail"`；第二段已经留下 `"target"`、`"key"`、`"locale"`、`"unknown"`。`except` 只是接管异常后的控制流，并不会把 `events` 恢复到调用前状态。

<!-- answer:end -->

---

<!-- quiz-section: id=B score=18 -->
## B. 参数种类、绑定矩阵与失败边界（18 分）

<!-- quiz-question: id=B1 score=10 -->
### B1（10 分）

给定一个同时出现五类参数的签名：

~~~python
def route_record(
    record_id,
    /,
    locale="en-US",
    *tags,
    dry_run,
    **metadata,
):
    return {
        "record_id": record_id,
        "locale": locale,
        "tags": tags,
        "dry_run": dry_run,
        "metadata": metadata,
    }


result = route_record(
    "prompt-010",
    "ja-JP",
    "menu",
    "reviewed",
    dry_run=False,
    reviewer="qa",
    priority=2,
)
~~~

完成以下任务：

1. 按定义顺序写出 `record_id`、`locale`、`tags`、`dry_run` 和
   `metadata` 各自的参数种类。
2. 写出本次调用成功后五个局部形参的精确绑定结果，以及 `tags` 和
   `metadata` 的对象类型。
3. 说明 `/`、`*tags` 和 `**metadata` 中哪些部分只是签名语法标记，
   哪些才是真正的局部名字。
4. 判断本次调用是否使用了 `locale` 的默认值，并说明“有默认值”和
   “positional-or-keyword”为什么是两个不同维度。

<!-- answer:start -->

### 1. 五个形参的参数种类

按定义顺序：

| 形参        | 参数种类              |
| ----------- | --------------------- |
| `record_id` | positional-only       |
| `locale`    | positional-or-keyword |
| `tags`      | var-positional        |
| `dry_run`   | keyword-only          |
| `metadata`  | var-keyword           |

对应到 `inspect.Parameter.kind` 的名称则是：

```text
record_id -> POSITIONAL_ONLY
locale    -> POSITIONAL_OR_KEYWORD
tags      -> VAR_POSITIONAL
dry_run   -> KEYWORD_ONLY
metadata  -> VAR_KEYWORD
```

### 2. 本次成功调用的精确绑定

调用：

```python
route_record(
    "prompt-010",
    "ja-JP",
    "menu",
    "reviewed",
    dry_run=False,
    reviewer="qa",
    priority=2,
)
```

位置输入从左向右处理：

```text
"prompt-010" -> record_id
"ja-JP"      -> locale
```

剩余位置输入由 `*tags` 收集：

```text
"menu"
"reviewed"
    ↓
tags -> ("menu", "reviewed")
```

关键字：

```text
dry_run=False -> dry_run
```

剩余的未知显式关键字由 `**metadata` 收集：

```text
reviewer="qa"
priority=2
    ↓
metadata -> {"reviewer": "qa", "priority": 2}
```

因此最终局部形参绑定为：

```python
record_id == "prompt-010"
locale == "ja-JP"
tags == ("menu", "reviewed")
dry_run is False
metadata == {"reviewer": "qa", "priority": 2}
```

对象类型：

```text
tags     -> tuple
metadata -> dict
```

于是 `result` 的内容为：

```python
{
    "record_id": "prompt-010",
    "locale": "ja-JP",
    "tags": ("menu", "reviewed"),
    "dry_run": False,
    "metadata": {
        "reviewer": "qa",
        "priority": 2,
    },
}
```

### 3. `/`、`*tags`、`**metadata` 中哪些是标记，哪些是名字

```python
record_id,
/
```

其中 `/` 是**签名语法分隔标记**，不是局部参数名字。真正的局部形参名字是 `record_id`。

```python
*tags
```

中：

- `*` 是语法标记，表示这是 var-positional parameter，并同时形成后续 keyword-only 区域；
- `tags` 才是真正的局部形参名字。

```python
**metadata
```

中：

- `**` 是语法标记，表示收集剩余关键字；
- `metadata` 才是真正的局部形参名字。

所以本题实际有五个局部参数名字：

```text
record_id
locale
tags
dry_run
metadata
```

而 `/`、`*`、`**` 本身都不是额外的局部名字。

### 4. 是否使用了 `locale` 的默认值，以及两个维度的区别

本次调用**没有**使用：

```python
locale="en-US"
```

这个默认值，因为第二个位置实参 `"ja-JP"` 已经显式绑定了 `locale`：

```text
locale -> "ja-JP"
```

“有默认值”和“positional-or-keyword”回答的是两个不同问题：

- **parameter kind** 回答：调用者允许用什么形式提供这个参数？
- **default** 回答：如果调用者没有提供它，是否有预先保存的备用对象？

本题 `locale` 是：

```text
kind    = positional-or-keyword
default = "en-US"
```

所以它既可以：

```python
route_record("id", "ja-JP", ..., dry_run=False)
```

按位置提供，也可以：

```python
route_record("id", locale="ja-JP", dry_run=False)
```

按关键字提供；若完全省略，才使用默认对象 `"en-US"`。

因此“有默认值”绝不能推出“keyword-only”，反之亦然。

<!-- answer:end -->

<!-- quiz-question: id=B2 score=8 -->
### B2（8 分）

阅读代码。不要依赖完整 `TypeError` 文案：

~~~python
body_events = []


def strict_entry(key, locale="en-US", *, dry_run):
    body_events.append((key, locale, dry_run))
    return f"{locale}:{key}"


def positional_identity(record_id, /):
    return record_id


calls = [
    lambda: strict_entry(dry_run=True),
    lambda: strict_entry("menu.start", key="menu.quit", dry_run=True),
    lambda: strict_entry("menu.start", dry_run=True, verbose=True),
    lambda: strict_entry("menu.start", "ja-JP", False, dry_run=True),
    lambda: positional_identity(record_id="prompt-011"),
]

for call in calls:
    try:
        call()
    except TypeError:
        print("TypeError")

print(body_events)
~~~

1. 写出全部六行输出。
2. 按调用顺序把五次失败分别分类为：缺失必填、同一形参重复赋值、未知关键字、
   过多位置实参、positional-only 误用。
3. 说明 `strict_entry` 是否有任何一次建立成功的局部形参绑定并进入函数体。
4. 对第二次调用说明：`key="menu.quit"` 为什么不会被某个不存在的
   `**kwargs` 收留，也不会覆盖已经按位置提供的 `key`。

<!-- answer:start -->

### 1. 全部六行输出

五次调用全部在进入目标函数体之前抛出 `TypeError`，因此输出为：

```text
TypeError
TypeError
TypeError
TypeError
TypeError
[]
```

最后：

```python
body_events
```

仍为空列表，因为 `strict_entry` 没有任何一次成功进入函数体。

### 2. 五次失败的分类

按调用顺序：

#### 第 1 次

```python
strict_entry(dry_run=True)
```

失败类别：

> **缺失必填形参**

`dry_run` 得到关键字输入 `True`，但必需形参 `key` 没有任何输入。`locale` 有默认值可以省略，但 `key` 不可以。

---

#### 第 2 次

```python
strict_entry(
    "menu.start",
    key="menu.quit",
    dry_run=True,
)
```

失败类别：

> **同一形参重复赋值**

位置实参 `"menu.start"` 已经为 `key` 提供值，随后 `key="menu.quit"` 又试图为同一个 positional-or-keyword 形参提供第二个值。

这不是“后一个覆盖前一个”，而是重复供值导致 `TypeError`。

---

#### 第 3 次

```python
strict_entry(
    "menu.start",
    dry_run=True,
    verbose=True,
)
```

失败类别：

> **未知关键字**

`key` 与 `dry_run` 都可以正常绑定，但签名没有名为 `verbose` 的形参，也没有 `**kwargs` 可以收集它，因此整体匹配失败。

---

#### 第 4 次

```python
strict_entry(
    "menu.start",
    "ja-JP",
    False,
    dry_run=True,
)
```

失败类别：

> **过多位置实参**

`strict_entry` 可以按位置接收的普通形参只有：

```text
key
locale
```

前两个位置实参分别填满它们。第三个位置实参 `False` 没有可用的位置参数槽，函数也没有 `*args`。

`dry_run` 是 keyword-only，不能因为第三个位置实参恰好是布尔值就自动接收它。

---

#### 第 5 次

```python
positional_identity(record_id="prompt-011")
```

失败类别：

> **positional-only 误用**

签名：

```python
def positional_identity(record_id, /):
```

要求 `record_id` 必须由位置输入提供。写成关键字 `record_id=...` 违反 `/` 所表达的调用合同，因此 `TypeError`。

### 3. `strict_entry` 是否有一次成功进入函数体

没有。

前三次针对 `strict_entry` 的调用分别由于：

```text
缺失 key
重复 key
未知 verbose
```

失败；第四次由于位置实参过多失败。

所有这些错误都发生在成功函数体入口之前。因此：

```python
body_events.append((key, locale, dry_run))
```

从未执行，最终：

```python
body_events == []
```

### 4. 为什么第二次的 `key=` 不会被“收留”或覆盖

签名是：

```python
def strict_entry(key, locale="en-US", *, dry_run):
```

其中根本没有：

```python
**kwargs
```

所以不存在一个可以收集额外关键字的 var-keyword parameter。

更重要的是，`key="menu.quit"` 本身也不是“未知关键字”：`key` 是一个明确声明、且允许按关键字绑定的 positional-or-keyword parameter。问题在于它已经由位置输入 `"menu.start"` 填过一次。

因此逻辑是：

```text
"menu.start" -> key
key="menu.quit" -> 再次试图绑定 key
                 ↓
              重复供值
                 ↓
              TypeError
```

Python 的参数匹配不采用“后来的关键字覆盖先前的位置实参”规则；同一形参只能得到一份合法输入。

<!-- answer:end -->

---

<!-- quiz-section: id=C score=18 -->
## C. 默认值、对象身份与可变状态（18 分）

<!-- quiz-question: id=C1 score=10 -->
### C1（10 分）

预测输出并追踪对象身份：

~~~python
definition_events = []


def make_history():
    definition_events.append("made")
    return []


def record_key(key, history=make_history()):
    history.append(key)
    return history


saved = record_key.__defaults__[0]

first = record_key("menu.start")

custom = []
explicit = record_key("dialog.ok", custom)

third = record_key("settings.audio")

print(definition_events)
print(first)
print(explicit)
print(third)
print(first is third)
print(record_key.__defaults__[0] is saved)
~~~

完成以下任务：

1. 写出六行精确输出。注意所有调用结束后才执行这些 `print`。
2. 说明 `make_history()` 在什么阶段、执行几次；不要把它描述成每次省略实参时
   重新执行。
3. 分别说明三次调用中局部形参 `history` 绑定哪个列表对象，并解释每次调用的
   函数帧是新的，为什么默认列表仍然可以相同。
4. 判断显式传入 `custom` 是否替换了函数对象保存的默认对象，以及它的修改对谁
   可见。
5. 说明这里的跨调用状态为什么不是 `global` 或 `nonlocal` 机制。

<!-- answer:start -->

### 1. 六行精确输出

完整输出为：

```text
['made']
['menu.start', 'settings.audio']
['dialog.ok']
['menu.start', 'settings.audio']
True
True
```

注意：三个 `record_key(...)` 调用全部结束后才开始执行这些 `print`。因此 `first` 和 `third` 虽然分别在不同时间获得返回值，却都引用同一个默认列表；打印 `first` 时，这个列表已经被第三次调用继续追加了 `"settings.audio"`。

### 2. `make_history()` 的执行时机和次数

执行：

```python
def record_key(key, history=make_history()):
```

这一函数定义语句时，Python 会求值默认表达式：

```python
make_history()
```

它：

1. 向 `definition_events` 追加 `"made"`；
2. 创建一个新列表；
3. 返回该列表；
4. 该列表随后作为 `record_key` 的默认对象由函数对象保存。

所以：

```python
make_history()
```

在本段程序中一共执行 **1 次**，执行阶段是：

> **`def record_key(...)` 被执行、函数对象被创建时。**

以后调用：

```python
record_key("menu.start")
record_key("settings.audio")
```

即使都省略 `history`，也不会重新执行 `make_history()`；它们复用已经保存的默认列表对象。

### 3. 三次调用中的 `history` 绑定

把函数保存的默认列表记为 `L0`，把 `custom` 所引用的列表记为 `L1`。

函数定义结束时：

```text
record_key.__defaults__[0] -> L0 []
saved                       -> L0 []
```

#### 第一次调用

```python
first = record_key("menu.start")
```

省略 `history`，因此本次新的函数帧中：

```text
key     -> "menu.start"
history -> L0
```

执行 `history.append(key)` 后：

```text
L0 == ["menu.start"]
```

并返回 `L0`，所以：

```text
first -> L0
```

#### 第二次调用

```python
explicit = record_key("dialog.ok", custom)
```

这次显式提供 `custom`，因此新函数帧中：

```text
key     -> "dialog.ok"
history -> L1
```

追加后：

```text
L1 == ["dialog.ok"]
```

所以：

```text
explicit -> L1
custom   -> L1
```

#### 第三次调用

```python
third = record_key("settings.audio")
```

再次省略 `history`，所以这个**第三个、全新的函数调用帧**中的局部形参又绑定同一个函数默认对象：

```text
history -> L0
```

再追加 `"settings.audio"`：

```text
L0 == ["menu.start", "settings.audio"]
```

并返回 `L0`：

```text
third -> L0
```

因此：

```python
first is third  # True
```

每次调用的局部函数帧确实是新的；共享发生的原因不是“函数帧复用”，而是：

> 不同调用中的局部形参 `history` 在省略实参时，都被绑定到了函数对象保存的**同一个默认列表对象**。

### 4. 显式 `custom` 是否替换函数默认对象

不会。

第二次调用：

```python
record_key("dialog.ok", custom)
```

只是让**这一次调用**的局部形参：

```text
history -> custom 所引用的 L1
```

它不会改写：

```python
record_key.__defaults__
```

所以：

```text
record_key.__defaults__[0] -> 仍然是 L0
saved                       -> 仍然是 L0
```

对 `history.append("dialog.ok")` 的修改发生在调用者显式提供的 `L1` 上，因此调用者通过：

```python
custom
```

也能观察到：

```python
["dialog.ok"]
```

### 5. 为什么不是 `global` / `nonlocal`

跨调用共享状态来自：

```text
def 执行时创建默认列表 L0
        ↓
函数对象保存 L0
        ↓
省略 history 的不同调用
都把各自局部形参 history 绑定到 L0
        ↓
对 L0 原地修改
```

这里没有使用 `global` 声明去重新绑定模块全局名字，也没有使用 `nonlocal` 去重新绑定 enclosing function 的 cell。

所以这属于：

> **函数默认对象的生命周期 + 多次调用对同一对象的共享引用**

而不是 `global` / `nonlocal` 名字绑定机制。

<!-- answer:end -->

<!-- quiz-question: id=C2 score=8 -->
### C2（8 分）

下面的函数意图是：省略 `options` 时，每次调用获得独立状态；显式传入字典时，
函数使用调用者的字典，并允许调用者观察到 `seen` 的修改。

~~~python
def build_label(
    key,
    options={"locale": "en-US", "seen": []},
):
    options["seen"].append(key)
    return {
        "label": f"{options['locale']}:{key}",
        "options": options,
    }
~~~

完成以下任务：

1. 在答题区重写 `build_label`，使用 `options=None` 表示“未提供”，并在每次
   省略调用的函数体内创建新的字典和列表。本题约定 `None` 不是合法业务值，
   不要求设计专用 sentinel。
2. 对你的修复版本判断下列身份关系，并说明理由：

~~~python
first = build_label("menu.start")
second = build_label("menu.quit")

supplied = {"locale": "ja-JP", "seen": []}
explicit = build_label("dialog.ok", supplied)

print(first["options"] is second["options"])
print(explicit["options"] is supplied)
print(supplied["seen"])
~~~

3. 精确区分修复代码中的“创建新字典”“局部名字 `options` 重新绑定”和
   “修改显式传入对象”。说明该修复为什么只隔离省略调用，并不自动复制或保护
   调用者显式提供的字典。

<!-- answer:start -->

### 1. 修复后的完整函数

```python
def build_label(
    key,
    options=None,
):
    if options is None:
        options = {
            "locale": "en-US",
            "seen": [],
        }

    options["seen"].append(key)

    return {
        "label": f"{options['locale']}:{key}",
        "options": options,
    }
```

这里按题目约定：

```text
None == “调用者未提供业务 options”
```

所以只有在 `options is None` 时，才在**本次调用期间**创建一套新的状态。

### 2. 三行输出和身份关系

运行：

```python
first = build_label("menu.start")
second = build_label("menu.quit")

supplied = {"locale": "ja-JP", "seen": []}
explicit = build_label("dialog.ok", supplied)

print(first["options"] is second["options"])
print(explicit["options"] is supplied)
print(supplied["seen"])
```

输出：

```text
False
True
['dialog.ok']
```

#### 第一行为何是 `False`

第一次省略：

```python
build_label("menu.start")
```

时创建新字典 `D1`，其中包含自己的新列表 `L1`。

第二次省略：

```python
build_label("menu.quit")
```

时又创建独立字典 `D2` 和列表 `L2`。

所以：

```text
first["options"]  -> D1
second["options"] -> D2
```

二者不是同一个对象：

```python
first["options"] is second["options"]  # False
```

#### 第二、三行为何如此

显式调用：

```python
build_label("dialog.ok", supplied)
```

不会进入 `options is None` 分支，因此本次局部形参：

```text
options -> supplied 所绑定的原字典
```

随后：

```python
options["seen"].append("dialog.ok")
```

原地修改这个显式传入字典内部的列表。

返回值中的：

```python
"options": options
```

仍引用同一个原字典，所以：

```python
explicit["options"] is supplied  # True
```

且：

```python
supplied["seen"] == ["dialog.ok"]
```

### 3. 创建、局部重绑和显式对象修改的区别

在省略调用中：

```python
if options is None:
    options = {
        "locale": "en-US",
        "seen": [],
    }
```

包含三个不同层次：

1. 字典显示式创建一个**新的顶层字典对象**；
2. 其中 `[]` 创建一个**新的列表对象**；
3. `options = ...` 把本次调用的局部形参名字 `options` 从 `None` **重新绑定**到这个新字典。

然后：

```python
options["seen"].append(key)
```

修改的是本次新字典中的新列表，因此不同省略调用之间互不共享。

但是显式传入：

```python
supplied
```

时，本次调用的局部形参一开始就直接绑定调用者的字典，并且不会进入创建新对象的分支。随后的：

```python
options["seen"].append(key)
```

修改调用者字典中原有的共享列表，所以调用者能观察到变化。

因此这个修复只承诺：

> **省略 `options` 的每次调用获得独立状态。**

它没有承诺：

> **显式传入对象会被复制或保护。**

若要保护显式传入字典，需要另外设计复制策略；那不是本题给出的合同。

<!-- answer:end -->

---

<!-- quiz-section: id=D score=20 -->
## D. 定义端收集、调用端解包与部分效果（20 分）

<!-- quiz-question: id=D1 score=10 -->
### D1（10 分）

阅读定义端收集代码：

~~~python
def collect_inputs(primary_key, *extra_keys, **controls):
    return {
        "primary_key": primary_key,
        "extra_keys": extra_keys,
        "controls": controls,
    }


shared_channels = ["menu"]

collected = collect_inputs(
    "menu.start",
    "menu.quit",
    shared_channels,
    locale="ja-JP",
    channels=shared_channels,
)

collected["controls"]["channels"].append("dialog")
empty = collect_inputs("settings.audio")

print(collected["extra_keys"])
print(collected["controls"])
print(shared_channels)
print(collected["extra_keys"][1] is collected["controls"]["channels"])
print(collected["controls"]["channels"] is shared_channels)
print(empty["extra_keys"])
print(empty["controls"])
~~~

1. 写出七行精确输出。
2. 写出第一次调用中三个形参的绑定结果，并说明 `extra_keys` 与 `controls`
   分别是什么类型。
3. 说明为什么 `extra_keys` 元组和 `controls` 字典是不同的收集容器，却可以
   在内部同时引用 `shared_channels` 这一个列表对象。
4. `append("dialog")` 修改的是哪一层对象？它是否修改了元组槽位、替换了字典
   中的值，或深拷贝了列表？
5. 解释没有剩余实参时，两个收集形参为什么仍然分别得到空元组和空字典；不要根据
   空元组显示形式推断跨调用身份合同。

<!-- answer:start -->

### 1. 七行精确输出

完整输出：

```text
('menu.quit', ['menu', 'dialog'])
{'locale': 'ja-JP', 'channels': ['menu', 'dialog']}
['menu', 'dialog']
True
True
()
{}
```

### 2. 第一次调用的三个形参绑定和类型

调用：

```python
collected = collect_inputs(
    "menu.start",
    "menu.quit",
    shared_channels,
    locale="ja-JP",
    channels=shared_channels,
)
```

成功后的形参绑定：

```text
primary_key -> "menu.start"

extra_keys  -> (
    "menu.quit",
    shared_channels 所引用的列表对象,
)

controls    -> {
    "locale": "ja-JP",
    "channels": shared_channels 所引用的列表对象,
}
```

对象类型：

```text
extra_keys -> tuple
controls   -> dict
```

`*extra_keys` 是定义端 var-positional 收集；`**controls` 是定义端 var-keyword 收集。

### 3. 为什么两个新容器可以同时引用同一个列表

调用端表达式：

```python
shared_channels
```

在两个不同位置被求值时，都得到同一个列表对象。

定义端随后创建不同的收集容器：

```text
extra_keys -> tuple T
controls   -> dict D
```

但创建外层容器并不会深复制其中的成员对象，因此关系是：

```text
                 ┌-> tuple T 的第 2 个元素
shared_channels -> list L
                 └-> dict D 的 "channels" 值
```

所以：

```python
collected["extra_keys"][1] is collected["controls"]["channels"]
```

为 `True`，并且：

```python
collected["controls"]["channels"] is shared_channels
```

也为 `True`。

### 4. `append("dialog")` 修改哪一层

语句：

```python
collected["controls"]["channels"].append("dialog")
```

先沿引用链取得：

```text
collected
  -> controls 字典
  -> "channels" 对应的共享列表 L
```

然后在列表 `L` 上执行原地修改：

```text
["menu"] -> ["menu", "dialog"]
```

它**没有**：

- 修改 `extra_keys` 元组的槽位；
- 把 `controls["channels"]` 替换成另一个列表；
- 深拷贝列表；
- 重新绑定调用方名字 `shared_channels`。

因为三个地方仍然引用同一个 `L`，所以它们随后都能观察到列表内容已经增加 `"dialog"`。

### 5. 没有剩余输入时为什么仍有空收集值

第二次调用：

```python
empty = collect_inputs("settings.audio")
```

只有 `primary_key` 获得显式输入。

按照变长参数的调用规则：

```text
没有剩余位置输入
    ↓
extra_keys -> ()

没有剩余关键字输入
    ↓
controls -> {}
```

所以这两个收集形参仍然是**已经正常绑定的局部名字**，而不是未绑定或自动变成 `None`。

这里：

```python
()
```

只说明本次没有剩余位置实参。不能根据空元组的显示形式或某次 `is` 观察，进一步声称“Python 语言保证所有调用中的空 `*args` 都必须是同一个 tuple 对象”。题目要求的稳定合同是其值和类型/绑定语义，而不是跨调用的空元组对象身份。

<!-- answer:end -->

<!-- quiz-question: id=D2 score=10 -->

### D2（10 分）

预测两次调用的事件，并区分调用端解包与定义端收集：

~~~python
events = []


def positional_source():
    events.append("positional")
    return ("prompt-012", "en-US")


def locale_keyword():
    events.append("locale keyword")
    return "fr-FR"


def flags_source():
    events.append("flags")
    return {"dry_run": True}


def audit_entry(key, locale, *, dry_run):
    events.append("body")
    return key, locale, dry_run


audit_entry(*positional_source(), **flags_source())
print(events)

events.clear()

try:
    audit_entry(
        *positional_source(),
        locale=locale_keyword(),
        **flags_source(),
    )
except TypeError:
    events.append("caught:TypeError")

print(events)
~~~

1. 写出两行精确输出。
2. 对第一次调用写出 `*` 和 `**` 分别装配出的实参，以及成功匹配后的三个
   局部形参绑定。
3. 第二次调用中的关键字名称彼此并不重复；请说明为什么仍然抛出 `TypeError`，
   并把失败定位到关键字输入装配还是目标签名匹配。
4. 第二次调用中哪些源表达式和副作用已经完成？`audit_entry` 是否建立局部形参
   绑定并进入函数体？异常是否回滚事件列表？
5. 说明调用端 `**flags_source()` 为什么不会为目标函数创造一个
   `**kwargs` 形参。目标函数没有任意关键字收集器，为什么第一次调用仍能成功？

<!-- answer:start -->

### 1. 两行精确输出

第一行：

```text
['positional', 'flags', 'body']
```

第二行：

```text
['positional', 'locale keyword', 'flags', 'caught:TypeError']
```

---

### 2. 第一次调用的展开与成功绑定

调用：

```python
audit_entry(*positional_source(), **flags_source())
```

#### `*positional_source()`

先执行：

```python
positional_source()
```

向 `events` 追加：

```text
"positional"
```

并返回：

```python
("prompt-012", "en-US")
```

调用端 `*` 将它展开为两个位置输入：

```text
位置输入 1: "prompt-012"
位置输入 2: "en-US"
```

#### `**flags_source()`

随后执行：

```python
flags_source()
```

追加：

```text
"flags"
```

并返回：

```python
{"dry_run": True}
```

调用端 `**` 装配出关键字输入：

```text
dry_run=True
```

#### 对目标签名匹配

目标：

```python
def audit_entry(key, locale, *, dry_run):
```

成功绑定为：

```text
key     -> "prompt-012"
locale  -> "en-US"
dry_run -> True
```

于是函数帧建立，进入函数体，执行：

```python
events.append("body")
```

最终第一行事件为：

```python
['positional', 'flags', 'body']
```

---

### 3. 第二次为何关键字不重名仍然 `TypeError`

第二次调用：

```python
audit_entry(
    *positional_source(),
    locale=locale_keyword(),
    **flags_source(),
)
```

三个来源依次成功产生：

```text
*positional_source()
    -> 位置输入 "prompt-012", "en-US"

locale=locale_keyword()
    -> 关键字输入 locale="fr-FR"

**flags_source()
    -> 关键字输入 dry_run=True
```

这里两个**关键字名称**：

```text
locale
dry_run
```

确实彼此不重复，所以不是“调用端两个 keyword source 产生同名键”的输入装配冲突。

真正的问题发生在对目标签名进行匹配时：

```text
第 1 个位置输入 -> key
第 2 个位置输入 -> locale
显式 locale="fr-FR" -> 又试图绑定 locale
```

所以同一个形参 `locale` 同时收到：

```text
位置值 "en-US"
关键字值 "fr-FR"
```

导致 `TypeError`。

因此本题应定位为：

> **调用输入已经装配完成后，在目标签名的 parameter matching 阶段发生重复形参供值。**

---

### 4. 第二次已经完成哪些副作用；是否有函数帧

执行顺序为：

1. `positional_source()`：
   - 追加 `"positional"`；
   - 返回 tuple；
   - `*` 展开成功。

2. `locale_keyword()`：
   - 追加 `"locale keyword"`；
   - 返回 `"fr-FR"`。

3. `flags_source()`：
   - 追加 `"flags"`；
   - 返回 mapping；
   - `**` 展开成功。

4. 随后在目标签名匹配时发现 `locale` 重复供值，抛出 `TypeError`。

因此三个源表达式及其副作用**全部已经完成**。

但是参数匹配没有整体成功，所以不会建立一个进入 `audit_entry` 函数体的成功函数帧/完整局部形参绑定，也不会执行：

```python
events.append("body")
```

外层捕获后才追加：

```text
"caught:TypeError"
```

异常不会回滚之前已经追加的：

```text
"positional"
"locale keyword"
"flags"
```

---

### 5. `**flags_source()` 不会创造目标的 `**kwargs`

调用端：

```python
**flags_source()
```

只负责把一个 mapping 展开为**多个关键字调用输入**。它不会修改目标函数的定义，也不会凭空创建：

```python
**kwargs
```

形参。

目标签名仍然固定是：

```python
def audit_entry(key, locale, *, dry_run):
```

第一次调用之所以能成功，是因为 `**flags_source()` 只产生：

```text
dry_run=True
```

而目标本来就显式声明了 keyword-only parameter：

```text
dry_run
```

所以它被正常匹配，无需 `**kwargs`。

只有 mapping 中存在目标签名不认识的额外关键字时，且目标又没有 `**kwargs`，才会因未知关键字而匹配失败。

<!-- answer:end -->

---

<!-- quiz-section: id=E score=14 -->
## E. 签名观察、绑定记录与证据强度（14 分）

<!-- quiz-question: id=E1 score=8 -->
### E1（8 分）

下面把“签名可以接受这种调用形状”和“函数体可以成功完成”拆成两类证据：

~~~python
import inspect


body_events = []


def render(record_id, /, text, *, locale="en-US"):
    body_events.append(record_id)
    return f"{locale}:{text.strip()}"


signature = inspect.signature(render)
bound = signature.bind("prompt-020", 404)

print(tuple(bound.arguments.items()))
print(tuple(body_events))

try:
    render("prompt-020", 404)
except AttributeError:
    print("caught:AttributeError")

print(tuple(body_events))

try:
    signature.bind(record_id="prompt-021", text="Quit")
except TypeError:
    print("caught:TypeError")

print(tuple(body_events))
~~~

完成以下任务：

1. 写出六行精确输出；异常只需使用代码中已经固定的标签，不要求复述解释器原始
   报错文本。
2. 写出 `bound.arguments` 记录的形参到对象的映射，并说明其中为什么暂时没有
   `locale`。指出默认值仍属于签名的一部分，但 `bind()` 不会自动把省略的默认项
   填进这份记录。
3. 解释 `signature.bind("prompt-020", 404)` 为什么能够成功：它检查的是调用
   形状能否绑定，不会因为整数 `404` 在函数体中没有 `strip()` 方法而失败。
4. 对真实 `render("prompt-020", 404)` 按时间线区分：实参求值、参数匹配、
   函数帧与局部绑定、`body_events.append(...)`，以及随后发生的异常。说明已经
   完成的列表副作用不会因异常自动回滚。
5. 最后一次 `signature.bind(...)` 为什么失败？它是否调用了 `render`、建立了
   `render` 的函数帧或改变了 `body_events`？

<!-- answer:start -->

### 1. 六行精确输出

完整输出为：

```text
(('record_id', 'prompt-020'), ('text', 404))
()
caught:AttributeError
('prompt-020',)
caught:TypeError
('prompt-020',)
```

---

### 2. `bound.arguments` 的映射及为什么没有 `locale`

执行：

```python
bound = signature.bind("prompt-020", 404)
```

对签名：

```python
def render(record_id, /, text, *, locale="en-US"):
```

产生的显式绑定记录是：

```text
record_id -> "prompt-020"
text      -> 404
```

即概念上：

```python
bound.arguments == {
    "record_id": "prompt-020",
    "text": 404,
}
```

所以：

```python
tuple(bound.arguments.items())
```

打印：

```text
(('record_id', 'prompt-020'), ('text', 404))
```

`locale` 没出现在这里，不代表签名没有 default，也不代表真实调用进入函数体后 `locale` 会未绑定。

它的 default：

```python
"en-US"
```

仍然属于 `Signature`/parameter 合同的一部分；只是 `Signature.bind()` 返回的 `BoundArguments.arguments` 默认只记录本次**显式绑定**的项目，不会自动把依赖 default 的参数补入。

若需要补全，可以另外调用：

```python
bound.apply_defaults()
```

但题目代码没有这么做。

---

### 3. 为什么 `bind("prompt-020", 404)` 能成功

`Signature.bind()` 检查的是：

> 给定的这些位置/关键字对象能否按照该 `Signature` 的参数形状完成合法映射。

这里：

```text
"prompt-020" -> positional-only record_id
404          -> text
locale       -> 可依赖 default
```

不存在：

- 缺失必需参数；
- 重复供值；
- 位置过量；
- 未知关键字；
- positional-only 误用。

所以绑定形状完全合法。

`bind()` 不执行：

```python
text.strip()
```

也不会检查 `404` 是否具有 `strip` 方法，因此不会因为 `text` 是整数而失败。

---

### 4. 真实调用的完整时间线

真实调用：

```python
render("prompt-020", 404)
```

依次发生：

1. 调用目标 `render` 求值得到函数对象。

2. 两个实参表达式都是简单常量，求值成功：

   ```text
   "prompt-020"
   404
   ```

3. 参数匹配成功：

   ```text
   record_id -> "prompt-020"
   text      -> 404
   locale    -> 默认对象 "en-US"
   ```

4. 建立本次真实函数调用的函数帧与局部形参绑定。

5. 进入函数体，首先执行：

   ```python
   body_events.append(record_id)
   ```

   所以列表变为：

   ```python
   ["prompt-020"]
   ```

6. 接着计算返回表达式：

   ```python
   f"{locale}:{text.strip()}"
   ```

   需要执行：

   ```python
   404.strip()
   ```

   整数没有 `strip` 方法，因此在**函数体内部**抛出 `AttributeError`。

7. 外层捕获并打印：

   ```text
   caught:AttributeError
   ```

此前已经完成的：

```python
body_events.append("prompt-020")
```

不会被异常自动回滚，所以后面打印：

```text
('prompt-020',)
```

---

### 5. 最后一次 `signature.bind(...)` 为什么失败

调用：

```python
signature.bind(
    record_id="prompt-021",
    text="Quit",
)
```

试图用关键字：

```text
record_id="prompt-021"
```

绑定：

```python
record_id
```

但 `record_id` 位于 `/` 前，是 positional-only parameter，不能按关键字提供，因此 `bind()` 抛出 `TypeError`。

这只是对 `Signature` 对象执行绑定模拟：

- 没有真实调用 `render`；
- 没有建立 `render` 的真实函数帧；
- 没有进入 `render` 函数体；
- 没有执行 `body_events.append(...)`。

所以捕获并打印：

```text
caught:TypeError
```

后，`body_events` 仍保持：

```python
["prompt-020"]
```

最终再打印：

```text
('prompt-020',)
```

<!-- answer:end -->

<!-- quiz-question: id=E2 score=6 -->
### E2（6 分）

某工程师要判断一个具体调用 `callable_obj("prompt-022", "Quit", locale="fr-FR")`
是否可靠，手上有以下五条相互独立的证据：

1. 在源文件中看到了一条 `def` 语句。
2. 当前进程中 `inspect.signature(callable_obj)` 显示相应的位置参数和
   keyword-only 参数。
3. 对这组实参执行 `inspect.signature(callable_obj).bind(...)` 成功，并取得了
   `BoundArguments.arguments`。
4. 用这组实参真实调用一次，函数返回了预期结果。
5. 用一个样例调用成功后，工程师宣称“所有语言代码、所有文本对象、所有业务状态
   都一定成功”。

完成以下任务：

1. 分别说明前四条证据能直接证明什么、不能证明什么。至少区分：源代码观察、
   运行时呈现的签名、调用形状绑定、函数体与业务逻辑真实执行。
2. 判断第 5 条结论是否成立，并给出不扩大本章范围的最小补证方案：应增加哪些
   代表性真实调用，而不是把一次成功外推为普遍结论。
3. 若第 2 条与第 3 条都成功，但第 4 条抛出函数体内部的 `ValueError`，这三条
   事实是否矛盾？请用“绑定合同”和“业务合同”解释。
4. 若只允许为这个具体调用选择一条最强的完成证据，应选择哪一条？说明为什么
   `bind()` 很适合诊断参数合同，却不能替代真实调用。

<!-- answer:start -->

这五条证据必须按**证据层级**分别解释，不能互相替代。

### 1. 前四条证据分别能证明什么、不能证明什么

#### 证据 1：在源文件中看到一条 `def` 语句

它能直接证明的主要是：

> 这份源代码文本声明了一个函数定义语句及其源码层参数结构/函数体文本。

它**不能单独证明**：

- 当前进程中的 `callable_obj` 一定就是该 `def` 创建的那个函数对象；
- 这条 `def` 当前一定已经执行；
- 当前名字没有被后续重新绑定；
- 当前运行时实际呈现的 callable 签名一定与看到的源码完全一致；
- 某组实参一定能成功调用；
- 函数体或业务逻辑一定成功。

所以这是**源代码观察证据**。

---

#### 证据 2：当前进程中 `inspect.signature(callable_obj)` 显示相应签名

它能直接支持：

> 当前运行时 `inspect` 对这个 callable 暴露/解析出了一份具有相应位置参数、keyword-only 参数等结构的 `Signature`。

这比只看源代码更接近当前进程中的对象。

但它仍不能证明：

- 原始实参表达式一定能求值；
- `*` / `**` 来源一定展开成功；
- 某组调用输入一定不会重复/缺失；
- 函数体会成功完成；
- 文本、locale 等业务值一定有效；
- 返回值与副作用符合业务合同。

所以这是**运行时签名呈现的内省证据**。

---

#### 证据 3：对具体实参执行 `.bind(...)` 成功

它能直接证明：

> 已经交给 `bind()` 的这一组位置/关键字对象，可以按照这份 `Signature` 完成合法的参数映射。

也就是可以排除这一次模拟中的典型调用形状问题，例如：

- 必需参数缺失；
- 同一参数重复供值；
- 不允许的 positional-only 关键字传法；
- 位置输入过多；
- 未知且无法收集的关键字。

但它不能证明：

- 原始实参表达式本身的求值过程；
- 调用端展开过程；
- 函数体行为；
- 值的业务有效性；
- 返回结果或副作用。

所以这是**调用形状 / 参数绑定合同证据**。

---

#### 证据 4：用这组实参真实调用一次并得到预期结果

对于这个**具体调用、当时的运行环境和业务状态**，这是前四条中最强的完成证据。

它能证明：

- 真实实参求值和调用流程已经走通；
- 参数匹配成功；
- 函数体实际执行；
- 这一次没有未捕获异常阻止完成；
- 返回值在这一次满足所检查的预期。

但是一次成功仍然不能证明：

- 所有 locale 都成功；
- 所有文本内容都成功；
- 所有外部/业务状态都成功；
- 所有未来版本都成功；
- 所有分支、边界值和异常路径都正确。

所以它是**具体真实调用的执行证据**，但不是全输入空间的数学证明。

---

### 2. 第 5 条结论是否成立；最小补证方案

第 5 条：

> “一个样例成功，所以所有语言代码、所有文本对象、所有业务状态都一定成功。”

**不成立。**

这是把一个具体样例的证据强度过度外推为“所有输入、所有状态”的普遍结论。

题目并没有给出完整的业务输入域，所以不能凭空声称某些具体 locale 或状态必然属于支持集合。最小合理补证方式应是根据**真实业务合同**补充代表性调用，至少覆盖实际存在的不同等价类和边界，例如：

- 默认 `locale` 与若干明确支持的非默认 `locale`；
- 普通文本、带前后空白的文本；
- 若合同允许空文本，则增加空/极短文本；若不允许，则验证对应失败路径；
- 会进入不同业务分支的代表性状态；
- 合同定义的边界值与预期失败值。

如果真实系统声称支持一组固定的语言代码，那么应从这组**已定义集合**中取代表值甚至逐项测试；题目没有给出该集合时，不应自行虚构“所有语言”的枚举范围。

核心原则：

> 用多个有代表性的真实执行样例扩大证据覆盖，而不是把一次成功直接外推为普遍成功。

---

### 3. 第 2、3 条成功而第 4 条抛 `ValueError` 是否矛盾

不矛盾。

三条事实可以同时成立：

```text
inspect.signature(...) 成功
    ↓
当前 callable 可呈现签名

Signature.bind(...) 成功
    ↓
这组对象满足参数绑定合同

真实调用进入函数体后抛 ValueError
    ↓
业务/函数体运行合同失败
```

`bind()` 解决的是：

> “这些调用输入能否合法映射到参数？”

函数体内部的 `ValueError` 解决的是：

> “已经获得合法参数绑定后，这些具体值是否满足业务规则、以及实际计算能否完成？”

所以：

```text
绑定合同成功
≠
业务合同成功
```

完全没有逻辑矛盾。

---

### 4. 只允许选择一条最强的具体调用完成证据

应选择：

> **第 4 条：用这组实参真实调用一次，函数返回预期结果。**

因为它实际覆盖了：

```text
调用发生
→ 参数匹配
→ 函数体执行
→ 这一次业务路径完成
→ 得到预期结果
```

而 `bind()` 只到：

```text
给定对象
→ 参数形状可以映射
```

为止。

因此 `Signature.bind()` 很适合：

- 诊断调用形状；
- 提前发现参数合同错误；
- 做参数路由/包装工具的有限验证。

但它不能替代：

- 函数体的真实执行；
- 业务值校验；
- 外部状态交互；
- 返回值和副作用验证。

即使选择第 4 条，也只能称为“这个具体调用在当前状态下成功”的最强证据，不能自动升级为对所有可能输入的普遍保证。

<!-- answer:end -->

---

<!-- quiz-section: id=F score=16 -->
## F. 本地化记录 API 工程设计（16 分）

<!-- quiz-question: id=F1 score=16 -->
### F1（16 分）

你正在为本地化提示记录设计一个纯函数 `plan_record`。它只负责规范化输入并返回
计划字典，不读写文件、不打印、不修改全局状态。请实现并分析以下合同。

函数签名必须是：

~~~python
def plan_record(
    record_id,
    /,
    text,
    *tags,
    locale="en-US",
    dry_run=False,
    metadata=None,
):
    pass
~~~

实现要求：

- `record_id` 只能按位置提供；`text` 可以按位置或关键字提供。
- 任意额外位置实参由 `tags` 收集成元组。
- `locale`、`dry_run`、`metadata` 都是 keyword-only。
- 本题约定 `None` 不是合法的业务元数据；省略 `metadata` 时，每次调用都创建
  一个新的空字典。
- 显式传入元数据字典时，函数用 `dict(metadata)` 创建浅拷贝，不能直接修改
  调用者的顶层字典。
- 返回字典按顺序包含 `record_id`、`text`、`tags`、`locale`、`dry_run`、
  `metadata` 六个键；`text` 的值为 `text.strip()`，其他值来自绑定结果或上述
  元数据处理。
- 不增加 `**kwargs`，不做类型校验，也不引入本章范围外的装饰器或注解。

完成以下任务，各小项合计 16 分：

1. **实现（8 分）**：在答题区写出完整可运行函数。清楚呈现 `metadata is None`
   的分支、局部名字的重新绑定，以及返回字典。
2. **对象与结果（4 分）**：基于你的实现，写出下列四行精确输出，并解释顶层
   字典已复制、嵌套列表却仍共享的浅拷贝边界。

~~~python
source_metadata = {
    "reviewer": "qa",
    "channels": ["menu"],
}

planned = plan_record(
    "prompt-030",
    " Start ",
    "menu",
    "reviewed",
    locale="ja-JP",
    metadata=source_metadata,
)

planned["metadata"]["reviewer"] = "local"
planned["metadata"]["channels"].append("dialog")

print(planned)
print(source_metadata)
print(planned["metadata"] is source_metadata)
print(planned["metadata"]["channels"] is source_metadata["channels"])
~~~

3. **调用合同（4 分）**：逐个判断下列调用是成功还是在进入函数体前失败；成功
   时写出关键绑定，失败时指出参数合同原因，不要求精确异常文本。

   - `plan_record(record_id="prompt-031", text="Quit")`
   - `plan_record("prompt-032", "Quit", "fr-FR")`
   - `plan_record("prompt-033", "Quit", verbose=True)`

   特别说明第二个调用中的 `"fr-FR"` 为什么会进入 `tags`，而不是自动绑定
   `locale`；再说明这里保留 `*tags`、keyword-only 控制项且不提供 `**kwargs`
   对 API 可读性和拼写错误暴露各有什么作用。

<!-- answer:start -->

### 1. 完整可运行实现

```python
def plan_record(
    record_id,
    /,
    text,
    *tags,
    locale="en-US",
    dry_run=False,
    metadata=None,
):
    if metadata is None:
        metadata = {}
    else:
        metadata = dict(metadata)

    return {
        "record_id": record_id,
        "text": text.strip(),
        "tags": tags,
        "locale": locale,
        "dry_run": dry_run,
        "metadata": metadata,
    }
```

这里：

- `metadata is None` 时，在**本次调用期间**创建新空字典；

- 显式传入 mapping/dict 时，通过：

  ```python
  metadata = dict(metadata)
  ```

  创建新的**顶层浅拷贝字典**，并把本次调用的局部名字 `metadata` 重新绑定到副本；

- 没有修改全局状态，也没有打印或读写文件。

---

### 2. 四行精确输出、顶层复制与嵌套共享

调用结束并执行两次后续修改后，输出为：

```text
{'record_id': 'prompt-030', 'text': 'Start', 'tags': ('menu', 'reviewed'), 'locale': 'ja-JP', 'dry_run': False, 'metadata': {'reviewer': 'local', 'channels': ['menu', 'dialog']}}
{'reviewer': 'qa', 'channels': ['menu', 'dialog']}
False
True
```

#### 初始参数绑定

调用：

```python
planned = plan_record(
    "prompt-030",
    " Start ",
    "menu",
    "reviewed",
    locale="ja-JP",
    metadata=source_metadata,
)
```

得到：

```text
record_id -> "prompt-030"
text      -> " Start "
tags      -> ("menu", "reviewed")
locale    -> "ja-JP"
dry_run   -> False
metadata  -> source_metadata 所引用的原字典（函数入口时）
```

因为显式提供了 `metadata`，进入：

```python
metadata = dict(metadata)
```

创建新顶层字典 `Dcopy`，随后本次局部名字 `metadata` 改绑：

```text
source_metadata -> Dsource
metadata        -> Dcopy
```

二者是不同顶层字典：

```python
planned["metadata"] is source_metadata  # False
```

但 `dict(metadata)` 是**浅拷贝**。原字典中的嵌套列表对象没有被递归复制：

```text
Dsource["channels"] ──┐
                      v
                  list L ["menu"]
                      ^
Dcopy["channels"]  ───┘
```

所以：

```python
planned["metadata"]["channels"] is source_metadata["channels"]
```

为：

```text
True
```

#### 后续修改

```python
planned["metadata"]["reviewer"] = "local"
```

修改的是副本 `Dcopy` 的顶层键绑定，因此：

```text
Dcopy["reviewer"]   == "local"
Dsource["reviewer"] == "qa"
```

调用方原顶层字典对应值不变。

但：

```python
planned["metadata"]["channels"].append("dialog")
```

取得的是两份字典共同引用的同一个嵌套列表 `L`，并原地修改它：

```text
["menu"] -> ["menu", "dialog"]
```

所以两个顶层字典随后都显示：

```python
"channels": ["menu", "dialog"]
```

这正是浅拷贝的边界：

> 顶层容器已复制；内部成员对象仍按引用共享，除非另外显式复制它们。

---

### 3. 三个调用的合同分析

#### 调用 1

```python
plan_record(
    record_id="prompt-031",
    text="Quit",
)
```

**失败，在进入函数体前抛出 `TypeError`。**

原因：

```python
record_id
```

位于 `/` 前，是 positional-only parameter，不能通过：

```python
record_id="prompt-031"
```

这种关键字形式绑定。

`text="Quit"` 本身作为 positional-or-keyword parameter 的关键字传法是合法的，但这不能弥补必需 positional-only `record_id` 没有获得合法位置输入。

函数没有 `**kwargs`，也不存在其他机制可以把这个错误关键字“变成”位置输入。

---

#### 调用 2

```python
plan_record(
    "prompt-032",
    "Quit",
    "fr-FR",
)
```

**成功。**

关键绑定：

```text
record_id -> "prompt-032"
text      -> "Quit"
tags      -> ("fr-FR",)
locale    -> "en-US"
dry_run   -> False
metadata  -> 本次调用中新建的 {}
```

关键点是：

```python
*tags
```

已经开始收集在 `text` 之后继续出现的所有额外**位置输入**。

而：

```python
locale
```

位于 `*tags` 之后，是 keyword-only parameter，只能通过：

```python
locale="fr-FR"
```

这种关键字形式显式提供。

因此第三个裸位置实参 `"fr-FR"` 不会“跳过 `*tags` 自动绑定 locale”，而是进入：

```python
tags == ("fr-FR",)
```

`locale` 仍使用默认值 `"en-US"`。

返回结果为：

```python
{
    "record_id": "prompt-032",
    "text": "Quit",
    "tags": ("fr-FR",),
    "locale": "en-US",
    "dry_run": False,
    "metadata": {},
}
```

---

#### 调用 3

```python
plan_record(
    "prompt-033",
    "Quit",
    verbose=True,
)
```

**失败，在进入函数体前抛出 `TypeError`。**

`record_id` 和 `text` 都能正常获得绑定，但是：

```text
verbose=True
```

既不对应任何显式 parameter，也没有 `**kwargs` 可以收集，因此属于未知关键字输入，签名匹配失败。

---

### `*tags`、keyword-only 控制项和不提供 `**kwargs` 的 API 意义

保留：

```python
*tags
```

表达真实的开放位置合同：

> 一个记录可以有任意数量的额外标签；这些位置输入统一收集为 tuple。

把：

```text
locale
dry_run
metadata
```

放在 `*tags` 后成为 keyword-only，则强制调用点显式写出配置名称，例如：

```python
locale="ja-JP"
dry_run=True
metadata=...
```

这能避免把 `"ja-JP"`、`True`、某个 dict 等策略/控制值混在长串位置实参中，提高调用可读性，也避免配置位置随着 `tags` 数量变化而产生歧义。

同时不提供：

```python
**kwargs
```

意味着当前 API 是**封闭的关键字合同**。像：

```python
verbose=True
```

这样的未声明关键字或拼写错误会在参数匹配阶段尽早暴露，而不会被一个宽泛 `kwargs` 静默吸收。

因此这一设计同时表达：

```text
tags：数量开放，但语义明确
控制项：必须具名
其他未知关键字：拒绝
```

这比“为了灵活而全部接收”更清楚地暴露了函数真实支持的调用形状。

<!-- answer:end -->

---

## Codex 批改记录（逐题审批，2026-08-26）

### 1. 覆盖账本

本次按稳定题号从 A1 到 F1 审批，共覆盖 `11 / 11` 题。原答案区完整保留，未改写
任何作答正文。客观输出、异常、对象身份和实现行为均使用项目当前解释器
`.venv-py314\Scripts\python.exe`（CPython `3.14.5`）做了针对性复核。

| 题号 | 分值 | 原答案位置 | 审批状态 | 发现 |
| --- | ---: | --- | --- | --- |
| A1 | 7 | 第 110–232 行的原答案区 | 已审批，`6.75 / 7` | 核心模型正确；“同时”引用的时间线表述需要收紧 |
| A2 | 7 | 第 295–470 行的原答案区 | 已审批，`7 / 7` | 两段输出、失败阶段与异常前效果均正确 |
| B1 | 10 | 第 522–706 行的原答案区 | 已审批，`10 / 10` | 五类参数、绑定结果、语法标记和默认值维度均正确 |
| B2 | 8 | 第 750–932 行的原答案区 | 已审批，`8 / 8` | 六行输出及五类匹配失败全部正确 |
| C1 | 10 | 第 986–1203 行的原答案区 | 已审批，`10 / 10` | 默认对象创建、保存、复用和身份追踪均正确 |
| C2 | 8 | 第 1246–1422 行的原答案区 | 已审批，`8 / 8` | 修复实现、身份输出及显式对象边界均正确 |
| D1 | 10 | 第 1475–1632 行的原答案区 | 已审批，`9.75 / 10` | 结果正确；引用关系图的箭头方向可能造成反向理解 |
| D2 | 10 | 第 1691–1939 行的原答案区 | 已审批，`10 / 10` | 解包顺序、匹配冲突和部分效果均正确 |
| E1 | 8 | 第 1999–2237 行的原答案区 | 已审批，`8 / 8` | `bind()`、默认项和真实调用证据边界均正确 |
| E2 | 6 | 第 2265–2467 行的原答案区 | 已审批，`6 / 6` | 四层证据强度与业务合同限制均正确 |
| F1 | 16 | 第 2551–2890 行的原答案区 | 已审批，`15.75 / 16` | 实现与结果正确；初始参数绑定和函数体内重绑被合并 |

审批游标：`A1 -> A2 -> B1 -> B2 -> C1 -> C2 -> D1 -> D2 -> E1 -> E2 -> F1`，
已全部完成，没有未审批题目。

### 2. 逐题审批

#### A1：`6.75 / 7`

实参表达式、形参、本次调用中的四个完整局部名字、模块全局与 enclosing 层的区别、
身份结果和“形参绑定不复制对象”均回答正确。

扣 `0.25` 分的精度点在“同一个字典**同时**被 `shared_options`、`options`、
`local_options`、`result_options` 引用”。普通时间线中：

- 函数体执行时，`shared_options`、`options`、`local_options` 可以同时引用原字典，
  但调用方的结果解包赋值尚未发生；
- 函数返回并完成外层解包后，`shared_options` 与 `result_options` 引用原字典，
  而普通执行中的该次函数帧及其局部绑定已经结束。

因此最精确的结论是“同一对象在调用前后可先后被这些不同名字引用”，不能把跨阶段
出现的所有绑定画成必然同一时刻共存。你的主体结论——名字的局部性不是对象所有权——
仍然完全成立。

#### A2：`7 / 7`

Python `3.14.5` 实测两行分别为
`['target', 'key', 'locale:fail', 'caught:ValueError']` 和
`['target', 'key', 'locale', 'unknown', 'caught:TypeError']`，与答案一致。
第一段在实参值表达式中失败，后续 `unknown` 没有求值；第二段在全部输入形成后因
未知关键字匹配失败。两段都没有可进入函数体的成功调用帧、完整局部形参绑定或
`"body"` 事件，较早的列表修改也不会回滚。

非扣分边界：这里对“没有函数帧”的结论应继续限定为语言层可观察的成功调用帧、
完整绑定和函数体入口，不把它外推成对 CPython 内部临时分配步骤的实现保证。原答案
已经使用了“可进入函数体的成功调用帧”这一审慎表述。

#### B1：`10 / 10`

五类参数依次识别为 positional-only、positional-or-keyword、var-positional、
keyword-only、var-keyword；五个绑定值以及 `tuple` / `dict` 类型都与运行结果
一致。`/`、`*`、`**` 是签名语法组成，`record_id`、`tags`、`metadata` 等才是
局部形参名字。你还准确区分了 parameter kind 与 default 这两个独立维度。

#### B2：`8 / 8`

实测为五行 `TypeError` 后接 `[]`。五次失败依次是缺失必填、重复供值、未知关键字、
过多位置实参和 positional-only 误用。第二次的 `key=` 不是未知关键字，而是已经
由位置输入供值的显式形参再次收到值；它不会覆盖先前输入，也不能被不存在的
`**kwargs` 收留。`strict_entry` 四次都未进入函数体。

#### C1：`10 / 10`

六行输出与实测逐字一致。你准确追踪了 `make_history()` 在执行 `def` 时只运行一次、
函数对象保存默认列表、两次省略调用的不同函数帧把各自局部形参绑定到同一默认对象，
以及显式 `custom` 不替换 `__defaults__` 中对象的过程。

非扣分补充：默认列表跨调用共享不是 `global` / `nonlocal` 机制；与此同时，
`make_history()` 中通过模块全局名字取得 `definition_events` 后原地 `append()` 也
不需要 `global` 声明。后者是全局名字读取加共享对象修改，与默认对象复用是两条
不同的机制线。

#### C2：`8 / 8`

修复代码、三行输出及对象身份关系全部正确。省略调用分别创建新顶层字典和新列表；
显式字典未复制，调用者可以观察其中 `seen` 列表的修改。你也准确区分了对象创建、
局部名字重绑和共享对象修改。

非扣分措辞提示：答案中的 `None == “调用者未提供业务 options”` 应理解为
“本 API 合同把 `None` 解释为未提供”，不是一次 Python `==` 比较。实现实际使用
`options is None`，因此代码和身份边界均正确。

#### D1：`9.75 / 10`

七行输出、三个形参绑定、`tuple` / `dict` 类型、共享嵌套列表、`append()` 的修改
层级以及空收集值均正确。

扣 `0.25` 分的是图示方向。原图容易读成 `list L` 反向指向元组槽位和字典值；对象
模型应当是 `shared_channels`、`extra_keys[1]` 和 `controls["channels"]` 三个
名字或容器槽位都持有指向同一个列表 `L` 的引用。列表不会因为被引用而反向持有这些
名字或槽位。相邻正文和两个 `is` 结论是正确的，所以只作轻微精度扣分。

#### D2：`10 / 10`

两行事件序列与实测一致。第二次的关键字名称 `locale` 与 `dry_run` 本身并不重复；
冲突来自第二个位置输入已经为形参 `locale` 供值，显式 `locale=` 又为同一形参供值，
因此失败属于目标签名匹配，不是 `**` mapping 内部的同名关键字装配冲突。三个源
表达式及其副作用均已完成，函数体未进入，异常不回滚列表。

调用端 `**mapping` 只产生关键字调用输入，不会改变定义端签名或创造 `**kwargs`；
第一次调用产生的 `dry_run=True` 本来就能匹配显式 keyword-only 形参。

#### E1：`8 / 8`

六行输出与实测一致。`BoundArguments.arguments` 在没有调用 `apply_defaults()` 时
不自动加入省略的 `locale`；`bind()` 只检查交给它的对象能否满足呈现的签名，不
执行 `text.strip()`。真实调用则成功建立初始绑定并进入函数体，先追加事件，随后
才因整数没有 `strip()` 抛出 `AttributeError`。最后一次 `bind()` 因
positional-only 误用失败，但没有调用 `render` 或改变事件列表。

#### E2：`6 / 6`

你把源代码观察、运行时呈现签名、具体对象的模拟绑定、真实调用完成和普遍业务结论
分成了不同证据层，且没有把单一样例外推为所有输入。`bind()` 成功而函数体抛出
`ValueError` 不矛盾：前者满足绑定合同，后者暴露业务合同或函数体执行失败。

非扣分补充：`inspect.signature()` 描述的是当前呈现给 `inspect` 的签名；自定义
或陈旧的 `__signature__` 仍可能与实际调用合同偏离。你的“暴露/解析出一份
Signature”措辞已经保留了这一限制。

#### F1：`15.75 / 16`

函数签名、实现、四行输出、浅拷贝边界和三种调用成败均经 Python `3.14.5` 复核。
`*tags`、keyword-only 控制项和封闭关键字合同的 API 取舍也解释完整。

扣 `0.25` 分的是第二个调用的“关键绑定”时间线。对
`plan_record("prompt-032", "Quit", "fr-FR")`：

1. 签名匹配成功并进入函数体时，初始局部形参绑定包括
   `metadata -> None`；`locale -> "en-US"`、`dry_run -> False` 也来自默认对象；
2. 进入函数体后，`if metadata is None` 才创建新空字典；
3. `metadata = {}` 随后把局部名字从 `None` 重新绑定到该字典；
4. 返回结果中的 `metadata` 才是这个新字典。

原答案直接把 `metadata -> 本次调用中新建的 {}` 列在“关键绑定”中，合并了初始
参数绑定与函数体内后续重绑。实现和最终返回结果都正确，扣分只针对这一章最核心的
阶段边界。

非扣分边界：本题所称“纯函数”按题面限定为无 I/O、无打印、无全局修改且调用期间
不改写输入顶层字典。浅拷贝仍保留嵌套列表别名，因此不能把它提升为深层隔离或任意
后续操作都无可观察共享效果。

### 3. 分区与总分复核

| 分区 | 题目得分 | 分区得分 |
| --- | --- | ---: |
| A | A1 `6.75 / 7`；A2 `7 / 7` | `13.75 / 14` |
| B | B1 `10 / 10`；B2 `8 / 8` | `18 / 18` |
| C | C1 `10 / 10`；C2 `8 / 8` | `18 / 18` |
| D | D1 `9.75 / 10`；D2 `10 / 10` | `19.75 / 20` |
| E | E1 `8 / 8`；E2 `6 / 6` | `14 / 14` |
| F | F1 `15.75 / 16` | `15.75 / 16` |
| **合计** | **11 / 11 题已审批** | **`99.25 / 100`** |

核算结果：题目满分合计 `100`，三个扣分点各 `0.25`，总扣分 `0.75`；分区小计
再次相加为 `99.25`，与逐题得分一致。

### 4. 本阶段末评语与能力判断

结论：`C18_Arguments` 阶段测验通过，参数绑定主干达到**优秀**。当前能力判断保持
为“中级入门前段已经稳固”，并新增一条可靠证据：你已经能把对象—名字—作用域—
控制流模型迁移到完整调用合同，独立审查参数种类、默认对象、收集与解包、匹配失败、
异常前效果和签名证据强度。

稳定优势：

- 能按“目标与实参求值 → 调用端展开/装配 → 目标签名匹配 → 初始局部形参绑定 →
  函数体”追踪成功与失败路径；
- 能准确处理五类参数、`/`、`*`、`**`、缺失、重复、未知和过量输入；
- 能用定义时求值、函数对象保存和跨调用对象身份解释可变默认值，而不是误归因于
  `global` / `nonlocal`；
- 能区分定义端收集和调用端解包，并保留失败前已经完成的副作用；
- 能限制 `inspect.signature()`、`Signature.bind()`、单次真实调用和业务合同各自
  的证明范围；
- 能设计带 positional-only、keyword-only、浅拷贝和封闭关键字合同的小型接口。

当前精修点不是主干缺失，而是三项时间线/图示精度：

1. 不把函数体运行期的局部别名和调用返回后的调用方名字写成必然“同时”存在；
2. 引用图应由名字或容器槽位指向对象，不要画成对象反向指向引用持有者；
3. 先写参数匹配形成的初始绑定，再写函数体内部创建对象和局部重绑，不能把最终值
   倒填成函数入口时的绑定。

本次审批完成后，`quiz_review` 已满足；下一生命周期动作是 `stage_note`。这不等于
C18 已完成最终收束，也不授权提前开始 C19。

### 5. 学习画像更新（可复用）

**稳定强项**：参数五分类、完整调用时间线、默认对象生命周期、可变默认修复、
`*args` / `**kwargs` 收集、调用端 `*` / `**` 解包、失败前部分效果、浅拷贝对象
边界，以及签名观察/模拟绑定/真实调用的证据分层均达到优秀。

**活跃精修点**：继续把“某一时刻有哪些名字/槽位持有引用”“参数入口初始绑定”
“函数体内后续重绑”分别记录；画引用图时统一让箭头从引用持有者指向对象。`None`
作为未提供标记时，应说“合同解释为未提供并用 `is None` 检查”，不要写成 Python
相等性结论。

**水平判断**：保持“中级入门前段已经稳固”；C18 参数与调用合同主干达到优秀，
可以进入阶段末笔记，不需要补考或额外主线补救。

**下一阶段观察点**：阶段笔记应沉淀求值—装配—匹配—初始绑定—函数体时间线、
默认对象和收集/解包边界，并保留上述三项精修。高阶函数、系统闭包、生成器和基准
仍按后续章节推进，不因本次高分提前扩张。

### 6. 验证证据与限制

- 项目解释器：CPython `3.14.5`，路径
  `.venv-py314\Scripts\python.exe`；A1、A2、B1、B2、C1、C2、D1、D2、E1 和
  F1 的客观输出、异常或身份行为均已针对性运行，结果与原答案一致。
- 结构复核：6 个分区、11 道稳定题号、11 对答案标记；分区声明和题目声明均合计
  `100`，没有未填充的命题占位符。
- 技能验证器在追加批改前及最终复核时均已运行；结构和分值标记正常，但原答案中
  31 个用于解释的片段型普通 `python` 围栏不能作为独立模块编译，因此完整编译
  检查失败。为遵守
  “保留原始作答”，本次没有把这些答案围栏改成 `python no-compile`；该格式限制不
  影响已逐题运行的客观结论或评分。
- 本次未操作 `tests/`，也未清理或改写无关 dirty worktree。
