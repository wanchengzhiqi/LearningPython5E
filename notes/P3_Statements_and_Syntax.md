# P3 Statements and Syntax

本笔记用于 `P3_Statements_and_Syntax`：Python 的语句、语法结构和程序执行路径。

P3 的核心任务不是背语法清单，而是把 P2 已经建立的对象模型推进到执行层：

```tex
源码形式
    -> 表达式求值：创建、查找、组合或调用对象
    -> 语句执行：绑定名字、修改对象、产生副作用或转移控制流
    -> 代码块归属：用缩进表达语法结构
    -> 控制流路径：决定下一条真正执行的语句
    -> 工程边界：输出、日志、文件、异常、资源释放、接口返回
```

读 P3 代码时，优先使用这几组边界：

```tex
表达式求值 vs 语句执行
返回值 vs 副作用
输出文本 vs 函数返回对象
脚本执行 vs REPL 回显
物理行 vs 逻辑行
代码块缩进 vs 表达式续行排版
源码存在 vs 执行路径到达
def 语句执行 vs 函数体调用执行
注释 vs 普通字符串表达式 vs 文档字符串
```

当前状态：

```tex
当前大阶段：P3_Statements_and_Syntax
已完成小阶段：
    C10_Introducing_Python_Statements
    C11_Assignments_Expressions_and_Prints
    C12_if_Tests_and_Syntax_Rules
    C13_while_and_for_Loops
阶段小测：
    C10：96 / 100，通过
    C11：100 / 100，通过
    C12：100 / 100，通过
    C13：99 / 100，通过
当前收束状态：C13 阶段测验审批、学习画像同步、阶段末笔记整理、收束追问补充和 C14 新会话启动模板已完成
下一小阶段：C14_Iterations_and_Comprehensions
```

语句清单专题按 Python 3.14 官方语言参考中的 simple statements 与 compound
statements 归类；其中不少内容属于后续章节预习，不要求在 C10 结束时一次性掌握。

参考资料：

```tex
Python Language Reference / Simple statements:
    https://docs.python.org/3/reference/simple_stmts.html

Python Language Reference / Compound statements:
    https://docs.python.org/3/reference/compound_stmts.html
```

## 12. C10 语句导论：表达式、语句、代码块与执行顺序

`C10_Introducing_Python_Statements` 的真正目标不是“记住几条语法规则”，而是建立一套看 Python 源码时的执行层分析模型：

```tex
源码是否存在
    -> 是否被解析/编译
    -> 当前执行路径是否到达该语句
    -> 表达式是否求值
    -> 求值得到什么对象
    -> 是否产生副作用
    -> 语句如何改变名字绑定、输出、返回或控制流
```

### 12.0 阶段状态和可追溯入口

```tex
2026-06-03：正式进入 C10 语句导论。
2026-06-10：C10 阶段小测完成，建议得分 96 / 100。
```

相关阶段文件：

```tex
practice/P3_Statements_and_Syntax/C10_Introducing_Python_Statements/
practice/P3_Statements_and_Syntax/C10_Introducing_Python_Statements/stage_quiz_introducing_python_statements.md
docs/P3_STATEMENTS_AND_SYNTAX_STARTUP_TEMPLATE.md
```

练习脚本：

```tex
01_expressions_statements_and_side_effects.py
02_script_vs_interactive_echo.py
03_logical_lines_and_blocks.py
04_order_and_control_flow_preview.py
```

### 12.1 阶段地图

本阶段按以下顺序推进：

```tex
1. 表达式求值 vs 语句执行。
2. 返回值 vs 副作用。
3. print() 输出 vs print() 返回值。
4. 脚本执行 vs REPL 自动回显。
5. 物理行 vs 逻辑行。
6. 代码块缩进 vs 表达式跨行缩进。
7. 顺序执行 vs 控制流选择。
8. break / continue 等后续控制流转移语句的预告。
9. def 语句执行 vs 函数体调用执行。
10. 注释、普通字符串表达式和文档字符串。
11. C10 阶段小测与代码审查式批改。
```

阶段验收观察点：

```tex
1. 能稳定区分表达式求值与语句执行。
2. 能说明值、返回值、副作用、输出和回显的层级差异。
3. 能判断一段源码中的逻辑行、缩进代码块和执行顺序。
4. 能把 P2 的对象模型自然延伸到 P3：
   表达式产生或访问对象，语句组织对名字、对象和外部边界的影响。
```

### 12.2 表达式求值与语句执行

表达式会被求值，得到一个对象作为值；语句是 Python 程序执行的源码单位，用来组织动作。语句可以包含表达式，但不能把“表达式有值”泛化成“所有语句都有返回值”。

```python
x = 1 + 2
```

这行代码中：

```tex
1 + 2 是表达式：
    求值得到整数对象 3。

x = 1 + 2 是赋值语句：
    执行效果是让名字 x 绑定到这个对象。
```

常见误区：

```tex
误区1：语句也像表达式一样都有一个值。
修正：表达式有值；语句是执行单位，重点在执行效果。

误区2：赋值语句“返回”右侧对象。
修正：赋值语句让目标绑定到对象；不要把语句效果说成普通返回值。

误区3：表达式求值结果没有被保存，就等于表达式没执行。
修正：只要执行路径到达，表达式会按语义求值；结果可能被丢弃。
```

工程应用：

```tex
读 CLI、日志、配置处理脚本时，先判断某一行是在“计算一个对象”，还是在“执行一个动作”。

对本地化资源处理工具：
    missing = source_keys - target_keys

右侧是集合差集表达式，整行是赋值语句。
后续报告逻辑依赖 missing 这个名字的绑定。
```

### 12.3 返回值、副作用、输出和回显

看到函数或方法调用表达式时，应固定问两个问题：

```tex
1. 它返回什么对象？
2. 它是否产生副作用？
```

`print(value)` 的主要作用通常是输出副作用：把文本写到输出流；它的返回值通常是 `None`。`list.append(value)` 的主要作用是原地修改列表；它的返回值也是 `None`。

```python
items = []
x = items.append("menu.start")
y = print(items)
```

执行后：

```tex
items -> ["menu.start"]
x -> None
y -> None
屏幕输出 -> ['menu.start']
```

常见误区：

```tex
误区1：append() 返回修改后的列表。
修正：append() 原地修改列表并返回 None。

误区2：屏幕上出现的文本就是 print() 的返回值。
修正：屏幕文本是输出副作用；print() 返回 None。

误区3：求值结果被丢弃也是副作用。
修正：丢弃结果不是副作用；修改对象、写文件、输出文本才是可观察副作用。
```

工程习惯：

```tex
1. 函数要给调用者结果，用 return。
2. 函数要给人看过程，用 print 或 logging。
3. 函数要改变已有对象，文档和命名都要暗示这是原地修改。
4. 不要把输出文本、日志记录和业务返回值混成同一件事。
```

### 12.4 脚本执行与 REPL 回显

脚本中的裸表达式会被执行并求值，但结果通常不会自动显示：

```python
"menu.start".upper()
```

作为 `.py` 文件运行时，这行通常不会产生屏幕输出。它不是没有求值，而是求值结果没有绑定给名字、没有传给 `print()`，也没有被其它语句使用。

REPL 中输入同样的表达式时，交互式环境通常会回显非 `None` 表达式值的 `repr()` 风格显示：

```python
>>> "menu.start".upper()
'MENU.START'
```

常见误区：

```tex
误区1：脚本没有显示，说明表达式没有执行。
修正：执行路径到达时表达式会求值，只是脚本不自动回显。

误区2：REPL 回显等于 print() 输出。
修正：REPL 回显通常是 display hook 显示表达式值；print() 是函数调用的输出副作用。

误区3：普通字符串表达式语句一定会在运行时创建字符串对象再丢弃。
修正：从源码语义看它是普通表达式语句；具体实现可能优化无副作用裸表达式。
```

工程应用：

```tex
1. 调试脚本时，不要依赖裸表达式“显示结果”。
2. 教学实验可用 REPL 快速观察值，但最终脚本要用明确的输出、日志或返回值。
3. 自动化脚本的输出是接口的一部分，随意 print 可能污染调用方解析。
```

### 12.5 物理行、逻辑行、续行和分号

物理行是编辑器里看到的一行；逻辑行是 Python 语法上认为的一条完整语句。

```python
config = {
    "locale": "zh_CN",
    "dry_run": True,
}
```

这段源码占多条物理行，但语法上是一条赋值语句。`()`、`[]`、`{}` 内部支持隐式续行。

三引号字符串（也只有三引号字符串）可以在字符串字面量内部包含换行，但它不应和括号内隐式续行混为同一种机制。分号可以在一个物理行里分隔多个简单语句：

```python
x = 1; y = 2; print(x + y)
```

工程习惯：

```tex
1. 优先使用括号内隐式续行，少用反斜杠显式续行。
2. 允许分号不代表推荐分号；工程代码中通常一行一条简单语句。
3. 格式换行不是对象结构；对象结构由表达式本身决定。
4. 长表达式换行时，让缩进服务阅读，不要制造类似代码块归属的错觉。
```

### 12.6 缩进代码块与控制流

Python <u>代码块的缩进</u>是语法结构，不是排版装饰。缩进表达归属关系：

```python
if missing:
    print("Missing keys:")
    print(sorted(missing))

print("Audit finished")
```

前两条 `print()` 属于 `if missing:` 的代码块；最后一条不属于该代码块。

代码块是否执行，取决于控制流是否进入。写在源码里不代表运行时一定执行。

常见误区：

```tex
误区1：代码块是运行时容器对象。
修正：代码块是源码语法结构；只有其中语句执行后，才会产生名字绑定、输出或对象修改。

误区2：源码里有这行，就说明这行执行过。
修正：必须判断控制流是否到达这行。

误区3：表达式跨行缩进完全自由。
修正：表达式跨行缩进必须处在合法续行环境中；否则缩进仍可能触发语法错误。
```

工程应用：

```tex
1. dry_run、verbose、debug、strict 等开关会改变执行路径。
2. 分析 bug 时先问：“这条语句是否真的被执行路径到达？”
3. 日志和返回值常用于验证控制流是否进入某个分支。
```

### 12.7 `def` 时间线：源码、函数对象和函数调用

`def` 相关问题要分三层：

```tex
1. 编译阶段：
   函数体源码被解析并编译成函数自己的 code object。

2. 执行 def 语句：
   创建函数对象，把函数名绑定到它。

3. 调用函数：
   函数体才从入口开始按控制流执行。
```

```python
print("before")

def demo():
    print("inside")

print("after")
```

脚本输出：

```tex
before
after
```

`print("inside")` 不会在执行 `def demo():` 时运行。只有调用 `demo()` 时才会执行函数体。

常见误区：

```tex
误区1：函数体在执行 def 时顺序执行一遍。
修正：执行 def 创建函数对象；函数体普通语句等调用时才执行。

误区2：函数体在编译阶段“执行走一遍”。
修正：更准确是解析、检查语法并编译成 code object；普通语句不会运行。

误区3：函数被调用时函数体所有语句都会执行。
修正：函数体从入口开始按控制流执行；if、return、break、continue、raise 都可能让部分语句不执行。
```

工程应用：

```tex
1. 函数定义阶段适合建立可复用动作；调用阶段才发生实际处理。
2. 函数体里的文件写入、网络请求、日志输出等副作用不会因为函数定义而发生。
3. 导入模块会执行顶层 def 语句，因此会创建函数对象；但不会调用这些函数。
```

### 12.8 注释、普通字符串表达式和文档字符串

注释以 `#` 开头，是源码说明，不是字符串字面量。

```python
# This is a comment.
```

三引号字符串不是注释，它仍然是字符串字面量。只有位于模块、类或函数体第一条语句位置的字符串字面量，才会被作为文档字符串特殊处理，并保存在相应对象的 `__doc__` 中。

```python
"""Module docstring."""

def load_resource():
    """Function docstring."""
    "ordinary string expression"
    return "ok"
```

这里：

```tex
模块 __doc__ 是 "Module docstring."。
load_resource.__doc__ 是 "Function docstring."。
"ordinary string expression" 不是文档字符串，也不是注释。
```

常见误区：

```tex
误区1：三引号字符串就是多行注释。
修正：三引号字符串是字符串字面量；真正注释是 #。

误区2：文档字符串是普通表达式求值产生的副作用。
修正：docstring 是特殊位置字符串字面量的特殊处理；__doc__ 是对象元数据。

误区3：任意能算出字符串的表达式都能成为文档字符串。
修正：docstring 需要字符串字面量，不是任意字符串表达式。
```

工程习惯：

```tex
1. 用 # 写局部解释或临时说明。
2. 用 docstring 写模块、类、函数的对外说明。
3. 不要用裸三引号字符串假装注释掉代码；它容易制造误解，也可能影响工具读取。
```

### 12.9 本阶段你提出过的问题与修正规则

1. 关于代码块缩进和表达式跨行缩进：

   ```tex
   你的理解：
       代码块缩进是语法结构；表达式跨行缩进相对更像可读性排版。

    修正：
       方向正确，但必须加条件：
       表达式跨行缩进要处在合法续行环境中，如 ()、[]、{} 内部或显式续行。
       否则行首缩进仍可能触发语法错误。
   ```

2. 关于 `break`、`continue`：

   ```tex
   你的问题：
       它们是否也算决定控制流走向的语句。

   修正：
       是。它们属于控制流转移语句。
       break 跳出最近一层循环；
       continue 跳过本轮剩余语句，进入下一轮循环判断或迭代。
   ```

3. 关于函数体是否在编译阶段“走一遍”：

   ```tex
   你的理解：
       函数体在源码编译阶段会“走”一遍，只是真正执行靠后。

   修正：
       不要说“执行走一遍”。
       更准确是：函数体源码会被解析、检查语法并编译成 code object；
       普通语句不会运行。运行要等函数调用。
   ```

4. 关于文档字符串：

   ```tex
   你的理解：
       特殊位置字符串字面量会成为文档字符串；
        三引号常用是因为方便多行。

    修正：
       主干正确。
       还要注意 docstring 取决于位置和字符串字面量形式，不取决于是否三引号；
       单引号、双引号也可以。
       普通位置的三引号字符串不是注释。
   ```

### 12.10 阶段测验暴露的薄弱处与修正规则

C10 阶段小测建议得分为 `96 / 100`。扣分点不在主干，而在术语精度和工程边界：

```tex
薄弱处1：示例代码中的 def f: 是语法笔误。
修正：函数定义必须写 def f():。概念说明里的示例代码也要能被 Python 解析。

薄弱处2：文档字符串模型偶尔仍接近“普通表达式求值后保存”。
修正：使用“特殊位置 + 字符串字面量 + __doc__ 元数据”模型。

薄弱处3：return 与函数调用表达式结果的关系还可更精炼。
修正：return 是控制流转移语句；函数调用表达式的值来自被调用函数执行到的 return，
      没有显式返回时通常是 None。

薄弱处4：日志文件副作用边界可以再工程化。
修正：除了文件内容、编码、缓冲、路径存在性，还要考虑权限、磁盘空间、文件占用；
      logging handler 也可能指向控制台、文件、队列、网络或外部系统。
```

这次测验确认的强项：

```tex
1. 能稳定区分表达式求值、语句执行、返回值和副作用。
2. 能正确预测 print(...)、list.append(...)、sorted(...)、if 分支和 return 的影响。
3. 能区分脚本裸表达式、REPL 回显和 print 输出。
4. 能说明 def 定义、函数对象创建和函数调用执行的时间线。
5. 能在本地化资源审计语境中解释集合差集、dry_run 早返回和日志副作用边界。
```

### 12.11 工程应知应会清单

