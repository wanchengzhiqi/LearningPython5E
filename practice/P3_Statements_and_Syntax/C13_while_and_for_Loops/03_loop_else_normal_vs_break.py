def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def find_key(records, target):
    for record in records:
        print('visit ->', record['key'])
        if record['key'] == target:
            print('  break: found target')
            break
    else:
        print('  else: loop exhausted without break')
        return None
    return record


def retry_until_ok(responses):
    attempts = 0
    while attempts < len(responses):
        value = responses[attempts]
        print('attempt', attempts + 1, '->', value)
        attempts += 1
        if value == 'ok':
            break
    else:
        return 'all attempts failed'
    return 'stopped early after success'


def main():
    records = [{'key': 'menu.start'}, {'key': 'menu.quit'}]

    section('1. for else runs only when no break happens')
    predict('Will the else block run when target is present?')
    print('result ->', find_key(records, 'menu.quit'))

    section('2. exhausted search triggers else')
    predict('Will the else block run when target is absent?')
    print('result ->', find_key(records, 'menu.options'))

    section('3. while else follows the same no-break rule')
    print(retry_until_ok(['fail', 'fail']))
    print(retry_until_ok(['fail', 'ok', 'ignored']))


if __name__ == '__main__':
    main()
