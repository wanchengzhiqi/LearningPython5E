# C19 高级函数主题阶段测验

<!-- quiz-validator: total=100 -->

- 章节：`P4_Functions_and_Generators / C19_Advanced_Function_Topics`。
- 章节角色：`normal`；总分：100 分；共 6 个分区、11 题。
- 命题日期：2026-09-20；运行语义：CPython 3.14.5。
- 唯一课程范围入口：[C19 启动模板](../../../docs/C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md)。
- 状态边界：正式主线已结束，当前进行阶段测验；本卷尚未作答、未批改，不表示章节已收束。
- 前置关卡：启动模板未安排测验前 capstone，也没有后续明确排期变更；路线图中的规则注册表／转换管线只是候选，不算待完成项目。
- 命题只读参考了学习画像；未更新画像、阶段笔记或其他长期记录。

## 作答约定

1. 优先先推理，再在当前虚拟环境中核验；可查本章学习文件。请区分“预测”“运行观察”和“修正后的解释”，不用隐去自己的推理变化。
2. 每题在对应的 `answer:start` 与 `answer:end` 之间作答，保留题号、分值和标记。可以扩展作答区，不必沿用固定篇幅。
3. 各题代码独立运行；同一题内默认按给定顺序执行。未要求精确异常消息时，只写异常类型、发生阶段与关键状态。
4. 引用图箭头从名字／容器槽位／环境绑定指向对象；区分对象身份、内容相等、修改和重绑。不要用偶然字符串身份、地址或内部 cell 表示来论证。
5. 编码题用普通函数、容器、循环、条件、已学异常处理与必要的基础注解即可。允许清晰的等价实现，不以最短代码为目标。
6. 全卷只使用合成内存数据。不得读写真实资源、数据库、网络、GUI、CLI 或 `tests/`；F1 是纸面小型接口题，不是新增 capstone。
7. 评分以各小问标明分值为准：结果、推理及边界分别给分；只给正确输出不能代替明确要求的解释。
8. 未作答前不提供标准答案，不预填得分，也不据本卷生成行为更新能力判断。

## 冻结命题蓝图

| 分区 | 题号与分值 | 考察结果 | 题型 | 小计 |
| --- | --- | --- | --- | --- |
| A | A1：6；A2：6 | 一等函数与高阶组合；证据不能越界 | 概念解释、判断纠偏 | 12 |
| B | B1：8；B2：10 | 引用保存／替换／调用；管线与回调异常 | 输出预测、时间线阅读 | 18 |
| C | C1：12；C2：12 | 环境隔离与对象共享；晚绑定的两种核心修复 | 对象图、状态追踪、局部改写 | 24 |
| D | D1：10；D2：6 | 递归基线、进展、局部绑定、返回链 | 轨迹预测、错误定位、循环比较 | 16 |
| E | E1：6；E2：8 | lambda 表达式与返回；注解与实际检查 | 输出预测、证据审查 | 14 |
| F | F1：16 | 参数、返回、异常、副作用和验证合同 | 小型接口实现、聚焦验证 | 16 |
| 合计 | 11 题 | C19 必学核心与必要精度边界 | — | 100 |

难度依据：既有函数对象、参数和作用域基础较稳；本章已能准确追踪闭包别名、异常前副作用、递归返回及调用方绑定。因此增加跨时点比较和少量组合变化，不重复单纯背定义。

排除范围：不考生成器／yield、性能基准、系统装饰器、泛型／ParamSpec／Protocol、完整静态类型工程、Tkinter／OOP、模块打包或异常机制专题。partial、cell／__closure__、递归深度限额的操作均不是本卷必考项；Python 3.14 注解延迟求值内部机制不另设考题。

代码与风格锚点：本目录 README 和正式编号 01—06 实验。其他同主题文件不构成追加考点来源。

## A—F 分区试题

<!-- quiz-section: id=A score=12 -->
## A. 概念解释与证据边界（12 分）

本区重在给出准确的概念边界。每个判断都要说明依据；可以用短例子或引用箭头，不需要写长篇定义。

<!-- quiz-question: id=A1 score=6 -->
### A1. 行为的传递与组合（6 分）

一个本地化工具允许调用者替换文本处理行为。阅读下面的独立片段：

~~~python
def strip_text(text):
    return text.strip()


def choose_rule(registry, name):
    return registry[name]


registry = {"strip": strip_text}
selected = choose_rule(registry, "strip")
value = selected(" Menu.Start ")
~~~

1. **对象与时点（2 分）**：分别说明 `strip_text`、`registry["strip"]`、`selected` 和最后的 `value` 在这段代码中代表什么。指出哪一条表达式真正开始执行 `strip_text` 的函数体；不要把字典取值描述成复制函数或移除原项。
2. **高阶函数（2 分）**：`choose_rule` 是否属于高阶函数？它没有在函数体里调用处理规则，是否影响你的判断？再说明“接受 callable”与“返回 callable”是否必须同时满足。
3. **可组合性（2 分）**：准备把 `strip_text` 和一个“给键加语言前缀”的函数串联。除了两者都能接收并返回字符串，还应明确哪两项行为合同？说明为什么不能仅凭相同的输入／输出类型就任意交换执行顺序。

作答重点：名字与对象、选择行为与执行行为、组合规则的实际合同。最后一问可自拟一组简短的转换说明，无需实现完整管线。

#### A1 作答区

<!-- answer:start -->

### 1. 对象与时点

答：

先按“名字／容器槽位 → 对象”的方式区分：

```text
strip_text                    → 函数对象 F_strip
registry                      → 字典对象 R
registry["strip"]             → 函数对象 F_strip
selected                      → 函数对象 F_strip
```

`strip_text` 是模块级名字，绑定到执行 `def strip_text(...)` 时创建的函数对象。  
`registry["strip"]` 是字典槽位，保存的是**同一个函数对象的引用**；把函数放进字典既不会复制函数，也不会执行函数体。

执行：

```python
selected = choose_rule(registry, "strip")
```

时，`choose_rule` 本次调用读取 `registry[name]`，把该槽位引用的函数对象作为自己的返回值交还调用方；随后调用方名字 `selected` 绑定到这个返回对象。因此 `selected` 与 `registry["strip"]` 都引用 F_strip。

真正开始执行 `strip_text` 函数体的是：

```python
selected(" Menu.Start ")
```

而不是字典取值或 `choose_rule` 的返回动作。该调用建立 `strip_text` 本次局部形参：

```text
text → 字符串对象 " Menu.Start "
```

函数体调用 `strip()` 后返回内容为 `"Menu.Start"` 的字符串对象，随后：

```python
value = selected(" Menu.Start ")
```

中的调用方名字 `value` 才绑定到这个返回对象。

所以最后可概括为：

```text
strip_text / registry["strip"] / selected
                ↓
            同一函数对象

value
  ↓
字符串对象 "Menu.Start"
```

### 2. 高阶函数

答：

`choose_rule` **属于高阶函数**。

原因是它的返回值可能是一个 callable；本题实际返回的就是 `registry[name]` 中保存的 `strip_text` 函数对象。高阶函数的常见判定条件是：

- 接受 callable 作为参数；**或**
- 返回 callable。

二者满足任意一个就可以构成高阶函数，并不要求必须同时满足。

因此：

```python
def choose_rule(registry, name):
    return registry[name]
```

虽然没有在函数体中执行：

```python
registry[name](...)
```

仍然是在**选择并返回行为对象**。  
“选择 callable”与“执行 callable”是两个不同阶段；没有立即调用规则，不影响其高阶函数性质。

### 3. 可组合性

答：

除了“二者都能接收字符串并返回字符串”这一表面类型形状，还至少应明确：

1. **异常合同**：哪些输入可能导致异常、异常是否原样传播、是否有业务层错误转换；
2. **副作用／状态修改合同**：函数是否修改外部列表、日志、共享配置或其他状态。

仅凭相同输入／输出类型不能推出两个步骤可以随意换序，因为转换语义本身通常**不满足交换律**。

例如设：

```text
strip_text:
    " Menu.Start " → "Menu.Start"

add_prefix:
    text → "en:" + text
```

若先 strip：

```text
" Menu.Start "
    ↓ strip
"Menu.Start"
    ↓ prefix
"en:Menu.Start"
```

若先 prefix：

```text
" Menu.Start "
    ↓ prefix
"en: Menu.Start "
    ↓ strip
"en: Menu.Start"
```

结果不同。即使两步在类型上都属于：

```text
str → str
```

也不能由类型形状单独证明执行顺序可交换；还必须看真实转换语义、异常和副作用合同。

<!-- answer:end -->

<!-- quiz-question: id=A2 score=6 -->
### A2. 声明、检查与结论强度（6 分）

某次代码审查中出现以下三条结论。逐条判断结论是否能由所述证据推出；若不能，给出更严格的替代表述，并补充一种仍需观察或验证的事实。**每条 2 分：证据边界 1 分，补充证据／反例 1 分。**

1. “注册表已经成功保存 `handler`，所以对应处理工作已经执行；以后调用这个名称也必然成功。”
2. “`callable(handler)` 为真，`inspect.signature(handler).bind("menu.start")` 也成功，所以真实调用一定返回正确字符串，而且不会修改外部状态。”
3. “`def apply(text: str) -> str` 的注解可以读取；一次真实运行也返回了字符串，所以运行时已经对所有输入和返回路径实施了字符串类型检查。”

本题仅使用已学的“呈现签名／形状匹配／元数据／真实调用／业务合同”分层，不要求解释 `inspect` 的内部实现，也不要求安装或运行静态类型检查工具。明确写出“本次观察支持什么”，避免把一次结果扩大成无条件保证。

#### A2 作答区

<!-- answer:start -->

### 1. “注册成功，所以已经执行且以后必然成功”

答：这个结论**不能推出**。

注册表成功保存 `handler`，最多能支持：

> 某个名字／槽位现在保存了 `handler` 对象的引用；注册动作本身已经正常完成。

它不能证明：

- `handler` 的函数体已经执行；
- 未来分发时一定会真正调用到它；
- 分发器提供的参数与它的签名一定匹配；
- 函数体一定正常返回；
- 返回值满足业务要求；
- 调用没有异常或副作用。

更严格的替代表述应是：

> “注册阶段成功保存了 `handler` 的引用；真正的业务执行要等后续显式调用发生，并且调用成功与否仍取决于调用形状、函数体行为和运行时状态。”

仍需补充观察的一项事实，例如：

```python
result = handler("menu.start")
```

应真实执行一次有代表性的调用，观察它是否正常返回、返回什么、是否产生异常或副作用。即使这一次成功，也只能证明这一个输入／状态下的实际行为，不能推广为所有未来调用必然成功。

### 2. `callable()` + `Signature.bind()` 成功，所以一定正确且无副作用

答：这个结论**不能推出**。

```python
callable(handler)
```

为真，只能支持“该对象具有可调用性质”。

而：

```python
inspect.signature(handler).bind("menu.start")
```

成功，只能支持：

> 这一组已经给出的调用输入，能够按照该 `Signature` 的参数形状完成匹配／绑定描述。

`bind()` 不执行函数体，也不验证：

