# Stage Quiz: while and for Loops

本测验用于当前小阶段：**while 与 for 循环：重复执行、控制流跳转、安全遍历和结构化扫描**。

它不只考循环语法，而是考你是否能把 C10/C11/C12 已经稳定掌握的“表达式求值、语句执行、名字绑定、对象修改、真值测试和控制流选择”模型，推进到 C13 的重复执行场景：循环条件或迭代来源如何产生下一步，每一轮循环体中哪些副作用发生，`break` / `continue` 如何改变路径，循环 `else` 何时执行，以及遍历过程中修改容器时有哪些风险。

总分：100 分。

答题规则：

1. 第一遍不要运行代码，先写预测、循环次数、输出顺序、最终绑定对象、副作用和理由。
2. 第二遍可以用当前日常学习环境 Python `3.14.5` 验证，并标注“验证前预测”和“验证后修正”。
3. 每道代码题尽量按这条链解释：循环开始前哪些表达式先求值；每轮条件或迭代器如何产生下一步；循环变量绑定到哪个对象；本轮哪些赋值、原地修改、输出副作用发生；`continue` 跳过哪些语句；`break` 终止哪一层循环；循环 `else` 是否执行。
4. 本卷不包含参考答案。你作答后交给我审批，我会保留你的原答案并追加批改记录。
5. 若你认为题目本身有歧义，可以直接指出；这也属于本阶段能力的一部分。

---

## A. 概念边界：循环、迭代、跳转与副作用（15 分）

### A1. 循环说法纠偏（6 分）

逐条判断下面说法是否准确；若不准确，请改写成更精确的说法。

```tex
1. while 条件只在第一次进入循环前检查一次。
2. continue 会结束整个循环。
3. break 会跳出当前循环，并且该循环的 else 不会执行。
4. for item in items 会把每个元素复制一份给 item。
5. zip(a, b) 默认会在较短输入耗尽时停止；zip(a, b, strict=True) 可以暴露长度不一致。
6. 循环后的变量一定能安全代表“找到的目标记录”。
```

要求至少说明：

1. `while` 条件每轮重新求值；
2. `break`、`continue`、循环 `else` 的控制流差异；
3. 循环变量绑定与对象复制的区别；
4. 循环结束后直接使用循环变量的风险。

答题区：

```tex
验证前预测：

1. “while 条件只在第一次进入循环前检查一次。”这个说法不准确。更精确的说法：
while 条件会在每一轮循环开始前重新求值，并对求值结果做真值测试。只要本轮条件为真，就进入循环体；如果某一轮条件为假，循环结束。因此 while 循环体中通常必须有某种状态变化，否则可能出现无限循环。
例如：
while n < 3:
    ...
这里的 n < 3 不是只检查一次，而是每轮都重新计算。
2. “continue 会结束整个循环。”这个说法不准确。更精确的说法：
continue 只结束当前这一轮循环体的剩余部分，然后回到当前循环的下一轮判断或下一次迭代。它不会终止整个循环。在 while 中，continue 会跳回循环头重新判断条件；在 for 中，continue 会进入下一次从迭代器取值的过程。若 while 中的 continue 跳过了状态推进语句，例如跳过 index += 1，就可能造成无限循环。
3. “break 会跳出当前循环，并且该循环的 else 不会执行。”这个说法准确。更完整的说法：
break 会立即终止当前所在的这一层循环，并跳到该循环之后继续执行。如果循环是因为 break 提前终止的，那么与该循环配套的 else 子句不会执行。注意：嵌套循环中，内层 break 只终止内层循环，不会自动终止外层循环，也不会自动阻止外层循环的 else。
4. “for item in items 会把每个元素复制一份给 item。”这个说法不准确。更精确的说法：
for item in items 每轮是把循环变量 item 绑定到当前迭代得到的元素对象，而不是复制元素对象。若元素是可变对象，item 和容器中的元素可能引用同一个对象。对 item 重新赋值只是让 item 重新绑定，不会修改容器；但如果通过 item 原地修改可变对象，例如 item["status"] = "bad"，容器中对应对象也会体现变化。
5. “zip(a, b) 默认会在较短输入耗尽时停止；zip(a, b, strict=True) 可以暴露长度不一致。”这个说法准确。更完整的说法：
普通 zip(a, b) 会并行取值，但默认在最短输入耗尽时停止，因此较长输入尾部数据会被静默忽略。在本地化资源中，如果 key 列和 target 列本应一一对应，这种静默截断可能隐藏数据缺失。zip(a, b, strict=True) 会在输入长度不一致时抛出 ValueError，更适合需要强对齐的数据扫描场景。
6. “循环后的变量一定能安全代表‘找到的目标记录’。”这个说法不准确。更精确的说法：
循环变量在循环结束后通常仍然保留最后一次绑定，但它不一定代表“找到的目标记录”。如果循环自然结束，它可能只是最后一条被遍历的记录；如果循环体零次执行，循环变量甚至可能没有被绑定，或保留外层旧绑定。因此如果要表达“是否找到目标”，更稳妥的写法是使用 found 标志、result 变量、break/else 结构，或在函数中 return 明确结果，而不是无条件依赖循环后的循环变量。

验证后修正：

无需修正。
```

### A2. `for` 遍历、迭代器与可重复遍历（5 分）

解释下面几类对象在 `for` 循环中的行为差异：

```tex
1. list
2. dict
3. set
4. file object
5. zip object
```

要求至少说明：

1. 哪些通常可以重复遍历，哪些通常会被逐步消耗；
2. 遍历 `dict` 时默认得到什么；
3. 为什么 `set` 的遍历顺序不适合当成业务顺序；
4. 为什么文件对象通常不建议在同一个循环中边读边写；
5. 如果报告需要稳定顺序，你会如何处理 `set` 或字典键集合。

答题区：

```tex
验证前预测：

1. list
list 是可迭代对象。每次执行 for item in some_list，都会基于这个列表创建新的迭代过程，因此通常可以重复遍历同一个 list。列表有稳定的位置顺序，遍历顺序就是当前列表元素顺序。不过，如果在遍历过程中删除或插入元素，列表迭代器大致按内部索引推进，容易造成跳过元素、重复处理或逻辑混乱。
2. dict
dict 是可迭代对象。for key in some_dict 默认遍历的是字典的 key，而不是 value 或 key-value pair。若要同时取 key 和 value，应使用 some_dict.items()。现代 Python 字典保留插入顺序，因此遍历字典时会按 key 的插入顺序产生 key。字典通常可以重复遍历，但遍历时不应增删 key，因为这会改变字典大小和 key 集合，可能触发 RuntimeError: dictionary changed size during iteration。
3. set
set 是可迭代对象，但 set 是无序集合，普通 set 的遍历顺序不应被当作业务顺序依赖。set 的主要语义是成员唯一性、快速成员测试和集合运算，而不是保留插入顺序。报告如果直接遍历 set，输出顺序可能不稳定，不利于日志、测试、CI 和人工复查。需要稳定报告时，应使用 sorted(some_set)。
4. file object
文件对象是可迭代对象，文本文件对象在 for line in f 中通常逐行产生字符串。文件对象与 list 不同，它依赖当前文件位置；遍历一次后，文件位置通常到达 EOF。若不 seek(0)，第二次继续遍历通常得不到内容。因此文件对象属于会被逐步消费的流式对象。同一个循环里边读边写同一个文件不建议，因为读写共享文件位置、缓冲区和 EOF 状态，还可能有追加语义，容易造成漏读、重复读、看不到刚写入内容或自增长扫描。
5. zip object
zip(...) 返回的是惰性的迭代器式对象。它会按需并行从多个输入中取下一项。zip 对象通常会被逐步消费，遍历一次后就耗尽，第二次遍历同一个 zip 对象通常没有内容。若需要重复使用，应重新创建 zip(...)，或显式转换为 list(zip(...)) 保存结果。
关于稳定顺序处理：
如果报告来自原始文件行，应保留原始 line_no 和扫描顺序；如果报告只是展示缺失 key 集合、额外 key 集合等集合式结果，应使用 sorted(...) 得到稳定、可复现的顺序。例如：
for key in sorted(missing_keys):
    ...

验证后修正：

无需修正。
```

### A3. 循环内副作用与结构化结果（4 分）

下面两种写法都可能“工作”，但工程含义不同。请比较它们。

```python
for record in records:
    print("checking", record["key"])
    if not record["target"]:
        print("empty target")
```

