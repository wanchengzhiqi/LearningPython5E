r"""
Definition, call, function-body, return, and caller timeline.

Run:
    python practice\P4_Functions_and_Generators\C16_Function_Basics\02_definition_call_and_return_timeline.py
"""


def normalize_key(key, timeline):
    timeline.append("body: entered")
    normalized = key.strip().lower()
    timeline.append(f"body: local normalized={normalized!r}")
    timeline.append("body: reaching return")
    return normalized


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. A definition exists before any call begins")
    predict("Does inspecting the function object execute normalize_key's body?")
    print("function type ->", type(normalize_key).__name__)
    print("function name ->", normalize_key.__name__)
    print("Observation: the call timeline has not been created yet.")

    section("2. A call enters the body and return hands an object back")
    predict("In what order will caller, body, return, and caller continuation occur?")
    timeline = ["caller: before call"]
    source = " MENU.Start "
    result = normalize_key(source, timeline)
    timeline.append("caller: after call")
    for event in timeline:
        print(event)
    print("source after call ->", source)
    print("returned result ->", result)
    print("Rule: the caller continues only after the call returns normally.")

    section("3. Call entry binds references rather than copying by default")
    predict("Why can the function append to the caller's timeline list?")
    print("timeline after call ->", timeline)
    print("timeline type ->", type(timeline).__name__)
    print(
        "Boundary: this observes a shared mutable object; complete argument "
        "matching belongs to C18."
    )

    section("4. Basic local state is part of this one call")
    predict("Is the local name normalized itself returned to the caller?")
    print("caller received object ->", result)
    print("caller binding name -> result")
    print(
        "Rule: return transfers an object reference; the caller chooses its own "
        "binding name."
    )


if __name__ == "__main__":
    main()
