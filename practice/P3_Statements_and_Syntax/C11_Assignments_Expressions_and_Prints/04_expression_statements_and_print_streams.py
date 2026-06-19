r"""
Expression statements, print() return value, and output stream boundaries.

Run:
    python practice\P3_Statements_and_Syntax\C11_Assignments_Expressions_and_Prints\04_expression_statements_and_print_streams.py
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory


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
    section("1. A bare expression statement can discard a useful value")
    predict("Will this script auto-display the uppercase key?")
    "menu.start".upper()
    value = "menu.start".upper()
    show_binding("value", value)
    print("Rule: the bare expression was evaluated, but the script did not echo it.")

    section("2. An expression statement may be useful because of a side effect")
    predict("What changes when events.append(...) is used as a statement?")
    events = []
    events.append("loaded source prompts")
    append_result = events.append("parsed prompt blocks")
    show_binding("events", events)
    show_binding("append_result", append_result)
    print("Correction: append_result is None; the list changed via mutation.")

    section("3. print() writes output and returns None")
    predict("What object is bound to printed?")
    printed = print("visible stdout line")
    show_binding("printed", printed)
    print("Rule: the text above is output side effect, not the return value.")

    section("4. sep and end change emitted text, not the return value")
    predict("What will the captured stdout contain?")
    stdout_buffer = StringIO()
    with redirect_stdout(stdout_buffer):
        result = print("id", 7, "active", sep=" | ", end=" <END>")
    show_binding("result", result)
    show_binding("captured_stdout", stdout_buffer.getvalue())

    section("5. print(..., file=...) sends output to a chosen stream")
    predict("Will this write to the console, StringIO, or both?")
    stream = StringIO()
    stream_result = print("Record not found: 404", file=stream)
    show_binding("stream_result", stream_result)
    show_binding("stream_text", stream.getvalue())
    print("Rule: file= redirects the output boundary; print() still returns None.")

    section("6. A real file stream is an external side-effect boundary")
    predict("Does print(..., file=handle, flush=True) return the written text?")
    with TemporaryDirectory() as temp_dir:
        report_path = Path(temp_dir) / "prompt_report.txt"
        with report_path.open("w", encoding="utf-8") as handle:
            file_result = print("missing_key=menu.quit", file=handle, flush=True)
        show_binding("file_result", file_result)
        show_binding("file_text", report_path.read_text(encoding="utf-8"))
    print("Rule: the file content is an external side effect; the return value is None.")


if __name__ == "__main__":
    main()
