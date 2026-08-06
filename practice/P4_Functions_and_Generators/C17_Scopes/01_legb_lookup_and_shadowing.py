r"""
LEGB name lookup and shadowing with deterministic observations.

Run:
    python practice\P4_Functions_and_Generators\C17_Scopes\01_legb_lookup_and_shadowing.py
"""

import builtins


scope_label = "global"


def read_global():
    return scope_label


def compare_local_and_enclosing():
    scope_label = "enclosing"

    def read_enclosing():
        return scope_label

    def read_local():
        scope_label = "local"
        return scope_label

    return read_local(), read_enclosing()


def read_builtin_length():
    return len(["menu.start", "menu.quit"])


def shadow_builtin_length():
    len = "local shadow"
    return len, builtins.len(["menu.start", "menu.quit"])


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. A bare name read uses the first matching LEGB binding")
    predict("Which binding does read_global() obtain?")
    print("module binding ->", scope_label)
    print("read_global() ->", read_global())
    print("Rule: this read reaches the global layer of this module.")

    section("2. Local and enclosing bindings can shadow outer layers")
    predict("Will the local and enclosing reads produce the same string?")
    local_value, enclosing_value = compare_local_and_enclosing()
    print("local read ->", local_value)
    print("enclosing read ->", enclosing_value)
    print("module binding after nested calls ->", scope_label)
    print("Rule: lookup stops at the first matching binding for that read.")

    section("3. Built-in lookup is the final LEGB fallback")
    predict("What happens when a local name shadows builtins.len?")
    local_len, real_length = shadow_builtin_length()
    print("ordinary built-in length ->", read_builtin_length())
    print("shadowed local len ->", local_len)
    print("explicit builtins.len result ->", real_length)
    print("Rule: shadowing changes which binding a bare name resolves to.")

    section("4. Lookup and binding are different questions")
    predict("Does LEGB alone explain where every assignment binds?")
    print("scope_label still global ->", scope_label == "global")
    print(
        "Boundary: LEGB describes bare-name reads; binding-target rules are "
        "examined separately in the next experiments."
    )


if __name__ == "__main__":
    main()
