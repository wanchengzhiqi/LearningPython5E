r"""
Script execution versus interactive echo.

Run:
    python practice\P3_Statements_and_Syntax\C10_Introducing_Python_Statements\02_script_vs_interactive_echo.py
"""

from code import InteractiveInterpreter
from contextlib import redirect_stdout
from io import StringIO


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def run_as_interactive(source_line):
    buffer = StringIO()
    interpreter = InteractiveInterpreter()
    with redirect_stdout(buffer):
        needs_more_input = interpreter.runsource(source_line)
    return buffer.getvalue().rstrip(), needs_more_input


def main():
    section("1. A script does not echo the value of a bare expression statement")
    predict("Will this script auto-display the result of 'menu.start'.upper()?")
    "menu.start".upper()
    print("Script output continues here; the expression value was discarded.")

    section("2. An interactive session echoes non-None expression values")
    predict("What would an interactive prompt show for 'menu.start'.upper()?")
    echo, needs_more = run_as_interactive("'menu.start'.upper()")
    print("interactive input  -> 'menu.start'.upper()")
    print("interactive output ->", repr(echo))
    print("needs_more_input   ->", needs_more)
    print("Rule: interactive echo displays repr(value) for non-None expression values.")

    section("3. print() output is not the same thing as interactive echo")
    predict("Will interactive Python echo None after print('Start')?")
    echo, needs_more = run_as_interactive("print('Start')")
    print("interactive input  -> print('Start')")
    print("interactive output ->", repr(echo))
    print("needs_more_input   ->", needs_more)
    print("Rule: print() writes text; the returned None is not echoed interactively.")

    section("4. None values are usually suppressed by interactive displayhook")
    predict("What does an interactive prompt display for the expression None?")
    echo, needs_more = run_as_interactive("None")
    print("interactive input  -> None")
    print("interactive output ->", repr(echo))
    print("needs_more_input   ->", needs_more)
    print("Rule: no echo does not mean no value; None is a real object.")


if __name__ == "__main__":
    main()
