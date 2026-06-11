# C10 阶段小测：Python 语句导论

所属阶段：`P3_Statements_and_Syntax / C10_Introducing_Python_Statements`

生成日期：2026-06-10

满分：`100`

作答建议：

1. 先不要运行代码，先手工预测。
2. 用“题号 + 判断 + 理由”的形式作答。
3. 解释时优先使用这些边界：表达式求值、语句执行、返回值、副作用、输出、回显、代码块归属、控制流进入、`def` 执行与函数调用时间线。
4. 作答后可把答案追加到本文的“我的作答”区域，再交给 Codex 逐题批改。

---

## 一、概念辨析（25 分）

### 1. 表达式、语句、返回值和副作用

用自己的话区分：

- 表达式求值；
- 语句执行；
- 返回值；
- 副作用。

### 2. `print()` 的输出与返回值

为什么 `print("hello")` 的输出不是它的返回值？

### 3. 脚本执行与 REPL 回显

为什么脚本中的裸表达式不会自动显示，而 REPL 中通常会回显非 `None` 表达式值？

### 4. 物理行与逻辑行

说明“物理行”和“逻辑行”的区别，并分别举一个例子：

- 一条逻辑语句跨多条物理行；
- 一条物理行写多条简单语句。

### 5. 注释、普通字符串与文档字符串

为什么三引号字符串不等于注释？什么位置上的字符串字面量会成为文档字符串？

---

## 二、代码预测（30 分）

请预测完整脚本输出，并说明 `result` 最终绑定到什么对象。

```python
"""Checkpoint module."""

print("start")

def inspect_keys(source, target, verbose):
    """Inspect localization keys."""
    "ordinary string"

    events = []
    missing = source - target

    print(events.append("entered"))

    if verbose:
        print("source:", sorted(source))
        events.append("verbose")

    if missing:
        print("missing:", sorted(missing))
        status = "needs_fix"
    else:
        status = "ok"

    print(events)
    return status

print("after def")

result = inspect_keys(
    {"menu.start", "menu.quit", "menu.options"},
    {"menu.start", "menu.options"},
    False,
)

result
```

请回答：

1. 完整输出是什么？
2. 模块 `__doc__` 的值是什么？
3. `inspect_keys.__doc__` 的值是什么？
4. `"ordinary string"` 是否执行？是否是文档字符串？
5. `print(events.append("entered"))` 为什么输出 `None`？
6. `if verbose:` 块有没有执行？
7. 最后一行 `result` 在脚本中会不会自动显示？在 REPL 中呢？

---

## 三、执行时间线（25 分）

```python
print("A")

def outer(flag):
    """Outer doc."""
    print("B")

    if flag:
        return "early"

    print("C")
    return "late"

print("D")

value = outer(True)

print("E")
```

请回答：

1. 执行到 `def outer(flag):` 时，函数体里的 `print("B")` 会不会立刻执行？为什么？
2. 完整输出是什么？
3. `print("C")` 有没有执行？为什么？
4. `return "early"` 是表达式还是语句？它如何影响控制流？
5. `value` 最终绑定到什么对象？

---

## 四、工程场景分析（20 分）

假设你在写游戏本地化资源审计脚本：

```python
def report_missing(source_keys, target_keys, dry_run):
    missing = source_keys - target_keys

    if dry_run:
        print("DRY RUN")
        return "skipped"

    if missing:
        print("Missing keys:", sorted(missing))
        return "needs_fix"

    print("No missing keys")
    return "ok"
```

请解释：

1. `missing = source_keys - target_keys` 中，哪部分是表达式？整行是什么语句？
2. 当 `dry_run=True` 时，后面的 `if missing:` 有没有机会执行？为什么？
3. 当 `dry_run=False` 且 `missing` 非空时，输出和返回值分别是什么？
4. 为什么这里的 `print(...)` 是副作用，而 `return ...` 是控制流转移？
5. 如果你要把结果写进日志文件，为什么这会引入新的副作用边界？

---

## 我的作答

