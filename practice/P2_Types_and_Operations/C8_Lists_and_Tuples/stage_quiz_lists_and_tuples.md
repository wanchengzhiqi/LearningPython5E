# Stage Quiz: Lists and Tuples

本测验用于当前小阶段：Python 列表和元组。

这份卷子已经按你本阶段的实际学习进度升级：它不只考列表/元组语法本身，还会考你是否能把对象模型迁移到新版迷你项目 `mini_project_localization_records.py`，包括 JSON/CSV 输入、`Record` / `namedtuple` 建模、结构化 JSON 报告、占位符检查、浅拷贝和共享引用边界。

总分：100 分。

答题规则：

1. 第一遍不要运行代码，先写预测、对象身份变化和理由。
2. 第二遍可以用 Python 3.9.13 验证，并标注“验证前预测”和“验证后修正”。
3. 每道代码题尽量按这条链解释：源码写了什么、创建了什么对象、名字绑定到哪里、哪一步原地修改、哪一步重新绑定、哪些对象共享、输出为什么这样显示。
4. 本卷不包含参考答案。你作答后交给我审批，我会保留你的原答案并追加批改记录。
5. 若你认为题目本身有歧义，可以直接指出；这也属于本阶段能力的一部分。

---

## A. 对象、绑定与方法返回值（18 分）

### A1. 赋值、原地修改和相等性（6 分）

预测输出，并解释 `records`、`alias`、`snapshot` 三个名字分别绑定到什么对象。

```python
records = ["menu.start", "menu.quit"]
alias = records
snapshot = records[:]

records.append("menu.options")

print(records)  # ["menu.start", "menu.quit", "menu.options"]，名字records绑定的列表对象并未发生身份变化（即records并未更换绑定关系），列表的append方法会原地修改原列表而不是创建新的列表
print(alias)  # ["menu.start", "menu.quit", "menu.options"]，名字alias绑定的列表对象并未发生身份变化（即alias并未更换绑定关系），事实上，从始至终alias和records绑定的是同一个列表对象
print(snapshot)  # ["menu.start", "menu.quit"]，名字snapshot绑定的列表对象是records指向的对象经浅拷贝后的“复制品”，这两个对象并不是同一个对象
print(records is alias)  # True
print(records is snapshot)  # False
print(records == snapshot)  # False
```

答题区：

```text
`records = ["menu.start", "menu.quit"]` 是一个赋值语句，其中的 `["menu.start", "menu.quit"]` 是创建新的列表对象的字面量表达式，并且，名字records被绑定到了这个列表对象上。
`alias = records` 是一个赋值语句，语句执行时，名字records将被替换成它所指向的列表对象，然后名字alias将被绑定在这个对象上。最终效果就是：alias和records绑定的是同一个列表对象。
`snapshot = records[:]` 是一个赋值语句，其中的表达式 `records[:]` 返回records绑定对象的完整切片，这样的操作通常来说是对列表对象的浅拷贝，它将创建一个新的列表对象，不过原对象内部保存的引用也将被新对象继承保留！而这个新的列表对象将被snapshot所引用。也就是说，此时的snapshot和records的关系是：它们指向的对象内容相同，但身份不同。
`records.append("menu.options")` 是一个列表对象的append方法调用表达式，此操作将原地修改records指向的列表对象，在列表末尾追加一项（"menu.options"）。
因为alias和records绑定的是同一个列表对象，而snapshot和records绑定的并不是同一个列表对象，所以，打印alias和records将看到它们指向的同一个列表对象发生了追加一项的变化，而打印snapshot时会发现它绑定的列表并不会同步这个变化。也正因如此，此时的 `records == snapshot` 将返回 False

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### A2. 方法返回值陷阱（6 分）

下面代码最终会输出什么？请解释 `append()`、`sort()`、`sorted()` 的返回值与对象效果。

```python
items = ["quest.long", "menu.start"]

append_result = items.append("debug.empty")
sort_result = items.sort()
sorted_result = sorted(items)

print(append_result)  # None，返回值为None旨在提示：列表的append方法直接原地修改原列表而不是创建并返回新的列表对象
print(sort_result)  # None，返回值为None旨在提示：列表的sort方法直接原地修改原列表而不是创建并返回新的列表对象
print(items) # ["debug.empty", "menu.start", "quest.long"]，名字items指向的对象从始至终都没有发生身份变化（即items并未更换绑定关系），只有内容上的改变
print(sorted_result)  # ["debug.empty", "menu.start", "quest.long"]，内置的sorted函数不会改变传入的实参对象，会创建并返回一个新的列表对象，其内容正是实参对象的内容在排序后的结果
print(items is sorted_result)  # False，名字items和sorted_result指向的对象内容相同，但是身份不同
```

答题区：

```text
`items = ["quest.long", "menu.start"]` 是一个赋值语句，其中的 `["quest.long", "menu.start"]` 是创建新的列表对象的字面量表达式，并且，名字items被绑定到了这个列表对象上。
`append_result = items.append("debug.empty")` 是一个赋值语句，其中的 `items.append("debug.empty")` 是一个列表对象的append方法调用表达式，此操作将原地修改items指向的列表对象，在列表末尾追加一项（"debug.empty"），并且，这个表达式还会返回一个 None，在这里，名字append_result被绑定到了这个None对象上。
`sort_result = items.sort()` 是一个赋值语句，其中的 `items.sort()` 是一个列表对象的sort方法调用表达式，此操作将原地修改items指向的列表对象，将列表内的元素按规则重新排序，并且，这个表达式还会返回一个 None，在这里，名字sort_result被绑定到了这个None对象上。
`sorted_result = sorted(items)` 是一个赋值语句，其中的 `sorted(items)` 是一个名为sorted的内置函数调用表达式，该函数将传入函数的实参对象（在这里，这个对象是items所绑定的列表对象）的内容按规则排序，并创建一个新的列表对象，使其包含前面的排序后的结果。要注意的是：这一系列操作并不会原地修改items指向的列表对象！最后，这个表达式将创建好的新的列表对象返回，在这里，名字sorted_result被绑定到了这个新的列表对象上。
综上，打印输出append_result和sort_result将看到 None，而items绑定的列表是在经历 append 和 sort 的原地修改之后被传入sorted函数的，因此，打印输出items和sorted_result所看到的内容会是一样的，只是要知道：名字items和sorted_result指向的对象内容虽然相同，但是它们的身份不同！也正因如此，此时的 `items is sorted_result` 将返回 False

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### A3. `+`、`+=` 与名字重新绑定（6 分）

分别说明 `a`、`b`、`c`、`d` 最终绑定到哪个列表对象。哪些步骤创建了新列表？哪些步骤原地修改了旧列表？

```python
a = ["ui"]
b = a
c = a + ["menu"]
a += ["checked"]
d = a

print(a)  # ["ui", "checked"]，名字a绑定的对象并没有发生身份变化（即a并未更换绑定关系，严格来说，a有过重新绑定的操作，不过重新绑定的对象仍是原对象），此外，a绑定的列表还被名字b和d共享
print(b)  # ["ui", "checked"]，名字b绑定的对象并没有发生身份变化（即b并未更换绑定关系），从始至终b和a指向同一个列表对象
print(c)  # ["ui", "menu"]，名字c绑定的是新的列表对象，c和a指向的对象的内容和身份都不同
print(d)  # ["ui", "checked"]，名字d绑定的对象并没有发生身份变化（即d并未更换绑定关系），从始至终d和a指向同一个列表对象
print(a is b)  # True
print(a is c)  # False
print(a is d)  # True
```

答题区：

```text
`a = ["ui"]` 是一个赋值语句，其中的 `["ui"]` 是创建新的列表对象的字面量表达式，并且，名字a被绑定到了这个列表对象上。
`b = a` 是一个赋值语句，语句执行时，名字a将被替换成它所指向的列表对象，然后名字b将被绑定在这个对象上。最终效果就是：b和a绑定的是同一个列表对象。
`c = a + ["menu"]` 是一个赋值语句，其中的表达式 `a + ["menu"]` 代表列表的拼接操作，此操作将创建一个新的列表对象，其内容是：a指向的列表追加一项（"menu"）后的内容（这只是一种比拟，实际上此时a绑定的列表没有发生任何变化），最后，这个表达式将创建好的新的列表对象返回，在这里，名字c被绑定到了这个新的列表对象上。
`a += ["checked"]` 是一个增强赋值语句，其中的 `+=` 会对a绑定的列表对象进行原地修改操作，即：在列表末尾追加一项（"checked"），然后，再让名字a重新绑定这个刚被原地修改了的列表对象，也就是说，a还是绑定在原对象上！与结果而言，这一番操作等价于 `a.append("checked")`。
`d = a` 是一个赋值语句，语句执行时，名字a将被替换成它所指向的列表对象，然后名字d将被绑定在这个对象上。最终效果就是：d和a绑定的是同一个列表对象。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

---

## B. 切片、嵌套列表与拷贝层级（20 分）

### B1. 切片读取 vs 切片赋值（6 分）

预测输出，并说明 `part = keys[1:]` 和 `keys[1:3] = ...` 的对象效果。

```python
keys = ["start", "load", "settings", "quit"]
part = keys[1:]
watcher = keys

