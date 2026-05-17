"""
Deep dive: percent formatting vs str.format() vs f-strings.

Run:
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\06_formatting_styles_deep_dive.py

This script is a comparison lab. It intentionally shows both normal usage and
failure cases so that the boundary between "template text", "Python source",
and "formatted str result" stays visible.
"""

from pathlib import Path
import json
import string


FORMATTER = string.Formatter()
HERE = Path(__file__).resolve().parent
LOCALIZATION_SAMPLE = HERE / "formatting_localization_samples.json"
TEMPLATE_SAMPLE = HERE / "formatting_templates.txt"


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(title, value):
    print(f"{title:<42} -> {value!r} ({type(value).__name__})")


def show_call(title, func):
    try:
        value = func()
    except Exception as exc:
        print(f"{title:<42} -> {type(exc).__name__}: {exc}")
    else:
        show(title, value)


def format_placeholders(text):
    names = []
    try:
        for _, field_name, format_spec, _ in FORMATTER.parse(text):
            if field_name is not None:
                names.append("{}" if field_name == "" else field_name.split(".", 1)[0].split("[", 1)[0])
            if format_spec:
                names.extend(format_placeholders(format_spec))
    except ValueError as exc:
        names.append(f"<format error: {exc}>")
    return names


def percent_placeholders(text):
    conversions = set("diouxXeEfFgGcrsa")
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

        if index < len(text) and text[index] in conversions:
            placeholders.append(text[start : index + 1])
            index += 1
        else:
            index = start + 1

    return placeholders


def load_localization_samples():
    with LOCALIZATION_SAMPLE.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_template_samples():
    samples = []
    with TEMPLATE_SAMPLE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            style, name, template = line.split("|", 2)
            samples.append({"style": style, "name": name, "template": template})
    return samples


def main():
    section("1. Same simple result, three different mechanisms")
    predict("Do all three expressions create str results? Do they modify source values?")
    item = "Potion"
    count = 7
    show("% expression", "%s x%02d" % (item, count))
    show("format() method", "{} x{:02d}".format(item, count))
    show("f-string", f"{item} x{count:02d}")
    show("item after formatting", item)
    show("count after formatting", count)

    section("2. Positional, named, and mapping-style placeholders")
    predict("Which style is easiest to keep stable in localization templates?")
    context = {"player": "Alex", "count": 3, "item": "Potion"}
    show("% tuple", "%s found %d %s(s)" % (context["player"], context["count"], context["item"]))
    show("% mapping", "%(player)s found %(count)d %(item)s(s)" % context)
    show("format positional", "{0} found {1} {2}(s)".format(context["player"], context["count"], context["item"]))
    show("format named", "{player} found {count} {item}(s)".format(**context))
    show("f-string named variables", f"{context['player']} found {context['count']} {context['item']}(s)")
    print("Rule: runtime localization templates usually prefer named placeholders.")

    section("3. Conversion: str-style display vs repr-style debugging")
    predict("Which outputs expose the hidden newline?")
    text = "Line 1\nLine 2"
    show("%s", "text=%s" % text)
    show("%r", "text=%r" % text)
    show("format default", "text={}".format(text))
    show("format !r", "text={!r}".format(text))
    show("f-string default", f"text={text}")
    show("f-string !r", f"text={text!r}")
    show("f-string debug =", f"{text=}")
    print("Direct print with str-style formatting:")
    print("text=%s" % text)
    print("Direct print with repr-style formatting:")
    print("text=%r" % text)

    section("4. Width, alignment, precision, and numeric bases")
    predict("Which parts are formatting display only, and which values are changed?")
    number = 255
    price = 12.5
    label = "HP"
    show("% width", "|%-8s|%08d|%.2f|" % (label, number, price))
    show("format width", "|{:<8}|{:08d}|{:.2f}|".format(label, number, price))
    show("f-string width", f"|{label:<8}|{number:08d}|{price:.2f}|")
    show("format binary/hex", "bin={:08b} hex={:04X}".format(number, number))
    show("f-string binary/hex", f"bin={number:08b} hex={number:04X}")
    show("number after formatting", number)
    show("price after formatting", price)

    section("5. Literal percent signs and literal braces")
    predict("Which characters must be escaped in each style?")
    progress = 80
    show("% literal percent", "Progress: %d%%" % progress)
    show("format literal braces", "Use {{key}} or actual {key}".format(key="Enter"))
    show("f-string literal braces", f"Use {{key}} or actual {'Enter'}")
    show_call("% missing escape", lambda: "Progress: %d%" % progress)
    show_call("format bad brace", lambda: "Press {key".format(key="Enter"))

    section("6. Runtime templates from sample file")
    predict("Can f-strings format templates loaded from files without eval?")
    samples = load_template_samples()
    data = {"key": "Enter", "count": 80, "name": "Alex"}
    for sample in samples:
        template = sample["template"]
        style = sample["style"]
        title = f"{sample['name']} [{style}]"
        if style == "format":
            show(title, template.format(**data))
        elif style == "percent":
            show(title, template % data)
        else:
            show(title, template)
    runtime_template = "Press {key} to start"
    show("f'{runtime_template}'", f"{runtime_template}")
    show("runtime_template.format(...)", runtime_template.format(**data))
    print("Rule: f-strings are parsed from Python source, not from strings loaded at runtime.")

    section("7. Failure cases are part of the API contract")
    predict("Which mistakes fail immediately, and why is that useful?")
    show_call("% too few args", lambda: "%s %s" % ("only-one",))
    show_call("% wrong numeric type", lambda: "%d" % "not-a-number")
    show_call("format missing key", lambda: "{player} has {count}".format(player="Alex"))
    show_call("format mixed numbering", lambda: "{} {0}".format("a", "b"))
    show_call("format invalid spec", lambda: "{:not_a_spec}".format(123))

    section("8. Localization placeholder checks from JSON")
    predict("Which translated strings should be reported, and which reorder is legal?")
    samples = load_localization_samples()
    for entry in samples["format_templates"]:
        source_names = format_placeholders(entry["source"])
        translated_names = format_placeholders(entry["translated"])
        show(entry["id"] + " source fields", source_names)
        show(entry["id"] + " translated fields", translated_names)
        print("same placeholder multiset ->", sorted(source_names) == sorted(translated_names))
    for entry in samples["percent_templates"]:
        source_slots = percent_placeholders(entry["source"])
        translated_slots = percent_placeholders(entry["translated"])
        show(entry["id"] + " source slots", source_slots)
        show(entry["id"] + " translated slots", translated_slots)
        print("same percent slots ->", source_slots == translated_slots)

    section("9. Engineering rules of thumb")
    print("1. Use f-strings for local, readable Python-source formatting.")
    print("2. Use format() for runtime templates, especially localization text.")
    print("3. Read old '%' formatting; keep it in logging calls and legacy code.")
    print("4. Use !r or %r when debugging invisible characters.")
    print("5. Never eval an untrusted string just to simulate an f-string.")


if __name__ == "__main__":
    main()
