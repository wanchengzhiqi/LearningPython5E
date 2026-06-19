#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SQLite storage layer for the local prompt template manager."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence


PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parents[2]
DEFAULT_DB_PATH = PROJECT_DIR / "data" / "prompt_templates.sqlite3"

VALID_STATUSES = {"active", "deleted"}


SCHEMA = """
CREATE TABLE IF NOT EXISTS records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    tags_json TEXT NOT NULL DEFAULT '[]',
    source_file TEXT,
    source_block_index INTEGER,
    source_start_line INTEGER,
    source_end_line INTEGER,
    source_hash TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
    is_locked INTEGER NOT NULL DEFAULT 0 CHECK(is_locked IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK(NOT(status = 'deleted' AND is_locked = 1))
);

CREATE INDEX IF NOT EXISTS idx_records_status ON records(status);
CREATE INDEX IF NOT EXISTS idx_records_category ON records(category);
"""

UNIQUE_SOURCE_HASH_INDEX_SQL = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_records_source_hash_unique
ON records(source_hash)
WHERE source_hash IS NOT NULL AND source_hash <> '';
"""


class ClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback) -> bool | None:
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def resolve_db_path(db_path: str | Path | None = None) -> Path:
    """Return the concrete database path without creating the database."""

    return Path(db_path).expanduser().resolve() if db_path else DEFAULT_DB_PATH


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def normalized_content_hash(content: str) -> str:
    return content_hash(normalize_content(content))


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, factory=ClosingConnection)
    connection.row_factory = sqlite3.Row
    return connection


def connect_readonly(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = resolve_db_path(db_path)
    if not path.exists():
        raise FileNotFoundError(path)
    connection = sqlite3.connect(
        f"file:{path.as_posix()}?mode=ro",
        uri=True,
        factory=ClosingConnection,
    )
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: str | Path | None = None) -> Path:
    path = resolve_db_path(db_path)
    with connect(path) as connection:
        connection.executescript(SCHEMA)
        ensure_schema_migrations(connection)
        ensure_database_indexes(connection)
    return path


def ensure_schema_migrations(connection: sqlite3.Connection) -> None:
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(records)").fetchall()
    }
    if "is_locked" not in columns:
        connection.execute(
            "ALTER TABLE records ADD COLUMN is_locked INTEGER NOT NULL DEFAULT 0"
        )


def ensure_database_indexes(connection: sqlite3.Connection) -> None:
    duplicate_rows = connection.execute(
        """
        SELECT source_hash, group_concat(id) AS ids, count(*) AS count
        FROM records
        WHERE source_hash IS NOT NULL AND source_hash <> ''
        GROUP BY source_hash
        HAVING count > 1
        """
    ).fetchall()
    if duplicate_rows:
        details = "; ".join(
            f"{row['source_hash']}: records {row['ids']}" for row in duplicate_rows
        )
        raise ValueError(
            "cannot enforce unique content hashes while duplicates exist: "
            f"{details}"
        )
    connection.execute(UNIQUE_SOURCE_HASH_INDEX_SQL)


def parse_tags(tags: str | Sequence[str] | None) -> list[str]:
    if tags is None:
        return []
    if isinstance(tags, str):
        raw_tags = re.split(r"[,，]", tags)
    else:
        raw_tags = list(tags)
    normalized: list[str] = []
    seen: set[str] = set()
    for tag in raw_tags:
        value = str(tag).strip()
        if value and value not in seen:
            normalized.append(value)
            seen.add(value)
    return normalized


def tags_to_json(tags: str | Sequence[str] | None) -> str:
    return json.dumps(parse_tags(tags), ensure_ascii=False)


def tags_from_json(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed]


def make_slug(title: str, category: str, content: str) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "-", title.strip().lower()).strip("-")
    if not base:
        base = re.sub(r"[^a-zA-Z0-9]+", "-", category.strip().lower()).strip("-")
    if not base:
        base = "record"
    return f"{base[:48]}-{content_hash(content)[:10]}"


def make_unique_slug(
    connection: sqlite3.Connection,
    title: str,
    category: str,
    content: str,
) -> str:
    base = make_slug(title, category, content)
    slug = base
    suffix = 2
    while connection.execute("SELECT 1 FROM records WHERE slug = ?", (slug,)).fetchone():
        slug = f"{base}-{suffix}"
        suffix += 1
    return slug


def normalize_content(content: str) -> str:
    return content.replace("\r\n", "\n").replace("\r", "\n").strip()


def validate_record_fields(title: str, category: str, content: str) -> tuple[str, str, str]:
    title = title.strip()
    category = category.strip()
    content = normalize_content(content)
    if not title:
        raise ValueError("title cannot be empty")
    if not category:
        raise ValueError("category cannot be empty")
    if not content:
        raise ValueError("content cannot be empty")
    return title, category, content


def row_to_record(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    record = dict(row)
    record["tags"] = tags_from_json(record.get("tags_json"))
    record["is_locked"] = bool(record.get("is_locked", 0))
    return record


def get_record(record_id: int, db_path: str | Path | None = None) -> dict | None:
    initialize_database(db_path)
    with connect(db_path) as connection:
        row = connection.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    return row_to_record(row)


def get_record_readonly(record_id: int, db_path: str | Path | None = None) -> dict | None:
    """Return one record without creating, migrating, or indexing the database."""

    with connect_readonly(db_path) as connection:
        row = connection.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    return row_to_record(row)


def list_records(
    *,
    db_path: str | Path | None = None,
    search: str | None = None,
    include_deleted: bool = False,
    category: str | None = None,
    limit: int | None = None,
) -> list[dict]:
    initialize_database(db_path)
    if limit is not None and limit < 1:
        raise ValueError("limit must be a positive integer")
    clauses: list[str] = []
    params: list[object] = []
    if not include_deleted:
        clauses.append("status = 'active'")
    if category:
        clauses.append("category = ?")
        params.append(category)
    if search:
        like = f"%{search}%"
        clauses.append(
            "(title LIKE ? OR category LIKE ? OR content LIKE ? OR tags_json LIKE ?)"
        )
        params.extend([like, like, like, like])

    query = "SELECT * FROM records"
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY id ASC"
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    with connect(db_path) as connection:
        rows = connection.execute(query, params).fetchall()
    return [row_to_record(row) for row in rows if row is not None]


def add_record(
    *,
    title: str,
    category: str,
    content: str,
    tags: str | Sequence[str] | None = None,
    db_path: str | Path | None = None,
    source_file: str | None = None,
    source_block_index: int | None = None,
    source_start_line: int | None = None,
    source_end_line: int | None = None,
    source_hash: str | None = None,
    status: str = "active",
    is_locked: bool = False,
) -> dict:
    title, category, content = validate_record_fields(title, category, content)
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")
    if status == "deleted" and is_locked:
        raise ValueError("deleted records cannot be locked")

    now = utc_now()
    computed_hash = normalized_content_hash(content)
    if source_hash is not None and str(source_hash).strip() != computed_hash:
        raise ValueError("source_hash does not match normalized content")
    source_hash = computed_hash
    initialize_database(db_path)
    with connect(db_path) as connection:
        duplicate = find_duplicate_by_hash(connection, source_hash)
        if duplicate is not None:
            raise ValueError(
                "duplicate content already exists as "
                f"record {duplicate['id']} ({display_state(duplicate)})"
            )
        slug = make_unique_slug(connection, title, category, content)
        cursor = connection.execute(
            """
            INSERT INTO records(
                slug, title, category, content, tags_json, source_file,
                source_block_index, source_start_line, source_end_line,
                source_hash, status, is_locked, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                slug,
                title,
                category,
                content,
                tags_to_json(tags),
                source_file,
                source_block_index,
                source_start_line,
                source_end_line,
                source_hash,
                status,
                int(is_locked),
                now,
                now,
            ),
        )
        record_id = int(cursor.lastrowid)
    record = get_record(record_id, db_path)
    if record is None:
        raise RuntimeError("record was inserted but could not be read back")
    return record


