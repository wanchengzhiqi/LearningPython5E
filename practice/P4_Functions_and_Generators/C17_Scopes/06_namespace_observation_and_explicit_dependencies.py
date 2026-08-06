r"""
Limited namespace observation and explicit dependency passing.

Run:
    python practice\P4_Functions_and_Generators\C17_Scopes\06_namespace_observation_and_explicit_dependencies.py
"""


DEFAULT_LOCALE = "en-US"


def observe_selected_names(locale):
    local_key = "menu.start"
    local_view = locals()
    global_view = globals()
    selected_names = tuple(
        sorted(name for name in ("locale", "local_key") if name in local_view)
    )
    return {
        "selected_local_names": selected_names,
        "locale_value": local_view["locale"],
        "key_value": local_view["local_key"],
        "module_has_default": "DEFAULT_LOCALE" in global_view,
        "len_is_module_global": "len" in global_view,
    }


def build_label_from_module(key):
    return f"{DEFAULT_LOCALE}:{key}"


def build_label_with_dependency(key, locale):
    return f"{locale}:{key}"


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    section("1. locals() can provide selected evidence about this call")
    predict("Which chosen local names are bound at the observation point?")
    evidence = observe_selected_names("ja-JP")
    print("selected local names ->", evidence["selected_local_names"])
    print("observed locale ->", evidence["locale_value"])
    print("observed key ->", evidence["key_value"])
    print("Rule: this is a selected runtime observation of one function call.")

    section("2. globals() observes this module namespace, not every scope")
    predict("Is built-in len stored as a module-global name in this file?")
    print("module has DEFAULT_LOCALE ->", evidence["module_has_default"])
    print("len is module global ->", evidence["len_is_module_global"])
    print("calling built-in len still works ->", len(("menu", "dialog")))
    print(
        "Rule: a missing module binding can still fall through to builtins "
        "during ordinary LEGB lookup."
    )

    section("3. Explicit dependencies make call inputs visible")
    predict("Which function lets the caller choose the locale directly?")
    print("implicit module configuration ->", build_label_from_module("menu.start"))
    print(
        "explicit dependency ->",
        build_label_with_dependency("menu.start", "fr-FR"),
    )
    print(
        "Rule: explicit input avoids hidden dependence on a mutable module "
        "binding and makes the choice visible at the call site."
    )

    section("4. Namespace mappings are evidence, not arbitrary write-back APIs")
    predict("Did this experiment modify either returned namespace mapping?")
    print("namespace mappings modified ->", False)
    print("synthetic module default ->", DEFAULT_LOCALE)
    print(
        "Boundary: the experiment reads selected keys only; it does not print "
        "whole namespaces or promise that mapping writes reliably rebind names."
    )


if __name__ == "__main__":
    main()
