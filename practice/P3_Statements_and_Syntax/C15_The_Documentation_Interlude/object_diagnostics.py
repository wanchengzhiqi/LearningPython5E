#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/21

import inspect
import reprlib
import sys
from contextlib import redirect_stdout
from io import StringIO


_LIMITED_REPR = reprlib.Repr(
    maxlevel=4,
    maxtuple=8,
    maxlist=8,
    maxdict=6,
    maxset=8,
    maxfrozenset=8,
    maxstring=120,
    maxlong=80,
    maxother=120,
)


def capture(operation):
    """Run one diagnostic operation and record success or failure."""

    try:
        value = operation()
    except Exception as exc:
        return {
            "status": "error",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }

    return {
        "status": "ok",
        "value": value,
    }


def qualified_type_name(obj):
    """Return a module-qualified runtime type name."""

    cls = type(obj)

    return f"{cls.__module__}.{cls.__qualname__}"


def truncate_text(text, limit):
    """Limit a text field without silently hiding truncation."""

    if len(text) <= limit:
        return text

    omitted = len(text) - limit

    return (
        text[:limit]
        + f"... <{omitted} characters omitted>"
    )


def limited_object_repr(obj):
    """Return a size-limited representation of an object."""

    return _LIMITED_REPR.repr(obj)


def summarize_documentation(obj, max_chars=300):
    """Return the first cleaned documentation paragraph."""

    doc = inspect.getdoc(obj)

    if doc is None:
        return None

    first_paragraph = doc.split("\n\n", 1)[0]

    summary = " ".join(
        line.strip()
        for line in first_paragraph.splitlines()
        if line.strip()
    )

    return truncate_text(
        summary,
        max_chars,
    )


def capture_help_information(obj, max_chars=3000):
    """Capture help(obj) output and its separate return value."""

    buffer = StringIO()

    with redirect_stdout(buffer):
        result = help(obj)

    text = buffer.getvalue()

    return {
        "return_value_repr": limited_object_repr(result),
        "text": truncate_text(
            text,
            max_chars,
        ),
        "original_text_length": len(text),
    }


def describe_object(
    obj,
    *,
    include_private=False,
    name_limit=20,
    static_member_limit=8,
    include_help=False,
    help_limit=3000,
):
    """Return a structured diagnostic report for one object.

    This report is a discovery aid, not a declaration of the
    object's complete or public API.
    """

    if not isinstance(name_limit, int):
        raise TypeError("name_limit must be int")

    if name_limit < 0:
        raise ValueError(
            "name_limit must be non-negative"
        )

    if not isinstance(static_member_limit, int):
        raise TypeError(
            "static_member_limit must be int"
        )

    if static_member_limit < 0:
        raise ValueError(
            "static_member_limit must be non-negative"
        )

    report = {
        "environment": {
            "python_version": sys.version,
            "executable": sys.executable,
            "implementation": sys.implementation.name,
        },
        "object": {
            "type": qualified_type_name(obj),
            "callable": callable(obj),
        },
    }

    report["object"]["repr"] = capture(
        lambda: limited_object_repr(obj)
    )

    report["documentation"] = capture(
        lambda: summarize_documentation(obj)
    )

    if callable(obj):
        report["signature"] = capture(
            lambda: str(
                inspect.signature(obj)
            )
        )
    else:
        report["signature"] = {
            "status": "not_applicable",
            "reason": "object is not callable",
        }

    try:
        all_names = dir(obj)
    except Exception as exc:
        report["candidate_names"] = {
            "status": "error",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }

        shown_names = []
    else:
        if include_private:
            filtered_names = all_names
        else:
            filtered_names = [
                name
                for name in all_names
                if not name.startswith("_")
            ]

        shown_names = filtered_names[:name_limit]

        report["candidate_names"] = {
            "status": "ok",
            "reported_count": len(all_names),
            "filtered_count": len(filtered_names),
            "shown": shown_names,
            "truncated": (
                len(filtered_names)
                > len(shown_names)
            ),
        }

    static_members = []

    for name in shown_names[:static_member_limit]:
        try:
            stored_value = inspect.getattr_static(
                obj,
                name,
            )
        except Exception as exc:
            static_members.append(
                {
                    "name": name,
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                }
            )
        else:
            static_members.append(
                {
                    "name": name,
                    "status": "ok",
                    "stored_type": (
                        qualified_type_name(
                            stored_value
                        )
                    ),
                    "stored_repr": capture(
                        lambda value=stored_value: (
                            limited_object_repr(value)
                        )
                    ),
                }
            )

    report["static_members"] = static_members

    if include_help:
        report["help"] = capture(
            lambda: capture_help_information(
                obj,
                max_chars=help_limit,
            )
        )
    else:
        report["help"] = {
            "status": "skipped",
            "reason": "include_help is False",
        }

    return report
