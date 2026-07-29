```python
def make_issue(
    code: str,
    message: str,
    severity: str = "error",
) -> dict[str, str]:
    """Build one localization issue record.

    This function returns a new dictionary and does not perform I/O.
    """
    return {
        "code": code,
        "message": message,
        "severity": severity,
    }
```
```tex
函数对象名称：
    make_issue

签名：
    (code: str,
     message: str,
     severity: str = "error")
    -> dict[str, str]

输入意图：
    code、message 和 severity 预期为字符串

运行期类型强制：
    注解本身不强制

正常返回：
    一个新字典，包含 code、message、severity

显示输出：
    无

输入对象修改：
    当前函数体不对实参对象执行原地修改

外部 I/O：
    无

可能异常：
    当前简单字典构造通常无需特定业务异常；
    但注解不保证任意自定义对象或后续实现永不出错

证据边界：
    docstring 和注解表达设计意图；
    函数体、测试和实际调用用于验证当前行为
```
