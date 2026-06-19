#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/16
# C11-03: unpacking assignment

print("=== Experiment 1: basic unpacking ===")

a, b = 10, 20

print("a =", a)
print("b =", b)


print("\n=== Experiment 2: unpacking from list ===")

x, y, z = ["en", "ja", "zh"]

print("x =", x)
print("y =", y)
print("z =", z)


print("\n=== Experiment 3: unpacking from string ===")

c1, c2, c3 = "abc"

print("c1 =", c1)
print("c2 =", c2)
print("c3 =", c3)


print("\n=== Experiment 4: starred unpacking in the middle ===")

first, *middle, last = [1, 2, 3, 4, 5]

print("first =", first)
print("middle =", middle)
print("last =", last)


print("\n=== Experiment 5: starred target may be empty ===")

head, *body, tail = [10, 20]

print("head =", head)
print("body =", body)
print("tail =", tail)


print("\n=== Experiment 6: nested unpacking ===")

entry = ("menu.start", ("en", "Start"))

key, (lang, text) = entry

print("key =", key)
print("lang =", lang)
print("text =", text)


print("\n=== Experiment 7: ignoring value by convention ===")

key, _, text = ("menu.exit", "ja", "終了")

print("key =", key)
print("text =", text)
print("_ =", _)


print("\n=== Experiment 8: parsing localization key ===")

full_key = "settings.audio.volume"

section, *path = full_key.split(".")

print("section =", section)
print("path =", path)


print("\n=== Experiment 9: parsing CSV-like row ===")

row = ["menu.start", "en", "Start", "reviewed", "2026-06-16"]

key, lang, text, *meta = row

print("key =", key)
print("lang =", lang)
print("text =", text)
print("meta =", meta)


print("\n=== Experiment 10: function return and unpacking ===")


def split_key(key):
    return key.split(".", 1)


category, item = split_key("menu.start")

print("category =", category)
print("item =", item)
