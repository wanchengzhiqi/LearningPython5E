"""
Decimal / Fraction: exact decimal intent and exact rational arithmetic.

Run:
    python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\02_decimal_fraction.py
"""

from decimal import Decimal, getcontext
from fractions import Fraction


def show(title, value):
    print(f"{title:<42} -> {value!r} ({type(value).__name__})")


def predict(question):
    print(f"[Predict] {question}")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main():
    section("1. Decimal expresses decimal arithmetic intent")
    predict("Will Decimal('0.1') + Decimal('0.2') equal Decimal('0.3') exactly?")
    show("Decimal('0.1') + Decimal('0.2')", Decimal("0.1") + Decimal("0.2"))
    show("Decimal('0.3')", Decimal("0.3"))
    show("Decimal('0.1') + Decimal('0.2') == Decimal('0.3')", Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

    section("2. Do not build Decimal from an already imprecise float casually")
    predict("Which one better preserves human decimal input: Decimal(0.1) or Decimal('0.1')?")
    show("Decimal(0.1)", Decimal(0.1))
    show("Decimal('0.1')", Decimal("0.1"))
    show("Decimal(str(0.1))", Decimal(str(0.1)))
    print("Rule: if the original input is text like money, keep it as text until Decimal parses it.")

    section("3. Decimal context controls precision for operations")
    predict("Does context precision change stored decimal literals or later arithmetic results?")
    old_prec = getcontext().prec
    try:
        getcontext().prec = 6
        show("Decimal(1) / Decimal(7)", Decimal(1) / Decimal(7))
        getcontext().prec = 28
        show("Decimal(1) / Decimal(7)", Decimal(1) / Decimal(7))
    finally:
        getcontext().prec = old_prec

    section("4. Fraction keeps rational relationships exact")
    predict("Why does Fraction(0.1) differ from Fraction('0.1')?")
    show("Fraction(1, 3) + Fraction(1, 6)", Fraction(1, 3) + Fraction(1, 6))
    show("Fraction('0.125')", Fraction("0.125"))
    show("Fraction(0.25)", Fraction(0.25))
    show("Fraction(0.1)", Fraction(0.1))
    show("Fraction('0.1')", Fraction("0.1"))
    show("Fraction(0.1).limit_denominator()", Fraction(0.1).limit_denominator())

    section("5. Engineering rule of thumb")
    print("money-like decimal input  -> Decimal from strings")
    print("ratio/proportion reasoning -> Fraction")
    print("measurement/simulation     -> float, with tolerance checks")


if __name__ == "__main__":
    main()