```python
issues = []

for record in records:
    if not record["target"]:
        issues.append((record["key"], "empty target"))
```

要求至少说明：

1. `print()` 在这里是什么副作用；
2. `issues.append(...)` 修改了哪个对象；
3. 为什么阶段项目或本地化审计工具更倾向返回结构化数据；
4. 人读输出和机器可读结果如何分层。

答题区：

```tex
验证前预测：

第一段代码：

for record in records:
    print("checking", record["key"])
    if not record["target"]:
        print("empty target")

这里的 print() 是输出副作用。它把信息写到标准输出，让人可以在终端中看到当前扫描状态，但它本身不会形成可复用的数据结构。print() 的返回值是 None，真正有意义的是它造成的 stdout 输出副作用。输出给人看是有用的，但不适合后续程序继续加工、过滤、排序、导出 JSON/CSV 或进行测试断言。
第二段代码：

issues = []

for record in records:
    if not record["target"]:
        issues.append((record["key"], "empty target"))

这里 issues.append(...) 修改的是 issues 这个列表对象本身。它把结构化问题记录追加到列表中。每条 issue 由 key 和问题类型组成，后续程序可以继续统计、排序、写入报告文件、转换为 JSON，或在单元测试中断言 issues 是否等于预期结果。
阶段项目或本地化审计工具更倾向返回结构化数据是因为：
1. 可以让机器继续处理；
2. 可以统一生成报告；
3. 可以测试；
4. 可以按严重程度、行号、key 排序；
5. 可以区分 warning、fatal_error、valid_records、stats 等不同结果；
6. 可以把核心扫描逻辑和展示逻辑分离。
更好的分层方式是：
核心扫描函数不直接 print，而是返回 report，例如：
{
    "issues": [...],
    "fatal_error": ...,
    "stats": {...},
    "valid_records": [...]
}
然后在外层展示层决定：
1. 是否 print 给人看；
2. 是否写入文件；
3. 是否 dry_run；
4. 是否导出 JSON/CSV；
5. 是否在 CI 中失败。

验证后修正：

无需修正。
```

---

## B. `while`、动态状态、`break` / `continue`（16 分）

### B1. 动态队列与 `while` 条件重新求值（8 分）

预测完整输出，并写出循环结束后各变量的最终值。

```python
queue = ["scan", "normalize", "scan", "report"]
seen = set()
processed = []
skipped = 0
round_no = 0

while queue:
    round_no += 1
    command = queue.pop(0)
    print("round", round_no, "command", command, "queue", queue)

    if command in seen:
        skipped += 1
        print("skip duplicate", command)
        continue

    seen.add(command)

    if command == "normalize":
        queue.append("validate")

    if command == "report":
        print("stop before validate?")
        break

    processed.append(command)
else:
    print("all commands consumed")

print("processed", processed)
print("seen", sorted(seen))
print("skipped", skipped)
print("queue", queue)
```

要求至少说明：

1. `while queue:` 每一轮检查的对象是什么；
2. `queue.pop(0)` 和 `queue.append(...)` 如何影响后续循环；
3. 第几个 `scan` 会触发 `continue`，它跳过了哪些语句；
4. `report` 触发 `break` 后，循环 `else` 是否执行；
5. `validate` 是否会被处理，原因是什么。

答题区：

```tex
验证前预测：

【完整输出】
round 1 command scan queue ['normalize', 'scan', 'report']
round 2 command normalize queue ['scan', 'report']
round 3 command scan queue ['report', 'validate']
skip duplicate scan
round 4 command report queue ['validate']
stop before validate?
processed ['scan', 'normalize']
seen ['normalize', 'report', 'scan']
skipped 1
queue ['validate']
【关键解释】
1. while queue: 每一轮检查的对象是什么？
while queue: 每一轮都会对 queue 这个列表对象做真值测试。空列表为 False，非空列表为 True。这里 queue 是动态变化的列表，每轮开始前都会重新检查当前 queue 是否非空，而不是只检查初始 queue。
2. queue.pop(0) 和 queue.append(...) 如何影响后续循环？
queue.pop(0) 会原地删除并返回列表第 0 个元素，因此队列头部元素被取出，后面的元素左移。queue.append("validate") 会在列表末尾追加新命令，可能让后续循环多处理一个动态生成的命令。
逐轮看：
初始 queue = ["scan", "normalize", "scan", "report"]
第 1 轮：
pop(0) 得到 "scan"，queue 变为 ["normalize", "scan", "report"]。"scan" 不在 seen，加入 seen。不是 normalize，不追加 validate。不是 report，不 break。processed 加入 "scan"。
第 2 轮：
pop(0) 得到 "normalize"，queue 变为 ["scan", "report"]。"normalize" 不在 seen，加入 seen。command == "normalize"，追加 "validate"。queue 变为 ["scan", "report", "validate"]。不是 report，不 break。processed 加入 "normalize"。
第 3 轮：
pop(0) 得到第二个 "scan"，queue 变为 ["report", "validate"]。"scan" 已经在 seen 中，触发 duplicate 分支。skipped += 1，打印 skip duplicate scan。continue 触发，跳过 seen.add(command)、normalize 判断、report 判断和 processed.append(command)。
第 4 轮：
pop(0) 得到 "report"，queue 变为 ["validate"]。"report" 不在 seen，加入 seen。不是 normalize，不追加 validate。command == "report"，打印 stop before validate?，然后 break。
3. 第几个 scan 会触发 continue，跳过了哪些语句？
第二个 scan，也就是第 3 轮的 command == "scan"，会触发 continue。它跳过了本轮后面的：
seen.add(command)
if command == "normalize": ...
if command == "report": ...
processed.append(command)
因此第二个 scan 不会被再次加入 processed，也不会再次加入 seen。
4. report 触发 break 后，循环 else 是否执行？
不执行。while...else 的 else 只在循环没有被 break 提前终止时执行。这里第 4 轮 report 触发 break，所以不会输出 all commands consumed。
5. validate 是否会被处理，原因是什么？
不会。validate 是在 normalize 那一轮追加到 queue 末尾的，但 report 在 validate 前面。第 4 轮先取出 report 并触发 break，循环直接结束，剩余 queue 仍然是 ["validate"]，所以 validate 没有机会被处理。
【最终变量】
processed == ["scan", "normalize"]
seen == {"scan", "normalize", "report"}，打印 sorted(seen) 得到 ['normalize', 'report', 'scan']
skipped == 1
queue == ["validate"]
round_no == 4
command 最后绑定到 "report"

验证后修正：

无需修正。
```

### B2. 哨兵循环与计数口径（4 分）

阅读代码，预测最终 `report`，并说明 `total`、`processed`、`empty` 的统计口径。

```python
commands = ["scan", "", "normalize", "QUIT", "report"]

index = 0
report = {
    "total": 0,
    "processed": [],
    "empty": 0,
    "stopped_by": None,
}

while index < len(commands):
    command = commands[index]
    index += 1
    report["total"] += 1

    if command == "QUIT":
        report["stopped_by"] = command
        break

    if not command:
        report["empty"] += 1
        continue

    report["processed"].append(command)

print(report)
print("index", index)
```

要求至少说明：

1. `index += 1` 放在 `break` 判断之前有什么影响；
2. 空字符串命中 `continue` 后跳过了什么；
3. `"report"` 是否会被处理；
4. 如果把 `report["total"] += 1` 放到空字符串判断之后，统计口径会怎样变化。

答题区：

