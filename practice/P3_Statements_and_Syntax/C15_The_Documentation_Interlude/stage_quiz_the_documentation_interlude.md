# C15 The Documentation Interlude 阶段测验

<!-- quiz-validator: total=100 -->

本卷用于验收 `P3_Statements_and_Syntax / C15_The_Documentation_Interlude`，
并以 `PART closer` 的职责抽查 C10-C15 的统一自查能力。总分 `100` 分。

## 冻结命题蓝图

考察范围：

- C15 核心：注释、普通字符串表达式、文档字符串、`__doc__`、`dir()`、
  `help()`、`pydoc`、官方文档、签名、版本范围与当前解释器最小实验；
- P3 综合：表达式与语句、绑定与修改、真值与分支、循环退出、迭代消费、
  结构化返回值与展示副作用；
- 工程迁移：为真实只读代码建立“主张—证据—限制—下一验证”报告；
- P4 仅考交接问题的识别，不考参数绑定、LEGB、闭包等尚未系统学习的机制。

明确排除：数据库连接或修改、未排期 capstone、P4 系统教学内容，以及与本章
目标无关的高级反射、描述符实现和静态类型工具细节。

| 分区 | 主题 | 题型 | 分值 |
| --- | --- | --- | ---: |
| A | 文档层级与证据来源 | 概念解释、源码分类 | 18 |
| B | 名称发现、属性访问与契约边界 | 代码预测、边界审查 | 18 |
| C | `help()`、`pydoc` 与官方文档 | 代码预测、证据判断 | 20 |
| D | 签名、版本与最小实验 | 调用形状、惰性失败、验证设计 | 16 |
| E | C10-C15 对象与控制流综合 | 代码阅读、状态追踪 | 18 |
| F | 工程证据报告与 P4 交接 | 综合设计 | 10 |
| **合计** |  |  | **100** |

## 作答说明

1. 请保留题号、分值标记与 HTML 注释；在每题的
   `answer:start` / `answer:end` 之间作答。
2. 代码预测题先写精确结果，再解释表达式求值、对象状态、控制流或证据边界。
3. 输出格式受环境影响时，应区分稳定语义与偶然排版，不必死记整段帮助文本。
4. 可以运行最小实验核对，但须保留“验证前判断”和“验证后修正”。

---

<!-- quiz-section: id=A score=18 -->
## A. 文档层级与证据来源（18 分）

<!-- quiz-question: id=A1 score=8 -->
### A1. 源码位置与 `__doc__`（8 分）

假设下面的源码保存为 `catalog_probe.py`，随后被正常导入：

```python
# Translator-facing note: keep the placeholder unchanged.
"""Helpers for a small localization catalog."""

"This is an ordinary module-level string expression."


def lookup(key):
    """Return a demonstration value for key."""

    "This later string is not the function docstring."
    return f"value:{key}"


def late_documentation():
    marker = "assignment is the first statement"
    """This string appears too late to become function metadata."""
    return marker
```

不运行代码，回答：

1. `catalog_probe.__doc__`、`lookup.__doc__` 和
   `late_documentation.__doc__` 分别是什么类型、什么值？
2. 注释、模块中的第二个字符串表达式、`lookup()` 内的第二个字符串表达式，
   哪些属于源码事实，哪些会进入对应对象的 `__doc__`？
3. 若用 `ast.parse()` 查看模块顶层，注释是否会成为一条 AST 语句？两个模块级
   字符串分别会以什么语句形态出现？
4. 用一句规则说明“字符串字面量”成为 docstring 所必须满足的位置条件。

评分关注：三个 `__doc__` 判断 4 分；源码、AST 与元数据分层 2 分；位置规则
及术语精度 2 分。

#### 你的作答

<!-- answer:start -->

### 1. 三个 `__doc__` 的类型和值

在“正常导入”且未使用会移除 docstring 的特殊优化方式这一前提下：

| 对象                      | `__doc__` 的类型 | `__doc__` 的值                                |
| ------------------------- | ---------------- | --------------------------------------------- |
| `catalog_probe` 模块      | `str`            | `'Helpers for a small localization catalog.'` |
| `lookup` 函数             | `str`            | `'Return a demonstration value for key.'`     |
| `late_documentation` 函数 | `NoneType`       | `None`                                        |

原因是模块体第一条实际语句是字符串字面量表达式，所以它成为模块 docstring；
`lookup()` 函数体第一条实际语句也是字符串字面量表达式，所以它成为函数 docstring。
`late_documentation()` 的第一条语句却是赋值语句：

```python
marker = "assignment is the first statement"
```

后面的字符串出现得太晚，只是普通字符串表达式语句，不会补写函数的 `__doc__`。

### 2. 源码事实与对象元数据的分层

三者都是可在源文件中直接看到的**源码事实**：

```python
# Translator-facing note: keep the placeholder unchanged.
"This is an ordinary module-level string expression."
"This later string is not the function docstring."
```

但它们都不会进入题目所问对象的 `__doc__`：

- 普通 `#` 注释不是模块 docstring，也不会成为模块对象的 `__doc__`；
- 模块中的第二个字符串表达式不是模块体第一条语句，因此不会成为模块 docstring；
- `lookup()` 内的第二个字符串表达式位于函数 docstring 之后，因此只是普通表达式语句。

这里必须区分：

```tex
源码中存在
≠
成为运行时对象的文档元数据
```

### 3. `ast.parse()` 中的形态

普通注释不会成为一条普通 AST 语句；标准 AST 主要描述 Python 的语法结构，
并不会为这里的普通 `#` 注释产生一个 `ast.stmt` 节点。

两个模块级字符串都会表现为顶层表达式语句，其大致形态分别是：

```python
ast.Expr(
    value=ast.Constant(
        value="Helpers for a small localization catalog."
    )
)
```

以及：

```python
ast.Expr(
    value=ast.Constant(
        value="This is an ordinary module-level string expression."
    )
)
```

二者 AST 节点类别相同；第一个之所以同时具有 docstring 身份，是因为它位于
`Module.body` 的首个语句位置，而不是因为它使用了三引号。

### 4. 一句话规则

> 一个字符串字面量表达式只有在模块、类或函数主体中占据规定的首条语句位置时，
> 才成为该主体的 docstring；引号形式本身不能决定它是不是 docstring。

<!-- answer:end -->

<!-- quiz-question: id=A2 score=10 -->
### A2. 主张属于哪一层证据（10 分）

某位开发者为同一个 `lookup_text` 函数记录了六条观察：

```tex
① Path(module.__file__).read_text(...) 中能找到一条 # FIXME 注释
② lookup_text.__doc__ 是一个 str
③ help(lookup_text) 在终端显示了函数名、签名和说明文字
④ lookup_text("menu.start") 返回 "Start"
⑤ 当前官方文档说明参数 fallback 是关键字参数，并列出了版本变化
⑥ Python 3.14.5 的最小实验得到预期返回值，并记录了 sys.executable
```

请建立一张“主张—证据层—不能证明什么”的简表，逐项回答：

1. ①至⑥分别主要属于源码文本、对象元数据、工具显示输出、业务返回对象、
   外部官方合同还是当前运行期观察中的哪一层？必要时可以说明一条观察横跨两层，
   但必须指出主证据是什么。
2. 每项至少写出一个不能由它单独推出的结论。例如：看到签名不等于证明调用
   无副作用；当前一次成功也不等于证明所有输入或未来版本都相同。
3. 如果旧书、搜索摘要、当前官方文档和 Python 3.14.5 实验彼此不一致，给出
   一个有限的核对顺序，并说明最终结论需要标注哪些版本/环境信息。

评分关注：证据层分类 4 分；每层能力边界 4 分；冲突核对顺序与环境记录 2 分。

#### 你的作答

<!-- answer:start -->

### 1～2. “主张—证据层—不能证明什么”简表

| 编号 | 主张/观察                                               | 主证据层                                             | 它单独不能证明什么                                           |
| ---: | ------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
|    ① | 用 `Path(...).read_text()` 能在文件中找到 `# FIXME`     | **源码文本层**                                       | 不能证明注释会进入 `module.__doc__`；不能证明运行时导入的是这份文件；不能证明注释描述的缺陷仍真实存在或相关代码一定会执行。 |
|    ② | `lookup_text.__doc__` 是 `str`                          | **对象元数据层**                                     | 不能证明说明文字完整、正确或最新；不能证明函数调用签名、返回值、异常和副作用；也不能仅凭此证明其来源一定是当前磁盘文件中的可见 docstring。 |
|    ③ | `help(lookup_text)` 在终端显示函数名、签名和说明        | **工具显示输出层**，其原料横跨对象元数据和运行期内省 | 不能证明整段排版是稳定机器接口；不能证明显示签名涵盖全部业务语义；不能证明调用没有副作用，也不能证明所有环境的 pager、标题和缩进相同。 |
|    ④ | `lookup_text("menu.start")` 返回字符串 `"Start"`        | **业务调用的返回对象层**；同时也是一次运行期行为     | 不能证明所有输入均返回相同类型；不能证明没有发生输出、状态修改或 I/O；不能证明未来版本或另一解释器仍相同。 |
|    ⑤ | 当前官方文档说明 `fallback` 的参数规则并列出版本变化    | **外部官方合同层**                                   | 不能单独证明本机实际导入的对象就是该文档对应版本；不能证明第三方包装器没有改写行为；签名和参数说明也不能代替本机对导入路径及异常时机的核验。 |
|    ⑥ | Python 3.14.5 最小实验得到预期值并记录 `sys.executable` | **当前运行期观察层**                                 | 不能自动升级为所有 Python 版本、实现、平台和输入上的语言保证；一次成功不能覆盖错误路径、边界输入、并发状态或未来补丁版本。 |