- annotation 类型是否真实满足；
- 返回值是否为正确字符串；
- 业务内容是否正确；
- 函数体是否抛异常；
- 是否修改外部状态。

更严格的替代表述是：

> “现有证据说明对象可调用，并且一个位置实参 `"menu.start"` 能按呈现签名完成形状匹配；尚未证明真实执行结果和副作用合同。”

还需真实调用并检查结果和状态，例如：

```python
before = events.copy()
result = handler("menu.start")
after = events.copy()
```

再观察：

```python
isinstance(result, str)
before == after
```

等事实。即便这些检查本次通过，也不能无条件证明所有输入、所有外部状态都满足合同。

### 3. 注解可读 + 一次返回字符串，所以运行时对所有路径实施了字符串检查

答：这个结论**不能推出**。

```python
def apply(text: str) -> str:
    ...
```

中的注解属于函数接口元数据／类型意图。Python 普通函数调用机制不会仅因为这些注解就自动：

- 拒绝非字符串实参；
- 把实参转换成字符串；
- 检查每条返回路径是否都返回字符串。

一次真实运行返回了字符串，只能支持：

> 该次具体输入、该次运行状态和该条实际执行路径最终返回了一个字符串对象。

它不能证明其他输入、其他分支也如此，更不能证明 Python 已安装了运行时类型强制。

更严格的替代表述是：

> “函数公开了 `str → str` 的注解意图，而且至少一次真实执行观察到了字符串返回；尚无证据表明所有调用路径都被运行时类型检查。”

仍需补充验证其他代表性路径，例如传入边界字符串、触发不同条件分支，再检查实际返回对象类型；如果业务需要真正的运行时强制，还必须显式实现相应检查，而不能把注解本身当作检查器。

<!-- answer:end -->

<!-- quiz-section: id=B score=18 -->
## B. 函数对象、分派与控制流（18 分）

本区代码均只修改题内列表。关注保存的函数引用和当前字典槽位可能在不同时间指向不同对象；异常出现时，应追踪最后成功的绑定，而不是只列异常名称。

<!-- quiz-question: id=B1 score=8 -->
### B1. 保存引用与稍后分派（8 分）

独立运行以下代码：

~~~python
events = []


def trim(text):
    events.append("trim")
    return text.strip()


def upper(text):
    events.append("upper")
    return text.upper()


def select_rule(registry, name):
    events.append("select")
    return registry[name]


registry = {"clean": trim}
selected = select_rule(registry, "clean")
alias = selected
registry["clean"] = upper

print("P1", selected is alias, selected is registry["clean"], events)
first = selected(" Menu.Start ")
second = registry["clean"]("Menu.Quit")
print("P2", first, second)
print("P3", events)
~~~

1. **输出预测（3 分）**：写出 P1、P2、P3 三行输出，每行 1 分。
2. **时点与引用（3 分）**：以“`registry["clean"] = upper` 已完成、尚未执行 P1”为时点，画出或文字列出 `selected`、`alias`、`trim`、`upper` 与字典槽位的指向；说明选择函数返回后，不能再把它的局部形参与调用者所有名字机械地画成始终共存。
3. **局部变化（2 分）**：重新从题首运行，只把 `alias = selected` 改成 `alias = selected(" X ")`。P1 中的两个身份判断、P1 的事件列表分别怎样变化？说明变化来自实参／调用执行，还是来自名字赋值本身。

字符串比较只要求内容；不要依赖字符串驻留或地址。第三问是独立改动，不与原运行结果累积。

#### B1 作答区

<!-- answer:start -->

### 1. 输出预测

答：

原程序依次输出：

```text
P1 True False ['select']
P2 Menu.Start MENU.QUIT
P3 ['select', 'trim', 'upper']
```

推理如下：

1. `select_rule(registry, "clean")` 先执行，向 `events` 追加 `"select"`，返回当时字典槽位中的 `trim` 函数对象。
2. `selected` 与 `alias` 都保存这个 `trim` 函数对象的引用。
3. `registry["clean"] = upper` 只把字典槽位重新绑定到 `upper` 函数对象，不会改写 `selected` 或 `alias`。
4. 所以 P1 时：
   - `selected is alias` 为 `True`；
   - `selected is registry["clean"]` 为 `False`；
   - `events == ["select"]`。
5. `selected(" Menu.Start ")` 实际调用旧引用 `trim`，追加 `"trim"`，返回 `"Menu.Start"`。
6. `registry["clean"]("Menu.Quit")` 通过当前字典槽位调用 `upper`，追加 `"upper"`，返回 `"MENU.QUIT"`。

### 2. 时点与引用关系

答：

在：

```python
registry["clean"] = upper
```

已经完成、但尚未执行 P1 时，可画成：

```text
名字 trim --------------------------┐
                                   │
名字 selected ---------------------┼──→ 函数对象 F_trim
                                   │
名字 alias ------------------------┘

名字 upper ----------------------------→ 函数对象 F_upper

名字 registry → 字典对象 R
R["clean"] --------------------------------→ 函数对象 F_upper
```

此时：

```text
events → ["select"]
```

字典槽位已经改指 `upper`，但先前从槽位取出的函数引用不会被追溯修改。

`select_rule` 那一次调用中的局部参数：

```text
registry
name
```

只属于那次已经结束的调用。函数正常返回后，不应把这些局部 parameter binding 机械地画成“永久和调用方名字一起继续存在”。真正持续存在的是仍被其他位置引用的对象，例如字典 R、函数对象 F_trim/F_upper 等。

### 3. 把 `alias = selected` 改为 `alias = selected(" X ")`

答：

这一小问从题首独立运行。

新的执行顺序中：

```python
alias = selected(" X ")
```

会先求值右侧调用。`selected` 此时仍引用 `trim`，所以调用：

```python
trim(" X ")
```

向 `events` 追加 `"trim"`，并返回字符串 `"X"`；随后调用方名字 `alias` 绑定到该字符串，而不是函数对象。

因此 P1 两个身份判断为：

```text
selected is alias                → False
selected is registry["clean"]    → False
```

P1 的事件列表为：

```text
['select', 'trim']
```

所以 P1 为：

```text
P1 False False ['select', 'trim']
```

变化来自**赋值右侧发生了函数调用**；普通赋值动作本身只是把 `alias` 绑定到右侧求值得到的返回对象，并不会自行执行函数体。

<!-- answer:end -->

<!-- quiz-question: id=B2 score=10 -->
### B2. 转换完成但调用未返回（10 分）

以下代码对两个输入依次执行完整尝试；每次开始都会清空事件列表并重新令 `result = "old"`：

~~~python
events = []


def strip_text(text):
    events.append(("strip", text))
    return text.strip()


def normalize_nonempty(text):
    events.append(("check", text))
    if not text:
        raise ValueError("empty key")
    return text.casefold()


def notify(value):
    events.append(("notify", value))
    raise RuntimeError("notification failed")


def pipeline(text):
    current = text
    for rule in (strip_text, normalize_nonempty):
        current = rule(current)
    notify(current)
    return current


for raw in (" Menu.Start ", "   "):
    events.clear()
    result = "old"
    try:
        result = pipeline(raw)
    except (ValueError, RuntimeError) as error:
        print(type(error).__name__)
    print(result, events)
~~~

1. **完整输出（4 分）**：按顺序写出四行输出。每次尝试的异常行与状态行合计 2 分。
2. **两层控制流（4 分）**：分别指出两次尝试中 `pipeline` 的局部 `current` 最后成功绑定的值、是否进入 `notify` 的函数体、调用方 `result` 的绑定是否完成。说明为什么已经产生的事件不会随异常自动消失。
3. **回调返回合同（2 分）**：只把 `notify` 的最后一句改为 `return None`，然后从干净状态仅执行第一个输入。此时调用方得到什么？为什么不能把“回调返回 None”直接等同于“整个 pipeline 返回 None”？

本题不要求吞掉异常、重试或建立事务机制。注意区分“转换步骤都成功”“回调也正常返回”和“外层调用已经正常返回”三个事实。

#### B2 作答区

<!-- answer:start -->

### 1. 完整输出

答：

四行输出依次是：

```text
RuntimeError
old [('strip', ' Menu.Start '), ('check', 'Menu.Start'), ('notify', 'menu.start')]
ValueError
old [('strip', '   '), ('check', '')]
```

第一轮 `" Menu.Start "`：

```text
strip_text
    → current = "Menu.Start"

normalize_nonempty
    → current = "menu.start"

notify("menu.start")
    → 先追加 ("notify", "menu.start")
    → 再抛 RuntimeError
```

所以 `pipeline(...)` 没有正常返回，调用方：

```python
result = pipeline(raw)
```

的左侧赋值没有完成，`result` 仍是 `"old"`。

第二轮 `"   "`：

```text
strip_text
    → current = ""

normalize_nonempty("")
    → 先追加 ("check", "")
    → 再抛 ValueError
```

因此没有进入 `notify`。

### 2. 两层控制流

答：

#### 第一次尝试：`raw == " Menu.Start "`

`pipeline` 的局部 `current` 最后成功绑定到：

```text
"menu.start"
```

过程为：

```text
初始 current → " Menu.Start "
strip 正常返回        → current 重绑 "Menu.Start"
normalize 正常返回    → current 重绑 "menu.start"
```

随后确实进入 `notify` 的函数体；它已经执行：

```python
events.append(("notify", value))
```

然后才抛出 `RuntimeError`。

因此：

- 两条转换规则都已完成；
- `notify` 已进入并产生副作用；
- `pipeline` 没有执行到 `return current`；
- 调用方 `result = pipeline(raw)` 的赋值没有完成；
- 调用方 `result` 保持 `"old"`。

#### 第二次尝试：`raw == "   "`

`strip_text` 正常返回空字符串，所以 `pipeline` 的 `current` 最后成功绑定为：

```text
""
```

接着 `normalize_nonempty("")` 已进入函数体并追加：

```text
("check", "")
```

然后在：

```python
raise ValueError("empty key")
```

处失败。

因此：

- `current` 仍保持上一条成功赋值得到的 `""`；
- `normalize_nonempty` 没有正常返回；
- `notify` 根本没有进入；
- 调用方结果赋值仍未完成；
- `result` 保持 `"old"`。

两次尝试中已经发生的 `events.append(...)` 都属于普通列表原地修改。异常只中断后续控制流，没有事务回滚语义，所以这些事件不会自动消失。

### 3. 把 `notify` 改为正常 `return None`

答：

只从干净状态执行第一个输入，并把：

```python
raise RuntimeError(...)
```

改成：

```python
return None
```

后，两个转换规则都会正常完成，`notify(current)` 也正常返回 `None`。

但是 `pipeline` 的代码是：

```python
notify(current)
return current
```

它**没有**写：

```python
current = notify(current)
```

所以 callback 的返回对象没有参与转换结果。

最终：

```python
pipeline(" Menu.Start ")
```

正常返回：

```text
"menu.start"
```

调用方 `result` 绑定到 `"menu.start"`。

不能把“回调返回 `None`”等同于“整个 pipeline 返回 `None`”，因为最终返回值由 `pipeline` 自己的：

```python
return current
```