```tex
验证前预测：

【完整输出】
{'total': 4, 'processed': ['scan', 'normalize'], 'empty': 1, 'stopped_by': 'QUIT'}
index 4
【关键解释】
初始：
commands = ["scan", "", "normalize", "QUIT", "report"]
index = 0
report["total"] = 0
report["processed"] = []
report["empty"] = 0
report["stopped_by"] = None
第 1 轮：
index < len(commands) 为 True。
command = commands[0] -> "scan"。
index += 1 后 index == 1。
total += 1 后 total == 1。
command 不是 "QUIT"，也不是空字符串。
processed 追加 "scan"。
第 2 轮：
index < len(commands) 为 True。
command = commands[1] -> ""。
index += 1 后 index == 2。
total += 1 后 total == 2。
command 不是 "QUIT"，是空字符串，所以 not command 为 True，因为空字符串是假值。
empty += 1 后 empty == 1。
continue 触发，跳过 processed.append(command)，所以空字符串不会进入 processed。
第 3 轮：
index < len(commands) 为 True。
command = commands[2] -> "normalize"。
index += 1 后 index == 3。
total += 1 后 total == 3。
command 不是 "QUIT"，也不是空字符串。
processed 追加 "normalize"。
第 4 轮：
index < len(commands) 为 True。
command = commands[3] -> "QUIT"。
index += 1 后 index == 4。
total += 1 后 total == 4。
command == "QUIT"，设置 stopped_by 为 "QUIT"，然后 break。循环结束。
"report" 不会被处理，因为它位于 "QUIT" 之后，break 直接终止 while 循环。
1. index += 1 放在 break 判断之前有什么影响？
这意味着即使当前命令是 "QUIT"，index 也已经先前进到下一个位置。因此遇到 "QUIT" 后，index 最终是 4，表示已经取过 commands[3]。如果 index += 1 放在 break 判断之后，那么遇到 "QUIT" 时可能不会前进，最终 index 会停在 3。
2. 空字符串命中 continue 后跳过了什么？
空字符串命中 not command 后，empty += 1，然后 continue。它跳过的是后面的 report["processed"].append(command)，所以空字符串只计入 empty，不计入 processed。
3. "report" 是否会被处理？
不会。因为第 4 轮遇到 "QUIT" 后 break，while 循环结束，commands[4] 的 "report" 没有机会被读取。
4. 如果把 report["total"] += 1 放到空字符串判断之后，统计口径会怎样变化？
当前 total 表示“已经读取/检查过的命令数量”，包括空字符串和 "QUIT"，所以 total == 4。如果把 report["total"] += 1 放到空字符串判断之后，并且仍放在 QUIT 判断之后，那么空字符串可能不会计入 total，甚至 QUIT 也可能不会计入 total，具体取决于移动后的位置。若放在 not command 分支之后、processed.append 之前，则 total 更像“非空且非 QUIT 的普通命令检查数”，空字符串不再计入；如果也在 QUIT 判断之后，QUIT 也不计入。这样 total 就不再表示“读过多少条命令”，而变成“通过前置过滤、准备处理的命令数量”。因此位置变化会改变统计口径，必须用命名或注释说明清楚。

验证后修正：

无需修正。
```

### B3. `break` 后统一收尾 vs 循环中直接 `return`（4 分）

下面两个函数都试图扫描记录。请比较它们的返回结构稳定性。

```python
def scan_with_break(records):
    report = {
        "completed": True,
        "issues": [],
        "fatal_error": None,
    }

    for record in records:
        if "key" not in record:
            report["completed"] = False
            report["fatal_error"] = "missing key"
            break

        if not record.get("target"):
            report["issues"].append((record["key"], "empty target"))
            continue

    report["issue_count"] = len(report["issues"])
    return report
```

```python
def scan_with_return(records):
    report = {
        "completed": True,
        "issues": [],
        "fatal_error": None,
    }

    for record in records:
        if "key" not in record:
            report["completed"] = False
            report["fatal_error"] = "missing key"
            return report

        if not record.get("target"):
            report["issues"].append((record["key"], "empty target"))
            continue

    report["issue_count"] = len(report["issues"])
    return report
```

要求至少说明：

1. 两个函数遇到缺少 `"key"` 的记录时分别如何退出；
2. 哪个函数更容易保证返回结构一致；
3. 什么时候“循环中直接 `return`”仍然是合理选择；
4. 如果这是本地化资源扫描工具，你更推荐哪种写法，为什么。

答题区：

```tex
验证前预测：

1. 两个函数遇到缺少 "key" 的记录时分别如何退出？
scan_with_break:
遇到缺少 "key" 的记录时，会执行：

report["completed"] = False
report["fatal_error"] = "missing key"
break

注意到：这里的 break 只结束 for 循环。函数不会立即返回，而是继续执行循环后的统一收尾逻辑：

report["issue_count"] = len(report["issues"])
return report

所以即使遇到 fatal error，返回的 report 也包含 issue_count 字段。
scan_with_return:
遇到缺少 "key" 的记录时，会执行：

report["completed"] = False
report["fatal_error"] = "missing key"
return report

注意到：这里的 return 会立即结束整个函数。循环后的统一收尾逻辑：

report["issue_count"] = len(report["issues"])
return report

不会执行。因此 fatal error 路径返回的 report 没有 issue_count 字段。
2. 哪个函数更容易保证返回结构一致？
scan_with_break 更容易保证返回结构一致。因为所有路径都会先跳出循环，然后经过统一收尾逻辑补齐 issue_count。scan_with_return 有多个函数出口，如果每个 return 前没有手动补齐字段，就容易出现不同路径返回的 report 结构不一致这样的现象。
3. 什么时候“循环中直接 return”仍然是合理选择？
如果函数本质是搜索型函数，例如“找到第一个符合条件的记录就返回”，直接 return 很合理。比如 find_first_missing_key(records) 找到缺 key 记录就立即返回结果，不需要统一统计和完整报告。函数很短、返回结构简单、没有统一收尾需求时，早 return 可以减少嵌套并让意图更直接。
4. 如果这是本地化资源扫描工具，我更推荐哪种写法，为什么？
更推荐 break 后统一收尾。因为本地化扫描工具通常要返回结构化 report，包括 completed、issues、fatal_error、issue_count、stats、valid_records 等字段。即使遇到 fatal error 停止扫描，也应该保证报告结构稳定，方便调用者、测试代码、日志导出和 UI 展示统一处理。break 表示“停止扫描”，但函数仍可继续整理 report；return 表示“整个函数立即结束”，容易绕过收尾逻辑。

验证后修正：

无需修正。
```
---

## C. `for`、`enumerate()`、`zip()` 与文件行扫描（17 分）

### C1. `enumerate()`、行号与原始顺序（5 分）

预测完整输出，并说明每条记录的行号如何产生。

```python
lines = [
    "menu.start=Start\n",
    "\n",
    "menu.exit=\n",
    "mail.reward=Reward: {count}\n",
]

issues = []
pairs = []

for line_no, raw_line in enumerate(lines, start=1):
    line = raw_line.rstrip("\n")
    print("line", line_no, repr(line))

    if not line:
        issues.append((line_no, "empty line"))
        continue

    key, target = line.split("=", 1)

    if not target:
        issues.append((line_no, key, "empty target"))
        continue

    pairs.append((line_no, key, target))

print("pairs", pairs)
print("issues", issues)
```

要求至少说明：

1. `enumerate(lines, start=1)` 每轮产生什么；
2. 为什么这里用 `rstrip("\n")` 而不是直接 `strip()`；
3. `split("=", 1)` 的作用是什么；
4. 空行和空译文分别如何进入 `issues`；
5. `pairs` 为什么保留 `line_no`。

答题区：

```tex
验证前预测：

【完整输出】
line 1 'menu.start=Start'
line 2 ''
line 3 'menu.exit='
line 4 'mail.reward=Reward: {count}'
pairs [(1, 'menu.start', 'Start'), (4, 'mail.reward', 'Reward: {count}')]
issues [(2, 'empty line'), (3, 'menu.exit', 'empty target')]
【关键解释】
1. enumerate(lines, start=1) 每轮产生什么？
enumerate(lines, start=1) 每轮产生一个二元组：
第 1 轮：(1, "menu.start=Start\n")
第 2 轮：(2, "\n")
第 3 轮：(3, "menu.exit=\n")
第 4 轮：(4, "mail.reward=Reward: {count}\n")
循环头：
for line_no, raw_line in enumerate(...):
会把行号绑定到 line_no，把原始行字符串绑定到 raw_line。
2. 为什么这里用 rstrip("\n") 而不是直接 strip()？
rstrip("\n") 只去掉文件行尾换行符，不会删除 key 或 target 中真实存在的前后空白。strip() 会删除左右所有空白字符，可能把本应被审计的空格删掉，从而把 blank 和 empty 混淆。虽然本题没有纯空格 target，但在本地化审计中保留原始空格非常重要。
3. split("=", 1) 的作用是什么？
split("=", 1) 只按第一个等号拆分成 key 和 target。这样如果 target 中包含额外的 "="，不会被继续拆碎。它适合解析 key=value 格式的目标字符串。
4. 空行和空译文分别如何进入 issues？
第 2 行 raw_line 为 "\n"，rstrip 后 line == ""，命中 if not line，加入：
(2, "empty line")
然后 continue，跳过 split。
第 3 行 raw_line 为 "menu.exit=\n"，rstrip 后 line == "menu.exit="，不是空行。split 后 key == "menu.exit"，target == ""，命中 if not target，加入：
(3, "menu.exit", "empty target")
然后 continue，不加入 pairs。
5. pairs 为什么保留 line_no？
因为报告要帮助用户定位原始文件位置。即使后续对 pairs 排序或过滤，line_no 仍然能指向原始输入第几行。报告“第几行有问题”时，原始顺序和原始行号是业务信息，不应该丢失。

验证后修正：

无需修正。
```

