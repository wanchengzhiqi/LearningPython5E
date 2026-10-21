import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()


# ---------- 原题 ----------
def with_summary(events):
    events.append("start")
    yield "menu.start"
    events.append("return")
    return {"produced": 1}


probe_events = []
probe = with_summary(probe_events)

head = next(probe)  # 第一次消费
print("A) head:", head, "| probe_events:", probe_events)

remaining = list(probe)  # 第二次消费：摘要在这里被忽略
print("B) remaining:", remaining)
print("   probe_events:", probe_events)

try:
    next(probe)  # 第三次消费：生成器已耗尽
except StopIteration as error:
    late_value = error.value
print("C) late_value:", late_value)
print()


# ---------- 对照组1：恰好“耗尽”的那一次 next 才能拿到 value ----------
def with_summary2(events):
    events.append("start")
    yield "menu.start"
    events.append("return")
    return {"produced": 1}


ev2 = []
g2 = with_summary2(ev2)
next(g2)  # 第一次：yield
try:
    next(g2)  # 第二次：恰好耗尽 -> value 带着摘要
except StopIteration as e:
    print("D) 恰好耗尽的 next 捕获到 value:", e.value)
    print("   ev2:", ev2)
print()


# ---------- 对照组2：yield from 会把子生成器的返回值转发出来 ----------
def delegator(events):
    summary = yield from with_summary(events)
    return ("delegated", summary)


ev3 = []
g3 = delegator(ev3)
try:
    while True:
        next(g3)
except StopIteration as e:
    print("E) yield from 转发的摘要:", e.value)
    print("   ev3:", ev3)
print()


# ---------- 对照组3：手动 try/except 循环可以拿到摘要 ----------
def with_summary3(events):
    yield "a"
    return {"n": 1}


ev4 = []
g4 = with_summary3(ev4)
summary4 = None
while True:
    try:
        next(g4)
    except StopIteration as e:
        summary4 = e.value
        break
print("F) 手动循环捕获:", summary4)
print()

# ---------- 边界：耗尽后再迭代，安静地得到空结果，不报错 ----------
print("G) 再 list(probe):", list(probe))
