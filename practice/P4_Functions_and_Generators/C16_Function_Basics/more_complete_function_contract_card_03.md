```python
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def save_summary(report, path):
    text = f"Issues: {len(report['issues'])}\n"

    report["saved"] = True
    logger.info("Saving report to %s", path)

    written = Path(path).write_text(
        text,
        encoding="utf-8",
    )

    print("Report saved")

    return written
```
```tex
函数名：
    save_summary

输入：
    report：包含 issues 的可变映射
    path：Path 可接受的路径输入

正常返回：
    写入的字符数

输入对象修改：
    将 report["saved"] 设置为 True

显示输出：
    向默认标准输出写入 "Report saved"

日志：
    产生一条 INFO 记录

外部 I/O：
    以 UTF-8 覆盖写入目标文件

异常：
    缺失 issues 时可能抛出 KeyError
    路径或权限问题可能抛出 OSError 等异常

部分失败边界：
    某些副作用可能在后续异常前已经发生
```