```tex
1. 写脚本时，不要依赖裸表达式显示结果；需要观察就用 print、日志或调试器。
2. print 适合人类观察，不适合当成函数结果传递；函数结果应通过 return。
3. append、sort、update 等原地修改方法常返回 None，不要把它们链式赋值给目标名字。
4. 设计函数时区分三件事：返回给调用者的数据、写到外部的日志、修改的已有对象。
5. dry_run、verbose、debug 是典型控制流开关；分析时先判断开关是否让代码块执行。
6. 日志、文件写入、网络请求、数据库更新都是副作用边界。
7. def 创建函数对象，不执行函数体；函数调用才执行函数体。
8. return 结束当前函数调用；其后的同一执行路径语句不会继续执行。
9. 文档字符串服务于模块、类、函数的可读性和工具提取；普通注释服务于局部说明。
10. 代码块缩进属于语法，不是视觉建议；表达式续行缩进服务可读性，但必须处在合法续行环境中。
```

### 12.12 阶段精髓小结

```tex
1. 表达式求值产生对象；语句执行组织程序动作。
2. 返回值和副作用要分开问，尤其是 print、append、sort、update。
3. 脚本不会自动显示裸表达式结果；REPL 通常回显非 None 表达式值。
4. 物理行不等于逻辑行；括号内续行和分号分隔语句是两个方向的例子。
5. 缩进代码块表达语法归属；代码块是否执行由控制流决定。
6. def 执行创建函数对象；函数调用才执行函数体。
7. return 是控制流转移语句，它为函数调用表达式提供结果。
8. 注释、普通字符串表达式和文档字符串不是一回事。
9. 工程代码中要区分返回对象、输出文本、写文件、修改对象这些不同边界。
10. C10 的核心价值，是把 P2 的对象模型推进到“程序下一步执行什么”的语句层。
```

### 12.13 阶段后专题：Python 语句大全（预习版）

这部分是全 P3 预习索引，不等于 C10 已经全部展开。它的用途是：今后遇到任意一条 Python 语句时，先能判断它属于哪类、改变了什么、常见工程风险在哪里。

官方语言参考把语句大体分成两类：

```tex
simple statement：
    通常包含在一个逻辑行内。
    多条简单语句可以用分号写在同一物理行，但工程上通常不推荐。

compound statement：
    由一个或多个 clause 组成，通常带冒号和缩进 suite。
    典型作用是选择、循环、异常处理、资源管理、定义名字空间或异步控制流。
```

#### 12.13.1 先按“改变什么”分类

```tex
1. 只求值或主要为了副作用：
   expression statement

2. 改变名字绑定、对象槽位或类型元数据：
   assignment、augmented assignment、annotated assignment、del、type

3. 改变执行路径：
   if、match、while、for、break、continue、return、yield、raise、try

4. 管理资源和异常边界：
   with、try、raise、assert

5. 创建可复用对象或命名空间：
   def、class、async def、import

6. 改变作用域解析规则：
   global、nonlocal

7. 异步专用控制流：
   async def、async for、async with
```

硬规则：

```tex
先问“这条语句改变了什么”：
    名字绑定？
    对象本体？
    输出或外部状态？
    控制流路径？
    作用域规则？
    资源生命周期？
    异常传播？
```

#### 12.13.2 简单语句总览

| 语句 | 本质和功用 | 典型用例 | 工程选择、习惯和禁忌 |
| --- | --- | --- | --- |
| 表达式语句 | 执行一个表达式；在脚本中值通常被丢弃，在 REPL 中可能被回显 | `print(report)`、`items.append(x)`、调试时临时计算 | 适合调用有意义副作用的函数；不要把脚本裸表达式当输出；无副作用裸表达式通常应删除或改成断言、赋值、日志 |
| 赋值语句 `=` | 让目标绑定到右侧求值得到的对象；目标也可能是属性、下标或解包结构 | `total = sum(values)`、`a, b = b, a`、`head, *tail = items` | 先求右侧再绑定左侧；解包数量要匹配；赋值不是复制对象；属性和下标赋值会委托对象协议，可能触发副作用或异常 |
| 链式赋值 | 多个目标绑定同一个右侧对象 | `a = b = []` | 不可变对象通常安全；可变对象会共享引用；不要用 `a = b = []` 创建两个独立列表 |
| 增强赋值 | 把读取、运算和写回合成一条语句，目标只求值一次；可变对象可能原地修改 | `count += 1`、`items += more`、`flags \|= new_flags` | 不要简单等同于 `x = x + y`；列表 `+=` 常原地扩展，元组 `+=` 创建新对象；属性、下标目标可能有协议副作用 |
| 注解赋值 | 给变量、属性或下标写类型注解，并可同时赋值 | `name: str = "Alice"`、`cache: dict[str, int] = {}` | 注解服务静态分析和 IDE，不是自动运行时类型检查；函数局部注解不等于赋值；复杂注解要避免影响可读性 |
| `assert` | 调试断言；条件假时抛 `AssertionError` | `assert count >= 0`、内部不变量检查 | 不要用于用户输入校验、权限检查、业务必需检查；优化模式 `-O` 可移除 assert 代码 |
| `pass` | 空操作，占位满足语法需要 | 暂空函数、暂空类、空分支 | 适合临时骨架；长期保留要有理由；空实现通常比用无意义字符串表达式更清晰 |
| `del` | 删除名字绑定、属性、下标或切片 | `del cache[key]`、`del obj.attr`、`del items[:]` | 删除名字不等于销毁对象本身；对象是否释放取决于引用；删除下标会修改容器；不要用 `del` 掩盖生命周期设计问题 |
| `return` | 结束当前函数调用，并把表达式结果作为函数调用表达式的值；无表达式时为 `None` | `return result`、早返回 `return "skipped"` | 只能在函数体语法范围内使用；`finally` 仍会执行；不要在 `finally` 里随意 `return` 覆盖原异常或原返回 |
| `yield` | 让函数成为生成器；暂停函数并产出一个值，之后可恢复 | 流式读取大文件、逐条产生审计 issue | 适合惰性数据流；不要和普通 `return list` 混淆；生成器体内的副作用会随迭代时机发生 |
| `raise` | 抛出异常或重新抛出当前异常；可用 `from` 建立异常链 | `raise ValueError("bad locale")`、`raise RuntimeError(...) from exc` | 适合表达无法正常完成的路径；不要裸 `except` 后吞掉异常；保留异常链能帮助定位根因 |
| `break` | 跳出最近一层循环 | 找到目标后停止搜索 | 只影响最近循环；会跳过循环 `else`；多层循环需要更明确的函数拆分、标志变量或异常策略 |
| `continue` | 跳过本轮循环剩余语句，进入下一轮判断或迭代 | 过滤非法行、跳过空记录 | 适合提前排除噪声；过多 `continue` 会让循环主线碎片化；注意它不会跳出循环 |
| `import` | 加载模块并把名字绑定到当前命名空间 | `import json`、`import pathlib` | 顶层导入最清楚；导入会执行模块顶层语句；避免通配符导入污染命名空间 |
| `from ... import ...` | 从模块中绑定指定名字 | `from pathlib import Path` | 适合高频、语义清楚的名字；注意名字来源在代码中变短后可能不明显；避免 `from module import *` |
| `from __future__ import ...` | 启用未来语义，必须放在模块开头附近 | 历史兼容语义切换 | 只在确有版本语义需求时使用；不要当普通导入随处放 |
| `global` | 声明当前代码块内某名字解析为模块全局名字 | 简短脚本中更新模块级计数器 | 它是作用域声明，不是创建全局对象；工程中优先用参数、返回值、对象状态，少依赖可变全局状态 |
| `nonlocal` | 声明当前代码块内某名字来自最近的外层函数作用域 | 闭包中维护计数、缓存状态 | 只适合小闭包；复杂状态改用类或显式对象；外层必须已有绑定 |
| `type` | Python 3.12+ 的类型别名语句，创建类型别名对象 | `type ResourceMap = dict[str, str]` | 服务类型表达和静态分析；不是运行时校验；与 `class` 创建新类型不同 |

#### 12.13.3 复合语句总览

| 语句 | 本质和功用 | 典型用例 | 工程选择、习惯和禁忌 |
| --- | --- | --- | --- |
| `if` / `elif` / `else` | 按条件选择执行路径 | `if missing:` 输出缺失资源；`if dry_run:` 早返回 | 条件表达式要读得像业务判断；避免过深嵌套；优先处理特殊情况后早返回，让主路径清楚 |
| `match` / `case` | 结构化模式匹配，根据对象形状和值选择分支 | 匹配命令、事件、JSON 记录形状 | 适合结构清晰的分派；不是 C 风格 `switch`；case 不会自动 fall through；复杂守卫条件要保持可读 |
| `while` | 条件为真时重复执行代码块 | 读取直到队列为空、重试直到成功 | 必须能看出退出条件如何改变；避免无限循环；轮询和重试要考虑超时、退避和取消 |
| `for` | 从可迭代对象逐个取值并执行代码块 | 遍历文件行、资源 key、issue 列表 | 优先用于可迭代数据流；不要在迭代 dict/set 时改变大小；需要修改时先快照或构造新容器 |
| 循环 `else` | 循环正常耗尽时执行；被 `break` 打断则不执行 | 搜索未找到时报告 | 语义强但读者容易忘；团队不熟悉时可用标志变量或函数早返回替代 |
| `try` / `except` | 捕获并处理异常路径 | 解析 JSON、打开文件、转换输入 | 只捕获能处理的异常；异常范围尽量小；不要用宽泛 `except Exception` 静默吞错 |
| `try` / `else` | 没有异常时执行成功路径 | 解析成功后写入结构化结果 | 适合把“可能失败的动作”和“成功后动作”分开；避免把太多代码塞进 `try` |
| `try` / `finally` | 无论是否异常都执行清理逻辑 | 释放锁、恢复状态、关闭资源 | 清理必须小而可靠；不要随意在 `finally` 中 `return` 或抛新异常覆盖原问题 |
| `except*` | 处理异常组中的部分异常 | 并发任务中多个错误同时返回 | 属于较高级异常模型；适合后续并发或任务组场景；普通单异常处理不需要它 |
| `with` | 进入上下文管理器，保证退出时执行清理协议 | `with open(path, encoding="utf-8") as f:` | 文件、锁、临时目录、数据库事务常用；优先用 `with` 管理资源；不要手写容易漏的 open/close |
| `def` | 创建函数对象并绑定名字；函数体调用时才执行 | 封装清洗函数、审计函数、转换函数 | 函数边界要清楚区分参数、返回值、副作用；定义不执行函数体；docstring 写对外契约 |
| `class` | 创建类对象并绑定名字；类体在定义类时执行 | 定义异常类型、数据模型、服务对象 | 类体会执行，不要放重副作用；实例状态放 `__init__`；类属性和实例属性要分清 |
| `async def` | 创建协程函数；调用后得到协程对象，需 await 驱动执行 | 异步网络请求、异步文件/数据库客户端 | 适合 I/O 并发；不要在异步函数中直接阻塞事件循环；调用不等于立即跑完 |
| `async for` | 异步迭代协议上的循环 | 消费异步消息流、异步分页 API | 只能在协程函数中使用；每步迭代可能挂起；错误处理和取消要明确 |
| `async with` | 异步上下文管理器，进入和退出都可 await | 异步连接、会话、事务 | 只能在协程函数中使用；适合需要异步释放资源的对象；不要用普通 `with` 替代异步清理 |

#### 12.13.4 容易误认为“语句”的语法

| 语法 | 实际身份 | 正确理解 |
| --- | --- | --- |
| `lambda` | 表达式 | 创建匿名函数对象；适合短小回调，不适合复杂逻辑 |
| 条件表达式 `a if cond else b` | 表达式 | 产生一个值；不同于 `if` 语句组织代码块 |
| 列表、集合、字典推导式 | 表达式 | 创建新容器或生成数据；复杂副作用不要塞进去 |
| 生成器表达式 | 表达式 | 创建惰性迭代器；真正计算发生在迭代时 |
| 布尔运算 `and` / `or` / `not` | 表达式运算 | 可短路并返回操作数对象；不是控制流语句，但会影响表达式内部求值路径 |
| 装饰器 `@decorator` | 定义语句的一部分 | 附着在 `def` 或 `class` 上，改变被定义对象的绑定结果；不是单独可执行语句 |
| 类型注解 `x: T` | 注解赋值语句的一部分或函数签名的一部分 | 服务静态分析和工具；默认不是运行时类型强制 |

#### 12.13.5 工程选型规则

1. 需要得到一个对象继续使用：

   ```tex
   优先设计表达式或函数 return。
   不要靠 print 输出再让人眼复制。
   ```

2. 需要改变已有对象：

   ```tex
   使用赋值、增强赋值、方法调用或容器修改语句。
   函数命名和文档要提示“会原地修改”。
   ```

3. 需要根据条件选择路径：

   ```tex
   简单二选一用 if。
   结构化对象分派可考虑 match。
   过深嵌套优先早返回或拆函数。
   ```

4. 需要重复处理数据：

   ```tex
   有可迭代数据时优先 for。
   依赖外部状态或直到条件变化时用 while。
   大数据流可考虑生成器 yield。
   ```

5. 需要处理失败路径：

   ```tex
   可恢复错误用 try/except。
   无法满足契约用 raise。
   内部不变量用 assert，但不要拿 assert 做业务校验。
   ```

6. 需要管理资源：

   ```tex
   优先 with。
   异步资源用 async with。
   不要让 close、release、commit、rollback 散落在多条路径里。
   ```

7. 需要复用一段动作：

   ```tex
   用 def。
   先把输入、输出和副作用边界说清，再写函数体。
   ```

8. 需要组织数据和行为：

   ```tex
   用 class。
   但不要为了“看起来高级”把简单函数和字典过早包装成类。
   ```

9. 需要跨模块能力：

   ```tex
   用 import。
   顶层导入清晰，局部导入只在解决循环依赖、启动成本或可选依赖时考虑。
   ```

10. 需要作用域内可变状态：

    ```tex
    优先参数、返回值、对象属性。
    global 和 nonlocal 是明确声明作用域规则的工具，不是默认状态管理方案。
    ```

#### 12.13.6 常见禁忌和踩坑清单

```tex
1. 不要把“表达式有值”扩展成“语句都有返回值”。
2. 不要把 print 的输出当成 print 的返回值。
3. 不要把 append、sort、update 的返回值当成修改后的对象。
4. 不要用裸三引号字符串假装注释掉代码。
5. 不要依赖脚本裸表达式自动显示结果。
6. 不要在工程代码中用分号压缩多条简单语句。
7. 不要在迭代 dict/set 时改变大小。
8. 不要用 assert 做必须执行的输入校验、权限校验或业务校验。
9. 不要吞掉异常后不给日志、不给上下文、不给调用者信号。
10. 不要在 finally 中随意 return，容易覆盖原返回值或原异常。
11. 不要把 def 定义当成函数体已经执行。
12. 不要忘记 class 语句的类体会在定义类时执行。
13. 不要把 import 当成纯声明；导入会执行被导入模块的顶层语句。
14. 不要滥用 global/nonlocal 让状态流向变隐蔽。
15. 不要把 type 语句或类型注解当成运行时类型检查。
16. 不要把 match 当成会自动 fall through 的 switch。
17. 不要在 async def 中直接执行长时间阻塞 I/O。
18. 不要把循环 else 理解成“每轮循环后执行”；它是“循环正常结束后执行”。
```

#### 12.13.7 与后续小阶段的关系

