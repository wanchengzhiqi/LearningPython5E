def record_tag(tag, history=[]):
    history.append(tag)
    return history


first = record_tag("menu")
print("after first: ", first, "id(first) =", id(first))

second = record_tag("dialog", [])
print("after second:", first, "id(first) =", id(first))
print("              second:", second, "id(second) =", id(second))

third = record_tag("settings")
print("after third: ", first, "id(first) =", id(first))
print("              third:", third, "id(third) =", id(third))

print()
print(first)
print(second)
print(third)
print(first is third)

print()
print("default object lives on function:", record_tag.__defaults__)
print("id of __defaults__[0]:", id(record_tag.__defaults__[0]))
