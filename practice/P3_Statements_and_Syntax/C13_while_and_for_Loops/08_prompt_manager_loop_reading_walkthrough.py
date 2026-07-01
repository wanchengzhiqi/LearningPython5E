from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PROMPT_MANAGER_DIR = REPO_ROOT / 'projects' / 'P3_Statements_and_Syntax' / 'prompt_template_manager'
sys.path.insert(0, str(PROMPT_MANAGER_DIR))

from prompt_store import normalized_content_hash, parse_tags  # noqa: E402


def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def source_loop_lines(limit=10):
    path = PROMPT_MANAGER_DIR / 'prompt_store.py'
    found = []
    for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(('for ', 'while ')) or stripped == 'continue':
            found.append((line_no, stripped))
            if len(found) >= limit:
                break
    return found


def simulate_import_blocks(blocks, existing_hashes):
    imported = []
    skipped = []
    for block in blocks:
        block_hash = normalized_content_hash(block['content'])
        if block_hash in existing_hashes:
            skipped.append(block['title'])
            continue
        imported.append(block['title'])
        existing_hashes.add(block_hash)
    return {'imported': imported, 'skipped': skipped}


def main():
    section('1. parse_tags loops over normalized raw tags')
    predict('Which empty or duplicate tags are skipped?')
    print(parse_tags(' imported, , C13, imported，loops '))

    section('2. read real loop lines from prompt_store.py')
    predict('Which lines use for, while, or continue?')
    for line_no, text in source_loop_lines():
        print(line_no, '->', text)

    section('3. simulate import_blocks without opening the database')
    blocks = [
        {'title': 'first', 'content': 'Prompt A'},
        {'title': 'duplicate', 'content': 'Prompt A'},
        {'title': 'second', 'content': 'Prompt B'},
    ]
    existing = {normalized_content_hash('Prompt A')}
    print(simulate_import_blocks(blocks, existing))
    print('Safety: no SQLite connection is opened or modified.')


if __name__ == '__main__':
    main()
