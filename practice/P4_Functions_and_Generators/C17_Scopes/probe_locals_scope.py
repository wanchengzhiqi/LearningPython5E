import sys

print("PYTHON:", sys.version)
print("EXE   :", sys.executable)
print("=" * 60)


def outer():
    x, y = 10, 12

    def middle():
        print("middle.locals():", locals())
        print("middle.y       :", y)   # <-- 注释/不注释这一行

        def inner():
            nonlocal x
            x = 2
            y = 20
            print("inner.locals() :", locals())
            return x

        return inner

    return middle


print("RESULT:", outer()()())
print("=" * 60)


def outer2():
    x, y = 10, 12

    def middle():
        print("middle2.locals():", locals())
        # print(y)   # 这一行被注释掉

        def inner():
            nonlocal x
            x = 2
            y = 20
            print("inner2.locals() :", locals())
            return x

        return inner

    return middle


print("RESULT2:", outer2()()())
print("=" * 60)

# 代码对象级别的证据：变量分类（varnames / freevars / cellvars）
m1 = outer()
i1 = m1()
m2 = outer2()
i2 = m2()

for label, f in [
    ("outer  (with print(y))", outer),
    ("middle (with print(y))", m1),
    ("inner  (with print(y))", i1),
    ("outer2 (no print(y))  ", outer2),
    ("middle2(no print(y))  ", m2),
    ("inner2 (no print(y))  ", i2),
]:
    code = f.__code__
    print(f"{label:27} varnames={code.co_varnames!r} freevars={code.co_freevars!r} cellvars={code.co_cellvars!r}")