### C2. `zip()` 默认截断与 `strict=True`（6 分）

阅读两段代码，分别预测输出或异常。

代码一：

```python
source_keys = ["menu.start", "menu.exit", "mail.reward"]
target_texts = ["开始", "退出"]

pairs = []

for key, target in zip(source_keys, target_texts):
    pairs.append((key, target))

print(pairs)
```

代码二：

```python
source_keys = ["menu.start", "menu.exit", "mail.reward"]
target_texts = ["开始", "退出"]

pairs = []

try:
    for key, target in zip(source_keys, target_texts, strict=True):
        pairs.append((key, target))
except ValueError as exc:
    print(type(exc).__name__)
    print("partial", pairs)
```

要求至少说明：

1. 普通 `zip()` 为什么可能隐藏数据缺失；
2. `strict=True` 在本地化资源对齐场景中有什么价值；
3. 异常发生前 `pairs` 中已经有什么；
4. 为什么这不等于事务式“全部成功或全部失败”。

答题区：

```tex
验证前预测：

【代码一输出】
[('menu.start', '开始'), ('menu.exit', '退出')]
【代码二输出】
ValueError
partial [('menu.start', '开始'), ('menu.exit', '退出')]
【关键解释】
1. 普通 zip() 为什么可能隐藏数据缺失？
普通 zip(source_keys, target_texts) 会在较短的 target_texts 耗尽时停止。source_keys 里第三个 "mail.reward" 没有对应 target，但普通 zip 不报错，直接静默丢弃这一项。因此它可能隐藏本地化资源的列长度不一致、漏译或数据缺失问题。
2. strict=True 在本地化资源对齐场景中有什么价值？
zip(..., strict=True) 要求所有输入同时耗尽。如果 key 列和 target 列本应一一对应，那么 strict=True 可以尽早暴露长度不一致，而不是让尾部 key 被静默忽略。在资源审计中，这比普通 zip 更安全。
3. 异常发生前 pairs 中已经有什么？
异常发生前，前两对已经成功产生并 append：
[('menu.start', '开始'), ('menu.exit', '退出')]
然后 zip 尝试继续取第三对时，source_keys 还有 "mail.reward"，target_texts 已经耗尽，于是抛出 ValueError。
4. 为什么这不等于事务式“全部成功或全部失败”？
因为 pairs 在异常发生前已经被部分修改了。前两次 append 已经发生，异常不会自动回滚 pairs。因此 zip(strict=True) 能暴露错误，但它不是事务机制。如果需要全部成功后才提交结果，应先构造临时列表，完整成功后再赋值或提交。

验证后修正：

无需修正。
```

### C3. 文件对象、一次性消费与重新读取（6 分）

不需要真的创建磁盘文件。阅读下面使用 `StringIO` 模拟文本文件的代码，预测输出并解释。

```python
from io import StringIO

stream = StringIO("a=1\nb=2\n")

first_pass = []

for line in stream:
    first_pass.append(line.rstrip("\n"))

second_pass = []

for line in stream:
    second_pass.append(line.rstrip("\n"))

stream.seek(0)

third_pass = []

for line in stream:
    third_pass.append(line.rstrip("\n"))

print("first", first_pass)
print("second", second_pass)
print("third", third_pass)
```

要求至少说明：

1. 第一次 `for line in stream` 后，文件位置发生了什么；
2. 第二次遍历为什么得不到同样内容；
3. `seek(0)` 的作用是什么；
4. 真实文件对象和这里的 `StringIO` 在这个例子中的共同点；
5. 为什么“边遍历文件边写同一个文件”通常不是好主意。

答题区：

```tex
验证前预测：

【完整输出】
first ['a=1', 'b=2']
second []
third ['a=1', 'b=2']
【关键解释】
1. 第一次 for line in stream 后，文件位置发生了什么？
第一次 for line in stream 会从当前位置开始逐行读取，直到读到 EOF。读取结束后，stream 的当前位置已经在文件末尾。
2. 第二次遍历为什么得不到同样内容？
第二次 for line in stream 从当前文件位置继续读。由于第一次遍历已经把位置推进到末尾，当前位置已经是 EOF，所以第二次没有新行可读，second_pass 为空列表。
3. seek(0) 的作用是什么？
stream.seek(0) 把当前位置移动回文件开头。之后第三次 for line in stream 又能从头读到 "a=1\n" 和 "b=2\n"，所以 third_pass 得到 ['a=1', 'b=2']。
4. 真实文件对象和这里的 StringIO 在这个例子中的共同点是什么？
二者都像流一样维护当前读取位置。for line in stream / for line in file 都会随着读取推进当前位置；读取到末尾后，如果不显式的 seek(0)，再次从同一对象遍历通常得不到有效内容。
5. 为什么“边遍历文件边写同一个文件”通常不是好主意？
文件对象的迭代依赖当前位置、缓冲区和 EOF 状态。边读边写同一个文件会让读写位置、缓冲刷新、追加语义、是否能看到刚写入内容等问题混在一起，容易导致漏读、重复读、读不到刚写入内容，甚至形成不断追加又读取的自增长扫描。工程上更推荐分阶段处理：先读，分析生成结构化结果，再写报告或写新文件。

验证后修正：

无需修正。
```

---

## D. 循环变量绑定、原地修改与新容器（16 分）

### D1. 循环变量不是元素副本（6 分）

预测完整输出，并说明 `records`、`valid`、`record` 之间的对象关系。

```python
records = [
    {"key": "menu.start", "target": "Start"},
    {"key": "menu.exit", "target": ""},
]

valid = []
issues = []

for record in records:
    if not record["target"]:
        issues.append((record["key"], "empty target"))
        continue

    valid.append(record)
    record["target"] = record["target"].upper()

print("records", records)
print("valid", valid)
print("issues", issues)

valid[0]["target"] = "BEGIN"

print("records after", records)
print("valid after", valid)
```

要求至少说明：

1. `for record in records` 每轮把 `record` 绑定到什么；
2. `valid.append(record)` 追加的是对象本身还是副本；
3. `record["target"] = ...` 修改的是哪个字典对象；
4. `valid[0]["target"] = "BEGIN"` 为什么会影响 `records`；
5. 如果你希望 `valid` 是独立报告条目，应如何改写。

答题区：

```tex
验证前预测：

【完整输出】
records [{'key': 'menu.start', 'target': 'START'}, {'key': 'menu.exit', 'target': ''}]
valid [{'key': 'menu.start', 'target': 'START'}]
issues [('menu.exit', 'empty target')]
records after [{'key': 'menu.start', 'target': 'BEGIN'}, {'key': 'menu.exit', 'target': ''}]
valid after [{'key': 'menu.start', 'target': 'BEGIN'}]
【关键解释】
1. for record in records 每轮把 record 绑定到什么？
第 1 轮，record 绑定到 records[0] 中的字典对象：
{"key": "menu.start", "target": "Start"}
第 2 轮，record 绑定到 records[1] 中的字典对象：
{"key": "menu.exit", "target": ""}
要注意的是，这里的 record 绑定的对象不是元素副本，而是列表中的元素对象本身。
2. valid.append(record) 追加的是对象本身还是副本？
valid.append(record) 追加的是当前 record 绑定的字典对象引用，不是副本。第 1 条记录有效时，valid[0] 和 records[0] 其实指向同一个字典对象。
3. record["target"] = ... 修改的是哪个字典对象？
第 1 轮中：
record["target"] = record["target"].upper()
修改的是 records[0] 那个字典对象本身，把 "Start" 改成 "START"。由于 valid[0] 与 records[0] 是同一个对象，所以 valid 中也看到 "START"。
第 2 条 target 是空字符串，命中 issues.append(...) 后 continue，因此不会 append 到 valid，也不会修改 target。
4. valid[0]["target"] = "BEGIN" 为什么会影响 records？
因为 valid[0] 和 records[0] 引用的是同一个字典对象。通过 valid[0] 修改这个字典的 "target"，也就是修改 records[0] 所指向的同一个对象，所以 records after 中第一条 target 变为 "BEGIN"。
5. 如果希望 valid 是独立报告条目，应如何改写？
应该构造新字典，而不是直接 append 原始 record。例如：
valid.append({
    "key": record["key"],
    "target": record["target"],
})
这样 valid 中的字典是新对象，不共享原始记录字典。若原始记录包含嵌套可变对象，还需要根据需求使用浅拷贝、深拷贝或显式构造嵌套结构。

验证后修正：

无需修正。
```

