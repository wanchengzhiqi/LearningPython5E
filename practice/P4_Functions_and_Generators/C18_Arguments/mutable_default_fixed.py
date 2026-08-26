def record_tag(tag, history=None):
    if history is None:
        history = []
    history.append(tag)
    return history


first = record_tag("menu")
second = record_tag("dialog", [])
third = record_tag("settings")

print(first)
print(second)
print(third)
print(first is third)
