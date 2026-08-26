import sys
print("PYTHON:", sys.version)
print("=" * 60)

seed = ["base"]

def make_default():
    print("MAKE")
    return seed

def record(item, records=make_default(), *, flags=[]):
    records.append(item)
    flags.append(len(records))
    return records, flags

# ---- 刚定义完 record 时（注意：MAKE 已经打印过了）----
default_records = record.__defaults__[0]
default_flags = record.__kwdefaults__["flags"]
print("after def        : seed is default_records?",
      seed is default_records, "| contents:", default_records, default_flags)
print("stored defaults  :", record.__defaults__, record.__kwdefaults__)

# ---- 重新绑定全局名字 seed ----
old_list = default_records
seed = ["replacement"]
print("after seed=...   : seed is default_records?",
      seed is default_records, "| seed =", seed,
      "| default_records =", default_records)
print("old list still alive and reachable:", old_list is record.__defaults__[0])

# ---- 两次调用 ----
a = record("A")
print("after record('A'):", "a[0] is default_records?", a[0] is default_records,
      "| a[1] is default_flags?", a[1] is default_flags,
      "| state:", a[0], a[1])

b = record("B")
print("after record('B'):", "a is b?", a is b,
      "| a == b?", a == b,
      "| a[0] is b[0]?", a[0] is b[0],
      "| a[1] is b[1]?", a[1] is b[1])
print("a now:", a)
print("b now:", b)
print("__defaults__   :", record.__defaults__)
print("__kwdefaults__ :", record.__kwdefaults__)
print("seed now:", seed)
print("same single records object for all calls?",
      a[0] is b[0] is default_records)
print("same single flags object for all calls?",
      a[1] is b[1] is default_flags)
