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
    C14_Iterations_and_Comprehensions
当前小阶段：
    C15_The_Documentation_Interlude（P3 的 PART closer）
阶段小测：
    C10：96 / 100，通过
    C11：100 / 100，通过
    C12：100 / 100，通过
    C13：99 / 100，通过
    C14：99 / 100，通过
    C15：98 / 100，通过
当前收束状态：C15 前置准备、正式主线、阶段测验逐题审批、学习画像同步和阶段末笔记均已完成；P3 长期记录职责复核与 final_closeout 尚待执行
下一原子动作：执行 C15 / P3 最终收束关卡；当前不提前进入 P4
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

C15_The_Documentation_Interlude：
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

## 16. C14 迭代与推导式：消费位置、求值时机和数据管道边界

`C14_Iterations_and_Comprehensions` 的真正目标不是背会几种推导式语法，而是能沿着下面的链条解释数据如何流动：

```tex
源对象
    -> iter(obj) 取得迭代器
    -> next(iterator) 推进消费位置
    -> 过滤、转换或配对
    -> 消费者决定何时停止
    -> 得到结果，同时留下一个可描述的剩余状态
```

因此，看到任何迭代代码都应继续追问：谁是 iterable，谁是 iterator；谁保存位置；哪一次索取触发了工作；停止时是正常耗尽、短路、`break`、异常，还是迭代器已经不可达；源容器和内部元素对象有没有被修改。

本阶段延续本地化资源审计与 `prompt_template_manager` 的真实代码语境：简单筛选、投影和稳定汇总可以使用推导式；包含统计、错误分流、日志、副作用或结构化报告的扫描继续保留显式循环。

### 16.0 阶段状态和可追溯入口

```tex
2026-07-09：建立 C14 正式实验脚本与 README，并开始有限主线学习。
2026-07-16：C14 阶段测验完成逐题审批，建议得分 99 / 100，通过；学习画像已同步。
2026-07-17：追加 C14 阶段末笔记；最终长期记录职责复核与 C15 启动模板尚待后续执行。
2026-07-19：完成长期记录职责复核并生成唯一 C15 启动模板；C14 正式收束。
```

相关阶段文件：

```tex
docs/C14_ITERATIONS_AND_COMPREHENSIONS_STARTUP_TEMPLATE.md
practice/P3_Statements_and_Syntax/C14_Iterations_and_Comprehensions/README.md
practice/P3_Statements_and_Syntax/C14_Iterations_and_Comprehensions/stage_quiz_iterations_and_comprehensions.md
notes/Python_Learning_Profile.md
```

正式实验脚本：

```tex
01_iter_next_stopiteration.py
02_repeatable_vs_one_shot_iterables.py
03_file_stringio_position_and_consumption.py
04_comprehension_filter_transform_scope.py
05_set_dict_comprehensions_stable_reports.py
06_generator_expressions_lazy_short_circuit.py
07_nested_comprehensions_execution_order.py
08_localization_iteration_pipeline.py
09_prompt_manager_iteration_reading_walkthrough.py
```

### 16.1 阶段地图

本阶段正式主线按以下有限地图推进：

```tex
1. iterable、iterator、iter()、next()、StopIteration 与 for 背后的协议。
2. 可重复遍历容器、独立迭代器和一次性迭代器对象。
3. 文件对象与 StringIO 的共享流位置、EOF 契约和 seek() 边界。
4. list / set / dict 推导式的过滤、转换、作用域、去重和碰撞。
5. 生成器表达式、map()、filter()、zip() 的惰性求值与一次性消费。
6. list()、sorted()、sum() 等完整消费者和 any()、all() 等短路消费者。
7. 嵌套推导式从左到右的子句顺序，以及与显式循环的等价维度。
8. zip(strict=True)、物化、多消费者、共享上游和稳定报告。
9. 本地化审计中的输入契约、统计口径、失败路径和结构化结果。
```

阶段验收观察点：

```tex
1. 能指出对象的协议角色和真正保存消费位置的对象。
2. 能逐次追踪 next()、list()、any() 等消费者推进到了哪里。
3. 能区分急切构造、惰性生产、完整消费和短路消费。
4. 能说明推导式隔离名字绑定，但不隔离共享对象或副作用。
5. 能把“等价改写”限定到数据、调用、作用域、身份和副作用等具体维度。
6. 能为一次性输入、对齐失败、重复 key 和稳定报告选择可审计的工程方案。
```

### 16.2 iterable、iterator 与迭代协议

可迭代对象和迭代器不是两个互斥类型标签，而是两种协议角色：

```tex
iterable：
    能交给 iter(obj) 取得一个迭代器。
    它可能是可重复遍历的容器，也可能本身就是一次性迭代器。

iterator：
    保存当前消费状态；支持 next(iterator) 取得下一项。
    它的 iter(iterator) 应返回自身，所以迭代器同时也是 iterable。
```

典型容器与迭代器的关系：

```python
items = [None, "HP", "MP"]
it = iter(items)

print(iter(items) is items)  # False：列表提供新的列表迭代器
print(iter(it) is it)        # True：迭代器返回自身
print(next(it))              # None：这是普通元素值
print(next(it))              # HP
print(next(it))              # MP
print(next(it, "END"))       # END：默认值接住了协议终止
```

`StopIteration` 是迭代协议的终止信号，不是源数据中自动出现的 `None`。`next(it, default)` 在迭代器耗尽时返回调用方提供的默认值；若这个默认值也可能是合法数据，应使用唯一对象：

```python
END = object()
item = next(it, END)

if item is END:
    print("iterator exhausted")
```

`for` 循环可以用下面的教学模型理解：

```python
iterator = iter(iterable)

while True:
    try:
        item = next(iterator)
    except StopIteration:
        break

    process(item)
```

真实 `for` 由解释器执行该协议，不需要业务代码手工捕获 `StopIteration`。这个展开模型的价值是帮助定位：`iter()` 通常在循环入口调用一次；每轮由 `next()` 取得一个元素；终止信号由循环语句吸收。

还要保留两个边界：

1. `iter(obj)` 是否创建新对象取决于 `obj` 的协议实现，不能机械地说“每次都新建”。
2. `iter(obj)` 能成功，是最直接的运行期可迭代性测试；`collections.abc.Iterable` 的名义判断可能看不到只依赖旧式 `__getitem__` 回退的对象。

### 16.3 独立消费位置、共享上游与文件式位置

同一个列表可以提供多个彼此独立的迭代器：

```python
items = ["HP", "MP", "SP"]
left = iter(items)
right = iter(items)

print(next(left))   # HP
print(next(left))   # MP
print(next(right))  # HP：right 有自己的位置
```

这里共享的是底层列表对象，不共享迭代器位置。列表仍完整；`left` 和 `right` 各自记录消费进度，这可以概念性地称为“独立游标”，但它不是对外公开的列表索引 API。反过来，若两个名字绑定同一个迭代器对象，它们共享同一个位置：

```python
source = iter(["HP", "MP", "SP"])
a = source
b = source

print(next(a))  # HP
print(next(b))  # MP
```

`zip`、`map`、`filter`、生成器表达式等会保存自己的迭代状态；若多个下游又共同引用同一个上游迭代器，下游之间仍会争用同一条数据流。先完整消费的下游可能让后来的下游只看到尾部，甚至直接为空。

文件式对象把迭代位置与底层流位置结合在一起：

```python
from io import StringIO

stream = StringIO("HP\nMP\nSP\n")

print(repr(next(stream)))        # 'HP\n'
print(repr(stream.readline()))   # 'MP\n'
print(list(stream))              # ['SP\n']
print(next(stream, "END"))       # END
print(repr(stream.readline()))   # ''
```

`next(stream)`、`readline()` 和 `list(stream)` 操作同一个流位置，但 EOF 契约不同：迭代协议使用 `StopIteration`，`readline()` 使用空字符串。`seek(0)` 是 `StringIO`/文件 API 提供的重新定位能力，不是通用迭代器协议的“重置按钮”；普通 `zip`、`map`、`filter` 和生成器没有对应的 `seek()`。

### 16.4 耗尽、部分消费、尾部保留与不可达

“源里还有数据”和“当前代码还能继续拿到那些数据”不是同一个问题。描述迭代状态时至少要同时看：

```tex
1. 源对象是什么：容器、流，还是一次性上游。
2. 当前迭代器推进到了哪里。
3. 迭代器是否真的到达 StopIteration。
4. 调用方是否仍持有该迭代器的引用。
5. 是否还能从源容器重新取得一个新迭代器。
```

四种常见状态应严格分开：

| 状态 | 当前迭代器 | 未读尾部 | 后续能力 |
| --- | --- | --- | --- |
| 正常耗尽 | 已到 `StopIteration` | 没有 | 再次消费仍为空 |
| 部分消费且仍可达 | 尚未耗尽 | 仍在当前迭代器之后 | 可从当前位置继续 |
| 部分消费但迭代器不可达 | 尚未耗尽，但临时引用已丢失 | 逻辑上仍在那个迭代器之后 | 不能再访问那条原消费轨迹 |
| 源容器仍完整 | 容器本身不保存单一消费位置 | 容器元素仍在 | 可调用 `iter(container)` 重新遍历 |

例如，函数内部直接遍历列表并在中途 `break`：

```python
def stop_at_bad(records):
    for record in records:
        if record == "BAD":
            break


records = ["HP", "BAD", "MP"]
stop_at_bad(records)
print(records)  # ['HP', 'BAD', 'MP']
```

这里的临时列表迭代器已经取出 `"BAD"`，但并未耗尽；函数返回后它通常不可达。列表本身完全没有被耗尽，因此之后可以创建新迭代器，从 `"HP"` 重新遍历。若调用方传入并保留的是 `source = iter(records)`，函数中途停止后，调用方则能继续从 `"MP"` 读取。

短路和错误检测还可能发生“探测性多取一项”：

```tex
zip(..., strict=True)：
    为确认某一侧更长，可能已经从那一侧取出一个无法组成结果的元素。

精确解包：
    为证明右侧“元素过多”，可能在目标数量之外再取一项，然后抛出 ValueError。

takewhile()：
    必须取出并检查第一个谓词为假的元素；该边界元素不会产出，也不会放回。
```

