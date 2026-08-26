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
    current_locals = locals()
    parameter_names = tuple(
        name for name in ("key", "locale", "options") if name in current_locals
    )
    return {
        "label": f"{locale}:{key.strip().lower()}",
        "options": options,
        "parameter_names": parameter_names,
    }


def fail_locale():
    call_events.append("argument:locale")
    raise ValueError("bad locale")


try:
    resolve_builder()(
        evaluate("key", "menu.quit"),
        locale=fail_locale(),
        options=evaluate("options", shared_options),
    )
except ValueError as e:
    print(f"caught: {type(e).__name__}: {e}")

print("call_events =", call_events)
print("events list is:", list(call_events))
