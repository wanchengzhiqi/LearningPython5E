"""
Common string methods and formatting.

Run:
    python practice\P2_Types_and_Operations\C7_String_Fundamentals\04_methods_and_formatting.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def show(title, value):
    print(f"{title:<36} -> {value!r} ({type(value).__name__})")


def show_ascii(title, value):
    """Show values with non-ASCII characters escaped for Windows terminals."""
    print(f"{title:<36} -> {ascii(value)} ({type(value).__name__})")


def placeholders(text):
    names = []
    start = 0
    while True:
        left = text.find("{", start)
        if left == -1:
            return names
        right = text.find("}", left + 1)
        if right == -1:
            return names
        names.append(text[left + 1:right])
        start = right + 1


def main():
    section("1. Transform methods return new strings")
    predict("Does strip() modify the original string object?")
    raw = "  HP Potion\n"
    cleaned = raw.strip()
    show("raw", raw)
    show("cleaned = raw.strip()", cleaned)
    show("raw after strip()", raw)
    print("raw is cleaned ->", raw is cleaned)
    print("Rule: string methods do not modify the original str object.")

    section("2. Search and test methods answer questions")
    predict("Which methods return bool, and which return positions?")
    key = "item.potion.small"
    show("key.startswith('item.')", key.startswith("item."))
    show("'potion' in key", "potion" in key)
    show("key.find('potion')", key.find("potion"))
    show("key.find('weapon')", key.find("weapon"))
    try:
        key.index("weapon")
    except ValueError as exc:
        print("key.index('weapon') ->", type(exc).__name__, str(exc))
    print("Rule: find() returns -1 when missing; index() raises ValueError.")

    section("3. split() and join() are core engineering tools")
    predict("What object types do split() and join() return?")
    path_key = "menu/options/audio"
    parts = path_key.split("/")
    rebuilt = ".".join(parts)
    show("path_key.split('/')", parts)
    show("'.'.join(parts)", rebuilt)
    show("type(parts)", type(parts))
    show("type(rebuilt)", type(rebuilt))

    section("4. replace() creates another string")
    predict("Does replace() change the source localization text?")
    source_text = "Hello, {player}! You got {count} item."
    translated_text = source_text.replace("Hello", "你好").replace("item", "道具")
    show("source_text", source_text)
    show("translated_text", translated_text)
    show("source_text placeholders", placeholders(source_text))
    show("translated_text placeholders", placeholders(translated_text))

    section("5. Case operations are language-aware enough for basics, not full localization")
    predict("What is the difference between lower() and casefold() for 'Stra\\u00dfe'?")
    word = "Stra\u00dfe"
    show_ascii("word", word)
    show_ascii("word.lower()", word.lower())
    show_ascii("word.casefold()", word.casefold())
    print("Rule: casefold() is stronger for caseless matching, but real localization may need domain rules.")

    section("6. Formatting produces strings; it does not change the original objects")
    predict("What are the type and content of the formatted result?")
    item_name = "Potion"
    count = 7
    price = 12.5
    line = f"{item_name:<10} x{count:02d} price={price:.2f}"
    show("item_name", item_name)
    show("count", count)
    show("price", price)
    show("line", line)
    print("Rule: f-strings, format(), and '%' formatting all create str results.")


if __name__ == "__main__":
    main()