> ## 一、概念辨析（25 分）
>
> ### 1. 判断：表达式求值、语句执行、返回值和副作用是四个不同层次
>
> **理由：**
>
> #### 1.1 表达式求值
>
> 表达式是 Python 可以求值的源码片段。表达式被求值后，会得到某个对象。
>
> 例如：
>
> ```python
> 1 + 2
> ```
>
> 这里的 `1 + 2` 是表达式。它求值得到整数对象 `3`。
>
> 再如：
>
> ```python
> ["a", "b"]
> ```
>
> 这里的 `["a", "b"]` 是列表的字面量表达式。它求值得到列表对象 `['a', 'b']`。
>
> ------
>
> #### 1.2 语句执行
>
> 语句是 Python 程序执行的源码单位。语句可以包含表达式，但语句本身并不是“值”且并不总是“都会返回一个值”。
>
> 例如：
>
> ```python
> x = 1 + 2
> ```
>
> 整行是赋值语句。
>
> 其中：
>
> ```python
> 1 + 2
> ```
>
> 是表达式，求值得到 `3`。
>
> 然后赋值语句执行，让名字 `x` 绑定到整数对象 `3`。
>
> 所以这行代码的重点不是“赋值语句返回了什么”，而是“赋值语句改变了名字绑定关系”。同样的道理，其它类型的语句，如：if复合语句，它的重点或是说主要目的，是“通过条件判断的结果来影响程序的执行路径”，也不是“返回了或是求得了哪个值对象”。
>
> ------
>
> #### 1.3 返回值
>
> 返回值主要用于函数调用表达式，或者更准确的说，是函数内部的 `return` 语句。
>
> 例如：
>
> ```python
> len(["a", "b"])
> ```
>
> 这里的 `len(["a", "b"])` 是函数调用表达式，内置函数 `len` 调用返回实参对象的“长度”，在这里，表达式返回整数对象 `2`。
>
> 再如：
>
> ```python
> def f():
>     return "ok"
> ```
>
> 当调用：
>
> ```python
> f()
> ```
>
> 时，函数执行到：
>
> ```python
> return "ok"
> ```
>
> 函数调用表达式 `f()` 的结果就是字符串对象 `"ok"`。
>
> ------
>
> #### 1.4 副作用
>
> 副作用是指除了“求值得到结果”之外，求值过程中对外部状态或对象状态产生的可见影响。
>
> 例如：
>
> ```python
> print("hello")
> ```
>
> 它的副作用是向标准输出流写入文本 `hello`。
>
> 它的返回值是 `None`。
>
> 再如：
>
> ```python
> items.append("x")
> ```
>
> 它的副作用是原地修改 `items` 绑定的列表对象。
>
> 它的返回值也是 `None`。
>
> 所以一般原则是：源代码中一旦见到函数或方法调用的表达式，应分开问：
>
> ```text
> 1. 它返回什么？
> 2. 它有没有副作用？
> ```
>
> ------
>
> ### 2. 判断：`print("hello")` 的输出不是它的返回值
>
> **理由：**
>
> ```python
> print("hello")
> ```
>
> 是内置函数print的调用表达式。正如刚才所述，分两层分析：
>
> ```text
> 1. 副作用：把 hello 输出到标准输出流；
> 2. 返回值：返回 None。
> ```
>
> 所以如果写：
>
> ```python
> x = print("hello")
> print(x)
> ```
>
> 完整输出是：
>
> ```text
> hello
> None
> ```
>
> 第一行 `hello` 来自 `print("hello")` 的输出副作用。
>
> 第二行 `None` 说明 `print("hello")` 的返回值是 `None`，并且 `x` 被绑定到了这个 `None` 对象。
>
> 因此，屏幕上看到的 `hello` 不是 `print("hello")` 的返回值。
>
> ------
>
> ### 3. 判断：脚本中的裸表达式不会自动显示，REPL 中通常会回显非 `None` 表达式值
>
> **理由：**
>
> 在 `.py` 脚本中，裸表达式会被求值，但结果通常会被丢弃，不会自动显示。
>
> 例如脚本中写：
>
> ```python
> 1 + 2
> "hello".upper()
> print("done")
> ```
>
> 作为脚本运行时，只会输出：
>
> ```text
> done
> ```
>
> 但要注意的是：前两行不是没有执行，而是：
>
> ```text
> 1 + 2 求值得到 3，但因为值对象没有被表达式语句保存或使用，所以最终结果被丢弃；
> "hello".upper() 求值得到 "HELLO"，但因为值对象没有被表达式语句保存或使用，所以最终结果被丢弃；
> 脚本环境不会自动或主动显示裸表达式的结果。
> ```
>
> 但在 REPL 中，情况有所不同：
>
> ```python
> >>> 1 + 2
> 3
> >>> "hello".upper()
> 'HELLO'
> ```
>
> 这里看到的 `3` 和 `'HELLO'` 是交互式环境的自动回显，不是 `print()` 自动执行。
>
> REPL 的回显通常更接近 `repr(...)` 风格。例如：
>
> ```python
> >>> "hello"
> 'hello'
> ```
>
> 而：
>
> ```python
> >>> print("hello")
> hello
> ```
>
> `print()` 输出的是字符串内容本身，不带外层引号。
>
> 所以：
>
> ```text
> 脚本裸表达式：求值，但通常不显示；
> REPL 裸表达式：求值后通常回显非 None 结果；
> REPL 回显不是 print 输出。
> ```
>
> ------
>
> ### 4. 判断：物理行和逻辑行不是同一个概念
>
> **理由：**
>
> #### 4.1 物理行
>
> 物理行是编辑器中肉眼看到的一行。
>
> 例如：
>
> ```python
> x = 1
> y = 2
> ```
>
> 这里有两条物理行。
>
> ------
>
> #### 4.2 逻辑行
>
> 逻辑行是 Python 语法上认为的一条完整语句。
>
> 一条逻辑语句可以跨多条物理行。
>
> 例如：
>
> ```python
> config = {
>     "locale": "en",
>     "dry_run": True,
> }
> ```
>
> 这里有四条物理行，但语法上却是一条赋值语句。
>
> 赋值号右边的字典字面量处在 `{}` 内部，支持隐式续行，所以这仍然是一条逻辑语句。
>
> ------
>
> #### 4.3 一条逻辑语句跨多条物理行的例子
>
> ```python
> total = (
>     1
>     + 2
>     + 3
> )
> ```
>
> 这段代码占据五条物理行，但语法上是一条赋值语句。因为同样的道理，赋值号右边的数值运算表达式处在 `()` 内部，支持隐式续行，所以这仍然是一条逻辑语句。
>
> 执行后：
>
> ```python
> total == 6
> ```
>
> ------
>
> #### 4.4 一条物理行写多条简单语句的例子
>
> ```python
> x = 1; y = 2; print(x + y)
> ```
>
> 这是一条物理行，但里面有三条简单语句：
>
> ```python
> x = 1
> y = 2
> print(x + y)
> ```
>
> 输出是：
>
> ```text
> 3
> ```
>
> 不过工程中通常不推荐用分号把多条语句压在一行，因为可读性、调试性和版本控制 diff 可读性都会下降。
>
> ------
>
> ### 5. 判断：三引号字符串不等于注释；只有在模块、函数体、类的第一条语句位置上的字符串字面量才会成为文档字符串
>
> **理由：**
>
> 注释以 `#` 开头，不会作为运行时代码执行。
>
> 例如：
>
> ```python
> # This is a comment
> ```
>
> 这是真正的注释。
>
> 而三引号字符串是字符串字面量。
>
> 例如：
>
> ```python
> """This is a string."""
> ```
>
> 它本质上仍然是字符串对象的源码表示，不是注释。只是因为它作为裸表达式在脚本中通常不会有副作用，它求得的值对象也通常被丢弃，所以从观感上来说，在脚本程序执行过程中它的表现和注释的表现差异不明显，但并不能据此得出“三引号字符串等于注释”的结论，而且也不建议利用这一点来让脚本中的三引号字符串字面量裸表达式承担注释的作用。
>
> 如果它出现在特殊位置，就会成为文档字符串。
>
> 常见文档字符串位置包括：
>
> ```text
> 1. 模块开头的第一条语句；
> 2. 函数体开头的第一条语句；
> 3. 类体开头的第一条语句。
> ```
>
> 例如：
>
> ```python
> """Module docstring."""
>
> def f:
>     """Function docstring."""
>     pass
> ```
>
> 模块开头的字符串会成为模块的 `__doc__`。
>
> 函数体开头的字符串会成为函数对象的 `__doc__`。
>
> 但仍然要强调的是：普通位置上的三引号字符串既不是注释，也不是文档字符串。
>
> 例如：
>
> ```python
> print("start")
>
> """ordinary string"""
> ```
>
> 这里的三引号字符串只是普通字符串表达式语句。它可能被求值后丢弃，也可能在具体实现中被优化掉，但它不是注释。
>
> ------
>
> ## 二、代码预测（30 分）
>
> 题目代码：
>
> ```python
> """Checkpoint module."""
>
> print("start")
>
> def inspect_keys(source, target, verbose):
>     """Inspect localization keys."""
>     "ordinary string"
>
>     events = []
>     missing = source - target
>
>     print(events.append("entered"))
>
>     if verbose:
>         print("source:", sorted(source))
>         events.append("verbose")
>
>     if missing:
>         print("missing:", sorted(missing))
>         status = "needs_fix"
>     else:
>         status = "ok"
>
>     print(events)
>     return status
>
> print("after def")
>
> result = inspect_keys(
>     {"menu.start", "menu.quit", "menu.options"},
>     {"menu.start", "menu.options"},
>     False,
> )
>
> result
> ```
>
> ------
>
> ### 1. 判断：完整输出是
>
> ```text
> start
> after def
> None
> missing: ['menu.quit']
> ['entered']
> ```
>
> **理由：**
>
> 先按三层时间线分析。
>
> ------
>
> #### 1.1 编译阶段
>
> Python 先编译模块源码。
>
> 模块开头的：
>
> ```python
> """Checkpoint module."""
> ```
>
> 会被识别为模块文档字符串。
>
> 函数体开头的：
>
> ```python
> """Inspect localization keys."""
> ```
>
> 会被识别为函数文档字符串。
>
> 但是函数体不会在编译或 `def` 执行时立刻运行。
>
> ------
>
> #### 1.2 顶层执行阶段
>
> 第一条顶层语句：
>
> ```python
> """Checkpoint module."""
> ```
>
> 是模块文档字符串，不输出。
>
> 接着执行：
>
> ```python
> print("start")
> ```
>
> 输出：
>
> ```text
> start
> ```
>
> 然后执行函数定义：
>
> ```python
> def inspect_keys(source, target, verbose):
>     ...
> ```
>
> 执行 `def` 时会创建函数对象，并把名字 `inspect_keys` 绑定到该函数对象。
>
> 但是函数体不会立刻执行。
>
> 所以此时不会输出：
>
> ```text
> None
> ```
>
> 也不会输出：
>
> ```text
> missing: ...
> ```
>
> 接着执行：
>
> ```python
> print("after def")
> ```
>
> 输出：
>
> ```text
> after def
> ```
>
> 然后执行：
>
> ```python
> result = inspect_keys(
>     {"menu.start", "menu.quit", "menu.options"},
>     {"menu.start", "menu.options"},
>     False,
> )
> ```
>
> 这时才调用函数。
>
> ------
>
> #### 1.3 函数调用执行阶段
>
> 调用时：
>
> ```tex
> source被绑定到了集合对象{"menu.start", "menu.quit", "menu.options"}上；
> target被绑定到了集合对象{"menu.start", "menu.options"}上；
> verbose被绑定到了bool实例对象False上
> ```
>
> 然后控制流进入函数体。
>
> 函数文档字符串：
>
> ```python
> """Inspect localization keys."""
> ```
>
> 不产生输出。
>
> 普通字符串表达式：
>
> ```python
> "ordinary string"
> ```
>
> 不是文档字符串，也不产生可见输出。
>
> 接着执行：
>
> ```python
> events = []
> ```
>
> 此时：
>
> ```python
> events == []
> ```
>
> 执行：
>
> ```python
> missing = source - target
> ```
>
> 右边：
>
> ```python
> source - target
> ```
>
> 是集合差集的运算表达式。
>
> 它求值得到：
>
> ```python
> {"menu.quit"}
> ```
>
> 所以：missing被绑定在了集合对象{"menu.quit"}上。
>
> 然后执行：
>
> ```python
> print(events.append("entered"))
> ```
>
> 先求值内层实参：
>
> ```python
> events.append("entered")
> ```
>
> 这个方法调用表达式的求值过程会产生副作用：
>
> ```python
> events
> ```
>
> 从：
>
> ```python
> []
> ```
>
> 变成：
>
> ```python
> ["entered"]
> ```
>
> 但是 `list.append(...)` 的返回值是：
>
> ```python
> None
> ```
>
> 所以外层实际变成：
>
> ```python
> print(None)
> ```
>
> 所以输出：
>
> ```text
> None
> ```
>
> 然后执行：
>
> ```python
> if verbose:
> ```
>
> 因为verbose被绑定到了bool实例对象False上，所以`if verbose:`的真值测试不会通过，所以`if`块不会执行。
>
> 也就是说，下面两行都不会执行：
>
> ```python
> print("source:", sorted(source))
> events.append("verbose")
> ```
>
> 因此不会输出 `source: ...`，并且 `events` 也不会追加 `"verbose"`。
>
> 此时：
>
> ```python
> events == ["entered"]
> ```
>
> 接着执行：
>
> ```python
> if missing:
> ```
>
> 因为missing被绑定在了集合对象{"menu.quit"}上，所以`if missing:`的真值测试通过，所以控制流将进入`if`块执行：
>
> ```python
> print("missing:", sorted(missing))
> ```
>
> 其中：
>
> ```python
> sorted(missing)
> ```
>
> 返回列表：
>
> ```python
> ["menu.quit"]
> ```
>
> 所以输出：
>
> ```text
> missing: ['menu.quit']
> ```
>
> 然后执行：
>
> ```python
> status = "needs_fix"
> ```
>
> 于是：
>
> ```python
> status == "needs_fix"
> ```
>
> `else` 分支不会执行。
>
> 然后执行：
>
> ```python
> print(events)
> ```
>
> 此时：
>
> ```python
> events == ["entered"]
> ```
>
> 所以输出：
>
> ```text
> ['entered']
> ```
>
> 最后执行：
>
> ```python
> return status
> ```
>
> 返回：
>
> ```python
> "needs_fix"
> ```
>
> 所以函数调用表达式：
>
> ```python
> inspect_keys(...)
> ```
>
> 求值得到字符串对象：
>
> ```python
> "needs_fix"
> ```
>
> 外层赋值语句：
>
> ```python
> result = inspect_keys(...)
> ```
>
> 让：
>
> ```python
> result
> ```
>
> 绑定到：
>
> ```python
> "needs_fix"
> ```
>
> 最后一行：
>
> ```python
> result
> ```
>
> 是脚本中的裸表达式语句，不会自动显示。
>
> 所以完整脚本输出是：
>
> ```text
> start
> after def
> None
> missing: ['menu.quit']
> ['entered']
> ```
>
> ------
>
> ### 2. 判断：模块 `__doc__` 的值是 `"Checkpoint module."`
>
> **理由：**
>
> 模块最开头的字符串字面量是：
>
> ```python
> """Checkpoint module."""
> ```
>
> 它位于模块第一条语句的位置，因此在源码编译阶段它就被识别为模块的文档字符串，当模块执行时模块对象的属性 `__doc__ `将指向这个表达式求值所得的字符串对象。
>
> 所以模块的：
>
> ```python
> __doc__
> ```
>
> 是：
>
> ```python
> "Checkpoint module."
> ```
>
> 注意，它不会通过标准输出流显示出来，除非显式写：
>
> ```python
> print(__doc__)
> ```
>
> ------
>
> ### 3. 判断：`inspect_keys.__doc__` 的值是 `"Inspect localization keys."`
>
> **理由：**
>
> 函数体开头的第一条语句是：
>
> ```python
> """Inspect localization keys."""
> ```
>
> 由于它所处位置的特殊性，这个表达式语句的核心表达式`"""Inspect localization keys."""`求得的值在源码编译阶段就被识别为函数的文档字符串，尽管它是函数体内的语句，但是，在函数体真正执行之前（即执行def复合语句创建函数对象之时）它的核心表达式的求值结果就已经作为函数元数据被保存了（创建的函数对象的属性 `__doc__` 将指向这个字符串结果对象）。
>
> 所以函数对象创建后：
>
> ```python
> inspect_keys.__doc__
> ```
>
> 的值是：
>
> ```python
> "Inspect localization keys."
> ```
>
> ------
>
> ### 4. 判断：`"ordinary string"` 在源码语义上会在函数调用执行到该行时作为普通表达式语句处理；它不是文档字符串
>
> **理由：**
>
> 函数体开头的第一条语句已经是：
>
> ```python
> """Inspect localization keys."""
> ```
>
> 所以函数的文档字符串是"Inspect localization keys."。
>
> 而后面的：
>
> ```python
> "ordinary string"
> ```
>
> 不是函数体中的第一条语句，因此它的求值结果不是文档字符串。
>
> 从 C10 的读代码模型看，它是普通字符串表达式语句。
>
> 它只有在函数被调用，并且执行流走到这一行时，才会作为普通表达式语句被处理。
>
> 其结果没有被保存、没有被 `print()` 输出，也没有作为函数的返回值返回，所以没有可见效果。
>
> 补充说明：在具体实现中，例如 CPython，像这种无副作用的裸表达式语句可能被优化掉，不一定真的在运行时创建一个新的字符串对象；但从源码语义和 C10 阶段读代码角度，应把它判断为“普通字符串表达式语句，既不是文档字符串，也不产生输出”。
>
> ------
>
> ### 5. 判断：`print(events.append("entered"))` 输出 `None`
>
> **理由：**
>
> 这一行要从内向外读：
>
> ```python
> print(events.append("entered"))
> ```
>
> 先执行参数表达式：
>
> ```python
> events.append("entered")
> ```
>
> 要注意此时：
>
> ```python
> events == []
> ```
>
> 表达式求值过程中发生副作用：
>
> ```python
> events == ["entered"]
> ```
>
> 但是 `list.append(...)` 的返回值是：
>
> ```python
> None
> ```
>
> 所以外层实际是：
>
> ```python
> print(None)
> ```
>
> 因此输出：
>
> ```text
> None
> ```
>
> 关键边界是：
>
> ```text
> append 的副作用：原地修改列表；
> append 的返回值：None；
> print 输出的是 append 的返回值 None。
> ```
>
> ------
>
> ### 6. 判断：`if verbose:` 块没有执行
>
> **理由：**
>
> 函数调用时第三个参数是：
>
> ```python
> False
> ```
>
> 所以函数内部：
>
> ```tex
> verbose被绑定到了bool实例对象False上
> ```
>
> 执行到：
>
> ```python
> if verbose:
> ```
>
> 时，真值测试未通过。
>
> 因此以下代码块不会执行：
>
> ```python
> print("source:", sorted(source))
> events.append("verbose")
> ```
>
> 所以完整输出中不会出现：
>
> ```text
> source: ...
> ```
>
> 并且 `events` 中也不会出现：
>
> ```python
> "verbose"
> ```
>
> 最终 `events` 还是：
>
> ```python
> ["entered"]
> ```
>
> ------
>
> ### 7. 判断：最后一行 `result` 在脚本中不会自动显示；在 REPL 中会自动回显
>
> **理由：**
>
> 在脚本中：
>
> ```python
> result
> ```
>
> 是裸表达式语句。
>
> 它会求值，得到字符串对象：
>
> ```python
> "needs_fix"
> ```
>
> 但是结果没有被保存、没有传给 `print()`，脚本环境也不会主动显示或自动回显，所以没有输出。
>
> 如果在 REPL 中，在已经执行过：
>
> ```python
> result = inspect_keys(...)
> ```
>
> 之后单独输入：
>
> ```python
> result
> ```
>
> 则交互式环境通常会回显：
>
> ```python
> >>> result
> 'needs_fix'
> ```
>
> 注意，REPL 回显通常接近 `repr(result)`，所以会显示带引号的：
>
> ```text
> 'needs_fix'
> ```
>
> 而如果写：
>
> ```python
> print(result)
> ```
>
> 则输出是：
>
> ```text
> needs_fix
> ```
>
> ------
>
> ## 三、执行时间线（25 分）
>
> 题目代码：
>
> ```python
> print("A")
>
> def outer(flag):
>     """Outer doc."""
>     print("B")
>
>     if flag:
>         return "early"
>
>     print("C")
>     return "late"
>
> print("D")
>
> value = outer(True)
>
> print("E")
> ```
>
> ------
>
> ### 1. 判断：执行到 `def outer(flag):` 时，函数体里的 `print("B")` 不会立刻执行
>
> **理由：**
>
> 执行 `def` 语句时，Python 会创建函数对象，并把名字：
>
> ```python
> outer
> ```
>
> 绑定到这个函数对象。
>
> 但是函数体不会在函数定义阶段运行。
>
> 所以函数体中的：
>
> ```python
> print("B")
> ```
>
> 不会在执行 `def outer(flag):` 时立刻执行。
>
> 它只有在函数被调用，并且执行流走到函数体中的这一行时才会执行，例如：
>
> ```python
> outer(True)
> ```
>
> 这也说明 `def` 执行与函数调用执行是两个不同阶段。
>
> ------
>
> ### 2. 判断：完整输出是
>
> ```text
> A
> D
> B
> E
> ```
>
> **理由：**
>
> 按顶层执行顺序分析。
>
> 第一条语句：
>
> ```python
> print("A")
> ```
>
> 输出：
>
> ```text
> A
> ```
>
> 接着执行：
>
> ```python
> def outer(flag):
>     ...
> ```
>
> 只创建函数对象，不执行函数体，所以此时不会输出 `B`。
>
> 然后执行：
>
> ```python
> print("D")
> ```
>
> 输出：
>
> ```text
> D
> ```
>
> 接着执行：
>
> ```python
> value = outer(True)
> ```
>
> 调用函数。
>
> 函数调用时：
>
> ```tex
> flag被绑定到了bool实例对象True上
> ```
>
> 然后控制流进入函数体。
>
> 函数文档字符串：
>
> ```python
> """Outer doc."""
> ```
>
> 不输出。
>
> 然后执行：
>
> ```python
> print("B")
> ```
>
> 输出：
>
> ```text
> B
> ```
>
> 接着执行：
>
> ```python
> if flag:
> ```
>
> 因为flag被绑定在了bool实例对象True上，所以`if flag:`的真值测试通过，所以控制流将进入`if`块执行：
>
> ```python
> return "early"
> ```
>
> 函数立刻返回 `"early"`。
>
> 因此后面的：
>
> ```python
> print("C")
> return "late"
> ```
>
> 不会执行。
>
> 回到顶层后，`value` 被绑定到 `"early"`。
>
> 最后执行：
>
> ```python
> print("E")
> ```
>
> 输出：
>
> ```text
> E
> ```
>
> 因此完整输出是：
>
> ```text
> A
> D
> B
> E
> ```
>
> ------
>
> ### 3. 判断：`print("C")` 没有执行
>
> **理由：**
>
> 函数调用是：
>
> ```python
> outer(True)
> ```
>
> 所以函数内部：
>
> ```tex
> flag被绑定到了bool实例对象True上
> ```
>
> 执行到：
>
> ```python
> if flag:
>     return "early"
> ```
>
> 时，`if flag:`的真值测试通过，函数执行：
>
> ```python
> return "early"
> ```
>
> 而`return` 会立即结束当前函数调用阶段，并把返回值交给调用者。
>
> 因此控制流不会继续往下走到：
>
> ```python
> print("C")
> ```
>
> 所以 `print("C")` 没有执行。
>
> ------
>
> ### 4. 判断：`return "early"` 是 return 语句，不是普通表达式；其中 的`"early"` 才是表达式
>
> **理由：**
>
> 整行：
>
> ```python
> return "early"
> ```
>
> 是 `return` 语句。
>
> 其中：
>
> ```python
> "early"
> ```
>
> 是字符串字面量表达式。
>
> 执行 `return "early"` 时，会先对其中的字符串字面量表达式求值得到：字符串对象 `"early"`，然后立即结束当前函数调用阶段，并把这个字符串对象作为函数调用的返回值交给调用者。
>
> 所以它对控制流的影响是：
>
> ```text
> 1. 结束当前函数的调用阶段；
> 2. 跳过函数体中 return 后面的语句；
> 3. 把 "early" 作为函数调用结果返回给调用者。
> ```
>
> 因此：
>
> ```python
> print("C")
> return "late"
> ```
>
> 都不会执行。
>
> ------
>
> ### 5. 判断：`value` 最终绑定到字符串对象 `"early"`
>
> **理由：**
>
> 顶层语句：
>
> ```python
> value = outer(True)
> ```
>
> 中，右边：
>
> ```python
> outer(True)
> ```
>
> 是函数调用表达式。
>
> 函数执行时，因为 `flag` 指向 `True`，所以执行：
>
> ```python
> return "early"
> ```
>
> 所以函数调用表达式 `outer(True)` 求值得到字符串对象：
>
> ```python
> "early"
> ```
>
> 于是赋值语句让：
>
> ```python
> value
> ```
>
> 绑定到：
>
> ```python
> "early"
> ```
>
> ------
>
> ## 四、工程场景分析（20 分）
>
> 题目代码：
>
> ```python
> def report_missing(source_keys, target_keys, dry_run):
>     missing = source_keys - target_keys
>
>     if dry_run:
>         print("DRY RUN")
>         return "skipped"
>
>     if missing:
>         print("Missing keys:", sorted(missing))
>         return "needs_fix"
>
>     print("No missing keys")
>     return "ok"
> ```
>
> ------
>
> ### 1. 判断：`source_keys - target_keys` 是表达式；整行 `missing = source_keys - target_keys` 是赋值语句
>
> **理由：**
>
> 这一行是：
>
> ```python
> missing = source_keys - target_keys
> ```
>
> 右边：
>
> ```python
> source_keys - target_keys
> ```
>
> 是集合差集的运算表达式。
>
> 如果：
>
> ```tex
> source_keys被绑定到了集合对象{"a", "b", "c"}上；
> target_keys被绑定到了集合对象{"a", "c"}上
> ```
>
> 那么：
>
> ```python
> source_keys - target_keys
> ```
>
> 求值得到：
>
> ```python
> {"b"}
> ```
>
> 整行：
>
> ```python
> missing = source_keys - target_keys
> ```
>
> 是赋值语句。
>
> 它会先执行右边表达式求值，然后把名字：
>
> ```python
> missing
> ```
>
> 绑定到求值结果。
>
> 所以这里要区分：
>
> ```text
> source_keys - target_keys：表达式，负责求值；
> missing = ...：赋值语句，负责让 missing 绑定结果对象。
> ```
>
> ------
>
> ### 2. 判断：当 `dry_run=True` 时，后面的 `if missing:` 没有机会执行
>
> **理由：**
>
> 当调用函数时：
>
> ```tex
> dry_run已被绑定在了bool实例对象True上
> ```
>
> 函数先执行：
>
> ```python
> missing = source_keys - target_keys
> ```
>
> 然后执行：
>
> ```python
> if dry_run:
> ```
>
> 因为`if dry_run:`的真值测试会通过，所以控制流进入归属于这个if复合语句的缩进代码块：
>
> ```python
> print("DRY RUN")
> return "skipped"
> ```
>
> 先执行：
>
> ```python
> print("DRY RUN")
> ```
>
> 输出：
>
> ```text
> DRY RUN
> ```
>
> 然后执行：
>
> ```python
> return "skipped"
> ```
>
> `return` 会立即结束当前的函数调用阶段。
>
> 因此控制流不会继续往下执行到：
>
> ```python
> if missing:
> ```
>
> 所以当 `dry_run=True` 时，后面的 `if missing:` 没有机会执行。
>
> 这体现了控制流转移：
>
> ```text
> return 一旦执行，当前函数调用阶段会立即结束；
> 后续语句不会继续执行。
> ```
>
> ------
>
> ### 3. 判断：当 `dry_run=False` 且 `missing` 非空时，会输出缺失键列表，并返回 `"needs_fix"`
>
> **理由：**
>
> 假设已有：
>
> ```tex
> source_keys被绑定在了集合对象{"menu.start", "menu.quit", "menu.options"}上；
> target_keys被绑定在了集合对象{"menu.start", "menu.options"}上；
> dry_run被绑定在了bool实例对象False上
> ```
>
> 那么先执行：
>
> ```python
> missing = source_keys - target_keys
> ```
>
> 得到：missing被绑定在集合对象{"menu.quit"}上。
>
> 然后执行：
>
> ```python
> if dry_run:
> ```
>
> 因为：dry_run被绑定在了bool实例对象False上，`if dry_run:`的真值测试不会通过，所以控制流会跳过归属于这个if复合语句的缩进代码块：
>
> ```python
> print("DRY RUN")
> return "skipped"
> ```
>
> 继续执行：
>
> ```python
> if missing:
> ```
>
> 因为：missing被绑定在了集合对象{"menu.quit"}上，`if missing:`的真值测试会通过，所以控制流进入归属于这个if复合语句的缩进代码块，于是执行：
>
> ```python
> print("Missing keys:", sorted(missing))
> return "needs_fix"
> ```
>
> 其中：
>
> ```python
> sorted(missing)
> ```
>
> 返回列表：
>
> ```python
> ["menu.quit"]
> ```
>
> 所以输出：
>
> ```text
> Missing keys: ['menu.quit']
> ```
>
> 然后：
>
> ```python
> return "needs_fix"
> ```
>
> 使函数返回字符串对象：
>
> ```python
> "needs_fix"
> ```
>
> 因此基于当前给定的背景下：
>
> ```text
> 输出：Missing keys: ['menu.quit']
> 返回值："needs_fix"
> ```
>
> 如果 `missing` 中有多个元素，`sorted(missing)` 会返回默认按字典顺序排列后的列表，实际输出内容取决于缺失键集合的具体内容。
>
> ------
>
> ### 4. 判断：这里的 `print(...)` 是副作用，而 `return ...` 是控制流转移
>
> **理由：**
>
> 例如：
>
> ```python
> print("Missing keys:", sorted(missing))
> ```
>
> 这行的核心是 `print(...)` 调用。
>
> 它会向标准输出流写入文本。
>
> 这属于副作用，因为它改变了程序外部可观察的状态：用户在屏幕或控制台上看到了输出内容。
>
> 但是 `print(...)` 的返回值通常是：
>
> ```python
> None
> ```
>
> 所以它的主要价值不是返回值，而是输出副作用。
>
> ------
>
> 而：
>
> ```python
> return "needs_fix"
> ```
>
> 是 `return` 语句。
>
> 它不是普通表达式语句。
>
> 它的执行效果是：
>
> ```text
> 1. 立即结束当前函数调用阶段；
> 2. 把 "needs_fix" 作为函数调用的返回值交给调用者；
> 3. 阻止函数继续执行后续语句。
> ```
>
> 所以 `return ...` 的核心是控制流转移和返回函数结果。
>
> 因此：
>
> ```text
> print(...)：产生输出副作用；
> return ...：结束函数并返回对象，是控制流转移。
> ```
>
> ------
>
> ### 5. 判断：如果把结果写进日志文件，会引入新的副作用边界
>
> **理由：**
>
> 当前函数中：
>
> ```python
> print(...)
> ```
>
> 的副作用主要是向标准输出流写入文本。
>
> 但如果改成把结果写入日志文件，例如：
>
> ```python
> with open("audit.log", "a", encoding="utf-8") as f:
>     f.write("Missing keys...\n")
> ```
>
> 或者使用日志系统：
>
> ```python
> logger.info("Missing keys: %s", sorted(missing))
> ```
>
> 就会引入新的副作用边界。
>
> 原因是写日志可能涉及：
>
> ```tex
> 1. 文件系统状态变化；
> 2. 文件内容可能被追加，也可能是覆盖；
> 3. 编码问题；
> 4. 缓冲区刷新问题；
> 5. 路径是否存在的问题
> ```