### D2. 构造新容器保留干净结果（5 分）

下面代码试图从原始记录中筛出有效记录，同时不修改输入。请阅读并回答。

```python
records = [
    {"key": "menu.start", "target": " Start "},
    {"key": "menu.exit", "target": ""},
    {"key": "mail.reward", "target": "Reward: {count}"},
]

valid_records = []
issues = []

for record in records:
    key = record["key"]
    target = record["target"].strip()

    if not target:
        issues.append((key, "empty target"))
        continue

    valid_records.append({
        "key": key,
        "target": target,
    })

print(records)
print(valid_records)
print(issues)
```

要求至少说明：

1. `strip()` 返回的新字符串对象是否会自动写回 `record["target"]`；
2. `valid_records.append({...})` 为什么不会共享原始字典对象；
3. 原始 `records` 中第 1 条记录的 `"target"` 最终是否仍带空格；
4. 这种写法在报告生成中有什么好处；
5. 如果原始记录里还有嵌套可变对象，这种“新字典”是否天然等于深拷贝。

答题区：

```tex
验证前预测：

【完整输出】
[{'key': 'menu.start', 'target': ' Start '}, {'key': 'menu.exit', 'target': ''}, {'key': 'mail.reward', 'target': 'Reward: {count}'}]
[{'key': 'menu.start', 'target': 'Start'}, {'key': 'mail.reward', 'target': 'Reward: {count}'}]
[('menu.exit', 'empty target')]
【关键解释】
1. strip() 返回的新字符串对象是否会自动写回 record["target"]？
不会。target = record["target"].strip() 会产生一个去掉前后空白的新字符串对象，并把局部名字 target 绑定到这个新字符串。它不会自动修改 record["target"]。字符串本身也是不可变对象，strip() 返回的是处理后的结果。
2. valid_records.append({...}) 为什么不会共享原始字典对象？
因为 append 的是一个新创建的字典：
{
    "key": key,
    "target": target,
}
这个字典对象不是原始 record。因此 valid_records 中的记录不会与 records 中的原始字典共享同一个外层字典对象。
3. 原始 records 中第 1 条记录的 "target" 最终是否仍带空格？
是。原始 records[0]["target"] 仍然是 " Start "，因为 strip() 的结果只保存在局部变量 target 中，又被放进新字典 valid_record 中，没有写回原始 records。
4. 这种写法在报告生成中有什么好处？
它把输入数据和输出结果分离。原始 records 保留原貌，valid_records 保存清洗后的干净结果，issues 保存问题。这样更适合审计、调试和生成报告，因为可以同时知道原始输入是什么、清洗结果是什么、哪些记录有问题。
5. 如果原始记录里还有嵌套可变对象，这种“新字典”是否天然等于深拷贝？
不一定。这里新建了外层字典，但如果把原始记录里的嵌套列表、嵌套字典直接放进去，那么嵌套对象仍可能共享引用。这种写法不是天然深拷贝。若需要完全独立的嵌套结构，应显式复制嵌套对象，或使用 copy.deepcopy，但工程上更推荐根据字段语义手动构造需要的报告结构。

验证后修正：

无需修正。
```

### D3. 嵌套循环与占位符检查（5 分）

预测 `issues` 的最终内容，并说明内外层循环分别负责什么。

```python
records = [
    {
        "key": "mail.reward",
        "source_placeholders": ["{player}", "{count}"],
        "target": "奖励：{count}",
    },
    {
        "key": "menu.start",
        "source_placeholders": [],
        "target": "开始",
    },
]

issues = []

for record in records:
    missing = []

    for placeholder in record["source_placeholders"]:
        if placeholder not in record["target"]:
            missing.append(placeholder)

    if missing:
        issues.append((record["key"], "missing placeholders", missing))

print(issues)
```

要求至少说明：

1. 外层循环每轮处理什么；
2. 内层循环每轮处理什么；
3. 为什么 `missing = []` 要放在外层循环体内部；
4. 最终 `issues` 中的 `missing` 是哪个列表对象；
5. 如果把 `missing = []` 放到外层循环之前，会产生什么风险。

答题区：

```tex
验证前预测：

【完整输出】
[('mail.reward', 'missing placeholders', ['{player}'])]
【关键解释】
1. 外层循环每轮处理什么？
外层循环 for record in records 每轮处理一条资源记录。第 1 轮处理 key 为 "mail.reward" 的记录；第 2 轮处理 key 为 "menu.start" 的记录。
2. 内层循环每轮处理什么？
内层循环 for placeholder in record["source_placeholders"] 每轮处理当前记录要求保留的一个占位符。第 1 条记录的 source_placeholders 是 ["{player}", "{count}"]，所以内层依次检查 "{player}" 和 "{count}" 是否出现在 target 中。第 2 条记录的 source_placeholders 是空列表，内层循环零次执行。
3. 为什么 missing = [] 要放在外层循环体内部？
因为 missing 应该表示“当前这一条记录缺失的占位符”。每处理一条新记录，都应该从空列表开始收集。如果 missing 放在外层循环之前，就会把上一条记录的缺失结果带到下一条记录，造成污染。
4. 最终 issues 中的 missing 是哪个列表对象？
issues 中的第三个元素 missing 是第 1 条记录那一轮创建的列表对象。它在第 1 条记录中被 append 了 "{player}"，因为 target "奖励：{count}" 中没有 "{player}"。"{count}" 存在，所以不加入。然后 issues.append((record["key"], "missing placeholders", missing)) 把这个列表对象作为元组元素保存进 issues。第 2 条记录创建了另一个新的 missing 空列表，但由于没有占位符缺失项，不会被加入 issues。
5. 如果把 missing = [] 放到外层循环之前，会产生什么风险？
所有记录会共享同一个 missing 列表。第 1 条记录加入的 "{player}" 会保留到后续记录中，导致后续即使没有缺失占位符，也可能因为 missing 非空而被误判有问题。更严重的是，issues 中保存的如果是同一个列表对象，后续对 missing 的修改还可能影响已经放入 issues 的内容。

验证后修正：

无需修正。
```

---

## E. 字典、集合、顺序与遍历时修改风险（16 分）

### E1. `dict` / `set` 的遍历顺序与稳定报告（5 分）

阅读代码，预测输出，并说明哪些顺序可以依赖，哪些不适合作为业务顺序依赖。

```python
source = {
    "menu.start": "Start",
    "menu.exit": "Exit",
    "mail.reward": "Reward: {count}",
}

target = {
    "menu.exit": "退出",
    "menu.start": "开始",
    "menu.debug": "调试",
}

missing = source.keys() - target.keys()
extra = target.keys() - source.keys()

print("source keys")
for key in source:
    print(key)

print("missing", missing)
print("extra sorted", sorted(extra))
```

要求至少说明：

1. 遍历 `source` 默认得到什么；
2. 字典插入顺序在这里有什么意义；
3. `missing` 和 `extra` 是什么类型的集合式结果；
4. 为什么直接打印集合不适合稳定报告；
5. 为什么 `sorted(extra)` 更适合写进可复现报告。

答题区：

