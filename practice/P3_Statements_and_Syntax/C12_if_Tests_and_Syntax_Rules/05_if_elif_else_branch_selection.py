r"""
if/elif/else branch selection, independent if statements, and block syntax.

Run:
    python practice\P3_Statements_and_Syntax\C12_if_Tests_and_Syntax_Rules\05_if_elif_else_branch_selection.py
"""

TRACE = []


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def condition(label, value):
    TRACE.append(f"condition:{label}")
    print(f"  condition {label!r} produced {value!r}")
    return value


def block(label):
    TRACE.append(f"block:{label}")
    print(f"  entered block {label!r}")


def independent_checks(severity):
    hits = []
    if severity >= 40:
        hits.append("warning")
    if severity >= 80:
        hits.append("critical")
    return hits


def exclusive_level(severity):
    if severity >= 80:
        return "critical"
    elif severity >= 40:
        return "warning"
    else:
        return "info"


def show_compile_result(label, source):
    try:
        compile(source, f"<{label}>", "exec")
    except SyntaxError as exc:
        print(f"{label:<18} -> {type(exc).__name__}: {exc.msg}")
    else:
        print(f"{label:<18} -> valid syntax")


def main():
    section("1. A condition expression is evaluated before its truth test")
    predict("Which condition and block events will be recorded?")
    TRACE.clear()
    if condition("missing_keys", ["menu.quit"]):
        block("report missing keys")
    else:
        block("clean report")
    print("trace ->", TRACE)

    section("2. Only the first matching if/elif/else branch runs")
    predict("Will the second condition expression be evaluated?")
    TRACE.clear()
    if condition("first", True):
        block("first")
    elif condition("second", True):
        block("second")
    else:
        block("else")
    print("trace ->", TRACE)
    print("Rule: a matched branch prevents later elif tests from being evaluated.")

    section("3. Multiple independent if statements are not an elif chain")
    predict("For severity 90, how many labels will each design produce?")
    print("independent_checks(90) ->", independent_checks(90))
    print("exclusive_level(90) ->", exclusive_level(90))
    print("Use independent if statements for cumulative rules; use elif for one choice.")

    section("4. No entered block means no block side effect")
    predict("Will block('write report') run?")
    TRACE.clear()
    if condition("dry_run is False", False):
        block("write report")
    print("trace ->", TRACE)

    section("5. Colons and indentation are syntax, not decoration")
    predict("Which source snippets compile?")
    valid_source = (
        "if True:\n"
        "    result = 'ok'\n"
    )
    missing_colon = (
        "if True\n"
        "    result = 'bad'\n"
    )
    missing_indent = (
        "if True:\n"
        "result = 'bad'\n"
    )
    show_compile_result("valid block", valid_source)
    show_compile_result("missing colon", missing_colon)
    show_compile_result("missing indent", missing_indent)

    section("6. Parentheses support readable multiline conditions")
    predict("Does visual continuation create another code block?")
    strict = True
    severity = "warning"
    missing_keys = ["menu.quit"]
    should_block = (
        severity == "error"
        or (strict and bool(missing_keys))
    )
    print("should_block ->", should_block)
    print("Rule: parentheses continue one expression; the indented suite is the block.")


if __name__ == "__main__":
    main()
