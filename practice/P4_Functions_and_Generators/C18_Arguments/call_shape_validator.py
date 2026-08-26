#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/8/20

from practice.P4_Functions_and_Generators.C18_Arguments.signature_auditor import export


def audit_call(func, /, *args, **kwargs):
    import inspect

    signature = inspect.signature(func)

    try:
        bound = signature.bind(*args, **kwargs)
    except TypeError as exc:
        return {
            "bindable": False,
            "error": str(exc),
        }

    bound.apply_defaults()

    return {
        "bindable": True,
        "bindings": dict(bound.arguments),
    }


print(
    audit_call(
        export,
        "source.csv",
        "target.json",
        strict=True,
    )
)