因此，异常或短路不是事务回滚。已经发生的 `next()`、函数调用、日志、计数和对象修改都不会自动撤销。阶段中关于 `zip(strict=True)` 的追问正说明了这一点：某个额外元素可能已被读取用于确认失配，即使它没有出现在已产出的 pair 或异常对象中。

### 16.5 急切求值、惰性生产与消费者

先区分“创建数据生产者”和“真正索取数据”：

```tex
急切构造：
    列表推导式、集合推导式、字典推导式；
    list()、tuple()、set()、dict()、sorted() 等需要建立完整结果的调用。

惰性生产：
    生成器表达式、map()、filter()、zip()、文件迭代。
    创建对象时通常只建立管道；后续 next() 才逐项驱动工作。

短路消费者：
    any() 遇到第一个真值停止；
    all() 遇到第一个假值停止。

完整消费者：
    list()、tuple()、set()、dict()、sorted()、sum() 通常持续索取到耗尽。
```

`map` / `filter` 的按需轨迹可以写成：

```python
raw = [" hp ", "   ", " mp "]

missing = filter(lambda text: not text.strip(), raw)
normalized = map(lambda text: text.strip().upper(), missing)
```

以上两行只建立惰性对象。第一次 `next(normalized)` 会向 `map` 索取一项；`map` 再向 `filter` 索取；`filter` 可能从 `raw` 的内部迭代器连续检查多项，直到找到通过谓词的原始元素；`map` 最后转换那一项。一次下游索取不保证只从源读取一个元素。

生成器表达式有一个容易漏掉的精确边界：最左侧 `for ... in` 后的表达式会在生成器创建时求值，以取得最外层迭代器；循环体、过滤条件、结果表达式和后续子句仍在消费时惰性执行。

```python
def source():
    print("source()")
    return [1, 2, 3]


generated = (value * 10 for value in source() if value % 2)
print("A")
print(next(generated))
```

这里 `source()` 先于 `"A"` 打印；奇偶检查和乘法仍等到 `next()` 才发生。

短路消费者既返回结果，也留下消费状态：

```python
records = [False, False, True, False]
checks = (value for value in records)

print(any(checks))   # True：在第三项短路
print(list(checks))  # [False]：第四项仍在尾部
```

`all()` 的对偶规则相同：遇到第一个假值停止。空输入遵循逻辑恒等值：

```python
all([])  # True：不存在反例
any([])  # False：不存在真值见证
```

还要注意：内置生成器对象本身通常为真，`bool(generator)` 不是“是否还有元素”的检测。更严格地说，迭代器协议没有规定所有自定义迭代器都必须永久为真；自定义类型仍可另行实现真值协议。对一次性迭代器试探是否为空通常会消费一项，若必须保留它，需要重新设计接口、缓存首项或使用合适的分叉策略。

物化是把一次性数据流变成可重复遍历外层容器的常见边界：

```python
active_records = list(record for record in records if record["enabled"])
keys = [record["key"] for record in active_records]
texts = [record["target"] for record in active_records]
```

代价是立即完成上游工作并占用与结果规模相关的内存。物化还只是收集元素引用；除非显式复制，内部可变对象仍与原数据共享。

### 16.6 列表、集合、字典推导式的执行与对象边界

一层列表推导式：

```python
result = [normalize(text) for text in raw if keep(text)]
```

按每个元素的真实执行顺序展开为：

```python
result = []

for text in raw:
    if keep(text):
        result.append(normalize(text))
```

虽然结果表达式写在最前面，但每项必须先由后面的 `if keep(text)` 判定；只有通过过滤才调用 `normalize(text)`。列表推导式是急切构造，赋值语句结束时遍历、过滤、转换和列表建立都已经完成。

Python 3 中，推导式循环目标位于推导式自己的隐式作用域中：

```python
text = "OUTER"
result = [text.strip() for text in [" HP ", " MP "]]

print(text)  # OUTER
```

隔离的是名字绑定，不是对象世界。推导式仍能修改它引用到的外部可变对象：

```python
audit = []
keys = ["ui.hp", "ui.mp"]

result = [audit.append(key) for key in keys]

print(result)  # [None, None]
print(audit)   # ['ui.hp', 'ui.mp']
```

这段代码合法却不清晰：`append()` 原地修改列表并返回 `None`，推导式因此制造无意义的结果列表，还把副作用隐藏在结果表达式中。只为副作用而遍历时，使用显式 `for`；若意图只是批量追加，且输入契约合适，也可使用 `audit.extend(keys)`。

集合推导式适合规范化后去重：

```python
nonempty_keys = {
    key.strip().lower()
    for key, text in records
    if text.strip()
}
```

集合没有业务顺序承诺。哈希随机化可能影响观察到的排列，但“集合是无序抽象”才是首要规则。人读或可比对报告应写 `sorted(nonempty_keys)`；这里的价值是稳定、可复现的报告顺序，不应把排序本身误称为“幂等性”。

字典推导式适合已经验证过的唯一 key 到 value 的映射：

```python
text_by_key = {
    key.strip().lower(): text.strip()
    for key, text in records
    if text.strip()
}
```

若多个原始 key 规范化为同一个 key，后写入的 value 会静默覆盖先前 value。覆盖现有 key 不会把它移动到字典末尾；该 key 仍保留第一次插入的位置。若重复本身是错误，就不能依赖字典推导式发现它，应在显式扫描中用 `seen_keys` 或结果映射按业务口径检测并报告。

字典直接迭代默认产出 key；需要稳定成功结果时可用：

```python
valid_items = sorted(valid_by_key.items())
```

这会建立按 key 排序的新外层列表，但其中的可变 value 仍是原映射里的同一个对象。排序稳定视图不等于深层隔离快照。

### 16.7 嵌套推导式与“等价改写”的具体维度

嵌套推导式的子句从左到右建立嵌套层次：

```python
result = [
    normalize(section, text)
    for section, entries in groups
    if enabled(section)
    for text in entries_for(section, entries)
    if keep(text)
]
```

真实顺序是：

```tex
1. 从 groups 取得一个 (section, entries)。
2. 调用 enabled(section)。
3. 只有外层条件为真，才求值 entries_for(section, entries)。
4. 从该内层 iterable 逐项取得 text。
5. 调用 keep(text)。
6. 只有内层条件为真，才调用 normalize(section, text) 并收集结果。
7. 返回外层循环处理下一组。
```

对应的显式循环是：

```python
result = []

for section, entries in groups:
    if enabled(section):
        for text in entries_for(section, entries):
            if keep(text):
                result.append(normalize(section, text))
```

这两个版本可以在以下维度上等价：遍历顺序、过滤路径、函数调用顺序、结果元素和结果顺序。但“语义等价”必须写明观察维度，不能无限扩大：

| 维度 | 是否自动等价 | 需要检查什么 |
| --- | --- | --- |
| 结果值与顺序 | 可能 | 过滤和转换顺序是否一致 |
| 上游取值次数 | 可能 | 惰性边界、短路和异常是否改变取值 |
| 函数调用及副作用顺序 | 可能 | `if`、结果表达式和嵌套入口的位置 |
| 外层名字环境 | 不自动 | 普通 `for` 目标会留在当前作用域 |
| 对象身份与共享引用 | 不自动 | 是否构造新容器、是否复制内部对象 |
| 异常时机与部分结果 | 不自动 | 急切/惰性求值何时触发异常 |
| 内存占用与可重复消费 | 不自动 | 是列表、生成器还是一次性上游 |
| 日志、统计和错误分流 | 不自动 | 是否隐藏了顺序或丢失中间状态 |

阶段测验 C1 暴露的精修点正发生在“名字环境”维度。将显式循环目标从 `text` 改名为 `candidate`，可以避免覆盖已有的外层 `text`，但普通 `for` 不创建块级作用域；循环后 `candidate` 仍会新增或被重绑定。因此它与推导式在数据结果上等价，却不在完整名字环境上等价。若确实需要隔离普通循环目标，应把循环放进函数等真实作用域，而不是只换一个变量名。

嵌套层数一多，读者需要在头脑中反向重建控制流。下列情况通常应退回显式循环：

```tex
1. 多层过滤对应不同业务原因。
2. 需要多个统计字段或逐步状态。
3. 有 break、continue、异常分流或资源清理。
4. 需要日志、文件写入或可审计副作用。
5. 中间结果有业务名称，值得显式保存。
6. 推导式已经无法一眼看出执行顺序。
```

### 16.8 `zip(strict=True)`、物化与多消费者

普通 `zip()` 默认在最短输入耗尽时停止，可能静默截断较长输入。`zip(..., strict=True)` 会在消费时验证所有输入是否同时耗尽，并在长度不一致时抛出 `ValueError`：

```python
pairs = zip(keys, texts, strict=True)
```

它能检查的是**当前两个迭代流的长度对齐**，不能恢复已经丢失的原始行身份。危险写法是先独立过滤两列，再配对：

```python
clean_keys = (key for key in keys if key.strip())
clean_texts = (text for text in texts if text.strip())
pairs = zip(clean_keys, clean_texts, strict=True)
```

即使过滤后的长度相等，某个 key 仍可能与另一原始行的 text 错配。可靠原则是先保留整行关系，再按整行过滤：

```python
clean_pairs = [
    (key, text)
    for key, text in zip(keys, texts, strict=True)
    if key.strip() and text.strip()
]
```

`strict=True` 的错误是惰性暴露、非事务式的。只有消费者继续索取到失配边界时才报错；之前已经产出的 pair、发生的计数和副作用不会回滚。为确认某侧更长，`zip` 还可能从该侧读取一个无法配对的额外元素。阶段追问中“为什么错误后只剩 `tail`，而不是 `note` 和 `tail`”的答案就是：`note` 已被失配检测用作探测项并丢失，只有尚未探测的 `tail` 仍留在上游。

一个一次性上游不能无计划地交给多个消费者：

```python
active = (record for record in records if record["enabled"])
keys = (record["key"] for record in active)
texts = (record["target"] for record in active)

print(list(keys))
print(list(texts))  # active 可能已被 keys 耗尽
```

常见修复有三类：

```tex
方案一：先物化。
    active_records = [record for record in records if record["enabled"]]
    适合数据规模可控、需要重复遍历和稳定快照边界的场景。

方案二：从可重复源分别重建管道。
    适合源容器可重复遍历、每次筛选成本可接受的场景。

方案三：itertools.tee() 分叉一次性上游。
    适合分支步调接近、不能重建源又不想立即全部物化的场景。
```

