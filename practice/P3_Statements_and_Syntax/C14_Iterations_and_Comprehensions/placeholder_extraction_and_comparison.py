#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by 天道酬勤 on 2026/7/10

from collections import Counter
from string import Formatter


_FORMATTER = Formatter()


def extract_placeholder_signatures(text):
    """
    提取 Python str.format 风格占位符签名。

    返回：
        (signatures, error_message)

    signatures 中每个元素为：
        (field_name, conversion, format_spec)
    """
    signatures = []

    try:
        for _, field_name, format_spec, conversion in _FORMATTER.parse(text):
            if field_name is None:
                continue

            signatures.append((
                field_name,
                conversion or "",
                format_spec or "",
            ))

    except ValueError as exc:
        return [], str(exc)

    return signatures, None


def format_placeholder_signature(signature):
    """把内部签名重新转换为便于报告展示的字符串。"""
    field_name, conversion, format_spec = signature

    result = "{" + field_name

    if conversion:
        result += f"!{conversion}"

    if format_spec:
        result += f":{format_spec}"

    return result + "}"


def compare_placeholders(source_text, target_text):
    source_signatures, source_error = extract_placeholder_signatures(
        source_text
    )
    target_signatures, target_error = extract_placeholder_signatures(
        target_text
    )

    result = {
        "source_parse_error": source_error,
        "target_parse_error": target_error,
        "source_placeholders": sorted(
            format_placeholder_signature(signature)
            for signature in source_signatures
        ),
        "target_placeholders": sorted(
            format_placeholder_signature(signature)
            for signature in target_signatures
        ),
        "missing_placeholders": [],
        "extra_placeholders": [],
        "matches": False,
    }

    if source_error is not None or target_error is not None:
        return result

    source_counts = Counter(source_signatures)
    target_counts = Counter(target_signatures)

    missing_signatures = source_counts - target_counts
    extra_signatures = target_counts - source_counts

    result["missing_placeholders"] = sorted(
        format_placeholder_signature(signature)
        for signature in missing_signatures.elements()
    )

    result["extra_placeholders"] = sorted(
        format_placeholder_signature(signature)
        for signature in extra_signatures.elements()
    )

    result["matches"] = (
        not result["missing_placeholders"]
        and not result["extra_placeholders"]
    )

    return result


print(compare_placeholders(
    "Welcome {player}",
    "欢迎 {player}",
))  # 正常匹配

print(compare_placeholders(
    "Welcome {player}",
    "欢迎 {name}",
))  # 改错了名字

print(compare_placeholders(
    "Score: {score:d}",
    "分数：{score}",
))  # 格式规格不同

print(compare_placeholders(
    "{player} attacks {player}",
    "{player} 发起攻击",
))  # 重复次数不同

print(compare_placeholders(
    "Literal: {{player}}",
    "字面内容：{{player}}",
))  # 转义花括号不是占位符