keys[1:3] = ["continue", "save", "options"]

print(part)  # ["load", "settings", "quit"]
print(keys)  # ["start", "continue", "save", "options", "quit"]
print(watcher)  # ["start", "continue", "save", "options", "quit"]
print(watcher is keys)  # True
```

答题区：

```text
`keys = ["start", "load", "settings", "quit"]` 是一个赋值语句，其中的 `["start", "load", "settings", "quit"]` 是创建新的列表对象的字面量表达式，并且，名字keys被绑定到了这个列表对象上。
`part = keys[1:]` 是一个赋值语句，其中的表达式 `keys[1:]` 代表对keys引用的列表对象作切片取值操作，它将：从左到右，把keys引用的列表对象的偏移量范围是1-3的3个元素提取出来并作为一个新的列表对象的内容，最后这个表达式将创建好的新的列表对象返回，在这里，名字part被绑定到了这个新的列表对象上。要注意的是：此时的keys所绑定的列表对象还没发生原地改变，而且part绑定的是新的对象，因此，可以说part指向的列表是旧列表的切片副本，它也不会受到此后keys绑定的对象发生原地改变的影响！还要注意的是：序列的索引取值、切片取值、拼接和重复操作都不会修改原对象！
`watcher = keys` 是一个赋值语句，语句执行时，名字keys将被替换成它所指向的列表对象，然后名字watcher将被绑定在这个对象上。最终效果就是：watcher和keys绑定的是同一个列表对象。
`keys[1:3] = ["continue", "save", "options"]` 是一个切片赋值语句，首先，列表的切片赋值操作将原地修改原列表对象，其次，这里的结果就是：keys引用的列表中偏移量范围是1-2的2个元素被“摘除”出来并将字面量表达式 `["continue", "save", "options"]` 所创建的新的列表对象“植入”原位。列表保存的是引用，在这里，相当于原列表替换了部分内含的引用，不过，是把列表中的两个引用换为了三个新的引用，之所以在此允许前后数目不一致，是因为 `[1:3]` 表达了连续的范围（区间），并不要求 `=` 两边的数据结构形状匹配，但若是形如 `[::2]` 这样的源码表示（即步长值的绝对值大于1），则表达了离散的位置，将严格要求 `=` 两边的数据结构形状必须匹配！

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### B2. 扩展切片赋值与形状匹配（5 分）

下面两段代码哪一段能成功？哪一段会报错？请解释“目标位置数量”和右侧元素数量的关系。

```python
items = ["A", "B", "C", "D", "E"]
items[::2] = ["x", "y", "z"]
print(items)  # ["x", "B", "y", "D", "z"]
```

```python
items = ["A", "B", "C", "D"]
items[::2] = ["x", "y", "z"]
print(items)  # ValueError
```

答题区：

```text
对于第一段代码：
`items = ["A", "B", "C", "D", "E"]` 是一个赋值语句，其中的 `["A", "B", "C", "D", "E"]` 是创建新的列表对象的字面量表达式，并且，名字items被绑定到了这个列表对象上。
而`items[::2] = ["x", "y", "z"]` 是一个切片赋值语句，首先，列表的切片赋值操作将原地修改原列表对象，其次，这里的结果就是：items引用的列表中偏移量分别是0、2、4这三个位置的三个引用被“摘除”出来并将字面量表达式 `["x", "y", "z"]` 所创建的新的列表对象所包含的三个引用一一对应的“插入”原位。正如前述，形如 `[::2]` 这样的源码表示（即步长值的绝对值大于1），表达了离散的位置而不是连续的区间范围，会严格要求 `=` 两边的数据结构形状必须匹配！也就是说，此时“目标位置数量”和右侧元素数量必须保证一致，否则将会报错 ValueError，很明显，此时“目标位置数量”和右侧元素数量确实一致，因此第一段代码的操作能成功！
对于第二段代码：
`items = ["A", "B", "C", "D"]` 是一个赋值语句，其中的 `["A", "B", "C", "D"]` 是创建新的列表对象的字面量表达式，并且，名字items被绑定到了这个列表对象上。
而`items[::2] = ["x", "y", "z"]` 是一个切片赋值语句，要注意的是：和第一段代码不同，items指向的对象长度是4而非5，这就导致这里的操作结果会是：items引用的列表中偏移量分别是0、2这二个位置的二个引用被“摘除”出来并试图将字面量表达式 `["x", "y", "z"]` 所创建的新的列表对象所包含的三个引用一一对应的“插入”原位。很明显，此时“目标位置数量”和右侧元素数量并非一致，因此最终的操作结果将是报错 ValueError！严格来说，报错将会发生在切片赋值语句的执行过程中，而不是等到打印输出items时才报错。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### B3. 嵌套列表共享引用（5 分）

预测输出，并解释为什么 `bad` 和 `good` 的表现不同。

```python
bad = [[]] * 3
good = [[] for _ in range(3)]

bad[0].append("menu.start")
good[0].append("menu.start")

print(bad)  # [["menu.start"], ["menu.start"], ["menu.start"]]
print(good)  # [["menu.start"], [], []]
print(bad[0] is bad[1])  # True
print(good[0] is good[1])  # False
```

答题区：

```text
`bad = [[]] * 3` 是一个赋值语句，其中的表达式 `[[]] * 3` 是通过列表支持的重复操作来创建新的列表对象的，要注意的是：对列表的重复操作会有复制引用的“副作用”！在这里，表达式将创建并返回一个长度为3且内部保存了三个指向同一个空列表的引用的外层列表。最后，名字bad被绑定到了这个列表对象上。
`good = [[] for _ in range(3)]` 是一个赋值语句，其中的表达式 `[[] for _ in range(3)]` 是通过列表推导式来创建新的列表对象的，要注意的是：不同于列表的重复操作，在这里，列表推导在每次循环后产生的结果列表都是新的列表对象，这意味着：整个表达式将创建并返回一个长度为3且内部保存了三个指向相互独立的空列表的引用的外层列表。最后，名字good被绑定到了这个列表对象上。
`bad[0].append("menu.start")` 是一个列表对象的append方法调用表达式，此操作将原地修改bad[0]指向的列表对象，在其末尾追加一项（"menu.start"）。前面刚提到：bad指向的列表内的引用都指向同一个列表对象，也就是说，bad[0]、bad[1]和bad[2]指向同一个可变对象，因此，对bad[0]引用对象的原地修改会被bad[1]和bad[2]同步。
`good[0].append("menu.start")` 是一个列表对象的append方法调用表达式，此操作将原地修改good[0]指向的列表对象，在其末尾追加一项（"menu.start"）。前面也提到：good指向的列表内的引用彼此独立，也就是说，good[0]、good[1]和good[2]指向不同的可变对象，因此，对good[0]引用对象的原地修改并不会被good[1]和good[2]同步。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### B4. 浅拷贝与深拷贝（4 分）

解释下面代码中 `shallow` 和 `deep` 的差异。重点说明外层列表、内层列表、字符串对象分别是否共享。

```python
import copy

original = [["menu.start", ["ui"]], ["menu.quit", ["ui"]]]
shallow = original[:]
deep = copy.deepcopy(original)

original[0][1].append("reviewed")
original.append(["menu.options", ["ui"]])

print(original)  # [["menu.start", ["ui", "reviewed"]], ["menu.quit", ["ui"]], ["menu.options", ["ui"]]]
print(shallow)  # [["menu.start", ["ui", "reviewed"]], ["menu.quit", ["ui"]]]
print(deep)  # [["menu.start", ["ui"]], ["menu.quit", ["ui"]]]
```

答题区：

