# Stage Quiz: Dictionaries, Files, and Core Type Synthesis

本测验用于当前小阶段：**字典和文件：映射、持久化边界与核心类型收束**。

这也是 Types and Operations 大阶段的阶段末综合验收卷。它不只考字典 API 或文件 API，而是考你是否能把对象模型、哈希、映射、可变性、文件对象、编码、JSON/CSV、本地化资源审计和核心对象类型选型放到同一张图里解释。

总分：100 分。

答题规则：

1. 第一遍不要运行代码，先写预测、对象身份变化、返回值和理由。
2. 第二遍可以用 Python 3.9.13 验证，并标注“验证前预测”和“验证后修正”。
3. 每道代码题尽量按这条链解释：源码写了什么、创建了什么对象、名字绑定到哪里、哪一步修改容器本体、哪一步修改容器中的可变值对象、文件或 JSON 边界在哪里、输出为什么这样显示。
4. 本卷不包含参考答案。你作答后交给我审批，我会保留你的原答案并追加批改记录。
5. 若你认为题目本身有歧义，可以直接指出；这也属于本阶段能力的一部分。

---

## A. 字典、哈希与映射对象边界（18 分）

### A1. 键去重、保留键对象与值覆盖（6 分）

预测输出，并解释 `1`、`1.0`、`True` 为什么会发生键冲突。注意区分“保留哪个键对象”和“更新哪个值对象引用”。

```python
d = {}
d[1.0] = "float"
d[True] = "bool"
d[1] = "int"

print(d)  # {1.0: 'int'}
print(list(d.keys()))  # [1.0]
print(next(iter(d.keys())) is 1.0)  # 当前环境下的输出是True，但要注意这是CPython3.9的实现优化细节
print(next(iter(d.keys())) == 1)  # True
```

答题区：

```text
`d = {}` 是一个赋值语句，其中的 `{}` 是创建新的空字典对象的字面量表达式，并且，名字d被绑定到了这个字典对象上。
`d[1.0] = "float"` 是一个赋值语句，语句执行时，将修改d指向的字典对象本体，即：这个字典的键槽位新增一个指向浮点数对象1.0的引用，同时字典的值槽位新增一个指向字符串对象（"float"）的引用，并且字典保存二者的映射关系。
`d[True] = "bool"` 是一个赋值语句，语句执行时，将修改d指向的字典对象本体。Python的字典对键对象的要求是：键唯一且可哈希！所以，在这里，Python会首先基于__eq__和__hash__来判断新增的键引用指向的对象（True）是否和已存的键引用指向的对象（1.0）重复，若重复，则只会保留已有的键对象并更新已有的键对象的引用所映射的值对象引用；若不重复，才会让字典的键槽位和值槽位分别新增新的对象的引用并保存二个引用的映射关系。而hash(True) == hash(1.0)且True == 1.0，这意味着：True和1.0这两个键对象被视为重复键，因此，最后的结果是：d指向的字典对象保留已有的键对象1.0，并更新已有的键对象的引用所映射的值对象（"float"）的引用成为指向新的值对象（"bool"）的引用。
`d[1] = "int"` 是一个赋值语句，语句执行时，将修改d指向的字典对象本体。同理，因为hash(1) == hash(1.0)且1 == 1.0，这意味着：1和1.0这两个键对象被视为重复键，因此，最后的结果是：d指向的字典对象保留已有的键对象1.0，并更新已有的键对象的引用所映射的值对象（"bool"）的引用成为指向新的值对象（"int"）的引用。
综上，最终的d指向的字典对象长度为1，意即它的键槽位只保存了一个键对象（1.0）的引用。此外，`d.keys()` 这个表达式返回的是d指向的字典的“键”视图对象，它动态连接于该字典，及时且诚实的反映字典的键槽位变化！同时，这个视图对象也是一个可迭代对象，每次响应iter调用时都会返回一个新的迭代器对象，在迭代场景下，将内含的元素（在这里，其实就是d绑定的字典的键槽位所保存的键对象引用）逐一提供给迭代工具。还有一点要注意的是：尽管在这里的 `print(next(iter(d.keys())) is 1.0)` 输出为 True，但“身份相等”并不是字典的键去重的判断标准。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### A2. 自定义键的 `__eq__` / `__hash__` 合同（6 分）

预测输出，并说明为什么写自定义可哈希对象时，参与 `__eq__` 的稳定字段也必须一致地参与 `__hash__`。

```python
class LocKey:
    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name

    def __eq__(self, other):
        return (
            isinstance(other, LocKey)
            and self.namespace == other.namespace
            and self.name == other.name
        )

    def __hash__(self):
        return hash((self.namespace, self.name))


a = LocKey("menu", "start")
b = LocKey("menu", "start")
c = LocKey("menu", "quit")

d = {a: "Start"}
d[b] = "Begin"
d[c] = "Quit"

print(a is b)  # False
print(a == b)  # True
print(len(d))  # 2
print(d[a])  # Begin
print(d[b])  # Begin
print(d[c])  # Quit
```

答题区：

```text
首先，由LocKey这个自定义类对象的主要逻辑不难看出：LocKey实例化时必须传入两个对象分别作为LocKey实例对象的namespace和name属性的值；当LocKey实例对象参与 “==” 运算时，只有同时满足这两个条件：相比较的对象也是LocKey实例对象、相比较的对象的namespace和name属性的值分别和自身的namespace和name属性的值相等，运算结果才为True；当LocKey实例对象响应hash调用时，将尝试返回仅由自身的namespace和name属性的值作为元素的二元元组的哈希值。
其次，必须说明的一点是：自定义可哈希对象时，要特别注意：参与 `__eq__` 的稳定字段必须一致地参与 `__hash__`！因为：若不满足该条件，容易导致实例对象出现“值相等但哈希值不相等”的情形，而这对于基于哈希的数据结构（如Python的dict和set）来说是很危险的：事实上，集合对象对自身内含元素的去重和上题提到的字典对象对键的去重它们本质是一样的：都是基于“==”和“hash”而非“is”！所以仅拿字典来说，倘若现有两个自定义类的实例对象满足“值相等但哈希值不相等”，那么于字典而言，这两个对象并不是重复的（字典默认先按哈希值走查找路线，哈希不同，通常根本不会进入“这是同一个键吗”的正确比较位置），它们都可以作为字典的键对象并共存，但实际上二者确实是相等的，换言之，它们破坏了字典的语义，使得字典的去重失效，甚至还会导致字典的删除、查找等功能变得混乱！总之，写自定义可哈希对象时，要保证：若有a == b，则必须有hash(a) == hash(b)！
`a = LocKey("menu", "start")` 、`b = LocKey("menu", "start")`、`c = LocKey("menu", "quit")` 都是赋值语句，最终的效果是：名字a、b、c分别被绑定到了不同的LocKey实例对象上，而且，通过对a和b指向的对象的实例化过程的观察不难发现：a == b的运算结果为真，而设计LocKey这个自定义类对象时，已经保证了：参与 `__eq__` 的稳定字段也一致地参与了 `__hash__`，所以也可以得出：hash(a) == hash(b)的结果也为真。
`d = {a: "Start"}` 是一个赋值语句，其中的 `{a: "Start"}` 是创建新的字典对象的字面量表达式，并且，名字d被绑定到了这个字典对象上。目前这个字典的键槽位保存了一个LocKey实例对象（a）的引用，并且它映射至值对象（"Start"）的引用。
`d[b] = "Begin"` 是一个赋值语句，语句执行时，将修改d指向的字典对象本体。因为hash(b) == hash(a)且b == a，这意味着：b和a这两个键对象被视为重复键，因此，最后的结果是：d指向的字典对象保留已有的键对象a，并更新已有的键对象的引用所映射的值对象（"Start"）的引用成为指向新的值对象（"Begin"）的引用。
`d[c] = "Quit"` 是一个赋值语句，语句执行时，将修改d指向的字典对象本体。因为c != a，这意味着：c和a这两个键对象不会被视为重复键，因此，最后的结果是：d指向的字典的键槽位新增一个LocKey实例对象（c）的引用，并且值槽位新增一个值对象（"Quit"）的引用，字典保存两个引用的映射关系。
综上，可知：最终的d指向的字典对象长度为2，意即它的键槽位保存了二个键对象（a和c）的引用。此外，虽说b指向的LocKey实例对象并没有作为d绑定的字典的键对象，但是，正因为hash(b) == hash(a)且b == a，所以，Python在执行 `d[b]` 时并不会报错 KeyError，基于哈希的字典在搜索键对象b时等同于搜索键对象a，也就是说，在这里，`print(d[a])` 和 `print(d[b])` 的输出是一样的。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### A3. 可哈希边界与工程选型（6 分）

逐项说明下面哪些对象可以作为字典键，哪些不可以，并解释原因。不要只写“可变/不可变”，要说明是否所有内部元素都支持哈希。

```python
keys = [
    "menu.start",
    ("zh_CN", "menu.start"),
    ("zh_CN", ["menu.start"]),
    frozenset({"menu.start", "menu.quit"}),
    {"menu.start", "menu.quit"},
]
```

答题区：