进一步说，④和⑥都涉及运行时，但主视角不同：④强调函数给调用者交付的业务对象；
⑥强调带有解释器和环境记录的可复现实验结果。

### 3. 多来源冲突时的有限核对顺序

建议采用以下顺序，而不是凭来源“名气”任选一个结论：

1. **先确认当前对象身份和环境**：记录 `type(obj)`、`obj.__module__`、必要时
   `module.__file__`，以及 `sys.version`、`sys.implementation.name`、
   `sys.executable`；先解决“实际运行的是谁”。
2. **阅读与目标版本匹配的当前官方参考文档**：优先确认对象类型、正式签名、
   参数语义、返回值、异常、副作用、Added/Changed/Deprecated 信息和实现说明。
3. **用 `inspect.signature()`、`__doc__`、`help()` 等调查本机对象**：它们是线索和
   当前对象证据，但不把帮助文本排版当成合同。
4. **在 Python 3.14.5 中设计最小实验**：分别覆盖正常路径和关键错误路径，记录
   完整输入、返回对象、输出、副作用、异常类型及异常时机。
5. **回看旧书和搜索摘要**：把它们作为历史或检索线索；若与当前证据不同，标注
   它适用的版本，或明确写成“旧资料已漂移”，而不是让它覆盖当前官方合同。
6. **仍有冲突时**：继续查目标补丁版本的变更记录、官方 issue/CPython 源码；
   源码用于解释当前实现，除非官方文档承诺，否则不自动写成跨实现保证。

最终结论至少应记录：

```tex
Python 完整版本与发布级别
Python 实现（如 CPython）
解释器绝对路径
操作系统/关键运行环境
被调查模块的来源路径和版本（可取得时）
官方文档所属版本
最小实验输入、完整结果或异常
结论层级：语言保证 / 标准库合同 / CPython 3.14.5 观察 / 项目业务规则
仍未证明的边界
```

<!-- answer:end -->

---

<!-- quiz-section: id=B score=18 -->
## B. 名称发现、属性访问与契约边界（18 分）

<!-- quiz-question: id=B1 score=8 -->
### B1. `dir()` 与动态属性代码预测（8 分）

预测下面五行 `print()` 的布尔结果，并解释每个结果由哪次协议调用产生：

```python
class Catalog:
    version = "1.0"

    def lookup(self, key):
        return f"value:{key}"

    def __getattr__(self, name):
        if name == "runtime_alias":
            return lambda key: self.lookup(key)
        raise AttributeError(name)

    def __dir__(self):
        names = set(super().__dir__())
        names.add("advertised_only")
        return sorted(names)


catalog = Catalog()

print("advertised_only" in dir(catalog))
print(hasattr(catalog, "advertised_only"))
print("runtime_alias" in dir(catalog))
print(hasattr(catalog, "runtime_alias"))
print(callable(catalog.version))
```

除精确输出外，还须说明：

- `dir()`、`hasattr()` 和 `callable()` 分别实际检查了什么；
- 为什么 `hasattr()` 本身会触发属性访问代码，以及它遇到
  `AttributeError` 与其它异常时的边界；
- 这段代码如何同时构成“出现在 `dir()` 中但不可访问”和“可访问但未出现在
  `dir()` 中”两个反例。

评分关注：五行输出 3 分；协议轨迹 3 分；`hasattr()` 异常边界和两个反例 2 分。

#### 你的作答

<!-- answer:start -->

### 精确输出

```tex
True
False
False
True
False
```

### 协议调用与逐行解释

#### 第一行

```python
"advertised_only" in dir(catalog)
```

`dir(catalog)` 调用自定义的 `Catalog.__dir__()`。该方法先调用
`super().__dir__()` 收集默认候选名称，再人为加入 `"advertised_only"`，最后返回
排序列表，所以成员测试结果为 `True`。

这一步只证明该字符串出现在 `dir()` 报告的候选名称中。

#### 第二行

```python
hasattr(catalog, "advertised_only")
```

`hasattr()` 会真正尝试执行相当于 `getattr(catalog, "advertised_only")` 的正常属性
访问。常规查找没有找到该属性，于是调用：

```python
catalog.__getattr__("advertised_only")
```

`__getattr__()` 对该名字抛出 `AttributeError`；`hasattr()` 将这一个异常解释为属性
不可取得，因此结果为 `False`。

#### 第三行

```python
"runtime_alias" in dir(catalog)
```

再次调用 `Catalog.__dir__()`。该方法只额外加入了 `advertised_only`，没有把
`runtime_alias` 加入列表；默认 `dir()` 也无法预知纯粹由 `__getattr__()` 动态生成的
该名称，因此结果为 `False`。

#### 第四行

```python
hasattr(catalog, "runtime_alias")
```

`hasattr()` 真实执行属性访问。常规查找失败后调用：

```python
catalog.__getattr__("runtime_alias")
```

这次返回一个 `lambda` 对象，没有抛出 `AttributeError`，所以 `hasattr()` 返回
`True`。此处 `hasattr()` 并不会调用该 lambda，只取得它。

#### 第五行

```python
callable(catalog.version)
```

先正常访问 `catalog.version`，通过类属性得到字符串 `"1.0"`；随后 `callable()`
检查这个字符串对象是否看起来可调用。字符串不可调用，所以结果为 `False`。
`callable()` 没有调用该对象，也没有证明任何特定参数调用能够成功。

### 三个工具分别检查什么

- `dir(obj)`：尝试报告适合继续调查的候选名称；这里还执行了自定义 `__dir__()`。
- `hasattr(obj, name)`：真正执行正常属性读取，并检查是否抛出 `AttributeError`。
- `callable(obj)`：检查对象是否具有可调用能力；即使结果为真，实际调用仍可能因
  参数、对象状态或函数体逻辑失败。

`hasattr()` 只将 `AttributeError` 转换为 `False`。如果 getter、descriptor、
`__getattribute__()` 或 `__getattr__()` 抛出 `RuntimeError`、`ValueError` 等其它异常，
该异常会继续传播，而不会被统一改成 `False`。

### 两个反例

本题同时证明：

```tex
advertised_only：出现在 dir() 中，但实际属性访问失败。
runtime_alias：不在 dir() 中，但正常属性访问成功。
```

因此：

```tex
名称被 dir() 发现
既不是属性可访问的充分条件，也不是必要条件。
```

<!-- answer:end -->

<!-- quiz-question: id=B2 score=10 -->
### B2. 从名称发现到可调用合同（10 分）

审查下面的插件调用：

```python
if "export" in dir(plugin):
    plugin.export("result.json")
```

作者声称：“`dir()` 已经证明 `export` 存在，而且没有下划线，所以可以安全按
公开 API 调用。”请完成一次有限合同审查：

1. 指出这两行代码仍未证明的至少六项事实。至少覆盖：属性是否真的可取得、
   属性访问是否会执行代码、取得的对象是否可调用、调用形状与参数语义、公开
   API/版本范围，以及文件或状态副作用。
2. 特别区分：
   - “名称被发现”与“属性可访问”；
   - “属性可访问”与“对象可调用”；
   - “调用形状能绑定”与“业务合同正确”；
   - “一次调用成功”与“无破坏性副作用”。
3. 在不真正写出 `result.json` 的前提下，提出一个从低风险证据到受控最小实验的
   验证顺序。说明哪一步只读、哪一步可能执行用户代码，以及为何不能把
   `Protocol`、ABC 或名字风格当成自动的运行期完整合同验证器。

评分关注：未经证明的合同项 4 分；四组边界 3 分；安全验证顺序及工具局限 3 分。

#### 你的作答

<!-- answer:start -->

### 1. 仍未证明的合同事实

```python
if "export" in dir(plugin):
    plugin.export("result.json")
```

至少没有证明以下事项：

1. `dir(plugin)` 的结果是否完整、准确；对象可能自定义 `__dir__()`，能够遗漏或编造
   名称，并且调用 `dir()` 本身也可能执行用户代码。
2. `"export"` 是否真的能通过正常属性访问取得；即便名字被报告，getter 或
   `__getattr__()` 仍可能抛出 `AttributeError`。
3. 访问 `plugin.export` 是否会触发 property、descriptor、延迟加载、网络请求、
   缓存修改或其它用户代码。
4. 取得的对象是否可调用；它可能只是字符串、配置对象或数据字段。
5. 即使 `callable()` 为真，也没有证明它接受一个位置参数；可能要求关键字参数、
   其它必需参数，或根本没有可内省签名。
6. 字符串参数的**业务语义**没有被证明：它可能是文件路径、URL、资源标识、目录、
   格式名，或只接受某种扩展名和编码。
7. `export` 是否为受支持的公共 API；不以下划线开头只是命名启发式，不等于文档和
   兼容性承诺。
8. 该接口适用于哪些插件版本、Python 版本和平台，是否已弃用或行为曾变化。
9. 返回值、异常类型、失败后的状态和是否支持重试均未证明。
10. 调用是否会创建/覆盖 `result.json`、创建目录、修改插件状态、写数据库、发送
    网络请求、输出日志，或产生部分写入。
11. 一次成功调用是否可重复、是否幂等、是否会保留打开的资源，也都未知。

### 2. 四组边界

#### 名称被发现与属性可访问

```tex
"export" in dir(plugin)
```

只说明名称出现在候选列表中。真正的：

```python
getattr(plugin, "export")
```

可能失败，反之动态属性也可能可访问却不出现在 `dir()` 中。

#### 属性可访问与对象可调用

属性读取成功只得到一个对象；还要单独判断 `callable(member)`。但 `callable()` 为真
仍不保证某个具体实参组合有效。

#### 调用形状能绑定与业务合同正确

`inspect.signature(member).bind(...)` 至多证明实参在参数数量、位置和关键字形式上
能够匹配签名。它不执行函数体，也不证明路径语义正确、文件允许覆盖、编码正确、
权限足够、返回类型符合预期或调用没有副作用。

