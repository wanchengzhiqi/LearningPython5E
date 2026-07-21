r"""
Documentation layers: comments, string expressions, and __doc__ metadata.

Run:
    python practice\P3_Statements_and_Syntax\C15_The_Documentation_Interlude\01_documentation_layers_and_dunder_doc.py
"""

import ast
import inspect
import sys


SOURCE_SAMPLE = '''
# A comment is source information, not a string object.
"""Sample module docstring."""
"An ordinary module string expression."
value = 3
'''


def documented_lookup(key):
    """Return a small display value for a localization key."""

    "This later string expression is not the function docstring."
    return f"value:{key}"


def not_documented():
    marker = "the first statement is an assignment"
    """This string is not in the special first-statement position."""
    return marker


class Catalog:
    """Minimal catalog used only for documentation inspection."""

    def lookup(self, key):
        """Return the key unchanged for this teaching example."""

        return key


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def string_expression_count(tree):
    return sum(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
        for node in tree.body
    )


def main():
    section("1. A docstring comes from a special source position")
    predict("Which objects have a non-None __doc__ value?")
    current_module = sys.modules[__name__]
    observations = {
        "module": current_module.__doc__,
        "documented_lookup": documented_lookup.__doc__,
        "not_documented": not_documented.__doc__,
        "Catalog": Catalog.__doc__,
        "Catalog.lookup": Catalog.lookup.__doc__,
    }
    for name, value in observations.items():
        print(f"{name}.__doc__ -> {value!r}")

    section("2. inspect.getdoc() returns cleaned human-facing text")
    predict("Does inspect.getdoc() return the function object or a string?")
    cleaned = inspect.getdoc(documented_lookup)
    print("type(cleaned) ->", type(cleaned).__name__)
    print("cleaned ->", cleaned)
    print("function call ->", documented_lookup("menu.start"))
    print("Rule: metadata text and the business return are separate.")

    section("3. Comments and ordinary strings remain source-level facts")
    predict("How many string expression statements are in SOURCE_SAMPLE?")
    tree = ast.parse(SOURCE_SAMPLE)
    print("top-level AST nodes ->", [type(node).__name__ for node in tree.body])
    print("string expression count ->", string_expression_count(tree))
    print("ast.get_docstring(tree) ->", ast.get_docstring(tree))
    print("comment represented as an AST statement ->", False)
    print(
        "Rule: only the first string literal is the module docstring; "
        "the second is an ordinary expression statement."
    )

    section("4. Source, metadata, and display answer different questions")
    predict("Can __doc__ reproduce the source comment or every source string?")
    print("source contains comment ->", "# A comment" in SOURCE_SAMPLE)
    print("source contains ordinary string ->", "ordinary module string" in SOURCE_SAMPLE)
    print(
        "module metadata contains source comment ->",
        "# A comment" in (current_module.__doc__ or ""),
    )
    print("Rule: inspect source for source facts and __doc__ for docstring metadata.")


if __name__ == "__main__":
    main()
