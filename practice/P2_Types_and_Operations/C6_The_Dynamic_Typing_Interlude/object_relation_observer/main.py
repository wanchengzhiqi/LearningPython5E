"""Object relationship observer for dynamic typing practice."""

import copy

from observer import run_scenario


def scenario_shared_reference():
    a = [1, 2]
    b = a
    b.append(3)

    run_scenario(
        "1. Shared reference: b = a",
        """
a = [1, 2]
b = a
b.append(3)
        """,
        {"a": a, "b": b},
        "b = a does not copy the list. Both names bind to the same list object.",
    )


def scenario_shallow_copy():
    a = [[1], [2]]
    b = a.copy()
    b.append([3])
    b[0].append(99)

    run_scenario(
        "2. Shallow copy: list.copy()",
        """
a = [[1], [2]]
b = a.copy()
b.append([3])
b[0].append(99)
        """,
        {"a": a, "b": b},
        "The outer lists are different objects, but a[0] and b[0] still share one inner list.",
        nested=True,
    )


def scenario_deep_copy():
    a = [[1], [2]]
    b = copy.deepcopy(a)
    b[0].append(99)

    run_scenario(
        "3. Deep copy: copy.deepcopy()",
        """
import copy

a = [[1], [2]]
b = copy.deepcopy(a)
b[0].append(99)
        """,
        {"a": a, "b": b},
        "Deep copy creates a new outer list and recursively copies the inner lists.",
        nested=True,
    )


def scenario_mutable_in_place():
    a = ["python"]
    b = a
    b += ["typing"]

    run_scenario(
        "4. Mutable object: in-place operation",
        """
a = ["python"]
b = a
b += ["typing"]
        """,
        {"a": a, "b": b},
        "For lists, += usually mutates the existing list object in place.",
    )


def scenario_immutable_rebinding():
    a = "py"
    b = a
    b += "thon"

    run_scenario(
        "5. Immutable object: rebinding",
        """
a = "py"
b = a
b += "thon"
        """,
        {"a": a, "b": b},
        "Strings are immutable. b += 'thon' creates a new string and rebinds b.",
    )


def append_in_function(xs):
    xs.append(3)
    return xs


def rebind_in_function(xs):
    xs = [9, 9, 9]
    return xs


def clear_in_function(xs):
    xs.clear()
    return xs


def scenario_function_arguments():
    original_for_append = [1, 2]
    append_result = append_in_function(original_for_append)

    original_for_rebind = [1, 2]
    rebind_result = rebind_in_function(original_for_rebind)

    original_for_clear = [1, 2]
    clear_result = clear_in_function(original_for_clear)

    run_scenario(
        "6. Function arguments: mutation, rebinding and clear",
        """
def append_in_function(xs):
    xs.append(3)
    return xs

def rebind_in_function(xs):
    xs = [9, 9, 9]
    return xs

def clear_in_function(xs):
    xs.clear()
    return xs
        """,
        {
            "append input": original_for_append,
            "append result": append_result,
            "rebind input": original_for_rebind,
            "rebind result": rebind_result,
            "clear input": original_for_clear,
            "clear result": clear_result,
        },
        "Function parameters are local names bound to argument objects. Mutation affects the shared object; rebinding only changes the local name.",
    )


def add_item(x, items=[]):
    items.append(x)
    return items


def scenario_default_argument():
    first = add_item("first")
    second = add_item("second")
    defaults_list = add_item.__defaults__[0]

    run_scenario(
        "7. Default argument: shared list in __defaults__",
        """
def add_item(x, items=[]):
    items.append(x)
    return items

first = add_item("first")
second = add_item("second")
defaults_list = add_item.__defaults__[0]
        """,
        {
            "first": first,
            "second": second,
            "__defaults__[0]": defaults_list,
        },
        "The local name items disappears after each call, but the default list survives because the function object keeps it in __defaults__.",
    )


def main():
    scenario_shared_reference()
    scenario_shallow_copy()
    scenario_deep_copy()
    scenario_mutable_in_place()
    scenario_immutable_rebinding()
    scenario_function_arguments()
    scenario_default_argument()


if __name__ == "__main__":
    main()
