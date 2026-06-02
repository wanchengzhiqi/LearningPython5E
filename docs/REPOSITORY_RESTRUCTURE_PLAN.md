# LearningPython5E Repository Restructure Plan

## Purpose

This file was created as a recovery checkpoint for the repository-governance
refactor started after the `myimporter` second-round configuration cleanup.
The refactor finished without interruption. The file is now retained as a
historical execution record, directory-design rationale, and validation
baseline.

## Confirmed Context

- `LearningPython5E` is a long-running learning repository, not a single app.
- A learning **major stage** maps to a book `PART`, such as
  `P1_Getting_Started` or `P2_Types_and_Operations`.
- A learning **minor stage** maps to a chapter, such as
  `C9_Dictionaries_and_Files`.
- `practice/` stores chapter-oriented experiments and exercises.
- `notes/` stores durable learning notes and the mastery profile.
- `projects/` should store reusable major-stage capstone projects.
- `tests/` is a hard exclusion: do not edit, move, delete, stage, unstage, or
  clean files under it.

## Problems Being Corrected

1. `myimporter` is a major-stage capstone but is split across repository-root
   `src/`, `cli.py`, `runtime_service.py`, `web_ui/`, and `requirements.txt`.
2. `localization_resource_auditor` is already under `projects/`, but the
   `projects/` tree does not yet express which major stage owns each capstone.
3. The repository-root `README.md` currently doubles as a `myimporter` manual.
4. The repository-root `requirements.txt` currently contains dependencies for
   one capstone rather than the learning repository as a whole.
5. The repository-root `src/` name is ambiguous: it looks repository-wide but
   currently belongs to one historical capstone.

## Target Structure

```text
LearningPython5E/
  README.md
  AGENTS.md
  docs/
    REPOSITORY_RESTRUCTURE_PLAN.md
  notes/
  practice/
    P1_Getting_Started/
    P2_Types_and_Operations/
  projects/
    P1_Getting_Started/
      myimporter_system/
        README.md
        requirements.txt
        cli.py
        runtime_service.py
        web_ui/
        plugins/
        src/
          myimporter/
    P2_Types_and_Operations/
      localization_resource_auditor/
        README.md
        localization_auditor.py
        data/
  tests/
```

## Design Rules

- Treat capstone projects equally regardless of implementation depth.
- Put project-specific launchers, UI files, plugins, dependencies, and README
  files inside the owning project directory.
- Use `src/` only inside a project when it has a clear package-source meaning.
- Keep the repository-root README focused on the learning journey, directory
  conventions, stage model, and links to project manuals.
- Keep project-specific dependencies next to the project that needs them.
- Preserve ignored caches; do not bulk-delete files or directories.

## Execution Checklist

- [x] Inspect current tree, references, README files, and dependency ownership.
- [x] Write this recovery plan before moving files.
- [x] Create PART-oriented project directories.
- [x] Move the full `myimporter` capstone under
      `projects/P1_Getting_Started/myimporter_system/`.
- [x] Move `localization_resource_auditor` under
      `projects/P2_Types_and_Operations/`.
- [x] Convert internal imports from `src.myimporter` to the project-local
      `myimporter` package shape.
- [x] Update launchers, settings path derivation, sitecustomize template, and
      documentation references.
- [x] Replace the root README with a repository-level guide.
- [x] Update `AGENTS.md` to match the new structure and dependency ownership.
- [x] Update the external global `sitecustomize.py` from the repository template
      after obtaining the required filesystem approval.
- [x] Run focused validation without operating on `tests/`.
- [x] Record final validation results below.

## Required Validation

1. Run `python -m py_compile` for moved `myimporter` modules and launchers.
2. Run `python -m json.tool` for example plugin manifests.
3. Exercise installer mode transitions and failed-transition rollback.
4. Start RuntimeService on a temporary port and validate CLI commands:
   `list`, `reload`, `deactivate`, `activate`, `status`, `shutdown`.
5. Exercise Web UI routes with Flask's test client.
6. Confirm the worker subprocess exits after RuntimeService shutdown.
7. Confirm the global `sitecustomize.py` is silent by default and works when
   explicitly enabled with the required source-path environment variable.
8. Run `git diff --check` for authorized non-`tests/` paths.
9. Confirm that `tests/` remains untouched by this refactor.

## Validation Results

Completed on 2026-06-02:

- `python -m py_compile` passed for the moved `myimporter` package, launchers,
  Web UI, example plugins, and `localization_resource_auditor`.
- `python -m json.tool` passed for both example plugin manifests.
- Installer mode transitions passed:
  `safe_mod -> runtime_mod -> dev_mod -> runtime_mod -> safe_mod`.
- Invalid path input and missing `MY_MODULE_PATHS` failed without replacing the
  working finder.
- `localization_resource_auditor --format json` produced JSON accepted by
  `python -m json.tool`.
- RuntimeService passed a temporary-port lifecycle test with CLI commands:
  `list`, `reload`, `deactivate`, `activate`, `status`, `shutdown`.
- Flask test-client checks passed for dashboard, plugin list, reload, and the
  intentionally disabled remote-install endpoint.
- The subprocess worker exited after RuntimeService shutdown.
- Global `sitecustomize.py` stayed silent by default and worked when explicitly
  enabled with `ENABLE_MYIMPORTER`, `MYIMPORTER_SOURCE_ROOT`, and
  `MY_MODULE_PATHS`.
- The global `sitecustomize.py` SHA-256 matched the repository template.
- Repository-root `src/` now contains only an ignored `__pycache__/` directory.
  It was intentionally preserved because bulk cache cleanup is out of scope.
- Historical answers inside the C9 stage quiz retain their original pre-move
  paths as learning traces. Current operational documentation uses the new path.
- `tests/` was not edited, moved, deleted, staged, unstaged, or cleaned during
  this refactor.
