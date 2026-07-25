#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/21

import json
from pathlib import Path
from pprint import pprint

from object_diagnostics import describe_object


samples = {
    "list_iterator": iter(
        ["start", "options", "quit"]
    ),
    "zip": zip(
        [1, 2],
        ["start", "quit"],
        strict=True,
    ),
    "dict_items": {
        "ui.start": "开始游戏",
        "ui.quit": "退出游戏",
    }.items(),
    "generator": (
        value.upper()
        for value in ["start", "quit"]
    ),
    "range": range(1, 6, 2),
    "enumerate": enumerate(
        ["start", "quit"],
        start=1,
    ),
    "map": map(
        str.upper,
        ["start", "quit"],
    ),
    "filter": filter(
        None,
        [
            "",
            "start",
            0,
            "quit",
        ],
    ),
}


reports = {
    label: describe_object(
        obj,
        name_limit=16,
        static_member_limit=6,
        include_help=False,
    )
    for label, obj in samples.items()
}


print("=== zip report ===")
pprint(
    reports["zip"],
    sort_dicts=False,
    width=100,
)


output_path = Path(
    "c15_object_reports.json"
)

output_text = json.dumps(
    reports,
    ensure_ascii=False,
    indent=2,
)

output_path.write_text(
    output_text,
    encoding="utf-8",
)

print()
print("saved:", output_path.resolve())
