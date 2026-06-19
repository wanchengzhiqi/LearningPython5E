# Prompt Template Manager

`prompt_template_manager` 是 `P3_Statements_and_Syntax` 下的本地支持性小工具。
它把项目内置样例中的 prompt 模板和说明性内容导入 SQLite，并
提供一个简单的 tkinter GUI 和一个命令行 CRUD 入口。

## 核心边界

- 默认导入来源是项目目录内的
  `sample_data/prompt_templates_demo.py`，这是一份长期保留的稳定样例。
- 导入后，SQLite 数据库才是真实数据源。
- 后续覆写、清空、移动或删除任意来源文件，都不会改变数据库中已保存的记录。
- 工具不会自动同步，也不会双向写回任何来源文件。
- `tests/test_demo.py` 仅作为历史兼容输入保留：只有用户显式运行 CLI 的
  `import-test-demo --legacy-test-demo`，才会只读解析它。
- 再次导入默认按 `source_hash` 跳过已存在内容，不覆盖数据库里的已有记录。
- 新增验证、自检和运行产物都不应落入仓库根目录的 `tests/`。

## 版本规则

当前版本新增了更严格的记录状态机：

- 记录列表默认按 `id ASC` 排序，修改、锁定、软删除和恢复不会让记录跳到顶部。
- `active` 记录可以修改、软删除或锁定。
- `locked` 记录只允许解锁，不允许修改、软删除、恢复或真删除。
- `deleted` 记录只允许恢复或真删除，不允许修改、软删除、锁定或解锁。
- `hard-delete` / “真删除”只允许作用于已经软删除的记录，执行后记录会从数据库
  中永久移除，不能再展示、搜索、修改或恢复。
- 新增和修改内容时，会按内容哈希阻止重复记录；这也避免了“新增一条与软删除
  记录完全相同的记录后，再恢复旧记录”造成的重复数据问题。
- `source_hash` 必须等于规范化后的 `content` 哈希。导入器、CLI 和 GUI 都不能
  写入“内容与哈希不一致”的记录。
- 新数据库会带有状态和锁定字段的 `CHECK` 约束；旧数据库会在初始化时自动补齐
  `is_locked` 字段，并创建非空 `source_hash` 的唯一索引。
- GUI 的“安全退出”健康检查是只读检查：如果数据库不存在或不可读，只报告问题，
  不会偷偷创建或迁移数据库。

## 运行环境

本工具只使用 Python 标准库：

- `sqlite3`
- `tkinter`
- `argparse`

默认使用仓库根目录的 `.venv-py314`。

```powershell
.\.venv-py314\Scripts\Activate.ps1
```

## GUI 用法

从仓库根目录运行：

```powershell
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_gui.py
```

GUI 支持：

- 初始化数据库；
- 导入项目内置样例；
- 搜索和查看记录；
- 新增记录；
- 修改未锁定的 `active` 记录，修改前会二次确认；
- 软删除未锁定的 `active` 记录，删除前会二次确认；
- 显示已删除记录，并恢复或真删除；
- 锁定和解锁单条 `active` 记录；
- 按当前选中记录的状态自动启用或禁用按钮，防止误操作；
- 在关闭窗口、切换记录、刷新、搜索、清空表单和导入前检查未保存内容；
- “安全退出”按钮会在未保存内容检查之外，再执行一次只读数据库健康检查。

点击“新增”时，如果右侧正在显示某条已有记录，GUI 会先清空详情区并进入新增
模式；再次填写内容并点击“保存新增”才会真正创建记录。

关闭窗口右上角 `×` 时，GUI 会检查当前表单是否存在未保存内容；如果存在，会
询问用户是否继续退出。点击“安全退出”时，GUI 也会先做同样的未保存内容检查，
然后只读检查记录状态、锁定状态、内容哈希和重复内容。安全退出不会自动保存
草稿，也不会自动修复数据库；如果检查发现问题，只提示并询问是否仍要退出。

## CLI 用法

```powershell
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py init
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py import-test-demo
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py import-test-demo --legacy-test-demo
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py list
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py list --include-deleted
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py show 1
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py search "阶段测验"
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py add --title "示例" --category "manual" --content "示例内容"
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py update 1 --title "新标题" --yes
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py delete 1 --yes
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py restore 1
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py lock 1
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py unlock 1
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_cli.py hard-delete 1 --yes
```

修改、软删除和真删除默认要求交互确认；传入 `--yes` 可用于脚本化操作。
`import-test-demo` 的默认来源是项目内置样例；`--legacy-test-demo` 只读解析
历史 `tests/test_demo.py`；`--source` 可显式指定其它 UTF-8 来源文件，并且
不能和 `--legacy-test-demo` 同时使用。内置样例和 legacy 来源默认跳过前三行
文件头；自定义 `--source` 默认从第 1 行开始解析，如需兼容旧格式可传入
`--skip-header-lines 3`。`--content-file` 必须指向可读取的 UTF-8 文本文件；
`--limit` 必须是正整数。

## 自检

项目内提供一份标准库 `unittest` 自检脚本，不依赖仓库根目录的 `tests/`：

```powershell
python projects\P3_Statements_and_Syntax\prompt_template_manager\prompt_manager_self_check.py
```

自检覆盖：

- 项目内置样例解析数量和分类；
- 历史兼容入口必须显式指向 `tests/test_demo.py`，默认不读取它；
- 重复导入幂等性；
- 内容哈希不变量；
- 锁定、软删除、恢复、真删除状态机；
- 缺失数据库的只读健康检查不会创建文件。

## 数据库位置

默认数据库路径：

```text
projects/P3_Statements_and_Syntax/prompt_template_manager/data/prompt_templates.sqlite3
```

数据库文件是本地运行产物，已被 `data/.gitignore` 忽略。可以通过 CLI 或 GUI
的 `--db` 参数指定其它数据库路径。

## 数据模型

核心表为 `records`：

```sql
records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    content TEXT NOT NULL,
    tags_json TEXT NOT NULL DEFAULT '[]',
    source_file TEXT,
    source_block_index INTEGER,
    source_start_line INTEGER,
    source_end_line INTEGER,
    source_hash TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
    is_locked INTEGER NOT NULL DEFAULT 0 CHECK(is_locked IN (0, 1)),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK(NOT(status = 'deleted' AND is_locked = 1))
)
```

`content` 是 prompt 或说明块的完整文本快照。`source_file`、行号和
`source_hash` 只用于追溯来源，不会让数据库继续依赖源文件。当前实现把
`source_hash` 固定为规范化内容哈希，并为非空 `source_hash` 创建唯一索引，
从数据库层阻止重复内容。

## 首次导入规则

解析默认内置样例时：

1. 跳过第 1-3 行文件元信息；
2. 保留第 5 行总说明作为 `source_note`；
3. 从第 7 行开始，按空白物理行分隔每个 prompt 或说明块；
4. 预计首次导入 12 条有效记录。

## 历史兼容入口

早期版本曾默认从仓库根目录的 `tests/test_demo.py` 导入。该路径现在只作为
legacy 兼容入口存在，因为 `tests/` 在本仓库里是历史手工实验区，不是当前
项目的稳定数据目录。兼容入口的规则是：

- 只能通过 CLI 显式使用 `import-test-demo --legacy-test-demo`；
- 读取过程只解析 UTF-8 文本，不写回、不移动、不清理 `tests/test_demo.py`；
- GUI 不提供 legacy 导入按钮，避免把 `tests/` 误认为长期依赖；
- 如果 legacy 文件缺失或内容被改动，默认内置样例和项目自检仍应保持可用。
