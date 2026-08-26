import sys
print("PYTHON:", sys.version)
print("=" * 50)

def mark(name, value):
    print("mark", name)
    return value

def configure(path, language):
    print("BODY")
    # 进入函数时：path 与调用方 p 绑定同一个列表对象？
    print("inside: path is p?", path is p)
    language = "en-US"
    path.append("done")
    print("inside after assignments:", path, language)

p = ["config.json"]
lang = "zh-CN"

configure(
    mark("P", p),
    mark("L", lang),
)

print(p)
print(lang)
print("=" * 50)

# 对照实验 1：给 path 重新赋值（改名重绑），不会影响调用方
p2 = ["a.json"]
def rebind(path):
    path = ["other.json"]      # 局部名字重新绑定到新列表对象
    path.append("x")

rebind(p2)
print("rebind case: p2 =", p2)

# 对照实验 2：不可变对象没有可原地修改的接口
s = "hello"
def try_change(t):
    t = t + "!"               # 新字符串对象；只重绑局部名字
try_change(s)
print("immutable case: s =", s)

# 对照实验 3：可变对象原地修改，两个名字都看到
a = []
b = a
print("aliases: a is b?", a is b)
b.append(1)
print("after b.append(1): a =", a, "b =", b)
