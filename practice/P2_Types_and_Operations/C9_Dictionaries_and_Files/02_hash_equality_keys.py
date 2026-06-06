r"""
Hash and equality: why dict keys must be hashable.

Run:
    python practice\P2_Types_and_Operations\C9_Dictionaries_and_Files\02_hash_equality_keys.py
"""


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


class LocalizedKey:
    def __init__(self, text, note):
        self.text = text
        self.note = note

    def __repr__(self):
        return f"LocalizedKey({self.text!r}, note={self.note!r})"

    def __eq__(self, other):
        if not isinstance(other, LocalizedKey):
            return NotImplemented
        return self.text == other.text

    def __hash__(self):
        return hash(self.text)


class CollisionKey:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"CollisionKey({self.text!r})"

    def __eq__(self, other):
        if not isinstance(other, CollisionKey):
            return NotImplemented
        return self.text == other.text

    def __hash__(self):
        return 117


def try_hash(value):
    try:
        print(f"hash({value!r}) ->", hash(value))
    except TypeError as error:
        print(f"hash({value!r}) -> TypeError: {error}")


def main():
    section("1. Equal keys with equal hashes collapse to one dict entry")
    predict("If two different key objects compare equal, can a dict keep both?")
    key_from_source = LocalizedKey("menu.start", "from source file")
    key_from_target = LocalizedKey("menu.start", "from target file")
    resources = {key_from_source: "Start"}
    resources[key_from_target] = "Begin"
    only_key = next(iter(resources))
    print("key_from_source == key_from_target ->", key_from_source == key_from_target)
    print("key_from_source is key_from_target ->", key_from_source is key_from_target)
    print("hash(key_from_source) == hash(key_from_target) ->", hash(key_from_source) == hash(key_from_target))
    print("resources ->", resources)
    print("len(resources) ->", len(resources))
    print("only_key is key_from_source ->", only_key is key_from_source)
    print("only_key is key_from_target ->", only_key is key_from_target)
    print("Rule: dict lookup uses hash plus equality, not object identity.")

    section("2. Same hash alone is not enough to collapse keys")
    predict("If two unequal objects have the same hash, does one overwrite the other?")
    collision_a = CollisionKey("menu.start")
    collision_b = CollisionKey("menu.quit")
    collisions = {collision_a: "Start", collision_b: "Quit"}
    print("collision_a == collision_b ->", collision_a == collision_b)
    print("hash(collision_a) == hash(collision_b) ->", hash(collision_a) == hash(collision_b))
    print("collisions ->", collisions)
    print("len(collisions) ->", len(collisions))
    print("Rule: hash narrows the search; == still decides whether keys are equal.")

    section("3. Hashable is not exactly the same word as immutable")
    predict("Which values can be dict keys?")
    try_hash("menu.start")
    try_hash(("menu", "start"))
    try_hash(("menu", ["start"]))
    try_hash(["menu", "start"])
    print("Rule: a tuple is hashable only when all items inside it are hashable.")

    section("4. dict.fromkeys() preserves order while removing repeated equal keys")
    predict("What order survives after dict.fromkeys(keys)?")
    keys = ["menu.start", "menu.quit", "menu.start", "menu.options"]
    unique_dict = dict.fromkeys(keys)
    unique_list = list(unique_dict)
    print("keys ->", keys)
    print("dict.fromkeys(keys) ->", unique_dict)
    print("list(dict.fromkeys(keys)) ->", unique_list)
    print("Rule: dict keys are unique and preserve first insertion order in modern Python.")

    section("5. Sets and dict keys share the same hash/equality foundation")
    predict("Which keys are missing, extra, or shared?")
    source_keys = {"menu.start", "menu.quit", "menu.options"}
    target_keys = {"menu.start", "menu.quit", "debug.unused"}
    print("source_keys - target_keys ->", sorted(source_keys - target_keys))
    print("target_keys - source_keys ->", sorted(target_keys - source_keys))
    print("source_keys & target_keys ->", sorted(source_keys & target_keys))
    print("Rule: set operations are ideal for localization key coverage checks.")


if __name__ == "__main__":
    main()
