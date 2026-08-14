# C18 Arguments

This directory contains the prepared learning artifacts for
`P4_Functions_and_Generators / C18_Arguments`. The authoritative curriculum
and pacing entry is
[C18_ARGUMENTS_STARTUP_TEMPLATE.md](../../../docs/C18_ARGUMENTS_STARTUP_TEMPLATE.md).

## Role and Route

- Chapter role: `normal`.
- Role evidence: C16 is the closed P4 `PART opener`; C17 is a closed normal
  chapter; the roadmap and source index place C18 between C17 and C19; and C21
  is the P4 `PART closer`. C18 therefore neither opens nor closes the PART.
  This role comes from the durable route and neighboring dependencies, not the
  chapter number alone.
- Preparation status: completed on 2026-08-12 after focused validation.
- Current lifecycle phase: `mainline` is next but has not started.
- Planned route: `preparation -> mainline -> quiz_authoring ->
  quiz_answering -> quiz_review -> stage_note -> final_closeout -> closed`.
- Default mainline exit: `mainline 100% -> stage quiz`.
- Capstone status: not scheduled. The localization audit function, argument
  binding matrix, and P4 function pipeline remain candidates rather than a
  required pre-quiz project.

The next atomic action is the first finite mainline lesson: distinguish call
target and argument-expression evaluation, signature matching, successful
parameter binding, and function-body entry. Preparation does not itself count
as that lesson.

## C16/C17 Handoff and C18 Boundary

C18 continues from two completed prerequisites without reopening them:

- C16 established that a call evaluates argument expressions, creates one
  call's local state, and does not automatically copy argument objects.
- C17 established that parameters are local names for one call, and that name
  binding, object identity, mutation, control flow, and evidence strength must
  be tracked separately.
- C18 adds the complete but finite binding contract: parameter kinds, matching
  failures, defaults, definition-side collection, call-side unpacking, and
  modern positional-only and keyword-only boundaries.
- The three C17 precision reminders carry forward: a process can have started
  without a later binding being complete; only real names create bindings; and
  objects do not acquire a local/global ownership property.

Higher-order functions, systematic closure late binding, recursion, lambda,
`functools.partial`, and annotations remain in C19. Generators remain in C20;
benchmarking and P4-wide pitfalls remain in C21.

## Run

From the repository root:

~~~powershell
.\.venv-py314\Scripts\python.exe --version

.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C18_Arguments\01_argument_evaluation_matching_and_local_binding.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C18_Arguments\02_parameter_kinds_and_binding_failures.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C18_Arguments\03_defaults_and_mutable_default_state.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C18_Arguments\04_varargs_and_varkw_collection.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C18_Arguments\05_call_unpacking_conflicts_and_partial_effects.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C18_Arguments\06_positional_keyword_only_and_signature_evidence.py
~~~

## Experiment Map

1. `01` records call-target and argument-expression evaluation, then separates
   successful signature matching, per-call local parameter bindings, body
   entry, object sharing, and a rejected call whose earlier effects remain.
2. `02` places all five parameter kinds in one bounded signature and observes
   missing, duplicate, unknown, excessive positional, and positional-only
   keyword failures without relying on version-specific error text.
3. `03` proves that default expressions run when the `def` executes, observes
   the default object stored by the function, exposes shared mutable default
   state, and contrasts a per-call-state repair.
4. `04` isolates definition-side `*extra_keys` and `**controls` collection,
   including the resulting tuple and dictionary and their shallow reference
   boundary.
5. `05` isolates call-side `*iterable` and `**mapping` unpacking, evaluation
   order, duplicate assignment, and effects that occur before a rejected call.
6. `06` uses `/` and `*` to express API intent and limits
   `inspect.signature()` / `Signature.bind()` evidence to call shape rather
   than body behavior or business correctness.

Every numbered file is an independent, deterministic learning snapshot. The
examples use synthetic localization and prompt-record data plus in-memory
objects only.

## Finite Mainline

Required core:

1. Distinguish actual argument expressions, formal parameters, matching, and
   the local parameter bindings created for one successful call.
2. Trace `call target -> argument evaluation -> unpacking -> matching -> local
   bindings -> body`, including the stage at which each failure occurs.
3. Recognize positional-only, positional-or-keyword, var-positional,
   keyword-only, and var-keyword parameters and their ordering boundaries.
4. Explain positional and keyword matching plus missing, duplicate, unknown,
   and excessive-argument `TypeError` paths.
5. Explain definition-time default evaluation, storage on the function object,
   and binding the saved default when an argument is omitted.
6. Trace why a mutable default object is shared across omitted-argument calls
   and create replacement state inside each call when isolation is required.
7. Distinguish definition-side `*args` / `**kwargs` collection from call-side
   `*iterable` / `**mapping` unpacking.
8. Design a small explicit parameter contract and state exactly what signature
   inspection and binding evidence can and cannot prove.

Necessary remediation:

- A call expression starting is not the same as parameter matching or binding
  having completed.
- If argument evaluation fails, the target body was not entered; if matching
  fails, the target body is also not entered.
- Effects completed while evaluating the target or arguments are not rolled
  back by a later `TypeError`.
- Parameter binding creates local name-to-object relationships; it does not
  copy the argument object or make that object "local".
- A caller's local scope is not an enclosing scope of the called function.
- Mutable defaults are saved objects reused by one function object, not a
  `global` or `nonlocal` mechanism.
- Definition-side collection and call-side unpacking are opposite boundaries,
  not one operation described from two spellings.
- Successful `Signature.bind()` proves only that a call shape maps to the
  inspected signature. It does not execute the body or prove types, results,
  exceptions, side effects, or business rules.

Optional enrichment includes deeper `__defaults__` / `__kwdefaults__`
observation, `inspect.Parameter`, `Signature.bind_partial()`, a dedicated
sentinel when `None` is a valid value, complex multiple unpackings, and extra
forwarding examples. It does not affect mainline completion or quiz scope.

## Engineering Context

The existing
[`prompt_template_manager`](../../../projects/P3_Statements_and_Syntax/prompt_template_manager/README.md)
is static background, not curriculum authority. Its real signatures provide a
few bounded API-design anchors:

- `print_record(record, *, show_content=True)` exposes a keyword-only display
  control.
- `add_record(*, ...)` exposes an all-keyword record-creation contract.
- `update_record(record_id, *, ...)` separates one record identity from
  keyword-only update fields.
- `parse_prompt_source(source_path=..., *, skip_header_lines=None)` separates a
  default source from a keyword-only parsing control.

The project does not supply the complete C18 evidence: its current Python
sources do not provide representative positional-only, `*args`, `**kwargs`, or
call-unpacking examples. The numbered experiments therefore remain
self-contained. They do not import or execute that project, connect to SQLite,
perform CRUD, dispatch its CLI, open its GUI, or reproduce its architecture.

## Safety and Preparation Boundary

- No experiment reads or operates on `tests/`.
- No experiment opens, initializes, migrates, reads, or modifies SQLite.
- No real file, network, CRUD, CLI, or GUI path is invoked.
- Observable effects are limited to standard output and synthetic in-memory
  lists, dictionaries, tuples, strings, function objects, and exception types.
- Error demonstrations print stable exception classes rather than depending on
  version-specific full messages.
- This preparation creates no capstone, quiz, stage note, C19-C21 practice
  file, or repository-level shared package.
- Every numbered file keeps its own helpers and entry guard so it can run
  independently.
