def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def main():
    section('1. while rechecks current state')
    predict('How many rounds run, and what changes the exit condition?')
    pending = ['menu.start', 'menu.options', 'menu.quit']
    round_no = 1
    while pending:
        print('round', round_no, 'condition sees', pending)
        key = pending.pop(0)
        print('  process', repr(key), 'and mutate the list')
        round_no += 1
    print('after loop ->', pending)

    section('2. progress must happen inside the body')
    predict('Which assignment prevents an infinite loop?')
    retries = 3
    while retries > 0:
        print('retry, remaining ->', retries)
        retries -= 1
    print('after loop ->', retries)

    section('3. object first, truth result second')
    batches = [['menu.start'], [], ['menu.quit']]
    index = 0
    while index < len(batches):
        batch = batches[index]
        print('batch=', batch, 'bool(batch)=', bool(batch))
        index += 1
    print('Rule: batch remains a list; bool(batch) is only the truth result.')


if __name__ == '__main__':
    main()
