import dis

def outer():
    x, y = 10, 12

    def middle():
        print(locals())
        print(y)  # kept

        def inner():
            nonlocal x
            x = 2
            y = 20
            print(locals())
            return x

        return inner

    return middle

middle = outer()
inner = middle()

for label, f in [("outer", outer), ("middle", middle), ("inner", inner)]:
    print("=" * 30, label, "=" * 30)
    dis.dis(f)
