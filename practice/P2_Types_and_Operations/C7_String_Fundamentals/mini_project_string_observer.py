"""
Mini project: string observer and localization text checker.

This is a stage-end practice tool for string fundamentals. It focuses on the
layers that often get mixed together:

    source literal -> str object -> display -> Unicode code points -> bytes

Run:
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\mini_project_string_observer.py
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\mini_project_string_observer.py "HP药水"
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\mini_project_string_observer.py --literal "'HP\nPotion'"
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\mini_project_string_observer.py --slice 1:-1:2 "Localization"
"""

import argparse
import ast
import string
import unicodedata
from collections import Counter


FORMATTER = string.Formatter()
PERCENT_CONVERSIONS = set("diouxXeEfFgGcrsa")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def character_name(char):
    try:
        return unicodedata.name(char)
    except ValueError:
        return "<no Unicode name>"


def observe_text(text, encoding="utf-8"):
    encoded = text.encode(encoding)
    return {
        "str": str(text),
        "repr": repr(text),
        "len_characters": len(text),
        "characters": [
            {
                "index": index,
                "char": char,
                "repr": repr(char),
                "code_point": f"U+{ord(char):04X}",
                "name": character_name(char),
            }
            for index, char in enumerate(text)
        ],
        "encoding": encoding,
        "byte_length": len(encoded),
        "byte_values": list(encoded),
        "hex": encoded.hex(" "),
    }


def print_observation(report):
    print("str()       :", report["str"])
    print("repr()      :", report["repr"])
    print("len(str)    :", report["len_characters"])
    print("encoding    :", report["encoding"])
    print("len(bytes)  :", report["byte_length"])
    print("bytes values:", report["byte_values"])
    print("bytes hex   :", report["hex"])
    print("characters  :")
    for item in report["characters"]:
        print(
            f"  [{item['index']}] {item['repr']:<8} "
            f"{item['code_point']:<10} {item['name']}"
        )


def parse_literal(literal_source):
    value = ast.literal_eval(literal_source)
    if not isinstance(value, str):
        raise TypeError(f"literal must produce str, got {type(value).__name__}")
    return value


def parse_slice_spec(spec):
    parts = spec.split(":")
    if len(parts) not in (2, 3):
        raise ValueError("slice spec must look like start:stop or start:stop:step")
    if len(parts) == 2:
        parts.append("")

    def parse_part(part):
        return None if part == "" else int(part)

    return slice(parse_part(parts[0]), parse_part(parts[1]), parse_part(parts[2]))


def slice_experiment(text, spec):
    current_slice = parse_slice_spec(spec)
    return {
        "text": text,
        "spec": spec,
        "normalized": current_slice.indices(len(text)),
        "result": text[current_slice],
    }


def method_experiment(text):
    return {
        "original": text,
        "strip": text.strip(),
        "upper": text.upper(),
        "casefold": text.casefold(),
        "replace_spaces": text.replace(" ", "_"),
        "split_spaces": text.split(),
        "join_characters": "|".join(text),
    }


def parse_format_placeholders(text):
    names = []
    errors = []

    def collect_fields(source):
        try:
            fields = FORMATTER.parse(source)
            for _, field_name, format_spec, _ in fields:
                if field_name is not None:
                    if field_name == "":
                        names.append("{}")
                    else:
                        names.append(field_name.split(".", 1)[0].split("[", 1)[0])
                if format_spec:
                    collect_fields(format_spec)
        except ValueError as error:
            errors.append(str(error))

    collect_fields(text)
    return names, errors


def format_placeholders(text):
    names, _ = parse_format_placeholders(text)
    return names


def percent_placeholders(text):
    placeholders = []
    index = 0
    while index < len(text):
        if text[index] != "%":
            index += 1
            continue

        start = index
        index += 1

        if index < len(text) and text[index] == "%":
            index += 1
            continue

        if index < len(text) and text[index] == "(":
            close_index = text.find(")", index + 1)
            if close_index == -1:
                index = start + 1
                continue
            index = close_index + 1

        while index < len(text) and text[index] in "#0- +":
            index += 1

        if index < len(text) and text[index] == "*":
            index += 1
        else:
            while index < len(text) and text[index].isdigit():
                index += 1

        if index < len(text) and text[index] == ".":
            index += 1
            if index < len(text) and text[index] == "*":
                index += 1
            else:
                while index < len(text) and text[index].isdigit():
                    index += 1

        if index < len(text) and text[index] in "hlL":
            index += 1

        if index < len(text) and text[index] in PERCENT_CONVERSIONS:
            placeholders.append(text[start : index + 1])
            index += 1
        else:
            index = start + 1

    return placeholders


