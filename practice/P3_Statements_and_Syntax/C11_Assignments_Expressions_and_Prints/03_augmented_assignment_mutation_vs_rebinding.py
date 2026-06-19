r"""
Augmented assignment: in-place mutation opportunity versus rebinding.

Run:
    python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\03_augmented_assignment_mutation_vs_rebinding.py
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
    section("1. list += usually mutates the existing list object")
    predict("If alias points to items, will alias see items += [...]?")
    items = ["menu.start"]
    alias = items
    before_id = id(items)
    items += ["menu.quit"]
    show_binding("items", items)
    show_binding("alias", alias)
    print("items id unchanged ->", before_id == id(items))
    print("Rule: list.__iadd__ can extend the existing list in place.")

    section("2. list + creates a new list and then assignment rebinds the name")
    predict("Will alias follow items = items + [...]?")
    before_id = id(items)
    items = items + ["menu.options"]
    show_binding("items", items)
    show_binding("alias", alias)
    print("items id changed ->", before_id != id(items))
    print("Rule: + produced a new list; assignment rebound only the name items.")

    section("3. Immutable objects normally cannot be modified in place")
    predict("Do tuple += and str += keep the same object identity?")
    status_path = ("active",)
    label = "prompt"
    old_status_path_id = id(status_path)
    old_label_id = id(label)
    status_path += ("locked",)
    label += "_template"
    show_binding("status_path", status_path)
    show_binding("label", label)
    print("tuple id changed ->", old_status_path_id != id(status_path))
    print("str id changed   ->", old_label_id != id(label))

    section("4. set |= and dict |= mutate the existing mapping/set")
    predict("Will aliases see the new flags and counts?")
    flags = {"active"}
    flag_alias = flags
    counts = {"active": 3}
    count_alias = counts
    flags |= {"locked"}
    counts |= {"deleted": 1}
    show_binding("flags", flags)
    show_binding("flag_alias", flag_alias)
    show_binding("counts", counts)
    show_binding("count_alias", count_alias)
    print("flags is flag_alias ->", flags is flag_alias)
    print("counts is count_alias ->", counts is count_alias)

    section("5. Advanced edge: augmented assignment can mutate before failing")
    predict("What happens to the inner list inside a tuple after holder[0] += [...]?")
    holder = (["menu.start"],)
    try:
        holder[0] += ["menu.quit"]
    except TypeError as exc:
        print("caught ->", exc)
    show_binding("holder", holder)
    print("Correction: the inner list was mutated, then tuple item assignment failed.")

    section("6. prompt_store.py pattern: params.extend vs query +=")
    predict("Which object changes in place, and which name receives a new object?")
    params = ["%阶段测验%"]
    query = "SELECT * FROM records"
    old_params_id = id(params)
    old_query_id = id(query)
    params.extend(["%阶段测验%", "%阶段测验%"])
    query += " WHERE title LIKE ? OR content LIKE ?"
    show_binding("params", params)
    show_binding("query", query)
    print("params id unchanged ->", old_params_id == id(params))
    print("query id changed    ->", old_query_id != id(query))


if __name__ == "__main__":
    main()