决定；callback 的正常返回值在这里被忽略。

<!-- answer:end -->

<!-- quiz-section: id=C score=24 -->
## C. 闭包环境、共享与晚绑定（24 分）

本区把“不同调用的绑定环境”与“绑定所指向的可变对象”分开考察。代码中的 tuple 仅用于保存可读的当时内容；不要求观察 __closure__ 或 cell。

<!-- quiz-question: id=C1 score=12 -->
### C1. 独立绑定与共享列表（12 分）

两个工厂调用显式接收同一个列表。请先按代码追踪，不预设“工厂调用不同，所以一切状态都隔离”。

~~~python
def make_tracker(label, history):
    count = 0

    def record(key):
        nonlocal count
        count += 1
        history.append((label, count, key))
        return count

    def read():
        return count, tuple(history)

    def replace(new_history):
        nonlocal history
        history = new_history

    return record, read, replace


shared = []
record_a, read_a, replace_a = make_tracker("A", shared)
record_b, read_b, replace_b = make_tracker("B", shared)

record_a("start")
saved_read = read_a()
old = shared
replace_a([])
record_b("quit")
record_a("audio")
shared = ["detached"]

print("C1", read_a())
print("C2", read_b())
print("C3", saved_read)
print("C4", old, shared)
~~~

1. **状态输出（4 分）**：写出 C1—C4 四行输出，每行 1 分。
2. **引用关系（4 分）**：比较 `replace_a([])` 调用前、以及所有打印开始前这两个时点。分别说明 A 环境的 `history`、B 环境的 `history`、外部 `old` 与外部 `shared` 各指向哪个列表。为列表取 L1/L2 等名字即可；不需要获取函数内部变量或使用内省。
3. **隔离的粒度（4 分）**：解释两个 `count` 为何不合并计数（1 分）；`replace_a` 改变的是哪个绑定、为何不重置计数也不修改旧列表（2 分）；`saved_read` 为何没有跟随后续追加而增长（1 分）。

第三问只需解释本例中的整数和由不可变元素组成的记录 tuple，不可把它推广成“tuple 自动深拷贝任意嵌套对象”。“闭包仍能访问绑定”和“每个闭包拥有一份数据副本”也不是同一个结论。

#### C1 作答区

<!-- answer:start -->

### 1. C1—C4 输出

答：

四行输出为：

```text
C1 (2, (('A', 2, 'audio'),))
C2 (1, (('A', 1, 'start'), ('B', 1, 'quit')))
C3 (1, (('A', 1, 'start'),))
C4 [('A', 1, 'start'), ('B', 1, 'quit')] ['detached']
```

### 2. 两个时点的引用关系

答：

记：

```text
L1 = 最初的 shared 列表
L2 = replace_a([]) 的实参表达式 [] 创建的新列表
L3 = shared = ["detached"] 创建的新列表
```

#### 时点一：`replace_a([])` 调用前

此时已经执行：

```python
record_a("start")
saved_read = read_a()
old = shared
```

所以：

```text
A 环境的 history binding ──┐
B 环境的 history binding ──┼──→ L1
外部 old -------------------┤      [('A', 1, 'start')]
外部 shared ----------------┘
```

同时：

```text
A 环境 count → 1
B 环境 count → 0
```

#### `replace_a([])` 的作用

调用时先创建新列表 L2，本次形参：

```text
new_history → L2
```

`nonlocal history` 让赋值：

```python
history = new_history
```

重绑的是**A 那次工厂调用中的 enclosing `history` binding**：

```text
A history：L1 → L2
```

它既不修改 L1 的内容，也不影响 B 环境中的 `history`。

随后：

```python
record_b("quit")
```

修改 B 仍引用的 L1；

```python
record_a("audio")
```

修改 A 已改指的 L2；

最后：

```python
shared = ["detached"]
```

只把模块名字 `shared` 重绑到 L3。

#### 时点二：所有打印开始前

关系为：

```text
A 环境 history --------------------→ L2
                                      [('A', 2, 'audio')]

B 环境 history --------┐
外部 old --------------┼------------→ L1
                       │              [('A', 1, 'start'),
                       │               ('B', 1, 'quit')]
                       │
外部 shared -----------------------→ L3
                                      ['detached']
```

注意：`old` 继续引用 L1；模块名字 `shared` 的后续重绑不会追溯改变 `old`。

### 3. 隔离的粒度

答：

#### 两个 `count` 为什么不合并

两次：

```python
make_tracker("A", shared)
make_tracker("B", shared)
```

是两次独立函数调用，各自建立一份自己的局部 `count` binding：

```text
A 环境 count
B 环境 count
```

所以 `record_a` 只通过 A 环境的 `nonlocal count` 重绑 A 的计数；`record_b` 只重绑 B 的计数。二者可以同时引用同一个 history 列表，却不意味着 `count` binding 也共享。

#### `replace_a` 改变什么

```python
replace_a([])
```

只重绑 A 环境的 enclosing `history`：

```text
A history → L1
变为
A history → L2
```

它没有执行：

```python
L1.clear()
```

或其他原地修改，因此旧列表 L1 内容保持不变；也没有触及 A 的 `count` binding，所以计数不会因此归零。

#### `saved_read` 为什么不继续增长

执行：

```python
saved_read = read_a()
```

时，`read_a` 返回：

```python
(count, tuple(history))
```

当时得到的是：

```text
(1, (('A', 1, 'start'),))
```

`tuple(history)` 在该时点建立一个新的 tuple 容器，把当时 history 中的记录对象引用放进去。之后向列表继续 `append`，不会把新元素自动追加进这个已经创建完成的 tuple。

本题记录项本身都是由字符串和整数组成的 tuple，可视为不可变记录，所以后续也没有“内部成员被修改”使旧快照变化的问题。

但不能把这个结论泛化成：

> “`tuple(...)` 会对任意嵌套对象做深拷贝。”

它只创建新的外层 tuple 容器，并不会自动深复制其中所有成员对象。

<!-- answer:end -->

<!-- quiz-question: id=C2 score=12 -->
### C2. 循环函数的两种修复（12 分）

下面的循环位于普通函数内部，`configs` 中的两个字典是不同对象：

~~~python
def build_late(configs):
    rules = []
    for config in configs:
        def label(key):
            return f"{config['locale']}:{key}"
        rules.append(label)
    return rules


configs = [{"locale": "en-US"}, {"locale": "ja-JP"}]
late_rules = build_late(configs)
print([rule("menu.start") for rule in late_rules])
print(late_rules[0] is late_rules[1])
~~~

1. **预测与解释（2 分）**：写出两行输出，并说明内部函数读取的是哪次外层调用中的哪个绑定、在什么时候读取。不要把问题归因于两个函数对象相同，也不要归因于 lambda。
2. **两种局部修复（4 分）**：分别实现 `build_defaults(configs)` 与 `build_factories(configs)`（各 2 分），保持返回规则顺序与输入顺序一致：
   - 默认参数版返回的每个规则使用 `label(key, saved_config=...)` 的形式，允许调用者通过第二个位置实参覆盖 `saved_config`。
   - 工厂版在每轮调用一个小工厂，返回的规则只有 `key` 这一个形参。
   - 两个版本都应保存各轮字典引用，不复制字典；不得通过硬编码语言、修改输入或立即执行所有规则规避晚绑定。
3. **修复后仍有共享对象（4 分）**：在你实现的函数基础上，运行下面的续接片段。写出 Q1—Q4 四行输出，每行 1 分，并用简短的指向关系解释原字典修改与列表槽位替换的不同。解释计入对应输出分，不另加分。
4. **合同差异（2 分）**：解释 Q4 是否永久改变第一条规则保存的默认对象（1 分）；为什么不能说默认参数版与工厂版对外具有完全相同的调用合同（1 分）。

以下片段依赖你在第 2 小问中的实现；从此处的新 `configs` 开始，不累计上一段中的其他状态：

~~~python
configs = [{"locale": "en-US"}, {"locale": "ja-JP"}]
default_rules = build_defaults(configs)
factory_rules = build_factories(configs)
old_config = configs[0]

configs[0]["locale"] = "zh-CN"
print("Q1", default_rules[0]("menu.start"), factory_rules[0]("menu.start"))

configs[0] = {"locale": "fr-FR"}
print("Q2", default_rules[0]("menu.start"), factory_rules[0]("menu.start"))
print("Q3", configs[0] is old_config)
print("Q4", default_rules[0]("menu.quit", {"locale": "ko-KR"}))
~~~

注意：修复“循环共享同一个 config 绑定”，并不等于禁止后来修改该绑定最初引用的字典；题目不要求冻结配置内容。

#### C2 作答区

<!-- answer:start -->

### 1. 原始晚绑定输出与解释

答：

两行输出是：

```text
['ja-JP:menu.start', 'ja-JP:menu.start']
False
```

`for` 位于一次 `build_late(configs)` 调用内部。该调用中只有一个局部名字／binding：

```text
config
```

循环每轮只是依次重绑它：

```text
第 1 轮：config → 第一个字典 {"locale": "en-US"}
第 2 轮：config → 第二个字典 {"locale": "ja-JP"}
```

每轮执行内部 `def label` 都会创建一个新的函数对象，所以：

```python
late_rules[0] is late_rules[1]
```

为 `False`。

但是两个函数稍后执行：

```python
return f"{config['locale']}:{key}"
```

时，读取的是**同一次外层 `build_late` 调用中的同一个 enclosing `config` binding**。所有规则都在外层返回后才调用；此时该 binding 最后的对象是第二个字典，所以两条规则都读到 `"ja-JP"`。

这与 `lambda` 无关；普通嵌套 `def` 同样会发生晚绑定。

### 2. 两种局部修复

#### 默认参数版

```python
def build_defaults(configs):
    rules = []

    for config in configs:
        def label(key, saved_config=config):
            return f"{saved_config['locale']}:{key}"

        rules.append(label)

    return rules
```

每轮真正执行内部 `def label(...)` 时，默认表达式：

```python
config
```

立即求值得到当轮字典对象，并由新创建的函数对象保存为 `saved_config` 的默认对象引用。

它保存的是**字典引用**，不复制字典。

最终规则接口是：

```text
label(key, saved_config=<保存的字典>)
```

所以调用者可以通过第二个位置实参覆盖该次调用的 `saved_config`。

#### 工厂版

```python
def build_factories(configs):
    def make_rule(saved_config):
        def label(key):
            return f"{saved_config['locale']}:{key}"

        return label

    rules = []

    for config in configs:
        rules.append(make_rule(config))

    return rules
```

每轮真正执行：

```python
make_rule(config)
```

都会建立一次新的工厂调用环境和新的参数 binding：

```text
saved_config → 当轮字典对象
```

内部 `label` 关联的是这一次工厂调用自己的 enclosing `saved_config`。

因此最终每条规则只有：

```text
key
```

一个形参，保存配置的 binding 不暴露给最终调用者。

同样没有复制字典对象。

### 3. Q1—Q4 输出与引用解释

答：

续接片段输出：

```text
Q1 zh-CN:menu.start zh-CN:menu.start
Q2 zh-CN:menu.start zh-CN:menu.start
Q3 False
Q4 ko-KR:menu.quit
```

