import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()

# ---------- 原题（正确版） ----------
def normalize(keys, index=0):
    if index == len(keys):
        return []
    current = keys[index].strip().casefold()
    tail = normalize(keys, index + 1)
    return [current, *tail]

print("A) normalize([' A ', ' B ']) :", normalize([" A ", " B "]))
print()

# ---------- 各层返回轨迹 ----------
def normalize_trace(keys, index=0, depth=0):
    if index == len(keys):
        r = []
        print(f"    {'  '*depth}基线 (index={index}) -> 返回 {r!r}")
        return r
    current = keys[index].strip().casefold()
    tail = normalize_trace(keys, index + 1, depth + 1)
    r = [current, *tail]
    print(f"    {'  '*depth}index={index} current={current!r} tail={tail!r} -> 返回 {r!r}")
    return r

print("B) 正确版各层轨迹:")
normalize_trace([" A ", " B "])
print()

# ---------- 改坏版：基线 return [] -> 裸 return ----------
def normalize_bad_trace(keys, index=0, depth=0):
    if index == len(keys):
        print(f"    {'  '*depth}基线 (index={index}) -> 裸 return（返回 None）")
        return
    current = keys[index].strip().casefold()
    tail = normalize_bad_trace(keys, index + 1, depth + 1)
    print(f"    {'  '*depth}index={index} current={current!r} tail={tail!r}  <- 即将执行 [current, *tail]")
    return [current, *tail]

print("C) 坏版各层轨迹:")
try:
    normalize_bad_trace([" A ", " B "])
except TypeError as e:
    print("    =>", type(e).__name__, ":", e)
    import traceback
    print("    逐帧回溯（外 -> 内，最内帧即最先出问题的语句）:")
    for fr in traceback.extract_tb(e.__traceback__):
        print(f"       {fr.name} @ line {fr.lineno}: {fr.line.strip()}")
print()

# ---------- 旁证1：裸 return 就是 return None；* 对 None 解包报错 ----------
def f():
    return
print("D) 裸 return 的值 :", f())
try:
    [*None]
except TypeError as e:
    print("   [*None] ->", type(e).__name__, ":", e)
print()

# ---------- 旁证2：* 的契约是“可迭代”，字符串会静默拆成单字符 ----------
print("E) [*'ab'] :", [*"ab"])
