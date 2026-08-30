# C19 Advanced Function Topics

This directory contains the prepared learning artifacts for
`P4_Functions_and_Generators / C19_Advanced_Function_Topics`. The authoritative
curriculum and pacing entry is
[C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md](../../../docs/C19_ADVANCED_FUNCTION_TOPICS_STARTUP_TEMPLATE.md).

## Role and Route

- Chapter role: `normal`.
- Role evidence: C16 is the closed P4 `PART opener`; C17 and C18 are closed
  normal chapters; the roadmap and source index place C19 between C18 and C20;
  C20 is also normal; and C21 is the P4 `PART closer`. C19 therefore neither
  opens nor closes the PART. This role comes from the durable route, startup
  template, and neighboring dependencies rather than the chapter number.
- Preparation status: completed on 2026-08-27 after focused validation.
- Lifecycle cursor: `preparation` is complete; `mainline` is the next phase and
  has not started in this preparation turn.
- Planned route: `preparation -> mainline -> quiz_authoring ->
  quiz_answering -> quiz_review -> stage_note -> final_closeout`.
- Default mainline exit: `mainline 100% -> stage quiz`.
- Capstone status: not scheduled. A composable rule registry or localization
  transformation pipeline remains a candidate checkpoint, not a required
  pre-quiz project.

## C16-C18 Handoff and C19 Boundary

C19 combines three completed prerequisites without reopening them:

- C16 established function objects, aliases, calls, returns, exceptions, and
  limited contract evidence.
- C17 established lexical name lookup, free names, enclosing bindings, and the
  minimal closure entry.
- C18 established complete argument evaluation, matching, initial parameter
  binding, defaults, collection, unpacking, and signature evidence boundaries.
- The C18 precision discipline carries forward: registration and later
  invocation are separate time stages; reference arrows go from names or
  container slots to objects; and initial parameter bindings must be separated
  from later object creation, mutation, or rebinding in a function body.

C19 adds first-class behavior composition, callbacks and dispatch, closure
sharing and late binding, bounded recursion, lambda, annotations, and
`Callable`. Generators remain in C20; benchmarking and P4-wide pitfalls remain
in C21. Systematic decorator design remains in P8/C39, and complete static type
engineering remains in PX1.

## Run

From the repository root:

~~~powershell
.\.venv-py314\Scripts\python.exe --version

.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\01_first_class_functions_references_and_call_timing.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\02_higher_order_callbacks_dispatch_and_composition.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\03_closure_environments_sharing_and_factory_isolation.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\04_late_binding_fixes_and_partial_references.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\05_recursion_base_progress_and_shared_objects.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C19_Advanced_Function_Topics\06_lambda_annotations_callable_and_evidence_limits.py
~~~

## Experiment Map

1. `01` separates aliases, container references, passing and returning a
   function object, and the later invocation point. It also shows that
   `callable()` does not prove a compatible call contract.
2. `02` gives higher-order transforms a uniform `str -> str` shape, separates
   callback registration from later dispatch, composes a small in-memory
   pipeline, and records partial effects when one rule fails.
3. `03` shows that returned functions keep access to required enclosing
   bindings, that closures from one factory call can share state, that another
   factory call is isolated, and that a closure is not a deep copy.
4. `04` exposes loop late binding with ordinary `def`, then compares default
   parameter and per-iteration factory repairs with a bounded
   `functools.partial` example. It proves that all three save references rather
   than copying mutable objects.
5. `05` makes the recursion base case, recursive step, decreasing progress
   measure, per-call local snapshots, and shared argument objects observable.
   It compares result semantics with a loop without benchmarking.
6. `06` limits lambda to short local expressions, observes annotations and a
   `Callable[[str], str]` shape, and proves through real calls that this
   metadata does not enforce runtime types, results, exceptions, side effects,
   or business rules.

Every numbered file is an independent, deterministic learning snapshot. The
examples use synthetic localization keys, in-memory containers, standard
library functions, and standard output only.

## Finite Mainline

Required core:

1. Distinguish a function object from an alias, container reference, argument,
   return value, and actual function call.
2. Trace higher-order transforms, callback registration and invocation,
   dictionary dispatch, and a small uniform transformation pipeline.
3. Explain how a closure accesses enclosing bindings after its factory call
   returns, how closures from one environment share state, and how separate
   factory calls isolate their environments.