#### 一次调用成功与无破坏性副作用

成功返回只能说明该次执行没有以未处理异常终止。它仍可能已经覆盖文件、修改状态、
写日志或数据库、发送网络请求，甚至成功返回本来就是这些副作用完成后的信号。

### 3. 从低风险证据到受控最小实验

建议按以下风险递增顺序调查：

1. **读项目 README、插件文档、版本说明和类型存根**：文件读取本身不调用插件
   方法，主要取得声明的公共入口、版本范围、参数和副作用说明；但文档可能过期。

2. **读取模块源码并用 AST/文本定位 `export` 定义**：这是源码层只读分析，不执行
   模块；可查看 docstring、装饰器、是否明显调用文件 API，但不能证明动态运行结果。

3. **确认当前对象身份和版本**：记录 `type(plugin)`、模块名、模块文件和包版本。
   注意：若插件尚未导入，导入会执行模块顶层代码，不是纯静态操作；应在隔离进程、
   禁止 `.pyc` 写入并有文件系统基线的条件下进行。

4. **有限静态属性调查**：

   ```python no-compile
   raw_export = inspect.getattr_static(plugin, "export")
   ```

   它尽量避免正常 descriptor 绑定和动态属性逻辑，但可能返回原始 descriptor，且
   不保证发现纯 `__getattr__()` 属性。

5. **查看文档和签名**：优先对类上的原始成员或已知函数对象使用
   `inspect.getdoc()`、官方文档和 `inspect.signature()`。这些步骤通常不调用
   `export` 函数体，但对任意恶意对象仍不能称为安全沙箱；签名也可能不可用。

6. **仅做调用形状验证**：若签名可得，使用：

   ```python no-compile
   signature.bind(temp_output_path)
   ```

   这不会执行 `export`，只检查参数绑定。

7. **受控最小执行**：不要传入真实 `result.json`。在一次性临时目录、一次性插件
   实例或子进程中传入临时输出路径；运行前后快照临时目录、插件可观察状态和任何
   被允许访问的持久化路径，并设置超时。明确标注：此步骤会执行用户代码，仍可能
   产生超出预期的副作用，所以只能在隔离和授权边界内进行。

8. **核对结果**：检查返回对象、临时文件字节、异常、输出以及状态变化；销毁临时
   环境，不能把临时成功直接推广到生产路径和全部输入。

`Protocol`、ABC 和名字风格都不能自动完成运行期完整合同验证：

- ABC 或 `isinstance()` 主要说明名义/注册关系或一组有限协议条件；
- 可运行时检查的 Protocol 至多能检查一部分结构存在性，不会自动执行并验证所有
  参数语义、返回值、错误路径和副作用；
- 非下划线名字只是惯例。

完整合同仍需文档、版本、对象身份、签名、受控实验和副作用证据共同支持。
<!-- answer:end -->

---

<!-- quiz-section: id=C score=20 -->
## C. `help()`、`pydoc` 与官方文档（20 分）

<!-- quiz-question: id=C1 score=9 -->
### C1. 帮助文本的输出与返回边界（9 分）

阅读下面的完整程序：

```python
from contextlib import redirect_stdout
from io import StringIO
import pydoc


def lookup_text(key, *, fallback=""):
    """Return a demonstration translation or fallback."""

    translations = {"menu.start": "Start"}
    return translations.get(key, fallback)


buffer = StringIO()
with redirect_stdout(buffer):
    help_result = help(lookup_text)

help_text = buffer.getvalue()
rendered = pydoc.render_doc(lookup_text, renderer=pydoc.plaintext)

print(help_result is None)
print(type(help_text).__name__)
print(bool(help_text))
print(lookup_text.__doc__ == help_text)
print(type(rendered).__name__)
print(lookup_text("menu.unknown", fallback="<missing>"))
```

1. 写出六行输出。对第二、三、五行只需给出这里可稳定判断的值，不必复刻帮助
   文本的完整排版。
2. 按执行顺序说明 `redirect_stdout` 捕获了什么；`help_result`、`help_text`、
   `rendered` 和最后一次业务调用分别绑定到什么类型的对象。
3. 为什么 `lookup_text.__doc__ == help_text` 不能因为两者都“包含文档”就判断为
   `True`？
4. 列出至少两项可能随终端、pager 或 Python 版本变化的展示细节，以及两项本题
   应坚持验证的稳定语义。

评分关注：输出 3 分；对象与输出/返回轨迹 3 分；docstring/帮助展示边界 2 分；
稳定语义与偶然格式 1 分。

#### 你的作答

<!-- answer:start -->

### 1. 六行精确输出

```tex
True
str
True
False
str
<missing>
```

### 2. 执行顺序、捕获内容与各名字的绑定

1. `buffer = StringIO()` 创建一个内存文本流对象。

2. 进入 `redirect_stdout(buffer)` 上下文后，当前进程在该上下文中的
   `sys.stdout` 被临时重定向到 `buffer`。

3. `help(lookup_text)` 生成面向人读的帮助内容，并把相应文本写入当前标准输出，
   因而该文本被 `buffer` 捕获；`help()` 调用本身返回 `None`，所以：

   ```python no-compile
   help_result is None
   ```

4. 离开上下文后恢复原标准输出。`buffer.getvalue()` 返回已经捕获的完整文本字符串，
   因而 `help_text` 绑定到一个非空 `str`。

5. `pydoc.render_doc(...)` 生成文本文档并**作为返回值**交付，因此 `rendered` 也绑定
   到一个 `str`；该行默认不会把 `rendered` 自动打印到控制台。

6. 最后调用：

   ```python no-compile
   lookup_text("menu.unknown", fallback="<missing>")
   ```

   字典中没有该键，所以业务调用返回字符串 `"<missing>"`，随后外层 `print()` 将其
   显示。

因此四个关键对象为：

| 名字             | 绑定对象                               |
| ---------------- | -------------------------------------- |
| `help_result`    | `None`，类型 `NoneType`                |
| `help_text`      | 捕获到的非空帮助文本，类型 `str`       |
| `rendered`       | `pydoc` 返回的人读文本文档，类型 `str` |
| 最后业务调用结果 | `'<missing>'`，类型 `str`              |

`redirect_stdout()` 捕获的是上下文期间写入当前 `sys.stdout` 的内容，不是只为
`help()` 定制的特殊返回通道；它不等于捕获 `stderr`、子进程输出或所有系统级输出。

### 3. 为什么比较结果为 `False`

```python
lookup_text.__doc__
```

是原始 docstring 元数据，其值只是：

```tex
Return a demonstration translation or fallback.
```

而 `help_text` 是 `pydoc` 组织后的完整帮助页文本，通常还包含对象类别、函数名、
签名、标题、换行和缩进等信息。即使帮助页把 docstring 作为原料纳入，它也不等于
原始 docstring 本身，所以两者的字符串内容不相等，结果为 `False`。

### 4. 易变的展示细节与稳定语义

可能变化的展示细节至少包括：

- 标题、大小写、空行数量和缩进；
- 函数签名在帮助页中的换行方式；
- pager 是否启用及分页提示；
- 终端宽度造成的折行；
- 不同 Python 补丁版本对成员说明和标题的排版。

本题应坚持验证的稳定语义至少包括：

- `help(lookup_text)` 产生帮助显示副作用，而其返回值是 `None`；
- 捕获结果 `help_text` 是非空 `str`；
- `pydoc.render_doc(...)` 返回 `str`；
- 未知键配合该 `fallback` 返回 `'<missing>'`；
- 原始 `__doc__` 与完整帮助页不是同一个观察层。

<!-- answer:end -->

<!-- quiz-question: id=C2 score=11 -->

### C2. 官方文档与本机证据的分工（11 分）

团队准备把终端中的 `help(some_api)` 文本逐行解析成自动调用规则；同时，他们
从一篇旧文章中看到的参数列表与当前环境不一致。请提出一份证据审查方案：

1. 分别说明 `some_api.__doc__`、`help(some_api)`、
   `pydoc.render_doc(some_api)`、`inspect.signature(some_api)`、官方文档和当前
   最小实验最适合回答的问题，以及各自不能替代哪一层证据。
2. 说明为什么逐行解析 `help()` 的标题、缩进和空行属于脆弱做法；若确实需要
   程序可消费的文本，`pydoc.render_doc()` 改善了哪一个边界，又仍然没有提供
   哪些完整合同保证。
3. 针对旧文章与当前环境冲突，按顺序核对以下合同字段：对象类型、签名、参数
   语义、返回值、异常、副作用、版本变化、实现说明。写明哪些优先从官方文档
   读取，哪些必须由当前解释器观察补充。
4. 给出最终实验记录的最小字段，至少包括 Python 版本、实现、解释器路径、实验
   输入、稳定结果或异常，以及所依据的官方文档入口。

评分关注：六类工具/来源分工 4 分；帮助文本格式边界 2 分；合同字段与冲突
核对顺序 3 分；可复现实验记录 2 分。

#### 你的作答

<!-- answer:start -->

### 1. 六类工具/来源的最适合用途与不可替代边界