```text
首先要明确的是：Python的字典对键对象的要求是：键唯一且可哈希！所以，在本题中，但凡是不可哈希对象都不可以作为字典的键对象。
`keys = ["menu.start", ("zh_CN", "menu.start"), ("zh_CN", ["menu.start"]), frozenset({"menu.start", "menu.quit"}), {"menu.start", "menu.quit"},]` 是一个赋值语句，其中的 `["menu.start", ("zh_CN", "menu.start"), ("zh_CN", ["menu.start"]), frozenset({"menu.start", "menu.quit"}), {"menu.start", "menu.quit"},]` 是创建并返回新的长度为5的列表对象的字面量表达式，列表保存了5个待判断对象的引用，并且，名字keys被绑定到了这个列表对象上。
`keys[0]` 也即 `"menu.start"`，这是一个创建并返回新的字符串对象的字面量表达式，Python的字符串对象默认按内容进行“等值性比较”，而字符串对象作为不可变对象，其内容不支持原地修改，可以说字符串对象的内容是稳定的，因此Python的字符串对象默认也按其内容可哈希。总之，这个字符串对象可以作为字典键；
`keys[1]` 也即 `("zh_CN", "menu.start")`，这是一个创建并返回新的元组对象的字面量表达式，Python的元组对象本体是否可哈希取决于内部槽位保存的引用指向的各对象是否都可哈希，只有元组内部所有的元素都可哈希，这个元组才是可哈希的。在这里，不难看出：这里新建的元组对象内部槽位保存的引用都指向字符串对象，前面刚解释过，字符串对象都是可哈希的，所以，这个元组对象确实是可哈希的，也就意味着：它可以作为字典键；
`keys[2]` 也即 `("zh_CN", ["menu.start"])`，这是一个创建并返回新的元组对象的字面量表达式，不过要注意的是：与前一个元组对象不同，这里新建的元组对象内部保存了一个指向列表对象的引用！Python的列表对象默认对其保存的所有引用指向的对象逐一进行“等值性比较”，然而列表对象作为可变对象，它支持对其内容的原地修改，这就意味着：它所保存的引用随时可能发生变化，是不稳定的，因此Python的列表对象是不可哈希的。前面刚提到过，只有元组内部所有的元素都可哈希，这个元组才是可哈希的，所以说，这里的这个元组对象是不可哈希的，它也不可以作为字典键；
`keys[3]` 也即 `frozenset({"menu.start", "menu.quit"})`，这是一个创建并返回新的冻结集合实例对象的调用表达式，Python的冻结集合实例对象既有类似元组那样的长度不可变的特点，也有类似集合那样的内部元素唯一且可哈希的要求。所以，冻结集合实例对象也是可哈希的，也就可以作为字典键；
`keys[4]` 也即 `{"menu.start", "menu.quit"}`，这是一个创建并返回新的集合对象的字面量表达式，虽然Python的集合对象内部所有元素都是可哈希的，但是，由于集合是可变对象，它也和列表一样，默认是对其内部保存的所有元素逐一进行“等值性比较”，这就意味着：它的内容是不稳定的，Python也将集合对象视为不可哈希对象。总之，这个集合对象不可以作为字典键。
```

---

## B. 字典方法、视图、拷贝与迭代风险（18 分）

### B1. 方法返回值与被修改对象（6 分）

预测输出，并说明 `get()`、`setdefault()`、`update()`、`pop()` 分别返回什么、是否修改字典。

```python
issues = {"menu.start": ["too long"]}

a = issues.get("menu.quit", [])
b = issues.setdefault("menu.quit", [])
b.append("missing")
c = issues.update({"menu.options": ["new"]})
d = issues.pop("menu.start")

print(a)  # []
print(b)  # ['missing']
print(c)  # None
print(d)  # ['too long']
print(issues)  # {'menu.quit': ['missing'], 'menu.options': ['new']}
print("menu.start" in issues)  # False
```

答题区：

```text
`issues = {"menu.start": ["too long"]}` 是一个赋值语句，其中的 `{"menu.start": ["too long"]}` 是创建并返回新的字典对象的字面量表达式，并且，名字issues被绑定到了这个字典对象上。目前这个字典的键槽位保存了一个字符串对象（"menu.start"）的引用，并且它映射至值对象（["too long"]）的引用。
`a = issues.get("menu.quit", [])` 是一个赋值语句，其中的 `issues.get("menu.quit", [])` 是（issues绑定的）字典对象的get方法的调用表达式，它表达：试图从issues绑定的字典对象中搜寻到键名为"menu.quit"的键，若找到了键就返回它映射的值，否则返回预设或给定的默认对象。很明显，此时的issues绑定的字典对象中并没有这样的键对象存在，所以这个调用表达式最后会返回给定的默认对象：一个空列表，最后，名字a被绑定到了这个列表对象上。此外，字典对象的get方法调用无论是否找到目标键，都不会原地修改字典本体。
`b = issues.setdefault("menu.quit", [])` 是一个赋值语句，其中的 `issues.setdefault("menu.quit", [])` 是（issues绑定的）字典对象的setdefault方法的调用表达式，它表达：试图从issues绑定的字典对象中搜寻到键名为"menu.quit"的键，若找到了键就返回它映射的值，否则，会先在这个字典的键槽位新增一个指向字符串对象"menu.quit"的引用，同时字典的值槽位新增一个指向预设或给定的默认对象（在这里，是给定的默认对象：[]）的引用，并且字典保存二者的映射关系，最后再返回预设或给定的默认对象（在这里，是给定的默认对象：[]）。很明显，此时的issues绑定的字典对象中并没有这样的键对象存在，所以这个调用表达式最后会原地修改字典对象本体并返回给定的默认对象：一个空列表，最后，名字b被绑定到了这个返回的空列表对象上。
`b.append("missing")` 是（b绑定的）列表对象的append方法的调用表达式，它会原地修改b绑定的列表对象，在列表尾部追加一个指向字符串对象（"missing"）的引用。要注意的是：这里的修改不仅作用在b指向的对象，也作用在issues绑定的字典对象刚刚新增的值对象上，因为它们二者实质是同一个可变对象。
`c = issues.update({"menu.options": ["new"]})` 是一个赋值语句，其中的 `issues.update({"menu.options": ["new"]})` 是（issues绑定的）字典对象的update方法的调用表达式，它表达：试图从issues绑定的字典对象中搜寻到键名为"menu.options"的键，若找到了键就更新它映射的值为["new"]，否则，会先在这个字典的键槽位新增一个指向字符串对象"menu.options"的引用，同时字典的值槽位新增一个指向列表对象（["new"]）的引用，并且字典保存二者的映射关系，最后，这个表达式总是返回None对象。很明显，此时的issues绑定的字典对象中并没有这样的键对象存在，所以这个调用表达式最后会原地修改字典对象本体并返回None对象，最后，名字c被绑定到了这个返回的None对象上。
`d = issues.pop("menu.start")` 是一个赋值语句，其中的 `issues.pop("menu.start")` 是（issues绑定的）字典对象的pop方法的调用表达式，它表达：试图从issues绑定的字典对象中搜寻到键名为"menu.start"的键，若找到了键就删除字典对象保存的关于该键的映射关系并返回它之前映射的值，否则，会报错KeyError（除非调用方法时传入了给定的默认对象，这种情况下会返回默认对象而不是直接报错）。很明显，此时的issues绑定的字典对象中存在这样的键对象，所以这个调用表达式最后会原地修改字典对象本体并返回这个键对象之前所映射的值对象，最后，名字d被绑定到了这个返回的列表对象（["too long"]）上。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### B2. 视图对象、列表快照与集合运算（6 分）

预测输出，并解释 `keys`、`items`、`snapshot` 的区别。顺带说明哪些视图支持集合运算，为什么。

```python
d = {"a": 1, "b": 2}
keys = d.keys()
items = d.items()
snapshot = list(keys)

d["c"] = 3
d["a"] = 10

print(keys)  # dict_keys(['a', 'b', 'c'])
print(items)  # dict_items([('a', 10), ('b', 2), ('c', 3)])
print(snapshot)  # ['a', 'b']
print(keys & {"a", "x"})  # {'a'}
print(("a", 10) in items)  # True
```

答题区：

```text
`d = {"a": 1, "b": 2}` 是一个赋值语句，其中的 `{"a": 1, "b": 2}` 是创建并返回新的字典对象的字面量表达式，并且，名字d被绑定到了这个字典对象上。目前这个字典的键槽位保存了二个字符串对象（"a"和"b"）的引用，并且它们分别映射至二个值对象（1和2）的引用。
`keys = d.keys()` 是一个赋值语句，其中的 `d.keys()` 是（d绑定的）字典对象的keys方法的调用表达式，它返回d绑定的字典的“键”视图对象，“键”视图对象如实的表达当前字典对象的键槽位保存的所有键对象引用，并且它和字典对象是动态连接的，这意味着：它也能及时的反映字典的键槽位发生的任何变化。最后，名字keys被绑定到了这个视图对象上。此外，字典对象的keys方法调用表达的语义更像“视察窗口”，因此它不会原地修改字典本体或是字典中的可变值对象。
`items = d.items()` 是一个赋值语句，其中的 `d.items()` 是（d绑定的）字典对象的items方法的调用表达式，它返回d绑定的字典的“条目”视图对象，“条目”视图对象如实的表达当前字典对象已保存的映射关系，并且它和字典对象是动态连接的，这意味着：它也能及时的反映字典所保存的映射关系中发生的任何变化。最后，名字items被绑定到了这个视图对象上。此外，字典对象的items方法调用表达的语义也像“视察窗口”，因此它不会原地修改字典本体或是字典中的可变值对象。
`snapshot = list(keys)` 是一个赋值语句，其中的 `list(keys)` 表达：把keys绑定的视图对象中的元素（其实就是d引用的字典对象的所有键对象）一一迭代出来并逐序放入一个列表中，最后返回该列表对象，名字snapshot被绑定到了这个列表对象上。要注意的是：以这种方式生成的列表对象并不能动态连接d指向的字典对象，它相当于将目前d绑定的字典对象的所有键对象的信息“截图并保存下来”，在此之后，列表的变化不会影响d引用的字典，d引用的字典的变化也不会影响该列表。
`d["c"] = 3` 是一个赋值语句，语句执行时，将修改d指向的字典对象本体。因为"c" != "a"且"c" != "b"，所以，最后的结果是：d指向的字典的键槽位新增一个字符串对象（"c"）的引用，并且值槽位新增一个值对象（3）的引用，字典保存这两个引用的映射关系。值得注意的是，字典的新增映射关系操作会改变字典的“键”视图对象、“值”视图对象和“条目”视图对象，但不会影响snapshot绑定的列表对象。
`d["a"] = 10` 是一个赋值语句，语句执行时，将修改d指向的字典对象本体。因为d绑定的字典对象的键槽位在新建时就已经保存了字符串对象（"a"）的引用，所以这里的赋值操作只会更新已有的键对象（"a"）的引用所映射的值对象（1）的引用成为指向新的值对象（10）的引用。也就是说，这里并没有发生d引用的字典对象的键槽位的新增引用操作，因此，这里的赋值操作会改变d绑定的字典的“值”视图对象和“条目”视图对象，但不会影响字典的“键”视图对象和snapshot绑定的列表对象。
综上所述，字典的“键”视图对象、“值”视图对象和“条目”视图对象都动态连接着字典本身，但它们分别侧重于反映字典的键槽位、值槽位和字典保存的映射关系的变化，比如说：本题的 `d["a"] = 10` 并不会改变d指向的字典的“键”视图对象，但却会改变另外两种视图对象。此外，由于字典对键的要求和集合对其元素的要求一致：唯一且可哈希，而字典对其值槽位保存的引用指向的值对象没有相关要求，所以，字典的“键”视图对象支持集合运算并返回集合作为结果对象，字典的“值”视图对象不支持集合运算，字典的“条目”视图对象只有在满足：字典的值槽位所保存的所有引用指向的值对象都是可哈希对象这样的条件时，才能支持集合运算。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### B3. 浅拷贝、嵌套可变对象与命名元组槽位（6 分）