---

## Codex 批改记录（逐题审批，2026-06-10）

### 总评

建议得分：`96 / 100`

审批结论：通过。当前答案已经达到 `C10_Introducing_Python_Statements` 小阶段收束要求，可以进入 C10 收束整理，并准备生成 C11 启动模板。

本次主要强项：

- 能稳定区分表达式求值、语句执行、函数调用返回值和副作用。
- 能正确预测 `print(...)`、`list.append(...)`、`sorted(...)`、`if` 分支和 `return` 对输出与执行路径的影响。
- 能把 `def` 执行与函数调用执行分开说明，明确函数体不会在执行 `def` 时立即运行。
- 能把脚本裸表达式与 REPL 回显分开说明，且能指出 REPL 通常显示 `repr(...)` 风格结果。
- 能在本地化资源审计语境中解释集合差集、缺失键报告、`dry_run` 早返回和日志副作用边界。

需要精修的地方：

1. `def f:` 是语法笔误，应写为 `def f():`。这不影响你对文档字符串概念的主干理解，但作为阶段测验答案，示例代码必须能被 Python 解析。
2. 文档字符串不要长期用“普通表达式求值后保存到 `__doc__`”来解释。更稳说法是：位于模块、类或函数体第一条语句位置的字符串字面量会被 Python 作为 docstring 特殊处理；模块对象或函数对象的 `__doc__` 指向对应字符串对象。
3. “函数调用的返回值”与“`return` 语句”之间的关系可以再压实：`return` 是控制流转移语句；函数调用表达式的值来自被调用函数执行到的 `return`，若没有显式返回则通常是 `None`。