4. Predict loop late binding and compare the two required repairs: saving each
   iteration's object reference in a default parameter and creating a new
   enclosing binding through a factory call.
5. Explain why a default, closure, or `partial` does not automatically copy a
   mutable object.
6. State a recursive base case, recursive step, progress measure, and
   termination argument while separating each call's local bindings from
   shared argument objects.
7. Explain lambda's single-expression boundary and its ordinary parameter,
   scope, and late-binding semantics.
8. Interpret parameter and return annotations plus `Callable` as limited
   metadata and shape intent rather than automatic runtime enforcement.
9. Write a small higher-order contract that identifies inputs, result,
   possible exceptions, side effects, and the evidence needed to validate it.

Necessary remediation:

- Saving or registering a callable is not the same time event as invoking it.
- A dictionary slot containing a callable does not prove that its body has run.
- A closure preserves access to enclosing bindings; it does not freeze values
  or copy every object reachable through those bindings.
- Loop late binding is not lambda-specific. Ordinary nested `def` functions can
  read the same later binding.
- A default-parameter repair saves the object reference evaluated at function
  creation; the parameter can still be overridden by a caller.
- Separate factory calls create separate bindings, but they can still share an
  explicitly supplied mutable object.
- A recursive function is not shown to terminate merely because it calls
  itself; the base case must be reachable and every recursive step must move a
  defined measure toward it.
- Each recursive call has its own local bindings even when several calls bind
  parameters to the same list or trace object.
- `callable()`, annotations, `Callable`, a visible signature, registration
  success, or one successful call cannot alone prove the full behavior
  contract.

Optional enrichment includes limited `__closure__` or cell observation,
`functools.partial` signature details, the current interpreter's recursion
limit, richer composition helpers, and only an entry-level view of a decorator
as a callable that accepts and returns a callable. Optional material does not
affect mainline completion or later quiz scope.

## Engineering Context

The existing
[`prompt_template_manager`](../../../projects/P3_Statements_and_Syntax/prompt_template_manager/README.md)
is static engineering background, not curriculum authority:

- In
  [`prompt_manager_cli.py`](../../../projects/P3_Statements_and_Syntax/prompt_template_manager/prompt_manager_cli.py),
  `set_defaults(func=command_...)` stores command function objects and
  `args.func(args)` performs the later dispatch call.
- In
  [`prompt_manager_gui.py`](../../../projects/P3_Statements_and_Syntax/prompt_template_manager/prompt_manager_gui.py),
  `command=self.some_method`, `command=lambda: ...`, and
  `bind(..., lambda _event: ...)` pass callable objects for later event-driven
  invocation.

Those sources provide real examples of function objects, delayed calls,
dispatch, bound methods, and bounded lambda use. They do not provide complete
evidence for closure late binding, recursion, `partial`, annotations, or
`Callable`, so the numbered experiments remain self-contained. This
preparation did not import or execute the project, connect to SQLite, perform
CRUD, dispatch its CLI, open its GUI, run a self-check, or expand into
`argparse`, Tkinter, or OOP teaching.

## Preparation Validation

- The selected interpreter is CPython `3.14.5` at
  `.venv-py314\Scripts\python.exe`.
- All six numbered scripts pass `python -m py_compile`.
- All six numbered scripts complete representative runs with deterministic
  synthetic output and expected handled exception classes.
- README headings, relative links, fenced blocks, file references, and finite
  scope markers pass focused Markdown checks.

These checks prove that the prepared artifacts are readable and runnable in
the current environment. They do not prove every future input path or the
complete business correctness of a real callback system.

## Safety and Preparation Boundary

- No artifact reads or operates on `tests/`.
- No artifact opens, initializes, migrates, reads, or modifies SQLite.
- No real file, network, CRUD, CLI, GUI, or self-check path is invoked.
- Observable effects are limited to standard output and synthetic in-memory
  function objects, strings, lists, dictionaries, tuples, and handled
  exceptions.
- Error demonstrations print stable exception class names instead of depending
  on version-specific full messages.
- Preparation created no capstone, quiz, stage note, C20-C21 practice file,
  repository-level shared package, decorator framework, generator-function or
  `yield` experiment, or benchmark.
- Every numbered file keeps its own helpers and entry guard so it can run
  independently.