```text
`original = [["menu.start", ["ui"]], ["menu.quit", ["ui"]]]` 是一个赋值语句，其中的 `[["menu.start", ["ui"]], ["menu.quit", ["ui"]]]` 是创建新的列表对象的字面量表达式，并且，名字original被绑定到了这个列表对象上。要注意的是，这里创建的列表不止最外层这一个，外层列表内部也嵌套了多层列表。
`shallow = original[:]` 是一个赋值语句，其中的表达式 `original[:]` 返回original绑定对象的完整切片，这样的操作通常来说是对列表对象的浅拷贝，它将创建一个新的列表对象，不过原对象内部保存的引用也将被新的列表对象继承保留！而这个新的列表对象将被shallow所引用。也就是说，此时的shallow和original的关系是：它们指向的对象内容相同，但身份不同，不过“身份不同”仅限于外层列表自身，外层列表内部包含的引用所指向的对象（无论是嵌套的列表（包括嵌套列表所包含的引用指向的任意对象）还是不可变的字符串）都是共享的，浅拷贝只能保护外层列表！对original绑定的外层列表作原地修改操作不会影响shallow绑定的列表，但是对original绑定的外层列表所包含的内层列表作原地修改操作将被shallow同步变化。
`deep = copy.deepcopy(original)` 是一个赋值语句，其中的 `copy.deepcopy(original)` 是一个从外部导入的名叫deepcopy的函数调用表达式，这个函数的作用是：把传入的实参对象（在这里，实参对象就是original所绑定的列表）做深拷贝处理并将处理结果返回。在这里，深拷贝也会创建一个新的列表对象作为结果对象，而名字deep被绑定到了这个新的列表对象上。不过不同于浅拷贝的是：深拷贝会递归至目标对象的每一层并对“沿途经历”的对象都做一次浅拷贝（严格来说，针对可哈希对象通常只会返回原对象而不会也做浅拷贝操作）！也就是说，此时的deep和original的关系是：它们指向的外层列表对象内容相同，但身份不同，要注意：“身份不同”不仅限于外层列表自身，外层列表内部包含的引用所指向的对象（无论是嵌套的列表（包括嵌套列表所包含的引用指向的任意对象）还是不可变的字符串）都不是共享的（这里为了简便，忽略了CPython的实现优化细节）！不论是对original绑定的外层列表，还是对外层列表所包含的内层列表作原地修改操作都将不会被deep同步变化。
`original[0][1].append("reviewed")` 是一个列表对象的append方法调用表达式，此操作将原地修改original[0][1]指向的列表对象（要注意这是内层列表），在其末尾追加一项（"reviewed"）。从前面对浅拷贝和深拷贝的阐述不难判断出：original[0]和shallow[0]指向同一个对象，而original[0]和deep[0]指向不同的对象，所以，这里的原地修改操作也会影响shallow，但不会影响deep。
`original.append(["menu.options", ["ui"]])` 是一个列表对象的append方法调用表达式，此操作将原地修改original指向的列表对象（要注意这是外层列表），在其末尾追加一项（["menu.options", ["ui"]]）。从前面对浅拷贝和深拷贝的阐述不难判断出：original、shallow和deep三者都指向不同的对象，所以，这里的原地修改操作只会影响original，而不会影响shallow和deep。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

---

## C. 元组、解包、`namedtuple` 与函数边界（20 分）

### C1. 逗号与圆括号（4 分）

分别写出下面变量的类型和值。

```python
a = ("menu.start")
b = ("menu.start",)
c = "menu.start",
d = ()
```

答题区：

```text
`a = ("menu.start")` 是一个赋值语句，其中的 `("menu.start")` 是被圆括号分组的创建新的字符串对象的字面量表达式，意即这个表达式返回是字符串对象，在这里，表达式 `("menu.start")` 等价于 `"menu.start"`，最后，名字a被绑定到了这个字符串对象上。
`b = ("menu.start",)` 是一个赋值语句，其中的 `("menu.start",)` 是创建新的元组对象的字面量表达式，要注意的是：想要通过字面量表达式的方式创建返回仅含一个元素的元组对象，必须在源码中写出逗号，只有圆括号（就像上面刚说明的情况）并不足以清晰表达创建元组对象的语义，事实上，通常而言，在不引发歧义的前提下，圆括号的存在对于创建元组的字面量表达式来说并非必须！最后，名字b被绑定到了这个元组对象上。
`c = "menu.start",` 是一个赋值语句，其中的 `"menu.start",` 是创建新的元组对象的字面量表达式，从上面的描述不难看出：这是合法的创建并返回只有一个元素的元组对象的表达式！最后，名字c被绑定到了这个元组对象上。
`d = ()` 是一个赋值语句，其中的 `()` 是创建新的空元组对象的字面量表达式，要注意的是：想要通过字面量表达式的方式创建返回一个内容为空的元组对象，必须在源码中写成一对圆括号，这种情景下只有一个逗号显然并不足以清晰表达创建空元组对象的语义！最后，名字d被绑定到了这个元组对象上。

“验证前预测”：
在交互式环境下分别输入并执行：
a = ("menu.start")
b = ("menu.start",)
c = "menu.start",
d = ()
print(type(a).__name__, a)
print(type(b).__name__, b)
print(type(c).__name__, c)
print(type(d).__name__, d)
对应的输出：
str menu.start
tuple ('menu.start', )
tuple ('menu.start', )
tuple ()
“验证后修正”：
预测正确，无须修正。
```

### C2. 元组不可变的真实边界（5 分）

预测输出，并解释哪一步是“替换元组槽位中的引用”，哪一步是“修改元组内部引用的可变对象”。

```python
record = ("menu.start", "Start", ["ui"])

try:
    record[1] = "Begin"
except TypeError as exc:
    print(type(exc).__name__)  # TypeError

record[2].append("checked")
print(record)  # ("menu.start", "Start", ["ui", "checked"])
```

答题区：

```text
首先，`record = ("menu.start", "Start", ["ui"])` 是一个赋值语句，其中的 `("menu.start", "Start", ["ui"])` 是创建新的元组对象的字面量表达式，并且，名字record被绑定到了这个元组对象上。要注意的是，这里创建的元组内含一个列表对象的引用！要知道，元组的不可变性指的是：元组保存的引用不可替换、不可删除、不可增添，这就不可避免的引入了隐性的陷阱：元组保存的引用一旦指向可变对象，那么元组可能发生内容上的变化，此时的元组虽然是不可变对象，但并不是可哈希对象了！
而上述代码中的这一步：`record[1] = "Begin"`，这是一个索引赋值语句，很明显，它在试图给元组对象作原地改变操作，更准确的说，它试图替换元组槽位中的既有引用！上面刚说过这对于元组类型对象来说是不被允许的，因此这一步会触发TypeError异常，代码中可看出该异常将被成功捕获，因此代码得以继续执行下去。
后续代码中的这一步：`record[2].append("checked")`，这是一个列表对象的append方法调用表达式。前面提到过：record绑定的元组对象内部含有指向列表对象的引用，所以在这里很明显，这个表达式会试图给元组内部引用的可变对象作原地改变操作，它修改的不是元组自身保存的引用，而是元组保存的引用所指向的可变列表对象，而列表对象的append方法只会改变列表的内容而不会改变列表的身份，因此最终的结果是：这步代码并不会报错，是合法的，同时它也是会改变元组内容的！

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### C3. 解包与扩展解包（5 分）

预测各名字绑定到什么对象，并指出 `middle` 的类型。

```python
record = ("menu.start", "Start", "Begin", ("ui", "menu"))
key, source, translation, tags = record

first, *middle, last = ["start", "load", "settings", "quit"]

print(key)  # menu.start
print(tags)  # ("ui", "menu")
print(middle)  # ["load", "settings"]
print(type(middle).__name__)  # list
```

答题区：

```text
`record = ("menu.start", "Start", "Begin", ("ui", "menu"))` 是一个赋值语句，其中的 `("menu.start", "Start", "Begin", ("ui", "menu"))` 是创建新的元组对象的字面量表达式，并且，名字record被绑定到了这个长度为4的元组对象上。
`key, source, translation, tags = record` 是一个常规的解包赋值语句，解包指的是：将一个可迭代对象的元素一一对应的绑定至目标名字上，而在这里，名字key、source、translation和tags分别绑定到了record[0]、record[1]、record[2]和record[3]各自指向的对象上。不过要注意的是：这种形式的解包赋值要求“目标名字数量”和待解包的可迭代对象的元素数量保持一致，否则将会报错 ValueError
`first, *middle, last = ["start", "load", "settings", "quit"]` 是一个扩展解包赋值语句，注意到其中的 `*middle` 指的是：在其它名字（如这里的first和last）绑定好对象后，剩下的待绑定对象（无论数目多少）将被组包成列表并让middle引用这个列表。这意味着：首先，middle绑定的对象始终是列表（无论原可迭代对象是否为列表类型），其次，这种形式的解包赋值并不会要求“目标名字数量”和待解包的可迭代对象的元素数量保持一致。比如在这里看起来就像是用三个名字去绑定四个对象，这里之所以合法，根本原因在于名字middle本质上还是只引用了一个列表对象，所谓的“多出来”的那一个对象被包含在列表内了。最终的效果就是：名字first和last分别绑定到了"start"和"quit"上，而名字middle绑定到了由可迭代对象剩下的中间两个元素所组成的列表对象（["load", "settings"]）上。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### C4. `namedtuple` 与 `_replace()`（6 分）

预测输出，并解释 `Record`、`record`、`updated` 的关系。

```python
from collections import namedtuple