---

### 一、概念辨析（23 / 25）

#### 1. 表达式、语句、返回值和副作用

评分：`5 / 5`

审批：通过。

你的区分是准确的：表达式求值得到对象，语句是 Python 程序执行的源码单位，副作用是求值或执行过程中对外部状态或已有对象产生的可观察影响。你把 `items.append("x")` 拆成“原地修改列表 + 返回 `None`”非常到位。

轻微补充：返回值不只在“函数内部的 `return` 语句”这一层讨论。更完整的链路是：

```text
return 语句决定函数调用表达式的结果；
函数调用表达式本身作为表达式，会求值得到这个返回对象。
```

#### 2. `print()` 的输出与返回值

评分：`5 / 5`

审批：通过。

你用：

```python
x = print("hello")
print(x)
```

解释 `hello` 是输出副作用、`x` 绑定到 `None`，判断完全正确。

#### 3. 脚本执行与 REPL 回显

评分：`5 / 5`

审批：通过。

你准确指出脚本裸表达式会求值但不自动显示，REPL 会回显非 `None` 表达式值，且回显通常接近 `repr(...)` 风格。这里没有扣分。

#### 4. 物理行与逻辑行

评分：`5 / 5`

审批：通过。

你的例子覆盖了括号内隐式续行和分号分隔简单语句，并且补充了工程上不推荐把多条语句压在一行的理由。判断准确。

