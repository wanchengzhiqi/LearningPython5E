import sys
import itertools
from collections import deque

print("sys.version   :", sys.version.replace("\n", " | "))
print("sys.executable:", sys.executable)
print()

# ===================== 问题 1: map/filter 等价版 =====================
target = [(x, y) for x in range(5) if x % 2 == 0
          for y in range(5) if y % 2 == 1]
print("A) 原推导式结果        :", target)

# --- 版本1: 只用手工嵌套的 map/filter（书的语境，刻意丑） ---
res_strict = list(itertools.chain.from_iterable(
    map(lambda x: map(lambda y: (x, y),
                      filter(lambda y: y % 2 == 1, range(5))),
        filter(lambda x: x % 2 == 0, range(5)))
))
print("B) 严格 map/filter 版  :", res_strict)
print("   与推导式一致        :", res_strict == target)

# --- 版本2: product + filter（工程推荐） ---
res_product = list(filter(
    lambda t: t[0] % 2 == 0 and t[1] % 2 == 1,
    itertools.product(range(5), repeat=2),
))
print("C) product+filter 版   :", res_product)
print("   与推导式一致        :", res_product == target)

# --- 陷阱: 复用一个已被耗尽的 filter 迭代器 ---
odds = filter(lambda y: y % 2 == 1, range(5))  # 有状态、一次性
res_bug = list(itertools.chain.from_iterable(
    map(lambda x: map(lambda y: (x, y), odds),
        filter(lambda x: x % 2 == 0, range(5)))
))
print("D) 复用 odds 的坑       :", res_bug)  # 只剩 x=0 的两对

# --- 3.x 的 map/filter 是惰性迭代器 ---
print("E) filter 对象的类型   :", type(odds).__name__)
print()


# ===================== 问题 2: 非递归排列 =====================
def permute1(seq):
    if not seq:
        return [seq]
    else:
        res = []
        for i in range(len(seq)):
            rest = seq[:i] + seq[i + 1:]
            for x in permute1(rest):
                res.append(seq[i:i + 1] + x)
        return res


def permute2(seq):
    if not seq:
        yield seq
    else:
        for i in range(len(seq)):
            rest = seq[:i] + seq[i + 1:]
            for x in permute2(rest):
                yield seq[i:i + 1] + x


print("F) permute1('abc')          :", permute1('abc'))
print("G) list(permute2('abc'))    :", list(permute2('abc')))
print("   itertools.permutations   :", list(itertools.permutations('abc')))
print("   ''.join 版               :", [''.join(t) for t in itertools.permutations('abc')])


# --- 非递归 1: 显式栈 DFS（倒序压栈 => 与递归版顺序一致） ---
def permute_stack(seq):
    results = []
    stack = [(seq[:0], seq)]  # (已固定前缀, 剩余待排)
    while stack:
        prefix, rest = stack.pop()
        if not rest:
            results.append(prefix)
        else:
            for i in reversed(range(len(rest))):  # 倒序压栈 -> 弹栈顺序=递归顺序
                stack.append((prefix + rest[i:i + 1], rest[:i] + rest[i + 1:]))
    return results


print()
print("H) permute_stack('abc')     :", permute_stack('abc'))
print("   与 permute1 顺序一致     :", permute_stack('abc') == permute1('abc'))


# --- 非递归 2: 生成器 + 显式栈（惰性且非递归） ---
def permute_gen_stack(seq):
    stack = [(seq[:0], seq)]
    while stack:
        prefix, rest = stack.pop()
        if not rest:
            yield prefix
        else:
            for i in reversed(range(len(rest))):
                stack.append((prefix + rest[i:i + 1], rest[:i] + rest[i + 1:]))


print("I) list(permute_gen_stack)  :", list(permute_gen_stack('abc')))
print("   惰性(首个 next)          :", next(permute_gen_stack('abc')))


# --- 非递归 3: 显式队列 BFS ---
def permute_queue(seq):
    results = []
    q = deque([(seq[:0], seq)])
    while q:
        prefix, rest = q.popleft()
        if not rest:
            results.append(prefix)
        else:
            for i in range(len(rest)):
                q.append((prefix + rest[i:i + 1], rest[:i] + rest[i + 1:]))
    return results


print("J) permute_queue('abc')     :", permute_queue('abc'))
print("   与 permute1 顺序一致     :", permute_queue('abc') == permute1('abc'))

# --- 规模核对: 4! = 24 ---
print("K) len(permute_stack('hack')) =", len(permute_stack('hack')),
      "| 与 permute1 一致:", permute_stack('hack') == permute1('hack'))

# --- 递归深度 vs 迭代：临时压低 recursion limit 对比 ---
old_limit = sys.getrecursionlimit()

sys.setrecursionlimit(30)
try:
    try:
        permute1('a' * 35)
    except RecursionError as e:
        print("L) 递归列表版(limit=30):", type(e).__name__, "— 深度先于 N! 爆炸发生")
finally:
    sys.setrecursionlimit(old_limit)

sys.setrecursionlimit(30)
try:
    g = permute2('a' * 35)
    print("   permute2 惰性: 对象已创建:", type(g).__name__, "| 创建时不报错")
    try:
        next(g)
    except RecursionError:
        print("   首次 next() 才炸")
finally:
    sys.setrecursionlimit(old_limit)

sys.setrecursionlimit(30)
try:
    first = next(permute_gen_stack('a' * 35))
    print("   同一低限额, 迭代生成器首个结果:", repr(first[:5]), "... 长度", len(first))
finally:
    sys.setrecursionlimit(old_limit)

print()
print("   注意: 迭代版绕开的是递归深度, 绕不开 35! 的结果爆炸——只能取前几个")