预测输出，并说明哪些操作修改了共享的内部对象，哪些操作只是替换了外层映射中的值引用。

```python
from collections import namedtuple

Resource = namedtuple("Resource", "label mapping pairs")

mapping = {"menu.start": {"text": "Start", "tags": ["ui"]}}
pairs = [("menu.start", "Start")]
r = Resource("source", mapping, pairs)

copy_mapping = r.mapping.copy()
copy_mapping["menu.start"]["tags"].append("checked")
copy_mapping["menu.start"] = {"text": "Begin", "tags": []}
r.pairs.append(("menu.quit", "Quit"))

print(r.mapping)  # {'menu.start': {'text': 'Start', 'tags': ['ui', 'checked']}}
print(copy_mapping)  # {'menu.start': {'text': 'Begin', 'tags': []}}
print(r.pairs)  # [('menu.start', 'Start'), ('menu.quit', 'Quit')]
print(r.mapping is copy_mapping)  # False
print(r.mapping["menu.start"] is copy_mapping["menu.start"])  # False
```

答题区：

```text
`Resource = namedtuple("Resource", "label mapping pairs")` 是一个赋值语句，其中的 `namedtuple("Resource", "label mapping pairs")` 是创建新的名叫Resource的命名元组类对象的调用表达式，同时其中的 `"label mapping pairs"` 明确的表明了新建的Resource类和它的实例对象至少含有label、mapping和pairs这三个属性。最后，名字Resource被绑定到了这个命名元组类对象上。
`mapping = {"menu.start": {"text": "Start", "tags": ["ui"]}}` 是一个赋值语句，其中的 `{"menu.start": {"text": "Start", "tags": ["ui"]}}` 是创建并返回新的字典对象的字面量表达式，并且，名字mapping被绑定到了这个字典对象上。要注意的是：这个字典嵌套了值槽位保存了可变值对象（["ui"]）引用的其它字典。
`pairs = [("menu.start", "Start")]` 是一个赋值语句，其中的 `[("menu.start", "Start")]` 是创建并返回新的列表对象的字面量表达式，目前这个列表只保存了一个指向二元元组的引用，并且，名字pairs被绑定到了这个列表对象上。
`r = Resource("source", mapping, pairs)` 是一个赋值语句，其中的 `Resource("source", mapping, pairs)` 是创建Resource类的实例对象的调用表达式，要注意：实例化过程中传入的"source"、mapping指向的字典对象和pairs指向的列表对象这三个对象将被实例对象的三个属性label、mapping和pairs一一绑定。最后，名字r被绑定到了这个新建的实例对象上。
`copy_mapping = r.mapping.copy()` 是一个赋值语句，其中的 `r.mapping.copy()` 是（r指向的Resource实例对象的mapping属性值）字典对象的copy方法的调用表达式，与列表对象的copy方法类似，这里的表达式也是将这个字典对象做浅拷贝（“顶层”复制）操作，最后返回新的字典对象并被名字copy_mapping绑定。前面提到过，mapping指向的字典对象内部嵌套了值槽位保存了可变值对象（["ui"]）引用的其它字典，并且mapping绑定的字典对象也被r绑定的实例对象的mapping属性所共享，而现在的copy_mapping绑定的字典虽然其外层字典和mapping绑定的字典不是同一个对象，但是它们内部的映射关系乃至键值槽位保存的引用都是共享的，也就是说，mapping引用的字典内部的可变值对象（["ui"]）一旦被原地修改，共享此内部可变对象的其它两个字典（r.mapping和copy_mapping绑定的对象）都将同步变化。
`copy_mapping["menu.start"]["tags"].append("checked")` 是列表对象的append方法的调用表达式，它会原地修改列表对象，在列表尾部追加一个指向字符串对象（"checked"）的引用。由前面的阐述可知：`copy_mapping["menu.start"]["tags"]` 既等价于 `r.mapping["menu.start"]["tags"]`，也等价于 `mapping["menu.start"]["tags"]`，也就是说，这里被原地修改的列表正是前面刚提到的被三个字典共享的内部可变值对象["ui"]，所以mapping、r.mapping和copy_mapping指向的字典都将看到各自内部的可变值对象的变化。
`copy_mapping["menu.start"] = {"text": "Begin", "tags": []}` 是一个赋值语句，语句执行时，将修改copy_mapping指向的字典对象本体。我们已经知道：copy_mapping绑定的字典对象内部保存的映射关系和mapping、r.mapping绑定的字典是共享的，所以，copy_mapping绑定的字典对象的键槽位在新建时就已经保存了字符串对象（"menu.start"）的引用，这里的赋值操作只会更新已有的键对象（"menu.start"）的引用所映射的值对象（{"text": "Start", "tags": ["ui", "checked"]）的引用成为指向新的值对象（{"text": "Begin", "tags": []}）的引用。也就是说，这里并没有发生copy_mapping引用的字典对象的键槽位的新增引用操作或是修改了共享的内部值对象的操作，而是替换了外层映射中的值引用。又因为copy_mapping引用的字典对象是r.mapping指向的字典对象经过“顶层”复制得到的，所以，copy_mapping引用的字典对象的外层映射中的值引用替换操作既不会影响r.mapping指向的字典对象，也不会影响mapping指向的对象，毕竟，mapping和r.mapping指向同一个字典对象，但是，copy_mapping指向另一个字典对象。
`r.pairs.append(("menu.quit", "Quit"))` 是列表对象的append方法的调用表达式，它会原地修改列表对象，在列表尾部追加一个指向二元元组对象（("menu.quit", "Quit")）的引用。由前述可知：r.pairs和pairs指向同一个列表对象，所以，这里被原地修改的列表正是pairs绑定的对象[("menu.start", "Start")]，严格来说，这里也发生了共享的内部对象的修改操作，只是这个可变对象不在字典的内部而是在一个命名元组实例对象的内部。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

---

## C. 文件、文本、字节与编码边界（18 分）

### C1. 路径、文件对象、文本内容与关闭边界（5 分）

解释下面代码中 `path`、`f`、`text` 分别是什么层次。`with` 代码块结束后，文件对象状态发生了什么？

```python
from pathlib import Path

path = Path("projects/localization_resource_auditor/data/source_en.json")
with path.open("r", encoding="utf-8") as f:
    text = f.read()

print(type(path).__name__)  # WindowsPath
print(type(text).__name__)  # str
print(f.closed)  # True
```

答题区：

```text
`path = Path("projects/localization_resource_auditor/data/source_en.json")` 是一个赋值语句，其中的 `Path("projects/localization_resource_auditor/data/source_en.json")` 是创建Path类的实例对象的调用表达式，实例化过程中传入的实参是相对/绝对路径字符串对象，最后表达式会返回一个路径对象，并且名字path被绑定到了这个新建的实例对象上。
而从后续代码片段不难看出：`path.open("r", encoding="utf-8")` 是（path绑定的）路径对象的open方法的调用表达式，它基于路径对象应用“读取”模式和UTF-8编码规范创建并返回一个文件对象（本质是Python世界与外部文件资源（在这里，正是路径字符串表达的路径语义所指向的JSON文件）的数据交换通道），在这里这个表达式等价于 `open("projects/localization_resource_auditor/data/source_en.json", "r", encoding="utf-8")`，又因为表达式被裹挟在with语句提供的上下文管理器中，所以名字f被绑定在了返回的文件对象上，最后，`text = f.read()` 也是一个赋值语句，其中的 `f.read()` 是（f绑定的）文件对象的read方法的调用表达式，它会试图把这里的相对路径字符串表达的路径语义所指向的JSON文件打开，并按UTF-8编码规范将文件内部的所有字节解码成字符串，最后把整个字符串对象返回，在这里，text绑定了返回的字符串对象。另请注意：这里对外部文件的“读取”操作已经触发了文件边界，外部世界的文本文件内部保存的字节会被解码成Python世界里待操作的Python str对象。
综上，给定代码中的 `path`、`f`、`text` 分别是路径对象层、文件对象层、文本内容（str对象）层。此外，`with` 代码块结束后，文件对象受上下文管理器的实现逻辑影响，会自动且隐式的调用自身的close方法，终止与外部文件的连接，意即通俗意义上的“关闭”文件。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### C2. `str`、`bytes`、`len()` 与 UTF-8（5 分）

预测输出，并解释为什么“Python 语言层按字符操作”和“外部世界最终由字节承载”并不矛盾。

```python
text = "启动"
raw = text.encode("utf-8")
again = raw.decode("utf-8")

print(len(text))  # 2
print(len(raw))  # 6
print(type(text).__name__)  # str
print(type(raw).__name__)  # bytes
print(again == text)  # True
```

答题区：