| 工具或来源                    | 最适合回答的问题                                             | 不能替代什么                                                 |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `some_api.__doc__`            | 当前对象暴露的原始文档元数据是什么；是否为 `str` 或 `None`   | 不能替代完整签名、版本历史、正式返回/异常/副作用合同，也不能证明描述与实现一致。正常属性访问本身也并非绝对静态。 |
| `help(some_api)`              | 在交互环境中向人展示对象类别、名称、签名、docstring 和相关成员的整理帮助 | 不能替代稳定的机器可解析格式；不能仅凭显示证明当前调用无副作用、文档适用于哪个版本或所有业务输入。 |
| `pydoc.render_doc(some_api)`  | 让程序直接得到一份面向人读的文本文档字符串，便于保存或自行显示 | 仍不是结构化 API 合同；不能保证标题、换行和成员排版跨版本稳定，也不自动给出完整的返回值、异常和副作用语义。 |
| `inspect.signature(some_api)` | 当前可调用对象呈现的参数名称、种类、默认值、注解和调用形状；可配合 `bind()` 检查实参匹配 | 不能保证所有 callable 都可内省；不能证明注解被运行期强制、函数体会成功、返回类型正确、无副作用或业务值有效。 |
| 当前版本官方文档              | 标准库/语言层公开合同：对象类型、正式签名、参数语义、返回值、异常、副作用、版本变化和实现说明 | 不能替代“本机实际导入的是哪个对象/版本”的确认；也不能自动覆盖第三方包装器和本地修改。 |
| 当前最小实验                  | 当前解释器、当前对象和指定输入实际产生的返回对象、输出、状态变化或异常时机 | 不能由一次或少量实验推出全部输入、未来版本、其它实现和平台都相同；观察到的排版和精确错误消息也未必是合同。 |

这些来源是互补关系：对象元数据和帮助工具提供线索，官方文档给出公开合同，当前
实验确认实际环境；任何一个都不应独占最终结论。

### 2. 为什么逐行解析 `help()` 很脆弱

`help()` 的首要目标是供人交互阅读，而不是给程序提供稳定序列化协议。其标题、
缩进、空行、折行、成员顺序、pager 行为和终端装饰可能随：

```tex
Python 版本
对象类别
终端宽度
pager 配置
renderer/环境
```

变化。逐行解析等于把偶然展示形式误当成 API。

`pydoc.render_doc()` 改善的是**输出交付边界**：它直接返回 `str`，调用者无须重定向
`stdout` 才能取得文本。但它仍然是人读文档，不提供结构化字段，也不保证：

- 文本排版稳定；
- 成员就是完整公共 API；
- 签名可用且含全部业务约束；
- 返回值、异常、副作用和版本合同完整；
- 文档一定与当前实现一致。

若程序需要调用规则，应优先使用明确的数据模型、正式配置/schema、已发布的类型
信息和官方结构化接口，而不是解析帮助页。

### 3. 旧文章与当前环境冲突时的合同核对

建议按以下顺序逐项核对：

1. **对象身份与类型**：先在当前环境记录 `type(some_api)`、`__module__`、模块文件、
   包版本；必要时确认是否被装饰器/包装器替换。这主要靠当前对象观察。
2. **签名和参数种类**：以目标版本官方参考文档为公开合同基准，再用
   `inspect.signature()` 检查当前对象呈现的签名；若不一致，先排查版本、包装器和
   实现差异。
3. **参数语义**：优先读官方条目正文，而不是只看签名；最小实验只验证少量关键
   边界，如默认值、关键字专用和非法值。
4. **返回值**：官方文档确认承诺的返回对象及惰性；当前实验记录本机的类型和值，
   但避免依赖未承诺的具体 `repr`。
5. **异常**：官方文档确认规定异常和触发条件；本机实验补充异常发生阶段、当前
   消息和异常前状态变化，其中消息/实现消费细节需单独标注。
6. **副作用**：优先看官方文档和源码中的明确说明；再在隔离输入、临时目录或状态
   快照下观察当前调用。不能因返回正常就推断无副作用。
7. **版本变化**：查 Added/Changed/Deprecated/Removed 说明及 What’s New，确定旧
   文章适用的版本区间。
8. **实现说明**：标记 `CPython implementation detail`；只有公开文档保证的行为才
   能直接写成跨实现依赖。当前 CPython 源码/实验用于解释，而不是自动升级合同。

因此，官方文档优先提供类型、正式签名、参数语义、返回、异常、副作用、版本和实现
边界；当前解释器观察必须补充对象身份、实际签名可见性、当前异常时机、环境路径和
实现展示。旧文章只保留为历史线索。

### 4. 可复现实验记录的最小字段

```tex
记录日期/编号
问题与验证前判断
Python 完整版本：sys.version
Python 实现：sys.implementation.name（必要时完整 sys.implementation）
解释器路径：sys.executable
操作系统/虚拟环境
目标对象：模块、限定名、模块文件、包版本
官方文档入口及文档版本
最小且完整的实验代码
实验输入与前置状态
返回对象（类型和值的稳定部分）
标准输出/标准错误
异常类型、异常时机和消息（消息标注为可能易变）
调用后的对象/文件/迭代器状态
验证后结论及其层级
不能证明的边界和下一最小检查
```

最终结论应明确写成“Python 3.14.5 当前环境观察”或“Python 3.14 标准库公开合同”，
而不是把二者混成无版本限制的绝对陈述。
<!-- answer:end -->

---

<!-- quiz-section: id=D score=16 -->
## D. 签名、版本与最小实验（16 分）

<!-- quiz-question: id=D1 score=8 -->
### D1. `Signature.bind()` 能证明什么（8 分）

预测程序输出或异常，并解释 `Signature.bind()` 的证明范围：

```python
import inspect


def normalize_text(
    text: str,
    *,
    strip: bool = True,
    upper: bool = False,
) -> str:
    result = text.strip() if strip else text
    return result.upper() if upper else result


signature = inspect.signature(normalize_text)
bound = signature.bind(" hp ", upper=True)

print(signature)
print(dict(bound.arguments))

try:
    signature.bind(" hp ", False)
except TypeError as exc:
    print(type(exc).__name__)
```

1. 写出三行输出；签名字符串按题中函数定义给出即可。
2. 为什么 `bound.arguments` 中没有自动出现使用默认值的 `strip`？若希望补入
   默认值，应在绑定结果上执行什么操作？
3. 第三个绑定为什么失败？指出哪两个参数是 keyword-only。
4. 即使第一组参数绑定成功，仍不能证明哪些事情？至少说明注解运行期强制、
   函数体实际执行、返回类型、异常、副作用和业务参数语义中的四项。

评分关注：输出和关键字参数 3 分；默认值边界 1 分；`bind()` 能力与限制 4 分。

#### 你的作答

<!-- answer:start -->

### 1. 三行输出

```tex
(text: str, *, strip: bool = True, upper: bool = False) -> str
{'text': ' hp ', 'upper': True}
TypeError
```

第一行是 `Signature` 对象的人读字符串形式；第二行中的字典保持参数声明/绑定顺序，
只包含本次显式绑定的 `text` 与 `upper`。

### 2. 默认值为什么没有自动进入 `bound.arguments`

`Signature.bind()` 返回的 `BoundArguments.arguments` 默认只记录**显式绑定**的实参。
`strip` 没有由调用者传入，只是在未来真正调用函数时会使用默认值，所以当前映射中
没有它。

若希望把缺失参数的默认值补入，应执行：

```python
bound.apply_defaults()
```

之后 `bound.arguments` 会包含：

```python
{
    "text": " hp ",
    "strip": True,
    "upper": True,
}
```

### 3. 第三个绑定为什么失败

函数签名中的 `*` 表示它之后的：

```tex
strip
upper
```

都是 keyword-only 参数。调用：

```python
signature.bind(" hp ", False)
```

试图把 `False` 作为第二个位置实参传入，但函数只有 `text` 能按位置接收；因此出现
`TypeError`。正确形式应类似：

```python
signature.bind(" hp ", strip=False)
```

### 4. 绑定成功仍不能证明什么

第一组绑定成功只证明参数在数量、位置和关键字形式上能映射到该签名。它不能证明：

1. `text: str`、`strip: bool`、`upper: bool` 注解会被 Python 自动执行为运行期类型
   检查；注解本身不是这里的强制验证器。
2. `normalize_text` 函数体已经执行；`bind()` 不调用目标函数。
3. 真正调用必定返回 `str`；返回注解不是该调用结果的运行期证明。
4. 函数体不会抛出异常；例如传入不支持 `.strip()` 的对象后，绑定仍可能成功但
   调用失败。
5. 调用没有输出、I/O、对象修改或其它副作用；签名不表达这些语义。
6. `strip`、`upper` 接受任意真值对象是否符合项目业务规则；绑定只关心调用形状，
   不验证“这些值应该是什么意思”。

因此：

```tex
Signature.bind() 证明调用形状可绑定
≠
证明函数执行合同正确
```

<!-- answer:end -->

<!-- quiz-question: id=D2 score=8 -->
### D2. 版本敏感 API 与惰性失败（8 分）

当前题目明确以仓库日常解释器 Python `3.14.5` 为观察环境。阅读：

```python
import itertools


batches = itertools.batched("ABCDE", 2, strict=True)
print(type(batches).__name__)
print(next(batches))

try:
    remaining = list(batches)
    print(remaining)
except ValueError as exc:
    print(type(exc).__name__)
```

并参考本章给出的官方入口：
`https://docs.python.org/3/library/itertools.html#itertools.batched`。

1. 写出实际会到达的三行输出；说明哪条 `print()` 永远不会执行。
2. 精确追踪创建 `batches`、第一次 `next()`、`list(batches)` 各自何时推进上游。
   `ValueError` 出现前，哪些字符已经被消费？不要把异常说成事务回滚。
3. 这项实验能支持怎样的、带版本范围的最小结论？它不能证明其它 Python 版本
   或任意实现中的什么？
4. 若旧资料中的签名没有 `strict`，说明应怎样联合使用官方版本说明、当前签名和
   当前最小实验，而不是只选择其中一个来源。

评分关注：输出与不可达语句 2 分；惰性消费轨迹 3 分；版本化结论 1 分；三类
证据联合 2 分。

#### 你的作答

<!-- answer:start -->

### 1. 实际到达的三行输出

在题目指定的 Python 3.14.5 环境中：

```tex
batched
('A', 'B')
ValueError
```

以下语句永远不会执行：

```python
print(remaining)
```

