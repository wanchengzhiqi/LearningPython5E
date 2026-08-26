import sys
print("PYTHON:", sys.version)
print("=" * 50)

seed = ["base"]


def make_default():
    print("MAKE")
    return seed


def record(
    item,
    records=make_default(),
    *,
    flags=[],
):
    records.append(item)
    flags.append(len(records))
    return records, flags


seed = ["replacement"]

a = record("A")
b = record("B")

print(a)
print(b)
print(record.__defaults__)
print(record.__kwdefaults__)
