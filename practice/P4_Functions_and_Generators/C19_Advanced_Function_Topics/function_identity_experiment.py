import sys

trace_calls = []


def tracer(frame, event, arg):
    if event == "call" and frame.f_code.co_name in ("mark", "choose"):
        trace_calls.append(frame.f_code.co_name)
    return tracer


def mark(text):
    print("MARK", text)
    return text.upper()


def choose():
    return mark


sys.settrace(tracer)

box = [mark]
a = mark
b = box[0]
c = choose()

print("before c('save'):")
print("trace_calls:", trace_calls)
print("same function object? mark is a is b is c ->",
      mark is a is b is c)

result = c("save")

print("after c('save'):")
print("trace_calls:", trace_calls)
print("result:", result)
print("identity still holds:", mark is a is b is c)

sys.settrace(None)
