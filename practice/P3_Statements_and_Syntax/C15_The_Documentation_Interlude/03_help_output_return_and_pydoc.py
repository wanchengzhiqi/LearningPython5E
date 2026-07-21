r"""
help() output, return value, local docstrings, and pydoc rendering.

Run:
    python practice\P3_Statements_and_Syntax\C15_The_Documentation_Interlude\03_help_output_return_and_pydoc.py
"""

from contextlib import redirect_stdout
from io import StringIO
import pydoc


def lookup_text(key, *, fallback=""):
    """Return a demonstration translation for key or fallback when unknown."""

    translations = {"menu.start": "Start", "menu.quit": "Quit"}
    return translations.get(key, fallback)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def capture_help(obj):
    buffer = StringIO()
    with redirect_stdout(buffer):
        result = help(obj)
    return result, buffer.getvalue()


def nonblank_excerpt(text, limit=10):
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return lines[:limit]


def main():
    section("1. help() writes human-facing text and returns None")
    predict("What is captured as output, and what object does help() return?")
    result, output = capture_help(lookup_text)
    print("help() return is None ->", result is None)
    print("captured output type ->", type(output).__name__)
    print("captured output length ->", len(output))
    print("output contains function name ->", "lookup_text" in output)
    print("output contains docstring text ->", "demonstration translation" in output)

    section("2. Check stable facts instead of memorizing display formatting")
    predict("Which excerpt lines are useful without becoming a format contract?")
    for line in nonblank_excerpt(output):
        print("help excerpt ->", line)
    print(
        "Rule: pager, spacing, headings, and rendering can vary; "
        "verify the signature and contract fields separately."
    )

    section("3. __doc__ is metadata; help() adds presentation")
    predict("Is raw __doc__ identical to the complete help() display?")
    print("lookup_text.__doc__ ->", lookup_text.__doc__)
    print("docstring equals complete help output ->", lookup_text.__doc__ == output)
    print("function business return ->", lookup_text("menu.start"))
    print("unknown-key return ->", lookup_text("menu.unknown", fallback="<missing>"))

    section("4. pydoc.render_doc() returns rendered text")
    predict("How does render_doc() differ from help() at the return boundary?")
    rendered = pydoc.render_doc(lookup_text, renderer=pydoc.plaintext)
    print("render_doc return type ->", type(rendered).__name__)
    print("rendered contains function name ->", "lookup_text" in rendered)
    print("rendered contains docstring text ->", "demonstration translation" in rendered)
    print("Rule: help() displays; pydoc also exposes text-producing APIs.")


if __name__ == "__main__":
    main()