`tee()` 创建的是多个逻辑迭代器，没有复制底层数据来源。为保证慢分支日后还能取得快分支已经越过的元素，它必须缓存分支之间的进度差。若一个分支读完而另一个几乎不动，缓存可能增长到接近全部数据；内存开销与分支步调差有关，不是恒定成本。

物化解决的是重复遍历和消费所有权问题，但不自动提供深拷贝、不可变性或事务性：

```python
snapshot = list(records)
```

`snapshot` 是新的外层列表；其中元素通常仍是原来的对象。若需要隔离报告，应根据契约构造新的干净记录、浅复制指定层级、深复制，或转换成不可变投影，而不是只依赖 `list()`。

### 16.9 稳定报告、输入契约与结构化扫描

稳定报告不等于“所有结果都排序”。顺序要服务于语义：

```tex
带 line_no 的 issues：
    通常保留源扫描顺序，方便回到原文件定位。

纯 key 集合、缺失占位符集合：
    使用 sorted(...)，得到可复现的人读顺序。

成功结果映射的汇总视图：
    valid_items = sorted(valid_by_key.items())。

时间线日志：
    最近优先时可 reversed(logs)，它反转既有位置顺序。

严重度排名：
    sorted(logs, key=severity, reverse=True)，它按内容重新排序。
```

`reversed()` 与降序排序不能混为一谈：前者基于已有位置，后者基于内容键建立新排名。字典视图如 `mapping.items()` 是动态、可重复遍历的视图；`list(mapping.items())` 或 `sorted(mapping.items())` 是创建时的浅外层快照，内部可变 value 仍可能共享。

真实扫描函数还必须把类型策略写成输入契约。下面的写法不是纯清洗细节：

```python
key = str(record["key"]).strip().lower()
target = "" if raw_target is None else str(raw_target).strip()
```

`str(...)` 会静默接纳整数、`None` 和自定义对象，可能掩盖上游类型错误或丢失结构信息。工程上应明确二选一：

```tex
严格模式：
    key / target 必须是 str；否则报告 fatal error 或普通 issue。

宽松模式：
    明确允许字符串化；规定 None、数字和自定义对象的转换语义，
    并接受信息损失与潜在 key 碰撞。
```

重复 key 也有不同口径：

```tex
if key in valid_by_key：
    “此前已有一次成功写入”的重复。
    第一次无效、第二次有效时，第二次仍可成为首个成功结果。

if key in seen_keys：
    “原始输入中已经出现过”的重复。
    不论第一次是否有效，第二次都报告重复。
```

必须先写清业务定义，再选择状态容器。不能让某个方便的推导式或映射结构偷偷替业务做决定。

本阶段综合审计函数保留显式循环，因为它同时承担：

```tex
1. 对任意 iterable 的单次消费和 enumerate() 原始位置。
2. read / disabled / enabled / valid 的不同统计口径。
3. 非字典、缺 key 等阻断错误与普通 issue 的分流。
4. break、continue、重复 key 状态和占位符检查。
5. 从原始输入构造新的干净结果，而不修改输入记录。
6. 扫描结束后的稳定 valid_items 和结构化 return。
```

统计语句的位置就是口径：取得元素后立即增加 `read`，表示“已从上游读取”；禁用分支前后决定 `enabled` 是否包含禁用记录；所有检查通过并成功写入后才增加 `valid`。核心函数返回 `report`，不直接 `print()`；CLI 展示、日志、JSON/CSV 和文件写入留在外层边界。

`prompt_template_manager` 的只读实验进一步给出了两种真实选型：

```tex
parse_tags：
    需要去重且保留首次出现顺序，显式循环比 set 推导式更符合契约。

tags_from_json 后的简单类型投影、活动且未锁定标题筛选：
    数据已经结构化，适合列表/字典推导式。

按内容哈希分组并找重复：
    需要逐步维护 digest -> ids 状态，显式循环更清楚。
```

相关实验只导入纯辅助函数并读取源码文本，没有打开、初始化或修改 SQLite 数据库。这也体现工程边界：为了学习迭代写法，不应顺手扩大到持久化状态变更。

### 16.10 本阶段你的理解轨迹、问题与修正规则

1. 关于真实 `None` 与终止信号：

   ```tex
   你的判断：
       next(it) 取得的 None 可以是普通元素；StopIteration 才是协议终止。

   结论：
       正确。
       不要根据元素真值猜测迭代是否结束；next(it, sentinel) 的 sentinel
       也应避免与合法数据相等或相同。
   ```

2. 关于两个列表迭代器和源列表：

   ```tex
   你的判断：
       iter(items) 两次得到两个独立迭代器，各自维护位置；items 本身完好无损，
       容器不应被描述为“耗尽”。

   结论：
       正确。
       iterator 同时也是 iterable，但 iterable 不一定是 iterator。
   ```

3. 关于 `zip`、`map`、`filter` 和生成器：

   ```tex
   你的判断：
       它们在 Python 3 中建立惰性、一次性的数据流；next() 按需索取，
       list() 从当前位置收集剩余项，第二次完整收集通常为空。

   结论：
       正确。
       还要继续指出过滤器为找到一个产出，可能检查多个上游元素。
   ```

4. 关于文件对象与 `seek(0)`：

   ```tex
   你的理解：
       next()、readline() 和 list(stream) 共享流位置；seek(0) 后可重新读取，
       但这不推翻一次性向前消费模型。

   结论：
       正确。
       更精确地说，seek() 是具体流对象的定位 API，它改变后续读取所依赖的
       流位置；它不是迭代器协议普遍提供的重置操作。
   ```

5. 关于推导式作用域和副作用：

   ```tex
   你的判断：
       推导式循环目标不会泄漏到外层，但 audit.append(key) 仍能修改外部列表；
       [audit.append(...)] 会收集 None，属于不清晰的副作用写法。

   结论：
       正确。
       作用域隔离名字绑定，不隔离共享对象、I/O、函数调用或异常。
   ```

6. 关于集合顺序与稳定报告：

   ```tex
   你的原表述：
       集合无序且受哈希随机化保护，所以直接打印不稳定；sorted() 使结果稳定。

   精修：
       结论方向正确，但语言契约首先是“set 没有业务顺序保证”；
       哈希随机化只是观察顺序变化的一个影响因素。
       sorted() 提供可复现顺序，不应把这种性质称为幂等性。
   ```

7. 关于生成器表达式的创建时机：

   ```tex
   你的判断：
       最左侧 iterable 表达式 source() 在生成器创建时求值；过滤和转换仍惰性。

   结论：
       正确。
       “生成器表达式完全什么都不做，直到 next()”是过度概括。
   ```

8. 关于 `any()` / `all()` 和剩余尾部：

   ```tex
   你的判断：
       any() 在第一个真值短路，all() 在第一个假值短路；未索取的尾部仍可继续；
       all([]) 为 True，any([]) 为 False。

   结论：
       正确。
       内置生成器对象的真值不能用来判断是否为空；但不要把这一观察扩写成
       “迭代器协议强制所有自定义迭代器永远为真”。
   ```

9. 关于 `tee()`：

   ```tex
   你的总结：
       tee() 没有复制底层来源；它用缓存弥补分支步调差，内存开销随最大滞后增长。

   结论：
       正确。
       “队列缓存”可以作为概念模型，但不应把它误当成必须依赖的具体内部实现。
   ```

10. 关于 `iter(callable, sentinel)`：

    ```tex
    你的发现：
        sentinel 使用 == 比较；False == 0，因此以 0 为 sentinel 时，
        callable 返回 False 会提前终止，而且这个终止值不产出。

    精修：
        False == 0 导致提前终止的判断正确，但不能只把 sentinel 参数改成 object()
        而让原 callable 继续用 0 表示结束；那样二者永远不相等，迭代反而不会按原位置停止。
        唯一 object 哨兵只在 callable 或包装器会于终止时返回“同一个哨兵对象”时成立。
        否则应选择天然且无歧义的返回值哨兵，或改用显式循环表达结束契约。
    ```

11. 关于 `enumerate()` 的位置：

    ```tex
    你的判断：
        先 enumerate 后过滤，编号代表源位置；先过滤后 enumerate，编号代表结果序号。

    结论：
        正确。
        行号审计通常应先编号，紧凑展示序号通常可后编号。
    ```

12. 关于 `islice()` 消费到哪里：

    ```tex
    你的初始误判：
        islice(start, stop, step) 只需产出足够次数，因此最后一次产出后即可停止，
        被 step 跳过的末尾元素应保留。

    修正：
        islice 基于当前迭代位置工作，不是对序列索引做无副作用随机访问。
        完整消费 islice 会把上游推进到 stop 边界，沿途未产出的跳步元素也会被读取；
        stop 位置本身不属于切片。若同时绕过 islice 直接消费共享上游，后续观察位置还会改变。
    ```

13. 关于 `dropwhile()`：

    ```tex
    你的判断：
        谓词第一次为假后，dropwhile 永久结束“丢弃前缀”阶段；
        后续元素全部原样产出，不再调用谓词。

    结论：
        正确。
        它不是对所有元素做 filter，而是在定位一个边界。
    ```

14. 关于恢复数据流与共享源：

    ```tex
    你的发现：
        用 chain() 把已探测首项接回去，只能恢复那一项与同一 source 的未来尾部；
        若外部先 next(source) 取走 MP，restored 就不可能再产出 MP。

    结论：
        正确。
        包装器没有复制共享上游，也不能撤销其它消费者已经发生的消费。
    ```

15. 关于 `zip(strict=True)`、精确解包和隐藏探测：

    ```tex
    你的重点追问：
        为什么失配后只剩 tail，而不是 note 与 tail？

    修正模型：
        为证明长度不一致，消费者必须多做一次 next() 探测；note 已被取出但无法组成结果，
        不会自动放回，tail 才是尚未读取的部分。
        同样，精确解包为了证明“过多”也可能消费目标数量之外的一项。
    ```

这些轨迹说明，本阶段真正需要长期保留的不是某个 API 的输出表，而是“每一次 `next()` 都会改变谁的状态，且不会自动回滚”的统一模型。

### 16.11 可选迭代工具的紧凑边界

以下工具是本会话中已经学习过的可选延伸，不属于 C14 阶段测验计分主线；只保留其耐久边界：

