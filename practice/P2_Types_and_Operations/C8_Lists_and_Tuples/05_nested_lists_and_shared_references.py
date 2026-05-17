"""
Nested lists, repeated references, and the default-argument sharing trap.

Run:
    python practice\P2_Types_and_Operations\C8_Lists_and_Tuples\05_nested_lists_and_shared_references.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_grid(name, grid):
    print(f"{name}: outer id={id(grid)} repr={grid!r}")
    for row_index, row in enumerate(grid):
        print(f"  row {row_index}: id={id(row)} repr={row!r}")


def collect_bad(key, bucket=[]):
    bucket.append(key)
    return bucket


def collect_good(key, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(key)
    return bucket


def main():
    section("1. Repetition repeats references when the element is mutable")
    predict("How many inner row lists does [[0] * 3] * 3 create?")
    bad_grid = [[0] * 3] * 3
    show_grid("bad_grid before", bad_grid)
    bad_grid[0][0] = 99
    show_grid("bad_grid after", bad_grid)
    print("bad_grid[0] is bad_grid[1] ->", bad_grid[0] is bad_grid[1])
    print("Rule: list repetition duplicates references, not nested objects.")

    section("2. A comprehension can create independent inner lists")
    predict("Will good_grid[0][0] = 99 affect row 1?")
    good_grid = [[0] * 3 for _ in range(3)]
    show_grid("good_grid before", good_grid)
    good_grid[0][0] = 99
    show_grid("good_grid after", good_grid)
    print("good_grid[0] is good_grid[1] ->", good_grid[0] is good_grid[1])
    print("Rule: the comprehension runs the inner expression separately each time.")

    section("3. Default list arguments are created when def runs")
    predict("Will collect_bad start from an empty list on every call?")
    first = collect_bad("menu.start")
    second = collect_bad("item.potion")
    print("first  ->", first, "id=", id(first))
    print("second ->", second, "id=", id(second))
    print("first is second ->", first is second)

    good_first = collect_good("menu.start")
    good_second = collect_good("item.potion")
    print("good_first  ->", good_first, "id=", id(good_first))
    print("good_second ->", good_second, "id=", id(good_second))
    print("good_first is good_second ->", good_first is good_second)
    print("Rule: use None as a sentinel when each call needs a fresh list.")

    section("4. Shared references are sometimes intentional")
    predict("When would sharing one list be a feature instead of a bug?")
    shared_log = []
    session_a = ["session-a", shared_log]
    session_b = ["session-b", shared_log]
    session_a[1].append("loaded menu.start")
    session_b[1].append("checked item.potion")
    print("session_a ->", session_a)
    print("session_b ->", session_b)
    print("session_a[1] is session_b[1] ->", session_a[1] is session_b[1])
    print("Rule: sharing is safe only when the contract says the object is shared.")


if __name__ == "__main__":
    main()