Record = namedtuple("Record", "key source translation tags")
record = Record("menu.start", "Start", "Start Game", ("ui", "menu"))
updated = record._replace(translation="Begin Game")

print(record)  # Record("menu.start", "Start", "Start Game", ("ui", "menu"))
print(updated)  # Record("menu.start", "Start", "Begin Game", ("ui", "menu"))
print(record is updated)  # False
print(record.tags is updated.tags)  # True
```

答题区：

```text
`Record = namedtuple("Record", "key source translation tags")` 是一个赋值语句，其中的 `namedtuple("Record", "key source translation tags")` 是创建新的名叫Record的命名元组类对象的调用表达式，同时其中的 `"key source translation tags"` 明确的表明了新建的Record类和它的实例对象至少含有key、source、translation和tags这四个属性。最后，名字Record被绑定到了这个命名元组类对象上。
`record = Record("menu.start", "Start", "Start Game", ("ui", "menu"))` 是一个赋值语句，其中的 `Record("menu.start", "Start", "Start Game", ("ui", "menu"))` 是创建Record类的实例对象的调用表达式，要注意：实例化过程中传入的"menu.start"、"Start"、"Start Game"和("ui", "menu")这四个对象将被实例对象的四个属性key、source、translation和tags一一绑定。最后，名字record被绑定到了这个新建的实例对象上。
`updated = record._replace(translation="Begin Game")` 是一个赋值语句，其中的 `record._replace(translation="Begin Game")` 是实例对象record的_replace方法的调用表达式，它会创建一个新的Record类的实例对象，并且对于这个新建的实例对象，除了它的translation属性会被改绑至"Begin Game"对象上，其它属性都从record相应处深拷贝而来，这会受到CPython的实现优化影响，比如这里的record四项属性指向的都是可哈希对象，因此这个新建的实例对象的其它三个属性各自绑定的对象实际上会和record对应的属性共享。最后，名字updated被绑定到了这次新建的实例对象上。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

---

## D. 新版迷你项目代码阅读（22 分）

以下题目围绕 `mini_project_localization_records.py`、`sample_localization_records.json` 和 `sample_localization_records.csv`。

### D1. 外部 JSON 进入内部对象模型（6 分）

阅读下面简化后的逻辑，解释一个 JSON object 如何最终变成 `Record`。

```python
def record_from_mapping(data, index):
    key = normalize_text(data["key"])
    return Record(
        key,
        normalize_text(data["source"]),
        normalize_text(data["translation"]),
        normalize_tags(data.get("tags", ()), index),
    )
```

请回答：

1. `data` 通常是什么类型？
2. `Record(...)` 创建的对象是什么？
3. `tags` 如果是 `["ui", "menu"]`、`"ui;menu"`、`None`，分别会变成什么？
4. 这里有没有复制外部 JSON 文件本身？

答题区：

```text
首先，一个外部JSON文件的路径会被作为命令行参数的一部分，被项目里的build_parser函数返回的解析器的parse_args方法所解析，进一步的，经由run_demo、load_records这两个函数的处理已经可以确认是属于外部JSON文件输入场景，然后转由函数load_json_records处理，而在这个函数中，关键行 `data = json.loads(path.read_text(encoding="utf-8"))` 使得JSON文件内部的JSON对象会被转换成Python对象（既可以是列表，也可以是字典，取决于JSON对象类型），再然后经由record_from_data把data合适的路由至函数record_from_mapping或函数record_from_sequence处理。考虑到题目本身给定的是函数record_from_mapping，不难判断：此时传入的data所引用的正是字典类型对象，否则该是由函数record_from_sequence处理data！
项目代码的开头有关键句 `Record = namedtuple("Record", "key source translation tags")`，这说明Record绑定的是名叫Record的命名元组类对象，因此，在这里的 `Record(...)` 创建的是命名元组类的实例对象（也就是函数record_from_mapping的返回值）。至此，一个JSON对象最终变成了Record的实例对象。
注意到Record实例化中，对于tags属性的值，会先将data指向的字典中的键名为'tags'的值交由函数normalize_tags处理，而从函数normalize_tags的函数体中不难看出：对于传入的None对象，它会返回一个空元组对象；对于传入的str对象，它会先将之按分号分隔成含有若干个元素的列表，再把列表中的元素（字符串对象）作首尾去除空白的处理，最后将非空的处理结果一一“装入”一个新的元组中并返回；对于传入的列表对象，它会把列表中的元素逐序取出并先后作字符串转型和首尾去除空白的处理，最后将非空的处理结果一一“装入”一个新的元组中并返回。所以，`tags` 如果是 `["ui", "menu"]`、`"ui;menu"`、`None`，那么，它们分别会变成('ui', 'menu')、('ui', 'menu')和()
另外，这里并没有涉及到复制外部JSON文件本身的流程！JSON文件的作用是数据来源，它所含有的JSON对象和Python对象并不是一回事，因此，流程中会涉及到数据结构的解析和转换，但不会是直接复制源文件本身。
```

### D2. CSV 输入与字段规范化（4 分）

解释为什么 CSV 文件需要表头 `key,source,translation`。如果 CSV 里 `tags` 是 `format;percent`，进入 `Record.tags` 后是什么对象？

答题区：

```text
首先，一个外部CSV文件的路径会被作为命令行参数的一部分，被项目里的build_parser函数返回的解析器的parse_args方法所解析，进一步的，经由run_demo、load_records这两个函数的处理已经可以确认是属于外部CSV文件输入场景，然后转由函数load_csv_records处理，而从函数load_csv_records的函数体中不难看出：若CSV文件没有表头，或是表头缺少 `key,source,translation` 这三者中的任意一个，都将直接抛出异常 ValueError，所以，CSV文件必须包含表头 `key,source,translation`！
在一切顺利的情况下，函数load_csv_records在执行过程中会涉及到对另一个函数record_from_mapping的调用，关键句是：`return [record_from_mapping(row, index) for index, row in enumerate(reader)]`，这意味着：如果CSV里的 `tags` 是 `format;percent`，那么和上一题的“`tags` 如果是 `"ui;menu"`，最终会变成什么？”类似，在这里，`format;percent` 进入  `Record.tags` 最终会变成('format', 'percent')
```

### D3. 占位符重排：什么时候允许，什么时候危险？（5 分）

判断下面两组翻译是否应该报占位符 mismatch，并解释原因。

```text
source      = "%(item)s x%(count)d"
translation = "%(count)d x%(item)s"
```

```text
source      = "%s x%d"
translation = "%d x%s"
```

答题区：

```text
对于第一组翻译而言，不应该报占位符 mismatch！首先，从源码中不难判断出这里涉及旧式的字符串格式化表达式，且采用的都是命名占位符，这类占位符对位置顺序相对而言不敏感，因为它的数据引用来源是映射对象，它只对名字本身敏感而不是名字的位置顺序，这能保证命名占位符在改变位置顺序的情况下依然能够精准取值；其次，通常来说，翻译文本为了达成语句通顺自然的目的，有时需要特定字段的重新排序。综上，这组翻译应该给pass！
而对于第二组翻译，首先，从源码中不难判断出这里也涉及旧式的字符串格式化表达式，但采用的都是位置占位符，这类占位符反而是依赖位置顺序的，因为它的数据引用来源多数时候是元组对象，而元组对象本身作为不可变序列，给值的时候自然是按序一一给出，倘若作为接收方的位置占位符换了位置，不仅很可能造成翻译文本的语义错误，甚至很可能触发异常 TypeError（比如这里的%s被换成了%d，若元组传入的值是字符串对象，d 这个类型码就会报错）。综上，对于这组翻译应该报占位符 mismatch！
```

### D4. JSON 报告输出边界（4 分）

解释这条转换链：

```text
Record -> record_to_dict(record) -> Python dict -> json.dumps(...) -> JSON 文本
```

请特别说明：为什么内部 `tags` 是 `tuple`，但 JSON 报告中的 `tags` 是数组/list 形式？

答题区：

