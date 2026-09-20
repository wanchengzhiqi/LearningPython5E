import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()

# ---------- 原题 ----------
events = []

def lower(text):
    events.append("lower")
    return text.lower()

def choose(rule):
    events.append("choose")
    return rule

registry = {"normalize": lower}
print("构造 registry 后 events   :", events)   # 引用不调用 -> []

selected = choose(registry["normalize"])
print("A) 第一处 events           :", events)
print("B) selected is lower       :", selected is lower)
print("   selected is registry['normalize']:", selected is registry["normalize"])
print("   selected.__name__       :", selected.__name__)
print("   id(selected)==id(lower) :", id(selected) == id(lower))

result = selected("MENU.START")
print("C) 第二处 events           :", events)
print("D) result                 :", repr(result), "| result == 'menu.start':", result == "menu.start")
print()

# ---------- 旁证1：只引用不调用 ----------
events2 = []
def lower2(text):
    events2.append("lower")
    return text.lower()

reg2 = {"normalize": lower2}
print("E) 构造 reg2 后 events2    :", events2)

# ---------- 旁证2：构造时误加括号 ----------
reg3 = {"normalize": lower2("X")}   # 这里 lower2 已被调用！
print("F) 构造 reg3 后 events2    :", events2, "| reg3['normalize'] =", repr(reg3["normalize"]))
print("   callable(reg2['normalize']):", callable(reg2["normalize"]),
      "| callable(reg3['normalize']):", callable(reg3["normalize"]))
try:
    reg3["normalize"]("Y")
except TypeError as e:
    print("   reg3['normalize']('Y')  ->", type(e).__name__, "-", e)
print()

# ---------- 旁证3：字符串与 is ----------
r2 = lower2("MENU.START")
print("G) r2 == 'menu.start'      :", r2 == "menu.start")
print("   r2 is 'menu.start'      :", r2 is "menu.start")
print("   'menu.start' is 'menu.start':", "menu.start" is "menu.start")
print()

# ---------- 旁证4：str.lower 也是普通函数对象 ----------
print("H) str.lower('ABC')        :", str.lower("ABC"))
print()

# ---------- 旁证5：Unicode 下 lower 可能改变长度 ----------
low_i = "İ".lower()
print("I) repr('İ'.lower())      :", repr(low_i), "| len:", len(low_i))
