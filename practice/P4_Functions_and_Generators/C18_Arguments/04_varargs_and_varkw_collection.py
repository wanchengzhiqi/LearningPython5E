r"""
Definition-side *args and **kwargs collection with shallow object boundaries.

Run:
    python practice\P4_Functions_and_Generators\C18_Arguments\04_varargs_and_varkw_collection.py
"""


def collect_audit_inputs(primary_key, *extra_keys, **controls):
    return {
        "primary_key": primary_key,
        "extra_keys": extra_keys,
        "controls": controls,
    }


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Definition-side *extra_keys collects surplus positional inputs")
    predict("Which object type stores the extra localization keys?")
    channels = ["menu"]
    collected = collect_audit_inputs(
        "menu.start",
        "menu.quit",
        "dialog.ok",
        locale="ja-JP",
        channels=channels,
    )
    print("primary key ->", collected["primary_key"])
    print("extra keys ->", collected["extra_keys"])
    print("extra keys type ->", type(collected["extra_keys"]).__name__)
    print("Rule: surplus positional arguments are collected into a tuple.")

    section("2. Definition-side **controls collects surplus keyword inputs")
    predict("Which object type stores the named control inputs?")
    print("controls ->", collected["controls"])
    print("controls type ->", type(collected["controls"]).__name__)
    print("selected locale ->", collected["controls"]["locale"])
    print("Rule: surplus keyword arguments are collected into a new dictionary.")

    section("3. The collection containers do not deep-copy their values")
    predict("Does collecting channels isolate the nested list object?")
    print("nested channels is caller object ->", collected["controls"]["channels"] is channels)
    collected["controls"]["channels"].append("dialog")
    print("caller channels after nested mutation ->", channels)
    another = collect_audit_inputs("settings.audio")
    print("controls dictionaries are distinct ->", collected["controls"] is not another["controls"])
    print(
        "Rule: each call establishes collection-parameter bindings; the "
        "argument objects stored inside them are not automatically copied."
    )

    section("4. Empty collections still have tuple and dictionary shapes")
    predict("What is collected when there are no surplus arguments?")
    print("empty extra keys ->", another["extra_keys"])
    print("empty controls ->", another["controls"])
    print(
        "Boundary: these values show tuple/dict shapes, not a guarantee about "
        "tuple identity across calls. Call-side unpacking is separate."
    )


if __name__ == "__main__":
    main()