```tex
C11_Assignments_Expressions_and_Prints：
    重点展开赋值、表达式语句、print、增强赋值、赋值目标和名字绑定。

C12_if_tests_and_syntax_rules：
    重点展开 if、布尔表达式、比较链、真值测试和语法细节。

C13_while_and_for_loops：
    重点展开 while、for、break、continue、循环 else、迭代协议。

C14_Iterations_and_Comprehensions：
    重点展开迭代工具、推导式、生成器表达式和 yield 的预备模型。

C15_Documentation：
    重点展开 docstring、注释、文档工具和代码可读性契约。

后续异常、函数、模块、类和异步章节：
    再系统展开 return、raise、try、with、def、class、import、async 等语句。
```

本专题的复盘硬规则：

```tex
看到一条 Python 语句，不先背语法名，而先问：

1. 它包含哪些表达式？
2. 哪些表达式会求值？
3. 它改变了哪个名字、哪个对象、哪个外部边界或哪条控制流路径？
4. 如果它不执行，是因为源码不存在、编译失败，还是控制流没有到达？
5. 如果它产生副作用，失败路径、资源释放和可测试性在哪里？
```

## 13. C11 赋值、表达式语句与输出：名字绑定、原地修改和 `print()` 边界

`C11_Assignments_Expressions_and_Prints` 的核心不是背更多赋值写法，而是把
C10 建立的“表达式求值 vs 语句执行”模型落实到每一个赋值目标和输出边界：

```tex
右侧表达式先求值
    -> 得到对象
    -> 左侧目标再绑定、写入、解包或触发对象协议
    -> 判断名字绑定是否改变
    -> 判断已有对象是否被原地修改
    -> 判断表达式结果是否被使用
    -> 判断输出副作用写向哪个流
```

本阶段复盘代码时，固定问以下问题：

```tex
1. 右侧表达式产生了什么对象？
2. 左侧目标是名字、属性、下标、切片，还是解包结构？
3. 改变的是名字绑定、对象本体、容器槽位，还是外部输出流？
4. 多个名字或容器槽位是否共享同一个可变对象？
5. 函数或方法调用返回什么？是否同时产生副作用？
6. 如果操作失败，之前已经发生的副作用是否会保留？（注意：解包赋值失败和元组内嵌列表的增强赋值的失败之间的区别）
```

### 13.0 阶段状态和可追溯入口

```tex
2026-06-15：正式进入 C11，先建立赋值与名字绑定模型。
2026-06-15 至 2026-06-17：按小步节奏完成链式赋值、解包、赋值目标、
                              增强赋值、表达式语句、print 输出流和综合复盘。
2026-06-19：C11 阶段测验逐题审批完成，建议得分 100 / 100，通过。
2026-06-19：学习画像已同步，C11 阶段末笔记完成整理。
```

相关阶段文件：

```tex
docs/C11_ASSIGNMENTS_EXPRESSIONS_AND_PRINTS_STARTUP_TEMPLATE.md
practice/P3_Statements_and_Syntax/C11_Assignments_Expressions_and_Prints/
practice/P3_Statements_and_Syntax/C11_Assignments_Expressions_and_Prints/
    stage_quiz_assignments_expressions_and_prints.md
projects/P3_Statements_and_Syntax/prompt_template_manager/
```

逐步实验脚本：

```tex
P3_C11_01_assignment_model.py
P3_C11_02_chain_and_multi_assignment.py
P3_C11_03_unpacking_assignment.py
P3_C11_04_attribute_subscript_slice_assignment.py
P3_C11_05_augmented_assignment.py
P3_C11_06_expression_statements_and_print.py
P3_C11_07_print_engineering_boundary.py
P3_C11_08_localization_audit_review.py
```

### 13.1 阶段地图

本阶段按以下顺序推进：

```tex
1. 普通赋值：右侧表达式先求值，左侧目标后处理。
2. 名字重新绑定 vs 对象原地修改。
3. 链式赋值、多目标赋值和共享可变对象。
4. 序列解包、星号解包、嵌套解包和数量不匹配错误。
5. 属性赋值、下标赋值、切片赋值和对象协议。
6. 增强赋值：原地修改机会、重新绑定和失败后副作用。
7. 表达式语句：求值、结果丢弃和有意义副作用。
8. print()：返回 None、输出副作用、sep/end/file/flush。
9. stdout、stderr、StringIO、文件流、日志与缓冲边界。
10. 本地化资源审计综合复盘与阶段测验。
```

阶段验收观察点：

```tex
1. 能否把“赋值执行效果”与“表达式返回值”分开。
2. 能否追踪多个名字和容器槽位保存的对象引用。
3. 能否判断增强赋值是否保留对象身份。
4. 能否识别属性、下标、切片目标可能触发对象协议。
5. 能否判断表达式语句的结果是否被丢弃、是否仍有副作用。
6. 能否说明 print 写向哪个流、返回值是否被错误使用。
7. 能否在工程函数中分离结构化返回数据和人类可读输出。
```

### 13.2 普通赋值的本质：右侧求值，左侧处理目标

最基础的赋值模型是：

```python
title = "menu.start".upper()
```

分层解释：

```tex
"menu.start".upper()
    是方法调用表达式；
    求值得到字符串对象 "MENU.START"。

title = "menu.start".upper()
    是赋值语句；
    执行效果是让名字 title 绑定到右侧得到的对象。
```

不能说“赋值语句返回了 `"MENU.START"`”。普通赋值语句不是普通表达式，不能
嵌入另一个表达式继续求值：

```python
# SyntaxError：增强赋值也是语句，不能作为 print 的实参表达式。
print(count += 1)
```

赋值也不是自动复制对象：

```python
source = ["menu.start"]
target = source

target.append("menu.quit")

print(source)           # ['menu.start', 'menu.quit']
print(source is target) # True
```

这里 `target = source` 只让两个名字绑定同一个列表对象。后续 `append()` 修改的
是共享列表本体，因此两个名字都能观察到变化。

本质总结：

```tex
名字重新绑定：改变某个名字下一步找到哪个对象。
对象原地修改：改变同一个对象的内部状态，所有别名都可能观察到。
赋值：默认不复制对象。
```

常见误区：

```tex
误区1：x = expr 会返回 expr 的值。
修正：expr 有值；赋值语句处理目标并产生执行效果。

误区2：变量“装着”对象。
修正：更稳定的模型是名字绑定对象；容器槽位保存对象引用。

误区3：a = b 会复制 b 指向的对象。
修正：普通赋值只共享对象；复制必须显式发生。
```

工程规则：

```tex
1. 中间结果需要继续使用时，用清楚的业务名字绑定它。
2. 需要独立容器时，显式构造或复制；不要期待赋值自动隔离。
3. 读代码时不要只盯等号，要先标出右侧表达式和左侧目标类型。
4. 避免把“赋值成功”描述成“赋值函数返回了某值”。
```

注解赋值只在本阶段预告：

```python
locale: str = "zh_CN"
```

它同时包含注解和赋值，但类型注解默认服务静态分析、IDE 和工具，不会自动把
运行时对象强制转换为 `str`，也不是运行时类型校验器。

### 13.3 链式赋值、多目标赋值和共享引用

链式赋值的右侧只求值一次：

```python
source = target = []
```

对象关系是：

```tex
一个列表对象 []
    <- source
    <- target
```

所以：

```python
source.append("menu.start")
print(target)  # ['menu.start']
```

如果需要两个独立列表，应分别创建：

```python
source = []
target = []
```

或在确实已有模板列表时显式复制：

```python
template = ["ui"]
source_tags = template.copy()
target_tags = template.copy()
```

链式赋值配合不可变对象通常不暴露原地修改风险：

```python
left = right = 0
left += 1

print(left)   # 1
print(right)  # 0
```

原因不是“链式赋值为整数复制了两份”，而是整数不可变，`left += 1` 产生结果
对象并重新绑定 `left`，`right` 仍绑定旧整数对象。

嵌套共享同样需要逐层分析：

```python
left = right = {"missing": []}
left["missing"].append("menu.quit")

print(right)  # {'missing': ['menu.quit']}
```

此处外层字典和内层列表都被共享。另一个常见陷阱是重复引用：

```python
rows = [[]] * 3
rows[0].append("menu.start")

print(rows)  # 三个槽位都观察到同一个内部列表变化
```

常见误区：

```tex
误区1：a = b = [] 会创建两个空列表。
修正：右侧只创建一个列表，两个目标共享它。

误区2：不可变对象上的链式赋值会自动复制对象。
修正：名字最初仍可绑定同一对象；后续运算通常创建结果对象并重新绑定。

误区3：只看外层容器数量，不看内部引用。
修正：先数对象，再画每个名字和槽位保存的引用。
```

工程适用场景和禁忌：

```tex
适用：多个状态名确实要共享同一个不可变配置对象。
谨慎：多个缓存、结果列表、错误列表需要独立状态时不要链式赋可变对象。
禁忌：用 a = b = [] 表达“初始化两个独立收集器”。
技巧：看到链式赋值右侧是 list/dict/set 或含可变对象的结构时，立即检查别名风险。
```

### 13.4 解包赋值：右侧整体求值，左侧按结构绑定

普通解包：

```python
key, text = ("menu.start", "Start Game")
```

安全交换：

```python
left, right = right, left
```

它能够安全交换，是因为右侧先整体求值并保留原对象引用，随后才处理左侧目标。

星号解包：

```python
head, *middle, tail = ["menu", "main", "start"]

print(head)    # menu
print(middle)  # ['main']
print(tail)    # start
```

星号目标得到一个新列表；即使收集不到元素，也得到空列表：

```python
head, *rest = ["menu.start"]
print(rest)  # []
```

但是“星号目标得到新外层列表”不等于深拷贝元素：

```python
entry = ("menu.start", ("Start", "开始"), ["ui", "main"])

key, (source_text, target_text), tags = entry
head, *rest = entry

tags.append("checked")

print(entry[2])          # ['ui', 'main', 'checked']
print(rest[1] is tags)   # True
```

`tags` 直接绑定原内部列表；`rest` 是新外层列表，但它保存的元素引用仍可能指向
原对象。

数量不匹配会抛出 `ValueError`：

```python
a, b = ["menu.start"]  # not enough values to unpack
```

解包失败发生在左侧目标写入之前；不会留下“只赋值了第一个目标”的半完成状态。

下划线只是约定：

```python
key, _, text = ("menu.start", "comment", "Start")
```

`_` 仍然是普通名字，并没有语言级“丢弃值”魔法。工程中用它表达“这个值刻意
不用”，但不要在同一作用域反复把 `_` 当成重要业务变量。

工程应用：

```tex
1. 解析固定形状的 CSV 行、数据库行、函数多返回值。
2. 分解本地化 key：namespace、group、name。
3. 用星号目标收集长度可变的中间部分。
4. 用嵌套解包表达嵌套记录形状，但结构过深时应改用具名对象或显式索引。
5. 外部数据形状不可信时，先校验长度或捕获明确异常，不要让解包错误难以定位。
```

### 13.5 名字、属性、下标和切片赋值目标

赋值左侧不一定是局部名字：

| 左侧目标 | 典型例子 | 主要效果 | 可能触发的边界 |
| --- | --- | --- | --- |
| 名字 | `result = value` | 改变名字绑定 | 命名空间和作用域 |
| 属性 | `entry.key = value` | 写入对象属性目标 | `__setattr__`、描述符、属性规则 |
| 下标 | `record["key"] = value` | 写入容器或自定义对象槽位 | `__setitem__`、校验、日志、副作用 |
| 切片 | `items[1:] = values` | 原地替换可变序列的一段 | 长度变化、别名可见性 |
| 解包 | `a, *rest = values` | 按结构处理多个目标 | 数量不匹配、浅层引用共享 |

属性赋值：

```python
class Entry:
    pass

entry = Entry()
entry.key = "menu.start"
```

更精确的说法是：把对象引用写入 `entry` 的属性目标。不要完全套用“局部变量名
重新绑定”的说法；自定义类型还可能通过 `__setattr__` 或描述符执行额外逻辑。

下标赋值和修改内部对象不是一回事：

```python
record = {"tags": ["ui"]}

record["tags"].append("checked")
# 修改旧列表对象本体。

record["tags"] = record["tags"] + ["reviewed"]
# 创建新列表，再替换字典中该 key 对应的值引用。
```

自定义下标协议可以产生多重副作用：

```python
class AuditStore:
    def __init__(self):
        self.data = {}
        self.history = []

    def __setitem__(self, key, value):
        self.history.append(("set", key, value))
        self.data[key] = value
```

执行：

```python
store["menu.start"] = "Start"
```

会触发 `__setitem__`，同时修改 `history` 和 `data`。所以属性或下标赋值不能简单
概括成“给变量改值”。

切片赋值会原地修改列表，并且普通步长切片可以改变长度：

```python
keys = ["menu.start", "menu.quit", "menu.options"]
keys[1:] = ["menu.settings"]

print(keys)  # ['menu.start', 'menu.settings']
```

还可以用空切片插入：

```python
keys[1:1] = ["menu.options"]
```

下标赋值通常替换一个槽位，切片赋值用右侧可迭代对象替换一段内容。字符串不
支持下标或切片赋值，因为 `str` 不可变：

```python
text = "hello"
# text[0] = "H"  # TypeError
```

工程规则：

```tex
1. 看到 obj.attr = value，检查属性校验、描述符和 __setattr__。
2. 看到 obj[key] = value，检查 __setitem__ 是否可能记录日志、校验或抛异常。
3. 区分“替换容器槽位引用”和“修改槽位指向的对象本体”。
4. 切片赋值会让所有列表别名看到变化；需要新列表时使用切片表达式或列表拼接。
5. 切片赋值右侧必须可迭代；扩展切片带步长时还可能要求长度匹配。
```

### 13.6 增强赋值：一次求目标、原地操作机会和写回

增强赋值不是简单的文本替换：

```python
x += y
```

应按以下模型理解：

```tex
1. 求值赋值目标一次。
2. 读取目标当前对象。
3. 尝试增强运算；对象可能原地修改，也可能返回新对象。
4. 把结果写回原目标。
```

不同对象的典型表现：

| 对象类型 | 示例 | 常见结果 |
| --- | --- | --- |
| `int` | `count += 1` | 创建结果整数并重新绑定 |
| `str` | `query += clause` | 创建结果字符串并重新绑定 |
| `tuple` | `items += more` | 创建结果 tuple 并重新绑定 |
| `list` | `items += more` | 通常原地扩展并保留身份 |
| `set` | `flags |= new_flags` | 原地更新集合 |
| `dict` | `record |= updates` | 原地更新映射，冲突 key 取右侧值 |

列表 `+=` 与列表 `+` 的别名差异：

```python
a = ["menu.start"]
alias_a = a
a += ["menu.quit"]

b = ["menu.start"]
alias_b = b
b = b + ["menu.quit"]
```

结果：

```tex
a is alias_a -> True
alias_a      -> ['menu.start', 'menu.quit']

b is alias_b -> False
alias_b      -> ['menu.start']
```

`append()`、`extend()` 和 `+=` 也要分开：

```tex
items.append(x)
    把 x 作为一个元素追加；原地修改；返回 None。

items.extend(iterable)
    把 iterable 的元素逐个追加；原地修改；返回 None。

items += iterable
    对 list 通常原地扩展；仍是增强赋值语句，不是方法调用表达式。
```

高级边界：tuple 内部 list 的增强赋值写回失败：

```python
box = (["menu.start"],)

try:
    box[0] += ["menu.quit"]
except TypeError:
    pass

print(box)  # (['menu.start', 'menu.quit'],)
```

执行顺序：

```tex
读取 box[0]
    -> 内部 list 先被 += 原地扩展
    -> 尝试把结果写回 box[0]
    -> tuple 不支持下标赋值，抛 TypeError
    -> 已发生的 list 修改不会自动回滚
```

