```python
def strip_text(text):
    return text.strip()


def lowercase_text(text):
    return text.lower()


def collapse_spaces(text):
    return " ".join(text.split())


def apply_pipeline(value, steps):
    for step in steps:
        if not callable(step):
            raise TypeError(
                f"pipeline item is not callable: {step!r}"
            )

        value = step(value)

    return value


SOURCE_PIPELINE = [
    strip_text,
    collapse_spaces,
]

KEY_PIPELINE = [
    strip_text,
    lowercase_text,
]

source = apply_pipeline(
    "  Start   New   Game  ",
    SOURCE_PIPELINE,
)

key = apply_pipeline(
    "  UI.MENU.START  ",
    KEY_PIPELINE,
)

print(source)
print(key)
```

```tex
函数名：
    apply_pipeline

输入：
    value：
        初始对象

    steps：
        可迭代对象，其中每个元素都应能以
        step(current_value) 的形式被调用

正常返回：
    最后一个步骤的调用结果；
    若 steps 为空，则返回初始 value

输入对象修改：
    apply_pipeline 自身只重新绑定局部名字 value；
    但具体 step 是否修改共享对象，取决于 step 的合同

显示输出：
    无

外部 I/O：
    apply_pipeline 自身无显式 I/O；
    具体 step 可能有副作用

异常：
    遇到不可调用元素时主动抛出 TypeError；
    任一 step 的参数错误、业务错误或其他异常也可能传播
```

这张合同卡揭示了一个重要边界：

> 高层函数自身没有显式副作用，不代表它调用的函数对象也没有副作用。
