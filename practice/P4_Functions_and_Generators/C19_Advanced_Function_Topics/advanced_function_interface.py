#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/9/11

from collections.abc import Callable


TextRule = Callable[[str], str]
StepObserver = Callable[[str, str], None]


def strip_text(text: str) -> str:
    return text.strip()


def remove_todo(text: str) -> str:
    return text.removeprefix("[TODO] ")


def require_nonempty(text: str) -> str:
    if not text:
        raise ValueError(
            "text must not be empty"
        )

    return text


def lower_text(text: str) -> str:
    return text.lower()


RULES: dict[str, TextRule] = {
    "strip": strip_text,
    "remove_todo": remove_todo,
    "require_nonempty": require_nonempty,
    "lower": lower_text,
}


def run_pipeline(
    text: str,
    rule_names: tuple[str, ...],
    *,
    on_step: StepObserver | None = None,
) -> str:
    current = text

    for name in rule_names:
        try:
            rule = RULES[name]
        except KeyError as exc:
            raise ValueError(
                f"unknown rule: {name}"
            ) from exc

        current = rule(current)

        if on_step is not None:
            on_step(name, current)

    return current


def make_counting_observer():
    count = 0

    def observe(
        name: str,
        text: str,
    ) -> None:
        nonlocal count

        count += 1

        print(
            f"#{count}",
            name,
            repr(text),
        )

    def read_count() -> int:
        return count

    return observe, read_count


observer, read_count = (
    make_counting_observer()
)


result = run_pipeline(
    "  [TODO] START GAME  ",
    (
        "strip",
        "remove_todo",
        "require_nonempty",
        "lower",
    ),
    on_step=observer,
)


print(
    "result:",
    repr(result),
)

print(
    "observed steps:",
    read_count(),
)
