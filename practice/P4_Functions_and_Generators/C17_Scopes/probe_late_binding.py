import dis
import functools
import sys

print("PYTHON:", sys.version)
print("=" * 70)

# ---------- 0. 书中的原始现象 ----------
def makeActions():
    acts = []
    for i in range(5):
        acts.append(lambda x: i ** x)  # i 是自由变量，不是值
    return acts

acts = makeActions()
print("original:", [f(2) for f in acts])
print("all share ONE cell? contents:",
      [c.cell_contents for c in acts[0].__closure__],
      [c.cell_contents for c in acts[-1].__closure__])


def makeActionsAndLoopVar():
    acts = []
    for i in range(5):
        acts.append(lambda: i)
    return acts, i            # i 在函数体内、循环结束后依然可见

_, final_i = makeActionsAndLoopVar()
print("loop var still visible after loop inside the function, final value =", final_i)
print("=" * 70)

# ---------- 1. 晚绑定本质：即使没有循环，重绑定也会改变闭包结果 ----------
def bind_then_call():
    n = 1
    f = lambda: n        # 捕获的是变量 n（cell），不是当时的值 1
    n = 99
    return f

print("late binding without loop:", bind_then_call()())
print("=" * 70)

# ---------- 2. 解法 A：默认参数在 def 执行时求值并保存 ----------
def makeActionsDefault():
    acts = []
    for i in range(5):
        acts.append(lambda x, i=i: i ** x)  # 每次循环创建一个新默认值对象绑定
    return acts

acts_d = makeActionsDefault()
print("default-arg fix :", [f(2) for f in acts_d])
print("stored defaults :", [f.__defaults__ for f in acts_d])
print("=" * 70)

# ---------- 3. 解法 B：工厂函数，每次调用制造独立作用域/cell ----------
def makePower(base):
    return lambda x: base ** x

acts_f = [makePower(i) for i in range(5)]
print("factory fix     :", [f(2) for f in acts_f])
print("distinct cells? :", [c.cell_contents for f in acts_f for c in f.__closure__])
print("=" * 70)

# ---------- 4. 解法 C：functools.partial 在创建时保存位置参数 ----------
acts_p = [functools.partial(lambda base, x: base ** x, i) for i in range(5)]
print("partial fix     :", [f(2) for f in acts_p])
print("partial.args    :", [f.args for f in acts_p])
print("=" * 70)

# ---------- 5. 字节码证据：一个用 DEREF（运行时找 cell），一个用 FAST（默认值已是局部参数） ----------
dis.dis(makeActions)
print("-" * 40)
dis.dis(makeActionsDefault)
print("=" * 70)

# ---------- 6. 默认值解法的代价/边界：参数可被调用方覆盖 ----------
print("caller overrides i:", acts_d[1](2, i=100), "(expected act1's own meaning: 1**2 == 1)")
print("=" * 70)

# ---------- 7. 若循环从未执行，自由变量从未绑定，调用时才报错 ----------
def never():
    acts = [lambda: i]
    for i in ():          # 循环体一次都不执行，i 从未绑定
        acts.append(lambda: i)
    return acts[0]

try:
    print(never()())
except NameError as e:
    print("empty-loop NameError:", type(e).__name__, str(e))
print("=" * 70)

# ---------- 8. 列表推导式有自己的作用域，但循环变量仍是同一个 cell ----------
funcs = [lambda: v for v in range(3)]
print("comprehension version:", [f() for f in funcs])
funcs_d = [lambda v=v: v for v in range(3)]
print("comprehension default:", [f() for f in funcs_d])
