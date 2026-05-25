#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/23

from dataclasses import dataclass, field


def normalize_key(text):
    return text.strip().casefold().replace("-", "_")


@dataclass(frozen=True)
class ResourceKey:
    raw: str
    _normalized: str = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "_normalized", normalize_key(self.raw))

    @property
    def normalized(self):
        return self._normalized

    def __eq__(self, other):
        if not isinstance(other, ResourceKey):
            return NotImplemented
        return self.normalized == other.normalized

    def __hash__(self):
        return hash(self.normalized)

    def __repr__(self):
        return f"ResourceKey(raw={self.raw!r}, normalized={self.normalized!r})"


a = ResourceKey(" MENU-START ")
b = ResourceKey("menu_start")

print(a == b)                 # True
print(a == "menu_start")      # False，不要随便让 ResourceKey(...) == "menu_start" 为真。因为如果你让自定义对象和普通 str 相等，就还必须保证它们哈希也一致；可是现在又做了 strip()、casefold()、replace() 规范化，很容易破坏跨类型契约。保守做法是：查字典时也用 ResourceKey("menu_start") 作为 key，而不是直接用 "menu_start" 这个 str。
print(hash(a) == hash(b))     # True

d = {}
d[a] = "Start"
d[b] = "Begin"

print(d)  # {ResourceKey(raw=' MENU-START ', normalized='menu_start'): 'Begin'}
print(len(d))  # 1
