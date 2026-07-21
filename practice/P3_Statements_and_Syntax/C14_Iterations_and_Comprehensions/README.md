# C14 Iterations and Comprehensions

This directory records `P3_Statements_and_Syntax / C14_Iterations_and_Comprehensions`.

The official entry for this chapter is
`docs/C14_ITERATIONS_AND_COMPREHENSIONS_STARTUP_TEMPLATE.md`. These scripts turn
that template into runnable experiments. The focus is not making every loop short.
The focus is deciding what Python is consuming, when it is consumed, and whether a
comprehension keeps the code clearer than an explicit loop.

`projects/P3_Statements_and_Syntax/prompt_template_manager/` is used only as a
read-only real-code background. The scripts do not open, initialize, migrate, or
modify its SQLite database.

## Stage Outcome

- The nine numbered experiments were validated with Python `3.14.5`.
- [`stage_quiz_iterations_and_comprehensions.md`](stage_quiz_iterations_and_comprehensions.md)
  was reviewed item by item; the suggested score is `99 / 100`.
- The durable chapter note is in
  [`notes/P3_Statements_and_Syntax.md`](../../../notes/P3_Statements_and_Syntax.md#16-c14-迭代与推导式消费位置求值时机和数据管道边界).
- C14 is a normal chapter. Its handoff target is the P3 closer,
  [`C15_The_Documentation_Interlude`](../../../docs/C15_THE_DOCUMENTATION_INTERLUDE_STARTUP_TEMPLATE.md).

## Core Chain

```text
iterable object
    -> iter(obj)
    -> iterator object
    -> next(iterator)
    -> one item at a time
    -> StopIteration when exhausted

repeatable containers:
    list, dict, set, str usually create a fresh iterator each time

one-shot iterators:
    file objects, zip, map, filter, generator expressions usually remember progress

eager collection:
    list comprehension, set comprehension, dict comprehension, list(), tuple(), set(), dict()

lazy producers:
    generator expression, zip, map, filter, file iteration

short-circuit consumers:
    any(), all()

full consumers:
    list(), tuple(), set(), dict(), sorted(), sum()
```

## Run

From the repository root:

```powershell
.\.venv-py314\Scripts\Activate.ps1
python --version

python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\01_iter_next_stopiteration.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\02_repeatable_vs_one_shot_iterables.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\03_file_stringio_position_and_consumption.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\04_comprehension_filter_transform_scope.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\05_set_dict_comprehensions_stable_reports.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\06_generator_expressions_lazy_short_circuit.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\07_nested_comprehensions_execution_order.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\08_localization_iteration_pipeline.py
python practice\P3_Statements_and_Syntax\C14_Iterations_and_Comprehensions\09_prompt_manager_iteration_reading_walkthrough.py
```

## Experiment Map

1. `01_iter_next_stopiteration.py`: `iter()`, `next()`, `StopIteration`, and `next(iterator, default)`.
2. `02_repeatable_vs_one_shot_iterables.py`: repeatable containers versus one-shot iterator objects.
3. `03_file_stringio_position_and_consumption.py`: file objects and `StringIO` position movement.
4. `04_comprehension_filter_transform_scope.py`: list comprehensions, filtering, transformation, and scope.
5. `05_set_dict_comprehensions_stable_reports.py`: set and dict comprehensions, deduplication, overwrite risk, stable reports.
6. `06_generator_expressions_lazy_short_circuit.py`: generator expressions, lazy evaluation, short-circuit consumers, one-shot risk.
7. `07_nested_comprehensions_execution_order.py`: nested comprehension order versus explicit loops.
8. `08_localization_iteration_pipeline.py`: localization resource filtering, placeholder checks, and structured reports.
9. `09_prompt_manager_iteration_reading_walkthrough.py`: read-only iteration experiments with real `prompt_template_manager` helpers and source text.

## Prediction Questions

Before running each section, pause at `[Predict]` and answer:

1. Which object is the iterable, and which object is the iterator?
2. Does `iter(obj)` create a new iterator, or return the same object?
3. Which `next()` call consumes which item?
4. Is this expression eager or lazy?
5. If the same object is consumed twice, what remains the second time?
6. Does the comprehension variable leak into the surrounding function scope?
7. Is this a simple filtering/projection problem, or should an explicit loop preserve statistics, errors, and side effects?
8. Does the report need stable ordering, such as `sorted(set_obj)`?

## Safety Boundaries

- No script writes to `tests/`.
- No script opens or mutates the prompt manager SQLite database.
- No shared helper module is extracted; repeated teaching helpers are kept in each script as chapter snapshots.
- Human-facing output is for observation only. Structured results stay as Python dictionaries and lists.
