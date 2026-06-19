#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/16
# C11-04: attribute, subscript, and slice assignment

print("=== Experiment 1: name rebinding ===")

a = [1, 2, 3]
b = a

a = [4, 5, 6]

print("a =", a)
print("b =", b)


print("\n=== Experiment 2: subscript assignment ===")

items = ["en", "ja", "zh"]
alias = items

items[1] = "jp"

print("items =", items)
print("alias =", alias)
print("items is alias:", items is alias)


print("\n=== Experiment 3: dictionary subscript assignment ===")

texts = {}

texts["menu.start"] = "Start"
texts["menu.exit"] = "Exit"
texts["menu.start"] = "Begin"

print("texts =", texts)


print("\n=== Experiment 4: string does not support item assignment ===")

s = "hello"

# Uncomment this line to see the error:
# s[0] = "H"

s = "H" + s[1:]

print("s =", s)


print("\n=== Experiment 5: attribute assignment ===")


class Player:
    pass


player = Player()
same_player = player

player.name = "Alice"
player.level = 10

print("player.name =", player.name)
print("same_player.name =", same_player.name)
print("player is same_player:", player is same_player)


print("\n=== Experiment 6: slice assignment with same length ===")

keys = ["a", "b", "c", "d"]

keys[1:3] = ["X", "Y"]

print("keys =", keys)


print("\n=== Experiment 7: slice assignment with shorter replacement ===")

keys = ["a", "b", "c", "d"]

keys[1:3] = ["X"]

print("keys =", keys)


print("\n=== Experiment 8: slice assignment with longer replacement ===")

keys = ["a", "b", "c", "d"]

keys[1:3] = ["X", "Y", "Z"]

print("keys =", keys)


print("\n=== Experiment 9: insertion by slice assignment ===")

keys = ["menu.start", "menu.exit"]

keys[1:1] = ["settings.audio", "settings.video"]

print("keys =", keys)


print("\n=== Experiment 10: subscript assignment vs slice assignment ===")

items = [1, 2, 3]
items[1] = ["a", "b"]

print("subscript result =", items)

items = [1, 2, 3]
items[1:2] = ["a", "b"]

print("slice result =", items)
