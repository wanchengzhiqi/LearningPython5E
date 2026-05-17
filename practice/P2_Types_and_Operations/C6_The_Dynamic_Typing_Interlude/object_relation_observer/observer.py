"""Helpers for observing Python object relationships.

This module is intentionally small and explicit. It is a learning aid for the
dynamic typing chapter, not a general-purpose debugger.
"""

from itertools import combinations


def print_section(title):
    line = "=" * len(title)
    print()
    print(line)
    print(title)
    print(line)


def print_code(code):
    print()
    print("[Code]")
    print(code.strip())


def print_conclusion(text):
    print()
    print("[Conclusion]")
    print(text.strip())


def describe_objects(names):
    """Print type, id and repr for a mapping of display names to objects."""
    print()
    print("[Objects]")
    print(f"{'name':<20} {'type':<18} {'id':<18} repr")
    print("-" * 78)
    for name, obj in names.items():
        type_name = type(obj).__name__
        print(f"{name:<20} {type_name:<18} {id(obj):<18} {repr(obj)}")


def compare_objects(names):
    """Print pairwise identity and equality relationships."""
    print()
    print("[Relations]")
    print(f"{'left':<20} {'right':<20} {'is':<8} {'==':<8}")
    print("-" * 60)
    for left, right in combinations(names, 2):
        left_obj = names[left]
        right_obj = names[right]
        print(f"{left:<20} {right:<20} {left_obj is right_obj!s:<8} {left_obj == right_obj!s:<8}")


def describe_nested(names, indexes=(0, 1)):
    """Print selected nested objects for containers that support indexing."""
    print()
    print("[Nested objects]")
    print(f"{'name[index]':<20} {'type':<18} {'id':<18} repr")
    print("-" * 78)
    for name, obj in names.items():
        for index in indexes:
            try:
                child = obj[index]
            except (IndexError, KeyError, TypeError):
                continue
            child_name = f"{name}[{index}]"
            print(f"{child_name:<20} {type(child).__name__:<18} {id(child):<18} {repr(child)}")


def run_scenario(title, code, names, conclusion, nested=False):
    print_section(title)
    print_code(code)
    describe_objects(names)
    compare_objects(names)
    if nested:
        describe_nested(names)
    print_conclusion(conclusion)
