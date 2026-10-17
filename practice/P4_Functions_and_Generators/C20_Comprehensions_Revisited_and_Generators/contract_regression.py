"""C20-19 | Python 3.14.5 mainline: lazy source -> audit -> publish.

Self-contained teaching regression, not a database/filesystem transaction.
"""


def lazy_rows(rows, events, *, fail_at=None):
    events.append("source:start")
    for index, row in enumerate(rows):
        if index == fail_at:
            events.append(("source:fail", index))
            raise RuntimeError("upstream unavailable")
        events.append(("source:yield", index))
        yield row
    events.append("source:complete")


def audit_records(records, *, limit=None):
    if limit is not None and (type(limit) is not int or limit < 0):
        raise ValueError("limit must be a nonnegative integer or None")

    scanned, mapping, issues, seen = 0, {}, [], set()
    status, error = None, None
    end = object()

    try:
        source = iter(records)
        while True:
            if limit is not None and scanned >= limit:
                status = "limit_reached"
                break

            row = next(source, end)
            if row is end:
                status = "complete"
                break

            scanned += 1
            if not isinstance(row, dict):
                issues.append((scanned, None, "invalid-record"))
                continue
            key = row.get("key")
            if not isinstance(key, str) or not key:
                issues.append((scanned, None, "invalid-key"))
                continue
            if key in seen:
                issues.append((scanned, key, "duplicate-key"))
                continue
            seen.add(key)
            text = row.get("text")
            if not isinstance(text, str):
                issues.append((scanned, key, "invalid-text"))
                continue
            text = text.strip()
            if not text:
                issues.append((scanned, key, "empty-text"))
                continue
            mapping[key] = text
    except Exception as exc:
        status = "failed"
        error = {"type": type(exc).__name__, "message": str(exc)}

    return {
        "status": status,
        "scanned": scanned,
        "mapping": mapping,
        "issues": issues,
        "error": error,
    }


def make_catalog():
    return {
        "current": {
            "revision": 1,
            "mapping": {"menu.start": "旧开始", "menu.quit": "旧退出"},
        }
    }


def try_publish(report, catalog):
    if report["status"] != "complete":
        return {"published": False, "reason": report["status"]}
    if report["error"] is not None:
        return {"published": False, "reason": "processing-error"}
    if report["issues"]:
        return {"published": False, "reason": "data-issues"}

    raw = report["mapping"]
    if not isinstance(raw, dict) or any(
        not isinstance(k, str) or not isinstance(v, str)
        for k, v in raw.items()
    ):
        return {"published": False, "reason": "invalid-mapping"}

    candidate = {
        "revision": catalog["current"]["revision"] + 1,
        "mapping": dict(raw),
    }
    catalog["current"] = candidate
    return {"published": True, "reason": None}


GOOD = [
    {"key": "menu.start", "text": " 开始 "},
    {"key": "menu.quit", "text": " 退出 "},
    {"key": "dialog.ok", "text": " 确定 "},
]


def execute(rows, *, limit=None, fail_at=None):
    events = []
    catalog = make_catalog()
    old = catalog["current"]
    source = lazy_rows(rows, events, fail_at=fail_at)
    assert events == []                    # generator body not started
    report = audit_records(source, limit=limit)
    decision = try_publish(report, catalog)
    return report, decision, events, catalog, old


def show(name, report, decision, events):
    print(
        f"{name:15} status={report['status']:13} "
        f"scanned={report['scanned']} "
        f"issues={len(report['issues'])} "
        f"published={decision['published']} "
        f"source_complete={'source:complete' in events}"
    )


def main():
    # A: Complete + clean -> publish a new version, preserving the old object.
    r, p, e, cat, old = execute(GOOD)
    assert (r["status"], r["scanned"], r["issues"]) == ("complete", 3, [])
    assert p["published"] and "source:complete" in e
    assert cat["current"] is not old
    assert old["mapping"]["menu.start"] == "旧开始"
    r["mapping"]["menu.start"] = "后来修改报告"
    assert cat["current"]["mapping"]["menu.start"] == "开始"
    show("A clean", r, p, e)

    # B: Full scan, recoverable data issues -> no publish.
    bad = GOOD[:1] + [
        {"key": "menu.start", "text": " 启动 "},
        {"key": "menu.blank", "text": "  "},
        {"key": "menu.bad", "text": None},
    ]
    r, p, e, cat, old = execute(bad)
    assert r["status"] == "complete" and r["scanned"] == 4
    assert r["issues"] == [
        (2, "menu.start", "duplicate-key"),
        (3, "menu.blank", "empty-text"),
        (4, "menu.bad", "invalid-text"),
    ]
    assert not p["published"] and cat["current"] is old
    show("B issues", r, p, e)

    # C: Stop early -> not complete, and do not publish partial mapping.
    r, p, e, cat, old = execute(GOOD, limit=1)
    assert r["status"] == "limit_reached" and r["scanned"] == 1
    assert e == ["source:start", ("source:yield", 0)]
    assert not p["published"] and cat["current"] is old
    show("C limit 1", r, p, e)

    # D: Limit matches input length, but no extra next() confirmed exhaustion.
    r, p, e, cat, old = execute(GOOD, limit=len(GOOD))
    assert r["status"] == "limit_reached" and r["scanned"] == 3
    assert "source:complete" not in e
    assert not p["published"] and cat["current"] is old
    show("D exact limit", r, p, e)

    # E: Unrecoverable upstream error, leaving diagnostic partial data.
    r, p, e, cat, old = execute(GOOD, fail_at=1)
    assert r["status"] == "failed" and r["scanned"] == 1
    assert r["error"]["type"] == "RuntimeError"
    assert r["mapping"] == {"menu.start": "开始"}
    assert ("source:fail", 1) in e and "source:complete" not in e
    assert not p["published"] and cat["current"] is old
    show("E failure", r, p, e)

    # F: Empty source is still a normal completion. Current policy ALLOWS it.
    r, p, e, cat, old = execute([])
    assert r["status"] == "complete" and r["scanned"] == 0
    assert e == ["source:start", "source:complete"]
    assert p["published"] and cat["current"]["mapping"] == {}
    show("F empty", r, p, e)

    # G: Deliberate contract gap: a previously consumed input can still look
    #    'complete' to audit_records. The gate cannot certify source provenance.
    events = []
    source = lazy_rows(GOOD, events)
    assert next(source)["key"] == "menu.start"  # external consumption
    catalog = make_catalog()
    r = audit_records(source)
    p = try_publish(r, catalog)
    assert r["status"] == "complete" and r["scanned"] == 2
    assert p["published"]                           # current policy permits it
    assert "menu.start" not in catalog["current"]["mapping"]
    show("G shared gap", r, p, events)

    print("All 7 contract regression cases passed (G demonstrates a known gap).")


if __name__ == "__main__":
    main()
