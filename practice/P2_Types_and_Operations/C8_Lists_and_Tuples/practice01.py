#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/5/17


def show(label, a, b=None):
    print(f"\n{label}")
    print("a:", repr(a), "id(a) =", id(a))
    if b is not None:
        print("b:", repr(b), "id(b) =", id(b), "a is b =", a is b)


a = ["menu", "start"]
b = a
show("1. after b = a", a, b)

a.append("exit")
show("2. after a.append('exit')", a, b)

result = a.append("options")
show("3. after result = a.append('options')", a, b)
print("result:", result)

a = a + ["credits"]
show("4. after a = a + ['credits']", a, b)

a += ["load"]
show("5. after a += ['load']", a, b)

b[:] = ["new_game", "continue"]
show("6. after b[:] = [...]", a, b)

b = ["settings"]
show("7. after b = ['settings']", a, b)