设最初：

```text
D1 = {"locale": "en-US"}
D2 = {"locale": "ja-JP"}
```

则构建规则后：

```text
default_rules[0] 保存的默认引用 ------→ D1
factory_rules[0] 的 enclosing binding → D1
old_config ---------------------------→ D1
configs[0] ---------------------------→ D1
```

执行：

```python
configs[0]["locale"] = "zh-CN"
```

是**原地修改 D1**，所以所有仍引用 D1 的位置都观察到：

```text
{"locale": "zh-CN"}
```

因此 Q1 两个规则都返回：

```text
zh-CN:menu.start
```

接着：

```python
configs[0] = {"locale": "fr-FR"}
```

创建新字典 D3，只替换列表槽位：

```text
configs[0] → D3
```

但先前规则保存的引用仍然：

```text
default_rules[0] → D1
factory_rules[0] → D1
old_config       → D1
```

所以 Q2 仍是：

```text
zh-CN:menu.start
```

而：

```python
configs[0] is old_config
```

为 `False`，得到 Q3。

Q4 显式传入第二个位置实参：

```python
{"locale": "ko-KR"}
```

因此这一次默认参数版规则的局部：

```text
saved_config → 新传入的 ko-KR 字典
```

返回：

```text
ko-KR:menu.quit
```

### 4. 合同差异

答：

Q4 **不会永久改变**第一条默认参数规则保存的默认对象。

显式第二个实参只影响本次调用的局部参数绑定：

```text
saved_config → {"locale": "ko-KR"}
```

函数对象原先保存的默认引用仍然指向 D1。所以下次仍只传一个 `key` 时，还是会使用 D1（当前内容为 `"zh-CN"`）。

两种修复的对外调用合同也不完全相同：

```text
默认参数版：
    label(key, saved_config=<default>)
    → 第二个参数可由调用者覆盖

工厂版：
    label(key)
    → 严格只有 key 一个业务参数
```

若对工厂版规则传第二个位置实参，会在参数匹配阶段抛出 `TypeError`，函数体不会进入。

因此，两种方案都解决了循环晚绑定，却通过不同机制保存配置，并暴露出不同的最终 callback 参数合同。

<!-- answer:end -->

<!-- quiz-section: id=D score=16 -->
## D. 递归进展与逐次调用（16 分）

本区仅讨论有限普通字符串列表，从 index=0 开始；执行期间输入列表长度和内容不变。无需实验递归深度上限，也不做时间或空间基准。

<!-- quiz-question: id=D1 score=10 -->
### D1. 深入、返回与共享轨迹（10 分）

阅读带有进入／返回轨迹的递归函数：

~~~python
def collect(keys, index, events):
    events.append(("enter", index))
    if index == len(keys):
        return []

    current = keys[index].strip().casefold()
    tail = collect(keys, index + 1, events)
    events.append(("leave", index))
    return [current, *tail]


keys = [" A ", " B "]
events = []
result = collect(keys, 0, events)
print(result)
print(events)
print(keys)
~~~

1. **结果与轨迹（4 分）**：写出三行输出，并说明为什么某一层有 enter 却没有 leave。结果与输入状态 2 分，完整事件顺序及该解释 2 分。
2. **终止论证（3 分）**：指出基线、递归步骤和一个非负整数进展量，解释它怎样严格向基线推进（2 分）。若输入为空列表，本题函数总共执行几次调用、产生哪些事件（1 分）？不要只说“有 return，所以会停”。
3. **逐次调用状态（3 分）**：在 `index=1` 的调用刚准备递归进入基线前，说明 `index=0` 与 `index=1` 两层各自的 `current`、各层 `tail` 是否已绑定（2 分）；说明两层的 `keys` 和 `events` 是否引用同一对象，以及这与独立局部绑定是否矛盾（1 分）。

第三问的时点位于内层递归调用发生之前，不是基线已经返回之后。返回语句构造的新列表与输入 `keys` 不是同一容器，但不要求讨论任何偶然的字符串对象身份。

#### D1 作答区

<!-- answer:start -->

### 1. 结果与轨迹

答：

三行输出：

```text
['a', 'b']
[('enter', 0), ('enter', 1), ('enter', 2), ('leave', 1), ('leave', 0)]
[' A ', ' B ']
```

详细轨迹：

```text
collect(keys, 0, events)
    append ("enter", 0)
    current = "a"
    ↓
    collect(keys, 1, events)
        append ("enter", 1)
        current = "b"
        ↓
        collect(keys, 2, events)
            append ("enter", 2)
            index == len(keys)
            return []
```

`index == 2` 这一层有 `"enter"`，却没有 `"leave"`，因为它命中基线后直接：

```python
return []
```

不会继续执行后面的：

```python
events.append(("leave", index))
```

基线返回后，返回链展开：

```text
index=1：
    tail = []
    append ("leave", 1)
    return ["b"]

index=0：
    tail = ["b"]
    append ("leave", 0)
    return ["a", "b"]
```

函数只读取输入 `keys`，没有修改它，因此最后仍为：

```text
[' A ', ' B ']
```

### 2. 终止论证

答：

**基线：**

```python
if index == len(keys):
    return []
```

当索引刚好到达列表长度时，没有剩余元素要处理。

**递归步骤：**

```python
collect(keys, index + 1, events)
```

每次非基线调用都把索引增加 `1`。

一个合适的非负整数进展量是：

```text
len(keys) - index
```

从题目约定的 `index=0` 开始，且输入长度在执行期间固定。每次递归：

```text
len(keys) - index
        ↓
len(keys) - (index + 1)
```

严格减少 `1`，最终从正整数减少到 `0`，此时满足基线。

所以终止的理由不是“代码里有 `return`”，而是：

> 基线与递归步骤共同保证一个良定义的非负整数进展量严格向 0 推进。

如果输入是空列表：

```python
keys = []
```

从 `index=0` 调用时：

```text
index == len(keys) == 0
```

第一次调用立即命中基线。因此：

- 总共只执行 **1 次** `collect` 调用；
- 事件只有：

```python
[("enter", 0)]
```

- 返回 `[]`；
- 没有任何 `"leave"` 事件。

### 3. 逐次调用状态

答：

题目指定时点是：

> `index=1` 那层已经计算好自己的 `current`，刚准备执行递归调用进入 `index=2` 基线之前。

此时：

#### `index=0` 那层

已经有：

```text
index   → 0
current → "a"
```

它已经执行到：

```python
tail = collect(keys, 1, events)
```

的右侧调用中，正在等待下层返回，所以它自己的：

```text
tail
```

**尚未完成赋值／尚未建立该绑定**。

#### `index=1` 那层

已经有：

```text
index   → 1
current → "b"
```

它正准备执行：

```python
tail = collect(keys, 2, events)
```

因此这一层的 `tail` 同样：

```text
尚未建立该绑定
```

不能把基线以后才返回的 `[]` 提前倒填到当前时点。

#### `keys` 与 `events` 的对象关系

两层调用都有各自独立的局部 parameter binding：

```text
index=0 调用的 keys   ──┐
index=1 调用的 keys   ──┼──→ 同一个输入列表对象
                         │
调用方 keys ------------┘

index=0 调用的 events ──┐
index=1 调用的 events ──┼──→ 同一个事件列表对象
                         │
调用方 events ----------┘
```

所以：

> 局部绑定独立，并不意味着所引用的对象必须不同。

这没有矛盾。不同调用帧中的名字是不同 binding，但这些 binding 完全可以指向同一个列表对象；因此深层向 `events` 追加的记录能被所有持有该列表引用的位置观察到。

<!-- answer:end -->

<!-- quiz-question: id=D2 score=6 -->
### D2. 基线错误与循环对照（6 分）

另一位同学把基线改成了“原列表为空”，仍然只递增索引：

~~~python
def broken_collect(keys, index=0):
    if not keys:
        return []
    current = keys[index].strip().casefold()
    tail = broken_collect(keys, index + 1)
    return [current, *tail]


result = "unchanged"
try:
    result = broken_collect([" A ", " B "])
except (IndexError, RecursionError) as error:
    print(type(error).__name__)
print(result)
~~~

1. **拒绝错误前提（2 分）**：有人断言“代码有基线而且 index 递增，必定正常完成；即使不完成，也必定先触及递归深度限制”。这两项断言是否成立？指出此输入首次失败的 `index`、具体操作、异常类型与调用方最终的 `result`。
2. **最小修复（2 分）**：在题首约定的输入合同内，只修改基线条件，使它能正确处理空列表与非空列表。给出修改后的条件，并解释修复前的条件为什么没有随着实际剩余工作量改变。
3. **有限等价（2 分）**：写一个普通循环函数，返回相同顺序的规范化字符串列表（1 分）。再指出：即使返回内容相等，为什么不能直接断言循环与递归的调用结构、对象身份及失败轨迹全部相同（1 分）？

不要求扩展支持任意外部 index、并发修改或非字符串元素。修复的目标是当前合同下的语义，不是建立通用递归框架。

#### D2 作答区

<!-- answer:start -->

### 1. 拒绝错误前提

答：

两个断言都不成立。

原函数：

```python
def broken_collect(keys, index=0):
    if not keys:
        return []
    current = keys[index].strip().casefold()
    tail = broken_collect(keys, index + 1)
    return [current, *tail]
```

对于：

```python
[" A ", " B "]
```

`keys` 在整个递归期间始终是同一个非空列表，并没有随着 `index` 增长而变为空，所以：

```python
if not keys:
```

永远不会成为真。

轨迹：

```text
index=0：keys[0] 合法
index=1：keys[1] 合法
index=2：尝试 keys[2]
```

在 `index=2` 时首先失败的具体操作是：

```python
keys[index]
```

即：

```python
keys[2]
```

抛出：

```text
IndexError
```

错误发生在这一层创建下一次递归调用之前，因此本输入根本没有先达到递归深度限制。

外层：

```python
result = broken_collect(...)
```

的右侧求值失败，赋值没有完成，所以调用方原有：

```text
result == "unchanged"
```

保持不变。

输出：

```text
IndexError
unchanged
```

### 2. 最小修复

答：

在题首约定：

- 从 `index=0` 开始；
- 输入列表执行期间长度固定；

的合同下，只需把基线改为：

```python
if index == len(keys):
    return []
```

完整核心结构为：

```python
def broken_collect(keys, index=0):
    if index == len(keys):
        return []

    current = keys[index].strip().casefold()
    tail = broken_collect(keys, index + 1)
    return [current, *tail]
```

原条件：

```python
if not keys:
```

检查的是**原列表对象整体是否为空**。对于一个一开始非空、执行期间不修改的列表，这个条件不会随着 `index` 推进而改变。

而实际剩余工作量与：

```text
len(keys) - index
```

有关。`index == len(keys)` 才真正表达“没有剩余元素需要处理”。

空列表时初始即：

```text
index == 0 == len(keys)
```

也能立即正常返回。

### 3. 有限等价的循环版本

答：

普通循环可以写成：

```python
def collect_loop(keys):
    result = []

    for key in keys:
        result.append(
            key.strip().casefold()
        )

    return result
```

