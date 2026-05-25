"""
Paths, file objects, text, bytes, JSON, and CSV boundaries.

Run:
    python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\05_files_text_bytes_json_csv.py
"""

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SAMPLE_JSON = HERE / "sample_localization_source.json"
SAMPLE_CSV = HERE / "sample_glossary.csv"


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(title, value):
    print(f"{title:<34} -> {value!r} ({type(value).__name__})")


def main():
    section("1. A path string or Path object is not a file object")
    predict("What type does open(path, ...) return?")
    path_text = str(SAMPLE_JSON)
    path_object = SAMPLE_JSON
    show("path_text", path_text)
    show("path_object", path_object)
    with open(path_object, "r", encoding="utf-8") as file:
        show("file", file)
        show("file.closed inside with", file.closed)
        first_line = file.readline()
        show("first_line", first_line)
    show("file.closed after with", file.closed)
    print("Rule: a path locates data; a file object is the active I/O interface.")

    section("2. Text mode decodes bytes into str by using an encoding")
    predict("What changes when reading the same file as text and as bytes?")
    text = SAMPLE_JSON.read_text(encoding="utf-8")
    raw_bytes = SAMPLE_JSON.read_bytes()
    show("text[:40]", text[:40])
    show("type(text)", type(text))
    show("raw_bytes[:24]", raw_bytes[:24])
    show("type(raw_bytes)", type(raw_bytes))
    show("text.encode('utf-8')[:24]", text.encode("utf-8")[:24])
    print("Rule: text APIs decode bytes to str; byte APIs keep raw bytes.")

    section("3. JSON text is parsed into new Python objects")
    predict("Does json.loads(text) return the original file text or a dict object?")
    data = json.loads(text)
    show("data", data)
    show("type(data)", type(data))
    show("list(data.keys())", list(data.keys()))
    show("data is text", data is text)
    print("Rule: JSON object text becomes a Python dict; it is not the same layer.")

    section("4. csv.DictReader yields row mappings from text rows")
    predict("What object shape does a CSV row become?")
    with SAMPLE_CSV.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    show("rows", rows)
    show("type(rows[0])", type(rows[0]))
    print("Rule: CSV starts as text lines; DictReader creates dict-like row objects.")

    section("5. json.dumps() returns str; writing decides the file boundary")
    predict("What type is json_text before it reaches a file?")
    report = {"key_count": len(data), "keys": sorted(data)}
    json_text = json.dumps(report, ensure_ascii=False, indent=2)
    show("json_text", json_text)
    show("type(json_text)", type(json_text))
    show("json_text.encode('utf-8')[:24]", json_text.encode("utf-8")[:24])
    print("Rule: serialization creates text; file writing encodes that text to bytes.")


if __name__ == "__main__":
    main()
