"""C12-04: conditional expressions and localization rule decisions."""

TRACE = []


def section(title):
    print("\n" + "=" * 68)
    print(title)


def choose(label, value):
    TRACE.append(label)
    print("  evaluated", label)
    return value


def decide_report(*, strict, dry_run, missing_keys, empty_keys, output_mode, severity):
    """Return a decision without writing files or changing resources."""
    if output_mode not in {"text", "json"}:
        return {"status": "invalid", "reason": "unsupported output mode"}
    if severity not in {"info", "warning", "error"}:
        return {"status": "invalid", "reason": "unsupported severity"}

    issue_keys = missing_keys or empty_keys
    has_issues = bool(issue_keys)
    is_blocking = severity == "error" or (strict and has_issues)

    if is_blocking:
        status = "blocked"
    elif has_issues:
        status = "review"
    else:
        status = "clean"

    return {
        "status": status,
        "action": "preview" if dry_run else "write",
        "output_mode": output_mode,
        "severity": severity,
        "issue_keys": list(issue_keys),
    }


def main():
    section("1. A conditional expression produces a value")
    print("[Predict] Which side is evaluated when dry_run is True?")
    TRACE.clear()
    dry_run = True
    action = choose("preview", "preview") if dry_run else choose("write", "write")
    print("action ->", action)
    print("trace ->", TRACE)

    section("2. Expression versus statement responsibility")
    output_mode = "json"
    suffix = ".json" if output_mode == "json" else ".txt"
    print("single selected value ->", suffix)
    if output_mode == "json":
        serializer = "json.dumps"
        content_type = "application/json"
    else:
        serializer = "plain text formatter"
        content_type = "text/plain"
    print("multi-step block ->", serializer, content_type)

    section("3. Localization report decisions")
    print("[Predict] Which scenarios block, request review, or remain clean?")
    scenarios = [
        dict(strict=True, dry_run=True, missing_keys=["menu.quit"], empty_keys=[], output_mode="json", severity="warning"),
        dict(strict=False, dry_run=False, missing_keys=[], empty_keys=["menu.start"], output_mode="text", severity="warning"),
        dict(strict=False, dry_run=False, missing_keys=[], empty_keys=[], output_mode="json", severity="info"),
        dict(strict=False, dry_run=True, missing_keys=[], empty_keys=[], output_mode="xml", severity="info"),
    ]
    for index, scenario in enumerate(scenarios, start=1):
        print("scenario", index, "->", decide_report(**scenario))
    print("The function returns structured data and performs no file-write effect.")


if __name__ == "__main__":
    main()