```text
首先，为了达成JSON报告输出的目的，`--report-json` 会作为启动项目的命令行参数的一部分，被项目里的build_parser函数返回的解析器的parse_args方法所解析，进一步的，调用链到达了run_demo这里，基于题目要求，我们目前已有Record类的实例对象，在此省略从run_demo开始再到Record实例被接收的细节，这意味着下一步我们会经由函数run_demo后续的处理逻辑，转到函数issue_report_data中处理由若干个Record实例对象所组成的列表。
而从函数issue_report_data的函数体中不难看出：前面说的列表对象会先交由函数issue_report处理，而函数issue_report最后会返回一个有三元元组组成的列表对象，重点在于这个返回的列表中的每个元组的偏移量为1的元素正是每个Record实例对象！而在函数issue_report_data的后续处理中，这些Record实例对象还要逐一传入函数record_to_dict去进行数据转换处理，函数record_to_dict会返回一个字典对象，这个字典对象的键名分别是'key','source','translation'和'tags'，前三个键对应的值分别是Record实例对象的三个属性key,source,translation所对应的值，而字典的名为'tags'的键对应的值是Record实例对象的tags属性值经过列表转型后的结果！最终，函数issue_report_data返回一个包含了函数record_to_dict所返回的字典的字典对象。
再往后，调用链将走至函数dump_issue_report_json，并将刚提到的字典传入处理，从函数dump_issue_report_json的函数体中不难看出：这个字典将被交予json.dumps进行JSON文本序列化处理，并返回JSON的字符串对象！最后，将其打印输出以完成JSON文本报告输出任务！
至于说：“为什么内部 `tags` 是 `tuple`，但 JSON 报告中的 `tags` 是数组/list 形式？”，首先，为了表达不希望记录的 `tags` 字段被无意或随意修改，会在程序内部保持该字段的值类型是元组；其次，JSON中没有元组这个数据类型，但存在和列表很相似的数组类型！这意味着：最终的JSON报告生成前，需要再把元组给转型成列表，这个转型操作其实在上面的流程阐释中也提到过了。
```

### D5. 运行命令预测（3 分）

不运行代码，预测下面命令的大体行为：它会使用内置样例还是外部文件？输出给人读还是给机器读？是否还会打印解包演示？

```powershell
python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\mini_project_localization_records.py --input practice\P2_Types_and_Operations\C8_Lists_and_Tuples\sample_localization_records.json --report-json
```

答题区：

```text
不难看出：这个命令行中含有参数 `--input practice\P2_Types_and_Operations\C8_Lists_and_Tuples\sample_localization_records.json` 以及 `--report-json`，前者说明了这是外部JSON文件输入场景，而后者说明了同时还有输出JSON报告的需求！
而从程序代码中，不难判断：
首先，因为命令行参数 `--input practice\P2_Types_and_Operations\C8_Lists_and_Tuples\sample_localization_records.json`被解析后会导致传入run_demo的名为input_path的参数值不为空，所以程序不会使用内置样例，而是使用命令行参数中提及的相对路径所指向的外部文件作为最初的数据来源；
其次，经过上一题的分析，我们已经知道 `--report-json` 这个命令行参数会导致最终的结果是：JSON文本数据被打印输出至终端！因此，可知这条命令的输出是给人读的而不是给机器读的；
最后，“是否会打印解包演示”对应了代码中的关键行 `if issues_only or not records: return`，很明显，命令行中没有参数 `--issues-only`，因此可以说：若外部JSON文件的内容为空，则不打印解包演示，否则依然还会打印解包演示！
```

---

## E. 工程设计与概念迁移（20 分）

### E1. 本地化记录结构设计（8 分）

你要处理一批游戏本地化记录，每条记录包含：

```text
key, source, translation, tags
```

要求：

- 记录集合需要支持追加、删除、排序、过滤。
- 单条记录不希望被随意改动字段。
- `tags` 不希望被无意原地修改。
- 需要检查重复 key、空翻译、真实换行与字面量 `\n` 混淆、占位符是否保留。
- 需要把检查结果输出成 JSON 供其它工具读取。

请设计你会使用的数据结构，并说明每个选择背后的对象模型理由。必须至少谈到 `list`、`tuple` / `namedtuple`、`dict`、`Counter` 或 `set` 中的三个。

答题区：

```text
首先，为了满足上述要求，我会采用下列数据结构来进行本地化记录结构的设计：
list
namedtuple / tuple
dict
set / Counter
1.对于list：按照这一要求“记录集合需要支持追加、删除、排序、过滤。”，我认为列表作为所谓的“记录集合”非常合适，因为列表是支持：原地修改（包括但不限于：元素的追加、任意位置的数据插入、元素的移除、内部元素的重新排序、内部元素的位置翻转等等）；收集任意类型对象；任意嵌套的可变序列！而且，对于这一要求“需要检查重复 key、空翻译、真实换行与字面量 `\n` 混淆、占位符是否保留。”，检查的过程中必然涉及到中间检查结果的存储，将结果简述这类str、结果来源如 `key`；`index`这类标志性字段的值都放进列表中，可以方便对检查结果进行任意的增删改查等原地操作！此外，对于这一要求“需要把检查结果输出成 JSON 供其它工具读取。”，Python的列表也是Python中为数不多可以直接进行JSON序列化处理的数据类型！
2.对于namedtuple：按照这一要求“单条记录不希望被随意改动字段。”，我认为命名元组作为所谓的“单条记录”非常合适。首先，由题目给定的背景可知每条记录的构成是稳定的，都是由字段 `key, source, translation, tags` 组成的结构；其次设计要求强调了单条记录不可变，而命名元组既拥有类似字典那样的“键名（在命名元组中是 `字段名` ）比偏移量数字更具可读性”的优点，也有字典所不具备的不可变的特性！
3.对于tuple：按照这一要求“`tags` 不希望被无意原地修改。”，我认为元组作为所谓的“`tags`”非常合适。`tags` 的内容通常都是若干个字符串对象，而且内容相对稳定不易变，将它们置入元组中可以“巩固”元组的不可变性使其变成可哈希对象，这进一步保障了“`tags` 不希望被无意原地修改。”的需求！另外，对于这一要求“需要检查重复 key、空翻译、真实换行与字面量 `\n` 混淆、占位符是否保留。”，前面也提到过，列表适合作为检查结果的临时存储，事实上，如果结果本身的结构稳定，且属于不再修改的最终结果的话，也可以考虑用元组储存！
4.对于dict：按照这一要求“需要把检查结果输出成 JSON 供其它工具读取。”，我认为字典作为所谓的“待输出成JSON的检查结果”非常合适。除了Python的列表，Python的字典也支持直接进行JSON序列化的操作！通常来说，“待输出成JSON的检查结果”不仅意味着是最终结果，还意味着这是一份具有结构清晰、一定体量等隐含特征的报告文本，而字典作为Python内置的核心对象类型中唯一的映射类型对象，它很显然“胜任这份工作”！
5.对于set：虽然在这里的问题上用处不广，但是考虑到“缺失关键字段”的检查使用集合运算会很方便，我还是不会放弃它
6.对于Counter：按照这一要求“需要检查重复 key”，我认为Counter实例对象作为所谓的“检查重复字段名的检查工具”非常合适。集合（甚至包括字典）虽然也有对元素（或者对字典的键名）去重的能力，但是它们很高效的把检查重复并去除重复这一套流程隐式的完成了，因此，对于不仅要“检”，还要“查”的场景，Counter实例对象会更加合适，它只作字段名数目的统计，业务上下一步究竟是报告还是去重它不做干涉，这也有利于程序的扩展性！
```

### E2. 找出潜在共享引用风险（5 分）

下面代码有什么风险？如何修改更稳？

```python
shared_tags = ["ui"]

records = [
    Record("menu.start", "Start", "Begin", shared_tags),
    Record("menu.quit", "Quit", "Quit Game", shared_tags),
]

records[0].tags.append("reviewed")
```

答题区：

```text
`shared_tags = ["ui"]` 是一个赋值语句，其中的 `["ui"]` 是创建新的列表对象的字面量表达式，并且，名字shared_tags被绑定到了这个列表对象上。
`records = [
    Record("menu.start", "Start", "Begin", shared_tags),
    Record("menu.quit", "Quit", "Quit Game", shared_tags),
]` 是一个赋值语句，其中的 `[Record("menu.start", "Start", "Begin", shared_tags), Record("menu.quit", "Quit", "Quit Game", shared_tags), ]` 是创建新的列表对象的字面量表达式，并且，名字records被绑定到了这个列表对象上。要注意：这个新建的列表对象目前保存了两个指向Record实例对象的引用，Record本身是命名元组类对象，它的实例本身是具有不可变的特性的，可是从实例化的具体过程中不难看出：传入了可变对象（shared_tags绑定的列表）作为实例对象的第四个属性（tags）的值，这意味着：名字shared_tags绑定的列表对象被records[0].tags和records[1].tags共享！也就是说，这一步引入了共享引用的风险。
而`records[0].tags.append("reviewed")` 是一个列表的append方法的调用表达式，此操作将原地修改records[0].tags指向的列表对象（要注意这是被共享的列表对象），在其末尾追加一项（"reviewed"）。前面刚提到：名字shared_tags、records[0].tags和records[1].tags指向的其实是同一个列表对象，因此这里的操作也会同步修改shared_tags和records[1].tags绑定的对象，结果就是：records绑定的记录集合（列表）中的所有记录（Record实例）都发生了tags属性值的变化！
这通常是不合理的，对于每一条记录来说，它们应该是相互独立的，哪怕某些记录需要针对性的修改，也必须约束修改范围以避免对无关记录的误改！针对本题的情况，由于tags属性值通常都是若干个字符串，而现在又有对包含tags属性值的容器修改的需求，所以可以考虑把第二步改为：records = [
    Record("menu.start", "Start", "Begin", shared_tags[:]),
    Record("menu.quit", "Quit", "Quit Game", shared_tags[:]),
]，
当然，力求最稳的话，还是更建议：把Record.tags约定为元组类型对象，如：
records = [
    Record("menu.start", "Start", "Begin", ("ui", )),
    Record("menu.quit", "Quit", "Quit Game", ("ui", )),
]，
当需要针对性的修改时，可以：`records[0].tags += ("reviewed",)`
```

