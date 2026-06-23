"""C12-01: truth testing protocols."""

def section(title):
    print("\n" + "=" * 68)
    print(title)


class BoolProbe:
    def __init__(self, enabled):
        self.enabled = enabled
        self.calls = 0

    def __bool__(self):
        self.calls += 1
        print("  __bool__ call", self.calls)
        return self.enabled


class LenProbe:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        print("  __len__ called")
        return len(self.items)


class BothProtocols:
    def __bool__(self):
        print("  __bool__ wins")
        return False

    def __len__(self):
        raise AssertionError("__len__ must not run")


class BadBool:
    def __bool__(self):
        return 1


class BadLen:
    def __len__(self):
        return -1


def main():
    section("1. Built-in truth values")
    print("[Predict] Which objects are truthy?")
    samples = [
        ("zero", 0),
        ("positive", 7),
        ("empty text", ""),
        ("text '0'", "0"),
        ("empty list", []),
        ("list containing empty text", [""]),
        ("empty dict", {}),
        ("dict containing a key", {"menu.start": ""}),
        ("None", None),
    ]
    for label, value in samples:
        branch = "truthy" if value else "falsy"
        print(f"{label:<28} value={value!r:<24} bool={bool(value)!r:<5} {branch}")

    section("2. if value is not value == True")
    print("[Predict] Is a non-empty list equal to True?")
    value = ["menu.start"]
    print("bool(value) ->", bool(value))
    print("value == True ->", value == True)  # Deliberate comparison.
    if value:
        print("if value entered the truthy block")

    section("3. __bool__, __len__, and priority")
    print("[Predict] Which protocol is called?")
    print("bool(BoolProbe(True)) ->", bool(BoolProbe(True)))
    print("bool(LenProbe([])) ->", bool(LenProbe([])))
    print("bool(BothProtocols()) ->", bool(BothProtocols()))

    section("4. Protocol error boundaries")
    print("[Predict] Are integer 1 and length -1 valid results?")
    for label, probe in (("BadBool", BadBool()), ("BadLen", BadLen())):
        try:
            bool(probe)
        except (TypeError, ValueError) as exc:
            print(label, "->", type(exc).__name__, exc)


if __name__ == "__main__":
    main()
