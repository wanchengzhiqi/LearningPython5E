# C16 Function Basics

This directory contains the validated learning and assessment artifacts for
`P4_Functions_and_Generators / C16_Function_Basics`. The authoritative
curriculum entry is
[C16_FUNCTION_BASICS_STARTUP_TEMPLATE.md](../../../docs/C16_FUNCTION_BASICS_STARTUP_TEMPLATE.md).

## Role and Route

- Chapter role: `PART opener`.
- Role evidence: P3 is closed, the roadmap and source index place C16 first in
  P4, and the function-object/call/return model is a shared dependency for
  C17-C21. This role is not inferred from the chapter number.
- Preparation status: completed on 2026-07-27 after focused validation.
- Closeout status: `final_closeout` completed on 2026-08-03; C16 is `closed`.
- Completed route: `preparation -> mainline -> quiz_authoring ->
  quiz_answering -> quiz_review -> stage_note -> final_closeout -> closed`.
- Default mainline exit: `mainline 100% -> stage quiz`.
- Capstone status: not scheduled. The candidate P4 function pipeline and
  benchmark report is not a required C16 artifact.

The finite mainline and all required chapter gates are complete. C17 teaching
must begin from its own startup template in a fresh conversation.

## Completion Evidence

- The five numbered experiments and finite mainline were completed and
  validated with the repository `.venv-py314` / Python 3.14.5 environment.
- The stage quiz was reviewed question by question: `11 / 11` questions,
  stable score `99.75 / 100`. The quiz validator confirmed 6 sections, 11
  questions, and 41 compilable Python code blocks.
- The final review judgment was synchronized to
  `notes/Python_Learning_Profile.md` without changing the stable score or the
  judgment that function basics reached an excellent level.
- The C16 stage-end note is recorded under `## 18` in
  [`notes/P4_Functions_and_Generators.md`](../../../notes/P4_Functions_and_Generators.md).
- No physical-book or later-topic follow-up is required for closure. Optional
  follow-up did not occur and does not create replacement work.
- No pre-quiz capstone was scheduled. Roadmap candidates and adjacent
  engineering artifacts are not retroactively treated as completed gates.
- The single next-chapter entry is
  [`docs/C17_SCOPES_STARTUP_TEMPLATE.md`](../../../docs/C17_SCOPES_STARTUP_TEMPLATE.md);
  C17 must start with preparation in a fresh conversation.

## P3 Handoff and P4 Boundary

C16 inherits the final P3 evidence without reopening P3:

- The learner is at a stable early-intermediate entry point and can already
  reason with objects, bindings, control flow, iterator state, and evidence
  layers. C15 closed with a recommended score of `98 / 100`.
- P3 established the distinctions between evaluation and execution, rebinding
  and mutation, returned objects and displayed text, and source claims and
  runtime observations.
- Existing project work separates structured reports from `print()`, logging,
  JSON text, and persistence effects.
- Remaining risks are now function-specific: do not confuse a function object
  with a call result, assume calls copy argument objects, call output a return
  value, or treat annotations and signatures as complete behavior checks.
- Runtime introspection can execute code. This preparation inspects only
  ordinary functions defined by its own scripts.

As a PART opener, C16 establishes the shared P4 vocabulary of function object,
definition, binding, call, body, result, exception, and side effect. It does
not teach the whole PART.

## Run

From the repository root:

~~~powershell
.\.venv-py314\Scripts\Activate.ps1
python --version

python practice\P4_Functions_and_Generators\C16_Function_Basics\01_def_function_objects_and_aliases.py
python practice\P4_Functions_and_Generators\C16_Function_Basics\02_definition_call_and_return_timeline.py
python practice\P4_Functions_and_Generators\C16_Function_Basics\03_return_paths_none_and_exceptions.py
python practice\P4_Functions_and_Generators\C16_Function_Basics\04_return_values_and_side_effect_contracts.py
python practice\P4_Functions_and_Generators\C16_Function_Basics\05_docstring_signature_and_annotation_evidence.py
~~~

## Experiment Map

1. `01`: `def` creates a function object, a name binds to it, aliases and
   containers can hold the same object, and parentheses perform a call.
2. `02`: definition and call happen at different times; a call enters the
   body, creates basic local state, reaches `return`, and gives an object back
   to the caller.
3. `03`: explicit values, bare `return`, implicit `None`, multiple paths,
   unreachable statements, and exceptions have different control-flow
   outcomes.
4. `04`: a structured return, displayed text, argument-object mutation, and
   controlled in-memory I/O are separate contract dimensions.
5. `05`: docstrings, signatures, `Signature.bind()`, `callable()`, and
   annotations provide limited metadata or shape evidence, not a guarantee
   that a call will succeed or enforce types.

## Finite Mainline

Required core:

1. Explain that executing `def` creates a function object and binds the
   definition name.
2. Separate the function object, aliases, the call expression, body execution,
   and the result object.
3. Trace `definition -> binding -> call -> body -> return/exception -> caller`.
4. Distinguish `return value`, bare `return`, fall-through `None`, unreachable
   code, and an exception path.
5. Separate returned data from display, logging, mutation, and external I/O.
6. Observe first-class function behavior and limited function metadata without
   turning C16 into a higher-order-function or typing chapter.

Necessary remediation:

- `function` and `function()` are not interchangeable expressions.
- Assignment and basic call entry bind references; they do not copy objects by
  default.
- `print()`, in-place mutation, and persistence are effects, not automatically
  the function's return value.
- `callable()`, annotations, a displayed signature, or successful
  `Signature.bind()` do not prove complete behavior.

Optional enrichment includes additional function attributes, frames,
bytecode, and extra real-project walkthroughs. It does not affect mainline
completion or the stage-quiz scope.

## Engineering Context

The existing
[`prompt_template_manager`](../../../projects/P3_Statements_and_Syntax/prompt_template_manager/README.md)
remains read-only background rather than curriculum authority:

- `prompt_store.py` uses small functions such as `content_hash()` and
  `normalized_content_hash()` to demonstrate calls and explicit returns.
- `prompt_manager_cli.py::print_record()` displays data and falls through to
  `None`, while CLI handlers return status codes separately.
- `set_defaults(func=command_show)` stores a function object; `args.func(args)`
  later calls one. C16 observes only that boundary and does not teach callback
  architecture.

The numbered experiments are self-contained and use synthetic localization
data. They do not connect to a database or invoke initialization, migration,
CRUD, CLI, or GUI paths.

Contract cards, refactor patches, and verification records stored beside the
numbered experiments are optional engineering background. They are not formal
numbered mainline artifacts, a C16 capstone, or C17 curriculum authority. Some
background verification records retain their original Python 3.13.5 evidence
scope and are not relabeled as formal Python 3.14.5 proof.

## Safety

- No experiment reads or operates on `tests/`.
- No real file, database, network, CLI, or GUI side effect is performed.
- `StringIO` is an in-memory teaching substitute, not proof of real persistence
  behavior.
- Initial preparation created no P4 capstone, stage quiz, P4 stage note,
  C17-C21 practice files, or repository-level shared package. Later lifecycle
  gates produced the validated C16 quiz and P4 stage note; no C17 practice
  artifact was created during C16 closeout.
- Each numbered file remains an independent learning snapshot.