对于题目约定的合法输入，它与修复后的递归版本返回相同顺序的规范化字符串内容。

但不能由“返回内容相等”推出两种实现的所有运行属性相同。

递归版：

- 每个元素对应新的函数调用层；
- 每层有独立局部 binding；
- 下层返回后逐层构造 `[current, *tail]`；
- 会创建多层中间返回列表。

循环版：

- 在一次函数调用中反复迭代；
- 使用一个显式 `result` 列表并原地 `append`；
- 没有同样的递归调用／返回链。

因此即使最终列表内容相等，也不能直接宣称：

- 调用结构相同；
- 中间对象身份相同；
- 发生异常时的调用栈和局部状态轨迹相同。

“值相等”只证明结果内容这一维度，不自动证明实现过程和对象身份等价。

<!-- answer:end -->

<!-- quiz-section: id=E score=14 -->
## E. lambda、注解与 Callable（14 分）

本区区分表达式结果、对象引用与接口元数据。注解默认不实施运行时类型检查；具体代码仍遵守普通参数匹配和函数体执行规则。

<!-- quiz-question: id=E1 score=6 -->
### E1. 排序键、对象身份与返回值（6 分）

以下排序 key 只读取 priority，不修改记录；后面的赋值与记录操作按源码顺序执行：

~~~python
records = [
    {"key": "menu.quit", "priority": 20},
    {"key": "menu.start", "priority": 10},
]
ordered = sorted(records, key=lambda record: record["priority"])
ordered[0]["key"] = "menu.begin"

notices = []
report = lambda record: notices.append(record["key"])
returned = report(ordered[0])

print([record["key"] for record in records])
print([record["key"] for record in ordered])
print(returned, notices, ordered[0] is records[1])
~~~

1. **输出预测（3 分）**：写出三行输出，每行 1 分。
2. **两项边界（2 分）**：说明 sorted 的 key 返回值是否替换了列表元素，以及为何修改 ordered 中的字典会影响 records（1 分）；说明 report 为什么返回该值，“单表达式”是否意味着没有副作用（1 分）。
3. **清晰改写（1 分）**：用具名 def 重写 report，使其仍向同一 notices 列表追加记录，但正常返回本次记录的 key 字符串。只需要这个小函数；不要把多步骤逻辑压成复杂 lambda。

不要求稳定排序的特殊细节；本例两个优先级不同。不能把“sorted 创建新外层列表”扩大为“字典元素也被自动复制”。

#### E1 作答区

<!-- answer:start -->

### 1. 三行输出

答：

输出依次为：

```text
['menu.quit', 'menu.begin']
['menu.begin', 'menu.quit']
None ['menu.begin'] True
```

原因如下。

`sorted(...)` 创建一个**新的外层列表**：

```text
ordered
```

并根据 key 函数返回的 priority 排序。两个原字典对象本身并没有被复制：

```text
records[1] --------------┐
                         ├──→ priority=10 的同一个字典对象
ordered[0] --------------┘
```

因此：

```python
ordered[0]["key"] = "menu.begin"
```

原地修改这个共享字典后：

- `ordered[0]["key"]` 变成 `"menu.begin"`；
- `records[1]["key"]` 也观察到同一修改。

原 `records` 的外层顺序不变，所以第一行是：

```text
['menu.quit', 'menu.begin']
```

`ordered` 的外层顺序是按 priority 排序后的 `[原 records[1], 原 records[0]]`，所以第二行：

```text
['menu.begin', 'menu.quit']
```

### 2. 两项边界

答：

#### sorted 的 key 返回值是否替换元素

不会。

```python
lambda record: record["priority"]
```

的返回值只是提供**排序键**，例如 `10`、`20`；这些整数并不会替换原列表元素。

`sorted` 新建的是外层列表 `ordered`，其中仍保存原来的字典对象引用。因此修改 `ordered[0]` 指向的字典，也会被仍引用该字典的 `records[1]` 观察到。

“新列表”不等于“元素对象也被复制”。

#### report 为什么返回 `None`

```python
report = lambda record: notices.append(record["key"])
```

`lambda` 会返回其唯一表达式的结果。

该表达式是：

```python
notices.append(...)
```

`list.append()` 在完成列表原地修改后正常返回：

```text
None
```

因此：

```python
returned
```

绑定到 `None`。

与此同时：

```text
notices == ["menu.begin"]
```

已经发生。

所以“lambda 函数体只能写一个表达式”绝不等于“这个表达式没有副作用”；一个函数调用表达式本身就完全可能修改外部对象。

### 3. 具名 `def` 改写

答：

```python
def report(record):
    key = record["key"]
    notices.append(key)
    return key
```

现在它仍向同一个 `notices` 列表追加本次记录的 key，同时正常返回该 key 字符串。

<!-- answer:end -->

<!-- quiz-question: id=E2 score=8 -->

### E2. 元数据与实际调用分层（8 分）

代码没有引入运行时类型检查库，也没有使用 future annotations。下面的元数据访问使用当前 Python 3.14.5 的正常函数属性语义：

~~~python
from collections.abc import Callable

TextRule = Callable[[str], str]
events = []


def apply_rule(text: str, rule: TextRule) -> str:
    events.append("apply:enter")
    result = rule(text)
    events.append("apply:leave")
    return result


def wrong_return(text):
    events.append("wrong:body")
    return 123


def zero_arguments():
    events.append("zero:body")
    return "ready"


def normalize(text):
    events.append("normalize:body")
    return text.strip().casefold()


metadata = apply_rule.__annotations__
print("M1", tuple(metadata), metadata["return"] is str)
print("M2", events, callable(zero_arguments))

for text, rule in (
    ("menu.start", wrong_return),
    ("menu.quit", zero_arguments),
    (404, normalize),
):
    events.clear()
    result = "old"
    error_name = None
    try:
        result = apply_rule(text, rule)
    except (TypeError, AttributeError) as error:
        error_name = type(error).__name__
    print(result, error_name, events)
~~~

1. **元数据观察（2 分）**：写出 M1、M2 两行输出，并说明为什么 metadata 不是“最近一次调用的实际参数／返回值记录”。
2. **真实运行（3 分）**：写出循环产生的三行输出，每次尝试 1 分。返回值不满足注解但没有异常时，仍应如实描述运行事实。
3. **错误发生层（2 分）**：分别指出 zero_arguments 与 normalize 两次失败发生在何处，以及相应规则函数体是否已进入；区分“外层参数绑定”“内部调用匹配”和“规则函数体操作”。
4. **合同修补（1 分）**：若业务要求规则正常返回值必须是 str，应把显式检查放在 apply_rule 的什么位置？说明这项检查为什么仍不能保证业务键正确，也不能回滚此前副作用。

本题不要求回忆注解延迟求值的实现细节；只需避免声称“注解是自动类型转换器”或“注解值就是某次运行的数据”。函数实际接受参数的形状，与注解描述的类型意图应分开解释。

#### E2 作答区

<!-- answer:start -->

### 1. M1、M2 元数据输出

答：

前两行输出为：

```text
M1 ('text', 'rule', 'return') True
M2 [] True
```

`apply_rule` 的注解键按定义中的参数及返回注解呈现：

```text
text
rule
return
```

读取：

```python
metadata = apply_rule.__annotations__
```

得到的是函数的**注解元数据映射**，不是某一次调用留下的：

- 实际参数对象记录；
- 实际返回值记录；
- 调用历史。

因此：

```python
metadata["return"] is str
```

为真，只说明返回注解求值得到的是 `str` 类型对象。

在这之前没有执行任何题中 rule，`events` 仍为：

```text
[]
```

而：

```python
callable(zero_arguments)
```

为 `True`，因为它是函数对象；这并不表示它能接受 `apply_rule` 将传入的那个位置实参。

### 2. 三次真实运行

答：

循环产生的三行输出依次是：

```text
123 None ['apply:enter', 'wrong:body', 'apply:leave']
old TypeError ['apply:enter']
old AttributeError ['apply:enter', 'normalize:body']
```

#### 第一次：`("menu.start", wrong_return)`

`apply_rule` 正常建立：

```text
text → "menu.start"
rule → wrong_return 函数对象
```

先追加：

```text
"apply:enter"
```

随后：

```python
rule(text)
```

真正调用 `wrong_return("menu.start")`。

它接受一个位置实参，所以参数匹配成功、进入函数体，追加：

```text
"wrong:body"
```

然后返回整数：

```text
123
```

尽管这违反 `TextRule` 的 `str → str` 类型意图，Python 本题没有运行时类型检查，因此没有异常。

`apply_rule` 接着追加：

```text
"apply:leave"
```

并返回 `123`。

因此外层 `result` 真正变为 `123`，`error_name` 仍是 `None`。

#### 第二次：`("menu.quit", zero_arguments)`

外层 `apply_rule` 参数绑定成功，并先追加：

```text
"apply:enter"
```

随后尝试：

```python
zero_arguments("menu.quit")
```

但 `zero_arguments()` 没有参数。

错误发生在**内部 rule 调用的参数匹配阶段**，抛出 `TypeError`；它的函数体没有进入，所以不会追加：

```text
"zero:body"
```

`apply_rule` 也不会执行 `"apply:leave"`。

外层 `result = apply_rule(...)` 的赋值失败，因此 `result` 仍是 `"old"`。

#### 第三次：`(404, normalize)`

外层 `apply_rule` 仍可正常绑定：

```text
text → 整数 404
rule → normalize 函数对象
```

注解不会阻止这一绑定。

它追加：

```text
"apply:enter"
```

调用：

```python
normalize(404)
```

时，内部参数形状匹配成功，所以 `normalize` 函数体确实进入，并先追加：

```text
"normalize:body"
```

然后执行：

```python
text.strip()
```

整数对象没有 `strip` 属性，故在**规则函数体对象操作阶段**抛出：

```text
AttributeError
```

`apply_rule` 不会执行 `"apply:leave"`，外层结果赋值也未完成，`result` 保持 `"old"`。

### 3. 两次失败的发生层

答：

可以分成：

```text
外层 apply_rule 参数绑定
        ↓
apply_rule 函数体
        ↓
内部 rule(text) 调用匹配
        ↓
规则函数体对象操作
```

#### `zero_arguments`

- 外层 `apply_rule("menu.quit", zero_arguments)` 参数绑定：成功；
- `apply_rule` 函数体：进入；
- `rule(text)` 内部调用匹配：失败；
- 异常：`TypeError`；
- `zero_arguments` 函数体：**没有进入**。

#### `normalize`

- 外层 `apply_rule(404, normalize)` 参数绑定：成功；
- `apply_rule` 函数体：进入；
- `normalize(404)` 内部参数匹配：成功；
- `normalize` 函数体：**已经进入**；
- 失败操作：整数对象执行 `.strip()`；
- 异常：`AttributeError`。

因此一个是“调用形状失败”，另一个是“函数体真实对象操作失败”。

### 4. 返回类型合同的显式检查

答：

若业务要求 rule 正常返回值必须是 `str`，检查应放在：

```python
result = rule(text)
```

**正常返回之后、将结果作为成功值继续使用之前**。

例如：