```text
`text = "启动"` 是一个赋值语句，其中的 `"启动"` 是创建并返回新的字符串对象的字面量表达式，并且，名字text被绑定到了这个长度为2的字符串对象上。"启"和"动"这两个非ASCII字符在Unicode字符集中各由一个码位组成，且属于常见中文字符，因此，在UTF-8编码规则下编码它们将各自占用3个UTF-8字节。
`raw = text.encode("utf-8")` 是一个赋值语句，其中的 `text.encode("utf-8")` 是（text绑定的）字符串对象的encode方法的调用表达式，它会试图将一个字符串按照默认或给定的编码规则（在这里，是给定的UTF-8编码规则）来编码成字节字符串对象，最后将字节字符串对象返回。在这里，名字raw被绑定到了这个字节字符串对象上。由前述可知：text引用的字符串对象经UTF-8编码后的结果共占6个UTF-8字节。
`again = raw.decode("utf-8")` 是一个赋值语句，其中的 `raw.decode("utf-8")` 是（raw绑定的）字节字符串对象的decode方法的调用表达式，它会试图将一个字节字符串对象按照默认或给定的编码规则（在这里，是给定的UTF-8编码规则）来解码成字符串对象，最后将字符串对象返回。在这里，名字again被绑定到了这个字符串对象上。很明显，这是对应于编码操作的逆向解码操作，而且最近的二次操作都应用相同的UTF-8编码规则，所以不难得出结论：again绑定的字符串对象和text绑定的字符串对象“值相等”但是“身份不同”。
此外，从物理层面看，外部世界的资源最底层确实是字节形态，不过这并不意味着：Python语言层的操作一定是字节级别的！Python操作的对象的类型和对象的方法语义决定了Python语言层是否按字节操作。比如本题的 `len(text)` 和 `len(raw)` 分别按字符数和字节数操作，因为text指向字符串而raw指向字节串，它们不是同一类型的对象，响应同一个内置函数时操作逻辑的不同导致结果也各不相同：len(text)的结果不是6而是2；len(raw)的结果不是2而是6，总之，“外部世界最终由字节承载”这是客观事实，而“Python 语言层按字符操作”是因为Python语言层的操作受制于对象类型提供的协议和方法语义，二者并不矛盾，后者没有否定前者，前者也不会制约后者。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### C3. `open()` 默认编码与工程风险（4 分）

解释为什么下面代码在某些 Windows 环境中不一定立刻报错，但工程上仍然不推荐省略 `encoding`。

```python
import json

data = {"text": "启动"}
rendered = json.dumps(data, ensure_ascii=False)

with open("report.json", "w") as f:
    f.write(rendered)
```

答题区：

```text
`data = {"text": "启动"}` 是一个赋值语句，其中的 `{"text": "启动"}` 是创建并返回新的字典对象的字面量表达式，并且，名字data被绑定到了这个字典对象上。目前这个字典的键槽位保存了一个字符串对象（"text"）的引用，并且它映射至值对象（"启动"）的引用。
`rendered = json.dumps(data, ensure_ascii=False)` 是一个赋值语句，其中的 `json.dumps(data, ensure_ascii=False)` 是通过外部导入得到的工具函数dumps的调用表达式，它会试图对data引用的字典对象进行JSON序列化操作并返回JSON str对象，在这里，因为data引用的字典对象本体支持直接JSON序列化操作，且字典的键槽位和值槽位所保存的所有引用也都指向支持直接JSON序列化操作的对象（字符串对象），所以这里的JSON序列化操作不会报错，返回的JSON str对象被rendered绑定。
而从后续代码片段中不难看出：`open("report.json", "w")` 是Python内置函数open的调用表达式，它基于路径字符串表达的路径语义所指向的JSON文件，应用“写入”模式和默认的编码规范创建并返回一个文件对象，又因为表达式被裹挟在with语句提供的上下文管理器中，所以名字f被绑定在了返回的文件对象上，最后，`f.write(rendered)` 是一个（f绑定的）文件对象的write方法的调用表达式，它会试图把这里的相对路径字符串表达的路径语义所指向的JSON文件打开，按默认的编码规范将rendered绑定的字符串对象编码成字节序列并尽数写入JSON文件，最后把写入的总字符数返回。另请注意：这里对外部文件的“写入”操作已经触发了文件边界，Python世界的str对象会被编码成字节序列再写入外部世界的文本文件内。
通常来说，实际的工程中并不推荐：在调用open函数时省略命名参数encoding的传参！因为在这种情况下，涉及文件边界的逻辑会应用默认的编码规则来进行相关的编解码操作，而不同的运行环境下，这个默认编码规则也可能不同，这就容易导致：解码使用的规范和编码用的不一致，往往结果不符预期（出现乱码或报错UnicodeDecodeError）！成熟的高质量项目会明确的表达编码规则，而不是依赖随环境变化而变化的“变量”。当前环境下运行上面的代码片段确实不会立刻报错，这是因为当前环境下的默认编码规则是cp936，它可以成功的编码这里的rendered指向的str对象，但是如若后续追加“显式的使用UTF-8编码规则读取这个JSON文件”的逻辑，解码时就很可能出现报错UnicodeDecodeError！
```

### C4. `write()` / `write_text()` 返回值与内容边界（4 分）

预测 `result` 大致表示什么，并说明磁盘文件里保存的是 Python `dict` 对象、JSON 文本，还是编码后的字节。

```python
from pathlib import Path
import json

data = {"message": "开始", "count": 2}
rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
result = Path("report.json").write_text(rendered, encoding="utf-8")

print(type(data).__name__)  # dict
print(type(rendered).__name__)  # str
print(type(result).__name__)  # int
```

答题区：

```text
`data = {"message": "开始", "count": 2}` 是一个赋值语句，其中的 `{"message": "开始", "count": 2}` 是创建并返回新的字典对象的字面量表达式，并且，名字data被绑定到了这个字典对象上。目前这个字典的键槽位保存了二个字符串对象（"message"和"count"）的引用，并且它们分别映射至二个值对象（"开始"和2）的引用。要注意的是：data指向的字典对象本身支持直接JSON序列化操作，且字典的键槽位和值槽位所保存的所有引用也都指向支持直接JSON序列化操作的对象。
`rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"` 是一个赋值语句，其中的 `json.dumps(data, ensure_ascii=False, indent=2) + "\n"` 是两个字符串对象的拼接操作，关键在于“加号”左侧的表达式：它是通过外部导入得到的工具函数dumps的调用表达式，它会试图对data引用的字典对象进行JSON序列化操作并返回JSON str对象。由前述可知，这里的JSON序列化操作不会报错，返回的JSON str对象会先和换行符这个字符串对象进行拼接运算，最后把运算结果（字符串对象）交予名字rendered绑定。
`result = Path("report.json").write_text(rendered, encoding="utf-8")` 是一个赋值语句，其中的 `Path("report.json").write_text(rendered, encoding="utf-8")` 是路径对象的write_text方法的调用表达式，它首先会试图打开Path实例化时传入的路径字符串（"report.json"）表达的路径语义所指向的JSON文件，接着按UTF-8编码规则将rendered绑定的字符串对象编码成字节序列并尽数写入这个JSON文件，最后把写入的总字符数返回。在这里，result绑定了返回的整数对象（字符数），同时这个表达式等价于 `Path("report.json").open("w", encoding="utf-8").write(rendered)`。另请注意：这里对外部文件的“写入”操作已经触发了文件边界，Python世界的str对象会被编码成字节序列再写入外部世界的文本文件内。
此外，本题给出的代码片段展现了一个Python对象从Python世界到外部世界的最简过程：data绑定的是一个Python字典对象，想要将它表达的信息写入外部世界的JSON文件中，就需要事先将Python dict对象序列化成JSON数据模型所支持的对象，而在这里，JSON序列化的结果是JSON str对象，注意此时仍在Python世界中，但通过基于外部文件创建文件对象的方式，就可以把尚在Python世界中的str按规定的编码规范编码成字节并写入外部世界的JSON文件中。事实上，不止是JSON文件，所有的磁盘文件内保存的都是编码后的字节。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

---

## D. JSON、CSV 与序列化边界（18 分）

### D1. JSON 文本、Python 对象与 `ensure_ascii`（5 分）

预测输出，并说明 `ensure_ascii` 改变的是返回对象类型、字符串内容，还是底层文件字节。

```python
import json

text = "启动"
a = json.dumps({"text": text}, ensure_ascii=True)
b = json.dumps({"text": text}, ensure_ascii=False)

print(type(a).__name__, type(b).__name__)  # str str
print(a)  # {"text": "\u542f\u52a8"}
print(b)  # {"text": "启动"}
print(json.loads(a) == json.loads(b))  # True
```

答题区：

```text
`text = "启动"` 是一个赋值语句，其中的 `"启动"` 是创建并返回新的字符串对象的字面量表达式，并且，名字text被绑定到了这个字符串对象上。
`a = json.dumps({"text": text}, ensure_ascii=True)` 是一个赋值语句，其中的 `json.dumps({"text": text}, ensure_ascii=True)` 是通过外部导入得到的工具函数dumps的调用表达式，其中的 `{"text": text}` 是创建并返回临时的字典对象的字面量表达式，同时要注意到这个临时的字典对象本身支持直接JSON序列化操作，且字典的键槽位和值槽位所保存的所有引用也都指向支持直接JSON序列化操作的对象（字符串对象），再然后，函数dumps的调用会试图对这个临时字典对象进行JSON序列化操作并返回JSON str对象，最后，名字a绑定了这个被返回的字符串对象。这里要注意的是：函数dumps在调用时给命名参数ensure_ascii传入了实参True，这意味着：待序列化的对象内容中含有的非ASCII字符会被自动转换成适配JSON的Unicode转义形式，比如这里的临时字典对象的值槽位保存的引用指向的正是以2个非ASCII字符（启动）作为内容的字符串对象，所以，a引用的字符串对象的内容会是 {"text": "\u542f\u52a8"}
`b = json.dumps({"text": text}, ensure_ascii=False)` 是一个赋值语句，其中的 `json.dumps({"text": text}, ensure_ascii=False)` 是通过外部导入得到的工具函数dumps的调用表达式，其中的 `{"text": text}` 是创建并返回临时的字典对象的字面量表达式，同时要注意到这个临时的字典对象本身支持直接JSON序列化操作，且字典的键槽位和值槽位所保存的所有引用也都指向支持直接JSON序列化操作的对象（字符串对象），再然后，函数dumps的调用会试图对这个临时字典对象进行JSON序列化操作并返回JSON str对象，最后，名字b绑定了这个被返回的字符串对象。这里要注意的是：函数dumps在调用时给命名参数ensure_ascii传入了实参False，这意味着：待序列化的对象内容中含有的非ASCII字符会被保留，比如这里的临时字典对象的值槽位保存的引用指向的正是以2个非ASCII字符（启动）作为内容的字符串对象，所以，b引用的字符串对象的内容会是 {"text": "启动"}
综上可知：a和b指向的字符串内容不相同，所以， `ensure_ascii` 改变的正是json.dumps返回的字符串的内容！不过，尽管a和b指向的字符串内容不相同，但这两个字符串在JSON中表达的语义是一样的，也正因如此，json.loads(a)和json.loads(b)的返回结果都是 {"text": "启动"}，JSON反序列化操作中对形如"\u542f\u52a8"这样的JSON str采取的解释转义操作类似于Python解释器对形如"\xc4"这样的Python转义序列所做的解释操作。

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### D2. JSON 不支持的对象与递归序列化（5 分）

预测哪一行会报错，并说明报错发生在外层对象、内层对象，还是 JSON 数据模型不支持的对象。

```python
import json

