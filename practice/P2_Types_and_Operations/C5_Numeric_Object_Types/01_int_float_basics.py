"""
int / float basics: literals, arithmetic, bases, and division.

Run:
    python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\01_int_float_basics.py
"""


def show(title, value):
    print(f"{title:<32} -> {value!r} ({type(value).__name__})")


def predict(question):
    print(f"[Predict] {question}")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main():
    section("1. int has arbitrary precision")
    predict("What type and how many decimal digits will 2 ** 100 have?")
    big = 2 ** 100
    show("2 ** 100", big)
    show("len(str(2 ** 100))", len(str(big)))
    show("big + 1", big + 1)

    section("2. base literals are different source forms for int objects")
    predict("Are 0b1010, 0o12, 0xA, and 10 different values or the same int value?")
    show("0b1010", 0b1010)
    show("0o12", 0o12)
    show("0xA", 0xA)
    show("int('1010', 2)", int("1010", 2))
    show("bin(10)", bin(10))
    show("oct(10)", oct(10))
    show("hex(10)", hex(10))

    section("3. division operators encode different intentions")
    predict("Before running, predict the result and type of /, //, %, and divmod().")
    show("5 / 2", 5 / 2)
    show("5 // 2", 5 // 2)
    show("5 % 2", 5 % 2)
    show("divmod(5, 2)", divmod(5, 2))
    show("-5 // 2", -5 // 2)
    show("-5 % 2", -5 % 2)
    print("Check: a == (a // b) * b + (a % b)")
    print(-5 == (-5 // 2) * 2 + (-5 % 2))
    show("divmod(-5, 2)", divmod(-5, 2))
    show("5 // -2", 5 // -2)
    show("5 % -2", 5 % -2)
    print("Rule: Python keeps a == (a // b) * b + (a % b), and // floors toward negative infinity.")

    section("4. float is binary approximate arithmetic")
    predict("Will 0.1 + 0.2 be exactly equal to 0.3?")
    show("0.1 + 0.2", 0.1 + 0.2)
    show("(0.1 + 0.2) == 0.3", (0.1 + 0.2) == 0.3)
    show("round(0.1 + 0.2, 10)", round(0.1 + 0.2, 10))
    show("abs((0.1 + 0.2) - 0.3)", abs((0.1 + 0.2) - 0.3))
    show("abs((0.1 + 0.2) - 0.3) < 1e-9", abs((0.1 + 0.2) - 0.3) < 1e-9)

    section("5. mixed arithmetic usually widens toward float")
    predict("Which operations stay int, and which widen to float?")
    show("3 + 2.0", 3 + 2.0)
    show("10 / 2", 10 / 2)
    show("10 // 2", 10 // 2)
    show("10 // 2.0", 10 // 2.0)
    print("Engineering note: use tolerance checks for float comparisons, not exact equality.")


if __name__ == "__main__":
    main()
