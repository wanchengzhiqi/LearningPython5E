call_events = []
shared_options = {"normalize": True}


def resolve_builder():
    call_events.append("target")
    return build_entry


def evaluate(label, value):
    call_events.append(f"argument:{label}")
    return value


def build_entry(key, *, locale, options):
    call_events.append("body")
    return key


def return_locale():
    call_events.append("argument:locale")
    return "fr"


result = resolve_builder()(
    evaluate("key", "menu.quit"),
    locale=return_locale(),
    options=evaluate("options", shared_options),
)
print("no-exception events:", call_events)
print("result:", result)
