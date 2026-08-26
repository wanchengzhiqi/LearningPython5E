import sys
print("PYTHON:", sys.version)
print("=" * 50)


def build_job(
    source,
    *files,
    language="zh-CN",
    **options,
):
    print("source:", source)
    print("files:", files)
    print("language:", language)
    print("options:", options)


build_job(
    "main.csv",
    "extra01.csv",
    "extra02.csv",
    language="ja-JP",
    encoding="utf-8",
    strict=True,
)