#### 5. 注释、普通字符串与文档字符串

评分：`3 / 5`

审批：主干通过，但有两个需要显式纠正的点。

问题 1：示例代码存在语法笔误：

```python
def f:
    """Function docstring."""
    pass
```

应改为：

```python
def f():
    """Function docstring."""
    pass
```

问题 2：你说普通位置的三引号字符串“求得的值对象通常被丢弃”，作为 C10 读代码模型可以接受；但更严谨地说，像这种无副作用的普通字符串表达式语句在具体实现中可能被优化掉，不应把“运行时一定创建字符串对象再丢弃”当作语言语义保证。你后面已经提到了这个边界，说明主干理解是稳的。

修正规则：

```text
# 注释：源码说明，不是字符串字面量。
普通字符串表达式语句：源码语义上是表达式语句，不是注释。
docstring：模块、类、函数体第一条语句位置上的字符串字面量，被特殊处理为 __doc__。
```

---

### 二、代码预测（29 / 30）

#### 1. 完整输出

评分：`6 / 6`

审批：通过。

你预测的完整输出正确：

```text
start
after def
None
missing: ['menu.quit']
['entered']
```

执行顺序分析也正确：先执行顶层 `print("start")`，执行 `def` 只创建函数对象，不执行函数体；调用 `inspect_keys(...)` 后才进入函数体。

