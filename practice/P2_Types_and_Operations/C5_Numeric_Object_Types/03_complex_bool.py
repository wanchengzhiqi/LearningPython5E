"""
complex / bool: numeric objects that are easy to underestimate.

Run:
    python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\03_complex_bool.py
"""

import cmath


def show(title, value):
    print(f"{title:<34} -> {value!r} ({type(value).__name__})")


def predict(question):
    print(f"[Predict] {question}")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main():
    section("1. complex numbers have real and imaginary parts")
    predict("What do abs(z), z.real, z.imag, and z.conjugate() mean for z = 3 + 4j?")
    z = 3 + 4j
    show("z", z)
    show("z.real", z.real)
    show("z.imag", z.imag)
    show("abs(z)", abs(z))
    show("z.conjugate()", z.conjugate())
    show("cmath.phase(z)", cmath.phase(z))

    section("2. complex is useful for 2D rotation style thinking")
    predict("If 1 + 0j is a point on the x-axis, where does multiplying by 1j move it?")
    point = 1 + 0j
    rotate_90_degrees = 1j
    show("point", point)
    show("point * 1j", point * rotate_90_degrees)
    show("point * 1j * 1j", point * rotate_90_degrees * rotate_90_degrees)

    section("3. bool is a subclass of int, but has its own meaning")
    predict("Which values become False, and why is bool('False') True?")
    truth = True
    one = 1
    show("isinstance(True, int)", isinstance(True, int))
    show("True == 1", True == 1)
    show("truth is one", truth is one)
    show("True + True + False", True + True + False)
    show("bool(0)", bool(0))
    show("bool(1)", bool(1))
    show("bool('')", bool(""))
    show("bool('False')", bool("False"))
    show("bool([])", bool([]))
    show("bool([0])", bool([0]))

    section("4. Engineering caution")
    print("Use bool for truth decisions, not for hidden arithmetic tricks.")
    print("Example: sum(flags) is fine for counting True values, but document intent.")


if __name__ == "__main__":
    main()
