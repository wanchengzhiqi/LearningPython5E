#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/28


def strip_text(text):
    print("strip_text")
    return text.strip()


def normalize_spaces(text):
    print("normalize_spaces")
    return " ".join(text.split())


def upper_text(text):
    print("upper_text")
    return text.upper()


PIPELINES = {
    "clean": [
        strip_text,
        normalize_spaces,
    ],
    "shout": [
        strip_text,
        normalize_spaces,
        upper_text,
    ],
}


def run_pipeline(text, steps):
    print("pipeline: begin")

    for step in steps:
        print("step:", step.__name__)
        text = step(text)

    print("pipeline: end")
    return text


def transform(text, mode):
    steps = PIPELINES[mode]
    return run_pipeline(text, steps)


result = transform(
    "   Save     Game   ",
    "shout",
)

print("result:", result)