### E3. `dict.fromkeys`、`set` 与保序去重（4 分）

如果有：

```python
keys = ["menu.start", "menu.quit", "menu.start", "menu.options"]
```

请比较下面两种去重方式的差异，并说明它们的去重本质是否都依赖 `==` 和 `hash`。

```python
list(dict.fromkeys(keys))
list(set(keys))
```

答题区：

```text
首先，`keys = ["menu.start", "menu.quit", "menu.start", "menu.options"]` 是一个赋值语句，其中的 `["menu.start", "menu.quit", "menu.start", "menu.options"]` 是创建新的列表对象的字面量表达式，并且，名字keys被绑定到了这个列表对象上。由于无论是字典，还是集合，它们的去重本质都依赖`__eq__`和`__hash__`，因此，作为可哈希对象的字符串是允许作为字典的键或是集合的元素的。也就是说，keys保存的引用所指向的对象都可以作为字典的键或集合的元素，同时，不难看出：keys[0]和keys[2]这两个引用指向的对象在字典或集合中将被当作重复键名或重复元素。
对于第一种去重方式：`list(dict.fromkeys(keys))` 是一个list调用表达式，该表达式会返回一个以keys绑定的列表作元素去重处理后的结果作为内容的新的列表对象，重点是其中的表达式 `dict.fromkeys(keys)`，它会试图把keys引用的列表内的所有元素按原有的顺序一一作为一个待返回的新建的字典对象的键，并且这个新建字典的每个键对应的值都用 None 占位。而字典会对内部的键名作去重处理，且当前版本的Python实现了字典对象的保序特点，所以，最终的效果就是：这种去重属于保序去重，而这个表达式返回的结果会是：["menu.start", "menu.quit", "menu.options"]
对于第二种去重方式：`list(set(keys))` 是一个list调用表达式，该表达式会返回一个以keys绑定的列表作元素去重处理后的结果作为内容的新的列表对象，重点是其中的表达式 `set(keys)`，它会试图把keys引用的列表内的所有元素按随机的顺序作为一个待返回的新建的集合对象的元素，这里要注意和第一种去重方式的差别：集合是无序、去重且基于哈希的容器类型，集合也会对内部的元素作去重处理，但它并不保证处理后的结果保留原有的顺序，所以，最终的效果就是：这种去重属于无序去重，当没有保序的前提下去达成去重的目的时，也可以考虑使用集合，而这个表达式返回的结果具体是什么内容难以预测，不过很可能与上一种方式的结果不同。
```

### E4. 阶段自评（3 分）

请用 5 到 8 句话自评：本阶段你最稳定掌握的 2 个点是什么？仍最容易出错的 2 个点是什么？你准备如何用迷你项目继续巩固？

答题区：

```text
本阶段最稳定掌握的点有：
①列表作为可能是Python中最通用的可变序列，我能明确的知道：针对列表对象的索引取值、切片取值、拼接和重复这些序列操作都不会原地修改原列表对象，但是对一个列表对象的索引赋值、切片赋值、+=这些操作会原地修改原列表！此外，列表的append、extend、insert、sort、reverse、pop、remove、clear这些明显的“增删改”方法也会原地修改原列表且大多数这类方法不会返回修改后的对象而是返回None对象，而列表的count、index等少数方法并不会修改原对象！
②元组作为可能是Python中与列表“关系最近”的不可变序列，我能明确的知道：元组语法中，真正创建元组的是逗号而不是圆括号！元组尽管是不可变对象，但和数字、字符串这两类可哈希对象不同的是：如果元组保存了可变对象的引用，那么元组的内容仍旧可能改变，同时这样的元组也不是可哈希对象！
本阶段仍易出错的点有：
①命名元组的理解还不够深入：我能感觉到它似乎是一个元组、类和字典的混合体，但就像bytearray对象一样，这种形似“混合数据结构”的对象需要更多的应用才能加深对它们的理解，当然这个问题的部分原因也包含：对类和字典的学习还待跟进！
②对于嵌套列表和共享引用还有些“卡点”：我知道列表的重复会复制引用！例如：L = [[0] * 3] * 3，我明白的是：L[0] is L[1] is L[2]，甚至有 L[0][0] is L[0][1] is L[0][2] is L[1][0] is L[1][1] is L[1][2] is L[2][0] is L[2][1] is L[2][2]，我真正疑惑的点在于：执行 `L[0][1] = 9` 之后，结果是 [[0, 9, 0], [0, 9, 0], [0, 9, 0]]，首先，L最内层的九个引用指向的都是数字这种不可变对象，我倾向于将这九个引用看成是九个临时变量a-i以便于理解，换言之，在更一般的情景下，九个名字指向同一个数字对象，而形如  `L[0][1] = 9` 这样的表达式可以类比成其中一个名字更换了绑定，那么，很容易想到其它八个名字不该受影响并继续绑定着原数字对象，再回到当前场景，这意味着结果应该是 [[0, 9, 0], [0, 0, 0], [0, 0, 0]]？可是，如果我把目光聚焦在“偏外层”的层面，也就是只看L指向的对象自身所保存的三个引用这一层级，似乎又说得通了：执行 `L[0][1] = 9` 之后，显然L[0]绑定的列表会发生原地改变，又因为L[0] is L[1] is L[2]，所以另外两个引用指向的可变对象也发生同样的改变，所以结果确实是 [[0, 9, 0], [0, 9, 0], [0, 9, 0]]？这种在不同层级的理解产生了不一样的预测结果是为什么？
最后，针对上述提问我准备在启动迷你项目的命令行中添加参数 `--shared-tags-demo` 来试着解决问题！
```

---

## 作答后审批说明

你完成作答后，把本文件交给我审批。我会：

1. 保留你的原答案。
2. 在文件中追加逐题批改记录。
3. 给出建议分数。
4. 判断当前小阶段是否通过。
5. 追加“学习画像更新”草案，并同步到 `notes/Python_Learning_Profile.md`（如需）。

---

## Codex 批改记录（逐题审批，2026-05-21）

审批原则：

- 保留原答案，不直接改写你的作答内容。
- 以代码审查方式处理：先指出问题，再给修正规则。
- 小偏差也记录，尤其是会影响“对象本体 / 名字绑定 / 原地修改 / 重新绑定 / 显示形式 / 共享引用 / 拷贝层级”的地方。

### 总体结论

建议分数：`88 / 100`

阶段判断：**通过列表和元组小阶段测验**。可以进入下一个小阶段。更准确地说，下一小阶段应是“字典和文件”，并承担当前大阶段核心对象类型的收束复盘；进入前建议先复盘本记录中的 4 个重点：`namedtuple._replace()` 的对象复用、`deepcopy` 对不可变对象的处理、`--report-json` 的提前返回控制流、嵌套列表重复引用的层级模型。

这份答卷的主干非常稳：大多数题都能按“源码 -> 对象 -> 名字绑定 -> 原地修改/重新绑定 -> 输出显示”的链条说明。真正扣分的地方不是不会运行结果，而是少数解释中把机制说得过头了，例如把 `_replace()` 说成深拷贝、把 `deepcopy` 对字符串的处理说成一定不共享、把 JSON 报告输出说成偏向人读，以及在嵌套列表层级上仍有一个尚未完全压实的问题。

### 逐题评分总表