这个例子说明：增强赋值不是事务式操作。后续步骤失败，不代表此前副作用会撤销。

工程适用场景：

```tex
count += 1：计数器更新，int 重新绑定。
query += clause：小规模字符串累积，但大量拼接应考虑 list + join。
issues += new_issues：希望原列表别名都看到扩展时使用。
flags |= new_flags：集合状态合并。
config |= overrides：字典覆盖更新，必须清楚冲突策略。
```

常见禁忌：

```tex
1. 不要无条件把 x += y 改写成 x = x + y，并声称语义完全一致。
2. 有别名时，不要忽略 list += 会影响所有共享引用。
3. 属性和下标增强赋值可能同时触发读取协议、原地运算和写回协议。
4. 不要假设异常发生就没有任何状态变化。
5. 不要用 += 隐藏一个本应显式说明的覆盖或累积规则。
```

### 13.7 表达式语句：求值不等于自动显示

表达式语句会对表达式求值；在普通脚本中，结果通常被丢弃：

```python
"menu.start".upper()
```

这行在脚本中通常没有可见输出。它不是没有求值，而是结果没有被绑定、返回、
传给其它函数或写入外部边界。

REPL 对非 `None` 表达式值通常进行回显：

```python
>>> "menu.start".upper()
'MENU.START'
```

REPL 回显不是 `print()` 输出；它通常通过交互式显示钩子展示表达式值的
`repr()` 风格形式。

表达式语句是否有意义，要看副作用和结果用途：

| 表达式语句 | 脚本中的判断 | 原因 |
| --- | --- | --- |
| `missing.append(key)` | 通常有意义 | 原地修改列表 |
| `print("done")` | 通常有意义 | 写入输出流 |
| `logger.warning(msg)` | 通常有意义 | 交给日志 handler |
| `sorted(missing)` | 通常可疑 | 新列表结果被丢弃 |
| `"menu.start".upper()` | 通常可疑 | 新字符串结果被丢弃 |

常见误区：

```tex
误区1：脚本没有显示，说明表达式没执行。
修正：执行路径到达时会按语义求值；只是脚本不自动回显结果。

误区2：返回值没保存，所以没有副作用。
修正：append、print、日志调用、文件写入都可能在结果被丢弃时产生副作用。

误区3：表达式被求值就一定有副作用。
修正：求值得到新对象不等于修改外部可观察状态。
```

工程规则：

```tex
1. 无副作用且结果未使用的表达式语句通常应删除或改为赋值、return、断言。
2. 有副作用的调用应从命名、文档和上下文中让读者看出目的。
3. 调试脚本不要依赖裸表达式显示结果；使用明确 print、logging 或调试器。
4. 自动化 CLI 的 stdout 可能是机器接口，随意 print 会污染调用方解析。
```

### 13.8 `print()`：返回 `None`，文本写入输出流

`print()` 是函数调用表达式：

```python
result = print("audit finished")
```

分层解释：

```tex
输出副作用：把文本写入目标输出流。
返回值：None。
名字 result：绑定到 None。
```

常用参数：

| 参数 | 作用 | 不会改变什么 |
| --- | --- | --- |
| `sep` | 连接多个待输出对象 | 不改变 `print()` 返回值 |
| `end` | 指定输出末尾文本 | 不改变对象本体 |
| `file` | 选择目标文本流 | 不把输出文本变成返回值 |
| `flush` | 请求刷新目标流 | 不保证物理持久化，不改变返回值 |

示例：

```python
from io import StringIO

buffer = StringIO()
result = print(
    "missing",
    "menu.quit",
    sep=": ",
    end="!\n",
    file=buffer,
)

print(result is None)        # True
print(buffer.getvalue())     # 取得已经写入内存流的文本
```

`buffer.getvalue()` 返回的字符串自带 `\n`；如果再交给默认 `print()`，外层
`print()` 还会追加自己的默认换行，因此屏幕上可能多出一个空行。这是输出文本
内容与外层输出格式共同作用的结果。

输出流边界：

```tex
sys.stdout：常规结果、人类可读报告；也可能被 shell 管道或重定向捕获。
sys.stderr：警告、错误、诊断信息；与 stdout 是不同的流。
StringIO：内存文本流，适合测试和捕获输出。
文本文件对象：持久化文本，需要路径、权限、编码、关闭和失败路径设计。
logging handler：可指向控制台、文件、队列、网络或外部日志系统。
```

stdout 和 stderr 即使显示在同一个终端，也不代表是同一个流；重定向、缓冲和
消费方都可能不同。

`flush=True` 的准确边界：

```tex
它请求刷新 Python 文本流相关缓冲。
它不改变输出文本。
它不改变 print() 返回的 None。
它不等同于操作系统级 fsync，也不保证数据已经永久写入物理介质。
```

`print(..., file=f)` 与 `f.write(...)`：

```tex
print：
    接受多个对象；会做文本转换；支持 sep/end；返回 None。

write：
    通常要求直接传入 str；不自动添加换行；返回写入字符数。
```

工程禁忌：

```tex
1. 不要写 report = print(...) 并期待 report 是报告文本。
2. 不要把业务结果只打印到屏幕；调用者需要的数据应通过 return 返回。
3. 不要默认 stdout 只给人看；CLI 中它可能是稳定接口。
4. 不要把 stderr 当成“程序一定失败”；它也常承载诊断和警告。
5. 写文件时不要忽略覆盖模式、编码、权限、磁盘空间、关闭和异常路径。
6. 描述默认参数时说“调用使用默认值”，不要说“参数指向默认值”。
```

### 13.9 工程连接：本地化审计与 `prompt_template_manager`

本阶段用真实代码形态连接了赋值、修改与输出边界。

`prompt_template_manager` 中的典型语义：

```python
record = dict(row)
```

创建新字典对象并让名字 `record` 绑定它。这是新外层对象，不代表内部所有值都
被深拷贝。

```python
record["tags"] = normalized_tags
```

这是下标赋值，修改字典中对应表项的值引用。

```python
clauses.append(clause)
params.extend(values)
```

这是方法调用表达式语句：原地修改已有列表，返回值通常是 `None`。

```python
query += " WHERE " + " AND ".join(clauses)
```

`query` 绑定 `str`，字符串不可变，因此这里创建结果字符串并重新绑定 `query`。

```python
print(message, file=sys.stderr)
```

把诊断文本写入错误流；返回值仍是 `None`。

本地化缺失 key 审计的最小数据流：

```python
def check_missing_keys(source_keys, target_keys, output=None):
    source_set = set(source_keys)
    target_set = set(target_keys)
    missing = sorted(source_set - target_set)

    result = {
        "missing_count": len(missing),
        "missing_keys": missing,
    }

    if output is not None:
        print("Missing count:", len(missing), file=output)
        for key in missing:
            print("missing:", key, file=output)

    return result
```

三层职责：

```tex
内部业务结果：dict/list/set 等结构化对象。
调用接口：return 把结构化结果交给调用者。
可选副作用：print(..., file=output) 生成人读摘要。
```

这样调用者可以不输出、输出到控制台、写入 `StringIO`、写文件或进一步转换成
JSON，而不需要从屏幕文本中反向解析业务数据。

### 13.10 阶段性综合复盘与固定检查表

本阶段多次使用本地化缺失 key 摘要，把知识点串到同一条执行链中：

```python
missing_count = 0
missing_keys = []
report = StringIO()

missing_count += 1
missing_keys.append("menu.quit")
printed = print("missing: menu.quit", file=report)
visible = missing_keys + ["menu.options"]
```

逐行判断：

```tex
missing_count += 1
    int 不可变；产生结果对象并重新绑定名字。

missing_keys.append(...)
    原地修改 list；返回 None；调用作为表达式语句使用。

printed = print(..., file=report)
    向 StringIO 写文本；printed 绑定 None。

visible = missing_keys + [...]
    创建新外层列表；不修改 missing_keys。
```

面对任意 C11 代码片段，使用这张检查表：

```tex
第一问：右侧何时求值，产生什么对象？
第二问：左侧目标属于哪一类？
第三问：目标处理后，哪个名字或槽位发生变化？
第四问：是否有已有可变对象被原地修改？
第五问：是否存在别名，谁能观察到变化？
第六问：调用表达式返回什么，结果是否被使用？
第七问：副作用写向内存、stdout、stderr、文件还是日志系统？
第八问：失败时，已经发生的副作用是否需要清理或回滚？
```

### 13.11 本阶段你的理解轨迹、问题与修正规则

本阶段没有出现持续卡住的主干问题。学习过程中的表现是：每完成一个小步后都能
确认对象关系和输出边界，并在收束前代码阅读题中稳定迁移。需要记录的重点不是
“大方向答错”，而是预防性修正、规格审查和术语精度。

1. 关于启动模板与学习节奏：

   ```tex
   你的明确要求：
       只以 C11 启动模板作为本会话正式教学入口，安全忽略已创建的同主题文件。

   落地规则：
       既有文件可以作为历史背景或阶段产物，但不能反过来决定教学顺序。
       本阶段按赋值 -> 链式赋值 -> 解包 -> 赋值目标 -> 增强赋值
       -> 表达式语句 -> print 输出流 -> 综合复盘推进。
   ```

2. 关于赋值语句“返回值”：

   ```tex
   预计误区：x = expr 返回 expr 的值。
   修正：右侧 expr 有值；赋值语句处理目标，不能当作普通返回值表达式。
   测验结果：已稳定掌握。
   ```

3. 关于链式赋值：

   ```tex
   预计误区：a = b = [] 创建两个列表。
   修正：右侧只创建一个列表；两个名字共享同一对象。
   测验结果：能继续追踪某个名字被列表 + 结果重新绑定后的别名分离。
   ```

4. 关于解包：

   ```tex
   预计误区：星号目标得到的列表等于深拷贝所有元素。
   修正：星号目标创建新外层 list，内部元素引用仍可能共享。
   补充：解包数量失败发生在左侧写入前，不会留下部分赋值。
   ```

5. 关于增强赋值：

   ```tex
   预计误区：x += y 永远等同于 x = x + y。
   修正：增强赋值给对象原地操作机会，并将结果写回目标；身份和别名行为可能不同。
   测验结果：能准确解释 tuple 内 list 已修改、写回却失败的非事务式边界。
   ```

6. 关于方法调用和 `print()`：

   ```tex
   预计误区：append 返回修改后的列表，print 返回已输出文本。
   修正：二者通常返回 None；价值主要来自原地修改或输出副作用。
   测验结果：已稳定掌握，并能设计结构化 return + 可选输出流接口。
   ```

7. 关于题干规格审查：

   ```tex
   你在测验中主动指出：
       C1 题干“三条赋值语句”的范围可能有歧义；
       D2 文字中的 text += "!" 与实际代码 text += ".start" 不一致。

    正确处理：
       明确指出歧义，以实际待执行代码为准，并说明不影响本题核心结论。
   ```

### 13.12 阶段测验暴露的薄弱处与修正规则

本阶段测验建议得分为 `100 / 100`，通过
`C11_Assignments_Expressions_and_Prints` 小阶段。没有发现影响代码行为判断、
对象模型、返回值、副作用或工程边界的实质错误。

不扣分但需要继续精修的三处术语：

```tex
精修点1：把“entry.key 绑定到字符串”说得更精确
修正：属性赋值通过属性目标或对象协议写入对象引用；它不是局部名字绑定。

精修点2：把“参数指向默认值”改得更精确
修正：调用时没有显式传入该实参，因此函数使用参数的默认值。

精修点3：条件表达式与真值测试继续分层
修正：target_text is None 等表达式先求值得到结果，if 再对结果做真值测试。
```

这次测验确认的强项：

```tex
1. 能稳定区分赋值语句执行效果、表达式值、返回值和副作用。
2. 能分析名字、属性、下标、切片和解包目标。
3. 能追踪链式赋值、浅拷贝和星号解包中的对象共享层级。
4. 能按对象类型判断增强赋值是原地修改还是重新绑定。
5. 能解释增强赋值失败后此前副作用不自动回滚。
6. 能把 print 的返回值、输出文本和 file 指定的输出流分开。
7. 能说明 stdout、stderr、StringIO、文件流、缓冲和持久化边界。
8. 能设计结构化返回数据与可选人读输出相分离的工程接口。
9. 能主动发现题干与代码不一致，并按可验证源码处理。
```

### 13.13 工程应知应会清单

```tex
1. 普通赋值先求右侧，再处理左侧目标。
2. 赋值语句有执行效果，但不要说它像函数一样返回右侧值。
3. a = b 共享对象，不自动复制。
4. 名字重新绑定不改变旧对象；旧对象是否仍存在取决于其它引用。
5. 原地修改会被所有共享该对象的别名观察到。
6. a = b = [] 只创建一个列表；独立收集器要分别创建。
7. 多目标赋值和解包会先完成右侧求值，再处理左侧目标。
8. 星号解包目标得到新 list，但不会深拷贝元素。
9. 解包数量不匹配会抛 ValueError；失败前不会部分写入左侧目标。
10. 下划线 `_` 只是“刻意不用”的命名约定，仍是普通名字。
11. 属性赋值可能触发 __setattr__ 或描述符协议。
12. 下标赋值可能触发 __setitem__，不只是修改内置容器。
13. record[k] = v 是替换表项；record[k].append(x) 是修改值对象。
14. 切片赋值原地修改列表，并可能改变列表长度。
15. str、tuple 等不可变对象不支持内容槽位赋值。
16. 增强赋值会读取目标、尝试增强运算并写回目标。
17. list += 通常原地扩展；list + 创建新列表。
18. int/str/tuple 的 += 通常创建结果对象并重新绑定名字。
19. set |= 和 dict |= 通常原地更新；要明确合并或覆盖规则。
20. 增强赋值不是事务；写回失败时此前原地副作用可能保留。
21. append/extend/sort/update 等原地方法通常返回 None。
22. sorted(...) 返回新列表；结果不使用的裸调用通常可疑。
23. 脚本裸表达式通常不自动显示；REPL 回显不是 print 输出。
24. print() 写文本并返回 None。
25. sep/end 改变输出文本格式，不改变 print 返回值。
26. file 决定输出流，不把输出文本变成返回值。
27. flush 改变刷新时机，不等于物理持久化保证。
28. stdout、stderr 即使显示在同一终端，也仍是不同流。
29. StringIO 是内存文本流，适合捕获输出和测试 file= 接口。
30. print(file=f) 与 f.write(text) 的参数、换行和返回值不同。
31. 函数应 return 结构化业务结果；print/logging 是可选副作用。
32. 自动化 CLI 要谨慎规划 stdout 和 stderr，避免污染机器可读输出。
33. 文件输出要考虑路径、权限、编码、覆盖、磁盘空间、缓冲和关闭。
34. 看到异常时检查此前是否已有对象修改、文件写入或日志副作用。
35. 类型注解服务工具，不自动实施运行时类型检查。
```

### 13.14 阶段精髓小结

```tex
1. 赋值的核心不是“盒子装值”，而是右侧求值后处理左侧目标。
2. 名字绑定、对象属性、容器槽位和输出流是不同层次。
3. 普通赋值不复制对象；共享引用必须显式纳入推理。
4. 链式赋值让多个目标获得同一个右侧对象。
5. 解包按结构处理目标；星号目标创建新外层列表但不深拷贝元素。
6. 属性、下标和切片赋值可能修改对象并触发协议。
7. 增强赋值给对象原地修改机会，不能无条件等同于普通二元运算后赋值。
8. list += 常保留身份；int/str/tuple += 常产生结果对象并重新绑定。
9. 增强赋值失败不保证回滚此前已经发生的原地修改。
10. 表达式语句会求值；脚本中结果通常被丢弃，但副作用仍可能发生。
11. 无副作用且结果未使用的表达式语句通常是可疑代码。
12. print() 的输出是副作用，返回值是 None。
13. sep/end 决定文本格式，file 决定输出位置，flush 决定刷新请求。
14. stdout、stderr、StringIO、文件和日志 handler 是不同工程边界。
15. 业务结果应通过 return 交给调用者，人读输出应作为可选副作用。
16. C11 的核心价值，是把 P2 的对象模型和 C10 的语句模型统一成可执行的代码阅读方法。
```