```python
def apply_rule(text: str, rule: TextRule) -> str:
    events.append("apply:enter")

    result = rule(text)

    if not isinstance(result, str):
        raise TypeError("rule must return str")

    events.append("apply:leave")
    return result
```

这样 `wrong_return` 返回 `123` 时会在 `apply_rule` 中显式失败。

但这仍只能验证**对象类型**，不能证明：

- 字符串一定是合法本地化 key；
- 大小写、前缀等业务规则正确；
- 没有不允许的业务内容。

同时，检查发生在 rule 已经真实执行并正常返回之后；此前 rule 已产生的副作用（例如向 `events` 追加）不会因为后续 `TypeError` 自动回滚。

<!-- answer:end -->

<!-- quiz-section: id=F score=16 -->

## F. 本地化工程接口（16 分）

本区是一道单文件内可完成的小型接口题，不要求建立项目、类、注册框架或测试套件。实现与实验都写在作答区，保持纯内存、可复盘。

<!-- quiz-question: id=F1 score=16 -->
### F1. 构建有限转换管线（16 分）

本地化团队希望先选择一组文本规则，稍后多次处理字符串。请实现：

`make_localizer(registry, names, *, on_success)`

它返回一个只有 text 业务参数的函数 `run(text)`。所有传入 callable 都是题内合成函数，不访问文件、数据库、网络或 GUI。题目对行为的要求如下。

**输入前提与范围**

- registry 是普通字典，键为规则名，值由调用方保证为 callable；names 是普通字符串列表，允许为空。
- 规则的预期接口是“接收一个字符串，正常返回字符串”，但调用方不保证实际调用形状、返回类型、业务结果或是否抛异常。
- on_success 由调用方保证为 callable，预期接收一个最终字符串；不要要求使用 inspect 预检完整签名。
- 不要求处理并发修改、无限输入、任意 iterable、配置深拷贝或异常包装框架；普通循环即可。

**构建阶段合同**

1. 按 names 当时的顺序，从 registry 取得对应的函数对象并保存到一个 tuple；只保存引用，不在构建时调用规则或 on_success。
2. 缺少规则名时，让字典查找的 KeyError 原样向外传播，不返回一个假装可用的 run。
3. 构建成功后，调用方修改 names 的内容或替换 registry 的条目，不应改变这个 run 已选择的规则序列。注意：这项要求固定的是规则对象引用，不保证那些函数所访问的外部状态被冻结。

**执行阶段合同**

1. 每次 run(text) 首先检查 text 是否为 str；不符则抛 TypeError，而且不调用任何规则或成功回调。
2. 按已保存顺序调用规则，每一步正常返回后立即检查结果是否为 str；不符则抛 TypeError，不继续执行后续规则或成功回调。
3. 规则自身抛出的异常原样传播，不重试、不吞掉，也不包装成另一种异常。
4. 所有规则成功后，调用一次 on_success(current)，忽略它的正常返回值；只有回调也正常返回后，run 才返回最终字符串。
5. 回调若抛异常，就向外传播，run 不正常返回；所有已发生的副作用保持原样，不承诺回滚。
6. 空规则序列也是合法的：仍先检查输入，再调用成功回调一次，最后返回原输入字符串，不额外 strip 或 casefold。

下面是一组可作为起点的合成数据；它只定义规则和配置，不包含待实现函数，也不是完整答案：

~~~python
events = []


def trim(text):
    events.append("trim")
    return text.strip()


def fold(text):
    events.append("fold")
    return text.casefold()


def record_success(text):
    events.append(("success", text))
    return "ignored receipt"


registry = {"trim": trim, "fold": fold}
names = ["trim", "fold"]
~~~

完成以下三部分：

1. **实现（8 分）**：写出 make_localizer 及其返回的 run。
   - 构建时有序保存引用、缺名传播且无规则执行：3 分。
   - 每次调用的输入检查、有序转换、逐步返回类型检查：3 分。
   - 回调时机、忽略回调正常返回值、异常原样传播和空链行为：2 分。
   - 可为参数与返回值添加基础注解，但不能把注解本身当作检查；不要求高级类型工具。同一个根因造成的同一实现缺陷不在多个评分点重复扣分。
2. **合同解释（4 分）**：用不超过四个短段分别解释下列边界，每项 1 分：
   - 保存 tuple 后，names 或 registry 条目变化为何不必改变已有 run。
   - 规则若是读取可变配置的闭包，为何配置后来变化仍可能影响结果。
   - 输出类型检查失败时，为什么不能声称此前执行过的规则没有副作用。
   - on_success 的返回值与 run 的返回值是什么关系，回调异常又如何影响调用方赋值。
3. **聚焦验证（4 分）**：写四组可运行的 assert／try-except 实验，每组可含多个断言，每组 1 分：
   - 构建不执行行为、正常结果，以及构建后修改 names／registry 条目仍保留原选择。
   - 某条规则返回非 str 或自身抛异常时，不执行后续规则／成功回调；至少选择一种失败方式并检查事件轨迹。
   - 成功回调先写入一条事件再抛异常：异常向外传播，调用方旧绑定保留，已经写入的事件仍存在。
   - 空规则序列对合法字符串仍触发一次回调；非 str 输入在所有规则／回调之前被拒绝。

验证不要求 pytest，也不允许把实验放进 tests/。你可自定义小型规则和事件列表；每组实验从明确的新状态开始，避免前一组事件残留导致误判。若使用 catch，只捕获该场景预期的异常，不能用静默吞错代替断言。验收关注合同是否逐条成立，而不是代码长短或抽象层数。

#### F1 作答区

<!-- answer:start -->

### 1. `make_localizer` 实现

答：

```python
def make_localizer(registry, names, *, on_success):
    # 构建阶段：
    # 按 names 当前顺序依次查表，只保存函数对象引用。
    # 任意名字缺失时，registry[name] 的 KeyError 原样传播。
    selected_rules = tuple(
        registry[name]
        for name in names
    )

    def run(text):
        # 执行阶段入口检查：失败时尚未调用任何规则或回调。
        if not isinstance(text, str):
            raise TypeError("text must be str")

        current = text

        for rule in selected_rules:
            # 规则自身的异常不捕获、不包装，原样传播。
            next_value = rule(current)

            # 只有规则正常返回后才执行返回类型检查。
            if not isinstance(next_value, str):
                raise TypeError(
                    "rule must return str"
                )

            current = next_value

        # 空规则序列时也会执行到这里：
        # current 仍是原输入字符串。
        # 正常返回值被忽略；异常原样传播。
        on_success(current)

        # 只有 callback 也正常返回，run 才正常返回。
        return current

    return run
```

#### 构建阶段

执行：

```python
selected_rules = tuple(registry[name] for name in names)
```

会按 `names` **当时的顺序**依次读取字典槽位，将得到的规则函数对象引用保存进一个 tuple。

它没有写：

```python
registry[name](...)
```

所以构建阶段不会调用任何规则，也不会调用 `on_success`。

如果中途某个名字不存在：

```python
registry[name]
```

直接产生 `KeyError`；本函数没有捕获它，因此异常原样传播，本次 `make_localizer(...)` 调用不会正常返回一个 `run`。

#### 执行阶段

每次调用 `run(text)`：

1. 先检查 `text` 是否为 `str`；
2. 按 tuple 中保存的顺序逐条调用规则；
3. 每条规则正常返回后立即检查其返回对象是否为 `str`；
4. 任一步异常都立即向外传播；
5. 所有规则成功后调用一次 `on_success(current)`；
6. 忽略 callback 的正常返回对象；
7. callback 也正常返回后，才 `return current`。

空规则序列时：

```text
selected_rules == ()
```

循环执行零次，但入口类型检查仍执行；之后 `on_success(text)` 调用一次，最后原样返回输入字符串。

---

### 2. 合同解释

答：

**（1）为什么后改 `names` 或 registry 槽位不改变已有 `run`：**  
构建阶段已经把按当时顺序查到的函数对象引用保存进独立 tuple `selected_rules`。后续修改 `names` 只是改变原列表内容；`registry["x"] = other_rule` 只是改写字典槽位。二者都不会追溯改写已经保存进 tuple 的那些引用。

**（2）为什么闭包规则仍可能受可变配置影响：**  
固定的是“规则函数对象引用”，不是该函数可达的所有外部对象快照。如果某条规则是 closure，并通过 enclosing binding 引用某个可变配置字典，之后原地修改该字典内容，调用同一个规则函数时仍可能读到新内容；构建阶段没有深拷贝配置。

**（3）规则输出类型检查失败为何不抹掉此前副作用：**  
返回类型检查发生在 `rule(current)` 已正常返回之后。此前该 rule 以及更早规则可能已经修改列表、计数、日志等外部状态。随后抛出的 `TypeError` 只中断控制流，不提供事务回滚，所以不能说“前面规则等于没执行”。

**（4）`on_success` 返回值、`run` 返回值与异常：**  
`on_success(current)` 的正常返回对象被忽略；`run` 的正常返回值始终由自己的 `return current` 决定。若 callback 抛异常，控制流到不了 `return current`，`run` 不正常返回；若调用方写 `result = run(...)`，右侧失败则这次调用方赋值不完成，旧绑定保留，而 callback 抛异常前已经完成的副作用仍存在。

---

### 3. 四组聚焦验证

以下每组都使用明确的新状态，不依赖上一组事件残留。

#### 验证组 1：构建不执行行为；正常结果；构建后修改配置不改变已选规则

```python
events1 = []


def trim1(text):
    events1.append("trim")
    return text.strip()


def fold1(text):
    events1.append("fold")
    return text.casefold()


def success1(text):
    events1.append(("success", text))
    return "ignored"


registry1 = {
    "trim": trim1,
    "fold": fold1,
}

names1 = ["trim", "fold"]

run1 = make_localizer(
    registry1,
    names1,
    on_success=success1,
)

# 构建阶段没有执行规则或 callback。
assert events1 == []

# 构建后修改原配置。
names1[:] = ["fold"]
registry1["trim"] = (
    lambda text: "REPLACED"
)

# 已有 run 仍使用构建时保存的 trim1、fold1。
value1 = run1(" A ")

assert value1 == "a"
assert events1 == [
    "trim",
    "fold",
    ("success", "a"),
]
```

这同时证明 callback 的 `"ignored"` 正常返回值没有成为 `run1` 的返回值。

#### 验证组 2：规则返回非字符串时立即失败，不执行后续规则／成功回调

```python
events2 = []


def bad2(text):
    events2.append("bad")
    return 123


def later2(text):
    events2.append("later")
    return text


def success2(text):
    events2.append("success")


run2 = make_localizer(
    {
        "bad": bad2,
        "later": later2,
    },
    ["bad", "later"],
    on_success=success2,
)

try:
    run2("x")
except TypeError:
    pass
else:
    raise AssertionError(
        "TypeError was expected"
    )

assert events2 == ["bad"]
```

`bad2` 的函数体已经执行并产生 `"bad"` 事件；返回对象 `123` 触发显式类型检查失败。`later2` 与 `success2` 均未执行。

#### 验证组 3：成功回调先产生副作用再抛异常

