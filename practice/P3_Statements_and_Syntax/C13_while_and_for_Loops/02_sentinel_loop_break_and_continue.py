def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def main():
    section('1. sentinel loop: read until QUIT')
    predict('Which commands are appended, skipped, or never read?')
    incoming = iter(['preview', '', 'SKIP', 'write', 'QUIT', 'ignored'])
    processed = []

    while True:
        command = next(incoming, 'QUIT')
        print('read ->', repr(command))
        if command == 'QUIT':
            print('  break stops the whole loop')
            break
        if not command:
            print('  continue skips blank input')
            continue
        if command == 'SKIP':
            print('  continue skips explicit marker')
            continue
        processed.append(command.lower())
        print('  appended normalized command')
    print('processed ->', processed)

    section('2. continue is not break')
    predict('Will values after the first even number still be visited?')
    odds = []
    for number in [1, 2, 3, 4]:
        if number % 2 == 0:
            print('continue at', number)
            continue
        odds.append(number)
        print('append odd ->', number)
    print('odds ->', odds)


if __name__ == '__main__':
    main()
