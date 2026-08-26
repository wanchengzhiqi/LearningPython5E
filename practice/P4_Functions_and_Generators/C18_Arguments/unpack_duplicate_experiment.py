events = []

def positional_source():
    events.append("positional")
    return ("prompt-008", "en-US")

def explicit_flag():
    events.append("explicit")
    return True

def mapping_source():
    events.append("mapping")
    return {"dry_run": False}

def target(key, locale, *, dry_run):
    events.append("body")

try:
    target(
        *positional_source(),
        dry_run=explicit_flag(),
        **mapping_source(),
    )
except TypeError:
    events.append("TypeError")

print("events:", events)
print("events list:", list(events))