```tex
验证前预测：

【完整输出】
source keys
menu.start
menu.exit
mail.reward
missing {'mail.reward'}
extra sorted ['menu.debug']
【关键解释】
1. 遍历 source 默认得到什么？
for key in source 默认遍历字典的 key，不是 value，也不是 key-value pair。因此输出的是 source 的三个 key。
2. 字典插入顺序在这里有什么意义？
source 字典按字面量插入顺序创建：
"menu.start"
"menu.exit"
"mail.reward"
现代 Python 字典保留插入顺序，所以 for key in source 会按这个顺序输出。这个顺序可以用于保留原资源声明顺序或报告扫描顺序。
3. missing 和 extra 是什么类型的集合式结果？
source.keys() 和 target.keys() 是字典 key 视图，它们支持集合式运算。
missing = source.keys() - target.keys()
表示 source 中有、target 中没有的 key，即 {"mail.reward"}。
extra = target.keys() - source.keys()
表示 target 中有、source 中没有的 key，即 {"menu.debug"}。
这些结果是集合式结果，通常表现为 set。
4. 为什么直接打印集合不适合稳定报告？
因为 set 没有业务顺序保证。即使本题 missing 只有一个元素，直接打印 {'mail.reward'} 看起来稳定，但一般情况下集合多个元素的输出顺序不应该作为报告顺序依赖。直接打印 set 不利于稳定日志、测试断言和版本比较。
5. 为什么 sorted(extra) 更适合写进可复现报告？
sorted(extra) 会返回按排序规则排列的列表，例如 ['menu.debug']。对多个 key 来说，sorted(...) 可以保证输出稳定、可复现，适合写入 CI 报告、审计日志、测试快照。对于“缺失了哪些 key / 多出了哪些 key”这类集合结果，排序不会破坏原始行号语义，因为它本来就是集合式结果。

验证后修正：

无需修正。
```

### E2. 遍历字典时删除键的风险（5 分）

下面代码意图删除空译文记录。请指出风险，并给出两种更安全的改写思路。

```python
records = {
    "menu.start": "开始",
    "menu.exit": "",
    "menu.debug": "",
}

for key, target in records.items():
    if not target:
        del records[key]

print(records)
```

要求至少说明：

1. 为什么遍历过程中改变字典大小有风险；
2. 这段代码可能触发什么类型的运行期错误；
3. “先收集要删除的键，再统一删除”如何写；
4. “构造新字典”如何写；
5. 两种写法在语义上有什么差异。

答题区：

```tex
验证前预测：

【输出或异常】
RuntimeError: dictionary changed size during iteration
如果不捕获异常，print(records) 不会执行。
【关键解释】
1. 为什么遍历过程中改变字典大小有风险？
records.items() 返回字典的动态视图。for key, target in records.items() 正在基于字典当前结构迭代。如果循环体中 del records[key] 删除 key，会改变字典大小和 key 集合，破坏当前迭代器对字典结构的假设。因此遍历过程中增删 key 是危险操作。
2. 这段代码可能触发什么类型的运行期错误？
通常会触发：
RuntimeError: dictionary changed size during iteration
3. “先收集要删除的键，再统一删除”如何写？
可以写：

keys_to_delete = []

for key, target in records.items():
    if not target:
        keys_to_delete.append(key)

for key in keys_to_delete:
    del records[key]

print(records)

这样第一轮只是扫描，不改 records 大小；第二轮才统一删除。
4. “构造新字典”如何写？
可以写：

cleaned = {}

for key, target in records.items():
    if target:
        cleaned[key] = target

print(cleaned)

当然也可以写成推导式：
cleaned = {key: target for key, target in records.items() if target}
5. 两种写法在语义上有什么差异？
先收集要删除的键，再统一删除：
保留原字典对象 records，并在第二阶段原地删除不合格项。适合确实需要修改原对象的场景。
构造新字典：
不修改原 records，而是生成一个新的 cleaned 结果。适合审计、过滤、清洗输出，能够保留原始输入，便于报告和调试。
此外，工程上，如果是本地化审计工具，通常更推荐构造新字典或结构化结果，避免边扫描边破坏输入数据。

验证后修正：

无需修正。
```

### E3. 成员测试、哈希与 key 查找（6 分）

解释下面四个表达式分别在检查什么，并说明字典 key 成员测试与集合成员测试的共同点。

```python
record = {"key": "menu.start", "target": "开始"}
known_keys = {"menu.start", "menu.exit"}

"key" in record
"menu.start" in record
"menu.start" in known_keys
record["key"] in known_keys
```

要求至少说明：

1. `x in dict_obj` 默认检查的是键、值还是键值对；
2. `dict[key]` 与 `key in dict` 的目的有什么不同；
3. 集合为什么适合做“是否已见过 / 是否属于允许集合”的成员测试；
4. 哈希值和相等性比较在字典 key 查找、集合成员测试中的大致作用；
5. 为什么“集合基于哈希”不只是为了去重。

答题区：

```tex
验证前预测：

给定：
record = {"key": "menu.start", "target": "开始"}
known_keys = {"menu.start", "menu.exit"}
1. "key" in record
结果为 True。x in dict_obj 默认检查的是字典的键。record 的键包括 "key" 和 "target"，所以 "key" in record 为 True。
2. "menu.start" in record
结果为 False。虽然 "menu.start" 是 record["key"] 对应的值，但它不是 record 的键。x in dict_obj 不检查 value，因此 "menu.start" in record 为 False。
3. "menu.start" in known_keys
结果为 True。known_keys 是集合，成员包括 "menu.start" 和 "menu.exit"。集合成员测试检查元素是否存在，所以结果为 True。
4. record["key"] in known_keys
结果为 True。record["key"] 先取出字典中的键 "key" 对应的值，即 "menu.start"。然后测试 "menu.start" 是否在 known_keys 集合中，由上面刚说的第三个表达式可知，结果为 True。
【关键解释】
1. x in dict_obj 默认检查的是键、值还是键值对？
默认检查键。若要检查值，应写 x in dict_obj.values()；若要检查键值对，应写 (key, value) in dict_obj.items()。
2. dict[key] 与 key in dict 的目的有什么不同？
key in dict 是成员测试，目的是判断这个 key 是否存在，返回 True 或 False。
dict[key] 是订阅取值，目的是取得 key 对应的 value；如果 key 不存在，通常抛出 KeyError。
3. 集合为什么适合做“是否已见过 / 是否属于允许集合”的成员测试？
集合基于哈希结构，成员测试平均意义上很快；集合天然去重，适合保存 seen_keys、known_keys、allowed_keys、missing_keys 等结果。例如扫描资源时，可以用 seen_keys 发现重复 key，用 known_keys 判断某个 key 是否属于允许集合。
4. 哈希值和相等性比较在字典 key 查找、集合成员测试中的大致作用？
字典 key 查找和集合成员测试都会先利用对象的 hash 值定位候选位置；如果发生哈希冲突，还需要用相等性比较确认是否真的是同一个逻辑 key / 元素。hash 相同不代表对象一定相等；但如果两个对象相等，则它们应有相同 hash。作为 dict key 或 set 元素的对象，其参与 hash 和 equality 的状态应保持稳定。
5. 为什么“集合基于哈希”不只是为了去重？
去重只是集合的自然结果之一。集合基于哈希还带来快速成员测试和集合运算能力，例如交集、并集、差集、对称差集。这在本地化审计中很有用，例如：
missing_keys = required_keys - actual_keys
extra_keys = actual_keys - required_keys
seen_keys 用于发现重复扫描项
allowed_keys 用于判断 key 是否合法。

验证后修正：

无需修正。
```

---

## F. 工程综合题：本地化资源扫描函数设计（20 分）

### F1. 结构化扫描报告预测（10 分）

阅读函数和输入，预测最终 `report`。重点写出 `completed`、`stats`、`issues`、`fatal_error`、`valid_records` 的最终内容。

```python
def scan_records(records):
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

    required_placeholders = {
        "mail.reward": ["{count}"],
        "mail.greet": ["{player}"],
    }

    for line_no, record in enumerate(records, start=1):
        report["stats"]["total"] += 1

        if "key" not in record:
            report["completed"] = False
            report["fatal_error"] = (line_no, "missing key")
            break

        if not record.get("enabled", True):
            report["stats"]["disabled"] += 1
            continue

        report["stats"]["enabled"] += 1

        key = record["key"]
        target = record.get("target", "")

        if not target:
            report["issues"].append((line_no, "warning", key, "empty target"))
            continue

        missing = []

        for placeholder in required_placeholders.get(key, []):
            if placeholder not in target:
                missing.append(placeholder)

        if missing:
            report["issues"].append((line_no, "warning", key, "missing placeholders", missing))
            continue

        report["stats"]["valid"] += 1
        report["valid_records"].append({
            "key": key,
            "target": target,
        })

    return report


records = [
    {"key": "menu.start", "target": "开始", "enabled": True},
    {"key": "mail.reward", "target": "奖励", "enabled": True},
    {"key": "menu.debug", "target": "", "enabled": False},
    {"target": "无键记录", "enabled": True},
    {"key": "mail.greet", "target": "你好，{player}", "enabled": True},
]

print(scan_records(records))
```