| 题目 | 得分 | 审批结论 |
| --- | ---: | --- |
| A1 | 6 / 6 | 正确。赋值不复制对象、完整切片创建新外层列表、`==` 与 `is` 的区分清楚。 |
| A2 | 6 / 6 | 正确。`append()` / `sort()` 返回 `None`，`sorted()` 返回新列表，解释到位。 |
| A3 | 5 / 6 | 主体正确；但 `a += ["checked"]` 更接近 `a.extend(["checked"])`，不能泛化为 `append("checked")`。 |
| B1 | 5.5 / 6 | 输出和主干正确；切片赋值时右侧列表对象本身不会被“植入”，而是其元素引用被写入目标区间。 |
| B2 | 5 / 5 | 正确。扩展切片赋值必须目标位置数量与右侧元素数量一致，且异常发生在赋值语句处。 |
| B3 | 5 / 5 | 正确。能区分重复引用和列表推导每次创建新内层列表。 |
| B4 | 3.5 / 4 | 主体正确；但 `deepcopy` 通常会复用不可变原子对象，例如字符串对象可以共享，这不是需要忽略的 CPython 小细节。 |
| C1 | 3.5 / 4 | 类型判断正确；元组 `repr` 的单元素显示是 `('menu.start',)`，逗号后通常不会显示空格。 |
| C2 | 4.5 / 5 | 主体正确；“元组内容发生变化”要更精确地说成“元组保存的引用没变，但引用指向的可变对象发生了原地修改”。 |
| C3 | 4.5 / 5 | 结果正确；扩展解包不是完全不受数量限制，仍要求非星号目标至少能绑定到元素。 |
| C4 | 4 / 6 | 结果主干部分正确；但 `namedtuple` 的 `repr` 写错，且 `_replace()` 不会深拷贝未替换字段。 |
| D1 | 5.5 / 6 | 正确。JSON 到 Python 对象、mapping 到 `Record`、`tags` 规范化都说清楚了。 |
| D2 | 4 / 4 | 正确。CSV 表头、必需字段和 `tags` 的分号拆分都判断准确。 |
| D3 | 5 / 5 | 正确。命名 `%` 占位符允许重排，位置 `%` 占位符重排危险。 |
| D4 | 3.5 / 4 | 主体正确；需要更明确：JSON 没有 tuple，`json.dumps()` 会把 Python 的 tuple/list 都序列化成 JSON array。 |
| D5 | 1 / 3 | 外部 JSON 输入判断正确；但 `--report-json` 输出是结构化机器可读 JSON，且会提前 `return`，不会打印解包演示。 |
| E1 | 7 / 8 | 工程设计整体合理；但“列表/字典可以直接 JSON 序列化”要加前提：内部元素也必须可序列化。 |
| E2 | 4 / 5 | 共享引用风险判断正确；但 `records[0].tags += (...)` 对 namedtuple 字段会失败，应使用 `_replace()` 并重新绑定记录。 |
| E3 | 3.5 / 4 | 主体正确；`set` 不是“随机顺序”，而是“不保证保留插入顺序”。Python 3.9 中 dict 保序是语言保证。 |
| E4 | 2 / 3 | 自评诚实且抓住了关键问题；嵌套列表层级处仍有概念卡点，下面单独修正。 |

分项合计：

```text
A. 对象、绑定与方法返回值：17 / 18
B. 切片、嵌套列表与拷贝层级：19 / 20
C. 元组、解包、namedtuple 与函数边界：16.5 / 20
D. 新版迷你项目代码阅读：19 / 22
E. 工程设计与概念迁移：16.5 / 20
总分：88 / 100
```

### 逐题批注与纠错

#### A1 审批

正确。你已经能稳定说明 `alias = records` 只是让两个名字绑定同一个列表对象，而 `snapshot = records[:]` 创建新的外层列表。这里没有发现实质性漏洞。

小措辞建议：`snapshot` 是浅拷贝结果，不建议叫“复制品”后就停住；你后文已经补上“内部保存的引用会继承保留”，这点很好。

#### A2 审批

正确。`append_result` 和 `sort_result` 都是 `None`，而 `items` 被原地修改；`sorted_result` 是新列表。这里对“方法返回值 vs 被修改对象”的区分稳定。

#### A3 审批

主体正确，但有一个需要显式纠正的小偏差：

```python
a += ["checked"]
```

对列表来说更接近：

```python
a.extend(["checked"])
```

而不是一般意义上的：

```python
a.append("checked")
```

本题里 `["checked"]` 只有一个元素，所以最终列表内容与 `append("checked")` 一样；但机制不同。`append(x)` 是把 `x` 作为一个元素追加进去，`extend(iterable)` / `+= iterable` 是把可迭代对象中的元素逐个追加进去。

对比：

```python
a = ["ui"]
a.append(["checked"])
print(a)  # ['ui', ['checked']]

b = ["ui"]
b += ["checked"]
print(b)  # ['ui', 'checked']
```

另外，你说“增强赋值后名字 a 重新绑定到同一个对象”可以接受，但要知道学习重点不是“它有没有执行一次 STORE”，而是：对列表而言，旧列表对象被原地扩展，外部别名能观察到变化。

#### B1 审批

主干正确。需要修正一个细节：普通切片赋值中，右侧 `["continue", "save", "options"]` 这个列表对象本身不会作为一个元素被塞进 `keys`；被写入 `keys` 的是右侧可迭代对象中的三个元素引用。

所以更精确的说法是：

```text
keys[1:3] 这个连续区间原来有 2 个槽位；
赋值后这个区间被替换为右侧 iterable 产生的 3 个元素；
keys 这个外层列表对象仍是原对象，只是内部槽位数量和引用发生了变化。
```

#### B2 审批

正确。你这题没有重犯之前那次“当前对象状态没算进去”的问题，已经能根据实际长度判断 `items[::2]` 命中的目标位置数量。

#### B3 审批

正确。`bad` 的外层列表有三个槽位，但三个槽位保存的是同一个内层空列表的引用；`good` 每轮列表推导都会创建新的内层空列表。解释到位。

#### B4 审批

主体正确，但这里有一个重要边界需要纠正：

你写道深拷贝后“外层列表内部包含的引用所指向的对象（无论是嵌套列表还是不可变字符串）都不是共享的”。这句话对嵌套列表是对的，对字符串不对。

更精确的规则是：

```text
copy.deepcopy() 会递归复制容器和多数可变对象；
对不可变原子对象，例如 str、int、None，通常直接复用原对象；
这种共享是安全的，因为不可变对象不能被原地修改。
```

校准实验：

```python
import copy

original = [["menu.start", ["ui"]]]
deep = copy.deepcopy(original)

print(original is deep)              # False
print(original[0] is deep[0])        # False
print(original[0][1] is deep[0][1])  # False
print(original[0][0] is deep[0][0])  # True，字符串可共享
```

所以本题应说：`deep` 隔离了外层列表和嵌套列表；字符串对象是否共享不影响行为，且通常会共享。

#### C1 审批

概念正确：创建非空元组的关键是逗号，空元组必须写 `()`。小扣分点只是显示形式：Python 的 `repr` 通常显示为：

```python
('menu.start',)
```

不是：

```python
('menu.start', )
```

这属于显示层细节，不影响主干判断。

#### C2 审批

主体正确。需要把“元组内容变化”这句话改得更锋利：

```text
元组自身保存的三个引用没有改变；
record[2] 仍然指向原来的那个列表对象；
发生变化的是这个列表对象的内容；
因此容器显示形式看起来变了，但元组槽位没有被替换。
```

这就是“元组浅不可变”的核心边界。

#### C3 审批

结果正确。补一个边界：扩展解包不是完全“数量无所谓”。星号目标可以接收 0 个或多个元素，但非星号目标仍必须有元素可绑定。

例如：

```python
first, *middle, last = ["only"]
```

会报 `ValueError`，因为 `first` 和 `last` 两个非星号目标至少需要两个元素。

#### C4 审批

这里是本卷的一个主要扣分点。

第一，`namedtuple` 实例的显示形式不是：

```python
Record("menu.start", "Start", "Start Game", ("ui", "menu"))
```

实际是：

```python
Record(key='menu.start', source='Start', translation='Start Game', tags=('ui', 'menu'))
```

第二，`record._replace(...)` 不会把其它字段“深拷贝而来”。它会创建一个新的 `Record` 实例，并把未替换字段的引用直接复用过来。这里的：

```python
print(record.tags is updated.tags)  # True
```

不是因为 `tags` 可哈希，也不是 CPython 优化，而是 `_replace()` 的正常语义：未替换字段沿用原来的对象引用。

正确模型：

```text
Record 是 namedtuple 工厂创建出来的类对象；
record 是这个类的一个实例；
updated 是 _replace() 返回的新实例；
record 和 updated 是两个不同的 Record 实例；
translation 字段绑定到不同字符串；
tags 字段复用同一个 tuple 对象。
```

#### D1 审批

正确。你能把 JSON 文件、`json.loads()` 后的 Python 对象、mapping 分支、`Record` 实例化、`tags` 规范化分层说明，这说明你已经能把列表/元组知识迁移到文件边界。

