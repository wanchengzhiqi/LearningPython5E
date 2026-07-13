r"""
File objects and StringIO remember their read position while being iterated.

Run:
    python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\03_file_stringio_position_and_consumption.py
"""

from io import StringIO
from pathlib import Path


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def clean_lines(lines):
    return [line.rstrip("\n") for line in lines]


def main():
    section("1. StringIO iteration advances the current position")
    predict("After readline(), where will the following for/list consumption start?")
    stream = StringIO("menu.start=Start\nmenu.quit=Quit\nmenu.debug=Debug\n")
    print("initial position ->", stream.tell())
    print("readline() ->", stream.readline().rstrip("\n"))
    print("position after readline ->", stream.tell())
    print("remaining lines ->", clean_lines(stream))
    print("position after list(stream) ->", stream.tell())
    print("second remaining lines ->", clean_lines(stream))
    print("Rule: iteration did not copy the stream; it consumed from the current position.")

    section("2. seek(0) resets the stream position")
    predict("What changes after stream.seek(0)?")
    stream.seek(0)
    print("position after seek ->", stream.tell())
    print("all lines again ->", clean_lines(stream))

    section("3. A real text file object is also consumed progressively")
    predict("If we open this script file, what remains after taking the first lines?")
    script_path = Path(__file__)
    with script_path.open(encoding="utf-8") as file_obj:
        first_line = next(file_obj).rstrip("\n")
        next_three = [line.rstrip("\n") for _, line in zip(range(3), file_obj)]
        after_preview = next(file_obj, "<EOF>").rstrip("\n")
    print("opened file ->", script_path.name)
    print("first line ->", first_line)
    print("next three ->", next_three)
    print("line after preview ->", after_preview)
    print("Rule: next() and zip(..., file_obj) share the same file iterator state.")

    section("4. Reopening creates a new file object with a fresh position")
    predict("Will a new open() start from the beginning again?")
    with script_path.open(encoding="utf-8") as file_obj:
        print("fresh first line ->", next(file_obj).rstrip("\n"))
    print("Correction: repeatable path, one-shot file object.")


if __name__ == "__main__":
    main()