#### 2. 模块 `__doc__`

评分：`4 / 4`

审批：通过。

模块 `__doc__` 的值是：

```python
"Checkpoint module."
```

你没有把三引号源码形式误写成字符串内容，这是正确的。

#### 3. `inspect_keys.__doc__`

评分：`3 / 4`

审批：主干正确，措辞扣 1 分。

你判断 `inspect_keys.__doc__ == "Inspect localization keys."` 正确。

需要纠正的是这句模型：

```text
它的核心表达式的求值结果就已经作为函数元数据被保存了
```

更稳说法：

```text
函数体第一条语句位置的字符串字面量被识别为函数 docstring；
执行 def 创建函数对象时，函数对象的 __doc__ 指向该字符串对象；
这不是普通函数体语句在函数调用时执行后的结果。
```

#### 4. `"ordinary string"` 是否执行，是否是文档字符串

评分：`4 / 4`

审批：通过。

你说它不是文档字符串，并且只有函数被调用、控制流走到该行时才按普通表达式语句处理，这个边界非常好。你还主动补充 CPython 可能优化无副作用裸表达式语句，这个补充是加分项。

#### 5. `print(events.append("entered"))`

评分：`4 / 4`

审批：通过。

你正确拆出了执行顺序：

```text
events.append("entered") 先执行；
events 被原地修改为 ["entered"]；
append 返回 None；
print(None) 输出 None。
```