进入 `C12_if_Tests_and_Syntax_Rules` 后，继续沿用同一套方法：先判断条件表达式
如何求值，再判断 `if` 是否进入代码块；同时重点观察真值测试协议、`and` / `or`
短路时返回的操作数对象、比较链求值顺序，以及条件表达式和 `if` 语句的边界。

## 14. C12 条件、真值测试与语法规则：短路求值、比较链和控制流选择

### 14.0 阶段状态和可追溯入口

本阶段正式名称：`C12_if_Tests_and_Syntax_Rules`。

当前阶段已经完成：正式实验脚本、逐步预测学习、阶段测验、逐题批改和学习画像同步。
阶段测验建议得分为 `100 / 100`，小阶段通过。

本阶段的正式入口是：

```tex
docs/C12_IF_TESTS_AND_SYNTAX_RULES_STARTUP_TEMPLATE.md
```

实践与验收材料主要位于：

```tex
practice/P3_Statements_and_Syntax/C12_if_Tests_and_Syntax_Rules/
    README.md
    01_truth_testing_objects_and_protocols.py
    02_short_circuit_operand_results.py
    03_comparisons_identity_and_membership.py
    04_comparison_chains_evaluation_order.py
    05_if_elif_else_branch_selection.py
    06_conditional_expressions_and_readability.py
    07_localization_rule_decision_pipeline.py
    08_prompt_manager_conditions_and_match_boundaries.py
    stage_quiz_if_tests_and_syntax_rules.md
```

目录中形如 `P3_C12_*.py`、`audit_control.py`、`synthetic_function_1st_edition.py`
的文件保留为个人练手或测试轨迹，不作为本阶段正式教学顺序和验收依据。

本阶段延续 C10/C11 的核心方法：

```tex
C10：表达式求值 vs 语句执行。
C11：右侧求值、左侧目标处理、名字绑定、原地修改和输出副作用。
C12：条件位置先得到对象，再按真值测试和控制流规则选择后续路径。
```

### 14.1 阶段地图

本阶段按启动模板逐步推进，顺序如下：

```tex
1. 真值测试基础：if x 不是 if x == True。
2. 自定义真值协议：__bool__()、__len__()、默认真值和错误边界。
3. and / or / not：短路求值、返回操作数对象和副作用是否发生。
4. 比较、身份和成员测试：==、is、in 问的是不同问题。
5. 比较链：中间表达式只求值一次，失败后短路。
6. if / elif / else：互斥分支链、多个独立 if、缩进归属和 pass。
7. 条件表达式：x if condition else y 产生值，不适合塞复杂副作用。
8. 本地化审计决策：strict、dry_run、缺失 key、空译文和输出路径。
9. match 边界：结构化模式分派，不是 C / Java 风格 switch。
```

贯穿全章的固定分析链：

```tex
第一问：条件位置里的表达式是否真正求值？
第二问：该表达式返回哪个对象？
第三问：该对象如何参与真值测试？
第四问：and / or / 比较链是否短路？
第五问：哪些调用、副作用或异常没有发生？
第六问：控制流进入哪个代码块？
第七问：最终名字绑定、对象修改或外部输出发生了什么？
```

### 14.2 真值测试的本质：对象先产生，真假再判定

`if` 后面的条件位置不是只能放 `True` 或 `False`。它放的是一个表达式；表达式先求值，得到一个对象，然后 Python 对这个对象做真值测试。

最核心的区别：

```python
if x:
    ...

if x == True:
    ...
```

二者不是一回事。

```tex
if x:
    对 x 绑定的对象做真值测试。

x == True:
    做相等性比较，问 x 绑定的对象是否与 True 相等。
```

典型例子：

```python
x = [1]

print(bool(x))     # True
print(x == True)  # False
```

`[1]` 是非空列表，因此真值为真；但列表 `[1]` 并不等于布尔对象 `True`。

本阶段必须长期保留三层边界：

```tex
对象本体：
    x 实际绑定的对象，例如 []、[""]、"0"、None、自定义实例。

真值测试结果：
    bool(x) 得到的 True 或 False。

相等性比较结果：
    x == True、x == False、x == "" 等比较表达式得到的 True 或 False。
```

容器的真值测试不递归检查内部所有元素：

```python
print(bool(""))    # False
print(bool([""]))  # True
```

空字符串是假值；装着一个空字符串的列表是非空列表，因此是真值。

工程规则：

```tex
1. 想判断“有没有元素”，可以使用 if items:。
2. 想判断“所有元素是否都为真”，使用 all(items)。
3. 想判断“是否存在任意真值元素”，使用 any(items)。
4. 不要把 if items: 误写成 if items == True:。
5. 对 None 与空字符串、空列表、0 有不同业务含义时，必须用 is None 精确判断。
```

### 14.3 真值协议：`__bool__()`、`__len__()` 和默认真值

Python 对对象做真值测试时，不是“反复调用特殊方法直到某次返回 bool”。更准确的规则是：<u>按优先级选择一个入口，只调用该入口**一次**；返回类型不合规则直接报错。</u>

规则可以压成这样：

```tex
1. 如果对象本身就是 True 或 False，真值判定直接得到对应真假。
2. 否则，如果类型提供 __bool__()，调用一次；它必须返回真正的 bool 对象。
3. 否则，如果类型提供 __len__()，调用一次；它必须返回非负整数。
4. 否则，普通对象默认为真。
```

注意两条协议边界：

```tex
__bool__():
    必须返回 True 或 False。
    返回 1、[]、"yes" 等对象都会 TypeError。

__len__():
    必须返回非负整数。
    返回 0 表示假；返回正整数表示真；返回负数会 ValueError。
```

典型实验：

```python
class ByLength:
    def __len__(self):
        print("__len__ called")
        return 1


class ByBoolAndLength:
    def __bool__(self):
        print("__bool__ called")
        return False

    def __len__(self):
        print("__len__ should not be called")
        return 1


print(bool(ByLength()))         # 调用 __len__，结果 True
print(bool(ByBoolAndLength()))  # 调用 __bool__，结果 False
```

本质总结：

```tex
__len__ 是没有 __bool__ 时的后备规则，
不是 __bool__ 出错后的异常恢复机制。
```

你在本阶段测验中已经掌握：

```tex
1. 普通自定义对象没有 __bool__ 和 __len__ 时默认为真。
2. StrictLocalizedEntries 有 __bool__ 时，不会退回去调用继承来的 __len__。
3. __bool__ 返回 1 会 TypeError，不会把 1 再拿去真值测试。
4. __len__ 返回 -1 是协议错误，不会被解释成真或假。
```

本阶段最后追问中，你提出过一个重要问题：如果条件位置表达式求值结果已经是 `bool` 对象，例如 `if True:`，是否还会机械调用特殊方法？

修正规则：

```tex
if True:
    表达式结果已经是布尔对象 True。
    语义上就是对 True 做真值判定，结果为真。

不要理解成：
    Python 递归调用 __bool__ / __len__，直到某次返回 bool。

应理解成：
    条件表达式先得到一个对象；Python 用真值测试协议判定它为真或假。
    对自定义对象，协议入口只按优先级选择一次；__bool__ 返回非 bool 会 TypeError。
```

这里也要区分两个说法：

```tex
条件位置里的表达式：
    if 后面的普通表达式，例如 strict and issues。

Python 语法里的条件表达式：
    x if condition else y，用来二选一地产生一个值。
```

二者都涉及“条件”，但不是同一个语法概念。

### 14.4 `and` / `or` / `not`：短路顺序和返回对象

`and` / `or` 使用真值测试结果决定路径，但最终返回的是某个操作数对象本身，不保证返回 `bool`。

规则：

```tex
a or b:
    如果 a 为真，返回 a；否则返回 b。

a and b:
    如果 a 为假，返回 a；否则返回 b。

not a:
    先对 a 做真值测试，再返回相反的 bool 对象。
```

例子：

```python
print([] or "fallback")          # fallback
print(["issue"] and "abort")    # abort
print(not [])                    # True
print(not ["issue"])             # False
```

工程上的典型坑：

```python
DEFAULT_PATH = "report.txt"

def choose_bad(value):
    return value or DEFAULT_PATH


def choose_good(value):
    return DEFAULT_PATH if value is None else value
```

如果 `value == ""` 是用户显式提供的有效值，`choose_bad("")` 会误把它替换成默认路径。

因此：

```tex
value or default：
    适合“所有假值都等同于没提供”的场景。

default if value is None else value：
    适合“只有 None 表示没提供，空字符串、0、空列表仍有业务含义”的场景。
```

短路还意味着未求值的表达式不会有副作用：

```python
def mark(name, value):
    print("call", name)
    return value


print(mark("left", "") and mark("right", "unused"))
```

输出中不会出现 `call right`，因为左侧返回空字符串，`and` 已经能确定结果为左侧操作数。

工程习惯：

```tex
1. 用 and / or 写条件时，先问它返回的是 bool 还是操作数对象。
2. 如果返回值要写入结构化结果字段，必要时显式 bool(...)，让类型稳定。
3. 不要依赖短路表达式隐藏重要副作用；重要动作优先写成清楚的 if 语句。
4. 条件表达式未选中的分支不会求值，未选分支里的函数调用不会发生。
```

### 14.5 比较、身份、成员测试和比较链

本阶段把几类看似相近的判断拆开：

```tex
== / !=：
    相等性。问两个对象在值意义上是否相等。

is / is not：
    身份。问两个名字或表达式结果是否指向同一个对象。

in / not in：
    成员关系。问某对象是否作为成员出现在容器或可迭代对象中。

bool(x) 或 if x:
    真值测试。问对象在条件语境中为真还是为假。
```

例子：

```python
record_a = {"key": "menu.start", "text": ""}
record_b = {"key": "menu.start", "text": ""}
records = [record_a]

print(record_a == record_b)       # True：内容相等
print(record_a is record_b)       # False：不是同一个字典对象
print(record_b in records)        # True：成员测试能找到相等元素
print(record_b is records[0])     # False：身份不同
print(record_a["text"] == "")     # True：相等性
print(bool(record_a["text"]))     # False：真值测试
print(record_a["text"] == False)  # False：相等性，不是在问真假
```

成员测试的复盘边界：

```tex
教学重点：
    x in records 不是要求 x is 某个元素。

更精细的说法：
    序列成员测试按成员关系寻找匹配元素，通常以相等性为核心；
    实现可能对同一对象做快速路径。

复盘时要反对的是：
    把 in 误解成身份测试。
```

比较链不是简单文本替换：

```python
def probe(name, value):
    print("probe", name)
    return value


print(probe("low", 1) < probe("mid", 3) <= probe("high", 3))
```

比较链的关键：

```tex
1. 从左到右求值。
2. 中间表达式只求值一次。
3. 前段比较失败后，后续表达式不再求值。
4. a < b > c 表示 a < b 且 b > c，不是 a < b 且 b < c。
```

工程应用：

```tex
low <= score < high：
    适合数值区间判断。

min_len <= len(text) <= max_len：
    适合本地化文本长度规则。

if key in mapping：
    适合检查 key 是否存在。

if value is None：
    适合判断“没有提供”。

if value == ""：
    适合判断“明确提供了空字符串”。
```

禁忌：

```tex
1. 不要用 is 比较普通字符串、数字等业务值。
2. 不要把 x == False 当成真值测试；要么 if not x，要么精确比较业务值。
3. 不要把比较链当成 b 会求值两次的文本展开式。
```

### 14.6 `if` / `elif` / `else`、多个独立 `if`、缩进和 `pass`

互斥分支链：

```python
if missing:
    action = "abort missing"
elif empty:
    action = "abort empty"
elif dry_run:
    action = "preview"
else:
    action = "write"
```

规则：

```tex
同一个 if / elif / else 链最多执行一个代码块。
一旦某个分支命中，后续 elif 条件不会再求值。
```

多个独立 `if`：

```python
issues = []

if missing:
    issues.append("missing")

if empty:
    issues.append("empty")

if dry_run:
    issues.append("dry-run")
```

规则：

```tex
每个 if 都独立检查，可能有多个代码块执行。
```

工程选型：

```tex
选择唯一最终动作：
    if / elif / else。

收集所有命中问题：
    多个独立 if。
```

缩进决定代码块归属，不由“肉眼最近的 if”单独决定：

```python
if enabled:
    if has_errors:
        print("blocked")
    else:
        print("ready")
else:
    print("disabled")
```

这里第一个 `else` 属于内层 `if has_errors`，第二个 `else` 属于外层 `if enabled`。

空代码块必须有真实语句，注释不算语句：

```python
if enabled:
    # TODO: implement later
else:
    print("disabled")
```

这段代码在解析/编译阶段失败。严格说，在语法失败之前，`enabled = True` 也不会作为脚本语句真正执行，控制流也不会进入 `if`。

合法占位：

```python
if enabled:
    pass
else:
    print("disabled")
```

`pass` 是真正的 Python 语句，表示什么也不做。

### 14.7 条件表达式：二选一地产生值

Python 语法里的条件表达式是：

```python
value_if_true if condition else value_if_false
```

它是表达式，会产生一个值；`if` 语句是复合语句，用来选择执行哪个代码块。

适合用条件表达式的情况：

```python
mode = "preview" if dry_run else "write"
severity = "error" if strict and has_blocking_issue else "warning"
path = "audit.txt" if output_path is None else output_path
```

不适合使用条件表达式的情况：

```tex
1. 分支里有多步副作用。
2. 分支优先级需要多行说明。
3. 需要收集多个问题，而不是选择一个值。
4. 表达式写完后读者必须重新拆回 if / else 才看懂。
```

未选中的分支不会求值：

```python
def build(label, value):
    print("build", label)
    return value


issues = ["empty text"]
message = build("issues", issues) if issues else build("ok", [])
```

这里不会调用 `build("ok", [])`。

本阶段要长期保留的写法判断：

```tex
简单值选择：
    条件表达式可以提升紧凑性。

业务动作选择：
    if / elif / else 更清楚。

多问题收集：
    多个独立 if 更清楚。
```

### 14.8 本地化审计决策：把条件写成业务规则

本阶段的工程主线是本地化资源审计：根据严格模式、预览模式、缺失 key、空译文和输出路径，决定严重级别、模式、动作和报告路径。

一个清晰的最小设计：

```python
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
```

这段设计体现的规则：

```tex
1. output_path is None 才使用默认路径。
2. output_path == "" 时保留空字符串，不被 or 默认值误伤。
3. strict and missing_keys 优先级高于 strict and empty_text_keys。
4. dry_run 只影响预览/写入模式，不掩盖阻断问题。
5. has_blocking_issue 显式 bool(...)，让结构化返回字段类型稳定。
6. action 是唯一最终动作，因此使用 if / elif / else。
7. issues 字段负责保留所有问题，不把“收集问题”和“选择动作”混在一起。
```

这是 C12 进入工程实践后的关键提升：条件写法不只是“能跑”，还要表达业务优先级、返回类型稳定性和副作用边界。

### 14.9 `match` / `case`：结构化模式分派，不是万能替代 `if`

