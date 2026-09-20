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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

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

（在此作答。）

<!-- answer:end -->

## 交卷说明

完成后保留全部原始答案，告知可以批改。批改阶段才会建立逐题覆盖账本、记录分数和学习画像更新；本轮生成考卷不执行这些步骤。