因为它只位于 `list(batches)` 成功返回后的下一行，而右侧物化过程中抛出了
`ValueError`。

### 2. 惰性推进与消费轨迹

#### 创建 `batches`

```python
batches = itertools.batched("ABCDE", 2, strict=True)
```

这一步创建 `itertools.batched` 迭代器对象，并为输入字符串取得一个上游迭代器；
不会预先生成全部批次，也尚未消费字符。因此：

```python
type(batches).__name__ == "batched"
```

#### 第一次 `next()`

```python
next(batches)
```

为了形成长度为 2 的完整批次，它从上游依次取得 `A`、`B`，生成：

```python
('A', 'B')
```

此时已消费字符 `A`、`B`，下一字符是 `C`。

#### `list(batches)`

`list()` 继续反复请求下一批：

1. 取得 `C`、`D`，成功形成 `('C', 'D')`；该元组会暂时进入正在构造的列表。
2. 再请求一批，取得 `E` 后上游耗尽，只得到长度为 1 的不完整批次。
3. 因 `strict=True`，该不完整批次不作为结果交付，而是抛出 `ValueError`。

所以错误出现前 `A`、`B`、`C`、`D`、`E` 都已经被上游迭代器消费。异常不会回滚
消费位置；正在构造的临时列表也不会作为 `list()` 返回值交给调用者，故
`remaining` 不完成本次绑定。

### 3. 带版本范围的最小结论

本实验结合 Python 3.14 标准库文档与 CPython 3.14.5 当前运行，可以支持：

> 在 Python 3.14.5 中，`itertools.batched(iterable, n, *, strict=True)` 返回惰性
> `batched` 迭代器；它按需取得至多 `n` 个输入元素，若最终批次短于 `n`，在消费
> 到该批次时抛出 `ValueError`。`batched()` 自 Python 3.12 加入，`strict` 选项自
> Python 3.13 加入。

它不能仅凭本次实验证明：

- Python 3.11 存在 `batched()`；
- Python 3.12 接受 `strict` 参数；
- 任意未来版本都使用相同内部类型、错误消息和实现；
- 所有 Python 实现都必须采用 CPython 相同的内部消费代码和具体类型显示。

### 4. 旧资料没有 `strict` 时的三类证据联合

1. **官方版本说明**：确认 `batched()` 在 3.12 加入，而 `strict` 在 3.13 加入，
   从而解释旧文章为什么可能没有该参数。

2. **当前签名/对象证据**：在目标 Python 3.14.5 中查看官方条目及必要时
   `inspect.signature(itertools.batched)`，确认当前调用形状为：

   ```python no-compile
   batched(iterable, n, *, strict=False)
   ```

3. **当前最小实验**：实际传入 `strict=True`，确认参数可接受，并验证不完整末批的
   `ValueError` 发生在迭代消费期间。

官方文档给出可依赖的版本化合同；当前签名确认本机对象呈现的调用结构；最小实验
确认实际解释器中的关键正常/失败路径。只选旧文章会过时，只看签名不知道惰性和
错误时机，只做实验又不能解释版本范围。
<!-- answer:end -->

---

<!-- quiz-section: id=E score=18 -->
## E. C10-C15 对象与控制流综合（18 分）

<!-- quiz-question: id=E1 score=10 -->
### E1. 本地化审计快照代码阅读（10 分）

阅读下面的本地化审计函数：

```python
def audit_snapshot(records, required_keys):
    enabled_records = [
        record for record in records if record.get("enabled", True)
    ]
    enabled_keys = {record["key"] for record in enabled_records}
    text_by_key = {
        record["key"]: record["target"]
        for record in enabled_records
        if record["target"]
    }
    missing_keys = sorted(required_keys - enabled_keys)
    empty_keys = [
        record["key"]
        for record in enabled_records
        if record["target"] == ""
    ]

    if missing_keys:
        action = "review-missing"
    elif empty_keys:
        action = "review-empty"
    else:
        action = "ready"

    return {
        "action": action,
        "enabled_count": len(enabled_records),
        "text_by_key": text_by_key,
        "missing_keys": missing_keys,
        "empty_keys": empty_keys,
    }


records = [
    {"key": "menu.start", "target": "Start"},
    {"key": "menu.quit", "target": ""},
    {"key": "menu.debug", "target": "Debug", "enabled": False},
]
alias = records
required = {"menu.start", "menu.quit", "menu.options"}

report = audit_snapshot(records, required)
display_result = print("human summary ->", report["action"])

print(report)
print(alias is records)
print(alias[0] is records[0])
print(display_result is None)
```

1. 写出五次 `print()` 的结果。报告字典须完整写出，并保持稳定的缺项顺序。
2. 按 C10-C14 的顺序追踪：
   - 哪些表达式产生新对象，哪些赋值只绑定名字；
   - `enabled` 和 `target` 分别在哪里接受真值测试；
   - 为什么缺项和空译文同时存在，但最终动作只有 `review-missing`；
   - 每个推导式的 iterable、临时 iterator、消费者及正常结束状态。
3. 判断函数是否修改了 `records` 或内部字典。新建 `enabled_records` 为什么不等于
   对记录字典做深拷贝？两个身份比较分别证明了什么、不能证明什么？
4. 将以下结论分别标注为源码推导或当前运行期观察：函数没有显式写入输入对象；
   样例输出为指定报告；`print()` 返回 `None`。说明联合两类证据为何强于只看输出。

评分关注：输出与报告 3 分；对象、真值、分支和消费轨迹 4 分；别名/浅层共享
边界 2 分；证据层标注 1 分。

#### 你的作答

<!-- answer:start -->

### 1. 五次 `print()` 的精确结果

```tex
human summary -> review-missing
{'action': 'review-missing', 'enabled_count': 2, 'text_by_key': {'menu.start': 'Start'}, 'missing_keys': ['menu.options'], 'empty_keys': ['menu.quit']}
True
True
True
```

`missing_keys` 来自 `sorted(...)`，所以稳定顺序为：

```python
['menu.options']
```

### 2. 对象、绑定、真值、分支和迭代轨迹

#### 调用前的对象与名字绑定

三个字典字面量各创建一个字典对象；外层列表字面量创建 `records` 列表。随后：

```python
alias = records
```

只把名字 `alias` 绑定到同一个列表，不创建列表副本。`required` 的集合字面量创建
一个新集合对象。

#### `enabled_records` 列表推导式

```python
enabled_records = [
    record for record in records if record.get("enabled", True)
]
```

- iterable：`records` 列表；
- 临时 iterator：由列表建立的列表迭代器；
- 消费者：列表推导式；
- 结束状态：迭代器正常耗尽，生成新的外层列表 `enabled_records`。

每个 `record.get("enabled", True)` 的结果接受真值测试：前两个记录没有 `enabled`，
默认得到 `True`；第三个得到 `False`，因此被过滤。新列表中放入的是前两个原字典
对象的引用，并未深复制字典。

#### `enabled_keys` 集合推导式

```python
enabled_keys = {record["key"] for record in enabled_records}
```

- iterable：`enabled_records`；

- 临时 iterator：新的列表迭代器；

- 消费者：集合推导式；

- 结束状态：正常耗尽并创建新集合：

  ```python no-compile
  {'menu.start', 'menu.quit'}
  ```

#### `text_by_key` 字典推导式

```python
text_by_key = {
    record["key"]: record["target"]
    for record in enabled_records
    if record["target"]
}
```

- iterable：`enabled_records`；
- 临时 iterator：又一个独立列表迭代器；
- 消费者：字典推导式；
- `record["target"]` 直接接受真值测试。

`"Start"` 为真，被加入字典；空字符串 `""` 为假，被过滤。因此创建：

```python
{'menu.start': 'Start'}
```

#### `missing_keys`

```python
required_keys - enabled_keys
```

先创建差集集合 `{'menu.options'}`；`sorted()` 再创建一个新列表：

```python
['menu.options']
```

#### `empty_keys` 列表推导式

```python
empty_keys = [
    record["key"]
    for record in enabled_records
    if record["target"] == ""
]
```

- iterable：`enabled_records`；
- 临时 iterator：新的列表迭代器；
- 消费者：列表推导式；
- 每轮先计算 `record["target"] == ""`，然后对这个比较结果 `bool` 做分支测试。

得到新列表：

```python
['menu.quit']
```

这里 `target` 的值参与比较；它在前一个字典推导式中则被直接用于真值测试。

#### 分支选择

`missing_keys` 是非空列表，因此：

```python
if missing_keys:
    action = "review-missing"
```

第一个分支已命中，后面的 `elif empty_keys` 不再测试，所以尽管空译文也存在，动作
仍只有 `review-missing`。最后返回一个新报告字典。

### 3. 是否修改输入及浅层共享

函数没有执行对 `records` 外层列表的写入，也没有对其中字典进行赋值、删除或原地
修改；对题目中的普通 list/dict 输入，样例执行后内容保持不变。

不过：

```python
enabled_records
```

只是一个新的外层列表，其中元素仍是原来两个字典对象。因此：

```tex
新外层列表
≠
深复制内部字典
```

如果随后执行 `enabled_records[0]["target"] = ...`，原记录字典也会反映变化。

两个身份判断：

- `alias is records` 为 `True`，证明两个名字当前绑定同一个外层列表；不能证明列表
  内容不可变，也不能说明未来重新绑定后仍相同。
- `alias[0] is records[0]` 为 `True`，证明这两个索引表达式当前得到同一个字典。
  由于 `alias` 与 `records` 本来就是同一列表，该结论实际上是前一结论的自然结果；
  它不能证明所有元素之间互不共享，也没有直接检查 `enabled_records[0]`。

### 4. 证据层标注

- “函数源码没有显式写入输入对象”：主要是**源码推导**。但若允许任意自定义
  mapping，其 `.get()`/`__getitem__()` 自身仍可能执行代码；对题目给出的普通字典
  样例则没有该动态风险。
