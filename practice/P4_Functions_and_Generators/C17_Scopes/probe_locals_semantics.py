import sys

print("PYTHON:", sys.version)
print("=" * 70)

# A. 函数作用域：每次调用返回新字典；改返回的字典不影响变量
def f_snapshot():
    a = 1
    d1 = locals()
    d2 = locals()
    print("A. d1 is d2?", d1 is d2, "| before:", d1)
    d1["a"] = 999
    print("   after d1['a']=999, real a =", a, "| d2 =", d2)

f_snapshot()
print("-" * 70)

# B. 自由变量（闭包变量）是否出现在 locals() 中
def outer():
    z = 10
    def inner():
        print("B. inner.locals():", locals(), "| 'z' in locals?", 'z' in locals())
        return z
    return inner

outer()()
print("-" * 70)

# C. 静态上是局部、但调用 locals() 时尚未绑定的名字：不出现
def f_unbound():
    print("C. before assignment:", locals())
    q = 5
    print("   after assignment :", locals())

f_unbound()
print("-" * 70)

# D. 通过 sys._getframe().f_locals 修改：3.13+ 是写穿代理，之前是普通快照
def f_flocals():
    v = 1
    frame = sys._getframe()
    frame.f_locals["v"] = 2
    print("D. real v after writing frame.f_locals:", v)

f_flocals()
print("-" * 70)

# E. 模块作用域：locals() 与 globals() 的关系
print("E. module scope: locals() is globals()?", locals() is globals())
print("-" * 70)

# F. 类体作用域：locals() 是类体命名空间的实际字典视图
class C:
    attr = 42
    print("F. class body locals():", locals())

print("-" * 70)

# G. 函数里的 global 名字不进入 locals()
g_counter = 7

def f_global():
    global g_counter
    print("G. locals() with global name:", locals(), "| g_counter =", g_counter)

f_global()