```python
events3 = []


def identity3(text):
    events3.append("rule")
    return text


def failing_success3(text):
    events3.append(
        ("success", text)
    )
    raise RuntimeError(
        "callback failed"
    )


run3 = make_localizer(
    {"id": identity3},
    ["id"],
    on_success=failing_success3,
)

result3 = "old"

try:
    result3 = run3("ready")
except RuntimeError:
    pass
else:
    raise AssertionError(
        "RuntimeError was expected"
    )

# 调用方赋值没有完成。
assert result3 == "old"

# callback 抛异常前写入的事件没有回滚。
assert events3 == [
    "rule",
    ("success", "ready"),
]
```

规则已经正常完成；callback 也已经进入并写入事件，但由于随后异常，`run3` 没有正常返回。

#### 验证组 4：空规则链仍回调一次；非字符串输入在所有行为之前拒绝

```python
events4 = []


def success4(text):
    events4.append(
        ("success", text)
    )
    return None


run4 = make_localizer(
    {},
    [],
    on_success=success4,
)

# 空规则序列：合法字符串原样返回，并通知一次。
value4 = run4(" Raw ")

assert value4 == " Raw "
assert events4 == [
    ("success", " Raw "),
]

# 新的观察状态。
events4.clear()

try:
    run4(404)
except TypeError:
    pass
else:
    raise AssertionError(
        "TypeError was expected"
    )

# 输入检查发生在规则／callback 之前。
assert events4 == []
```

以上四组分别验证了构建阶段、规则返回合同、callback 异常边界以及空链／入口类型检查，但仍只是针对这些明确路径的证据；它们不应被扩大解释为“任意第三方规则在所有输入和外部状态下都满足完整业务合同”。

<!-- answer:end -->

## 交卷说明

完成后保留全部原始答案，告知可以批改。批改阶段才会建立逐题覆盖账本、记录分数和学习画像更新；本轮生成考卷不执行这些步骤。

---

## Codex 批改记录（逐题审批，2026-09-26）

本区追加于完整原卷之后，不改写题干或原答案。卷首“尚未作答、未批改”属于命题时快照；最新状态以本批改区为准。

### 逐题覆盖账本

当前阶段：`quiz_review` 已完成；章节角色：`normal`。下一关卡 `stage_note` 尚未开始；本章没有已排期的测验前 capstone，本次不执行阶段笔记或最终收束。

下列原答案行号以批改前版本为基准（追加批改不改变这些行号），包含答案区标记。各题发现、扣分与运行证据会在对应审批条目中展开。

| 题号 | 满分 | 原答案位置 | 审批状态 | 发现 / 得分 / 证据 |
| --- | ---: | --- | --- | --- |
| A1 | 6 | A1 作答区，L76–212 | 已审批 | 6/6；对象、合同与顺序正确；内存验证通过 |
| A2 | 6 | A2 作答区，L227–334 | 已审批 | 6/6；补充浅拷贝比较的证据限制；反例验证通过 |
| B1 | 8 | B1 作答区，L385–494 | 已审批 | 8/8；原版/变体与引用时点正确；运行通过 |
| B2 | 10 | B2 作答区，L548–721 | 已审批 | 10/10；两层异常与 callback 返回边界正确；运行通过 |
| C1 | 12 | C1 作答区，L779–969 | 已审批 | 12/12；绑定隔离与列表共享正确；四行运行吻合 |
| C2 | 12 | C2 作答区，L1021–1271 | 已审批 | 12/12；两种修复/引用边界正确；澄清简写；运行通过 |
| D1 | 10 | D1 作答区，L1311–1517 | 已审批 | 10/10；递归进展与精确时点正确；轨迹验证通过 |
| D2 | 6 | D2 作答区，L1549–1726 | 已审批 | 6/6；失败定位/修复/循环对照正确；运行通过 |
| E1 | 6 | E1 作答区，L1763–1885 | 已审批 | 6/6；排序引用/lambda 返回/def 改写正确；运行通过 |
| E2 | 8 | E2 作答区，L1950–2205 | 已审批 | 8/8；元数据与两层调用正确；澄清属性查找；运行通过 |
| F1 | 16 | F1 作答区，L2291–2600 | 已审批 | 16/16；实现/四项合同/四组实验均通过；补充边界通过 |

审批游标：A1–F1 已全部审批，`11 / 11` 全覆盖；分区与总分已复核，稳定得分 `100 / 100`。画像同步及最终文件检查已完成；下一原子动作是 C19 阶段笔记，不重批已审批题目。

原卷保留基线：UTF-8、LF，70382 字节，2604 行；SHA-256 `c9cf58660694317959f5c004e83e917bc8786866a0220d8ec0e8ec2e3fddb1da`。最终核对该原始字节前缀及全部 11 个答案区。

### 逐题审批详情

#### A1：6 / 6（2 + 2 + 2）

- 对象与时点：2/2。函数名字、字典项保存的引用、返回到调用方后的绑定，以及真正调用 `selected(...)` 均区分正确。
- 高阶性质：2/2。按本题“选择并返回规则函数”的合同，属于高阶函数；接受 callable 与返回 callable 不必同时满足。这个判断依赖本题返回的是函数，不能从任意通用字典取值函数的语法无条件推出。
- 可组合性：2/2。异常与副作用两项合同有效；先去空白与先加前缀的反例确实给出不同结果。
- 术语澄清，不扣分：`registry["strip"]` 在表达式位置是下标取值表达式，图中用它标示对应字典项的引用位置是可接受的简写。它不是复制或移除函数。
- 运行证据：题干执行后 `selected is strip_text is registry["strip"]` 为真、`value == 'Menu.Start'`；两种顺序分别得到 `en:Menu.Start` 与 `en: Menu.Start`。无扣分。

#### A2：6 / 6（2 + 2 + 2）

- 三项分别 2/2：注册只保存引用；`callable()` 与呈现签名匹配不证明真实业务行为；注解与一次返回不等于所有路径实施了运行时类型检查。补充观察均有针对性，且明确限制了一次观察的外推范围。
- 必须限定的证据边界，不扣分：原答 L293–302 用 `events.copy()` 做前后比较，它只是浅层外壳快照。若元素含共享可变对象，前后可能一起变化；即使元素不可变，先改后恢复也可能让最终比较相等。因此 `before == after` 只说明所比较的观察结果相等，不能单独证明这次调用期间没有修改，更不能覆盖未观察的外部状态。原答并未宣称这些检查能证明完整无副作用合同，因此作为验证方案补充，不扣分。
- 运行证据：合成函数能同时通过 `callable()`、签名 `bind()`，随后追加事件并返回 `123`，即使注解写了 `str` 也不会自动拦截；另验证了浅拷贝前后共同引用内部字典时，修改发生但比较仍相等。

#### B1：8 / 8（3 + 3 + 2）

- 三行输出 3/3，指定时点引用图和局部形参生命周期 3/3，调用版别名变化 2/2。原版及独立变体输出均与原答一致。
- 已修复 C18 的历史精度点：没有把已返回调用的局部形参与后续调用方名字机械画成永久共存；引用箭头方向正确。
- 术语澄清，不扣分：“字典槽位重新绑定”在该图中指替换键对应的 value 引用；具体操作是修改字典对象，不是重新绑定名字 `registry`，也不是改写此前保存的函数对象或别名。
- 运行证据：原版 P1 为 `True False ['select']`；改为 `alias = selected(" X ")` 后，P1 为 `False False ['select', 'trim']`。差异来自右侧调用，不是名字绑定自行执行函数。无扣分。

#### B2：10 / 10（4 + 4 + 2）

- 完整输出 4/4；两次最后成功的 `current`、callback 进入情况、调用方旧绑定及非回滚边界 4/4；callback 正常返回 `None` 后外层仍返回转换结果 2/2。
- 控制流表述精确：第二轮失败发生在新的 `current = rule(current)` 右侧调用，未完成这一次重绑；第一轮虽然转换完成，callback 异常仍阻止外层 `return current` 与调用方赋值完成。
- 运行证据：原题四行与答案逐行一致；callback 改为正常返回 `None` 且只跑首个输入后，调用方得到 `menu.start`，三个事件保留。无扣分。

分组检查点：A 区 `12 / 12`，B 区 `18 / 18`，累计 `30 / 30`；A1–B2 已审批，下一题 C1。

#### C1：12 / 12（4 + 4 + 4）

- 输出 4/4；两个时点的引用关系 4/4；独立计数、A 环境重绑与结果快照 4/4。两次工厂调用的绑定独立，但可以共同引用 L1；`replace_a([])` 只改变 A 环境的 `history`，不重置计数、不修改 L1。
- 原答正确限制了 `tuple(history)`：本题新建外层 tuple 并保存当时记录引用，既不跟随后续列表追加，也不是任意嵌套对象的深拷贝。本例记录由不可变字符串、整数和 tuple 组成，快照内容不会因后续追加改变。
- 运行证据：C1—C4 四行与原答逐行一致；主审与独立复核结论一致。无扣分。

#### C2：12 / 12（2 + 4 + 4 + 2）

- 晚绑定解释 2/2；默认参数版与工厂版分别 2/2；Q1—Q4 及对象解释 4/4；覆盖默认值与接口差异 2/2。
- 两个函数对象不同，但稍后读取同一次外层调用中的同一个 `config` 绑定；默认参数保存定义时所得字典引用，工厂版每次建立独立 enclosing 绑定。两种修复都没有复制字典。
- 精度澄清，不扣分：L1034 的“该调用中只有一个局部名字／binding”应明确读成“只有一个供这些规则共享的 `config` 绑定”，不是说整次调用只有一个局部名字；还有 `configs`、`rules`、`label`。后续解释已准确限定共享的是 `config`。
- 引用图澄清，不扣分：L1204–1205 的“规则 → D1”承接前文，是间接引用简写；严格路径是“函数保存的默认引用／关联的 enclosing 绑定 → D1”，不是函数对象等于字典。L1138 的“不暴露给最终调用者”只指普通调用接口不提供配置形参，并非安全隔离承诺。
- 运行证据：直接使用原答两种实现，晚绑定原版与 Q1—Q4 均吻合；Q4 之后单参数调用仍使用 `zh-CN`，工厂版额外第二位置参数确实触发 `TypeError`。无扣分。

#### D1：10 / 10（4 + 3 + 3）

- 结果和事件轨迹 4/4；基线、非负进展量与空输入 3/3；精确时点的局部绑定及共享对象 3/3。
- 你没有把基线返回后的 `tail = []` 提前填进尚未返回的时点：外层 `current == 'a'`、内层 `current == 'b'`，两层 `tail` 均尚未绑定。独立调用的局部名字可以引用同一份 `keys`、`events`。
- 运行证据：三行输出吻合；在题目指定时点用临时、已恢复的进程内跟踪核对得到 `('a', 'b', False, False, True, True)`，依次对应两层 current、两个 tail 是否已绑定、两个共享身份判断；空输入仅一次调用、事件 `[('enter', 0)]`。
- 终止论证在题设固定有限输入、从 0 开始的算法模型下成立；它不是解释器对任意长度输入都保证正常返回的资源承诺。本题不扩展考查递归限额。无扣分。

#### D2：6 / 6（2 + 2 + 2）

