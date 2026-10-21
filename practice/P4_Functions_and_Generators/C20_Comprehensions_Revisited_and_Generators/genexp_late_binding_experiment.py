import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()


# ---------- 原题（events 换成具名列表以便观察，语义不变） ----------
def scale(items, factor, events):
    events.append("scale:start")
    for item in items:
        yield item * factor


values = [1, 2]
factor = 2

events = []
expr = (n * factor for n in values)
func = scale(values, factor, events)

values = [7, 8]
factor = 10

print("A) list(expr):", list(expr))  # ?
print("B) list(func):", list(func))  # ?
print("   events    :", events)
print()


# ---------- 旁证1：生成器函数参数在“调用时”绑定对象 ----------
def show(items, factor):
    yield items, factor


gv = [1]
gf = 2
gg = show(gv, gf)
gv = [9]
gf = 99
print("C) list(gg):", list(gg))  # [([1], 2)] —— 调用时绑定
print()

# ---------- 旁证2：genexp 最左 iterable 提前求值；体表达式延迟求值 ----------
v = [1, 2]
f2 = 5
e = (n * f2 for n in v)  # 此刻捕获的是 v 指向的列表对象
v_old = v
v = [7, 8]  # 重绑定：genexp 看不见
v_old.append(3)  # 原地修改旧列表：genexp 看得见
f2 = 50
print("D) list(e):", list(e))  # [50, 100, 150]：旧对象(含追加的3) + 最新 factor
print()

# ---------- 旁证3：消费时机决定 genexp 看到的自由变量 ----------
f = 2
e2 = (n * f for n in [1, 2])
before = list(e2)  # 先消费：看到 2
f = 10
print("E) 先消费  :", before)
f = 2
e3 = (n * f for n in [1, 2])
f = 10
print("   后消费  :", list(e3))  # [10, 20]
print()

# ---------- 旁证4：只有“最左”for 的 iterable 提前求值 ----------
o = [1]
i = [10]
ge = (x + y for y in o for x in i)
o = [2]  # 最左 iterable 已捕获 -> 被忽略
i = [20]  # 内层 iterable 延迟求值 -> 生效
print("F) 嵌套 genexp:", list(ge))  # [21]
print()

# ---------- 旁证5：生成器函数体延迟执行 ----------
events2 = []
func2 = scale(values, factor, events2)
print("G) 调用后 events2:", events2)  # [] —— 函数体还没跑
r2 = list(func2)
print("   消费后 events2:", events2, "| 结果:", r2)
