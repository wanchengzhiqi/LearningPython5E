#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/23


class BadKey:
    def __init__(self, value, h):
        self.value = value
        self.h = h

    def __eq__(self, other):
        return isinstance(other, BadKey) and self.value == other.value

    def __hash__(self):
        return self.h

    def __repr__(self):
        return f"BadKey({self.value!r}, h={self.h})"


a = BadKey("MENU_START", 1)
b = BadKey("MENU_START", 2)

print(a == b)          # True
print(hash(a), hash(b))  # 1 2

d = {a: "A", b: "B"}
print(d)
print(len(d))

"""
这很危险：明明 a == b，字典却把它们当成两个不同键保存了。因为字典先按哈希值走查找路线，哈希不同，通常根本不会进入“这是同一个键吗”的正确比较位置。
对字典的影响：去重会坏，查找会坏，更新会坏，删除也可能坏。比如 d = {a: "A"} 时，b in d 可能是 False，即使 b == a 为真，也可能无法通过 d[b] 访问到 d[a] 的值。
"""

s = {a, b}
print(len(s))  # 2

"""对集合也一样，这违反了直觉中的“集合去重”，因此，哈希值必须与相等性保持一致，否则会导致字典和集合等基于哈希的数据结构出现严重问题。"""


class CollisionKey:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, CollisionKey) and self.value == other.value

    def __hash__(self):
        return 42

    def __repr__(self):
        return f"CollisionKey({self.value!r})"


a = CollisionKey("MENU_START")
b = CollisionKey("MENU_QUIT")
c = CollisionKey("MENU_START")

print(a == b)  # False
print(a == c)  # True
print(hash(a), hash(b), hash(c))  # 42 42 42

d = {a: "A", b: "B", c: "C"}
print(d)  # {CollisionKey('MENU_START'): 'C', CollisionKey('MENU_QUIT'): 'B'}
print(len(d))  # 2

s = {a, b, c}
print(len(s))  # 2

"""虽然 a 和 c 的哈希值相同，但它们在字典中被正确地识别为相等的键，因此 d 中只有两个键：一个是 a/c，另一个是 b。这说明哈希冲突虽然会导致性能下降（因为需要更多的比较来区分键），但只要 __eq__ 方法正确实现，字典和集合仍能够正确地处理键的相等性。"""