def update_record(
    record_id: int,
    *,
    db_path: str | Path | None = None,
    title: str | None = None,
    category: str | None = None,
    content: str | None = None,
    tags: str | Sequence[str] | None = None,
) -> dict:
    current = get_record(record_id, db_path)
    if current is None:
        raise KeyError(f"record not found: {record_id}")
    ensure_active_unlocked(current, action="update")

    new_title = current["title"] if title is None else title
    new_category = current["category"] if category is None else category
    new_content = current["content"] if content is None else content
    new_title, new_category, new_content = validate_record_fields(
        new_title,
        new_category,
        new_content,
    )
    new_tags_json = current["tags_json"] if tags is None else tags_to_json(tags)
    new_source_hash = normalized_content_hash(new_content)
    if new_source_hash != current.get("source_hash"):
        with connect(db_path) as connection:
            duplicate = find_duplicate_by_hash(connection, new_source_hash, exclude_id=record_id)
        if duplicate is not None:
            raise ValueError(
                "duplicate content already exists as "
                f"record {duplicate['id']} ({display_state(duplicate)})"
            )

    with connect(db_path) as connection:
        connection.execute(
            """
            UPDATE records
            SET title = ?, category = ?, content = ?, tags_json = ?,
                source_hash = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                new_title,
                new_category,
                new_content,
                new_tags_json,
                new_source_hash,
                utc_now(),
                record_id,
            ),
        )
    record = get_record(record_id, db_path)
    if record is None:
        raise RuntimeError("record was updated but could not be read back")
    return record


def set_record_status(record_id: int, status: str, db_path: str | Path | None = None) -> dict:
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")
    current = get_record(record_id, db_path)
    if current is None:
        raise KeyError(f"record not found: {record_id}")
    if status == "deleted":
        ensure_active_unlocked(current, action="delete")
    if status == "active":
        ensure_status(current, "deleted", action="restore")
        source_hash = current.get("source_hash")
        if source_hash:
            with connect(db_path) as connection:
                duplicate = find_duplicate_by_hash(
                    connection,
                    str(source_hash),
                    exclude_id=record_id,
                    statuses={"active"},
                )
            if duplicate is not None:
                raise ValueError(
                    "cannot restore because duplicate active content exists as "
                    f"record {duplicate['id']}"
                )
    with connect(db_path) as connection:
        connection.execute(
            "UPDATE records SET status = ?, is_locked = 0, updated_at = ? WHERE id = ?",
            (status, utc_now(), record_id),
        )
    record = get_record(record_id, db_path)
    if record is None:
        raise RuntimeError("record status was changed but could not be read back")
    return record


def soft_delete_record(record_id: int, db_path: str | Path | None = None) -> dict:
    return set_record_status(record_id, "deleted", db_path)


def restore_record(record_id: int, db_path: str | Path | None = None) -> dict:
    return set_record_status(record_id, "active", db_path)


def lock_record(record_id: int, db_path: str | Path | None = None) -> dict:
    current = get_record(record_id, db_path)
    if current is None:
        raise KeyError(f"record not found: {record_id}")
    ensure_status(current, "active", action="lock")
    if current["is_locked"]:
        raise ValueError(f"record {record_id} is already locked")
    with connect(db_path) as connection:
        connection.execute(
            "UPDATE records SET is_locked = 1, updated_at = ? WHERE id = ?",
            (utc_now(), record_id),
        )
    record = get_record(record_id, db_path)
    if record is None:
        raise RuntimeError("record was locked but could not be read back")
    return record


def unlock_record(record_id: int, db_path: str | Path | None = None) -> dict:
    current = get_record(record_id, db_path)
    if current is None:
        raise KeyError(f"record not found: {record_id}")
    ensure_status(current, "active", action="unlock")
    if not current["is_locked"]:
        raise ValueError(f"record {record_id} is not locked")
    with connect(db_path) as connection:
        connection.execute(
            "UPDATE records SET is_locked = 0, updated_at = ? WHERE id = ?",
            (utc_now(), record_id),
        )
    record = get_record(record_id, db_path)
    if record is None:
        raise RuntimeError("record was unlocked but could not be read back")
    return record


def hard_delete_record(record_id: int, db_path: str | Path | None = None) -> dict:
    current = get_record(record_id, db_path)
    if current is None:
        raise KeyError(f"record not found: {record_id}")
    ensure_status(current, "deleted", action="hard-delete")
    with connect(db_path) as connection:
        connection.execute("DELETE FROM records WHERE id = ?", (record_id,))
    return current


def source_hash_exists(source_hash: str, db_path: str | Path | None = None) -> bool:
    initialize_database(db_path)
    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT 1 FROM records WHERE source_hash = ? LIMIT 1",
            (source_hash,),
        ).fetchone()
    return row is not None


def record_value(record: Mapping[str, object] | sqlite3.Row, key: str) -> object:
    if isinstance(record, sqlite3.Row):
        return record[key]
    return record.get(key)


def display_state(record: Mapping[str, object] | sqlite3.Row) -> str:
    if record_value(record, "status") == "deleted":
        return "deleted"
    if bool(record_value(record, "is_locked")):
        return "locked"
    return "active"


def ensure_status(record: Mapping[str, object] | sqlite3.Row, expected: str, *, action: str) -> None:
    if record_value(record, "status") != expected:
        raise ValueError(
            f"cannot {action} record {record_value(record, 'id')}: "
            f"state is {display_state(record)}"
        )


def ensure_active_unlocked(record: Mapping[str, object] | sqlite3.Row, *, action: str) -> None:
    ensure_status(record, "active", action=action)
    if bool(record_value(record, "is_locked")):
        raise ValueError(f"cannot {action} locked record {record_value(record, 'id')}")


def find_duplicate_by_hash(
    connection: sqlite3.Connection,
    source_hash: str,
    *,
    exclude_id: int | None = None,
    statuses: set[str] | None = None,
) -> sqlite3.Row | None:
    clauses = ["source_hash = ?"]
    params: list[object] = [source_hash]
    if exclude_id is not None:
        clauses.append("id <> ?")
        params.append(exclude_id)
    if statuses is not None:
        placeholders = ", ".join("?" for _ in statuses)
        clauses.append(f"status IN ({placeholders})")
        params.extend(sorted(statuses))
    query = "SELECT * FROM records WHERE " + " AND ".join(clauses) + " LIMIT 1"
    return connection.execute(query, params).fetchone()


def validate_database_integrity(db_path: str | Path | None = None) -> list[str]:
    """Return read-only integrity warnings for the local prompt database."""

    issues: list[str] = []
    content_hashes: dict[str, list[int]] = {}
    source_hashes: dict[str, list[int]] = {}
    try:
        with connect_readonly(db_path) as connection:
            rows = connection.execute(
                """
                SELECT id, title, category, content, source_hash, status, is_locked
                FROM records
                ORDER BY id ASC
                """
            ).fetchall()
    except FileNotFoundError:
        return [f"database does not exist: {resolve_db_path(db_path)}"]
    except sqlite3.Error as exc:
        return [f"database cannot be read: {exc}"]

    for row in rows:
        record_id = int(row["id"])
        status = str(row["status"])
        locked_raw = row["is_locked"]
        is_locked = bool(locked_raw)
        title = str(row["title"] or "").strip()
        category = str(row["category"] or "").strip()
        content = normalize_content(str(row["content"] or ""))
        source_hash = str(row["source_hash"] or "").strip()

        if status not in VALID_STATUSES:
            issues.append(f"record {record_id} has invalid status: {status}")
        if locked_raw not in (0, 1, False, True):
            issues.append(f"record {record_id} has invalid is_locked value: {locked_raw}")
        if status == "deleted" and is_locked:
            issues.append(f"record {record_id} is deleted but still locked")
        if not title:
            issues.append(f"record {record_id} has empty title")
        if not category:
            issues.append(f"record {record_id} has empty category")
        if not content:
            issues.append(f"record {record_id} has empty content")

        computed_hash = normalized_content_hash(content)
        content_hashes.setdefault(computed_hash, []).append(record_id)
        if source_hash:
            source_hashes.setdefault(source_hash, []).append(record_id)
            if source_hash != computed_hash:
                issues.append(f"record {record_id} source_hash does not match content")

    for duplicate_ids in content_hashes.values():
        if len(duplicate_ids) > 1:
            ids = ", ".join(str(record_id) for record_id in duplicate_ids)
            issues.append(f"records share identical content: {ids}")
    for duplicate_ids in source_hashes.values():
        if len(duplicate_ids) > 1:
            ids = ", ".join(str(record_id) for record_id in duplicate_ids)
            issues.append(f"records share identical source_hash: {ids}")

    return issues


def import_blocks(
    blocks: Iterable[Mapping[str, object]],
    *,
    db_path: str | Path | None = None,
) -> dict[str, object]:
    initialize_database(db_path)
    imported: list[dict] = []
    skipped: list[Mapping[str, object]] = []
    for block in blocks:
        block_content = str(block["content"])
        block_hash = normalized_content_hash(block_content)
        supplied_hash = block.get("source_hash")
        if supplied_hash is not None and str(supplied_hash).strip() != block_hash:
            raise ValueError(
                "source block hash does not match content: "
                f"block {block.get('source_block_index')}"
            )
        if source_hash_exists(block_hash, db_path):
            skipped.append(block)
            continue
        imported.append(
            add_record(
                db_path=db_path,
                title=str(block["title"]),
                category=str(block["category"]),
                content=block_content,
                tags=block.get("tags"),
                source_file=str(block.get("source_file") or ""),
                source_block_index=int(block["source_block_index"]),
                source_start_line=int(block["source_start_line"]),
                source_end_line=int(block["source_end_line"]),
                source_hash=block_hash,
            )
        )
    return {"imported": imported, "skipped": skipped}
