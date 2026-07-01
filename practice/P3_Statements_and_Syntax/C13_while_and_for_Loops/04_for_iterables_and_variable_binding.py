from pathlib import Path


def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def main():
    section('1. for takes elements from different iterables')
    predict('What does the loop variable bind to in each loop?')
    for char in 'ui':
        print('string char ->', char)
    for key in {'menu.start': 'Start', 'menu.quit': 'Quit'}:
        print('dict key ->', key)
    for tag in {'system', 'ui'}:
        print('set element, order is not a contract ->', tag)
    sample_path = Path(__file__).with_name('sample_c13_resource_lines.txt')
    with sample_path.open(encoding='utf-8') as file:
        for line in file:
            print('file line ->', line.rstrip('\n'))

    section('2. loop variable rebinding does not copy elements')
    records = [{'key': 'menu.start', 'seen': False}, {'key': 'menu.quit', 'seen': False}]
    for record in records:
        print('before ->', record)
        record['seen'] = True
        record = {'key': 'local-only'}
        print('local rebound ->', record)
    print('records after mutation and rebinding ->', records)
    print('Rule: item is rebound each round; mutable element objects can still be changed.')


if __name__ == '__main__':
    main()