- 首次失败定位 2/2；最小基线修复 2/2；循环实现及有限等价解释 2/2。
- 原版首先在 `index == 2` 的 `keys[index]` 取值失败，下一次递归尚未发生；`IndexError` 不会完成调用方赋值，旧值 `unchanged` 保留。单纯增长 index 不会让原非空列表变空。
- 原答没有把结果内容相等扩大为调用结构、中间对象、局部绑定及失败轨迹全部相同，边界正确。
- 运行证据：原版输出与原答一致；直接提取原答修复函数和循环函数，对空列表、题设两项列表、含空串与 `Straße` 的合法短列表做对照，结果全部一致。无扣分。

分组检查点：C 区 `24 / 24`，D 区 `16 / 16`；A1–D2 已审批，累计 `70 / 70`，下一题 E1。

#### E1：6 / 6（3 + 2 + 1）

- 三行输出 3/3；排序键与共享字典、lambda 表达式结果与副作用两项边界 2/2；具名 `def` 改写 1/1。
- `sorted()` 的 key 只提供比较用键，不替换结果元素；新外层列表仍引用原字典。`lambda` 返回 `append()` 的结果 `None`，不意味着其唯一表达式没有副作用。改写后的 `report` 同时追加 key 并返回 key，符合要求。
- 运行证据：题干三行输出逐行吻合；直接运行原答具名函数，确认返回 `menu.begin` 且同一 notices 列表只新增该项。无扣分。

#### E2：8 / 8（2 + 3 + 2 + 1）

- 元数据输出与含义 2/2；三个实际运行分支 3/3；两次失败层次 2/2；显式返回类型检查位置及证据限制 1/1。
- `wrong_return` 实际返回 123 而没有自动注解检查；`zero_arguments` 在内部调用匹配时失败、函数体未进入；`normalize(404)` 已进入函数体，之后发生对象属性操作失败。原答正确区分了外层与内部两次调用。
- 操作粒度澄清，不扣分：L2163 的“整数对象执行 `.strip()`”应精确为“求值 `text.strip()` 时，对整数查找 `strip` 属性就失败了”，不是已经找到并执行了一个 `strip` 方法后才失败。原答 L2125 已指出属性不存在，因此不视为机制误判。
- 运行证据：M1/M2 和循环三行全部吻合。直接运行原答检查版 `apply_rule`，错误返回路径只保留 `apply:enter`、`wrong:body`，然后显式 `TypeError`；正常规范化路径仍返回字符串并记入 `apply:leave`。无扣分。

#### F1：16 / 16（8 + 4 + 4）

实现评分（8/8）：

- 构建有序引用 tuple、缺名原样传播且不执行规则／callback：3/3。`tuple(...)` 在本次构建中完成对表达式的消费，不把查表推迟到以后的 run。
- 每次入口类型检查、有序执行、每步返回后立即验类型：3/3。使用临时 `next_value`，检查成功后再更新 `current`，边界清晰。
- callback 时机、忽略正常返回值、异常传播与空链：2/2。没有重试、吞异常、包装或额外规范化；callback 正常返回后才返回转换结果。

合同解释（4/4）：四项各 1 分。引用选择快照不是可达配置深快照；规则正常返回后的类型失败不回滚效果；callback 自身返回不等于外层返回；callback 异常阻止调用方这次赋值完成。均准确。

四组实验（4/4）：四组各 1 分。已直接执行原答实现及四段实验，所有 assert 通过；异常分支的 `except ...: pass` 配有 `else: raise AssertionError` 和具体轨迹断言，不属于用静默吞错代替验证。

补充运行证据（不增设评分门槛）：

- 缺名 `KeyError` 保留键信息、无规则或 callback 执行，构造调用方旧绑定保留。
- 非空链传入 404 时同样在任何规则／callback 前失败；多次正常调用仍复用已选规则并各通知一次。
- 规则抛出的预先创建异常与调用方捕获异常为同一对象，后续规则及 callback 均未进入。
- callback 的异常对象同样原样传播，调用方旧绑定及此前事件保留。
- 规则读取的闭包配置原地变化后，已有 run 仍读到新值，验证“选择冻结不等于状态冻结”。
- 不接收实参的规则在内部匹配阶段失败，规则体、后续规则及 callback 均未进入；公开签名也符合题设。

证据范围澄清，不扣分：原答第四组用空链验证非法输入，直接观察到的是 callback 未执行；非空链规则也未执行由实现检查位置支持，并已补测确认。题干未要求为此额外编写第五组，不能据此倒扣分。以上验证仍只覆盖明确合成路径，不证明任意第三方函数的完整合同。

分组检查点：E 区 `14 / 14`，F 区 `16 / 16`；A1–F1 共 `11 / 11` 全部审批完成。下一动作：复核分区与总分，然后形成末评；稳定前不更新画像。

### 分区与总分复核

| 分区 | 逐题得分 | 小计 | 扣分 |
| --- | --- | ---: | ---: |
| A | A1 6 + A2 6 | 12 / 12 | 0 |
| B | B1 8 + B2 10 | 18 / 18 | 0 |
| C | C1 12 + C2 12 | 24 / 24 | 0 |
| D | D1 10 + D2 6 | 16 / 16 | 0 |
| E | E1 6 + E2 8 | 14 / 14 | 0 |
| F | F1 16 | 16 / 16 | 0 |
| 总计 | 11 题均已审批 | **100 / 100** | **0** |

已用程序逐一核对覆盖账本中的题号、满分、已审批状态、详情得分与分区之和：`12 + 18 + 24 + 16 + 14 + 16 = 100`。没有未审批题或未计分小问。全部澄清均已标明不扣分：其原因是上下文已有正确机制，补充旨在限制简写或验证手段的证据范围，不为表述风格另造评分门槛。

### 本阶段末评语与能力判断

结论：**C19 阶段测验通过，稳定得分 100 / 100。** 本次没有发现需要扣分的核心概念错误、输出错误或实现缺陷；精度提醒已逐题显式记录。

你已能把 C16—C18 的名字、对象、绑定与调用时间线迁移到高级函数组合：能够解释注册与执行的分离，区分闭包环境独立和可变对象共享，比较默认参数与工厂修复的接口差异；也能按精确时点分析递归返回链、异常前效果和调用方赋值。F1 表明这些能力不只停留在输出预测，已经能组织成合同清楚的小型接口与聚焦实验。

能力判断：**中级入门前段已经稳固；C19 高级函数有限主干达到优秀，具备独立审查与实现小型高阶函数 API 的能力。** 满分针对本卷已定义范围，不代表已经完成 P4、掌握全部 Python 高级机制，或有限实验能证明任意第三方代码安全正确。

当前需要保留的精度纪律：

1. 浅拷贝前后相等不是“这次调用从未修改任何状态”的证明；要说明观察对象、时间点、共享层级和未覆盖路径。
2. “一个共享绑定”须指明具体名字；函数到配置对象的图若省略中间引用层，应明确是简写。
3. 属性查找失败与找到方法后执行失败是不同阶段；本题整数的 `strip` 在属性获取处就失败。
4. 路径测试补充实现审查，不能替代完整合同证明；不把补充验证提升成新的必学范围。

### 验证记录

- 解释器：项目 `.venv-py314\Scripts\python.exe`，CPython 3.14.5；验证使用 `-B -X utf8`，纯内存合成数据。
- A—E 的题干输出、规定变体及用户完整修复函数均已针对性验证；F1 原实现和四组实验全部通过，额外合同路径见 F1 审批。
- 原卷前 70382 字节的 SHA-256 与批改前基线一致，全部 11 个答案区的独立哈希也与批改前逐一吻合，提供题干和原答案未改写的强一致性证据。没有把追加批改与用户原始作答混写。
- Markdown 的 187 个围栏块全部闭合；全卷 6 分区、11 题、100 分标记与答案区配对有效。
- 技能 `validate_stage_quiz.py` 已运行，但整卷严格验证**未通过**：原答 L91、160、2389、2392、2395、2398 含行末双空格（Markdown 硬换行）；L679、688、716、1058、1345、1382、1577、1644、1662 的说明性 Python 片段不是独立模块。保留原答，不清理空格、不改围栏标签来伪造通过；这些不是用户完整实现的语法缺陷，不扣知识分。
- 95 个普通 Python 围栏中，86 个可独立编译，另外 9 个是上述有上下文的片段；只在内存中移除原答案内容再调用同一验证逻辑，题干加批改区视图通过（6 分区、11 题、11 个题干 Python 块）。这项分层检查不冒充整卷验证器通过。

### 学习画像更新

以下结论由已复核的分数与运行证据形成，供后续笔记和启动模板复用；画像文件同步状态在末尾单独记录。

- 阶段：`P4_Functions_and_Generators / C19_Advanced_Function_Topics`，`normal`；`quiz_review` 已完成，下一关卡为 `stage_note`。
- 稳定强项：函数引用与调用时点；管线／callback 的返回、异常和非回滚合同；闭包绑定独立与对象共享；晚绑定两种修复及调用接口差异；递归基线、进展量、调用局部状态；lambda 和注解的证据边界；小型高阶 API 实现与路径验证。
- 已改善的历史精度点：B1 明确区分已结束调用的局部形参与调用者后续绑定，C1/C2 引用方向及层级主干正确，D1 不把后续返回值提前倒填到当前局部绑定。
- 活跃薄弱点：本卷未发现主干误解；保留浅快照证据强度、间接引用图、属性查找阶段及测试覆盖范围的精度提醒，不把这些提醒标成未完成必学内容。
- 水平判断：中级入门前段已经稳固，C19 高级函数有限主干达到优秀；不由本卷外推未学的生成器函数、系统装饰器、完整类型工程或大型项目能力。
- 后续关注：先将 C19 证据沉淀为阶段笔记；以后进入 C20 时继续精确区分创建、实际执行、暂停／恢复与消费时点，不在本轮开始教学。
- 关卡：没有已排期 pre-quiz capstone；阶段笔记与最终收束尚未执行，尚未关闭 C19，也不生成下一章模板。

画像同步完成：`notes/Python_Learning_Profile.md` 已更新当前快照、C19 能力行、新历史评估、精度观察和下一关卡。此前历史评估正文经对照保持不变，历史成绩不变；未同步用户级 Codex memory。

最终文件检查：原答案保留、11 题覆盖、分数一致性、Markdown 围栏、新增内容无尾空格及画像当前状态均通过。`git diff --check` 仍仅报告用户原答的 6 处行末双空格，与严格考卷验证器的已说明格式限制一并保留，不报告成全量无警告。

工作区事实：本轮开始时考卷已因用户作答而处于 modified；本轮只在原卷之后追加批改记录，并按授权更新画像。相对 HEAD 的较大考卷差异含用户原始答案，不能视为本轮重写。未暂存、提交或清理其他文件；没有操作 `tests/`。

下一原子动作：在用户后续要求下，向 `notes/P4_Functions_and_Generators.md` 生成 C19 阶段末综合笔记。本轮停于审批与画像完成，未开始阶段笔记、最终收束、下一章模板或 C20 教学。

<!-- REVIEW_CURSOR:COMPLETE_NEXT_STAGE_NOTE -->
