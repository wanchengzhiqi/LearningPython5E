def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def main():
    section('1. removing from the same list can skip elements')
    predict('How many empty strings remain after the unsafe loop?')
    unsafe = ['ok', '', '', 'keep']
    for value in unsafe:
        if value == '':
            unsafe.remove(value)
    print('unsafe result ->', unsafe)

    section('2. build a new list when filtering')
    original = ['ok', '', '', 'keep']
    safe = []
    for value in original:
        if value:
            safe.append(value)
    print('original ->', original)
    print('safe ->', safe)

    section('3. changing dict size during iteration raises an error')
    resources = {'menu.start': 'Start', 'debug.temp': 'Temp', 'menu.quit': 'Quit'}
    try:
        for key in resources:
            if key.startswith('debug.'):
                del resources[key]
    except RuntimeError as exc:
        print('RuntimeError ->', exc)
    print('after failed loop ->', resources)

    section('4. collect keys first, mutate after traversal')
    resources = {'menu.start': 'Start', 'debug.temp': 'Temp', 'menu.quit': 'Quit'}
    to_delete = []
    for key in resources:
        if key.startswith('debug.'):
            to_delete.append(key)
    for key in to_delete:
        del resources[key]
    print('safe dict result ->', resources)


if __name__ == '__main__':
    main()
