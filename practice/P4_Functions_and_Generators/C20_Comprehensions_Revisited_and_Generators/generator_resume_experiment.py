import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()


# ---------- 原题 ----------
def track(label, record, events):
    count = 0
    events.append((label, "start"))
    while count < 2:
        count += 1
        events.append((label, "yield", count, record["text"]))
        yield record
        events.append((label, "resume", count, record["text"]))
    events.append((label, "end", count))


events = []
source = {"text": "Start"}
original = source

left = track("A", source, events)
right = track("B", source, events)

first = next(left)
print("A) 第一次推进 left 后 events:", events)
print("   first is original:", first is original)

first["text"] = "Begin"  # 原地修改 D0 -> 所有共享者可见
source = {"text": "Detached"}  # 重绑定 source -> 不影响 D0

from_right = next(right)
print("B) B 首次推进新增:", events[-2:])
print("   from_right is original:", from_right is original,
      "| source is original:", source is original)

again = next(left)
print("C) A 第二次推进新增:", events[-2:])
print("   again is original:", again is original)
print()

# ---------- 题目核心：first 重绑定后推进 right ----------
first = {"text": "Separate"}  # 新建 D2，只重绑定 first；D0 未动
last_from_right = next(right)
print("D) B 本次新增两条事件:", events[-2:])
print("E) last_from_right is original:", last_from_right is original)
print("   last_from_right['text']:", last_from_right["text"])
print("   first is original:", first is original, "| first['text']:", first["text"])
print()

print("F) 完整事件流:")
for e in events:
    print("   ", e)
print()

# ---------- 边界：B 的 end 事件要第三次 next 才出现 ----------
try:
    next(right)
except StopIteration:
    pass
print("G) 第三次 next(right) 后末尾事件:", events[-2:])
print()

# ---------- 对比：原地修改 vs 重绑定，对生成器 record 绑定的可见性 ----------
events2 = []
d0 = {"text": "X"}
d1 = {"text": "X"}
g0 = track("C", d0, events2)
g1 = track("D", d1, events2)
next(g0)  # C 暂停在第一次 yield
next(g1)  # D 暂停在第一次 yield

d0["text"] = "MUTATED"  # 原地修改
next(g0)  # C 恢复
d1 = {"text": "REBOUND"}  # 只重绑定名字 d1
next(g1)  # D 恢复

resume_c = [e for e in events2 if e[0] == "C" and e[1] == "resume"][0]
resume_d = [e for e in events2 if e[0] == "D" and e[1] == "resume"][0]
print("H) 原地修改后 C 的 resume:", resume_c)
print("I) 重绑定后   D 的 resume:", resume_d)
