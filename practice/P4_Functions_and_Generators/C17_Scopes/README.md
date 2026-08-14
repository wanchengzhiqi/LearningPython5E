# C17 Scopes

This directory contains the completed and validated learning artifacts for
`P4_Functions_and_Generators / C17_Scopes`. The authoritative curriculum and
pacing entry remains the historical
[C17_SCOPES_STARTUP_TEMPLATE.md](../../../docs/C17_SCOPES_STARTUP_TEMPLATE.md).

## Role and Route

- Chapter role: `normal`.
- Role evidence: C16 is the closed P4 `PART opener`, the roadmap and source
  index place C17 between C16 and C18, and C21 is the P4 `PART closer`. C17
  therefore neither opens nor closes the PART; this role is not inferred from
  the chapter number.
- Preparation status: completed on 2026-08-03 after focused validation.
- Current lifecycle phase: `closed` since 2026-08-12.
- Completed route: `preparation -> mainline -> quiz_authoring ->
  quiz_answering -> quiz_review -> stage_note -> final_closeout -> closed`.
- Default mainline exit: `mainline 100% -> stage quiz`.
- Capstone status: not scheduled. A scope tracer or configuration function is
  only a roadmap candidate, not a required pre-quiz project.

Completion evidence:

- Six numbered scripts provide the independently runnable evidence for the
  finite C17 map.
- [stage_quiz_scopes.md](stage_quiz_scopes.md) has `11 / 11` questions
  individually reviewed and a stable score of `99.25 / 100`.
- The final learning profile and C17 stage note are synchronized; optional
  follow-up material remains non-blocking and does not change the score.
- No capstone was scheduled or created.
- The sole next-chapter entry is
  [C18_ARGUMENTS_STARTUP_TEMPLATE.md](../../../docs/C18_ARGUMENTS_STARTUP_TEMPLATE.md);
  C18 preparation belongs in a new session.
- Unnumbered practice files are retained as optional learning traces, not as
  required formal evidence.

## C16 Handoff and C17 Boundary

C17 continues from the completed C16 call model without reopening it:

- Executing `def` creates a function object and binds a name; calling enters
  one call's local state.
- Names, objects, rebinding, mutation, return values, output effects, and
  evidence strength are already stable prerequisites.
- C17 adds the missing name-resolution model: how a bare name is classified,
  where a read looks, and where a binding operation targets.
- The prior `StringIO` and string-identity precision reminders remain evidence
  discipline, not new C17 curriculum.

Complete argument matching remains in C18. Closure late binding, callback
composition, recursion, lambda, and systematic annotations remain in C19.
Generators remain in C20; benchmarking and P4-wide pitfalls remain in C21.

## Run

From the repository root:

~~~powershell
.\.venv-py314\Scripts\python.exe --version

.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C17_Scopes\01_legb_lookup_and_shadowing.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C17_Scopes\02_local_names_and_unboundlocalerror.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C17_Scopes\03_module_globals_and_global_statement.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C17_Scopes\04_enclosing_names_nonlocal_and_rebinding.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C17_Scopes\05_free_names_and_closure_entry.py
.\.venv-py314\Scripts\python.exe practice\P4_Functions_and_Generators\C17_Scopes\06_namespace_observation_and_explicit_dependencies.py
~~~

## Experiment Map

1. `01` separates names, bindings, and lookup, then observes local,
   enclosing, module-global, and built-in resolution plus shadowing.
2. `02` contrasts a successful module-name read with names classified as
   local, including later assignment and path-dependent
   `UnboundLocalError`.
3. `03` shows that module globals belong to this module, mutation of a found
   object does not itself require `global`, and rebinding a module name from a
   function does.
4. `04` contrasts reading an enclosing name, mutating an enclosing object,
   local shadowing, and `nonlocal` rebinding of the nearest enclosing
   function name.
5. `05` establishes the closure entry model: an inner function can keep
   reading a free name after the outer call has returned.
6. `06` observes selected `locals()` and `globals()` evidence without
   writing through either mapping, then compares implicit module configuration
   with explicit dependency passing.

Each file is an independent, deterministic learning snapshot. The examples use
synthetic localization data and only in-memory objects.

## Finite Mainline

Required core:

1. Distinguish a name, a binding, a namespace, a scope, and a name lookup.
2. Explain function-local name classification and the real
   `UnboundLocalError` path.
3. Trace LEGB reads through local, enclosing, global, and built-in layers,
   including shadowing.
4. Explain that a global name belongs to one module namespace rather than a
   universal cross-module store.
5. Use `global` to target a module binding without describing an object as a
   "global object".
6. Use `nonlocal` to target the nearest enclosing function binding.
7. Separate cross-scope rebinding from mutation of an already found shared
   object.
8. Establish nested functions, free names, closure entry, and limited
   namespace observation.

Necessary remediation:

- A function's local namespace is not the caller's namespace or a copy of an
  argument object.
- LEGB read lookup and binding-target classification are related but different
  rules.
- Object mutability does not decide whether a name is local.
- `UnboundLocalError` does not mean the similarly named module binding is
  absent.
- `global` and `nonlocal` change a binding target, not object ownership,
  type, identity, or mutability.
- Mutating a shared module or enclosing object does not by itself imply a
  `global` or `nonlocal` declaration.
- `locals()` and `globals()` observations are not promoted into a general
  arbitrary write-back contract.

Optional enrichment includes `__closure__`, cell objects, symbol-table or
bytecode inspection, complex closure state, late binding, and extra project
walkthroughs. It does not affect mainline completion or quiz scope.

## Engineering Context

The existing
[`prompt_template_manager`](../../../projects/P3_Statements_and_Syntax/prompt_template_manager/README.md)
is static background, not curriculum authority:

- `prompt_store.py` defines `DEFAULT_DB_PATH` at module scope, and
  `resolve_db_path()` reads that module name only when an explicit
  `db_path` was not supplied.
- CLI and store functions pass `db_path` explicitly through call boundaries,
  illustrating why dependencies need not live in hidden mutable global state.
- Those files are not imported or executed by these experiments. Their module
  constants cannot be repackaged as a complete `global` or `nonlocal`
  lesson.

The numbered scripts use smaller synthetic examples so the language mechanism
remains observable without database, CLI, or GUI behavior.

## Safety and Preparation Boundary

- No experiment reads or operates on `tests/`.
- No experiment opens, initializes, migrates, reads, or modifies SQLite.
- No real file, network, CRUD, CLI, or GUI path is invoked.
- Observable effects are limited to standard output and synthetic in-memory
  lists, dictionaries, strings, and function objects.
- `locals()` and `globals()` are used only for selected read observations;
  the scripts do not write through their returned mappings or print an entire
  namespace.
- This chapter creates no capstone, C18-C21 practice file, or repository-level
  shared package.
- Every numbered file keeps its own helpers and entry guard so it can run
  independently.