payload = {
    "mapping": {"a": "A"},
    "record": ("a", "A"),
    "keys": {"a", "b"},
}

print(json.dumps({"record": payload["record"]}, ensure_ascii=False))  # {"record": ["a", "A"]}
print(json.dumps(payload, ensure_ascii=False))  # 报错TypeError
```

答题区：

```text
`payload = {"mapping": {"a": "A"}, "record": ("a", "A"), "keys": {"a", "b"},}` 是一个赋值语句，其中的 `{"mapping": {"a": "A"}, "record": ("a", "A"), "keys": {"a", "b"},}` 是创建并返回新的字典对象的字面量表达式，并且，名字payload被绑定到了这个字典对象上。目前这个字典的键槽位保存了三个字符串对象（"mapping"、"record"和"keys"）的引用，并且它们分别映射至三个值对象（{"a": "A"}、("a", "A")和{"a", "b"}）的引用。要注意的是：payload指向的字典对象的值槽位保存了一个指向不支持直接JSON序列化操作的对象（{"a", "b"}）的引用。
`print(json.dumps({"record": payload["record"]}, ensure_ascii=False))` 是内置函数print的调用表达式，其中的 `json.dumps({"record": payload["record"]}, ensure_ascii=False)` 是通过外部导入得到的工具函数dumps的调用表达式，其中的 `{"record": payload["record"]}` 是创建并返回临时的字典对象的字面量表达式，同时要注意到这个临时的字典对象本身及其键槽位保存的引用指向的键对象（"record"）都支持直接JSON序列化操作，且字典的值槽位所保存的引用指向的值对象被payload["record"]所共享，至于 `payload["record"]` 这个表达式返回的对象正是payload绑定的字典对象的名为"record"的键所映射的值对象：("a", "A")，也就是说，在当前上下文中，临时创建的字典对象等价于表达式 `{"record": ("a", "A")}` 返回的字典对象，而元组对象本体也是支持直接JSON序列化操作的对象，因为在JSON序列化时Python的元组会被视为JSON数组，就像列表在被JSON序列化时类似，不过，由于JSON中实际上没有tuple这样的对象模型，所以在反序列化操作后返回的不再是最初的元组对象，而是新的列表对象，另外，这里的元组("a", "A")内部保存的引用也都指向字符串对象，这意味着这个元组确实支持直接JSON序列化操作，总而言之，这个新建的临时字典对象支持直接JSON序列化的操作。再然后，函数dumps的调用会试图对这个临时字典对象进行JSON序列化操作并返回JSON str对象，最后，返回的str会被打印输出至终端。
`print(json.dumps(payload, ensure_ascii=False))` 是内置函数print的调用表达式，其中的 `json.dumps(payload, ensure_ascii=False)` 是通过外部导入得到的工具函数dumps的调用表达式，其中的payload绑定的字典对象的值槽位保存了一个指向集合对象（{"a", "b"}）的引用，然而JSON的对象模型中并没有set这样的对象类型，因此Python的set不支持直接JSON序列化的操作，所以当函数dumps的调用试图对payload引用的字典对象进行JSON序列化操作时，会直接报错TypeError。
综上，Python执行至这一行：`print(json.dumps(payload, ensure_ascii=False))` 的时候会报错TypeError，而如前所述，报错实际上发生在payload绑定的字典对象的内层值对象payload["keys"]上，因为它是集合对象，它是 JSON 数据模型不支持的对象

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### D3. `namedtuple._asdict()`、`Counter` 与 JSON report（4 分）

以下代码在 Python 3.9 中能否成功序列化？请预测 `report["issue"]` 的类型，并说明理由。

```python
from collections import Counter, namedtuple
import json

Issue = namedtuple("Issue", "code detail")

pairs = [("a", "A"), ("a", "B"), ("b", "C")]
counts = Counter(key for key, _ in pairs)
issue = Issue("duplicate", {"values": [value for key, value in pairs if key == "a"]})

report = {
    "duplicates": dict(counts),
    "issue": issue._asdict(),
}

text = json.dumps(report, ensure_ascii=False)

print(type(report["issue"]).__name__)  # dict
print(type(text).__name__)  # str
```

答题区：

```text
`Issue = namedtuple("Issue", "code detail")` 是一个赋值语句，其中的 `namedtuple("Issue", "code detail")` 是创建新的名叫Issue的命名元组类对象的调用表达式，同时其中的 `"code detail"` 明确的表明了新建的Issue类和它的实例对象至少含有code和detail这二个属性。最后，名字Issue被绑定到了这个命名元组类对象上。
`pairs = [("a", "A"), ("a", "B"), ("b", "C")]` 是一个赋值语句，其中的 `[("a", "A"), ("a", "B"), ("b", "C")]` 是创建并返回新的列表对象的字面量表达式，目前这个列表保存了三个指向二元元组的引用，并且，名字pairs被绑定到了这个列表对象上。
`counts = Counter(key for key, _ in pairs)` 是一个赋值语句，其中的 `Counter(key for key, _ in pairs)` 是创建Counter类的实例对象的调用表达式，并且名字counts被绑定到了这个新建的实例对象上。实例化过程中传入的实参是一个创建生成器对象的表达式：它返回的生成器对象在迭代场景下会从pairs指向的列表中逐个取出列表已保存的引用指向的二元元组，并在把每个元组保存的第一个引用赋值给临时变量名key后返回key，所以最终的效果是：Counter类收集到三个key（"a"，"a"，"b"）并统计每个key出现的次数，counts大致上等价于Counter({"a": 2, "b": 1})。又因为Counter实例对象是类字典对象，所以 `dict(counts)` 不会报错并返回新的字典对象{"a": 2, "b": 1}
`issue = Issue("duplicate", {"values": [value for key, value in pairs if key == "a"]})` 是一个赋值语句，其中的 `Issue("duplicate", {"values": [value for key, value in pairs if key == "a"]})` 是创建Issue类的实例对象的调用表达式，而名字issue被绑定到了这个新建的实例对象上。要注意：实例化过程中传入的"duplicate"和{"values": [value for key, value in pairs if key == "a"]}这二个对象将被实例对象的二个属性code和detail一一绑定，其中的 `{"values": [value for key, value in pairs if key == "a"]}` 是创建并返回新的字典对象的字面量表达式：它返回的字典的键槽位保存了一个字符串对象（"values"）的引用，与之映射的值槽位上的引用指向一个通过列表推导式新建的列表对象，这个列表推导式的大致意思是：从pairs指向的列表中逐个取出列表已保存的引用指向的二元元组，并在每个元组保存的第一个引用指向的对象与字符串对象"a"“值相等”的条件下，把该元组保存的第二个引用存入待返回的结果列表中。因此，不难判断：issue.detail的值是{"values": ["A", "B"]}。另外，命名元组实例对象继承了名叫_asdict的方法属性，`issue._asdict()` 便是（issue绑定的）命名元组实例对象的_asdict方法的调用表达式，它在当前运行环境下会返回一个新的字典对象：这个字典的键槽位保存的二个引用分别指向issue的两个属性的名字（"code"和"detail"），而这两个键引用映射的两个值引用则分别指向issue的两个属性的值（"duplicate"和{"values": ["A", "B"]}）
`report = {"duplicates": dict(counts), "issue": issue._asdict(),}` 是创建并返回新的字典对象的字面量表达式，并且，名字report被绑定到了这个字典对象上。由前述不难判断：目前这个字典的键槽位保存了二个字符串对象（"duplicates"和"issue"）的引用，并且它们分别映射至二个值对象（{"a": 2, "b": 1}和{"code": "duplicate", "detail": {"values": ["A", "B"]}}）的引用。要注意的是：report指向的字典对象本身支持直接JSON序列化操作，且字典的键槽位和值槽位所保存的所有引用也都指向支持直接JSON序列化操作的对象。
`text = json.dumps(report, ensure_ascii=False)` 是一个赋值语句，其中的 `json.dumps(report, ensure_ascii=False)` 是通过外部导入得到的工具函数dumps的调用表达式，注意到这个传入的report指向的字典对象本身支持直接JSON序列化操作，且字典的键槽位和值槽位所保存的所有引用也都指向支持直接JSON序列化操作的对象，再然后，函数dumps的调用会试图对这个字典对象进行JSON序列化操作并返回JSON str对象，最后，名字text绑定了这个被返回的字符串对象。也就是说，本题给定的代码片段在当前运行环境下最后可以成功序列化！

“验证前预测”：
已在问题区以注释的形式写出。
“验证后修正”：
预测正确，无须修正。
```

### D4. CSV 单元格、`DictReader` 与结构边界（4 分）

解释为什么 CSV 单元格适合保存扁平文本字段，却不适合直接保存 Python 的嵌套 `list` / `dict` 结构。`csv.DictReader` 读出的一行更接近什么对象？如果你需要保留嵌套结构，优先选择 CSV 还是 JSON？为什么？

