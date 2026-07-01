def section(title):
    print()
    print('=' * 64)
    print(title)
    print('=' * 64)


def predict(question):
    print('[Predict]', question)


def main():
    keys = ['menu.start', 'menu.options', 'menu.quit']

    section('1. direct iteration when the element is enough')
    predict('Do we need indexes to print every key?')
    for key in keys:
        print('key ->', key)

    section('2. enumerate when position is part of the result')
    predict('Which object is the line number, and which object is the key?')
    for line_no, key in enumerate(keys, start=1):
        print('line', line_no, 'key', key)

    section('3. zip when two streams should advance together')
    source_texts = ['Start', 'Options', 'Quit']
    target_texts = ['开始', '选项', '退出']
    for key, source, target in zip(keys, source_texts, target_texts):
        print(key, '->', source, '/', target)

    section('4. range when you need counts or neighbor indexes')
    for retry in range(3):
        print('retry number ->', retry + 1)
    for index in range(len(keys) - 1):
        print('adjacent pair ->', keys[index], keys[index + 1])
    print('Rule: range(len(seq)) is not the default choice for ordinary element loops.')


if __name__ == '__main__':
    main()
