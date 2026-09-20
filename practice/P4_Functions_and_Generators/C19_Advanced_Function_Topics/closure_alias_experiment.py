import sys

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()

# ---------- 原题 ----------
def make_tracker(label):
    count = 0
    history = []

    def record(key):
        nonlocal count
        count += 1
        entry = f"{label}:{count}:{key}"
        history.append(entry)
        return entry

    def snapshot():
        return count, tuple(history), history

    return record, snapshot, history

record, snapshot, exposed = make_tracker("ui")

print("A) 初始 exposed is snapshot()[2] :", exposed is snapshot()[2])  # 同一个列表

old = exposed
exposed = ["detached"]          # 重绑定名字，不是改对象

record("open")
old.append("manual")

print()
print("B) snapshot()                 :", snapshot())
print("C) snapshot()[:2]             :", snapshot()[:2])
print("D) exposed                    :", exposed)
print()
print("E) old is 闭包里的 history     :", old is snapshot()[2])
print("   exposed is 闭包里的 history :", exposed is snapshot()[2])
print("   old is exposed             :", old is exposed)
print()

# ---------- 旁证1：snapshot 的第三个元素是“活”的内部列表，不是拷贝 ----------
live = snapshot()[2]
live.append("via-live")
print("F) 通过第三个元素改内部列表后 snapshot()[1] :", snapshot()[1])
print()

# ---------- 旁证2：闭包 cell 直接观察（CPython 内省） ----------
cells = {name: cell.cell_contents
         for name, cell in zip(record.__code__.co_freevars, record.__closure__)}
print("G) record 的闭包 cell :", cells)
print()

# ---------- 旁证3：history 只用 append（不重绑定）所以不需要 nonlocal；
#            而 replace 里 h = [x] 是“重绑定”，会遮蔽外层 ----------
def make_shadow():
    h = []
    def add(x):
        h.append(x)          # 调用方法：改的是外层 h 指向的对象
    def replace(x):
        h = [x]              # 赋值：本地新建名字，外层的 h 不受影响
    return add, replace, h

add, replace, h2 = make_shadow()
add(1)
replace(99)
print("H) replace(99) 之后外层 h2 =", h2)   # [1]
add(2)
print("   add(2) 之后 h2 =", h2)           # [1, 2] —— add 始终操作外层对象
print()

# ---------- 旁证4：count += 1 是“重绑定”，没有 nonlocal 会怎样 ----------
def make_count_bad():
    count = 0
    def bump():
        count += 1          # 未声明 nonlocal
    return bump

try:
    make_count_bad()()
except UnboundLocalError as e:
    print("I) 无 nonlocal 的 count += 1 ->", type(e).__name__, "-", e)
