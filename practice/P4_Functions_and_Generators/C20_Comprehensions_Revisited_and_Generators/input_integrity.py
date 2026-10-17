"""C20-20: source ownership, trusted coverage manifest, non-empty publishing policy.

Python 3.14.5 learning semantics. Self-contained standard-library-only example.
Scope: single-threaded in-memory objects; manifest and record IDs are trusted inputs.
"""
from collections import Counter


def audit_records(records, *, limit=None):
    """C20-19 core: exhaustive unless limited or interrupted by an exception."""
    if limit is not None and (type(limit) is not int or limit < 0):
        raise ValueError("limit must be a nonnegative integer or None")
    scanned, mapping, issues, seen_keys = 0, {}, [], set()
    end = object()
    status, error = None, None
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
            if key in seen_keys:
                issues.append((scanned, key, "duplicate-key"))
                continue
            seen_keys.add(key)
            raw = row.get("text")
            if not isinstance(raw, str):
                issues.append((scanned, key, "invalid-text"))
                continue
            text = raw.strip()
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


def audit_with_manifest(source_factory, expected_ids, *, allow_empty=False, limit=None):
    """New C20-20 layer: track record-level coverage independently of business keys."""
    expected = tuple(expected_ids)
    if any(type(x) is not int for x in expected) or len(expected) != len(set(expected)):
        raise ValueError("expected_ids must contain unique integer row IDs")
    observed = []

    def traced_source():
        # Calls the factory as this generator is actually consumed.
        for row in source_factory():
            row_id = row["row_id"]
            if type(row_id) is not int:
                raise TypeError("row_id must be int")
            observed.append(row_id)
            yield row

    report = audit_records(traced_source(), limit=limit)
    observed_counts = Counter(observed)
    observed_set = set(observed)
    expected_set = set(expected)
    missing = sorted(expected_set - observed_set)
    unexpected = sorted(observed_set - expected_set)
    duplicated_ids = sorted(k for k, count in observed_counts.items() if count > 1)

    verified = (
        report["status"] == "complete"
        and not missing
        and not unexpected
        and not duplicated_ids
    )
    report["coverage"] = {
        "expected_ids": expected,
        "observed_ids": tuple(observed),
        "missing": missing,
        "unexpected": unexpected,
        "duplicated_ids": duplicated_ids,
        "verified": verified,
    }
    report["allow_empty"] = allow_empty
    return report


def make_catalog():
    return {
        "current": {
            "revision": 1,
            "mapping": {"menu.start": "旧开始", "menu.quit": "旧退出"},
        }
    }


def try_publish_verified(report, catalog):
    """Existing gate plus the two new requirements: coverage and non-empty policy."""
    if report["status"] != "complete":
        return {"published": False, "reason": report["status"]}
    if report["error"] is not None:
        return {"published": False, "reason": "processing-error"}
    if report["issues"]:
        return {"published": False, "reason": "data-issues"}
    if not report["coverage"]["verified"]:
        return {"published": False, "reason": "coverage-mismatch"}
    if not report["allow_empty"] and not report["coverage"]["expected_ids"]:
        return {"published": False, "reason": "empty-not-allowed"}

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


ROWS = [
    {"row_id": 0, "key": "menu.start", "text": " 开始 "},
    {"row_id": 1, "key": "menu.quit", "text": " 退出 "},
    {"row_id": 2, "key": "dialog.ok", "text": " 确定 "},
]
EXPECTED = (0, 1, 2)


def fresh_source():
    """Creates a fresh generator each invocation, from repeatable ROWS."""
    yield from ROWS


def run_case(name, factory, expected, *, allow_empty=False, limit=None):
    cat = make_catalog()
    old = cat["current"]
    report = audit_with_manifest(factory, expected, allow_empty=allow_empty, limit=limit)
    outcome = try_publish_verified(report, cat)
    if not outcome["published"]:
        assert cat["current"] is old
    print(
        f"{name:21} status={report['status']:13} "
        f"observed={list(report['coverage']['observed_ids'])!s:10} "
        f"missing={report['coverage']['missing']!s:5} "
        f"verified={str(report['coverage']['verified']):5} "
        f"published={str(outcome['published']):5} "
        f"reason={outcome['reason']}"
    )
    return report, outcome, cat


def main():
    # A. Fresh generator, trusted manifest, complete normal consumption.
    a, p, cat = run_case("A fresh complete", fresh_source, EXPECTED)
    assert a["coverage"]["verified"] and p["published"]
    assert list(cat["current"]["mapping"]) == ["menu.start", "menu.quit", "dialog.ok"]

    # F. Previously uncovered policy: empty source may or may not be publishable.
    f, p, _ = run_case("F empty rejected", lambda: iter(()), (), allow_empty=False)
    assert f["status"] == "complete" and f["coverage"]["verified"]
    assert p["reason"] == "empty-not-allowed"
    f2, p2, _ = run_case("F empty allowed", lambda: iter(()), (), allow_empty=True)
    assert f2["status"] == "complete" and p2["published"]

    # G. Broken provider contract: returns previously advanced *same* iterator.
    shared = iter(ROWS)
    assert next(shared)["row_id"] == 0
    g, p, _ = run_case("G previously consumed", lambda: shared, EXPECTED)
    assert g["status"] == "complete" and g["coverage"]["missing"] == [0]
    assert p["reason"] == "coverage-mismatch"

    # The factory alone is insufficient if it hands back a used iterator.
    # An unexpected row ID also breaks the manifest contract.
    def extra_source():
        yield from ROWS
        yield {"row_id": 99, "key": "extra.key", "text": " 额外 "}

    u, p, _ = run_case("U unexpected ID", extra_source, EXPECTED)
    assert u["coverage"]["unexpected"] == [99]
    assert p["reason"] == "coverage-mismatch"

    # Duplicate record identity can be detected even with distinct business keys.
    def duplicate_id_source():
        yield from ROWS
        yield {"row_id": 1, "key": "extra.key", "text": " 额外 "}

    d, p, _ = run_case("D duplicate row ID", duplicate_id_source, EXPECTED)
    assert d["coverage"]["duplicated_ids"] == [1]
    assert p["reason"] == "coverage-mismatch"

    # Even identical observed ID membership is insufficient when limit prevents
    # confirmation of the underlying iterator's StopIteration.
    l, p, _ = run_case("L exact limit", fresh_source, EXPECTED, limit=3)
    assert l["coverage"]["missing"] == []
    assert not l["coverage"]["verified"] and p["reason"] == "limit_reached"

    print("All 7 C20-20 contract cases passed.")


if __name__ == "__main__":
    main()
