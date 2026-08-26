def collect_audit_inputs(primary_key, *extra_keys, **controls):
    return {
        "primary_key": primary_key,
        "extra_keys": extra_keys,
        "controls": controls,
    }


channels = ["menu"]

result = collect_audit_inputs(
    "menu.start",
    "menu.quit",
    channels,
    locale="ja-JP",
)

print("bindings:")
for key, value in result.items():
    print(f"  {key:11} = {value!r}")
print("  type(extra_keys):", type(result["extra_keys"]).__name__)
print("  id(extra_keys[1]) == id(channels):",
      id(result["extra_keys"][1]) == id(channels))

channels.append("dialog")

print()
print("after channels.append('dialog'):")
print("  channels =", channels)
print("  extra_keys =", result["extra_keys"])

print()
print(result["extra_keys"])
print(result["controls"])
print(result["extra_keys"][1] is channels)