#### 6. `if verbose:` 块是否执行

评分：`4 / 4`

审批：通过。

你用“`verbose` 绑定到 `False`，真值测试不通过”来解释，而不是写成 `verbose == False`，表述准确。

#### 7. 最后一行 `result`

评分：`4 / 4`

审批：通过。

你正确区分了脚本中裸表达式不自动显示，以及 REPL 中会回显类似 `repr(result)` 的形式。`'needs_fix'` 与 `print(result)` 输出 `needs_fix` 的差异也说明得清楚。

---

### 三、执行时间线（25 / 25）

#### 1. 执行到 `def outer(flag):` 时是否执行函数体

评分：`5 / 5`

审批：通过。

你准确说明：执行 `def` 创建函数对象并绑定名字，函数体不在函数定义阶段运行。

#### 2. 完整输出

评分：`5 / 5`

审批：通过。

输出预测正确：

```text
A
D
B
E
```

#### 3. `print("C")` 是否执行

评分：`5 / 5`

审批：通过。

你正确指出 `return "early"` 结束当前函数调用，因此控制流不会继续走到 `print("C")`。

#### 4. `return "early"` 是表达式还是语句

评分：`5 / 5`

审批：通过。

你说整行是 `return` 语句，其中 `"early"` 是字符串字面量表达式，这个拆分准确。你对控制流影响的三点总结也正确。