答题区：

```text
这是因为CSV的本质是二维表文本：即一行代表一条记录，一列代表一个字段，一个单元格本质上也只是文本，CSV不像JSON，它没有嵌套数据模型，也就没法表达字段本来的语义，所以 CSV 单元格不适合直接保存 Python 的嵌套 `list` / `dict` 结构，即便强行将这类数据结构塞进 CSV 单元格内也会变成字符串这种文本形式，但它非常适合保存 key、source、translation、tags这类扁平文本字段。
而`csv.DictReader` 读出的一行更接近一个Python字典对象，即“字段名字符串-->单元格文本字符串”的映射，但要注意这里返回的Python dict对象的键槽位和值槽位保存的引用都指向了字符串对象，不论写入CSV时对象原来的类型！所以这又一次说明了 CSV 单元格并不适合直接保存具有层级结构的Python对象，CSV并不会自动保留这类对象的结构。
如果我确实需要保留嵌套结构，我会优先选择JSON！首先，如前所述，CSV也确实可以保存这类数据结构，但是从CSV文件中再把它们读出来后都变成了str，想要还原/恢复它们的初始对象类型需要额外的解析步骤，且对于越复杂的嵌套结构，解析起来越繁杂易错；其次，JSON的数据模型反而是天然对应常见的Python嵌套结构：如dict、list、tuple，也就是说，存入JSON文件的嵌套结构再读回来通常能够恢复多数的数据类型。
```

---

## E. 阶段综合项目代码阅读：Localization Resource Auditor（18 分）

### E1. `object_pairs_hook` 与重复 JSON key（5 分）

解释为什么项目中不直接把 JSON object 解析成普通 `dict`，而要先用 `json.loads(..., object_pairs_hook=JsonObjectPairs)` 保留 pair list。

请用下面这个样例说明“折叠前”和“折叠后”的区别：

```python
text = '{"menu.start": "开始游戏", "menu.start": "启动"}'
```

答题区：

```text
项目中不直接把 JSON object 解析成普通 dict，是因为普通 dict 对 key 的去重是自动且隐式的，也就意味着它并不能保留重复 key 的历史信息。对于本地化资源审计器来说，重复 key 本身就是重要问题；如果在 json.loads() 阶段直接变成普通 dict，后出现的同名 key 会覆盖先出现的同名 key，项目就无法知道这个 key 曾经重复出现过，也无法报告被覆盖前的值。
以 text = '{"menu.start": "开始游戏", "menu.start": "启动"}' 为例，如果直接执行 json.loads(text)，结果会变成 {'menu.start': '启动'}。这是折叠后的结果：两个相同 key 不能同时存在于普通 dict 中，第二个 "menu.start" 会更新同一个 key 对应的值引用，所以最后只保留 "启动"。这一步修改的是 dict 本体中的映射关系，而不是修改字符串对象本身。
而项目使用 json.loads(text, object_pairs_hook=JsonObjectPairs)，是为了在折叠成 dict 之前先得到 pair list。折叠前的数据更接近 [("menu.start", "开始游戏"), ("menu.start", "启动")]。这个结构保留了 JSON object 中键值对的出现顺序，也保留了重复 key，因此项目可以在此之后用 Counter(key for key, _ in pairs) 统计 key 出现次数，并能记录重复 key 的所有值。
随后项目才手动构造普通 dict：mapping = {}; for key, value in pairs: mapping[key] = value。这一步会发生 dict 的正常键覆盖，最终得到 {"menu.start": "启动"}。因此，pair list 用于审计重复 key，mapping 用于后续快速按 key 查找和比较 source/target。两者分别服务于不同目的。
这个设计清楚地区分了 JSON 文本边界和 Python 对象边界：text 起初只是 JSON 文本字符串；经过 json.loads(..., object_pairs_hook=JsonObjectPairs) 后才变成 Python 的 pair list；再经过手动赋值才折叠成普通 dict。项目保留这两个阶段，是为了让“折叠前的原始键值对序列”和“折叠后的 dict 映射结果”都可观察，从而既能发现资源文件中的重复 key，又能继续利用 dict 做高效的本地化资源比较。
```

### E2. `Resource` 记录的多层对象模型（4 分）

项目中的 `Resource` 包含：

```python
Resource = namedtuple("Resource", "label path text pairs mapping duplicate_counts")
```

逐项解释这 6 个字段分别保存什么对象或信息。重点说明为什么同一个资源文件要同时保留 `text`、`pairs` 和 `mapping`。

答题区：

```text
Resource = namedtuple("Resource", "label path text pairs mapping duplicate_counts") 定义了一个稳定的资源记录结构，用来保存：一个 JSON 本地化资源文件从路径到文本、从 JSON 文本到 Python 对象、再从键值对序列到普通字典映射的多个阶段状态。
label 保存资源角色标签，通常是 "source" 或 "target"，用于区分当前资源是源语言文件还是目标语言文件。生成重复 key 问题时，项目会根据这个标签构造类似 duplicate_source_key 或 duplicate_target_key 的问题记录。
path 保存 Path 对象，表示资源文件在磁盘上的位置。它不是文件对象，也不是文件内容，只是路径对象。真正打开文件是在包括函数 read_text_file() 在内的相关逻辑中完成的。
text 保存从文件中读取出的原始 JSON 文本，是 Python str 对象。它来自 open(..., encoding="utf-8-sig") 和 file.read()，所以它已经经过文本模式解码，但仍然只是 JSON 文本，不是 Python dict。保留 text 是为了让项目能观察“文件字节经过编码解码进入 Python 后”的文本边界。
pairs 保存 JSON object 折叠成普通 dict 之前的键值对序列。项目使用 json.loads(text, object_pairs_hook=JsonObjectPairs)，让 JSON object 先变成 pair list，而不是直接变成普通 dict。随后项目校验每个 key 和 value 是否都是字符串，并把它们加入 pairs。因此 pairs 通常是一个 list，内部元素是二元 tuple，例如 [("menu.start", "开始游戏"), ("menu.start", "启动")]。它的最大价值是保留原始顺序和重复 key。
mapping 保存折叠后的普通 Python dict。项目通过 mapping = {}; for key, value in pairs: mapping[key] = value 构造它。如果同一个 key 出现多次，后面的值会覆盖前面的值。例如 [("menu.start", "开始游戏"), ("menu.start", "启动")] 折叠后会变成 {"menu.start": "启动"}。这一步修改的是 dict 容器本体中的映射关系，而不是修改字符串对象本身。mapping 的意义是提供高效的 key 查找，方便后续比较 source 和 target 的 key 集合，并执行占位符、换行、长度、术语等检查。
duplicate_counts 保存 key 出现次数统计，类型是 Counter。它通过 Counter(key for key, _ in pairs) 得到。由于它基于折叠前的 pairs 统计，所以能够发现普通 dict 已经看不到的重复 key。例如某个 key 在 pairs 中出现两次，duplicate_counts[key] 就是 2，项目便可以生成重复 key 问题，并报告所有重复值以及 dict 最终保留的值。
同一个资源文件需要同时保留 text、pairs 和 mapping，是因为它们服务于不同层次。text 表示原始 JSON 文件文本，适合观察文件内容和 JSON 解析前的边界；pairs 表示 JSON object 折叠前的键值对序列，适合发现重复 key 和保留原始顺序；mapping 表示折叠后的普通 dict，适合高效查找和后续审计比较。如果只保留 mapping，重复 key 的历史信息会消失；如果只保留 pairs，后续按 key 查找和比较会不方便；如果只保留 text，则无法直接做结构化审计。因此三者需要同时存在！
```

### E3. `audit_resources()` 的集合与列表协作（4 分）

解释项目中为什么用：

```python
source_keys = set(source.mapping)
target_keys = set(target.mapping)
```

再分别计算：

```python
source_keys - target_keys
target_keys - source_keys
source_keys & target_keys
```

为什么后续常常要再套 `sorted(...)`？

答题区：

```text
项目中使用 source_keys = set(source.mapping) 和 target_keys = set(target.mapping)，是因为 source.mapping 和 target.mapping 都是普通 dict，而直接迭代 dict 时默认得到的是 key。因此 set(source.mapping) 等价于把资源映射中的所有 key 提取出来，创建一个新的 set 对象。这里不会修改原来的 source.mapping 或 target.mapping，只是从它们那儿读取 key，并创建新的集合。
把 key 转成 set 后，项目就可以非常自然地表达源文件和目标文件之间的 key 关系。source_keys - target_keys 表示源文件中有、目标文件中没有的 key，也就是目标文件缺失的翻译 key，项目会据此生成 missing_target_key 问题记录。target_keys - source_keys 表示目标文件中有、源文件中没有的 key，也就是额外的目标 key，项目会据此生成 extra_target_key 警告记录。source_keys & target_keys 表示两个文件共有的 key，只有这些共有 key 才能继续取出 source.mapping[key] 和 target.mapping[key]，进行空翻译、长度、换行、占位符和术语表检查。
综上，这里用 set 转型体现了 set 的工程用途：它适合表达去重后的成员集合，并且非常适合做差集、交集这类关系判断，这里用 set 不是单纯为了“换一种容器”，而是因为问题本身就是集合关系问题。
至于说后续常常套 sorted(...)，是因为 set 的另一个特点是无序，它本身不承担稳定输出顺序的职责。集合适合成员测试和集合运算，但它的迭代顺序不应作为报告顺序依赖。项目生成审计报告时，需要输出稳定、可读、可复现。如果直接遍历 set 运算结果，报告中 key 的顺序可能不适合阅读，也会让测试结果变得不稳定。因此项目用 sorted(source_keys - target_keys)、sorted(target_keys - source_keys)、sorted(source_keys & target_keys)，把集合结果转成排序后的 list，再按稳定顺序生成问题记录。
```

### E4. `--observe` 对象观察窗（5 分）

说明 `--observe` 额外展示的信息如何对应你当前阶段的核心痛点。至少覆盖：

- 字典视图 vs 列表快照；
- JSON 重复 key 折叠边界；
- 浅拷贝共享内部可变对象；
- `str` 长度 vs UTF-8 字节长度；
- JSON 文本 vs Python 对象。

