"""
String literals and escapes: source form, parsed str object, and characters.

Run:
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\01_literals_and_escapes.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show_text(source_form, value):
    print(f"source form : {source_form}")
    print(f"type        : {type(value).__name__}")
    print(f"len         : {len(value)}")
    print(f"str(value)  : {str(value)}")
    print(f"repr(value) : {repr(value)}")
    print("characters :")
    for index, char in enumerate(value):
        print(f"  [{index}] {repr(char):<8} ord={ord(char):>6} code=U+{ord(char):04X}")


def try_compile(source_form):
    print(f"compile({source_form!r})")
    try:
        compile(source_form, "<string-literal-demo>", "eval")
    except SyntaxError as exc:
        print(f"  SyntaxError: {exc.msg}")
    else:
        print("  ok")


def main():
    section("1. Quotes are source syntax, not object content")
    predict("Does the object created by 'spam' contain quote characters?")
    show_text("'spam'", "spam")
    show_text('"spam"', "spam")
    print("Rule: different quote styles can create equal string objects.")
    print("'spam' == \"spam\" ->", "spam" == "spam")

    section("2. Escapes are handled while Python parses the literal")
    predict("How many characters are in 'sp\\nm' and where is the newline?")
    show_text("'sp\\nm'", "sp\nm")
    show_text("'sp\\tm'", "sp\tm")
    show_text("'sp\\\\m'", "sp\\m")
    print("Rule: the backslash belongs to the source form; after parsing, it may become one real character.")

    section("3. Hex and Unicode escapes create characters, not bytes")
    predict("Are '\\x41', '\\u0041', and 'A' different object types?")
    show_text("'\\x41\\u4F60'", "\x41\u4F60")
    show_text("'A你'", "A你")
    print("Rule: \\xhh and \\uxxxx in a str literal still create Unicode characters.")

    section("4. Raw strings reduce escaping, but they are still Python literals")
    predict("What is the difference between a normal Windows path and a raw-string path?")
    normal_path = "C:\new\name.txt"
    raw_path = r"C:\new\name.txt"
    escaped_path = "C:\\new\\name.txt"
    show_text('"C:\\new\\name.txt"', normal_path)
    show_text('r"C:\\new\\name.txt"', raw_path)
    show_text('"C:\\\\new\\\\name.txt"', escaped_path)
    print("Rule: raw strings are useful for paths and regex-like text, but the quote boundary still matters.")
    try_compile("r'abc\\'")

    section("5. Triple-quoted literals preserve real newlines")
    predict("Is the line break in a triple-quoted literal one character or two characters?")
    message = """Line 1
Line 2"""
    show_text('"""Line 1\\nLine 2"""', message)

    section("6. Unknown escapes in Python 3.9 are retained, but avoid relying on them")
    predict("What object does the literal source 'sp\\cm' create in Python 3.9?")
    value = eval("'sp\\cm'")
    show_text("'sp\\cm'", value)
    print("Engineering rule: write an intended backslash as '\\\\' or use a raw string when appropriate.")


if __name__ == "__main__":
    main()
