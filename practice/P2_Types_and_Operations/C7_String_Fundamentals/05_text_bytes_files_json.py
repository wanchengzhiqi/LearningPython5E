"""
Text, bytes, UTF-8 files, JSON, and Windows paths.

Run:
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\05_text_bytes_files_json.py
"""

import json
from pathlib import Path


SAMPLE_FILE = Path(__file__).with_name("sample_localization_utf8.txt")


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(title, value):
    print(f"{title:<38} -> {value!r} ({type(value).__name__})")


def main():
    section("1. str is text; bytes is encoded data")
    predict("How many characters and how many UTF-8 bytes are in 'HP药水'?")
    text = "HP药水"
    encoded = text.encode("utf-8")
    decoded = encoded.decode("utf-8")
    show("text", text)
    show("len(text)", len(text))
    show("encoded", encoded)
    show("len(encoded)", len(encoded))
    show("list(encoded)", list(encoded))
    show("encoded.hex(' ')", encoded.hex(" "))
    show("decoded", decoded)
    print("Rule: encoding maps str to bytes; decoding maps bytes back to str.")

    section("2. bytes indexing returns int byte values")
    predict("What type is encoded[0]?")
    show("encoded[0]", encoded[0])
    show("encoded[:1]", encoded[:1])
    print("Rule: bytes indexing returns an int from 0 to 255; slicing bytes returns bytes.")

    section("3. Read a UTF-8 text file as text and as raw bytes")
    predict("What changes when reading with read_text() vs read_bytes()?")
    file_text = SAMPLE_FILE.read_text(encoding="utf-8")
    file_bytes = SAMPLE_FILE.read_bytes()
    show("file_text", file_text)
    show("type(file_text)", type(file_text))
    show("file_bytes[:20]", file_bytes[:20])
    show("type(file_bytes)", type(file_bytes))
    print("Rule: text file APIs decode bytes into str using the encoding you specify.")

    section("4. JSON strings are text; writing to a file or socket needs bytes eventually")
    predict("What type does json.dumps() return?")
    payload = {
        "item.potion": "HP药水",
        "menu.start": "开始游戏",
        "dialog.line": "Line 1\nLine 2",
    }
    json_text = json.dumps(payload, ensure_ascii=False, indent=2)
    ascii_json_text = json.dumps(payload, ensure_ascii=True)
    show("json_text", json_text)
    show("type(json_text)", type(json_text))
    show("ascii_json_text", ascii_json_text)
    show("json_text.encode('utf-8')[:20]", json_text.encode("utf-8")[:20])
    print("Rule: JSON library gives you str; files/network boundaries decide encoding.")

    section("5. Windows path strings are a classic escape trap")
    predict("Why is 'C:\\new\\name.txt' dangerous if written without care?")
    bad_path = "C:\new\name.txt"
    raw_path = r"C:\new\name.txt"
    escaped_path = "C:\\new\\name.txt"
    show("bad_path", bad_path)
    show("raw_path", raw_path)
    show("escaped_path", escaped_path)
    print("Rule: for Windows paths, prefer pathlib or raw strings when backslashes are visible in source.")


if __name__ == "__main__":
    main()
