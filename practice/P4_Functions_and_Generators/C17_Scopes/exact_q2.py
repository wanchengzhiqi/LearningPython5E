import sys
print(sys.version)
print('----- version A: print(y) kept -----')

def outer():
    x, y = 10, 12

    def middle():
        print(locals())
        print(y)  # 如果这行被注释掉，整个代码片段的输出会变化吗？为什么？

        def inner():
            nonlocal x
            x = 2
            y = 20
            print(locals())

            return x

        return inner

    return middle


print(outer()()())

print('----- version B: print(y) commented out -----')

def outer():
    x, y = 10, 12

    def middle():
        print(locals())
        # print(y)  # 这行被注释掉

        def inner():
            nonlocal x
            x = 2
            y = 20
            print(locals())

            return x

        return inner

    return middle


print(outer()()())
