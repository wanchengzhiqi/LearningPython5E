#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/10/9

events = []

records = [
    {"key": "menu.start", "text": " 开始 "},
    {"key": "menu.start", "text": " 启动 "},
    {"key": "menu.quit", "text": " 退出 "},
    {"key": "menu.bad", "text": None},
    {"key": "menu.after", "text": " 后续 "},
]


def normalize(source, events, owner):
    events.append(("start", owner))

    for record in source:
        key = record["key"]
        events.append(("read", owner, key))

        raw = record["text"]

        if not isinstance(raw, str):
            events.append(("error", owner, key))
            raise TypeError("text must be str")

        text = raw.strip()

        events.append(("yield", owner, key, text))
        yield key, text

    events.append(("end", owner))


source = iter(records)

g_a = normalize(source, events, "A")
g_b = normalize(source, events, "B")

# T0：两个生成器已经创建
print("T0:", events)
print("identity:", g_a is g_b, iter(source) is source)

# T1：交错推进
first_a = next(g_a)
first_b = next(g_b)

mapping = {
    key: text
    for key, text in (first_a, first_b)
}

print("T1:", first_a, first_b)
print("mapping:", mapping)

# T2：尝试完整消费 A 的剩余部分
try:
    tail_a = list(g_a)
except TypeError as exc:
    error_type = type(exc).__name__

checkpoint = events.copy()

print("T2:", error_type)
print("checkpoint:", checkpoint)

# T3：A 已经异常终止，但 B 尚未结束
next_b = next(g_b)
rest_b = list(g_b)

print("T3:", next_b, rest_b)
print("A after error:", next(g_a, "END"))
print("final events:", events)
