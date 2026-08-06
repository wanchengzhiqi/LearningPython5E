r"""
Function-local name classification and UnboundLocalError paths.

Run:
    python practice\P4_Functions_and_Generators\C17_Scopes\02_local_names_and_unboundlocalerror.py
"""


module_status = "global ready"


def read_module_status():
    return module_status


def read_then_rebind():
    before = module_status
    module_status = "local changed"
    return before, module_status


def read_branch_local(flag):
    if flag:
        branch_status = "branch ready"
    return branch_status


def transform_explicitly(status):
    before = status
    status = f"{status} -> local result"
    return before, status


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. Reading a module name works when the function does not bind it")
    predict("Does read_module_status() need a global declaration just to read?")
    print("read result ->", read_module_status())
    print("module binding ->", module_status)
    print("Rule: a read can fall through to the module global layer.")

    section("2. A later assignment classifies the name as local for the block")
    predict("Will the first line of read_then_rebind() read the module binding?")
    try:
        read_then_rebind()
    except UnboundLocalError as error:
        print("exception type ->", type(error).__name__)
    print("module binding unchanged ->", module_status)
    print(
        "Rule: the function's binding operation makes module_status local "
        "throughout that code block; the earlier read finds no local value."
    )

    section("3. A local name can be unbound on only some control-flow paths")
    predict("Does read_branch_local(False) have a value to return?")
    print("true path ->", read_branch_local(True))
    try:
        read_branch_local(False)
    except UnboundLocalError as error:
        print("false path exception ->", type(error).__name__)
    print("Rule: local classification and runtime binding state are distinct.")

    section("4. Explicit input and return avoid hidden cross-scope rebinding")
    predict("Which bindings change when transform_explicitly() is called?")
    original = "caller ready"
    before, after = transform_explicitly(original)
    print("before ->", before)
    print("after ->", after)
    print("caller binding unchanged ->", original)
    print(
        "Boundary: object mutability does not decide local classification; "
        "complete argument matching remains in C18."
    )


if __name__ == "__main__":
    main()
