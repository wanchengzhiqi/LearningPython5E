#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Focused self-checks for prompt_template_manager.

This file intentionally lives beside the tool instead of the repository-level
tests/ directory, which is reserved as historical learning data in this repo.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from import_test_demo import (
    DEFAULT_SOURCE,
    LEGACY_TEST_DEMO_SOURCE,
    import_prompt_source,
    parse_prompt_source,
    parse_test_demo,
)
from prompt_store import (
    add_record,
    display_state,
    get_record,
    get_record_readonly,
    hard_delete_record,
    list_records,
    lock_record,
    restore_record,
    soft_delete_record,
    unlock_record,
    validate_database_integrity,
)


class PromptManagerSelfCheck(unittest.TestCase):
    def make_db_path(self) -> Path:
        handle, raw_path = tempfile.mkstemp(
            prefix="prompt_manager_self_check_",
            suffix=".sqlite3",
        )
        os.close(handle)
        path = Path(raw_path)
        path.unlink()
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        return path

    def make_source_path(self, text: str) -> Path:
        handle, raw_path = tempfile.mkstemp(
            prefix="prompt_manager_source_",
            suffix=".py",
        )
        os.close(handle)
        path = Path(raw_path)
        path.write_text(text, encoding="utf-8")
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        return path

    def test_default_source_parse_count(self) -> None:
        blocks = parse_prompt_source()

        self.assertEqual(len(blocks), 12)
        self.assertEqual(blocks[0].category, "source_note")
        self.assertEqual(blocks[-1].category, "reasoning_exam_request")
        self.assertEqual(DEFAULT_SOURCE.parent.name, "sample_data")
        self.assertEqual(DEFAULT_SOURCE.name, "prompt_templates_demo.py")

    def test_legacy_test_demo_is_explicit_compatibility_source(self) -> None:
        self.assertEqual(LEGACY_TEST_DEMO_SOURCE.parent.name, "tests")
        self.assertEqual(LEGACY_TEST_DEMO_SOURCE.name, "test_demo.py")

    def test_custom_source_starts_at_first_line_by_default(self) -> None:
        source_path = self.make_source_path(
            "# first custom prompt\n"
            "\n"
            "# second custom prompt\n"
        )

        blocks = parse_prompt_source(source_path)

        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].content, "first custom prompt")
        self.assertEqual(blocks[0].source_start_line, 1)

    def test_custom_source_accepts_utf8_bom(self) -> None:
        source_path = self.make_source_path(
            "\ufeff# first custom prompt\n"
            "\n"
            "# second custom prompt\n"
        )

        blocks = parse_prompt_source(source_path)

        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].content, "first custom prompt")

    def test_legacy_named_parser_accepts_explicit_source(self) -> None:
        source_path = self.make_source_path(
            "#!/usr/bin/env python\n"
            "# -*- coding: utf-8 -*-\n"
            "# temporary compatibility source\n"
            "\n"
            "# 第一条兼容样例\n"
            "\n"
            "# 第二条兼容样例\n"
        )
        blocks = parse_test_demo(source_path)

        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].title, "第一条兼容样例")
        self.assertEqual(blocks[0].source_file, str(source_path))

    def test_import_is_idempotent(self) -> None:
        db_path = self.make_db_path()

        first = import_prompt_source(db_path=db_path)
        second = import_prompt_source(db_path=db_path)

        self.assertEqual(len(first["imported"]), 12)
        self.assertEqual(len(second["imported"]), 0)
        self.assertEqual(len(second["skipped"]), 12)
        self.assertEqual(len(list_records(db_path=db_path, include_deleted=True)), 12)
        self.assertEqual(validate_database_integrity(db_path), [])

    def test_source_hash_must_match_content(self) -> None:
        db_path = self.make_db_path()

        with self.assertRaisesRegex(ValueError, "source_hash"):
            add_record(
                title="Bad hash",
                category="manual",
                content="real content",
                source_hash="not-the-real-hash",
                db_path=db_path,
            )

    def test_state_machine_and_duplicate_content_guards(self) -> None:
        db_path = self.make_db_path()
        record = add_record(
            title="State sample",
            category="manual",
            content="stateful content",
            db_path=db_path,
        )

        locked = lock_record(record["id"], db_path)
        self.assertEqual(display_state(locked), "locked")
        with self.assertRaisesRegex(ValueError, "locked"):
            soft_delete_record(record["id"], db_path)

        unlocked = unlock_record(record["id"], db_path)
        self.assertEqual(display_state(unlocked), "active")
        deleted = soft_delete_record(record["id"], db_path)
        self.assertEqual(display_state(deleted), "deleted")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            add_record(
                title="Duplicate sample",
                category="manual",
                content="stateful content",
                db_path=db_path,
            )

        restored = restore_record(record["id"], db_path)
        self.assertEqual(display_state(restored), "active")
        soft_delete_record(record["id"], db_path)
        hard_delete_record(record["id"], db_path)
        self.assertIsNone(get_record(record["id"], db_path))

    def test_integrity_check_is_read_only_for_missing_database(self) -> None:
        db_path = self.make_db_path()

        issues = validate_database_integrity(db_path)

        self.assertEqual(len(issues), 1)
        self.assertIn("database does not exist", issues[0])
        self.assertFalse(db_path.exists())

    def test_readonly_record_lookup_does_not_initialize_missing_database(self) -> None:
        db_path = self.make_db_path()

        with self.assertRaises(FileNotFoundError):
            get_record_readonly(1, db_path)

        self.assertFalse(db_path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
