#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/20

import inspect


def export(
    source,
    /,
    target,
    mode="json",
    *fields,
    encoding="utf-8",
    strict,
    **options,
):
    pass


if __name__ == '__main__':
    sig = inspect.signature(export)

    print("SIGNATURE:")
    print(sig)

    print("\nPARAMETERS:")

    for parameter in sig.parameters.values():
        has_default = (
            parameter.default is not inspect.Parameter.empty
        )

        print(
            f"{parameter.name:10}",
            f"kind={parameter.kind!s:30}",
            f"default={parameter.default!r}",
            f"has_default={has_default}",
        )