```tex
iter(callable, sentinel)：
    重复调用无参数 callable，结果与 sentinel 相等时停止并吞掉该结果。

tee(iterable, n)：
    建立逻辑分支；共享一次性来源，通过缓存吸收分支进度差。

chain(a, b, ...)：
    顺序串联 iterable；不会复制任何共享上游。

islice(iterable, start, stop, step)：
    按迭代位置取样；完整消费会推进到 stop，跳过项同样会消耗。

takewhile(predicate, iterable)：
    产出真值前缀；第一个假值边界元素已被检查并丢弃。

dropwhile(predicate, iterable)：
    丢弃真值前缀；第一个假值起全部原样产出，不再检查谓词。

groupby(iterable, key=...)：
    只分组相邻连续项；组迭代器共享上游，通常应及时消费当前组。

pairwise(iterable)：
    保存一个前项形成相邻二元组；绕过它消费共享上游会改变后续邻接关系。

batched(iterable, n, strict=False)：
    按批次消费；strict=True 遇到不完整尾批时会在尾部报错，
    但此前完整批次和副作用已经发生。

reversed(sequence)：
    反转既有位置顺序；不是按某个字段计算排名。
```

这些 API 的共同风险仍是共享状态、隐藏探测、部分消费和错误不回滚。知道工具名字不等于应该使用它；显式循环更能表达业务边界时，清晰度优先。

### 16.12 阶段测验暴露的薄弱处与修正规则

C14 阶段测验建议得分为 `99 / 100`。十二个计分项均完成逐题审批；全部输出预测正确，扣分只发生在两个术语覆盖范围上。

```tex
扣分点1：普通循环换名不等于获得推导式作用域（C1，扣 0.5 分）

原答案：
    使用 candidate 可保留外层 text，因此与推导式保持相同外部绑定效果。

修正：
    candidate 在普通 for 所在作用域中仍会新增或重绑定。
    两个版本的数据流、调用顺序和 result 等价，不代表完整名字环境等价。

长期规则：
    说“等价”时明确结果、调用、作用域、身份、异常和副作用中的具体维度。
```

```tex
扣分点2：fatal break 后的临时列表迭代器不一定耗尽（F1，扣 0.5 分）

原答案：
    records 是列表时，列表不耗尽；耗尽的是 for 内部创建的迭代器。

修正：
    只有正常完整扫描才会耗尽内部迭代器。
    中途 break 时，它可能只消费到阻断记录；函数返回后只是因未保存而不可达。

长期规则：
    严格区分已耗尽、部分消费且可达、尾部仍在但迭代器不可达，
    以及源容器仍能重新提供新迭代器。
```

三项不扣分但必须保留的工程补强：

```tex
1. str(...) 是输入转换策略，不是无害细节；严格拒绝还是允许转换必须成约。
2. sorted(mapping.items()) 只建立排序稳定的新外层列表，不深复制可变 value。
3. duplicate 的定义若从“第二次成功写入”改成“第二次原始出现”，
   必须从 valid_by_key 检查改为独立 seen_keys 状态。
```

本次测验确认的稳定强项：

```tex
1. 能从协议层解释 iterable、iterator、iter()、next() 和 StopIteration。
2. 能精确追踪独立位置、共享上游、文件位置、短路尾部和重复消费。
3. 能指出惰性工作由哪个消费者的哪一次索取触发。
4. 能解释推导式作用域、共享可变对象和副作用之间的层次。
5. 能处理 set/dict 碰撞、稳定排序、zip 对齐与物化边界。
6. 能设计一次扫描任意 iterable 的结构化本地化审计函数。
```

### 16.13 工程应知应会、禁忌和技巧清单

协议与状态：

```tex
1. iterable 的职责是提供迭代器；iterator 的职责是保存位置并逐项产出。
2. iterator 的 iter(iterator) 返回自身，因此 iterator 同时也是 iterable。
3. next() 只能直接作用于 iterator；for 会先替你调用 iter()。
4. StopIteration 是协议终止；None、False、0 和空字符串都可能是合法数据。
5. next(it, default) 的 default 若可能与数据冲突，应使用唯一哨兵对象。
6. 不要机械假设 iter(obj) 每次都创建新对象；检查对象的协议角色。
7. 列表、字典、集合和字符串通常可重复遍历，因为能提供新迭代器。
8. zip、map、filter、生成器表达式和多数文件对象通常保存一次性消费位置。
9. 两个独立迭代器可以读取同一容器而互不共享位置。
10. 两个名字或两个下游若共享同一迭代器，就共享并竞争同一位置。
11. 容器不称为“耗尽”；应说明某个迭代器是否耗尽。
12. 短路、break、异常只说明停止原因，不自动说明迭代器已耗尽。
13. 尾部仍存在时，还要说明迭代器是否可达、源是否可重新迭代。
14. 文件 next()、readline() 和迭代收集共享文件位置；EOF 契约各不相同。
15. seek() 是流定位 API，不是所有迭代器共有的重置协议。
```

求值与消费：

```tex
16. 列表、集合、字典推导式在赋值完成前已经急切构造结果。
17. 生成器表达式、map()、filter()、zip() 在消费者索取时逐项工作。
18. 生成器表达式最左侧 iterable 表达式在创建时求值，其余环节仍可惰性。
19. 一次下游 next() 可能让 filter 检查多个上游元素。
20. list()、sorted()、sum() 等通常完整消费；any()、all() 会短路。
21. any() 短路后可能留下尾部；all() 同理。
22. all([]) 为 True，any([]) 为 False。
23. 不要用 bool(generator) 判断生成器是否为空或耗尽。
24. 用 next() 试探一次性迭代器前，先接受它会推进位置；必要时缓存首项。
25. 物化能建立可重复遍历的外层容器，但会立即计算并占用结果规模的内存。
26. 物化收集的是元素引用；新外层容器不等于深拷贝。
```

推导式与等价改写：

```tex
27. 推导式每项先执行 for，再执行对应 if，最后求值结果表达式。
28. 多层 for / if 子句从左到右建立与显式嵌套循环相同的控制层次。
29. 推导式循环目标不泄漏，但外部可变对象仍可能被原地修改。
30. 不要用推导式只做 append()、日志、文件写入或其它复杂副作用。
31. 集合推导式适合去重和成员集合；报告输出前按语义决定是否 sorted()。
32. 字典推导式的重复 key 会静默后写覆盖；覆盖不会移动首次插入位置。
33. 重复 key 是错误时，用显式状态检测，不要依赖构造后的字典反推。
34. “等价改写”要标明结果、调用顺序、名字环境、身份、异常和副作用维度。
35. 普通 for 换变量名只避免覆盖某个名字，不会获得推导式作用域。
36. 包含统计、break、多个 continue、错误分流或结构化报告时，优先显式循环。
```

对齐、多消费者与报告：

```tex
37. 普通 zip() 默认静默截断到最短输入。
38. zip(strict=True) 检查长度同时耗尽，不检查原始记录语义身份。
39. 不要先独立过滤强相关的两列再 zip；先保持整行关系，再过滤整行。
40. zip(strict=True) 惰性报错且不回滚，失配探测可能额外消费一项。
41. 多消费者需要明确所有权：物化、从可重复源重建，或谨慎使用 tee()。
42. tee() 的缓存随分支步调差增长，不能当作零成本复制。
43. enumerate() 放在过滤前得到源位置，放在过滤后得到紧凑结果序号。
44. 带 line_no 的 issues 通常保留源顺序；纯 key 集合和缺项集合通常排序。
45. reversed() 反转既有顺序；sorted(..., key=..., reverse=True) 按内容排名。
46. sorted(mapping.items()) 是排序后的浅外层视图，不是深层不可变快照。
47. 动态字典视图与 list(...) 快照要分开：前者随映射变化，后者固定外层项序列。
```

输入契约与扫描工具：

```tex
48. str(...) 静默转换必须是明确业务策略，不能由实现顺手决定。
49. key、target、None、数字和自定义对象的接受/拒绝规则应写进输入契约。
50. duplicate 是“第二次出现”还是“第二次成功写入”，要先定义再选 seen_keys 或 valid_by_key。
51. 统计语句的位置决定 read、enabled、valid 等字段的真实口径。
52. fatal error 表示结构上无法可靠继续；ordinary issue 表示可记录后继续扫描。
53. 异常与 break 不会回滚此前的计数、追加、读取或对象修改。
54. 核心扫描函数返回结构化 report；print、日志和文件写入属于外层展示边界。
55. 原始输入到成功结果优先构造新的干净记录，不直接复用或修改输入字典。
56. 简单过滤、投影、缺项排序适合推导式；多步分组、统计和错误控制适合显式循环。
57. 读取真实项目代码作为教学背景时，保持持久化边界；本阶段不打开或修改 prompt manager SQLite。
```

最常见禁忌可以压缩为七条：

```tex
1. 不把容器说成耗尽。
2. 不把短路或 break 自动说成迭代器耗尽。
3. 不用生成器对象的真值判断剩余元素。
4. 不让两个消费者无意争用同一个一次性上游。
5. 不把 zip(strict=True) 当作语义对齐或事务回滚机制。
6. 不为追求一行代码把统计、错误和副作用塞进推导式。
7. 不把“新外层容器/排序视图”误称为深拷贝或深层快照。
```

### 16.14 阶段精髓小结

```tex
1. C14 的核心不是把 for 写短，而是理解谁在提供数据、谁在保存位置、谁在消费。
2. iterable 能提供 iterator；iterator 用 next() 逐项推进，并以 StopIteration 终止。
3. None 是普通数据的可能值，不能代替协议终止信号。
4. 可重复遍历属于源对象提供新迭代器的能力；一次性消费属于具体迭代器状态。
5. 多个独立迭代器有独立位置；多个引用或下游共享同一迭代器时共享位置。
6. 文件对象把迭代位置与流位置结合；seek() 是额外流能力，不是通用重置协议。
7. 已耗尽、部分消费且可达、尾部仍在但迭代器不可达、源容器可重遍历必须分开。
8. 惰性生产把工作推迟到消费者索取；急切构造在表达式结束前完成结果。
9. 短路消费者的价值不仅是返回真假，还包括避免不必要的后续计算。
10. 短路、异常和失配检测可能留下尾部，也可能为了判定边界多消费一项。
11. 推导式适合清楚的过滤、转换和容器构造；复杂状态迁移应保留显式循环。
12. 推导式隔离循环目标名字，不隔离共享对象、副作用、异常或底层数据来源。
13. 集合负责集合语义，不负责业务顺序；稳定报告按语义排序。
14. 字典碰撞默认静默后写覆盖；重复是错误时必须显式审计。
15. 嵌套推导式按左到右子句展开；可读性低于显式循环时应主动展开。
16. 等价改写只在指定观察维度成立，不自动覆盖作用域、身份、异常和副作用。
17. zip(strict=True) 检查当前流长度，不保证原始行身份，也不提供回滚。
18. 物化解决重复遍历和所有权问题，但付出立即计算、内存和浅引用共享代价。
19. 输入类型转换、重复口径、统计位置和稳定顺序都属于业务契约。
20. C14 的工程价值，是把 C13 的显式循环提升为可解释、可组合、可审计的数据流模型。
```