`match` 是结构化模式匹配语句，不是 C / Java 风格 `switch`。

本阶段应掌握的边界：

```tex
1. case 按顺序尝试。
2. 第一个匹配成功的 case 执行后，整个 match 结束。
3. Python match 不会自动 fall-through。
4. case _ 是通配模式，通常作为兜底。
5. mapping pattern 可以允许 subject 有额外键。
6. case {"key": key} 中右侧 key 通常是捕获绑定，不是比较已有变量。
```

例子：

```python
event = {"kind": "missing", "key": "menu.quit", "strict": True}

match event:
    case {"kind": "missing", "key": key, "strict": True}:
        result = f"abort:{key}"
    case {"kind": "empty_text", "key": key}:
        result = f"empty:{key}"
    case _:
        result = "ok"
```

`key` 是捕获绑定。如果要和已有变量比较，通常使用 guard 或常量模式设计。

工程选型：

```tex
适合 match：
    已经有结构化事件、命令、消息或 AST-like 数据，需要按形状分派。

不适合 match：
    只是几个布尔条件按优先级做业务决策。

本阶段决策函数内部：
    if / elif / else 更直接。

决策函数生成 event 后：
    match 可以用于结构化分派。
```

### 14.10 本阶段你的理解轨迹、问题与修正规则

本阶段整体表现很稳。你在每一步预测题中都能按“表达式求值 -> 对象 -> 真值测试 -> 短路/分支 -> 副作用”这条链解释。需要记录的是少数术语边界和一次重要追问。

1. 关于 `if x` 与 `x == True`：

   ```tex
   预计误区：if x: 等价于 if x == True:。
   修正：if x 是真值测试；x == True 是相等性比较。
   学习结果：已稳定掌握。
   ```

2. 关于容器内部元素真假：

   ```tex
   预计误区：列表里有假值元素，所以列表整体为假。
   修正：列表真值测试看容器是否为空，不递归检查内部所有元素。
   学习结果：能准确解释 [""] 为真、"" 为假。
   ```

3. 关于 `__bool__()` 与 `__len__()`：

   ```tex
   预计误区：__bool__ 出错后 Python 会尝试 __len__。
   修正：__len__ 只是没有 __bool__ 时的后备，不是异常恢复机制。
   测验精修：LocalizedEntries 的 __len__ 是本类直接定义；StrictLocalizedEntries 才继承它。
   ```

4. 关于真值测试是否“反复调用直到 bool”：

   ```tex
   你的追问：if True: 这种条件对象已经是 bool 时，真值测试到底发生什么？

   修正：表达式求值得到 True 后，条件语境判定它为真。
   不要理解成反复机械调用 __bool__ / __len__ 直到返回 bool。
   对自定义对象，协议入口只按优先级选择一次；__bool__ 返回非 bool 会 TypeError。
   ```

5. 关于 `and` / `or`：

   ```tex
   预计误区：and / or 统一返回 True 或 False。
   修正：它们根据真值测试决定路径，但返回操作数对象。
   学习结果：能准确解释 issue 和 should_abort 是 list，而不是 bool。
   ```

6. 关于默认值陷阱：

   ```tex
   预计误区：value or default 是通用默认值写法。
   修正：它会替换所有假值，包括 ""、0、[]、None。
   学习结果：能在 output_path == "" 场景中改用 is None 精确判断。
   ```

7. 关于成员测试：

   ```tex
   预计误区：x in records 要求 x 是列表里那个同一对象。
   修正：成员测试不是身份要求，通常以相等性匹配为核心。
   精修：后续可补入同一对象快速路径这一实现细节，但本阶段不依赖它。
   ```

8. 关于解析/编译期与运行期：

   ```tex
   测验精修点：非法空代码块在解析/编译阶段失败。
   修正：失败前没有任何赋值语句真正执行，也没有控制流进入 if。
   ```

9. 关于 `match`：

   ```tex
   预计误区：match 是支持 fall-through 的 switch。
   修正：match 是结构化模式匹配；命中一个 case 后整个 match 结束。
   学习结果：能准确解释 mapping pattern 捕获绑定和 case _ 通配兜底。
   ```

### 14.11 阶段测验暴露的薄弱处与修正规则

本阶段测验建议得分为 `100 / 100`，通过 `C12_if_Tests_and_Syntax_Rules` 小阶段。
没有发现影响程序结果、控制流归属、对象返回值或协议规则判断的实质错误。

不扣分但需要继续精修的三处术语：

```tex
精修点1：方法来源表述
原表述倾向：LocalizedEntries 调用继承来的 __len__。
修正：LocalizedEntries.__len__ 是本类直接定义；StrictLocalizedEntries 继承它但因 __bool__ 优先而不调用。

精修点2：解析期与运行期
原表述倾向：片段 2 中 enabled 绑定到 True 后会进入 if。
修正：片段 2 语法非法，解析/编译阶段失败；没有运行期赋值和控制流进入。

精修点3：成员测试细节
原表述：record_b in records 使用相等性，不是身份。
修正：对本阶段核心正确；更精细地说，成员测试不是身份要求，通常以相等性匹配为核心，具体实现可能对同一对象快速命中。
```

本次测验确认的强项：

```tex
1. 能稳定区分对象本体、真值测试结果和相等性比较。
2. 能解释容器真值测试不递归检查内部元素。
3. 能说明普通自定义对象默认真值，以及 __bool__ / __len__ 的优先级。
4. 能判断 __bool__ 返回非 bool、__len__ 返回负数等协议错误。
5. 能准确预测 and / or 的操作数返回和短路副作用。
6. 能说明 not 始终返回 bool。
7. 能区分 ==、is、in、bool(...) 问的是不同问题。
8. 能预测比较链的求值顺序和短路行为。
9. 能区分 if / elif / else 的互斥选择与多个独立 if 的问题收集。
10. 能说明缩进决定 else 归属，注释不能充当代码块，pass 是合法语句。
11. 能区分条件表达式产生值与 if 语句组织代码块。
12. 能在本地化审计决策中写出清晰的阻断优先级和默认路径规则。
13. 能说明 match 的结构化分派边界和无 fall-through 语义。
```

### 14.12 工程应知应会清单

```tex
1. if x 是真值测试，不是 x == True。
2. bool(x) 返回布尔结果，不等于 x 本身。
3. 空字符串、空容器、0、None 通常是假值。
4. 非空容器为真，不递归检查元素真假。
5. __bool__ 优先于 __len__。
6. __bool__ 必须返回 bool；返回其它对象会 TypeError。
7. __len__ 必须返回非负整数；0 假，正数真，负数错误。
8. 普通自定义对象没有 __bool__ / __len__ 时默认为真。
9. and / or 根据真值测试短路，但返回操作数对象。
10. not 永远返回 True 或 False。
11. 条件表达式和 if 语句都只求值实际需要的分支。
12. 未求值的表达式不会产生函数调用、副作用或异常。
13. value or default 会替换所有假值，不适合区分 None 与 ""。
14. 只想在 None 时默认，使用 default if value is None else value。
15. 结构化返回字段如果需要 bool，显式使用 bool(...)。
16. == 问相等性，is 问身份；普通业务值比较用 ==。
17. x in container 问成员关系，不要等同于身份测试。
18. if not x 问真假；x == False 问相等性。
19. 比较表达式返回 bool。
20. 比较链中间表达式只求值一次。
21. 比较链前段失败后，后续表达式不再求值。
22. if / elif / else 链最多执行一个代码块。
23. 多个独立 if 可能执行多个代码块。
24. 唯一动作选择用 if / elif / else。
25. 收集多个问题用多个独立 if。
26. 缩进决定代码块归属。
27. 注释不能充当代码块；pass 可以。
28. 语法非法时，脚本在解析/编译阶段失败，运行期语句不会执行。
29. 条件表达式适合简单值选择，不适合复杂副作用。
30. match 适合结构化数据分派，不是所有 if / elif 的替代品。
31. Python match 不自动 fall-through。
32. case {"key": key} 通常是捕获绑定，不是比较已有变量。
33. case _ 是通配兜底。
34. CLI 和审计工具中要分清：阻断问题、警告问题、dry-run、输出路径和报告副作用。
35. 条件写法优先服务业务语义和可维护性，不要为了短而牺牲可读性。
```

### 14.13 阶段精髓小结

```tex
1. C12 的核心不是会写 if，而是能解释条件控制流为什么走到某条路径。
2. 条件位置先求值表达式，得到对象；然后对象接受真值测试。
3. if x 与 x == True 是不同问题：真值测试 vs 相等性比较。
4. bool(x) 是真值结果，不是 x 本身。
5. 容器真值看空不空，不递归检查元素真假。
6. 自定义对象真值协议优先看 __bool__，再看 __len__，否则默认真。
7. __bool__ 返回类型不合法不会被 __len__ 补救。
8. __len__ 返回整数，由长度是否为 0 决定真假。
9. and / or 不保证返回 bool；它们返回被规则选中的操作数对象。
10. not 保证返回 bool。
11. 短路意味着未被求值的一侧没有调用、没有副作用、没有异常。
12. value or default 是便利写法，也是默认值陷阱。
13. ==、is、in、bool(...) 分别问相等性、身份、成员关系和真假。
14. 比较链不是文本替换；中间表达式只求值一次。
15. if / elif / else 用于互斥选择，多个独立 if 用于多项收集。
16. 缩进是语法结构，决定 else 归属；注释不能占据代码块。
17. 条件表达式产生值，if 语句组织代码块。
18. match 是结构化模式匹配，不是带 fall-through 的 switch。
19. 工程条件要表达优先级、返回类型和副作用边界。
20. C12 的价值，是把 C10 的语句模型和 C11 的赋值/副作用模型推进到“哪些代码会执行、哪些代码不会执行”。
```

进入 `C13_while_and_for_Loops` 后，要把这套条件控制流模型继续迁移到循环：每轮条件如何重新求值、循环体如何改变退出条件、`break` / `continue` 如何改变控制流、循环 `else` 何时执行，以及遍历过程中修改容器会带来什么风险。

## 15. C13 while 与 for 循环：重复执行、控制流跳转和安全遍历

`C13_while_and_for_Loops` 的真正目标不是“会写两个循环语法”，而是把 C12 的条件控制流模型推进到重复执行：

```tex
循环开始前：
    条件表达式或可迭代对象如何准备下一步。

每一轮：
    变量绑定到哪个对象；
    哪些赋值、原地修改、输出或追加副作用发生；
    continue 跳过了哪些语句；
    break 终止了哪一层循环。

循环结束后：
    是正常耗尽、条件变假，还是 break 提前终止；
    循环 else 是否执行；
    循环变量、队列、统计字段、报告对象最终处于什么状态。
```

本阶段延续本地化资源审计语境：逐条扫描资源、跳过禁用记录、收集普通问题、遇到阻断结构错误提前停止、生成结构稳定的 `report`。

### 15.0 阶段状态和可追溯入口

```tex
2026-07-01：正式进入 C13 while 与 for 循环。
2026-07-07：C13 阶段测验完成审批，建议得分 99 / 100，通过。
```

相关阶段文件：

```tex
docs/C13_WHILE_AND_FOR_LOOPS_STARTUP_TEMPLATE.md
practice/P3_Statements_and_Syntax/C13_while_and_for_Loops/
practice/P3_Statements_and_Syntax/C13_while_and_for_Loops/stage_quiz_while_and_for_loops.md
notes/Python_Learning_Profile.md
```

阶段脚本和样例数据：

```tex
01_while_condition_rechecks_and_exit_state.py
02_sentinel_loop_break_and_continue.py
03_loop_else_normal_vs_break.py
04_for_iterables_and_variable_binding.py
05_range_enumerate_zip_selection.py
06_mutating_while_iterating_risks.py
07_localization_resource_scan_loop_pipeline.py
08_prompt_manager_loop_reading_walkthrough.py
sample_c13_resource_lines.txt
```

### 15.1 阶段地图

本阶段按以下主线推进：

```tex
1. while 条件每轮重新求值。
2. 循环体如何改变退出条件，避免无限循环。
3. while True、哨兵值、break 和 continue。
4. 循环 else 的真实语义：没有 break 才执行。
5. for 遍历字符串、列表、字典、集合、文件和 zip 等对象。
6. 循环变量绑定：重新绑定名字，不复制元素对象。
7. range()、enumerate()、zip() 和 zip(strict=True) 的选型。
8. 文件对象、zip 对象和迭代器式对象的一次性消费。
9. 遍历中修改列表、字典、集合的风险。
10. 用快照、收集后处理、构造新容器来安全处理数据。
11. 嵌套循环和占位符检查。
12. 本地化资源扫描 report：stats、issues、fatal_error、valid_records。
```

阶段验收观察点：

```tex
1. 能预测循环次数、输出顺序和最终变量绑定。
2. 能说明 while 条件每轮检查的是当前对象状态。
3. 能判断 break / continue / loop else 的路径差异。
4. 能区分循环变量重新绑定和可变元素原地修改。
5. 能识别边遍历边修改容器的风险，并给出安全替代写法。
6. 能把循环控制流组织成结构化扫描函数，而不是只用 print 输出过程。
```

### 15.2 `while`：条件每轮重新求值，不是只检查一次

`while condition:` 的核心不是“进入一次后自动循环”，而是：每一轮开始前都重新求值 `condition`，并对结果做真值测试。

```python
queue = ["scan", "normalize", "report"]

while queue:
    command = queue.pop(0)
    print(command, queue)
```

这里 `while queue:` 每轮检查的是当前 `queue` 列表对象的真值：非空为真，空列表为假。`queue.pop(0)` 会原地修改列表，影响下一轮条件是否仍然为真。

常见误区：

```tex
误区1：while 条件只在第一次进入循环前检查一次。
修正：while 条件每轮都会重新求值。

误区2：循环次数由某个看起来像计数器的变量天然决定。
修正：循环次数由循环条件和循环体中的状态变化共同决定。

误区3：while queue: 绑定的是初始列表长度。
修正：它每轮看的是当前 queue 是否为空；pop、append、clear 都会影响后续判断。
```

工程规则：

```tex
1. while 适合动态状态、队列、轮询、哨兵输入、重试逻辑。
2. 写 while 时必须能指出哪个状态变化保证退出。
3. 如果 continue 会跳过状态推进语句，优先重构，避免无限循环。
4. 对本地化扫描队列，while queue: 表示“还有任务未处理”，不是固定轮数循环。
```

### 15.3 `while True`、哨兵值、`break` 和 `continue`

`while True` 常用于“先读一条，再根据内容决定是否停止”的哨兵模式：

```python
commands = ["scan", "", "normalize", "QUIT", "report"]
index = 0
processed = []
empty = 0

while index < len(commands):
    command = commands[index]
    index += 1

    if command == "QUIT":
        break

    if not command:
        empty += 1
        continue

    processed.append(command)
```

控制流含义：

```tex
break：
    立即结束当前这一层循环。
    循环后面的语句继续执行。

continue：
    只结束当前这一轮循环体的剩余部分。
    while 中回到条件重新判断；for 中进入下一次取值。

普通执行到底：
    本轮循环体剩余语句全部执行，然后自然进入下一轮。
```

常见坑：

```tex
1. 把 continue 误解成结束整个循环。
2. 在 continue 前忘记推进 index，导致 while 无限循环。
3. 忘记 break 不会撤销本轮已经发生的副作用。
4. 统计字段放在不同位置，会改变统计口径。
```

统计口径规则：

```tex
统计读取过多少条：
    计数放在读出 command 后、任何过滤和 break 之前。

统计非空普通命令：
    计数放在空字符串过滤和 QUIT 哨兵判断之后。

统计成功处理过多少条：
    计数放在真正处理成功之后。
```

