# C20 生成器函数状态

本目录属于 `P4_Functions_and_Generators / C20_Comprehensions_Revisited_and_Generators`。
唯一课程范围与节奏权威是 [C20 启动模板](../../../docs/C20_COMPREHENSIONS_REVISITED_AND_GENERATORS_STARTUP_TEMPLATE.md)。

## 角色、依据与准备状态

- 章节角色：`normal`。启动模板、[路线图第 6 节](../../../docs/PYTHON_LEARNING_ROADMAP.md)
  和 [C19 收束账本](../C19_Advanced_Function_Topics/README.md) 一致：
  C16 是 P4 opener，C19 已 closed，C20 承接前置，C21 才是 PART closer。
  本章不打开或关闭 P4；角色不是按编号猜测。
- 校准依据：[学习画像](../../../notes/Python_Learning_Profile.md)、
  [P4 笔记 21.0—21.14](../../../notes/P4_Functions_and_Generators.md)
  和 [C19 最终批改区](../C19_Advanced_Function_Topics/stage_quiz_advanced_function_topics.md)。
  考卷中的 stage_note 游标是批改时的历史快照，C19 最新状态以收束账本为准。
- 2026-10-02：`preparation` 已完成并验证；正式主线尚未开始，等待用户要求进入。
  六个脚本的成功运行只证明学习工件可运行，不构成学习者掌握证据。
- 本轮新增六个独立编号脚本和本 README；没有原有 C20 文件需要覆盖。
- 当前没有已排期 pre-quiz capstone；第 06 组是有限实验，流式管线候选不升级为项目。
- 关卡：`preparation -> mainline -> quiz_authoring -> quiz_answering ->
  quiz_review -> stage_note -> final_closeout -> closed`。

## 有限主线与文件职责

以下六组就是启动模板的必学核心；编号是实验组织方式，不规定每次对话的固定长度。

| 组 | 文件 | 理解目标与观察边界 |
| --- | --- | --- |
| 01 | [函数、对象与启动时点](01_generator_function_object_and_start_timing.py) | 参数求值/匹配、对象创建、首次 next、产出对象身份；无函数体执行不等于无参数效果 |
| 02 | [暂停、恢复与共享](02_yield_resume_local_state_and_shared_objects.py) | yield 后恢复位置、独立局部计数、共享记录、外部重绑；最后一次产出不等于已结束 |
| 03 | [结束、耗尽与重建](03_return_stopiteration_exhaustion_and_recreation.py) | return、自然结束、StopIteration.value、for 的消费、新调用；终止值不是额外产出值 |
| 04 | [表达式与函数对照](04_generator_expression_and_function_semantics.py) | 最左侧 iterable 的即时求值、后续名字读取、参数绑定、作用域、失败时点；相同结果只证明有限等价 |
| 05 | [最小 yield from](05_yield_from_sequential_delegation.py) | 子迭代顺序、空子序列、恢复外层、对象身份和结束；不复制数据、不并发 |
| 06 | [流式与物化管线](06_streaming_materialized_localization_pipeline.py) | 正常、空输入、break 后剩余、共享游标、重新遍历、所有权、异常前效果与赋值边界 |

C14 的 iterable/iterator、推导式和短路消费，以及 C16—C19 的函数/作用域/参数模型
只作短桥接。重点展开本章新增的暂停、恢复、局部状态与跨时点消费。

必要补救仅针对实际暴露的创建/执行混淆、暂停/结束混淆、消费状态误判、
共享引用/深快照混淆，以及异常时点和证据强度问题；目前不预设新的能力缺陷。
可选 `gi_frame`、`send()/throw()/close()`、更深的委托返回值与双向协议
不增加必学分母。异步/并发、完整资源管理和异常专题、性能测量、装饰器系统、
全面静态类型工程与通用流处理框架不在本章必学范围。

## 运行方式

在仓库根目录的 PowerShell 执行；明确使用项目解释器，不依赖裸 `python`。
每个脚本都可以单独运行，不导入其他编号脚本，也不需要第三方依赖。