def placeholder_counts(placeholders):
    return dict(sorted(Counter(placeholders).items()))


def placeholder_report(text):
    format_names, format_errors = parse_format_placeholders(text)
    return {
        "format_placeholders": format_names,
        "format_errors": format_errors,
        "percent_placeholders": percent_placeholders(text),
        "contains_newline": "\n" in text,
        "contains_literal_backslash_n": "\\n" in text,
    }


def compare_localization(source, translated):
    source_keys = set(source)
    translated_keys = set(translated)
    shared_keys = sorted(source_keys & translated_keys)
    placeholder_mismatches = []
    format_syntax_errors = []
    newline_mismatches = []

    for key in shared_keys:
        source_report = placeholder_report(source[key])
        translated_report = placeholder_report(translated[key])
        if source_report["format_errors"] or translated_report["format_errors"]:
            format_syntax_errors.append(
                {
                    "key": key,
                    "source": source_report["format_errors"],
                    "translated": translated_report["format_errors"],
                }
            )
        elif placeholder_counts(source_report["format_placeholders"]) != placeholder_counts(
            translated_report["format_placeholders"]
        ):
            placeholder_mismatches.append(
                {
                    "key": key,
                    "source": placeholder_counts(source_report["format_placeholders"]),
                    "translated": placeholder_counts(translated_report["format_placeholders"]),
                }
            )
        if source_report["percent_placeholders"] != translated_report["percent_placeholders"]:
            placeholder_mismatches.append(
                {
                    "key": key,
                    "source": source_report["percent_placeholders"],
                    "translated": translated_report["percent_placeholders"],
                }
            )
        if source_report["contains_newline"] != translated_report["contains_newline"]:
            newline_mismatches.append(key)

    return {
        "missing_keys": sorted(source_keys - translated_keys),
        "extra_keys": sorted(translated_keys - source_keys),
        "placeholder_mismatches": placeholder_mismatches,
        "format_syntax_errors": format_syntax_errors,
        "newline_mismatches": newline_mismatches,
    }


def print_mapping(title, mapping):
    print(title)
    for key, value in mapping.items():
        print(f"  {key}: {value!r}")


def run_demo(encoding):
    section("1. Observe a localization string")
    print_observation(observe_text("HP药水\nUse {count} now?", encoding))

    section("2. Escape experiment with a Python literal source")
    literal_source = "'Line 1\\nLine 2'"
    parsed = parse_literal(literal_source)
    print("literal source:", literal_source)
    print_observation(observe_text(parsed, encoding))

    section("3. Slice experiment")
    result = slice_experiment("Localization", "1:-1:2")
    print_mapping("slice report:", result)

    section("4. Method experiment")
    print_mapping("method report:", method_experiment("  HP Potion  "))

    section("5. Localization key and placeholder check")
    source = {
        "menu.start": "Start",
        "item.potion": "Potion x{count}",
        "dialog.warning": "Line 1\nLine 2",
        "system.percent": "Progress: %d%%",
    }
    translated = {
        "menu.start": "开始游戏",
        "item.potion": "药水 x{amount}",
        "dialog.warning": "第1行\\n第2行",
        "unused.debug": "调试",
        "system.percent": "进度：%s%%",
    }
    print_mapping("localization report:", compare_localization(source, translated))


def build_parser():
    parser = argparse.ArgumentParser(description="Observe Python strings and localization text.")
    parser.add_argument("text", nargs="*", help="Text to observe. Multiple words are joined with spaces.")
    parser.add_argument("--encoding", default="utf-8", help="Encoding used for byte observation.")
    parser.add_argument("--literal", help="Parse a Python string literal source, such as \"'HP\\nPotion'\".")
    parser.add_argument("--slice", dest="slice_spec", help="Run a slice experiment, e.g. 1:-1:2.")
    parser.add_argument("--methods", action="store_true", help="Show common method results for the text.")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.literal:
        text = parse_literal(args.literal)
    elif args.text:
        text = " ".join(args.text)
    else:
        run_demo(args.encoding)
        return

    section("String observation")
    print_observation(observe_text(text, args.encoding))

    if args.slice_spec:
        section("Slice experiment")
        print_mapping("slice report:", slice_experiment(text, args.slice_spec))

    if args.methods:
        section("Method experiment")
        print_mapping("method report:", method_experiment(text))


if __name__ == "__main__":
    main()