一个术语小修正：严格说 JSON 中的 `object` 对应 Python `dict`，JSON 中的 `array` 对应 Python `list`。你后面已经回到 mapping/dict 分支，所以没有实质问题。

#### D2 审批

正确。CSV 的 `DictReader` 需要表头来生成每一行的 mapping；`key`、`source`、`translation` 是必需列；`format;percent` 会被 `normalize_tags()` 转成 `('format', 'percent')`。

#### D3 审批

正确。你对本地化中的“命名占位符可重排、位置占位符不应随意重排”理解很好。

小措辞建议：题目里的两行文本本身是“格式化模板字符串”，还不是完整的“格式化表达式”。完整表达式需要再加 `% data` 这一侧。

#### D4 审批

主体正确。再压实一层：

```text
内部 Record.tags 使用 tuple，是为了避免项目内部无意原地修改；
record_to_dict() 主动把 tuple 转成 list；
json.dumps() 会把 Python list 序列化成 JSON array；
即使直接把 tuple 交给 json.dumps()，它也会按数组形式输出，因为 JSON 没有 tuple 类型。
```

你的回答已经抓住了“内部对象模型”和“外部 JSON 文本格式”不是一回事。

#### D5 审批

这题有两处实质错误。

正确判断：

```text
1. 会使用 --input 指定的外部 JSON 文件，不使用内置样例。
2. --report-json 输出的是结构化 JSON，主要定位是机器可读；只是因为 indent=2，也兼顾人类查看。
3. 不会打印解包演示。
```

原因在 `run_demo()` 的这段控制流：

```python
if report_json or json_output:
    data = issue_report_data(records, max_length, source_name)
    if json_output:
        dump_issue_report_json(data, json_output)
    if report_json:
        dump_issue_report_json(data)
    return
```

一旦 `--report-json` 为真，函数会在这里直接 `return`。所以后面的普通 `Issue report`、`Unpacking one record` 都不会执行。

你原回答里引用的：

```python
if issues_only or not records: return
```

只有在没有进入 JSON 报告分支时才有机会执行。

#### E1 审批

工程设计整体合理。你已经能把可变集合用 `list`、稳定单条记录用 `namedtuple`、`tags` 用 `tuple`、重复 key 用 `Counter`、报告输出用 `dict` 组合起来，这正是本阶段迷你项目想训练的能力。

需要修正两个边界：

1. “Python 的列表/字典可以直接 JSON 序列化”要加前提：里面的元素也必须是 JSON 可序列化的对象。比如 `Record`、`set`、任意自定义对象不能不经转换就稳定输出为 JSON。
2. `tags` 用 tuple 的核心理由是避免原地修改和表达稳定结构；“变成可哈希对象”只是附带条件，而且只有当 tuple 内部元素也都可哈希时才成立。

#### E2 审批

共享引用风险判断正确，但修正方案里有一个重要错误。

你建议：

```python
records[0].tags += ("reviewed",)
```

这对 `namedtuple` 字段会失败。增强赋值对属性目标大致等价于：

```python
records[0].tags = records[0].tags + ("reviewed",)
```

而 `namedtuple` 实例不允许给字段重新赋值，所以会报：

```text
AttributeError: can't set attribute
```

更稳的写法是创建新记录，并替换列表里的那一条记录：

```python
records[0] = records[0]._replace(
    tags=records[0].tags + ("reviewed",)
)
```

这正好再次体现本阶段主线：**元组/命名元组不可原地改字段；要表达更新，就创建新对象并让外层列表的某个槽位重新绑定到新对象。**

#### E3 审批

主体正确。两个措辞需要修正：

1. `set` 的顺序不是“随机”，而是“不保证保留输入顺序”。某一次运行可能看起来稳定，但语言语义不承诺它等于原顺序。
2. 在 Python 3.9 中，`dict` 保持插入顺序已经是语言保证，不只是“当前版本实现特点”。因此 `list(dict.fromkeys(keys))` 是保序去重的常见写法。

#### E4 审批

你的自评很有价值，因为它准确暴露了当前阶段最值得补的一块：嵌套列表的“槽位层级”。

关键修正如下。

对于：

```python
L = [[0] * 3] * 3
```

不要把它理解成“九个临时变量 a-i”。更准确的对象图是：

```text
inner = [0, 0, 0]
L = [inner, inner, inner]
```

也就是说：

```python
L[0] is L[1] is L[2]  # True
```

外层列表 `L` 有 3 个槽位；这 3 个槽位都保存同一个内层列表对象的引用。内层列表对象只有一个，它自己有 3 个槽位。

所以：

```python
L[0][1] = 9
```

分两步看：

```text
L[0]     -> 取出那个唯一的 inner 列表；
[1] = 9  -> 把 inner 的第 1 个槽位改为指向整数 9。
```

被改的是同一个 `inner` 对象。因为 `L[0]`、`L[1]`、`L[2]` 都只是从不同外层槽位看向同一个 `inner`，所以显示结果会是：

```python
[[0, 9, 0], [0, 9, 0], [0, 9, 0]]
```

你“九个名字”的类比错在：这里没有九个独立内层槽位，只有一个内层列表的三个槽位，被外层列表显示了三次。数字 `0` 是否不可变不是这里的关键；关键是“有几个内层列表对象”。如果写成：

```python
L = [[0] * 3 for _ in range(3)]
```

才是三个独立内层列表对象，此时 `L[0][1] = 9` 的结果才会是：

```python
[[0, 9, 0], [0, 0, 0], [0, 0, 0]]
```

### 本阶段末评语与能力判断

你已经通过本阶段。更准确地说，你不是“刚刚会用列表和元组”，而是已经能把它们放进对象模型、文件输入、JSON/CSV 边界、本地化记录处理、占位符检查这些工程场景里解释。

当前稳定掌握：

- `a = b` 不复制列表对象，只复制绑定关系。
- `append()`、`sort()` 等原地方法返回 `None`，`sorted()` 返回新列表。
- 普通切片读取创建新外层列表，切片赋值原地修改旧列表。
- 浅拷贝只复制外层容器，深拷贝隔离嵌套可变对象。
- 元组由逗号创建，元组槽位不可替换，但槽位中的可变对象仍可被修改。
- 能把 `list`、`namedtuple`、`tuple`、`dict`、`Counter` 组合成一个合理的小型本地化批处理工具。

仍需主动复盘：

- `_replace()` 返回新 `namedtuple` 实例，但未替换字段复用原引用，不是深拷贝。
- `copy.deepcopy()` 对不可变原子对象通常复用原对象；深拷贝的学习重点是隔离可变嵌套对象。
- `--report-json` / `--json-output` 这类 CLI 选项会改变控制流，不能只根据后半段普通输出逻辑预测行为。
- 嵌套列表重复引用要先数“容器对象有几个”，再看每个容器的槽位保存哪些引用。
- 描述元组不可变时，尽量说“槽位引用不可替换”，少说“元组内容变了”这种容易混层的话。

阶段结论：**列表和元组小阶段通过，建议进入“字典和文件”小阶段，并在该阶段末尾进行核心对象类型收束复盘。**

### 学习画像更新（写入档案版）

阶段：列表和元组

证据：

- 阶段测验建议得分：`88 / 100`。
- 已完成并复盘 `mini_project_localization_records.py`，包含 JSON/CSV 输入、结构化 JSON 报告、`Record` / `namedtuple`、占位符检查、浅/深拷贝与共享引用演示。
- 答卷能稳定解释多数列表原地修改、名字绑定、切片、拷贝、元组不可变和解包行为。
- 答卷暴露的主要弱点集中在少数高级边界：`_replace()` 不是深拷贝、`deepcopy` 对不可变对象可共享、JSON 报告分支提前返回、嵌套列表重复引用层级仍需再压实。

当前判断：

你在 Python 类型和运算阶段已经从“语法层学习者”进入“对象模型驱动的准中级入门者”。列表和元组阶段达到通过标准，且工程迁移能力明显增强。下一阶段可以进入“字典和文件”，但需要特别关注哈希、相等性、键对象不可变性、插入顺序、视图对象、浅拷贝、文件对象、文本/字节/编码边界，以及 JSON object 与 Python dict 的边界。

下一阶段关注点：

- 字典的键为什么必须可哈希，`==` 和 `hash` 如何共同影响键去重。
- 字典保存的是键和值的引用，修改可变值对象和重新绑定某个键对应的值不是一回事。
- `dict.fromkeys()`、字典推导式、`Counter`、`defaultdict` 等工具的对象模型和工程用途。
- 路径字符串、文件对象、文本内容、字节内容、编码/解码之间的边界。
- JSON object、Python dict、配置文件、本地化资源表之间的边界。
- 在阶段末尾横向复盘数字、字符串、列表、元组、字典、集合和文件这些核心对象类型。