要求至少说明：

1. 第 2 条记录为什么是普通 issue，而不是 fatal error；
2. 第 3 条记录为什么不会检查空译文；
3. 第 4 条记录为什么会中断循环；
4. 第 5 条记录是否会被处理；
5. `valid_records` 为什么构造新字典，而不是直接追加原始 `record`。

答题区：

```tex
验证前预测：

【最终 report】
{
    'completed': False,
    'stats': {
        'total': 4,
        'disabled': 1,
        'enabled': 2,
        'valid': 1,
    },
    'issues': [
        (2, 'warning', 'mail.reward', 'missing placeholders', ['{count}'])
    ],
    'fatal_error': (4, 'missing key'),
    'valid_records': [
        {'key': 'menu.start', 'target': '开始'}
    ],
}
【逐条解释】
第 1 条：
{"key": "menu.start", "target": "开始", "enabled": True}
line_no == 1。
stats["total"] += 1 -> total == 1。
有 key，不 fatal。
enabled 为 True，不跳过。
stats["enabled"] += 1 -> enabled == 1。
key = "menu.start"。
target = "开始"。
target 非空。
required_placeholders.get("menu.start", []) 得到空列表。
最终 missing = []。即 missing 指向空列表，为假。
stats["valid"] += 1 -> valid == 1。
valid_records 追加新字典：
{"key": "menu.start", "target": "开始"}
第 2 条：
{"key": "mail.reward", "target": "奖励", "enabled": True}
line_no == 2。
stats["total"] += 1 -> total == 2。
有 key，不 fatal。
enabled 为 True，不跳过。
stats["enabled"] += 1 -> enabled == 2。
key = "mail.reward"。
target = "奖励"。
target 非空。
required_placeholders.get("mail.reward", []) 得到 ["{count}"]。
检查 "{count}" 是否在 "奖励" 中，结果不在。
所以有：missing = ["{count}"]。missing 非空，issues 追加：
(2, "warning", "mail.reward", "missing placeholders", ["{count}"])
然后 continue。
因此第 2 条是普通 issue，不是 fatal error，也不计入 valid。
第 3 条：
{"key": "menu.debug", "target": "", "enabled": False}
line_no == 3。
stats["total"] += 1 -> total == 3。
有 key，不 fatal。
record.get("enabled", True) 为 False。
stats["disabled"] += 1 -> disabled == 1。
continue 触发。
因此不会执行 enabled += 1，不会读取 target，不会检查空译文，也不会加入 issues。这表示 disabled 记录被配置为跳过，不作为质量问题处理。
第 4 条：
{"target": "无键记录", "enabled": True}
line_no == 4。
stats["total"] += 1 -> total == 4。
if "key" not in record 为 True。
设置：
completed = False
fatal_error = (4, "missing key")
break
至此循环中断。
第 5 条：
{"key": "mail.greet", "target": "你好，{player}", "enabled": True}
不会被处理。因为第 4 条缺少 key，这是阻断性结构错误，已经 break 终止循环。
【题目要求回答】
1. 第 2 条记录为什么是普通 issue，而不是 fatal error？
因为第 2 条有 key，记录结构完整，可以定位到具体资源 "mail.reward"。它的问题是 target 缺少必需占位符 "{count}"，这是内容一致性问题，适合加入 issues 后继续扫描，不破坏整体扫描前提。
2. 第 3 条记录为什么不会检查空译文？
因为此记录的 enabled 为 False。代码在检查 enabled 后立即 stats["disabled"] += 1 并 continue，跳过后续 target 检查、placeholder 检查和 valid 追加。因此 disabled 记录不参与质量检查。
3. 第 4 条记录为什么会中断循环？
因为它缺少 "key"。key 是定位资源和生成报告的基础字段，缺少 key 是结构性 fatal error。代码设置 completed = False 和 fatal_error = (4, "missing key") 后 break，停止扫描。
4. 第 5 条记录是否会被处理？
不会。第 4 条已经 break，for 循环终止，第 5 条没有机会进入循环体。
5. valid_records 为什么构造新字典，而不是直接追加原始 record？
构造新字典可以让输出结果只包含清洗后需要的字段 key 和 target，避免共享原始 record 对象，避免后续修改 valid_records 时影响输入数据，也避免把 enabled 等输入控制字段混入有效结果。这样报告结果更稳定、更清晰、更适合机器处理。

验证后修正：

无需修正。
```

### F2. 小设计题：写出扫描函数骨架（10 分）

请设计一个 `scan_localization_records(records)` 函数。可以写真实 Python 代码，也可以写接近代码的清晰伪代码，但必须表达出循环结构和关键控制流。

需求：

```tex
1. 输入 records 是一组字典记录。
2. 每条记录至少期望有 key、target、enabled 三类信息。
3. enabled 为 False 的记录应计入 disabled，然后跳过后续检查。
4. 缺少 key 是阻断问题：设置 completed=False、fatal_error=(line_no, "missing key")，然后停止扫描。
5. target 为空是普通质量问题：加入 issues，然后继续扫描下一条。
6. 对 mail.reward 检查 {count}，对 mail.greet 检查 {player}。
7. 通过检查的记录加入 valid_records。
8. 函数不要在核心扫描逻辑里 print。
9. 不要修改输入记录本身，返回结构化 report。
10. 报告顺序应能帮助定位原始输入位置。
```

要求至少说明：

1. 你会使用 `for`、`while` 还是二者组合，为什么；
2. 你会把 `line_no` 放进哪些报告条目；
3. 你如何使用 `continue` 降低嵌套；
4. 你如何使用 `break` 或统一 `return` 保持报告结构稳定；
5. 你如何避免修改输入对象。

答题区：

```python
# 可以在这里写代码或伪代码
def scan_localization_records(records):
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

    required_placeholders = {
        "mail.reward": ["{count}"],
        "mail.greet": ["{player}"],
    }

    for line_no, record in enumerate(records, start=1):
        report["stats"]["total"] += 1

        if "key" not in record:
            report["completed"] = False
            report["fatal_error"] = (line_no, "missing key")
            break

        if not record.get("enabled", True):
            report["stats"]["disabled"] += 1
            continue

        report["stats"]["enabled"] += 1

        key = record["key"]
        target = record.get("target", "")

        if not target:
            report["issues"].append(
                (line_no, "warning", key, "empty target")
            )
            continue

        missing_placeholders = []

        for placeholder in required_placeholders.get(key, []):
            if placeholder not in target:
                missing_placeholders.append(placeholder)

        if missing_placeholders:
            report["issues"].append(
                (
                    line_no,
                    "warning",
                    key,
                    "missing placeholders",
                    missing_placeholders,
                )
            )
            continue

        report["stats"]["valid"] += 1
        report["valid_records"].append(
            {
                "line_no": line_no,
                "key": key,
                "target": target,
            }
        )

    return report
```

```tex
设计说明：
1. 使用 for、while 还是二者组合，为什么？
这里使用 for 循环，因为 records 是一组可迭代记录，任务本质是“逐条扫描资源记录”。for record in records 或 enumerate(records, start=1) 能自然表达逐项遍历。while 更适合动态条件、手动下标推进、轮询或队列式处理；本题不需要手动维护 index，因此 for 更清楚，也更不容易写出无限循环。
2. line_no 放进哪些报告条目？
line_no 应放进 issues、fatal_error 和 valid_records 中。
- issues 中放 line_no，是为了告诉用户原始输入第几条资源有普通质量问题；
- fatal_error 中放 line_no，是为了告诉用户阻断性结构错误出现在哪一条记录；
- valid_records 中也可放 line_no，便于追踪有效记录来自原始输入哪个位置。
3. 如何使用 continue 降低嵌套？
enabled 为 False 时，计入 disabled 后 continue，跳过 target 和 placeholder 检查。
target 为空时，加入 issues 后 continue，跳过 placeholder 检查和 valid_records 追加。
missing_placeholders 非空时，加入 issues 后 continue，跳过 valid_records 追加。
这样每个分支处理完当前记录后立即进入下一条，避免写成多层 if/else 嵌套，扫描逻辑更清晰。
4. 如何使用 break 或统一 return 保持报告结构稳定？
缺少 key 是阻断问题。遇到缺 key 时设置：
report["completed"] = False
report["fatal_error"] = (line_no, "missing key")
然后 break 停止扫描。
这里使用 break 后统一 return report，而不是在循环内部直接 return。这样函数只有一个统一出口，更容易保证 report 始终包含 completed、stats、issues、fatal_error、valid_records 等字段。如果后续要增加 issue_count、blocked、summary 等收尾字段，也可以放在循环后统一补齐。
5. 如何避免修改输入对象？
代码没有对 record 本身赋值，也没有修改 record["target"]。target = record.get("target", "") 只是把值绑定到局部变量。通过检查的记录加入 valid_records 时，构造了一个新字典：
{
    "line_no": line_no,
    "key": key,
    "target": target,
}
而不是直接 valid_records.append(record)。这样 valid_records 不共享原始记录的外层字典对象，后续修改报告不会影响输入 records。

验证后修正：

无需修正。
```