## 17. C15 文档间奏：源码、对象元数据、工具输出与合同证据

`C15_The_Documentation_Interlude` 的真正目标不是“记住几个查文档的函数”，而是把
C10-C14 已建立的对象与执行模型升级为一套证据驱动的调查方法：

```tex
先明确要判断的主张
    -> 区分源码、对象元数据、人读输出、签名、官方合同和当前运行观察
    -> 把合同拆成类型、参数、返回、异常、副作用、版本和实现说明
    -> 选择风险最低、足以回答问题的最小核验
    -> 记录解释器、输入、观察结果和未证明范围
    -> 只形成证据真正支持的有限结论
```

C15 是 P3 的 `PART closer`。它既要建立日常查证能力，也要把表达式、赋值、条件、
循环、迭代和推导式压缩成可重复使用的 P3 自查链；P4 只保留入口问题，不在本章
提前系统展开。

### 17.0 阶段状态和可追溯入口

```tex
2026-07-19：完成 C15 前置准备，确认章节角色为 P3 的 PART closer；capstone 未排期。
2026-07-22 至 2026-07-23：完成六步有限正式主线，主线达到 100%。
2026-07-24：完成 11 / 11 题逐题审批，阶段测验建议得分 98 / 100。
2026-07-24：学习画像同步完成，并追加本阶段末笔记。

当前生命周期阶段：final_closeout（尚未执行）。
```

唯一权威路线：

```tex
docs/C15_THE_DOCUMENTATION_INTERLUDE_STARTUP_TEMPLATE.md
```

六步正式主线与验收证据：

```tex
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/README.md
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/01_documentation_layers_and_dunder_doc.py
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/02_dir_name_discovery_boundaries.py
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/03_help_output_return_and_pydoc.py
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/04_signature_version_and_contract_checks.py
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/05_prompt_manager_documentation_walkthrough.py
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/06_p3_closer_self_check.py
practice/P3_Statements_and_Syntax/C15_The_Documentation_Interlude/stage_quiz_the_documentation_interlude.md
notes/Python_Learning_Profile.md
```

目录中的其它对象诊断、卡片模板、质量门和 JSON 报告属于相邻同主题补充工件，只能
作为可选设计背景或既有完成证据；它们不定义必学范围，不证明正式主线关卡，也不是
capstone。后续收束仍须保留其既有 dirty-worktree 状态。

路线图中的“可配置本地化批处理工作流”只是候选，不是已排期 capstone。本章没有
因为 closer 角色临时发明强制项目；正式路径保持为：

```tex
preparation
    -> mainline
    -> quiz_authoring
    -> quiz_answering
    -> quiz_review
    -> stage_note
    -> final_closeout（尚待）
```

### 17.1 阶段地图、应知应会与本质模型

有限主线共六步：

```tex
第一步：文档层级
    注释、普通字符串表达式、docstring、__doc__、工具显示和业务返回。

第二步：名称发现
    dir()、真实属性访问、动态属性、callable() 与公共合同的不同关卡。

第三步：帮助文本
    help() 的显示副作用与 None 返回；pydoc.render_doc() 的 str 返回。

第四步：合同核验
    当前签名、官方文档、版本信息、异常、副作用与最小实验。

第五步：只读实码走查
    固定白名单、检查导入路径、合成输入、结构化证据与有限持久化护栏。

第六步：P3 closer 自查
    把 C10-C15 的对象、控制流、迭代状态和证据来源用于同一段代码。
```

必学核心：

1. 能把源码事实、对象元数据、面向人的显示、函数返回对象、公开合同和当前运行
   观察分开。
2. 能把 `dir()` 用作候选名称入口，而不是对象全部能力或稳定 API 清单。
3. 能把对象类型、调用形状、参数语义、返回、异常、副作用、版本变化和实现说明
   当作不同合同字段核对。
4. 能记录当前 Python 解释器和实现，用最小实验验证稳定语义，而不是背偶然排版。
5. 能在真实代码中先限定授权范围和调用白名单，再进行低风险、可复核的调查。
6. 能用证据账本说明“结论来自哪里、不能证明什么、下一步最小检查是什么”。

必要补救在本章结束时已经压实：

```tex
help() 显示人读文本，但返回 None。
dir() 发现名字，不证明可访问、可调用、公开、稳定或无副作用。
docstring 取决于特殊首语句位置，不取决于是否使用三引号这一外观。
文档中的公开合同与当前解释器观察不能互相冒充。
```

更多 `pydoc` / `inspect` 功能、pager 排版、文档生成器、完整沙箱设计和额外项目
源码走查都属于可选拓展，不影响本章验收，也没有被提升为必学范围。

本章最重要的证据阶梯是：

```tex
dir(obj)
    发现候选名称

__doc__ / help() / pydoc
    获取当前环境中的本地人读线索

官方文档
    确认公开合同、版本范围和明确承诺

inspect.signature() 等聚焦探针
    观察当前对象的运行期形状

最小实验
    验证当前解释器中的稳定行为
```

这不是要求每次机械调用全部工具。应先问“当前主张需要哪一层证据”，再选择最小
充分组合；工具越多，不代表结论自动越可靠。

### 17.2 文档层级：在 C10 的 docstring 模型上增加证据边界

C10 的 `12.8` 已经完整解释注释、普通字符串表达式和文档字符串的基本区别，本节
不重复定义和示例。C10 已确认“三引号只是字符串写法、特殊首语句位置决定 docstring、
普通注释不占语句位置、后置字符串只是普通表达式”；C15 只增加证据分工：

```tex
源码 / AST：
    回答注释、字符串表达式、语法位置和源码结构。

obj.__doc__：
    回答当前运行对象通过属性访问呈现什么文档元数据。普通模块、函数和按惯例定义的
    类通常得到 str 或 None；对任意自定义对象，访问可能返回其它对象、执行代码或失败。

inspect.getdoc(obj)：
    成功时返回清理缩进后的人读 str 或 None，并可能沿继承关系寻找文档；它仍是
    运行期内省，不等同于只对 obj.__doc__ 做静态清理。

对象业务调用：
    按函数合同执行并返回业务对象；不能由文档文本替代。
```

长期证明边界：

1. `__doc__` 不能还原源码注释、全部普通字符串、精确空白或源码位置。
2. 源码中存在字符串，不证明它已经成为某个对象的 docstring；必须检查语法位置。
3. 当前 `__doc__` 为 `None` 不一定证明作者从未写过 docstring；例如 `-OO` 优化可能
   移除 docstring，运行期元数据也可能被包装或改变。
4. AST 和源码适合回答源码结构；对象元数据适合回答当前运行对象携带什么信息。
5. `inspect.getdoc()` 是运行期内省，还可能继承基类文档；不应对任意不可信对象先验
   宣称为只读取目标自身 `__doc__` 的静态、无副作用操作。

本节新增的常见误区是：把 `__doc__` / `inspect.getdoc()` 当成完整源码或稳定公共合同，
以及把运行期内省误称为静态安全读取。基础位置错误继续回看 `12.8`，不在这里复刻。

### 17.3 `dir()`、属性访问、可调用性与公共合同是不同关卡

`dir(obj)` 返回的是名称字符串列表，不是已经解析好的属性值，更不是稳定 API 清单。
默认结果可能组合实例、类、继承层次和自定义 `__dir__()` 提供的候选名称。

本章的两个反向例子必须长期保留：

```tex
自定义 __dir__()：
    可以广告 advertised_only，但真实属性访问失败。

动态 __getattr__()：
    可以提供 runtime_alias，即使它没有出现在 dir() 中。
```

因此：

```tex
name in dir(obj)  既不是属性可访问的充分条件，也不是必要条件。
```

从发现到合同至少有六道独立关卡：

| 关卡 | 工具或证据 | 仍不能自动证明 |
| --- | --- | --- |
| 名称被发现 | `name in dir(obj)` | 属性真实存在或可访问 |
| 当前可访问 | `getattr()` / `hasattr()` | 无副作用、下次仍相同 |
| 当前可调用 | `callable(value)` | 参数适配、调用成功、语义正确 |
| 调用形状可绑定 | `inspect.signature()` / `bind()` | 类型、函数体、返回和副作用 |
| 公共合同成立 | 官方文档、项目合同、版本声明 | 当前实现一定无缺陷 |
| 当前样例行为 | 最小实验 | 所有输入、版本和实现都相同 |

`hasattr(obj, name)` 不是静态存在性查询。它会执行一次真实属性访问：

- property、descriptor、`__getattr__()` 和自定义 `__getattribute__()` 都可能运行；
- 整条访问链最终抛出 `AttributeError` 时，它返回 `False`；
- 这个 `AttributeError` 也可能来自 property/descriptor 内部缺陷，所以 `False` 不能
  独立证明“属性本来就不存在”；
- 其它异常通常仍会传播。

`inspect.getattr_static()` 会尽量绕过常规动态属性解析，适合观察存储的 descriptor
或原始成员，但它返回的可能正是 property/descriptor 对象，而不是普通访问结果。
它不能发现所有动态名称，也不是任意恶意对象的权限沙箱。

本章你对：

```python
if "export" in dir(plugin):
    plugin.export("result.json")
```

给出的六类质疑是准确的：可访问性、可调用性、参数合同、公共性、版本范围和副作用
都未被证明。需要保留的两项精修是：

1. 准确协议名是 `__dir__`，不是 Markdown 显示中丢失下划线的 `**dir**`。
2. `Protocol` / ABC 可以帮助表达结构或抽象要求，但不会自动完成版本协商、完整运行期
   签名核验、行为语义验证或副作用保证；必要时还要结合能力声明、契约测试和失败策略。