答题区：

```text
项目中的 --observe 是一个对象模型观察模式。它不会改变资源审计的核心逻辑，也不会改变 source、target、glossary 的加载和检查方式；它只是让 report_data() 在正常的 summary 和 issues 之外，额外加入 "observations" 字段。这个字段由 object_observations() 生成，专门展示字典视图、列表快照、重复 key 折叠、浅拷贝、文本与字节、JSON 文本与 Python 对象这些边界。
首先，--observe 展示了字典视图和列表快照的区别。项目中创建了 key_view = source.mapping.keys() 和 key_snapshot = list(source.mapping.keys())。前者是 dict_keys 视图对象，会和原字典保持动态关联；后者是新建的 list，是当时 key 集合的快照。项目还创建了 view_demo = dict(source.mapping)，再取 view = view_demo.keys()，随后向 view_demo 新增 "__observer.demo__" 这个 key。新增 key 修改的是 view_demo 这个 dict 容器本体，因此后续从 view 转成 list 时会看到变化；但修改前保存的 before_view 或 key_snapshot 不会变化，因为它们是 list 快照。
其次，--observe 展示了 JSON 重复 key 的折叠边界。项目读取 JSON 时没有直接把 JSON object 解析成普通 dict，而是先通过 object_pairs_hook=JsonObjectPairs 保留 pair list。这样，重复 key 在折叠前仍然可见。普通 dict 不能同时保存两个相等 key，所以在 mapping[key] = value 的循环中，后出现的同名 key 会更新已有映射，最终通常保留最后一个值。duplicate_boundary() 会展示某个重复 key 在 pair list 中出现了几次、折叠前有哪些 value、折叠成 dict 后最终保留了哪个 value。
第三，--observe 展示了浅拷贝共享内部可变对象的问题。项目构造了 shallow_original = {"tags": ["ui", "menu"]}，然后执行 shallow_copy = shallow_original.copy()。这会创建一个新的外层 dict，但内部的 "tags" 仍然指向同一个 list。之后执行 shallow_copy["tags"].append("reviewed") 时，真正被修改的是内部 list 对象，而不是外层 dict 的映射关系。因此 shallow_original 和 shallow_copy 都能看到 tags 列表中新增的 "reviewed"。这说明浅拷贝只能隔离外层容器，不能自动隔离嵌套可变对象。
第四，--observe 展示了 str 长度和 UTF-8 字节长度的区别。项目从目标映射中取出 menu.start 的文本，得到的是 Python str，然后执行 .encode("utf-8") 得到 bytes。len(sample_text) 统计的是 Unicode 字符数量，而 len(sample_bytes) 统计的是编码后的字节数量。对于中文文本，二者通常不同，因为一个中文字符在 UTF-8 中通常占多个字节。
第五，--observe 强调了 JSON 文本和 Python 对象的区别。项目输入阶段先用 open(..., encoding="utf-8-sig") 把文件字节解码成 Python str，此时得到的是 JSON 文本；再用 json.loads() 把 JSON 文本解析成 Python 对象，包括 pair list、dict、Counter 和 Resource。输出阶段则相反：项目先构造 Python 的报告数据 dict，再用 json.dumps() 生成 JSON 文本字符串；如果指定输出路径，才会把这个字符串按 UTF-8 写入文件。因此 JSON 文件内容、Python 字符串、Python dict/list、JSON 报告文本、最终文件字节是不同层次。
综上，--observe 对应的不是业务功能扩展，而是学习功能扩展。它把当前阶段最重要的对象边界可视化：视图不是快照，重复 key 在 dict 中会折叠，浅拷贝会共享内部可变对象，str 和 bytes 属于不同层次，JSON 文本和 Python 对象也不是同一物。
```

---

## F. 核心对象类型横向收束与设计题（10 分）

### F1. 核心类型选型表（5 分）

为“游戏本地化资源审计工具”选择合适对象类型，并解释理由。

| 需求 | 你的选择 | 理由 |
| --- | --- | --- |
| 保存资源 key 到文本的映射 | dict | Python内置核心数据类型中唯一属于映射类型的正是dict，此外，需求本质是“键值间的映射关系”，且资源 key 和文本通常都是str，所以为了满足该需求以及将来可能的JSON序列化需求，dict是很合适的 |
| 保存待排序、待过滤的问题记录集合 | list | 需求已经很明确的要求选择的容器类型支持排序、过滤的操作，此外，问题记录通常也需要“增删改查”，所以为了满足上述需求，list会是合适的 |
| 表示单条稳定 issue 记录 | namedtuple | 需求强调了“单条稳定的记录”，而namedtuple既有元组的轻量和不可替换记录中字段的特性，又能通过字段名提升可读性，所以namedtuple是合适的 |
| 检查缺失 key、额外 key、共同 key | set | 需求点明了一种集合关系问题，且资源 key 通常是str，因此，选择set可以通过它所支持的集合运算（差集、交集）来满足需求 |
| 统计重复 key 或问题类型次数 | Counter | Counter专门用于计数，很适合用在工具中：统计每个 key 出现的次数、统计每种问题类型出现的次数等等 |
| 输出机器可读结构化报告 | str | 通常来说，结构化报告的“前身”是dict，但是需求强调了“机器可读”，所以这类报告需要经历类似JSON序列化这样的“加工”操作生成，也就代表了报告最后的类型是str |

### F2. 迷你设计题：一次完整数据流（5 分）

设计一个最小但完整的数据流，用文字或伪代码说明：

```text
读取 source.json / target.json
    -> 检查缺失 key、额外 key、重复 key、占位符差异
    -> 生成人读文本报告和机器读 JSON 报告
```

要求至少说清楚：

1. 哪一步是文件边界；
2. 哪一步是 JSON 文本到 Python 对象；
3. 哪一步使用 `dict`、`set`、`list`、`Counter`；
4. 哪一步必须把内部对象转换成 JSON 可序列化结构；
5. 哪一步把 Python `str` 编码成外部文件字节。

答题区：

```text
第一步是文件边界。程序接收路径字符串或 Path 对象，通过 open(..., encoding="utf-8-sig") 或 Path.read_text(encoding="utf-8-sig") 读取文件 source.json / target.json。此时外部文件字节被解码成 Python 内存中的 str。这个 str 只是 JSON 文本，还不是 Python 字典。
第二步是 JSON 文本到 Python 对象的边界。程序调用 json.loads(source_text) 和 json.loads(target_text)，把 JSON 文本解析成 Python 对象。若 JSON 顶层是 object，则通常得到 Python dict。此时才有了资源 key 到文本的映射，例如 {"menu.start": "Start Game"}。
第三步使用Python内置的核心对象类型完成审计。dict 用来保存资源 key 到文本的映射；set 用来提取 key 集合，并通过 source_keys - target_keys 找缺失 key，通过 target_keys - source_keys 找额外 key，通过 source_keys & target_keys 找共同 key；list 用来保存逐条产生的问题记录，因为问题需要追加、排序和输出；Counter 用来统计问题类型次数、严重程度次数，或者在保留 pair list 的情况下统计重复 key 次数。
第四步是 JSON 可序列化边界。程序内部对象不一定都能直接输出成 JSON。例如 Counter、set、Path、namedtuple 都应先转换成 JSON 默认支持的结构。Counter 转成普通 dict，set 转成排序后的 list，Path 转成 str，namedtuple 转成普通 dict。最终报告对象应只包含 dict、list、str、int、float、bool、None 等 JSON 可序列化对象。
第五步是输出边界。若输出给人阅读，可以把报告对象渲染成普通文本 str 并 print()。若输出给机器读取，则调用 json.dumps(report, ensure_ascii=False, indent=2) 把 Python 报告对象转换成 JSON 文本字符串。如果需要写入文件，再通过 Path("report.json").write_text(json_text, encoding="utf-8") 把 Python str 编码成外部文件字节。
```

---

## 作答后提交说明

作答时请直接在每题的“答题区”中填写。你提交后，我会按阶段测验批改规则追加：

- `## Codex 批改记录（逐题审批，YYYY-MM-DD）`
- 建议得分；
- 主要强项；
- 主要修正点；
- 是否通过“字典和文件：映射、持久化边界与核心类型收束”小阶段；
- 是否通过 Types and Operations 大阶段收束验收；
- `学习画像更新`，用于同步到 `notes/Python_Learning_Profile.md` 和下一阶段启动模板。

---

## Codex 批改记录（逐题审批，2026-05-29）

### 总评与建议得分

建议得分：**96 / 100**

阶段判断：

- **通过**“字典和文件：映射、持久化边界与核心类型收束”小阶段。
- **通过** Types and Operations 大阶段收束验收。

整体判断：本次答卷已经达到阶段末优秀水平。你不仅能预测多数代码输出，而且能按“源码形式 -> 对象创建 -> 名字绑定 -> 容器修改 -> 序列化/文件边界”的链路解释原因。尤其是哈希与相等性、字典键覆盖、视图对象、浅拷贝、文件/文本/字节/JSON 分层、`object_pairs_hook` 和阶段项目整体数据流，都已经形成较稳定的对象模型。

主要扣分不来自主干错误，而来自少数工程边界的表述精度：`frozenset` 的可哈希条件、浅拷贝中“映射关系共享”的措辞、JSON 不能完整恢复所有 Python 嵌套类型、机器可读报告的“内部结构层”和“JSON 文本层”需要同时表达，以及设计重复 key 审计时应明确使用 `object_pairs_hook` 或 pair list。

---

### A. 字典、哈希与映射对象边界（17.5 / 18）

#### A1（6 / 6）

预测正确。你准确说明了 `1.0`、`True`、`1` 满足相等且哈希相等，因此字典保留首次插入的键对象 `1.0`，后续只更新该逻辑键对应的值引用。

需要保留的纠偏意识：`next(iter(d.keys())) is 1.0` 这类身份比较只是在当前运行环境里因为常量复用而表现为 `True`，它不是字典键去重的语义依据。字典去重依据是 `hash()` 与 `==`。

#### A2（6 / 6）

