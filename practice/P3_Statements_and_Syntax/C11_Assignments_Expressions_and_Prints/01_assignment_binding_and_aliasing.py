r"""
Assignment, binding, chained assignment, and aliasing.

Run:
    python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\01_assignment_binding_and_aliasing.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_binding(name, value):
    print(f"{name:<18} type={type(value).__name__:<10} id={id(value)} repr={value!r}")


def main():
    section("1. Ordinary assignment binds a name to the right-side object")
    predict("Does assignment copy the string object, print it, or bind a name to it?")
    content = "  请补充菜单翻译  "
    normalized = content.strip()
    show_binding("content", content)
    show_binding("normalized", normalized)
    print("content is normalized ->", content is normalized)
    print("Rule: the right side is evaluated first; assignment then binds the name.")

    section("2. Assignment does not copy a mutable object")
    predict("If alias and record name the same dict, what does alias['tags'].append change?")
    record = {"title": "C11 prompt", "tags": ["imported"]}
    alias = record
    alias["tags"].append("assignment")
    show_binding("record", record)
    show_binding("alias", alias)
    print("record is alias ->", record is alias)
    print("Rule: assignment copied no dict; both names refer to the same object.")

    section("3. Chained assignment shares one right-side object")
    predict("After left.append('menu.start'), what will right contain?")
    left = right = []
    left.append("menu.start")
    show_binding("left", left)
    show_binding("right", right)
    print("left is right ->", left is right)
    print("Correction: a = b = [] is not two independent lists.")

    section("4. Use separate expressions when you need separate mutable objects")
    predict("Are source_keys and target_keys the same list here?")
    source_keys, target_keys = [], []
    source_keys.append("menu.start")
    target_keys.append("menu.quit")
    show_binding("source_keys", source_keys)
    show_binding("target_keys", target_keys)
    print("source_keys is target_keys ->", source_keys is target_keys)

    section("5. prompt_store.py pattern: list mutation vs string rebinding")
    predict("Which objects are mutated, and which name is rebound?")
    clauses = []
    params = []
    query = "SELECT * FROM records"
    original_query_id = id(query)

    clauses.append("status = 'active'")
    clauses.append("category = ?")
    params.append("quiz_generation_request")
    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    show_binding("clauses", clauses)
    show_binding("params", params)
    show_binding("query", query)
    print("query id changed ->", original_query_id != id(query))
    print("Rule: list.append mutates the list; str += creates a new str and rebinds query.")


if __name__ == "__main__":
    main()