长期锚点：

> `dir()` 给候选名字；属性查找给当前值；签名给对象向 `inspect` 呈现的调用形状；
> 官方文档中明确写出的公开承诺给公开合同证据；实验给当前环境证据。

### 17.4 `help()`、`pydoc`：显示副作用与文本返回

C11 已经压实“可见输出不等于函数返回值”。C15 只把这个模型迁移到文档工具：

```python
buffer = StringIO()

with redirect_stdout(buffer):
    help_result = help(lookup_text)

help_text = buffer.getvalue()
```

这里形成两个不同对象和一项输出效果：

```tex
help_result
    绑定 None。

help_text
    绑定从当前 Python 层 stdout 捕获到的 str。

help(lookup_text)
    在求值过程中组织并显示人读帮助。
```

因此：

```python
print(help(lookup_text))
```

的执行顺序是：内层 `help()` 先显示帮助文本并返回 `None`，外层 `print()` 再把这个
`None` 显示出来。末行 `None` 不是文档正文，也不表示 `help()` 失败。

四个相近入口必须分开：

| 操作 | 主要回答 | 返回边界 |
| --- | --- | --- |
| `obj.__doc__` | 当前对象经属性访问呈现的文档元数据 | 普通模块/函数通常为 `str` 或 `None`；任意对象不保证 |
| `inspect.getdoc(obj)` | 清理缩进、且可能继承而来的人读文档 | 成功时为 `str` 或 `None` |
| `help(obj)` | 向人显示整理后的帮助 | 成功完成时返回 `None` |
| `pydoc.render_doc(obj)` | 生成可继续处理的渲染文本 | 成功完成时返回 `str` |

`pydoc.render_doc()` 返回 `str`，但“返回文本”仍不等于“已经显示文本”，也不等于
“返回结构化 API 元数据”。若要显示，仍需显式 `print(rendered)`；若要可靠提取签名，
不应解析其人读排版，而应使用对应的结构化工具。

不要把标题措辞、空行、缩进、pager、终端控制字符、折行宽度、成员排列或当前版本
的具体展示提升为合同。稳定测试应围绕真正需要的语义，例如返回值是 `None`、文本
非空、包含对象名称或必要说明；不要把整段帮助页逐字符锁死。

还要保留两项工程边界：

1. `redirect_stdout()` 替换当前 Python 进程中的 `sys.stdout` 绑定，不是通用的操作
   系统级输出沙箱，也不保证捕获子进程、底层文件描述符写入或所有并发输出。
2. `help()`、`pydoc` 和 `inspect.getdoc()` 都会调查当前运行对象；面对自定义对象时，
   不能先验认定它们只做静态文本读取。

本节锚点：

> `__doc__` 是对象经属性访问呈现的元数据；成功的 `help()` 调用以显示为主并返回
> `None`，成功的 `pydoc.render_doc()` 调用返回渲染文本，业务调用则按自身合同返回结果。

### 17.5 官方文档、签名、版本与最小实验

面对版本敏感 API，第一步不是猜输出，而是记录谁产生了证据：

```python
environment = {
    "executable": sys.executable,
    "version": tuple(sys.version_info[:3]),
    "implementation": platform.python_implementation(),
}
```

本章的有效环境是仓库 `.venv-py314` 中的 CPython `3.14.5`。裸 `python`、IDE 标签、
旧书年份和搜索摘要都不能代替 `sys.executable`、`sys.version` 与实现名称。

#### 17.5.1 签名描述对象向 `inspect` 呈现的调用形状

```python
signature = inspect.signature(normalize_text)
bound = signature.bind(" hp ", upper=True)
bound.apply_defaults()
```

`inspect.signature()` 成功时可以揭示对象向它呈现的位置参数、仅限位置参数、仅限关键字
参数、默认值、可变参数和当前注解表示。`Signature.bind()` 尝试把一组实参与该签名
建立映射；
`apply_defaults()` 再把未显式提供的默认项补进 `BoundArguments.arguments`。

它们不能证明函数体能成功执行、注解已经被运行期强制、参数值符合业务范围、返回
对象符合注解、不会抛出其它异常、没有副作用或接口属于稳定公共 API。

只有在已经取得 `Signature` 对象后，`signature.bind(...)` 才只是本地参数映射，不会
调用目标函数。对象还可能提供自定义、过期或失真的 `__signature__`，所以绑定成功只
证明实参符合这一个 `Signature` 对象，不保证真实 `__call__` 接受它们。取得签名的
前一步仍可能触发当前对象的 `__wrapped__`、`__signature__`、`__getattribute__` 或
descriptor 逻辑。

真实项目源码启用了：

```python
from __future__ import annotations
```

所以当前 `str(inspect.signature(...))` 可能把注解显示为带引号的字符串形式：

```tex
(content: 'str') -> 'str'
```

这不表示调用者要传入类型名字符串，也不表示 Python 自动执行类型验证；它只是当前
注解求值策略在签名显示层的表现。

#### 17.5.2 官方合同与当前证据互补

完整核对清单是：

```tex
对象类别或返回类型
正式签名
参数语义与默认值
返回对象与协议
异常类型和发生条件
副作用与资源消费
版本增加、变化或废弃信息
实现说明与 implementation detail
示例的适用前提
```

证据职责不能混用：

| 证据 | 可以支持 | 不能自动提升为 |
| --- | --- | --- |
| 官方文档中明确写出的公开承诺 | 公开合同和适用版本范围 | 把示例、伪代码或实现细节全部提升为合同；当前对象的精确身份或零缺陷实现 |
| 当前签名 | 当前对象向 `inspect` 呈现的调用形状 | 真实调用必然接受该形状；完整行为、返回和副作用合同 |
| 当前源码 | 当前实现路径与机制 | 永久稳定的公开 API |
| 当前实验 | 给定环境和输入下的观察 | 所有版本、实现和输入的普遍保证 |

`itertools.batched(..., strict=True)` 在本章只作为版本化证据案例：官方文档说明
`batched()` 加入于 3.12，`strict` 加入于 3.13；当前 3.14.5 最小实验确认不完整尾批
在消费到该边界时抛出 `ValueError`。这个例子不需要重讲 C14 的全部惰性消费模型，
重点是版本声明、异常合同和当前行为如何互证。

`inspect.getsource()` 也可能对内置对象、动态生成对象或缺少源码的环境抛出
`TypeError` / `OSError`。源码可得性不是所有对象的通用保证，更不能替代官方合同。

#### 17.5.3 最小实验验证主张，不验证整个世界

好的最小实验应：

1. 只针对一个具体命题；
2. 使用完整、独立、可运行的最小输入；
3. 记录解释器、实现、版本与关键环境；
4. 保留完整关键输出和异常发生位置；
5. 验证稳定语义，不锁死偶然异常措辞或帮助排版；
6. 写出不能证明的范围和下一最小检查。

可复用记录结构：

```python
claim = {
    "claim": "strict mode rejects an incomplete final batch",
    "source": "official docs + CPython 3.14.5 experiment",
    "observation": "ValueError occurs when the short final batch is requested",
    "cannot_prove": [
        "all Python implementations use the same internal type",
        "the full exception text is a stable interface",
    ],
    "next_minimal_check": "repeat after a version change that affects the API",
}
```

长期规则：官方文档中明确写出的公开承诺提出可依赖的合同，当前对象与最小实验提供
本地证据；发生冲突时先核对对象身份、解释器、版本、包装层和资料版本，而不是凭印象
选一个“看起来更权威”的结果。

### 17.6 只读真实代码走查：授权、白名单、证据账本与证明强度

本章使用真实 `prompt_template_manager` 作为工程背景，但没有让它替代启动模板或扩张
教学范围。正确问题不是“这个项目里还有什么可以运行”，而是：

> 如何在不误触数据库、CLI 或 GUI 的前提下，调查一个真实模块的职责、接口形状、文档缺口和当前行为？

#### 17.6.1 先限定授权，再使用反射

可靠顺序是：

```tex
1. 明确允许读取的项目、文件和函数。
2. 静态阅读模块顶层，判断 import 会执行什么。
3. 建立固定目标白名单，不从 dir() 结果扩张调用范围。
4. 分别读取 README、模块 docstring、函数 docstring、签名和当前源码。
5. 只用合成输入调用已确认的非持久化路径。
6. 添加与风险相称的前后护栏，并写清它们的证明上限。
```

`import module` 会执行模块顶层代码，所以“只是导入定义”不是普遍安全保证。本次可以
在限定证据范围内导入 `prompt_store`，是因为事先检查了当前模块及当前已检查的导入
路径，没有发现数据库连接、初始化、迁移、CRUD、CLI 或 GUI 入口会在该路径执行，
而不是因为 Python 导入天然只读。这个判断只覆盖已检查的当前导入图和环境；环境特定
导入钩子并未被穷尽证明，也不能据此保证任意依赖变化后的安全性。

允许调用的目标被冻结为：

```python
PURE_TARGETS = (
    "resolve_db_path",
    "normalized_content_hash",
    "parse_tags",
    "tags_from_json",
)
```

这里的 `PURE_TARGETS` 是任务范围内“未进入持久化写路径”的白名单简称，不是对每个
函数作数学纯函数证明。尤其 `resolve_db_path()` 可能观察当前目录、用户目录和路径
解析环境；准确说法是“本次审查确认的非持久化路径解析助手”。

#### 17.6.2 多层文档回答不同问题

```tex
项目 README：
    项目用途、用户入口、运行方法和整体边界。

模块 docstring：
    当前模块的大致职责。

函数 docstring：
    当前对象携带的局部人读说明。

inspect.signature()：
    当前对象向 inspect 呈现的调用形状与注解显示。

源码位置与源码内容：
    当前实现如何工作、调用图进入哪里。

合成输入实验：
    当前环境中给定输入的实际行为。
```

四个助手的调查暴露了真实文档缺口：`resolve_db_path()` 有明确 docstring，另外三个
函数没有局部 docstring。`parse_tags()` 当前按首次出现顺序去重并会对序列元素执行
`str()`；`tags_from_json('["documentation", 15, null]')` 当前得到字符串化的 `15`
和 `None`。这些是源码与实验支持的当前实现事实，不能自动宣布为理想或永久公共合同。

#### 17.6.3 前后状态相同只是一项有限观察

```python
before = database_path.exists()
run_selected_helpers()
after = database_path.exists()
assert before == after
```

