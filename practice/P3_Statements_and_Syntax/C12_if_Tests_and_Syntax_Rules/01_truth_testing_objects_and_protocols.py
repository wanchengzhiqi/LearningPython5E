r"""
Truth testing for built-in objects and custom protocol objects.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\01_truth_testing_objects_and_protocols.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


class BoolProbe:
    def __init__(self, label, result):
        self.label = label
        self.result = result
        self.calls = 0

    def __bool__(self):
        self.calls += 1
        print(f"  {self.label}.__bool__() call #{self.calls}")
        return self.result


class LenProbe:
    def __init__(self, label, length):
        self.label = label
        self.length = length
        self.calls = 0

    def __len__(self):
        self.calls += 1
        print(f"  {self.label}.__len__() call #{self.calls}")
        return self.length


class BothProtocols:
    def __bool__(self):
        print("  BothProtocols.__bool__() was selected")
        return False

    def __len__(self):
        raise AssertionError("__len__() must not run when __bool__() exists")


class BadBool:
    def __bool__(self):
        return 1


class BadLen:
    def __len__(self):
        return -1


class DefaultTruthy:
    pass


def main():
    section("1. Built-in objects participate in truth testing")
    predict("Which objects are falsy, and which non-empty objects are truthy?")
    samples = [
        ("integer zero", 0),
        ("nonzero integer", -3),
        ("empty string", ""),
        ("string containing zero", "0"),
        ("empty list", []),
        ("list containing empty string", [""]),
        ("empty dict", {}),
        ("dict with an empty value", {"menu.start": ""}),
        ("None", None),
    ]
    for label, value in samples:
        branch = "truthy branch" if value else "falsy branch"
        print(
            f"{label:<28} value={value!r:<24} "
            f"bool(value)={bool(value)!r:<5} -> {branch}"
        )

    section("2. if value is not shorthand for if value == True")
    predict("Can a non-empty list be truthy without being equal to True?")
    value = ["menu.start"]
    print("bool(value) ->", bool(value))
    print("value == True ->", value == True)  # Deliberate contrast for teaching.
    if value:
        print("if value entered the block")
    if value == True:  # Deliberate contrast for teaching.
        print("if value == True entered the block")
    else:
        print("if value == True did not enter the block")
    print("Rule: if asks for truth testing; == asks for equality first.")

    section("3. __bool__ has priority; __len__ is the fallback protocol")
    predict("Which special method will each object call?")
    enabled = BoolProbe("enabled", True)
    empty_batch = LenProbe("empty_batch", 0)
    nonempty_batch = LenProbe("nonempty_batch", 2)
    print("bool(enabled) ->", bool(enabled))
    print("bool(empty_batch) ->", bool(empty_batch))
    print("bool(nonempty_batch) ->", bool(nonempty_batch))
    print("bool(BothProtocols()) ->", bool(BothProtocols()))

    section("4. Objects without either protocol are truthy by default")
    predict("What is bool(DefaultTruthy())?")
    print("bool(DefaultTruthy()) ->", bool(DefaultTruthy()))

    section("5. Truth protocols have strict result boundaries")
    predict("May __bool__ return integer 1, or may __len__ return -1?")
    for label, probe in (("BadBool", BadBool()), ("BadLen", BadLen())):
        try:
            print(label, "->", bool(probe))
        except (TypeError, ValueError) as exc:
            print(label, "raised", type(exc).__name__, "->", exc)

    print()
    print("Summary: the object and its truth-test result are different layers.")


if __name__ == "__main__":
    main()