#### 5. `value` 最终绑定对象

评分：`5 / 5`

审批：通过。

`value` 最终绑定到字符串对象 `"early"`，判断正确。

---

### 四、工程场景分析（19 / 20）

#### 1. 表达式与赋值语句

评分：`4 / 4`

审批：通过。

`source_keys - target_keys` 是集合差集表达式；整行 `missing = source_keys - target_keys` 是赋值语句。你的解释准确。

#### 2. `dry_run=True` 时后续 `if missing:` 是否执行

评分：`4 / 4`

审批：通过。

你正确指出 `return "skipped"` 会立即结束当前函数调用，因此后面的 `if missing:` 没有机会执行。

#### 3. `dry_run=False` 且 `missing` 非空时的输出和返回值

评分：`4 / 4`

审批：通过。

你给出的输出与返回值正确：

```text
输出：Missing keys: ['menu.quit']
返回值："needs_fix"
```

也正确补充了如果缺失键不止一个，实际输出取决于 `sorted(missing)` 的排序结果。

#### 4. `print(...)` 与 `return ...`

评分：`4 / 4`

审批：通过。

你把 `print(...)` 归为输出副作用，把 `return ...` 归为控制流转移和函数结果返回，表述准确。

#### 5. 日志文件副作用边界

评分：`3 / 4`

审批：主干通过，建议补全边界。

你已经指出日志写入会引入文件系统状态、写入模式、编码、缓冲刷新和路径存在性问题。建议再补两类工程边界：

- 权限与失败路径：日志路径不可写、磁盘满、文件被占用时，写日志可能失败。
- 处理器边界：如果使用 `logging`，输出目标未必是普通文件，也可能是控制台、轮转文件、网络、队列或外部日志系统。

这不是 C10 的核心扣分点，但能帮助你把“副作用边界”迁移到后续异常、日志和工程化阶段。

---

## 本阶段末评语与能力判断

你已经通过 C10 阶段小测。当前对 Python 语句导论的核心模型已经比较稳定：

```text
表达式求值 -> 得到对象或触发副作用；
语句执行 -> 组织名字绑定、控制流、输出和返回；
代码块归属 -> 由缩进语法表达；
代码块是否执行 -> 由控制流决定；
def 执行 -> 创建函数对象；
函数调用 -> 才执行函数体；
return -> 结束当前函数调用并给调用表达式提供结果。
```

你的答案显示，C10 的主线已经不再停留在“背输出结果”，而是能按对象、名字绑定、执行路径和副作用边界逐层解释。尤其 `append()` / `print()` / `return` 的组合题、`if` 早返回路径、脚本与 REPL 差异、docstring 与普通字符串表达式的区别，都已经达到进入下一章的要求。

当前仍需持续警惕的细点：

- 文档字符串是特殊位置字符串字面量的特殊处理，不要长期套用“普通表达式求值产生副作用”的模型。
- 示例代码要保持可解析，避免 `def f:` 这类小语法笔误干扰概念表达。
- 后续进入 C11 后，赋值语句、增强赋值、链式赋值和表达式语句会继续挑战“表达式有值，语句组织动作”这个边界。

结论：`C10_Introducing_Python_Statements` 建议通过，可以进入小阶段收束整理，并准备开启 `C11_Assignments_Expressions_and_Prints`。

---

## 学习画像更新

阶段：`P3_Statements_and_Syntax / C10_Introducing_Python_Statements`

证据：

- 已完成 C10 阶段小测，建议得分 `96 / 100`。
- 能独立解释表达式求值、语句执行、返回值、副作用、脚本回显、REPL 回显、物理行、逻辑行、缩进代码块、`def` 时间线、函数调用和 `return` 控制流转移。
- 能在游戏本地化资源审计场景中解释集合差集、缺失键输出、`dry_run` 早返回和日志文件副作用边界。

稳定强项：

- 对 `print()` 输出与返回值、`append()` 原地修改与返回 `None` 的边界掌握稳定。
- 能用“名字绑定到对象”解释赋值语句结果，而不是把语句误说成普通值。
- 能正确追踪 `if` 分支、`return` 早返回和函数调用表达式最终绑定对象。
- 能区分脚本裸表达式不显示与 REPL 回显非 `None` 表达式值。

仍需关注：

- 文档字符串的解释要保持“特殊位置 + 字符串字面量 + `__doc__` 元数据”模型。
- 后续 C11 学习赋值与输出时，要继续避免把语句效果说成“语句返回值”。
- 遇到工程副作用时，要逐渐补入失败路径、权限、编码、缓冲和外部系统边界。

当前能力判断：

你已经完成从 P2 对象模型到 P3 语句层模型的第一步迁移。当前水平可以判断为：**C10 语句导论已通过，具备进入 C11 赋值、表达式语句与输出专题的条件**。