~~~powershell
$chapterPath = 'practice\P4_Functions_and_Generators\C20_Comprehensions_Revisited_and_Generators'
$taskPython = '.\.venv-py314\Scripts\python.exe'
$chapterScripts = @(
    '01_generator_function_object_and_start_timing.py'
    '02_yield_resume_local_state_and_shared_objects.py'
    '03_return_stopiteration_exhaustion_and_recreation.py'
    '04_generator_expression_and_function_semantics.py'
    '05_yield_from_sequential_delegation.py'
    '06_streaming_materialized_localization_pipeline.py'
)
$chapterFiles = @($chapterScripts | ForEach-Object { Join-Path $chapterPath $_ })
& $taskPython -X utf8 -c "import sys; print(sys.version); print(sys.executable)"
& $taskPython -X utf8 -m py_compile @chapterFiles
if ($LASTEXITCODE -ne 0) { throw 'C20 compile failed' }
foreach ($chapterFile in $chapterFiles) {
    & $taskPython -B -X utf8 $chapterFile
    if ($LASTEXITCODE -ne 0) { throw "C20 run failed: $chapterFile" }
}
~~~

只跑第一组时：

~~~powershell
& '.\.venv-py314\Scripts\python.exe' -B -X utf8 'practice\P4_Functions_and_Generators\C20_Comprehensions_Revisited_and_Generators\01_generator_function_object_and_start_timing.py'
~~~

每组显示分段轨迹与 `OK:` 结尾，断言核对身份、结果或关键事件。
预期异常必须实际发生，否则显式失败；不依赖对象地址、完整错误文本或手动输入。
请保留正常断言模式，不用 `-O` 跳过实验核验。
`py_compile` 会在本章生成忽略的 `__pycache__`；运行脚本本身只使用内存和 stdout。

## 第 06 组的有限合同

- 输入是有限可迭代对象，其元素为普通字典，含字符串 key/text 和列表 tags；
  不做通用模式验证，缺字段等合同外输入不在本实验保证范围。
- 按输入顺序规范化 key、去除 text 两端空白并过滤空 text；不去重、不排序。
  key/text 错型在消费该记录时显式抛 TypeError，异常向调用者传播。
- 每个成功转换产出新字典，tags 刻意保留源列表引用；调用者拥有源数据，
  可以修改共享 tags，但不能把物化误称深复制或独占所有权。
- 流式版本逐项传递，物化版本先收集所有规范化记录，再执行过滤。
  合法输入的最终内容相等；事件顺序、失败前交付与部分效果分别检查。
- 重放时明确选择重新遍历源列表或复用已保存结果；重复消费同一耗尽对象
  不会重放。新管线若仍接收同一上游迭代器，也不会重置上游游标。
- break 留下可继续消费的流；未处理异常传播出生成器后，该次执行终止。
  外部另有引用的上游游标可能仍有尾部，不能与失败生成器混为一谈。
- `result = list(stream)` 失败时不完成该次赋值，但此前消费与事件不会回滚。
  手动收集的 delivered 列表则保留异常前已经交付的项。

## 验证记录与未证明事项

验证环境：2026-10-02，项目 `.venv-py314\Scripts\python.exe`，CPython 3.14.5。

- 六个编号文件均通过 `py_compile`。
- 六个文件均完成代表性运行，退出码为 0，实验断言及预期异常分支通过。
- README 核验 UTF-8、标题、围栏配对、相对链接、六文件映射和有限范围标记；
  新增文件检查结尾换行及行末空白。
- 检查限定在本章及明确列出的只读权威材料，没有操作 `tests/`。

这些证据只覆盖已写明的合成输入与当前解释器，不证明任意业务数据、
第三方迭代器或真实工程的完整合同。未做速度或内存基准；惰性不等于零工作、
一定更快或无条件常量内存，保留的事件日志本身也随消费增长。
用 return 结束生成器，不手工 raise StopIteration 冒充 return。

## 工程背景与下一原子动作

`projects/P3_Statements_and_Syntax/prompt_template_manager/` 可以在后续有需要时
作静态背景。本轮的六组目标由合成记录覆盖，不要求真实项目使用生成器；
没有导入或执行该项目，没有运行 GUI/CLI/self-check 或连接 SQLite/CRUD。
不创建项目、测验、C21 工件或新阶段笔记，不预写能力判断，不更新全局记忆。

下一原子动作：用户要求进入主线后，先呈现上述有限地图，再直接讲授
“生成器函数、生成器对象、产出对象，以及调用创建与首次推进”的第一个实质步骤，
以 01 为运行锚点。当前没有待回答或待收束的选答题。

核心与必要补救完成后，默认 `mainline 100% -> stage quiz`；
只有后续明确授权并持久协调关卡，才插入 capstone。测验审批与稳定评分后
才更新画像，再追加 P4 阶段笔记和执行最终收束。本轮停在准备完成。