这段检查只证明两个离散采样时点的 `Path.exists()` 布尔值相同。它不能证明：

```tex
文件字节、大小、mtime 或权限未变
SQLite 逻辑记录、事务、锁或 sidecar 未变
文件没有在中途删除后重建
没有中途修改后恢复
其它进程没有并发写入
路径仍指向同一个文件实体
```

本次“未进入数据库路径”的更强证据来自固定白名单、当前源码检查、合成输入和调用图
没有进入连接/迁移/CRUD；`exists()` 相等只是一项额外低成本护栏。

若比较两个已采样字节序列，直接保存基线字节并比较相等比只比较哈希更直接。相同
SHA-256 仍是极强证据，但存在理论碰撞；无论哈希还是直接字节比较，都只覆盖采样
结果，不能排除采样间修改、并发写入或 TOCTOU。

#### 17.6.4 严格只读、受控写入与权限沙箱必须分开

```tex
严格只读：
    不创建、不删除、不改写；使用已授权源码、纯内存值或确认不存在且绝不创建的合成路径。

受控写入实验：
    明确授权输出位置、产物和清理方式；例如生成本章 JSON 报告。

普通子进程隔离：
    分离解释器状态并可设置超时，但默认仍继承可访问的文件系统和网络能力。

权限沙箱：
    由操作系统或专门隔离机制限制真正可访问的资源。
```

`TemporaryDirectory()` 会真实创建并在退出时删除目录，所以不能一边使用它，一边把
实验称为“严格只读”。临时目录、一次性对象和普通子进程都只能降低污染或耦合，不是
权限沙箱。需要临时工作区时，应明确改称“受控写入实验”并遵守当前删除规则。

Git 观察也必须使用显式允许路径；不能以“只读状态检查”为由宽范围枚举被硬排除的
`tests/`。

#### 17.6.5 正式实践价值与相邻可选工件边界

正式主线的工程价值锚定在 `05_prompt_manager_documentation_walkthrough.py`：先审查导入
路径、冻结四个 helper 白名单、分层读取 README/docstring/签名/源码，再用合成输入和
有限持久化护栏验证明确获准的最小行为。测验 F1 进一步把它整理为带 `claim`、来源、
观察、未证明范围和下一检查的证据报告。

目录中的 `object_diagnostics.py`、两份卡片模板、对象报告、质量门和质量报告只作为
相邻可选工程背景。它们展示了“逐项捕获内省失败”“自动观察与人工合同分开”“内部
报告、JSON 文本、显示和文件字节分层”等设计思路，但未纳入六步正式主线，不作为
主线完成、测验前关卡或 capstone 证据。两个 JSON 文件也是相邻受控写入产物，不是
正式只读走查产生的证明；后续收束不得覆盖、还原、暂存、取消暂存或清理其既有状态。

### 17.7 P3 综合自查与 P4 交接边界

`06_p3_closer_self_check.py` 把六个章节压缩成处理代码时可依次执行的问题：

```tex
C10：哪些表达式求值，哪些语句真正执行，输出与返回怎样分开？
C11：哪些名字或槽位重新绑定，哪些对象原地修改，谁共享引用？
C12：哪个对象接受真值测试，哪些分支和副作用因短路被跳过？
C13：每轮状态怎样变化，循环正常结束、continue、break 还是异常退出？
C14：谁提供 iterator，谁保存位置，哪个消费者推进，尾部还剩什么？
C15：每项结论来自源码、元数据、显示、签名、官方合同还是当前实验？
```

在 `audit_snapshot(records, required_keys)` 中，这条链形成统一解释：

1. 调用创建并返回新的结构化报告，赋值再把 `report` 绑定到它；`print()` 仍只产生
   展示副作用并返回 `None`。
2. 推导式创建新外层容器，但 `enabled_records` 仍保存原记录字典引用；源码没有写入
   输入不等于发生了深拷贝。
3. `record.get("enabled", True)` 和 `record["target"]` 分别发生真值测试；最终
   `if / elif` 只选一个动作，但报告仍可保留其它已计算诊断字段。
4. 每次列表推导式都取得独立列表迭代器；若输入改成一次性 iterator，第一次扫描会
   推进它，即使没有修改源对象内容。
5. 源码可证明控制流和显式写入；签名不能证明元素合同；最小实验只能确认当前输入的
   当前结果。

相邻的 `p3_localization_quality_gate.py` 可以帮助观察这条六问链怎样迁移到本地化问题，
但它只是可选背景，不是正式主线工件或完成证据。它的受控 JSON 写入也不能并入
`05` 的只读边界，更不能因为产物完整就被追认为 capstone。

P4 只保留以下入口问题：

```tex
def 语句执行时创建什么函数对象，名字何时与它绑定？
调用时实参怎样与形参建立临时绑定？
函数体中的名字按什么规则解析？
return 怎样交回对象，返回合同与副作用合同如何划分？
注解为什么不等于 Python 自动执行的运行期类型验证？
```

这些是下一 PART 的坐标，不是 C15 已经教授完成的函数机制。

### 17.8 本阶段你的理解轨迹、问题与修正规则

本章大多数选答题被你主动跳过。根据教学协议，这只是节奏选择，不是掌握不足；每题
都在下一主课前完成最小收束，没有要求补答，也没有扩大必学范围。

#### 17.8.1 docstring 与业务返回

上一题被跳过后保留的必要结论是：

```tex
lookup.__doc__
    来自函数体首条字符串字面量。

lookup("menu.start")
    来自函数业务执行。

普通注释
    不是语句，不会挡住后面的首条 docstring。

赋值后的三引号字符串
    位置已经太晚，只是普通字符串表达式。
```

该边界在 A1 中获得满分，说明 C10 曾出现的 docstring 模型偏差已经稳定修复，不应
继续记成当前弱项。

#### 17.8.2 你对 `dir()` 启发式检查的主动合同审查

你把：

```python
if "export" in dir(plugin):
    plugin.export("result.json")
```

概括为“用过于乐观的启发式检查替代合同验证”，并主动列出六类未经证明的假设：

1. 名称可发现不证明属性可访问；
2. 属性可访问不证明对象可调用；
3. 可调用不证明接受一个位置字符串参数；
4. 没有前导下划线不证明是稳定公共 API；
5. 当前属性存在不证明跨版本兼容；
6. 调用可能失败、修改状态或产生破坏性 I/O 副作用。

这是本章最有价值的主动迁移证据。精修只有三项：

```tex
精修1：
    协议名必须写作 __dir__；**dir** 是 Markdown 转义造成的错误外观。

精修2：
    hasattr() 也执行属性访问，可能触发 property/descriptor/__getattr__，
    还可能把内部误抛的 AttributeError 转成 False。

精修3：
    Protocol / ABC 有助于表达结构或抽象要求，但不自动验证完整签名、版本协商、
    行为语义和副作用；仍需能力声明、运行期核验和契约测试。
```

#### 17.8.3 `help()` 的嵌套输出题

你选择跳过：

```python
print(help(lookup_text))
```

最小收束是“内层先显示帮助，返回 `None`，外层再显示 `None`”。C1 中对
`help()`、`redirect_stdout()`、`pydoc.render_doc()` 和业务返回的全部判断正确，
说明“输出效果 vs 返回对象”已经从 C11 稳定迁移到文档工具。

#### 17.8.4 `batched(strict=True)` 的惰性异常题

你选择跳过后的最小收束是：

```tex
created
('A', 'B')
('C', 'D')
ValueError
```

第四个 `print()` 在求值实参 `next(batches)` 时抛错，所以外层 `print()` 尚未开始。
D2 获得满分，并能继续说明已消费项、未完成绑定和不回滚，说明 C14 的消费状态模型
已经稳定迁移到版本化 API 核验。

#### 17.8.5 `before == after` 的证明范围

你跳过的只读走查题被收束为：两个 `Path.exists()` 采样结果相同，只能证明两次布尔
观察相同，不能证明内容、事务、元数据或中间状态未变。F1 把这条思路扩展到了哈希、
sidecar、并发和 TOCTOU，但在“严格只读”和证明强度上仍出现一次精度偏差，已在
下一节单独修复。

#### 17.8.6 重复错误与已经修复的问题要分层记录

历史上需要长期警惕的模式：

```tex
相等 == vs 身份 is
对象本体 vs repr()/输出显示
新外层对象 vs 深拷贝
部分消费后停止 vs 已耗尽
内部报告对象 vs JSON 文本 vs 展示 vs 文件字节
```

其中前四项在 C15 测验中表现稳定：E1 正确说明浅层共享，E2 精确追踪异常路径和
迭代器位置，也没有把相等与身份混用。它们应作为长期检查表保留，但不能误写成
本章反复犯错。

真正再次出现的轻微迁移偏差是最后一项：F1 的 `json.dumps()` 被放在“人读显示”
语境中，却没有显式 `print()`。本章新增的一次性精修则是运行期内省安全、临时目录
与严格只读、哈希证明强度及字符串化注解显示；这些不是同一错误的多次重复。

### 17.9 阶段测验暴露的薄弱处与修正规则

C15 阶段测验建议得分为 `98 / 100`，覆盖 `11 / 11` 题：

| 分区 | 主题 | 得分 |
| --- | --- | ---: |
| A | 文档层级与证据来源 | 18 / 18 |
| B | `dir()`、属性访问与合同边界 | 17.5 / 18 |
| C | `help()`、`pydoc` 与官方资料 | 20 / 20 |
| D | 签名、版本与最小实验 | 16 / 16 |
| E | C10-C15 综合代码阅读 | 18 / 18 |
| F | 只读工程调查与 P4 交接 | 8.5 / 10 |
| **总分** |  | **98 / 100** |

#### 17.9.1 B2：知道有风险，但没有展开内省的执行入口（扣 0.5 分）

原答案已经知道普通内省不是安全沙箱，但没有显式说明：

```tex
inspect.getdoc()
    可能读取 __doc__。

inspect.signature()
    可能读取 __wrapped__、__signature__ 等属性。

这些属性读取
    可能触发自定义 __getattribute__、descriptor 或包装器逻辑。
```

精确修复：

1. `inspect.getattr_static()` 尽量绕开常规动态解析，但返回的可能是原始 descriptor，
   也不是安全沙箱。
2. `inspect.getdoc()` 和 `inspect.signature()` 对任意自定义对象都不能先验视为纯静态
   读取。
