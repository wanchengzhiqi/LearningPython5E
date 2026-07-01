import re


PLACEHOLDER_RE = re.compile(r'\{[a-z_]+\}')


def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def placeholders(text):
    return set(PLACEHOLDER_RE.findall(text))


def audit_records(records, *, strict=False, max_length=12):
    issues = []
    checked = []
    completed_without_break = False

    for record in records:
        key = record['key']
        if not record.get('enabled', True):
            continue

        source = record['source']
        target = record.get('target')
        if target is None:
            issues.append({'key': key, 'kind': 'missing-target'})
            if strict:
                break
            continue

        checked.append(key)
        if target == '':
            issues.append({'key': key, 'kind': 'empty-target'})
            continue
        if placeholders(source) != placeholders(target):
            issues.append({'key': key, 'kind': 'placeholder-mismatch'})
        if len(target) > max_length:
            issues.append({'key': key, 'kind': 'too-long'})
    else:
        completed_without_break = True

    return {
        'status': 'blocked' if strict and not completed_without_break else 'review',
        'checked': checked,
        'issues': issues,
        'completed_without_break': completed_without_break,
    }


def main():
    records = [
        {'key': 'menu.start', 'source': 'Start {player}', 'target': '开始 {player}'},
        {'key': 'menu.debug', 'source': 'Debug', 'target': '调试', 'enabled': False},
        {'key': 'menu.options', 'source': 'Options', 'target': ''},
        {'key': 'menu.score', 'source': 'Score {points}', 'target': '分数'},
        {'key': 'menu.quit', 'source': 'Quit', 'target': None},
    ]

    section('1. collect all issues in non-strict mode')
    predict('Which records are skipped, checked, or reported?')
    print(audit_records(records, strict=False))

    section('2. strict mode stops at the first missing target')
    predict('Will loop else run after break?')
    print(audit_records(records, strict=True))
    print('Rule: this function returns data; it does not write a report file.')


if __name__ == '__main__':
    main()