- “样例输出为题中指定报告”：是可由源码预测、再由**当前运行期观察**确认的结论。
- “`print()` 返回 `None`”：首先是内置函数的公开 API 合同，也可由当前实验
  `display_result is None` 再确认；不应只把一次观察误写成偶然现象。

联合源码与运行证据更强：源码能解释所有求值、别名和分支，并发现未走到的路径；
运行结果确认当前解释器与实际数据确实按模型工作。只看输出看不到临时对象、浅层
共享、短路分支和是否曾发生未展示的状态变化。
<!-- answer:end -->

<!-- quiz-question: id=E2 score=8 -->
### E2. 可重复容器与一次性输入边界（8 分）

沿用 E1 的 `audit_snapshot()`，只改变调用方：

```python
source_records = [
    {"key": "menu.start", "target": "Start"},
    {"key": "menu.quit", "target": "Quit"},
]
record_stream = iter(source_records)

report = audit_snapshot(
    record_stream,
    {"menu.start", "menu.quit"},
)

print(report["action"])
print(list(record_stream))
print(source_records)
print(list(source_records))
```

1. 写出四行输出，并说明报告中的 `action` 为什么是该值。
2. `audit_snapshot()` 没有对 `record_stream` 调用写入方法，为什么调用结束后它仍然
   发生了可观察的状态变化？指出真正保存消费位置的对象。
3. 严格区分：一次性迭代器耗尽、源列表未修改、源列表仍能提供新迭代器。不要把
   “函数没有修改元素”扩大成“调用对任何输入都没有状态影响”。
4. 如果第一次推导式中途因缺少 `record["key"]` 而抛出异常，能否自动断言
   `record_stream` 已耗尽？说明更精确的状态结论以及为何异常不提供回滚。

评分关注：输出 2 分；消费位置与状态变化 3 分；三层边界 2 分；异常后的有限
结论 1 分。

#### 你的作答

<!-- answer:start -->

### 1. 四行输出

```tex
ready
[]
[{'key': 'menu.start', 'target': 'Start'}, {'key': 'menu.quit', 'target': 'Quit'}]
[{'key': 'menu.start', 'target': 'Start'}, {'key': 'menu.quit', 'target': 'Quit'}]
```

第一次推导式把两条记录都保留下来；`enabled_keys` 正好包含两个必需键，所以
`missing_keys == []`。两个 `target` 均为非空字符串，所以 `empty_keys == []`。
因此 `if` 与 `elif` 都不命中，`action` 为 `"ready"`。

### 2. 为什么未调用“写入方法”仍有状态变化

```python
record_stream = iter(source_records)
```

创建的是一次性列表迭代器，消费位置保存在 `record_stream` 指向的 iterator 对象中，
而不是保存在 `source_records` 列表对象中。

`audit_snapshot()` 的第一条列表推导式执行：

```python no-compile
for record in records
```

这里的 `records` 正是传入的 `record_stream`。推导式反复调用该 iterator 的迭代协议，
直到正常耗尽。因此即使没有调用类似 `.append()` 的写入方法，iterator 的内部游标
已经推进到末尾，这是可观察的状态变化：

```python
list(record_stream) == []
```

### 3. 三层边界

1. **一次性迭代器已耗尽**：同一个 `record_stream` 不能自动从头再来。
2. **源列表未被修改**：列表仍包含原来的两个字典，顺序和内容未变。
3. **源列表可重复迭代**：`source_records` 是可重复 iterable；每次
   `iter(source_records)` 或 `list(source_records)` 都可以建立新的迭代器，从头读取
   当前列表内容。

因此“函数没有修改记录元素”不能扩大为“调用没有影响任何输入状态”；它确实消费了
传入的一次性 iterator。

### 4. 关于题设异常的精确纠偏

题干说“第一次推导式中途因缺少 `record["key"]` 而抛出异常”，但**按当前源码，
第一次推导式并不访问 `record["key"]`**；它只调用：

```python
record.get("enabled", True)
```

所以仅仅缺少 `"key"` 不会让第一条推导式报错。缺少 `"key"` 会在后面的：

```python
enabled_keys = {record["key"] for record in enabled_records}
```

触发 `KeyError`。由于第一条推导式此前已经正常把 `record_stream` 全部消费并物化为
`enabled_records`，在这个**具体修正后的场景**中，`record_stream` 已耗尽。

若把问题理解为“第一条推导式因其它异常在中途失败”，例如某个对象没有 `.get()`，
则不能自动断言 iterator 已耗尽。更精确的结论是：

- 失败项已经先从 iterator 中取出，随后在过滤表达式求值时失败；
- 失败项以前的项目已消费；
- 失败项之后可能仍有未消费项目；
- 异常不会把 iterator 游标回滚，也不会返回那份未完成的临时列表。

所以异常后的状态必须按实际失败位置描述，不能用“报错”推导“必然耗尽”或“自动
恢复”。
<!-- answer:end -->

---

<!-- quiz-section: id=F score=10 -->
## F. 工程证据报告与 P4 交接（10 分）

<!-- quiz-question: id=F1 score=10 -->
### F1. 只读真实代码验证方案（10 分）

你需要为真实项目 `prompt_template_manager` 做一次只读文档走查。允许观察的函数
固定为：

```python
PURE_TARGETS = (
    "resolve_db_path",
    "normalized_content_hash",
    "parse_tags",
    "tags_from_json",
)
```

本轮禁止调用数据库连接、初始化、迁移、CRUD、CLI 或 GUI 入口。已有检查只做了：

```python
before = database_path.exists()
run_selected_helpers()
after = database_path.exists()
assert before == after
```

请设计一份可执行但保持只读边界的验证方案；可以写伪代码、Python 代码或结构化
步骤，但必须包含：

1. 一个固定目标白名单，以及从 README、模块源码/元数据、`inspect.getdoc()`、
   `inspect.signature()` 到合成输入最小实验的有限顺序。逐步标明哪些操作只读，
   哪些属性访问或函数调用可能执行代码。
2. 一个结构化报告模型，至少含 `environment`、`targets`、`claims` 和
   `persistence_guard`。每条 `claim` 至少保存：主张、证据来源、观察结果、不能
   证明什么、下一最小检查。人读 `print()` 应放在报告返回值之外。
3. 精确评价 `before == after`：它证明了什么，又不能证明数据库内容、字节、
   大小、修改时间、删除后重建或事务/访问状态中的什么。若要求字节一致，补充
   哪类只读证据；同时说明检查时序本身仍有哪些有限性。
4. 给出至少三条 P4 交接问题，例如函数对象、实参与形参绑定、函数内部名字解析、
   返回合同与副作用。这里只列出后续要回答的问题，不得假装本卷已经系统教授
   P4 机制。

评分关注：白名单与风险递增顺序 3 分；结构化证据报告 3 分；持久化检查的证明
边界 2 分；P4 交接问题与范围纪律 2 分。

#### 你的作答

<!-- answer:start -->

### 一、只读边界、固定白名单与风险递增顺序

固定目标必须由代码常量决定，不能根据 `dir()` 动态扩大：

```python
PURE_TARGETS = (
    "resolve_db_path",
    "normalized_content_hash",
    "parse_tags",
    "tags_from_json",
)
```

根据真实项目 `prompt_template_manager` 中既有的 `prompt_store.py` 的源码，这四个目标分别只做路径解析、规范化内容哈希、标签解析和 JSON 标签反序列化；本轮明确不允许触及 `connect*`、`initialize_database`、迁移、索引、CRUD、导入批处理、CLI 或 GUI。

建议按以下顺序执行，每一步都冻结证据并决定是否继续：

#### 第 0 步：建立持久化基线

在导入项目模块前记录：

```tex
数据库路径及 data 目录是否存在
数据库、-wal、-shm、-journal 文件清单
存在文件的大小、mtime_ns 和 SHA-256
项目源码及 README 的 SHA-256
当前工作目录和 Git 工作区状态（可用时）
```

这一步只读取文件系统，但需要承认某些文件系统的读操作可能更新访问时间；它不是
“无任何系统状态影响”的绝对沙箱。

#### 第 1 步：读取 README 与目录结构

读取项目 `README.md`，只提取：

```tex
公开入口声明
运行方式
数据库路径说明
四个 helper 的公开用途（若有）
版本或兼容性要求
```

这是源码/文档文件读取，不执行 Python 模块。若设计人员只明确了 README 的存在位置但
对其正文一无所知，则最终报告必须记录“README 主张需在实际走查时读取”，不能臆造
其内容。

#### 第 2 步：读取 `prompt_store.py` 源码和 AST

直接读取源文件字节并 `ast.parse()`：

- 确认四个白名单名字均对应模块级函数定义；

- 记录函数 docstring、注解和源码位置；

- 扫描其调用关系，确认没有直接调用数据库连接/CRUD；

- 特别记录：

  ```tex
  resolve_db_path -> Path(...).expanduser().resolve() 或 DEFAULT_DB_PATH
  normalized_content_hash -> normalize_content -> content_hash
  parse_tags -> re.split/list/str.strip/集合去重
  tags_from_json -> json.loads，捕获 JSONDecodeError，要求解析结果为 list
  ```

该步骤是静态只读证据，不执行模块，也不能证明动态名称解析永远指向当前看到的函数。

#### 第 3 步：受控导入以取得运行时元数据

`inspect.getdoc()` 与 `inspect.signature()` 需要活对象。导入会执行模块顶层代码，
因此不是纯静态操作。应在独立子进程中：

```tex
使用题目指定 Python 3.14.5 解释器
设置 PYTHONDONTWRITEBYTECODE=1 或使用 -B，避免创建 __pycache__
禁止调用任何非白名单函数
将 stdout/stderr、退出码和导入前后持久化快照写入内存报告
设置超时
```

