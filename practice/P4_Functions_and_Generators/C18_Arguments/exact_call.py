import sys
print("PYTHON:", sys.version)
print("=" * 40)

def mark(name, value):
    print("mark", name)
    return value


def configure(path, language):
    print("BODY")
    language = "en-US"
    path.append("done")


p = ["config.json"]
lang = "zh-CN"

configure(
    mark("P", p),
    mark("L", lang),
)

print(p)
print(lang)
