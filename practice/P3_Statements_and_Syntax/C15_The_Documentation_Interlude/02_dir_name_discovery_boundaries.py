r"""
dir() as name discovery rather than a complete API contract.

Run:
    python practice\P3_Statements_and_Syntax\C15_The_Documentation_Interlude\02_dir_name_discovery_boundaries.py
"""


MISSING = object()


class Catalog:
    """Catalog with inherited, instance, dynamic, and advertised names."""

    category = "localization"

    def __init__(self):
        self.instance_only = "runtime state"
        self.version = "1.0"

    def lookup(self, key):
        """Return a display value for key."""

        return f"value:{key}"

    def __getattr__(self, name):
        if name == "runtime_alias":
            return lambda key: self.lookup(key)
        raise AttributeError(name)

    def __dir__(self):
        discovered = set(super().__dir__())
        discovered.add("advertised_only")
        return sorted(discovered)


def section(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def predict(question):
    print(f"[Predict] {question}")


def main():
    catalog = Catalog()

    section("1. dir() gathers candidate names from several places")
    predict("Which selected names appear on the instance and on the class?")
    selected = [
        name
        for name in dir(catalog)
        if name in {"category", "instance_only", "version", "lookup", "advertised_only"}
    ]
    print("selected dir(instance) names ->", selected)
    print("instance_only in dir(instance) ->", "instance_only" in dir(catalog))
    print("instance_only in dir(class) ->", "instance_only" in dir(Catalog))
    print("lookup in dir(instance) ->", "lookup" in dir(catalog))
    print("vars(instance) ->", vars(catalog))
    print("Rule: dir() is broader than the instance's own __dict__.")

    section("2. Discovery does not prove accessibility")
    predict("Can custom __dir__ advertise a name getattr() cannot retrieve?")
    print("advertised_only in dir(instance) ->", "advertised_only" in dir(catalog))
    print("hasattr(instance, 'advertised_only') ->", hasattr(catalog, "advertised_only"))
    print("Rule: custom __dir__ can advertise a name without an attribute.")

    section("3. Accessibility does not require appearance in dir()")
    predict("Can __getattr__ provide a dynamic name that dir() omits?")
    print("runtime_alias in dir(instance) ->", "runtime_alias" in dir(catalog))
    print("hasattr(instance, 'runtime_alias') ->", hasattr(catalog, "runtime_alias"))
    print("runtime_alias('menu.start') ->", catalog.runtime_alias("menu.start"))
    print("Rule: a dynamic attribute may be accessible but absent from dir().")

    section("4. A discovered name still needs contract checks")
    predict("Is every discovered name callable or guaranteed to be public?")
    for name in ("lookup", "version", "advertised_only"):
        value = getattr(catalog, name, MISSING)
        accessible = value is not MISSING
        display = repr(value) if accessible else "<missing>"
        print(
            f"{name}: accessible={accessible}, "
            f"callable={callable(value) if accessible else False}, value={display}"
        )
    print(
        "Rule: verify accessibility, callability, documentation, version scope, "
        "side effects, and public-API status after discovery."
    )


if __name__ == "__main__":
    main()