测验暴露的精修点：

```tex
不能只说“total 的含义取决于位置”。
更好的说法是：
    移到 if not command: ... continue 之后，并且仍在 QUIT 分支之后，
    本例 total 会只统计 scan 和 normalize，即 2。
```

### 15.4 循环 `else`：没有 `break` 才执行

循环 `else` 不是 `if` 的 `else`，也不是“条件为假就执行”的普通反面分支。它的语义是：循环没有被 `break` 提前终止时执行。

```python
target = "menu.quit"
records = ["menu.start", "menu.options"]

for key in records:
    if key == target:
        print("found", key)
        break
else:
    print("not found")
```

这里没有找到目标，循环自然耗尽，因此执行 `else`。

要点：

```tex
1. for 正常耗尽 -> else 执行。
2. while 条件变假正常结束 -> else 执行。
3. break 提前终止 -> else 不执行。
4. continue 不会阻止 else；它只跳过当前这一轮剩余语句。
5. 空循环如果没有 break，也会执行 else。
```

工程应用：

```tex
搜索一个目标：
    找到后 break；else 表示没找到。

扫描所有记录：
    没有 fatal break 时，else 可表示扫描完整完成。

结构化报告：
    completed 表示是否完整扫描，不等于 issues 是否为空。
```

你在阶段中形成的关键判断：

```tex
“找到目标”这类语义不应该无条件放在循环之后。
更稳妥的写法：
    找到时在 break 前处理，或者保存 found_record，再在循环后统一处理。
    未找到时用 loop else 明确表达。
```

### 15.5 `for`：遍历元素对象，循环变量每轮重新绑定

`for item in items:` 的本质不是“复制元素给 item”，而是每轮从可迭代对象中取得下一个元素对象，并把循环变量 `item` 绑定到它。

```python
records = [
    {"key": "menu.start", "target": "Start"},
    {"key": "menu.exit", "target": ""},
]

for record in records:
    if record["target"]:
        record["target"] = record["target"].upper()
```

如果元素是可变对象，`record` 和列表里的元素引用同一个字典。通过 `record["target"] = ...` 修改的是那个字典对象本身，`records` 中也会体现变化。

边界规则：

```tex
record = {...}：
    重新绑定循环变量，不会替换 records 中的元素。

record["target"] = "START"：
    通过循环变量修改当前字典对象，会影响 records 中对应元素。

valid.append(record)：
    追加当前对象引用，不是复制字典。

valid.append({"key": record["key"], "target": target})：
    构造新的外层字典，避免共享原始 record。
```

常见误区：

```tex
误区1：for item in items 会复制元素对象。
修正：循环变量绑定到元素对象，是否共享要看元素本身是不是同一个可变对象。

误区2：循环结束后的 record 一定代表“找到的目标”。
修正：它通常只是最后一次绑定；循环零次执行时甚至可能没有新绑定。

误区3：append(record) 得到的是一份独立报告。
修正：append 的是对象引用；需要独立报告时构造新 dict。
```

工程习惯：

```tex
1. 审计工具中优先构造干净 report 条目，不直接暴露输入 record。
2. 如果要保留原始行号，把 line_no 放入 valid_records 或 issues。
3. 如果报告条目包含嵌套可变对象，外层新字典不等于深拷贝；要按字段语义显式复制。
```

### 15.6 `range()`、`enumerate()`、`zip()`：按意图选择循环工具

三者不是“循环高级写法”，而是表达不同意图的工具。

```tex
直接遍历元素：
    for record in records:
    适合只关心元素对象。

range(...):
    for index in range(len(records)):
    适合确实需要数字序列或手工下标控制。

enumerate(...):
    for line_no, line in enumerate(lines, start=1):
    适合同时需要元素和位置。

zip(...):
    for key, target in zip(keys, targets):
    适合并行遍历多个输入。

zip(..., strict=True):
    适合要求多个输入强对齐，长度不一致应视为错误。
```

本地化场景中的典型选择：

```python
for line_no, raw_line in enumerate(lines, start=1):
    line = raw_line.rstrip("\n")
    key, target = line.split("=", 1)
```

为什么用 `enumerate(start=1)`：

```tex
1. 报告给人看时通常从第 1 行开始计数。
2. issues 中保存 line_no，能定位原始文件位置。
3. 比手工维护 index 更少出错。
```

为什么用 `split("=", 1)`：

```tex
只按第一个等号拆分。
如果翻译文本中也出现 =，不会把 target 拆碎。
```

为什么用 `rstrip("\n")` 而不是无脑 `strip()`：

```tex
rstrip("\n")：
    去掉行尾换行符，保留 key 或 target 中真实存在的空格。

strip()：
    去掉两端所有空白，可能掩盖本应审计的空格问题。
```

`zip()` 的关键坑：

```tex
普通 zip：
    在最短输入耗尽时停止，较长输入尾部被静默丢弃。

zip(strict=True)：
    长度不一致时抛出 ValueError，能暴露对齐错误。

但 strict=True 不是事务机制：
    异常发生前，循环体里已经执行过的 append、print、写文件等副作用不会自动回滚。
```

工程规则：

```tex
1. 只要元素：直接 for item in items。
2. 要行号或位置：enumerate()。
3. 要并行匹配：zip()。
4. 资源列必须一一对应：zip(strict=True)。
5. 不要滥用 range(len(seq))；除非确实需要下标或要修改槽位。
```

### 15.7 文件对象、流式迭代和 `a+` 模式边界

文件对象可以被 `for line in file:` 遍历，它像流一样维护当前位置。

```python
from io import StringIO

stream = StringIO("a=1\nb=2\n")

first = [line.rstrip("\n") for line in stream]
second = [line.rstrip("\n") for line in stream]
stream.seek(0)
third = [line.rstrip("\n") for line in stream]
```

结果语义：

```tex
first：
    读到 a=1 和 b=2。

second：
    空列表，因为第一次遍历后位置已经在 EOF。

third：
    seek(0) 回到开头后，重新读到内容。
```

文件对象和 `zip` 类似，常见边界是“一次性消费”：同一个对象遍历一次后，再遍历可能没有内容。要重复使用，需要重新打开文件、`seek(0)`，或把内容显式保存成列表。

不建议边读边写同一个文件：

```tex
1. 读写共享文件位置，容易漏读或重复读。
2. 缓冲区刷新时机可能让刚写入内容不可见。
3. 追加写可能导致文件不断增长，扫描边界不清楚。
4. 出错时很难判断哪些内容已经读过、哪些内容已经写入。
```

`a+` 模式的合理用途：

```tex
`a+` 表示打开文件用于读写，并且写入通常追加到文件末尾。
它适合“打开一个日志或记录文件，必要时读取已有内容，然后追加新记录”。

典型场景：
    读取已有审计日志末尾状态；
    追加本次运行摘要；
    保存简单的本地追踪记录。

注意：
    打开后文件位置通常在末尾。
    如果要读已有内容，通常需要 seek(0)。
    即使能读写同一文件，也不等于适合在同一个迭代循环里边读边写。
```

工程习惯：

```tex
1. 审计工具优先分阶段：先读输入 -> 生成 report -> 再写输出。
2. 输入文件和输出报告文件尽量分开。
3. 对同一个文件既读又写时，显式管理 seek、flush、关闭和失败路径。
4. 需要稳定可复盘时，把原始输入、结构化 report、最终输出分层保存。
```

### 15.8 遍历时修改容器：列表、字典、集合的风险不同

边遍历边修改容器，是 C13 最重要的工程坑之一。

列表的风险：

```python
items = ["", "scan", "", "report"]

for item in items:
    if not item:
        items.remove(item)
```

列表迭代通常按位置推进；删除当前或前面的元素会让后续元素左移，容易跳过元素。它未必立刻报错，但逻辑可能已经错了。

字典和集合的风险：

```python
records = {"menu.start": "开始", "menu.exit": ""}

for key, target in records.items():
    if not target:
        del records[key]
```

遍历字典或集合时改变大小，通常会触发运行期错误，例如：

```tex
RuntimeError: dictionary changed size during iteration
RuntimeError: set changed size during iteration
```

但要注意：

```tex
运行期错误不等于事务回滚。
异常发生前，已经删除或添加的内容可能已经改变了原对象。
```

测验精修点：

```tex
E2 中如果捕获异常后查看 records，可能看到：
    "menu.exit" 已经被删除，
    "menu.debug" 还留着。

所以“会报错”还不够，工程上还要问：
    报错前对象是否已经部分改变？
```

安全替代写法：

```tex
快照遍历：
    for key in list(records):
        ...

先收集后处理：
    keys_to_delete = []
    for key, target in records.items():
        if not target:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del records[key]

构造新容器：
    cleaned = {}
    for key, target in records.items():
        if target:
            cleaned[key] = target
```

工程选型：

```tex
需要保留原输入用于审计：
    构造新容器。

确实要修改原对象：
    先收集要改的 key 或 index，再统一处理。

只是遍历一个静态视图：
    可以使用 list(records.items()) 快照。
```

### 15.9 字典和集合：顺序、哈希、成员测试和稳定报告

字典和集合都基于哈希结构支持高效成员查找，但它们的业务语义不同。

字典：

```tex
dict 保存 key -> value 映射。
现代 Python 字典保留插入顺序。
查找某个 key 平均很快。
```

集合：

```tex
set 保存唯一元素。
它不仅用于去重，还用于快速成员测试和集合运算：差集、交集、并集、对称差集。
普通 set 不承诺业务顺序。
```

你在阶段中追问过的问题，可以压缩为这三条：

```tex
1. 字典如何同时保留插入顺序和高效 key 查找？
   现代 CPython 的字典实现把哈希表查找和紧凑保存条目的布局结合起来；语言层面从 Python 3.7 起承诺 dict 保留插入顺序。

2. 集合为什么也是哈希结构？只是为了去重吗？
   不是。去重是结果之一；更重要的是快速成员测试和集合运算。

3. dict[key] 和 key in dict / item in set 是否是同类机制？
   它们都依赖对象的哈希值和相等性协议定位候选元素；目的不同：dict[key] 是取值，key in dict / item in set 是成员测试。
```

成员测试边界：

```python
record = {"key": "menu.start", "target": "开始"}
known_keys = {"menu.start", "menu.exit"}

"key" in record              # 检查字典 key
"menu.start" in record       # 仍然检查 key，不检查 value
"menu.start" in known_keys   # 检查集合元素
record["key"] in known_keys  # 先取 value，再做集合成员测试
```

稳定报告规则：

```tex
带 line_no 的问题报告：
    优先保留原始文件顺序。

纯 key 集合报告：
    优先 sorted(...)，保证稳定、可读、可复现。

dict 扫描报告：
    可利用插入顺序表达资源声明顺序。

set 直接打印：
    不适合作为稳定报告格式。
```

### 15.10 本地化扫描函数：把循环组织成结构化 report

本阶段最终把循环知识落在资源扫描函数上。推荐报告结构：

```python
report = {
    "completed": True,
    "stats": {
        "total": 0,
        "disabled": 0,
        "enabled": 0,
        "valid": 0,
    },
    "issues": [],
    "fatal_error": None,
    "valid_records": [],
}
```

典型控制流：

```tex
for line_no, record in enumerate(records, start=1):
    total += 1

    缺 key：
        结构性问题，设置 fatal_error，completed = False，break。

    enabled 为 False：
        计入 disabled，continue。

    target 为空：
        内容质量问题，加入 issues，continue。

    占位符缺失：
        内容一致性问题，加入 issues，continue。

    通过检查：
        valid += 1，构造新字典加入 valid_records。
```

你在阶段中总结得很准确的两个判断：

```tex
缺 key：
    结构性问题，后续扫描前提被破坏；使用 fatal_error + break。

译文为空或占位符缺失：
    内容质量问题，不破坏继续扫描其它资源的能力；使用 issues.append(...) + continue。
```

`break` 后统一 `return report` 的价值：

```tex
break：
    停止扫描循环。

循环后的统一收尾：
    补齐 issue_count、summary、completed 等结构字段。

统一 return：
    让调用者拿到稳定结构。
```

循环中直接 `return report` 也不是绝对错误，但更适合短小搜索函数或无需统一收尾的函数。对审计报告函数，优先使用 `break` 后统一收尾。

工程规则：

```tex
1. 核心扫描函数不要直接 print；返回 report。
2. 人读输出、JSON 导出、日志写入放在外层展示层。
3. 用 continue 降低嵌套，但不要让 continue 跳过必要统计。
4. 用 break 表达 fatal 停止扫描，再统一整理 report。
5. valid_records 构造新字典，避免共享原始 record。
6. line_no 是定位信息，普通 issue、fatal_error、必要时 valid_records 都可以保留。
```

### 15.11 本阶段你的理解轨迹、问题与修正规则

1. 关于 `while queue:` 的循环次数：

   ```tex
   你的判断：
       循环次数由 queue 指向的列表在每轮中的当前长度和变化决定，
       不是由 round_no 这类计数变量决定。

   结论：
       正确。
       round_no 只是统计轮数；真正驱动循环继续的是 queue 的真值。
   ```

2. 关于 `QUIT` 之后的命令：

   ```tex
   你的判断：
       读取到 QUIT 后，index 已经前进，但 break 会终止循环，
       所以 QUIT 后面的 report 不会处理。

   结论：
       正确。
       这说明你已经能把“本轮已发生的副作用”和“后续控制流停止”分开。
   ```

3. 关于 `continue` 的路径：

   ```tex
   你的判断：
       disabled 记录命中 continue 后，不会继续检查 target。

   结论：
       正确。
       continue 是本轮剩余语句的跳过，不是整个循环的终止。
   ```

4. 关于“找到目标”的语句位置：

   ```tex
   你的理解：
       “找到目标”这类语义不应无条件写在循环之后。
       它应放在 break 前，或结合 loop else 表达“未找到”。

   结论：
       正确。
       循环之后只能说明循环结束，不能自动说明找到目标。
   ```

5. 关于 fatal 与 ordinary issue：

   ```tex
   你的理解：
       缺 key 是结构性问题，使用 fatal_error + break。
       译文为空是内容质量问题，使用 issues.append(...) + continue。

   结论：
       正确。
       这正是扫描工具中“能否继续扫描”的关键分界。
   ```

6. 关于 break 后统一 return：

   ```tex
   你的理解：
       break 只结束循环，函数仍可执行统一收尾逻辑；
       循环中直接 return 会绕过后续收尾，可能让返回结构不稳定。

   结论：
       正确。
       对结构化报告函数尤其重要。
   ```

7. 关于可变序列和哈希结构在遍历中修改的差异：

   ```tex
   你的追问：
       为什么列表和 dict/set 自身长度变化时表现差异明显？

   修正模型：
       列表迭代主要面对索引位置变化，可能跳过或重复处理元素；
       dict/set 迭代依赖哈希表结构，改变大小会破坏迭代器对结构版本的假设，通常直接 RuntimeError。

   工程结论：
       不要在遍历原容器时改变其结构；使用快照、收集后处理或构造新容器。
   ```

8. 关于文件对象边读边写和 `a+`：

   ```tex
   你的追问：
       如果文件对象被迭代时边读边写会怎样？既然不建议，a+ 有什么用？

   修正模型：
       文件迭代依赖当前位置和缓冲；边读边写同一个文件会让 EOF、flush、追加位置和可见性混在一起。
       a+ 的价值是读写同一个文件句柄，尤其适合读已有内容后追加新记录；
       但它不意味着推荐在同一个 for line in file 循环里边读边写。
   ```