从目标模块的源码可见，顶层会导入标准库、计算 `PROJECT_DIR/REPO_ROOT/DEFAULT_DB_PATH`、
创建常量字符串和定义类/函数；没有顶层数据库连接。但这仍是**源码审查后的当前判断**，
导入执行风险必须在报告中保留。

导入后只通过模块命名空间中的固定名称取得目标：

```python
targets = {
    name: vars(prompt_store)[name]
    for name in PURE_TARGETS
}
```

不使用 `dir()` 自动扩展目标集。

#### 第 4 步：收集 `getdoc` 和 `signature`

对四个活函数执行：

```python
inspect.getdoc(func)
inspect.signature(func)
```

这一步不调用这四个函数体；但它属于运行期内省，不能对任意恶意对象宣称绝对无代码
执行风险。对本题已确认的普通 Python 函数，预期签名为：

```python no-compile
resolve_db_path(db_path: str | Path | None = None) -> Path
normalized_content_hash(content: str) -> str
parse_tags(tags: str | Sequence[str] | None) -> list[str]
tags_from_json(value: str | None) -> list[str]
```

签名只证明当前呈现的调用结构和注解，不证明注解被强制，也不证明函数“纯”。

#### 第 5 步：合成输入最小实验

只调用白名单 helper，并且只传入不接触真实数据库的合成输入：

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)

    cases = {
        "resolve_db_path": [
            (None,),                     # 只返回 DEFAULT_DB_PATH 对象，不打开它
            (tmp_path / "nested" / "demo.sqlite3",),
            ("~/synthetic-demo.sqlite3",),
        ],
        "normalized_content_hash": [
            ("  line1\r\nline2  ",),
            ("line1\nline2",),
        ],
        "parse_tags": [
            (None,),
            ("python, docs，python,  ",),
            ([" docs ", "python", "docs", 3],),
        ],
        "tags_from_json": [
            (None,),
            ("",),
            ('["docs", 3, null]',),
            ('{"not": "a list"}',),
            ("invalid json",),
        ],
    }
