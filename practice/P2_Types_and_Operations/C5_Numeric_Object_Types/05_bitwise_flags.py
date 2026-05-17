"""
Bitwise operations: read, combine, remove, and toggle binary flags.

Run:
    python practice\P2_Types_and_Operations\C5_Numeric_Object_Types\05_bitwise_flags.py
"""


READ = 0b001
WRITE = 0b010
EXECUTE = 0b100


def bits(value):
    if value < 0:
        return f"{value:b}"
    return format(value, "03b")


def show(title, value):
    print(f"{title:<36} -> {value!r:<5} bits={bits(value)}")


def predict(question):
    print(f"[Predict] {question}")


def has_flag(flags, flag):
    return (flags & flag) == flag


def add_flag(flags, flag):
    return flags | flag


def remove_flag(flags, flag):
    return flags & ~flag


def toggle_flag(flags, flag):
    return flags ^ flag


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main():
    section("1. Define each permission as one bit")
    predict("Why should each flag use exactly one bit?")
    show("READ", READ)
    show("WRITE", WRITE)
    show("EXECUTE", EXECUTE)

    section("2. Combine flags with OR")
    predict("What bits are set after READ | WRITE?")
    user = READ | WRITE
    show("READ | WRITE", user)
    print("has READ:", has_flag(user, READ))
    print("has EXECUTE:", has_flag(user, EXECUTE))

    section("3. Add, remove, and toggle flags")
    predict("Which operator adds, removes, or toggles a single permission bit?")
    user = add_flag(user, EXECUTE)
    show("add EXECUTE", user)
    user = remove_flag(user, WRITE)
    show("remove WRITE", user)
    user = toggle_flag(user, EXECUTE)
    show("toggle EXECUTE", user)
    user = toggle_flag(user, EXECUTE)
    show("toggle EXECUTE again", user)

    section("4. Shifts move bit positions")
    predict("What happens when the single 1 bit shifts left or right?")
    show("1 << 0", 1 << 0)
    show("1 << 1", 1 << 1)
    show("1 << 2", 1 << 2)
    show("8 >> 1", 8 >> 1)

    section("5. Inversion is not limited to the visible three bits")
    predict("What is ~READ? Is it simply 0b110?")
    show("~READ", ~READ)
    show("~WRITE", ~WRITE)
    show("READ & ~READ", READ & ~READ)
    show("(READ | WRITE) & ~WRITE", (READ | WRITE) & ~WRITE)
    print("Rule: Python integers are not fixed-width here, so ~x == -x - 1.")
    print("For fixed-width display, mask after inversion, e.g. (~READ) & 0b111.")
    show("(~READ) & 0b111", (~READ) & 0b111)

    section("6. Engineering model")
    print("Flags compress many yes/no states into one int.")
    print("Use named constants so bit math remains readable.")


if __name__ == "__main__":
    main()
