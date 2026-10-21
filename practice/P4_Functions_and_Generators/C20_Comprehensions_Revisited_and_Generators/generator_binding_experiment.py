import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()


# ---------- 原题（含插入行） ----------
def argument(record, events):
    events.append("argument:evaluated")
    return record


def produce(record, events):
    events.append("body:start")
    yield record
    events.append("body:after-yield")


events = []
record = {"key": "menu.start"}

factory = produce
stream = factory(argument(record, events), events)
print("A) 首次 print:", tuple(events))  # 实参已求值，函数体还没跑

record["key"] = "menu.continue"  # ← 插入行

item = next(stream)
print("B) 推进后 events:", tuple(events))
print("C) item['key']   :", item["key"])
print("D) item is record:", item is record)
print("E) iter(stream) is stream:", iter(stream) is stream)
print("F) record['key'] :", record["key"])
print()

# ---------- 边界1：推进之后再改 record，item 也同步可见（同一对象） ----------
record["key"] = "menu.quit"
print("G) 再次改 record 后 item['key']:", item["key"])
print()

# ---------- 边界2：body:after-yield 要第二次 next 才出现 ----------
try:
    next(stream)
except StopIteration:
    pass
print("H) 第二次 next 后 events:", tuple(events))
print()


# ---------- 旁证1：普通函数里参数同样绑定对象引用，不是拷贝 ----------
def sink(d):
    return d


rec2 = {"key": "x"}
s = sink(rec2)
rec2["key"] = "y"
print("I) s['key'] =", s["key"], "| s is rec2:", s is rec2)
print()

# ---------- 旁证2：调用时实参急切求值；生成器函数体延迟到首次 next ----------
events3 = []


def side(v):
    events3.append("arg-evaluated")
    return v


def gen2(ev):
    ev.append("body:start")
    yield


g2 = gen2(side(events3))
print("J) 调用后 events3:", events3)  # 只有 arg-evaluated
next(g2)
print("   next 后 events3:", events3)  # 才出现 body:start
print()


# ---------- 旁证3：yield 显式拷贝才会断开身份 ----------
def produce_copy(record, events):
    events.append("body:start")
    yield dict(record)


events4 = []
rec4 = {"key": "menu.start"}
it4 = next(produce_copy(rec4, events4))
print("K) 显式拷贝版: it4 is rec4:", it4 is rec4, "| it4:", it4)
print()


# ---------- 旁证4：函数体延迟执行 => 值在“首次推进时”才被读取 ----------
def produce_key(record, events):
    events.append("body:start")
    key = record["key"]  # 首次 next 时才执行这一行
    yield key


events5 = []
rec5 = {"key": "menu.start"}
g5 = produce_key(rec5, events5)
rec5["key"] = "menu.continue"  # 绑定后、首次推进前修改
print("L) 生成器推进时读值:", next(g5))  # menu.continue（延迟读取看到新值）


# 对比：普通函数在“调用时”就读值
def read_now(record, events):
    events.append("body:start")
    return record["key"]


rec6 = {"key": "menu.start"}
v6 = read_now(rec6, [])
rec6["key"] = "menu.continue"
print("M) 普通函数调用时读值:", v6)  # menu.start（调用时已读走旧值）