```

实际调用会执行函数体，因此属于本方案中风险最高的一层，但根据源码和合成输入，
不应调用数据库 API。必须在调用前后重新验证：

```tex
临时目录中没有意外创建文件
真实 data 目录和数据库快照未变化
stdout/stderr 无异常意外输出
返回对象类型和值符合源码主张
```

例如可验证的有限主张包括：

- 两种换行形式规范化后得到相同 SHA-256；
- `parse_tags()` 去除空白、忽略空项、按首次出现顺序去重；
- `tags_from_json()` 对无效 JSON/非列表返回空列表，对列表元素执行 `str()`；
- `resolve_db_path()` 只返回具体 `Path`，没有创建数据库。最后一项必须由持久化
  guard 补证，而不能只看返回值。

### 二、结构化报告模型

采集函数只返回结构化数据；人读输出由另一个显示函数处理：

```python
report = {
    "environment": {
        "python_version": sys.version,
        "implementation": sys.implementation.name,
        "executable": sys.executable,
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "module_file": str(prompt_store.__file__),
        "source_sha256": source_hash,
        "readme_sha256": readme_hash,
    },
    "targets": {
        name: {
            "whitelisted": True,
            "runtime_type": f"{type(func).__module__}.{type(func).__qualname__}",
            "signature": str(inspect.signature(func)),
            "doc": inspect.getdoc(func),
            "source_location": source_location[name],
            "called": False,
        }
        for name, func in targets.items()
    },
    "claims": [],
    "persistence_guard": {
        "paths": guarded_paths,
        "before": before_snapshot,
        "after": None,
        "existence_equal": None,
        "byte_hashes_equal": None,
        "metadata_equal": None,
        "sidecar_listing_equal": None,
        "limitations": [],
    },
}
```

每条 claim 至少采用：

```python
{
    "target": "parse_tags",
    "claim": "重复标签按首次出现顺序去重，空标签被忽略",
    "evidence_source": [
        "prompt_store.py source",
        "inspect.signature",
        "synthetic runtime case",
    ],
    "observation": {
        "input": "python, docs，python,  ",
        "result": ["python", "docs"],
    },
    "cannot_prove": [
        "未证明任意自定义 Sequence 元素的 str() 没有副作用",
        "未证明未来项目版本保持同一规则",
    ],
    "next_minimal_check": "增加含非字符串对象和异常 __str__ 的隔离测试",
    "evidence_level": "source + CPython 3.14.5 observation",
}
```

采集函数不在内部打印；人读显示放在外部：

```python
report = run_readonly_walkthrough()
print_report(report)       # 只展示
# 或 json.dumps(report, ...)
```

这样返回值、展示副作用和持久化检查相互分离。

### 三、`before == after` 的精确证明边界

现有代码：

```python
before = database_path.exists()
run_selected_helpers()
after = database_path.exists()
assert before == after
```

最多证明：在两个离散采样时点，`database_path.exists()` 得到相同布尔值。也就是：

- 原来不存在，结束时仍未发现该路径；或
- 原来存在，结束时该路径仍存在。

它不能证明：

```tex
数据库字节内容未变
文件大小未变
mtime/ctime/权限未变
SQLite 逻辑记录未变
未创建或修改 -wal、-shm、-journal
文件没有在中途删除后重建
路径现在仍指向同一个文件实体
没有打开连接、锁、事务或访问状态
没有修改后恢复到原内容
没有其它进程同时写入
```

若要求**最终字节一致**，至少增加只读快照：

```python
{
    "exists": path.exists(),
    "is_file": path.is_file(),
    "size": path.stat().st_size,
    "mtime_ns": path.stat().st_mtime_ns,
    "sha256": sha256(path.read_bytes()).hexdigest(),
}
```

并对数据库目录的 sidecar 文件清单及其哈希做前后比较。必要时还记录平台可用的文件
标识，以帮助发现“删除后用另一文件重建”。

即便前后 SHA-256 相同，也只能证明两个采样时刻读取到的最终字节相同，仍不能排除：

- 中途修改后又恢复；
- 采样间的并发写入；
- 只改变了未纳入快照的元数据或外部状态；
- 哈希读取本身与并发写入存在 TOCTOU 时间窗口。

要进一步强化，应使用独立子进程、只读/临时文件系统、禁止网络、OS 文件事件审计、
排除并发写者并监测整个测试窗口；但仍应把这种保证写成受控环境下的有限证据，而非
绝对安全证明。

### 四、P4 交接问题（只列问题，不提前系统作答）

1. 执行 `def` 时究竟创建了什么对象，函数名何时与该对象绑定？函数对象与
   `function()` 的调用结果有什么区别？
2. 调用 `parse_tags(value)` 时，实参对象怎样与形参 `tags` 建立临时绑定；这种绑定
   是否复制对象，函数内对可变对象的操作怎样影响调用者？
3. 函数体中的名字按什么规则解析；局部名字、模块名字和内置名字之间的完整作用域
   规则是什么？
4. `return` 如何终止函数执行并把对象交给调用者；没有显式 `return` 为什么得到
   `None`？
5. 怎样为函数写清楚返回合同、异常合同和副作用合同；“返回新列表”和“修改传入
   列表”应如何选择？
6. 注解在函数定义和调用中扮演什么角色，为什么不能把它直接当成 Python 自动执行的
   类型验证？

这些问题属于 P4 的正式学习入口；本卷只识别它们，不在这里展开参数绑定、LEGB、
闭包等完整机制。
<!-- answer:end -->

---

## Codex 批改记录（逐题审批，2026-07-24）

### 覆盖账本

下表先冻结本轮审批覆盖。原答案均保留在原作答区；本记录只追加发现与结论。

| 题号 | 分值 | 原答案位置 | 审批状态 | 发现 | 得分 |
| --- | ---: | --- | --- | --- | ---: |
| A1 | 8 | 行 85–164 | 已审批 | 三个 `__doc__`、AST 形态与位置规则准确 | 8 |
| A2 | 10 | 行 194–242 | 已审批 | 六类证据分层、外推边界与冲突核对顺序完整 | 10 |
| B1 | 8 | 行 293–397 | 已审批 | 五行输出与协议轨迹准确；补充 `hasattr()` 掩盖内部 `AttributeError` 的风险 | 8 |
| B2 | 10 | 行 428–541 | 已审批，轻微扣分 | 内省步骤可能执行用户代码的具体机制没有显式展开 | 9.5 |
| C1 | 9 | 行 595–683 | 已审批 | 六行输出、对象绑定与输出/返回边界准确 | 9 |
| C2 | 11 | 行 709–801 | 已审批 | 工具分工、格式脆弱性、合同字段和实验记录完整 | 11 |
| D1 | 8 | 行 850–929 | 已审批 | `bind()`、默认值、keyword-only 与证明范围准确 | 8 |
| D2 | 8 | 行 967–1063 | 已审批 | 惰性消费、异常时机和版本范围准确 | 8 |
| E1 | 10 | 行 1142–1317 | 已审批 | 输出、对象/控制流、浅层共享与证据层全部准确 | 10 |
| E2 | 8 | 行 1355–1432 | 已审批 | 主动识别题干不可能路径并给出正确分支分析 | 8 |
| F1 | 10 | 行 1484–1807 | 已审批，扣分 | 严格只读、序列化/显示、签名显示和哈希证明强度仍需收紧 | 8.5 |

审批游标：`F1`，共 `11 / 11` 题完成，无遗漏。

### A1 — 8 / 8

三个 `__doc__` 的类型和值完全正确；对 `-OO` 可能移除 docstring 的前提限制也很
严谨。注释、普通字符串表达式、运行时元数据和 AST 语句形态分层准确。尤其是
“首条语句位置，而不是三引号形式决定 docstring 身份”，抓住了本题核心。

### A2 — 10 / 10

六项观察的主证据层全部分类正确，并且逐项写出了不能外推的结论。④“业务返回
对象”和⑥“带环境记录的运行期实验”虽都发生在运行时，但主视角不同；答案对此
处理准确。冲突核对顺序有限、可执行，最终记录字段足以限定结论适用范围。

### B1 — 8 / 8

Python 3.14.5 实测五行依次为：

```text
True
False
False
True
False
```

`__dir__()`、`__getattr__()`、类属性读取和 `callable()` 的轨迹均正确。

不扣分精度补充：`hasattr()` 会把整个属性读取链最终抛出的 `AttributeError`（含其
子类）转换为 `False`。这个异常也可能来自 property/descriptor 内部缺陷，而不只是
“属性确实不存在”；因此 `hasattr(...) is False` 不能独立证明缺少该属性。其它异常
仍会传播。

### B2 — 9.5 / 10

未经证明的合同项、四组边界、`inspect.getattr_static()`、`Signature.bind()`、
Protocol/ABC 和命名惯例的局限都很完整。

扣 `0.5` 分：答案知道普通内省不是安全沙箱，但没有显式说明具体执行入口。
`inspect.getdoc()`、`inspect.signature()` 可能读取 `__doc__`、`__wrapped__`、
`__signature__` 等属性，从而触发自定义 `__getattribute__`、descriptor 或包装器逻辑。
只有在已经取得普通 `Signature` 对象后，`signature.bind(...)` 才只是本地参数映射，
不调用目标函数。临时目录、一次性实例和普通子进程也只是降低污染，并不是文件系统、
网络或权限沙箱。

### C1 — 9 / 9

当前解释器实测六项为：

```text
True
str
True
False
str
<missing>
```

`help()` 的显示副作用与 `None` 返回、`redirect_stdout()` 的捕获范围、
`pydoc.render_doc()` 返回 `str` 而不自动显示，以及 docstring 与完整帮助页的区别
均准确。

### C2 — 11 / 11

六类工具/来源的能力边界、帮助文本的格式脆弱性、合同字段核对顺序与实验记录字段
完整。两点不扣分补充：

- 官方文档中的“对象类型”应理解为它明确承诺的对象类别或返回类型合同，不能替代
  当前环境中实际对象身份、包装层和具体实现类型的确认；
- `help()`、`pydoc.render_doc()`、`inspect.signature()` 都是运行期内省操作，
  对任意自定义对象不能先验视为纯静态、无副作用读取。

### D1 — 8 / 8

签名、初始 `bound.arguments`、`TypeError`、`apply_defaults()` 后的映射以及两个
keyword-only 参数均正确。答案也准确限定：`bind()` 只证明调用形状可映射，不执行
函数体，不强制注解，也不验证返回、异常、副作用或业务值语义。

### D2 — 8 / 8

Python 3.14.5 实测输出为 `batched`、`('A', 'B')`、`ValueError`；
`print(remaining)` 不可达。A–E 在异常前均已被上游消费，临时列表没有返回，
`remaining` 的绑定不完成，且不存在回滚。

补充边界：当前 CPython 3.14.5 在构造 `batched` 对象时已调用上游 `iter()`，但尚未
请求元素；这是当前实现观察。答案已经把内部类型、具体显示和消费实现限制在当前
版本，没有错误提升为跨实现合同，因此不扣分。

### E1 — 10 / 10

五次输出与当前解释器逐项一致。对象创建与名字绑定、两个真值位置、互斥分支、四次
推导式消费、集合差集和 `sorted()` 的新对象、浅层共享及两个身份比较的证明范围均
完整。把源码推导、公开合同和当前运行观察联合起来，而不是只从输出反推内部行为，
体现了 C15 的证据分层。

### E2 — 8 / 8

四行输出与迭代器状态完全正确。答案还准确指出题干第 4 问存在内部矛盾：第一条
推导式只调用 `record.get(...)`，不会因缺少 `record["key"]` 在那里抛错；真正的
`KeyError` 会出现在后续 `enabled_keys` 集合推导式。该具体路径中第一条推导式已经
耗尽 `record_stream`；若第一条推导式因其它表达式中途失败，则只能确认失败项及其
之前项目已取出，尾部可能仍在，且异常不回滚。题干瑕疵不扣分。

### F1 — 8.5 / 10

固定白名单、风险递增顺序、结构化 claim、持久化 sidecar、TOCTOU、P4 交接边界均
很强。扣分与纠正如下：

1. 白名单与风险顺序 `2 / 3`：`TemporaryDirectory()` 会真实创建并在退出时删除
   目录，因此不属于本题的严格只读走查，也与当前禁止递归清理的安全边界冲突。
   应改用预先声明、确认不存在且绝不创建的合成路径，或仅运行完全内存型 helper；
   若确需临时工作区，应另行授权并把阶段改称受控写入实验。Git 状态读取也应使用
   明确允许路径，不能宽范围枚举 `tests/`。
2. 结构化报告 `2.75 / 3`：`json.dumps(report, ...)` 只返回序列化后的 `str`，并不
   展示。若要人读输出，应先得到 `rendered`，再显式 `print(rendered)`，继续区分
   结构化报告、JSON 文本对象和输出副作用。
3. 持久化边界 `1.75 / 2`：相同 SHA-256 是极强证据，但因理论碰撞不能逻辑上
   “证明字节相同”。若题意要求比较两个已采样字节序列，应保存基线字节并直接做
   相等比较；即便如此也只覆盖两个非原子采样时点，不能排除中途修改、并发写入或
   快照内部 TOCTOU。
4. P4 交接 `2 / 2`：问题覆盖函数对象、参数绑定、名字解析、返回/副作用和注解，
   没有提前系统教授 P4。

另作不重复扣分的显示层纠正：`prompt_store.py` 使用
`from __future__ import annotations`，所以当前 `str(inspect.signature(...))` 中注解
带引号。答案给出的是语义化转写，不应标作当前显示文本的精确复刻。

### 结构与客观验证记录

使用环境：

```text
CPython 3.14.5
D:\MySoftwareDownload\PythonPractice\LearningPython5E\.venv-py314\Scripts\python.exe
```

针对性运行确认：A1 元数据/AST、B1 动态属性、C1 帮助输出、D1 参数绑定、D2 惰性
批次、E1/E2 报告与迭代状态均与以上逐题结论一致。F1 只导入受审源码并调用固定的
四个白名单 helper；未调用连接、初始化、迁移、CRUD、CLI 或 GUI。代表性结果包括：

```text
parse_tags([" docs ", "python", "docs", 3]) -> ["docs", "python", "3"]
tags_from_json('["docs", 3, null]') -> ["docs", "3", "None"]
两种规范化换行输入的哈希相等
合成 sentinel 路径在调用前后均不存在
```

原答题区有 8 个普通 `python` 围栏实际承载缩进片段、签名显示或伪代码，导致验证器
把它们当独立模块编译时报错。本轮只把这些围栏标记为 `python no-compile`，未改变
其中任何答案文字、代码字符或作答顺序；其余普通 Python 围栏继续接受编译检查。

### 分区与总分复核

| 分区 | 满分 | 得分 |
| --- | ---: | ---: |
| A | 18 | 18 |
| B | 18 | 17.5 |
| C | 20 | 20 |
| D | 16 | 16 |
| E | 18 | 18 |
| F | 10 | 8.5 |
| **总分** | **100** | **98** |

建议得分：`98 / 100`。所有逐题得分、分区小计和总分已复核一致。

### 本阶段末评语与能力判断

`C15_The_Documentation_Interlude` 阶段测验通过。你已经能稳定区分源码文本、对象
元数据、人读工具输出、业务返回对象、官方公开合同和当前解释器观察，并把
`dir()`、`help()`、`pydoc`、签名与最小实验组织成有限调查链。更重要的是，你能把
C10-C14 的对象、绑定、真值、控制流、迭代消费和结构化报告模型迁移到真实代码
审查中，还主动识别并修正了 E2 题干的不可能路径。

当前能力可判断为：**中级入门前段已经稳固，具备用证据账本独立审查小型 Python
数据流程和 API 合同的能力**。尚需精修的已不是主干概念，而是安全与证明强度：
运行期内省可能执行代码；临时目录与普通子进程不等于只读或权限沙箱；序列化字符串
不等于展示；哈希一致是强证据而非逻辑上的绝对字节同一证明。

本次审批完成后，生命周期进入 `stage_note`；章节尚未执行最终收束。

### 学习画像更新

可复用于阶段笔记与后续启动模板的稳定证据：

- **稳定强项**：能精确区分 docstring 特殊位置、`__doc__` 元数据、源码注释和普通
  字符串表达式；能解释 `dir()` 的发现边界、`hasattr()` 的执行性、`help()` 的输出
  与 `None` 返回、`pydoc.render_doc()` 的文本返回，以及签名/官方文档/实验的分工。
- **P3 综合能力**：能按表达式与语句、绑定与修改、真值与分支、循环退出、迭代器
  消费和证据来源追踪代码；能识别题干与源码不一致，而不顺着错误前提作答。
- **工程迁移能力**：能设计白名单、结构化 claim、环境记录、持久化 guard 和 P4
  交接问题，且主动保留版本、实现、未证明边界和下一最小检查。
- **当前精修点**：运行期内省也可能触发用户代码；严格只读不应创建/删除临时目录；
  `json.dumps()` 返回文本但不展示；未来注解会改变签名显示；哈希一致不能提升为无
  条件的字节同一证明。
- **水平判断**：中级入门前段已稳固，C15 建议得分 `98 / 100`，P3 的证据驱动自查
  框架已经建立。
- **下一阶段风险**：进入 P4 时继续区分函数对象与调用结果、实参与形参绑定、名字
  解析、返回合同与副作用，并避免把注解或内省工具误当成自动运行期合同验证器。