3. 只有取得普通 `Signature` 对象后，`signature.bind(...)` 才只做本地参数映射，
   不调用目标。
4. 普通子进程、临时目录和一次性实例只降低污染，不提供文件、网络或权限隔离。

长期规则：

> 反射与内省本身也是运行期行为；在调用前不仅审查目标函数，还要审查调查工具会触发哪些协议。

#### 17.9.2 F1：工程证明边界仍需收紧（扣 1.5 分）

白名单与风险顺序：`2 / 3`。

```tex
偏差：
    使用 TemporaryDirectory()，同时把方案称为严格只读。

修复：
    创建和清理临时目录都是真实写入/删除。
    严格只读使用不创建的合成路径或纯内存 helper；
    需要临时工作区时改称受控写入实验，并另行确认授权与清理边界。

补充：
    Git 状态只检查明确允许路径，不能宽范围枚举 tests/。
```

结构化报告：`2.75 / 3`。

```python
rendered = json.dumps(report, ensure_ascii=False, indent=2)
print(rendered)
```

`json.dumps()` 返回 JSON 文本 `str`，第二行 `print()` 才产生人读显示副作用。

持久化证明：`1.75 / 2`。

```tex
相同 SHA-256：
    是极强一致性证据，但存在理论碰撞，只覆盖采样结果。

直接字节相等：
    可严格比较两份已采样字节序列，但仍不能排除采样间修改、并发写入或 TOCTOU。
```

P4 交接：`2 / 2`。问题覆盖函数对象、参数绑定、名字解析、返回/副作用和注解，且
没有提前系统教学。

#### 17.9.3 不扣分但必须保留的精度补充

1. `hasattr()` 可能把 property/descriptor 内部缺陷抛出的 `AttributeError` 也转成
   `False`，所以 `False` 不能独立证明属性不存在。
2. CPython 3.14.5 在本次 `batched` 构造时调用上游 `iter()`、尚未请求元素，这是
   当前实现观察，不应提升为所有实现合同。
3. `from __future__ import annotations` 使当前签名显示字符串化注解；无引号写法只能
   作为语义化转写，不能标作 `str(signature)` 的精确显示。
4. E2 题干把 `KeyError` 放在一个并未访问 `record["key"]` 的推导式中。你主动拒绝
   错误前提，定位到后续集合推导式，并按真实控制流说明消费状态；这是能力证据，不扣分。

#### 17.9.4 测验确认的稳定能力

```tex
1. 能准确区分源码、AST、对象元数据、工具显示、业务返回、官方合同和当前观察。
2. 能把 dir()、help()/pydoc、签名、官方资料与最小实验组织成有限调查链。
3. 能把对象、绑定、真值、分支、循环退出和迭代消费迁移到真实 API 审查。
4. 能发现题干与实际代码不一致，并以源码和运行路径为准。
5. 能设计白名单、结构化 claim、环境记录、持久化 guard 和下一最小检查。
```

审批后验证器确认 `6` 个分区、`11` 道题和 `58` 个可编译 Python 代码块结构有效。
最终能力判断为：中级入门前段已经稳固，能够用对象、控制流和证据分层独立审查
小型 Python 数据流程与 API 合同。

### 17.10 工程应知应会、习惯、禁忌和技巧清单

证据与合同：

```tex
1. 调查前先写清具体主张；“这个 API 靠谱吗”过于宽泛，无法设计最小验证。
2. 每项结论标记来源：源码、元数据、显示、签名、官方合同或当前实验。
3. 官方文档中的对象类别/返回类型不等于当前导入对象的精确身份。
4. 当前源码解释当前实现，不自动构成永久公开合同。
5. 当前实验只覆盖记录的环境、对象、输入和执行路径。
6. 先记录 sys.executable、Python 版本和实现，再比较旧书或版本敏感 API。
7. 合同至少拆分：类型、调用形状、参数语义、返回、异常、副作用、版本、实现说明。
8. 帮助页示例是理解入口，不要把示例输入输出提升为全部合同。
9. 验证稳定语义，不锁死帮助排版、异常全文、内部类型名和 repr 偶然细节。
10. 结论必须带 cannot_prove 和 next_minimal_check，避免把有限观察写成绝对保证。
```

名称发现与运行期内省：

```tex
11. dir() 返回候选名称字符串，不返回已经验证的属性对象。
12. 自定义 __dir__() 可以虚构名称；动态 __getattr__() 可以提供未列出的名称。
13. name in dir(obj) 既不充分证明可访问，也不必要地覆盖所有可访问属性。
14. getattr()/hasattr() 会执行属性协议；property、descriptor 和动态查找都可能运行。
15. hasattr() 只吞掉最终 AttributeError；其它异常通常传播。
16. hasattr() 为 False 也可能是属性内部误抛 AttributeError，不是绝对不存在证明。
17. callable() 只提供可调用线索，不证明参数、返回、异常、副作用或公共性。
18. inspect.getattr_static() 观察存储成员，不等同于普通访问结果，也不是权限沙箱。
19. inspect.signature() 给对象向它呈现的调用形状，不保证与真实调用永久一致。
20. Signature.bind() 只验证实参与该 Signature 的映射，不执行函数体或注解检查。
21. Protocol / ABC 不自动验证完整运行期签名、版本兼容和行为语义。
22. 前导下划线是命名惯例；没有下划线不是稳定公共 API 的证明。
```

文档显示与结构化数据：

```tex
23. __doc__ 是经属性访问呈现的对象元数据；对任意对象不保证只得到 str 或 None。
24. inspect.getdoc() 成功时返回清理后文本或 None，还可能继承文档；它不返回被调查对象。
25. help() 成功时显示人读帮助并返回 None。
26. print(help(obj)) 的末行 None 来自外层 print()，不是文档内容。
27. pydoc.render_doc() 成功时返回人读 str，但不自动显示，也不是结构化合同对象。
28. 内部 dict/list、JSON str、stdout 显示和文件字节必须分别命名。
29. json.dumps() 负责序列化并返回 str；print() 或写入函数才产生外部效果。
30. 需要程序化签名或成员信息时使用对应结构化工具，不解析 help() 排版。
```

真实项目、安全与持久化：

```tex
31. import 会执行代码；导入前检查目标模块、相关依赖和导入钩子，不能把“只导入定义”当保证。
32. 真实代码调查先冻结授权范围和白名单，不因 dir() 发现新名称就扩张调用目标。
33. 只用合成输入调查已确认路径，不把真实业务数据带入教学探针。
34. “未显式 open()”不等于无副作用；还要检查被调函数、导入和协议方法。
35. Path 对象只描述路径；它不是打开的文件对象，也不是 sqlite3.Connection。
36. before == after 只证明所采样字段相等；字段外状态和采样间变化仍未证明。
37. SHA-256 相同是强证据，不是无碰撞、覆盖整个时间窗口的逻辑绝对证明。
38. 严格只读不能创建/删除 TemporaryDirectory；需要工作区时改称受控写入实验。
39. 普通子进程可隔离进程状态并设置超时，但默认不是文件系统或网络权限沙箱。
40. Git 检查使用明确允许路径；tests/ 是硬排除，不能借只读检查宽范围枚举。
41. SQLite 走查同时关注主文件、-wal、-shm、-journal 等可能 sidecar，但仍按任务范围取证。
42. 受控输出文件要明确格式、编码、位置和是否覆盖；不要把它混入只读证明。
```

P3 综合代码审查：

```tex
43. 先区分表达式求值、语句执行、返回对象和显示副作用。
44. 再追踪名字重新绑定、对象原地修改和浅层共享引用。
45. 对条件写清实际接受真值测试的对象，以及短路跳过了哪些求值或副作用。
46. 对循环写清状态变化、退出原因和异常前已发生的动作。
47. 对迭代管道写清 iterable、iterator、消费者、当前位置、尾部和是否可达。
48. “源码没有显式写入”与“任意输入绝无状态变化”不是同一命题。
49. 新外层列表或排序视图不等于深拷贝内部可变对象。
50. 结构化 report 保留程序可处理的事实；print/log/JSON 文件属于外层展示与持久化。
51. 题干、注释和代码冲突时，以真实源码控制流和可验证行为为准，并显式指出矛盾。
52. P4 交接只列函数对象、参数绑定、名字解析、return 和注解问题，不提前系统作答。
```

最常见禁忌可压缩为十条：

```tex
1. 不把 dir() 当成完整 API 合同。
2. 不把 hasattr() 当成无副作用静态检查。
3. 不把 callable() 当成调用一定成功。
4. 不把签名或注解当成自动业务验证。
5. 不把 help() 显示说成返回文档字符串。
6. 不解析偶然的人读排版来建立机器合同。
7. 不把当前实现观察无版本地外推。
8. 不把临时目录或普通子进程说成严格只读/权限沙箱。
9. 不把 JSON 文本、显示输出和文件字节混成同一对象。
10. 不把前后采样相同说成整个窗口绝无变化。
```

### 17.11 阶段精髓小结

```tex
1. C15 的核心不是查到一段说明，而是知道每项结论由哪层证据支持。
2. docstring 由语法位置决定；`__doc__` 是运行对象呈现的元数据，不是完整源码或合同。
3. 名称发现、属性访问、可调用性、呈现的 `Signature` 与公开合同是五道不同关卡。
4. 成功的 `help()` 调用以显示为主并返回 `None`；成功的 `render_doc()` 返回 `str`
   而不自动显示；人读排版不是机器接口。
5. 官方文档中明确写出的公开承诺、当前签名、当前源码和当前实验各有适用范围，
   不能互相越权替代。
6. `import` 和运行期内省都可能执行代码；真实项目调查先冻结授权、审查导入路径、
   固定白名单，再用合成输入做最小验证。
7. 严格只读、受控写入、普通子进程隔离和权限沙箱是四种不同边界。
8. 内部对象、JSON `str`、显示输出和文件字节必须分层命名；前后采样与哈希都只提供
   有限证据，不能证明整个时间窗口绝无变化。
9. C10-C15 可统一为：求值/执行 -> 绑定/修改 -> 真值/分支 -> 循环退出
   -> iterator 位置 -> 证据来源；能限定证明强度，才形成可迁移的代码审查能力。
10. C15 已完成主线、测验审批、画像和阶段末笔记；下一关卡是 P3 的
    `final_closeout`，尚未开始 P4。
```