9. 关于字典、集合和哈希：

   ```tex
   你的追问：
       dict 如何保序又高效查找？set 为什么基于哈希？dict[key] 到底发生什么？

   修正模型：
       dict 的语言语义承诺插入顺序，同时底层利用哈希结构做 key 查找；
       set 的价值不只去重，还包括快速成员测试和集合运算；
       dict key 查找与 set 成员测试都依赖 hash 与 equality 的协作。
   ```

10. 关于报告顺序：

    ```tex
    你的理解：
        带行号的问题报告，优先保留原始文件顺序；
        纯 key 集合报告，优先 sorted() 保证稳定、可读、可复现。

    结论：
        正确。
        这是本地化审计报告中非常重要的可复盘规则。
    ```

### 15.11.1 收束追问补充：占位语句、哨兵循环和旧式 `map(None)`

本节记录 C13 阶段笔记完成后继续追问的两个专题。它们都属于 C13 的收束补充：一个补上“语句 / 表达式 / 值”的边界，另一个补上旧书写法如何迁移到现代 Python 的迭代工具。

#### 15.11.1.1 `pass`、`...` 和 `None`：不要把三者混成“空”

三者看起来都可能和“什么也不做”有关，但层级完全不同：

```tex
pass：
    语句。
    用在语法要求必须有语句的位置，明确表示这里什么也不做。

...：
    表达式。
    求值得到内置单例对象 Ellipsis。

None：
    值。
    表示没有值、缺失值、无返回结果或不适用。
```

典型用法：

```python
def placeholder_function():
    pass


class FutureProtocol:
    ...


def maybe_get_target(record):
    if "target" not in record:
        return None
    return record["target"]
```

关键边界：

```tex
pass 不产生值，也不改变控制流。
    在循环中命中 pass 后，本轮后续语句仍会继续执行。
    想跳过本轮剩余语句，应使用 continue。

... 能放进函数体，是因为表达式语句本身合法。
    def f(): ... 没有显式 return，函数调用结果仍然是 None。
    ... is Ellipsis 为 True，bool(...) 也为 True。

None 是业务语义上的“没有值”。
    判断 None 应使用 is None / is not None。
    如果 None 可能是合法业务值，就不要把 None 当作哨兵。
```

工程习惯：

```tex
空分支、空循环体、空函数体：
    用 pass。

类型桩、协议、重载声明、教学骨架：
    可以用 ...。

运行时不应被调用的未实现逻辑：
    优先 raise NotImplementedError。

表示缺失、未找到、没有返回结果：
    用 None，并用 is None 判断。

None 也是合法数据时：
    使用唯一哨兵，例如 MISSING = object()。
```

#### 15.11.1.2 质数示例中的循环 `else`

书中质数片段适合展示循环 `else`：找到因子时 `break`，没有 `break` 才进入 `else`。但作为工程函数，它不应只依赖注释中的 `y > 1` 前提，也不应只用 `print` 表达结果。

更适合当前阶段的写法是保留 `while ... else`，但把结果返回为结构化数据：

```python
def prime_report(n):
    report = {
        "input": n,
        "is_prime": False,
        "factor": None,
        "reason": "",
        "checked_divisors": [],
    }

    if isinstance(n, bool) or not isinstance(n, int):
        report["reason"] = "not an integer"
        return report

    if n < 2:
        report["reason"] = "less than 2"
        return report

    if n == 2:
        report["is_prime"] = True
        report["reason"] = "2 is the smallest prime"
        return report

    if n % 2 == 0:
        report["factor"] = 2
        report["reason"] = "even number greater than 2"
        return report

    divisor = 3
    while divisor * divisor <= n:
        report["checked_divisors"].append(divisor)

        if n % divisor == 0:
            report["factor"] = divisor
            report["reason"] = "has a factor"
            break

        divisor += 2
    else:
        report["is_prime"] = True
        report["reason"] = "no factor found up to square root"

    return report


def is_prime(n):
    return prime_report(n)["is_prime"]
```

这段函数的重点不是数学技巧本身，而是 C13 控制流边界：

```tex
1. bool 是 int 的子类，工程上通常要显式排除 True / False。
2. n < 2 不是质数，不能靠注释保证调用方永远传入 y > 1。
3. 检查到平方根即可，用 divisor * divisor <= n 避免浮点 sqrt 边界。
4. while 的 else 表示“没有 break”，不是“循环至少执行过一次”。
5. n = 3、5、7 时循环体一次也不执行，但没有 break，所以 else 仍会执行。
6. 核心函数返回数据；print 属于外层展示边界。
```

#### 15.11.1.3 C 式“取值并判断”循环在 Python 中的现代写法

C 中常见模式：

```c
while ((x = next()) != NULL) {
    process(x);
}
```

在 Python 中，普通赋值语句 `x = ...` 不能出现在表达式位置。但现代 Python 有赋值表达式 `:=`，并且很多场景更应该直接使用 `for` 或迭代工具。

书中给出的三种旧式等价写法里，更推荐第一种的显式哨兵版本：

```python
while True:
    x = get_next()
    if x is None:
        break
    process(x)
```

不推荐把判断写成 `if not x: break`，除非接口契约明确规定任何假值都代表结束。否则 `0`、`""`、`[]`、`False` 这些合法数据都会被误判为结束。

三种写法的取舍：

```tex
while True + break：
    取值、判断停止、处理数据的顺序最清楚。
    推荐使用显式哨兵判断，例如 is None 或 is MISSING。

x = True; while x: ...：
    不推荐。
    初始 True 是人为占位值，同一个条件常被测两次，可读性较差。

预读一次，再在循环尾部再读一次：
    简单场景可用，但取值语句重复。
    如果循环体中出现 continue，尾部取值可能被跳过，容易造成死循环或重复处理旧值。
```

现代 Python 的优先级通常是：

```tex
1. 数据源本身可迭代：
       for x in obj:
           process(x)

2. 重复调用函数直到返回哨兵：
       for line in iter(file.readline, ""):
           process(line)

3. 需要在 while 条件里取值并判断：
       while (x := get_next()) is not None:
           process(x)

4. None 可能是合法业务值：
       MISSING = object()
       while (x := next(iterator, MISSING)) is not MISSING:
           process(x)

5. 普通迭代器耗尽：
       优先 for；不要手动把 StopIteration 当普通业务分支处理。
```

#### 15.11.1.4 旧式 `map(None, ...)` 与现代 `zip` / `zip_longest`

旧版 Python 曾支持 `map(None, ...)` 的退化形式。Python 3 不再支持：`None` 会被当作函数调用，消费结果时触发 `TypeError`。

```python
list(map(None, [1, 2]))
# TypeError: 'NoneType' object is not callable
```

现代替代规则：

```python
from itertools import zip_longest

list(zip([1, 2], ["a"]))
# [(1, "a")]

list(zip_longest([1, 2], ["a"], fillvalue=None))
# [(1, "a"), (2, None)]
```

如果要模拟旧式行为，可以写成：

```python
from itertools import zip_longest


def legacy_map_none(*iterables):
    if not iterables:
        raise TypeError("legacy_map_none() requires at least one iterable")

    if len(iterables) == 1:
        return list(iterables[0])

    return list(zip_longest(*iterables, fillvalue=None))
```

更现代的工程表达通常不复刻旧接口，而是直接写出真实意图：

```tex
zip(a, b)：
    截断到最短输入。

zip(a, b, strict=True)：
    要求长度一致，不一致就抛出 ValueError。

zip_longest(a, b, fillvalue=None)：
    补齐到最长输入，缺项用 None 表示。

list(a)：
    单个 iterable 的急切列表化。
```

本地化资源扫描中的选型：

```tex
key 列表和 target 列表必须一一对应：
    使用 zip(..., strict=True)。

允许缺项，但要把缺项报告出来：
    使用 zip_longest(..., fillvalue=MISSING)，其中 MISSING = object()。

只是为了复刻旧书语法：
    不推荐。现代代码应优先表达截断、强对齐或补齐这三种明确语义。
```

### 15.12 阶段测验暴露的薄弱处与修正规则

C13 阶段测验建议得分为 `99 / 100`，通过本阶段。主干没有概念性错误；扣分集中在两个工程精度点。

```tex
精修点1：统计字段的位置和口径

原答卷倾向：
    total 的含义取决于 report["total"] += 1 放在哪里。

修正：
    方向正确，但阶段末要进一步给出具体值和口径。
    本题中如果 total += 1 放到空字符串过滤之后，并且仍在 QUIT 分支之后，
    total 会只统计 scan 和 normalize，即 2。

长期规则：
    total、enabled、valid、processed 这类名字要和代码位置一致。
```

```tex
精修点2：运行期错误不等于事务回滚

原答卷倾向：
    遍历 dict 时删除 key 会 RuntimeError，print 不会执行。

修正：
    正确，但还要补充：异常发生前的删除可能已经生效。
    本题中 menu.exit 可能已经被删除，menu.debug 仍留在字典中。

长期规则：
    看到“异常”时继续问：异常前哪些副作用已经发生？是否需要回滚或避免半成品状态？
```

本次测验确认的强项：

```tex
1. 能稳定预测 while 动态队列、break、continue、loop else。
2. 能准确分析循环后变量、队列、seen 集合、processed 列表和 skipped 计数。
3. 能解释 enumerate 行号、rstrip("\n")、split("=", 1) 的工程意义。
4. 能说明 zip(strict=True) 暴露错误但不回滚前面副作用。
5. 能解释 file / StringIO 的位置推进和一次性消费。
6. 能识别循环变量绑定、原地修改、append 原对象引用和构造新容器的差异。
7. 能说明 missing 列表应放在外层循环内部，避免跨记录污染。
8. 能分析 dict/set 顺序、成员测试、hash/equality 协作和稳定报告排序。
9. 能设计结构稳定、无核心 print 副作用的本地化资源扫描函数。
```

### 15.13 工程应知应会清单

```tex
1. while 条件每轮重新求值。
2. while 循环必须能指出退出条件如何变化。
3. while queue: 检查当前 queue 是否非空，不绑定初始长度。
4. while True 通常要配合哨兵、break 或明确退出条件。
5. break 结束当前这一层循环。
6. continue 只跳过当前这一轮剩余语句。
7. break 不撤销本轮已经发生的副作用。
8. continue 前后统计字段的位置决定统计口径。
9. 循环 else 只在没有 break 时执行。
10. continue 不会阻止循环 else。
11. 搜索目标时，found 语义应由 break/else、found_record 或 return 明确表达。
12. for 循环变量每轮重新绑定到元素对象，不复制元素。
13. 重新绑定循环变量不会替换容器槽位。
14. 通过循环变量原地修改可变元素，会影响容器中的同一对象。
15. append(record) 保存对象引用，不是复制 record。
16. 生成报告时优先构造新字典，避免共享原始输入对象。
17. 新外层字典不等于深拷贝嵌套可变对象。
18. 只需要元素时直接遍历。
19. 需要行号或位置时使用 enumerate()。
20. 需要并行遍历时使用 zip()。
21. 要求强对齐时使用 zip(strict=True)。
22. 普通 zip 默认静默截断较长输入。
23. zip(strict=True) 不是事务机制。
24. 文件对象遍历会推进文件位置。
25. 文件对象、zip 对象、迭代器式对象通常会被一次性消费。
26. 重读同一文件对象通常需要 seek(0) 或重新打开。
27. 不建议在同一个文件迭代循环里边读边写。
28. a+ 适合读已有内容后追加新记录，但仍要显式管理文件位置。
29. 遍历列表时删除或插入元素可能跳过或重复处理。
30. 遍历 dict/set 时改变大小通常会 RuntimeError。
31. RuntimeError 不等于自动回滚；异常前可能已有部分副作用。
32. 安全修改容器：快照、先收集后处理、构造新容器。
33. dict 默认遍历 key。
34. dict 保留插入顺序，适合保留资源声明顺序。
35. set 不适合表达业务顺序。
36. 纯 key 集合报告优先 sorted(...)。
37. 带 line_no 的问题报告优先保留原始顺序。
38. key in dict 是检查 key，不是检查 value。
39. dict[key] 是取值；key in dict 是存在性测试。
40. set 的价值包括去重、快速成员测试和集合运算。
41. 哈希结构查找依赖 hash 与 equality 协作。
42. 扫描函数核心逻辑返回结构化 report，不直接 print。
43. 人读输出、日志、JSON/CSV 导出属于外层展示或持久化边界。
44. fatal error 用 completed=False + fatal_error + break。
45. ordinary issue 用 issues.append(...) + continue。
46. disabled 记录先计入 disabled，再 continue 跳过质量检查。
47. valid_records 应保存干净输出字段，必要时保留 line_no。
48. 统计字段命名要表达口径：读取过、启用过、有效过、处理过。
49. 嵌套循环中内层 break 只结束内层循环。
50. 缺 key、空 target、占位符缺失应区分结构问题和内容问题。
51. pass 是语句；... 是表达式，值是 Ellipsis；None 是普通对象和值。
52. pass 不会跳过本轮后续语句；需要跳过本轮应使用 continue。
53. def f(): ... 的函数调用结果仍然是 None，除非显式 return。
54. None 判断用 is None；None 可能是合法业务值时使用自定义哨兵。
55. 循环 else 的“没有 break”语义同样适用于循环体一次也没执行的情况。
56. C 式取值并判断循环在现代 Python 中优先考虑 for、iter(callable, sentinel) 或 :=。
57. 避免用 if not x 作为结束判断，除非所有假值都确实代表结束。
58. 预读一次再在循环尾读下一项的写法，要警惕 continue 跳过尾部取值。
59. Python 3 不支持 map(None, ...)，应根据意图选择 zip、zip(strict=True) 或 zip_longest。
60. zip_longest 补齐缺项时，若 None 是合法业务值，应使用 MISSING = object()。
```

### 15.14 阶段精髓小结

```tex
1. C13 的核心不是写 while 和 for，而是解释重复执行如何推进状态。
2. while 每轮重新求值条件；循环体改变的状态决定后续轮次。
3. for 从可迭代对象中取元素对象，并把循环变量绑定到它。
4. 循环变量绑定不是复制；可变元素原地修改会影响原容器。
5. break 终止当前循环；continue 跳过当前这一轮剩余语句。
6. 循环 else 的语义是“没有 break”。
7. 循环后的变量不自动代表“找到的目标”。
8. range、enumerate、zip 是表达循环意图的工具，不是越复杂越好。
9. zip 默认静默截断；strict=True 能暴露长度不一致。
10. 文件对象和迭代器式对象常常只能被消费一次。
11. 遍历中修改容器是高风险操作：列表可能漏检，dict/set 可能报错。
12. 报错之前的副作用可能已经发生，异常不是回滚机制。
13. 安全处理数据优先用快照、收集后处理或构造新容器。
14. dict 保序和 set 无业务顺序要分开看。
15. 哈希结构不只用于去重，也用于快速成员测试和集合运算。
16. 本地化扫描中，缺 key 是结构性 fatal；空译文和占位符缺失是普通 issue。
17. report 的 completed、stats、issues、fatal_error、valid_records 要表达不同层次的结果。
18. 核心扫描函数返回结构化数据；print、日志、文件写入放到外层。
19. 统计字段的位置就是统计口径，必须和字段命名一致。
20. C13 的价值，是把 C12 的“是否进入某个代码块”推进到“多轮执行如何改变对象、控制流和报告结构”。
```

进入 `C14_Iterations_and_Comprehensions` 后，要把 C13 已经压稳的显式循环模型继续推进到迭代协议、迭代器对象、推导式、生成器表达式、惰性求值和急切求值边界。下一阶段的重点不是把所有循环写短，而是判断哪些循环可以清晰地改写为推导式，哪些循环因为统计、错误处理、副作用或结构化报告需要继续保留显式写法。