预测正确。你对自定义键的 `__eq__` / `__hash__` 合同解释到位，尤其是指出 `a == b` 必须推出 `hash(a) == hash(b)`，否则会破坏字典和集合的查找、去重、删除语义。

这里的解释已经达到工程可用水平。

#### A3（5.5 / 6）

主体正确。字符串、全由可哈希元素构成的元组、示例中的 `frozenset` 可以作为键；含列表的元组、普通 `set` 不可以作为键。

小扣分点：你写到“冻结集合实例对象也是可哈希的”时，表述略宽。更精确地说：`frozenset` 是否可哈希，也取决于其所有元素是否可哈希。本题中元素都是字符串，所以它可哈希。

---

### B. 字典方法、视图、拷贝与迭代风险（17.5 / 18）

#### B1（6 / 6）

预测正确。`get()` 不修改字典；`setdefault()` 在缺 key 时写入默认对象并返回它；`update()` 修改字典并返回 `None`；`pop()` 删除键并返回旧值。你也正确指出了 `b.append(...)` 修改的是被字典保存的同一个列表对象。

#### B2（6 / 6）

预测正确。你准确区分了 `dict_keys` / `dict_items` 视图对象和 `list(keys)` 快照，并说明了 `keys` 支持集合运算、`values` 通常不支持集合运算、`items` 在条目可哈希时可参与集合式操作。

这题表现很好，说明视图对象不再是薄弱点。

#### B3（5.5 / 6）

输出预测正确，核心边界也正确：浅拷贝只复制外层字典，最初共享内部嵌套字典和内部列表；对共享内部列表 `append()` 会影响原对象；随后替换 `copy_mapping["menu.start"]` 只改变副本外层映射，不影响 `r.mapping`。

小扣分点：你在解释浅拷贝时说“内部的映射关系乃至键值槽位保存的引用都是共享的”，这句话容易过界。浅拷贝后的两个外层字典拥有各自独立的映射表；共享的是键对象和值对象的引用，不是外层映射关系本身。你后文其实已经用“替换副本外层映射不影响原字典”纠正了这个方向，但前一句建议以后改成：**浅拷贝复制新的外层映射表，表项中的 key/value 引用仍指向原对象。**

---

### C. 文件、文本、字节与编码边界（17.5 / 18）

#### C1（4.5 / 5）

主体正确。`path` 是路径对象，`f` 是打开后的文件对象，`text` 是读取出的 Python `str`，`with` 退出后文件对象关闭。

小扣分点：`f.read()` 不是“试图把文件打开”，文件在 `path.open(...)` 时已经打开；`read()` 是从已经打开的文件对象读取内容并返回 `str`。这个措辞很小，但文件对象边界处建议压准。

#### C2（5 / 5）

预测正确。你准确说明了 `str` 的 `len()` 按字符层操作，`bytes` 的 `len()` 按字节数操作，也解释了“底层由字节承载”和“Python 语言层按对象协议操作”不矛盾。

#### C3（4 / 4）

回答正确。你指出省略 `encoding` 会依赖环境默认编码，当前 Windows 环境中可能用 `cp936`，不一定立刻报错，但可能写出非 UTF-8 字节，后续按 UTF-8 读取就可能失败。

#### C4（4 / 4）

回答正确。`data` 是 Python `dict`，`rendered` 是 JSON 文本 `str`，`result` 是写入字符数的 `int`；磁盘文件保存的是编码后的字节。

---

### D. JSON、CSV 与序列化边界（17.5 / 18）

#### D1（5 / 5）

预测正确。你已经修正了此前关于 `ensure_ascii=False` 的模糊说法：它不改变 `json.dumps()` 的返回类型，返回值仍是 `str`；但它会改变返回字符串的实际内容。

#### D2（5 / 5）

预测正确。你准确说明了 tuple 可以被 JSON 编码成 array，但 JSON 不支持 set，所以第二个 `json.dumps(payload, ...)` 会在递归处理到 `payload["keys"]` 时抛出 `TypeError`。

#### D3（4 / 4）

预测正确。你已经掌握 Python 3.9 中 `namedtuple._asdict()` 返回普通 `dict`，并正确说明该 report 可成功 JSON 序列化。

这是本轮测验前暴露过的风险点，本题通过说明已经压实。

#### D4（3.5 / 4）

主体正确。CSV 是二维表文本，单元格是文本字段，`csv.DictReader` 读出的一行更接近字段名到单元格文本的映射；若要保留嵌套结构，应优先选择 JSON。

小扣分点：你写“JSON 的数据模型天然对应常见的 Python 嵌套结构：如 dict、list、tuple，并且读回来通常能够恢复多数数据类型”。这句话需要收紧。JSON 能自然表达 object/array/string/number/bool/null，对应 Python 中常见的 `dict/list/str/int/float/bool/None`；但 tuple 会变成 list，set 不支持，非字符串 dict key 也可能发生转换或限制。因此更精确的说法是：**JSON 适合保存由 JSON 数据模型支持的嵌套结构，但不保证完整恢复所有 Python 类型语义。**

---

### E. 阶段综合项目代码阅读（18 / 18）

#### E1（5 / 5）

回答优秀。你准确解释了为什么不能直接把 JSON object 解析成普通 `dict`，以及 pair list、普通 mapping、`Counter` 在重复 key 审计中的分工。

#### E2（4 / 4）

回答完整。`Resource` 的 6 个字段解释准确，并且能说明为什么同一个资源文件需要同时保留 `text`、`pairs`、`mapping` 和 `duplicate_counts`。

#### E3（4 / 4）

回答正确。你准确说明了 `set(source.mapping)` 提取 key 集合快照，差集/交集分别对应缺失、额外、共同 key，`sorted(...)` 用于稳定报告顺序。

#### E4（5 / 5）

回答优秀。`--observe` 的学习目的解释清楚，覆盖了视图/快照、重复 key 折叠、浅拷贝、文本/字节、JSON 文本/Python 对象等核心痛点。

---

### F. 核心对象类型横向收束与设计题（8 / 10）

#### F1（4 / 5）

大多数选型正确：`dict`、`list`、`namedtuple`、`set`、`Counter` 都合适。

主要扣分点在“输出机器可读结构化报告”这一行。你选择 `str`，并说明最终要经 JSON 序列化生成文本，这抓住了输出边界；但题目问的是“结构化报告”的对象选型，更完整答案应分两层：

```text
内部报告模型：dict / list / str / int / bool / None
输出边界：json.dumps(...) 返回 JSON 文本 str
文件边界：write_text(..., encoding="utf-8") 写入 UTF-8 字节
```

因此，单写 `str` 会弱化“机器可读结构化”的内部对象层。

#### F2（4 / 5）

整体数据流清晰，文件边界、JSON 文本到 Python 对象、`dict/set/list/Counter`、JSON 可序列化转换、UTF-8 写入边界都覆盖到了。

主要扣分点：题目明确要求检查重复 key，而普通 `json.loads(source_text)` 会直接把重复 key 折叠进 `dict`，丢失早期值。你的答案后面提到“在保留 pair list 的情况下统计重复 key”，但在数据流设计中应更明确写出：

```python
pairs = json.loads(text, object_pairs_hook=list)
counts = Counter(key for key, _ in pairs)
mapping = dict(pairs)
```

也就是说，重复 key 审计必须发生在普通 `dict` 折叠之前。

---

## 本阶段末评语与能力判断

### 通过结论

你通过了当前小阶段：**字典和文件：映射、持久化边界与核心类型收束**。

你也通过了当前大阶段：**Types and Operations** 的阶段末收束验收。

### 能力判断

本次测验显示，你已经能稳定使用对象模型解释 Python 核心内置类型，而不是只背 API 或运行结果。尤其是以下能力已经形成：

- 能解释字典键去重依赖 `hash()` 与 `==`，不是 `is`。
- 能区分修改字典本体、替换某个键的值引用、修改字典中保存的可变值对象。
- 能解释视图对象和列表快照的差异。
- 能说明浅拷贝只复制外层容器，内部可变对象仍可能共享。
- 能把路径对象、文件对象、文本 `str`、`bytes`、编码、JSON 文本、Python 对象结构和磁盘字节分层说明。
- 能把 `dict`、`list`、`tuple` / `namedtuple`、`set`、`Counter`、JSON/CSV 和文件边界放进一个实际本地化资源审计项目中理解。

当前水平判断：**准中级入门已经基本坐稳，正在进入“能用对象模型做小型工程设计”的阶段。**

### 仍需复盘的活跃边界

1. `frozenset` 是否可哈希取决于其所有元素是否可哈希，不要把“冻结集合”直接等同于无条件可哈希。
2. 浅拷贝复制的是新的外层映射表，表项中的 key/value 引用仍共享；不要说“外层映射关系本身共享”。
3. JSON 不保证完整恢复所有 Python 类型语义：tuple 会变 list，set 不支持，非字符串 key 有边界。
4. “机器可读结构化报告”要分清内部 `dict/list` 报告模型、JSON 文本 `str`、文件字节三层。
5. 需要审计 JSON 重复 key 时，必须在普通 `dict` 折叠前使用 `object_pairs_hook` 或 pair list。

### 学习画像更新

稳定强项：

- 对对象、名字绑定、可变性、映射、哈希、视图、浅拷贝、文本/字节、JSON/CSV 和文件边界的主干理解已经稳定。
- 已能把多种核心对象类型组合到项目级场景中，并能解释每种类型承担的职责。
- 对阶段综合项目 `localization_resource_auditor` 的架构和数据流已经达到可复盘、可迁移的理解水平。

仍需关注：

- 工程设计题中要更明确地区分“内部模型”和“输出边界”。
- 遇到序列化问题时，要先确认目标数据模型支持哪些类型，再判断是否需要转换。
- 后续进入语句、函数或更大项目时，继续保持“对象本体 / 名字绑定 / 显示形式 / 外部边界”的解释习惯。

下一阶段建议：

- 可以进入下一大阶段学习。
- 下一阶段应继续保持预测题和小项目节奏，重点观察控制流、函数调用、作用域、异常处理和模块边界如何与当前已经掌握的对象模型结合。
