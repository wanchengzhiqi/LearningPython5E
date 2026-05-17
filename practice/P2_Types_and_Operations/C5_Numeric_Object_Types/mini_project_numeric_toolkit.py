"""
Mini project: numeric toolkit for conversion, money, ratios, flags, and text.

This file is a small stage-end practice result. It deliberately keeps the
functions plain so every part can be connected back to numeric object types.

Run:
    python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\mini_project_numeric_toolkit.py
"""

import math
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


READ = 1 << 0
WRITE = 1 << 1
EXECUTE = 1 << 2
REVIEW = 1 << 3
DELETE = 1 << 4

PERMISSIONS = {
    "read": READ,
    "write": WRITE,
    "execute": EXECUTE,
    "review": REVIEW,
    "delete": DELETE,
}


def fixed_width_bits(value, width=8):
    """Display the low `width` bits of an int, including negative ints."""
    mask = (1 << width) - 1
    return format(value & mask, f"0{width}b")


def describe_int(value, width=8):
    return {
        "decimal": value,
        "binary": bin(value),
        "octal": oct(value),
        "hex": hex(value),
        "bit_length": value.bit_length(),
        f"low_{width}_bits": fixed_width_bits(value, width),
    }


def parse_int(text, base=0):
    """Parse an integer literal-like string; base=0 accepts 0b/0o/0x prefixes."""
    return int(text, base)


def as_money_decimal(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError("money values should be str, int, or Decimal, not bool/float")
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, str):
        return Decimal(value)
    raise TypeError(f"unsupported money value: {value!r}")


def money_total(prices, unit=Decimal("0.01")):
    total = Decimal("0")
    for price in prices:
        total += as_money_decimal(price)
    return total.quantize(unit, rounding=ROUND_HALF_UP)


def completion_ratio(done, total):
    if total == 0:
        raise ValueError("total must not be zero")
    return Fraction(done, total)


def ratio_percent(ratio, unit=Decimal("0.01")):
    percent = Decimal(ratio.numerator) * Decimal("100") / Decimal(ratio.denominator)
    return percent.quantize(unit, rounding=ROUND_HALF_UP)


def rounding_report(value):
    return {
        "value": value,
        "repr": repr(value),
        "format_.2f": format(value, ".2f"),
        "round_2": round(value, 2),
        "floor": math.floor(value),
        "trunc": math.trunc(value),
        "int": int(value),
    }


def is_single_bit(permission):
    return isinstance(permission, int) and permission > 0 and permission & (permission - 1) == 0


def permission_names(flags):
    return [name for name, permission in PERMISSIONS.items() if flags & permission]


def permission_report(flags):
    return {
        "names": permission_names(flags),
        "has_read": has_all_permissions(flags, READ),
        "has_read_or_write": has_any_permissions(flags, READ | WRITE),
        "raw_flags": describe_int(flags, width=4),
    }


def has_any_permissions(flags, mask):
    return bool(flags & mask)


def has_all_permissions(flags, mask):
    return (flags & mask) == mask


def add_permission(flags, permission):
    if not is_single_bit(permission):
        raise ValueError(f"permission must be one non-overlapping bit: {permission!r}")
    return flags | permission


def remove_permission(flags, permission):
    return flags & ~permission


def toggle_permission(flags, permission):
    return flags ^ permission


def localization_key_report(source_keys, translated_keys):
    source = set(source_keys)
    translated = set(translated_keys)
    done = source & translated
    coverage = Fraction(1, 1) if not source else completion_ratio(len(done), len(source))
    return {
        "missing": sorted(source - translated),
        "extra": sorted(translated - source),
        "done": sorted(done),
        "coverage": coverage,
        "coverage_percent": ratio_percent(coverage),
    }


def character_report(text, encoding="utf-8"):
    encoded = text.encode(encoding)
    return {
        "text": text,
        "characters": len(text),
        "bytes": len(encoded),
        "code_points": [f"U+{ord(char):04X}" for char in text],
        "byte_values": list(encoded),
        "encoded_hex": encoded.hex(" "),
    }


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main():
    section("1. int literal parsing and display")
    value = parse_int("0x2d")
    print(describe_int(value))
    print("b'\\x2d'[0] is a byte value:", b"\x2d"[0])
    print("ord('-') is a Unicode code point:", ord("-"))

    section("2. float display, rounding, floor, and truncation")
    print(rounding_report(2.675))
    print(rounding_report(-2.675))

    section("3. money total with Decimal")
    print(money_total(["19.99", "5.50", "0.015"]))

    section("4. exact ratios with Fraction")
    ratio = completion_ratio(37, 128)
    print({"ratio": ratio, "percent": ratio_percent(ratio)})
    print({"Fraction(0.1)": Fraction(0.1), "limit_denominator": Fraction(0.1).limit_denominator()})

    section("5. permission flags")
    flags = READ | EXECUTE
    print(permission_report(flags))
    flags = add_permission(flags, REVIEW)
    print("after adding REVIEW:", permission_report(flags))
    flags = remove_permission(flags, EXECUTE)
    print("after removing EXECUTE:", permission_report(flags))
    print("toggle WRITE once:", permission_report(toggle_permission(flags, WRITE)))
    print("toggle DELETE once:", permission_report(toggle_permission(flags, DELETE)))
    print("toggle WRITE twice:", permission_report(toggle_permission(toggle_permission(flags, WRITE), WRITE)))
    print("~WRITE as Python int:", describe_int(~WRITE, width=4))

    section("6. localization key report")
    source_keys = ["menu.start", "menu.exit", "item.potion", "item.elixir"]
    translated_keys = ["menu.start", "item.potion", "unused.debug"]
    print(localization_key_report(source_keys, translated_keys))

    section("7. localization character report")
    print(character_report("HP药水"))
    print(character_report("Start"))


if __name__ == "__main__":
    main()
