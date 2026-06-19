#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/6/17
# C11-08: localization audit review
# Python 3.14.5

print("=== C11-08: Localization Audit Review ===")


print("\n=== Step 1: resource dictionaries ===")

en_resources = {
    "menu.start": "Start",
    "menu.exit": "Exit",
    "settings.audio": "Audio",
    "settings.video": "Video",
}

ja_resources = {
    "menu.start": "開始",
    "menu.exit": "終了",
    "settings.audio": "オーディオ",
    "dialogue.intro": "こんにちは",
}

print("EN resources:", en_resources)
print("JA resources:", ja_resources)


print("\n=== Step 2: key view set operations ===")

en_keys = en_resources.keys()
ja_keys = ja_resources.keys()

common_keys = en_keys & ja_keys
missing_in_ja = en_keys - ja_keys
extra_in_ja = ja_keys - en_keys

print("Common keys:", common_keys)
print("Missing in JA:", missing_in_ja)
print("Extra in JA:", extra_in_ja)


print("\n=== Step 3: unpacking assignment ===")

audit_title, source_lang, target_lang = "Localization Audit", "en", "ja"

print("audit_title:", audit_title)
print("source_lang:", source_lang)
print("target_lang:", target_lang)


print("\n=== Step 4: starred unpacking ===")

sample_key = "settings.audio.volume"

section, *path = sample_key.split(".")

print("section:", section)
print("path:", path)


print("\n=== Step 5: list assignment and += ===")

missing_keys = []
alias_missing_keys = missing_keys

missing_keys += list(missing_in_ja)

print("missing_keys:", missing_keys)
print("alias_missing_keys:", alias_missing_keys)
print("same object:", missing_keys is alias_missing_keys)


print("\n=== Step 6: list + creates a new list ===")

extra_keys = []
alias_extra_keys = extra_keys

extra_keys = extra_keys + list(extra_in_ja)

print("extra_keys:", extra_keys)
print("alias_extra_keys:", alias_extra_keys)
print("same object:", extra_keys is alias_extra_keys)


print("\n=== Step 7: subscript assignment ===")

stats = {
    "common": 0,
    "missing_in_ja": 0,
    "extra_in_ja": 0,
}

stats["common"] = len(common_keys)
stats["missing_in_ja"] = len(missing_in_ja)
stats["extra_in_ja"] = len(extra_in_ja)

print("stats:", stats)


print("\n=== Step 8: augmented assignment on dictionary values ===")

stats["missing_in_ja"] += 1
stats["missing_in_ja"] -= 1

print("stats after += and -=:", stats)


print("\n=== Step 9: slice assignment ===")

report_lines = [
    "Localization audit report",
    "=========================",
    "Common keys:",
    str(common_keys),
    "Missing in JA:",
    str(missing_in_ja),
]

report_lines[4:6] = [
    "Missing in JA:",
    repr(missing_in_ja),
    "Extra in JA:",
    repr(extra_in_ja),
]

print("report_lines:", report_lines)


print("\n=== Step 10: print to file ===")

with open("c11_08_audit_report.txt", "w", encoding="utf-8") as f:
    print(audit_title, file=f)
    print("=" * len(audit_title), file=f)
    print("Source language:", source_lang, file=f)
    print("Target language:", target_lang, file=f)
    print("Stats:", stats, file=f)
    print("Common keys:", repr(common_keys), file=f)
    print("Missing in JA:", repr(missing_in_ja), file=f)
    print("Extra in JA:", repr(extra_in_ja), file=f)

print("Report written: c11_08_audit_report.txt")


print("\n=== Step 11: print return value ===")

result = print("This line is printed by print().")
print("print() returned:", result)