---

## 作答后提交说明

请直接在每题的“答题区”中作答。你可以保留“验证前预测”和“验证后修正”两段，也可以只写完整推理；如果你运行了代码，请标明哪些结论来自运行验证。

提交后我会按阶段测验批改方式进行逐题审批：保留你的原答案，在本文件末尾追加 `## Codex 批改记录（逐题审批，YYYY-MM-DD）`，给出建议得分、主要强项、需要精修的边界、是否通过本阶段，以及可同步到学习画像的更新。

---

## Codex 批改记录（逐题审批，2026-07-07）

### 总体审批结论

建议得分：`99 / 100`。

本阶段测验通过。你的主干预测、对象绑定分析、循环控制流解释、文件/迭代器一次性消费边界、字典/集合成员测试、以及本地化资源扫描报告设计都已经稳定。扣分不是因为主线概念错误，而是两个很小但值得保留的工程精度点：

1. B2 中“把 `report["total"] += 1` 放到空字符串判断之后”的口径可以再收紧：若它移动到 `if not command: ... continue` 之后，并且仍位于 `QUIT` 分支之后，那么本题最终 `total` 会从“读取过的命令数”变成“真正进入普通处理路径的非空、非哨兵命令数”，本例应为 `2`。
2. E2 中你正确指出会抛出 `RuntimeError`，但还应显式补一句：异常不是事务回滚；在抛错前，字典可能已经被部分修改。本题中如果捕获异常再观察，`"menu.exit"` 已经被删除，而 `"menu.debug"` 仍留在字典中。

### 逐题审批

| 题目 | 得分 | 审批意见 |
| --- | ---: | --- |
| A1 | 6 / 6 | 正确。`while` 重新求值、`continue` 只跳过本轮、`break` 抑制循环 `else`、循环变量绑定而非复制、以及循环后变量残留风险都解释到位。嵌套循环中内层 `break` 只结束内层这一点补充得很好。 |
| A2 | 5 / 5 | 正确。能区分 list/dict 的可重复遍历、file/zip 的逐步消费，也能说明 dict 默认遍历 key、set 不承诺业务顺序、稳定报告用 `sorted(...)`。 |
| A3 | 4 / 4 | 正确。`print()` 输出副作用、`issues.append(...)` 修改列表对象、核心扫描返回结构化 report、展示层再负责输出，这条工程分层很清楚。 |
| B1 | 8 / 8 | 正确。完整输出、`queue` 动态变化、第二个 `scan` 的 `continue`、`report` 触发 `break` 后跳过 `else`、`validate` 留在队列中都预测正确。 |
| B2 | 3.5 / 4 | 主体正确。最终输出和 `index == 4` 判断正确；对 `continue`、`QUIT`、`report` 不被处理的解释也正确。小扣分点是第 4 问可以给出更具体口径：若 `total += 1` 放到空字符串过滤之后，本例通常会只统计 `scan` 和 `normalize`，即 `total == 2`。 |
| B3 | 4 / 4 | 正确。能准确区分 `break` 后统一收尾与循环中直接 `return`，并能联系结构化 report 的字段一致性。 |
| C1 | 5 / 5 | 正确。`enumerate(..., start=1)`、`rstrip("\n")` 保留业务空白、`split("=", 1)`、空行/空译文分流、保留 `line_no` 的工程意义都讲清楚了。 |
| C2 | 6 / 6 | 正确。普通 `zip()` 静默截断、`strict=True` 暴露长度不一致、异常前已有部分 `append`、非事务性边界都到位。 |
| C3 | 6 / 6 | 正确。文件位置、EOF 后二次遍历为空、`seek(0)`、`StringIO` 与真实文件对象的共同流式位置模型、边读边写风险都解释准确。 |
| D1 | 6 / 6 | 正确。循环变量绑定到原字典对象、`valid.append(record)` 共享外层字典、后续通过 `valid[0]` 修改会反映到 `records[0]`，以及构造新字典的修正方案都准确。 |
| D2 | 5 / 5 | 正确。`strip()` 不写回原记录、新外层字典不共享原始字典、原始空格保留、报告生成的输入/输出分离、以及新字典不等于深拷贝都说明到位。 |
| D3 | 5 / 5 | 正确。内外层循环职责、`missing = []` 放置位置、`issues` 中保存的是那一轮的列表对象、共享列表风险都解释清楚。 |
| E1 | 5 / 5 | 正确。字典默认遍历 key、字典插入顺序、key view 集合运算、set 直接显示不适合稳定报告、`sorted(...)` 的复现价值都到位。 |
| E2 | 4.5 / 5 | 主体正确。会触发 `RuntimeError: dictionary changed size during iteration`，且两种安全改写都正确。小扣分点：需要显式说明异常发生前可能已经部分删除，因此“报错”不代表原字典保持原样。 |
| E3 | 6 / 6 | 正确。四个表达式的成员测试对象、`dict[key]` 与 `key in dict` 的目的差异、set 的成员测试和集合运算价值、hash 与 equality 的配合都解释到位。 |
| F1 | 10 / 10 | 正确。最终 report 预测准确，尤其是第 3 条 disabled 记录先 `continue` 而不检查空译文、第 4 条缺 key 中断、第 5 条不处理、`valid_records` 构造新字典这些关键点都稳。 |
| F2 | 10 / 10 | 正确。函数骨架满足需求：使用 `enumerate`，disabled/empty/missing placeholders 均用 `continue` 降低嵌套，fatal 用 `break` 后统一返回，不在核心逻辑中 `print`，并构造新字典避免修改输入。 |

### 本阶段末评语与能力判断

你已经通过 `C13_while_and_for_Loops` 阶段测验。相比 C12，你这次不是只会判断单次分支，而是已经能追踪“循环每轮如何推进状态”：队列被 `pop` / `append` 改变、`continue` 跳过哪些后续语句、`break` 如何抑制循环 `else`、文件和 `zip` 如何被逐步消费、循环变量何时只是重新绑定名字、何时经由可变对象产生原地修改副作用。

工程侧也明显稳定：你能把本地化扫描拆成 `stats`、`issues`、`fatal_error`、`valid_records`，并能说明为什么核心函数返回结构化数据而不是直接 `print`。这说明 C13 的循环知识已经进入了你现有的对象模型和工程报告模型，而不是停留在语法层。

### 学习画像更新

稳定强项：

- 能准确预测 `while` 动态条件、队列式状态变化、`break` / `continue` / 循环 `else` 的控制流结果。
- 能区分 `for` 遍历产生元素绑定、循环变量重新绑定、可变元素原地修改和构造新容器之间的边界。
- 能把 `range` / `enumerate` / `zip(strict=True)`、文件行迭代、dict/set 遍历顺序和稳定报告策略放入本地化审计场景。
- 能设计结构稳定的扫描 report，并保持核心扫描逻辑与人读输出副作用分离。

仍需精修：

- 统计字段的位置要继续绑定到明确口径：读取过、启用过、有效过、真正处理过，不要只说“取决于位置”，最好给出该位置对应的精确含义和示例最终值。
- 运行期错误不等于事务回滚。遍历中修改 dict/list/set 这类风险场景，要继续观察“异常发生前是否已经产生部分副作用”。

新的能力判断：

你当前已经稳定通过 P3 中的 C10-C13，水平可以判断为：**准中级入门已经坐稳，并正在进入能用小型函数式流程组织真实数据扫描任务的中级入门前段**。下一阶段 `C14_Iterations_and_Comprehensions` 应重点把这次已经压稳的循环模型推进到迭代协议、推导式、惰性对象与急切求值的边界上。
