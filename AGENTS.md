# AGENTS.md

This file is the working contract for AI coding agents in this repository.

## Project Purpose

`femic-tfl6-instance` is the standalone FEMIC deployment instance for the
FRST 558 North Island / Tree Farm Licence 6 teaching case.
The target runtime is Patchworks, using the existing K3Z teaching model as the
closest style and structure reference.

## Current Repo State

The repository is in bootstrap state. It contains:

- FEMIC instance scaffolding under `config/`, `runbooks/`, and runtime folders;
- source payloads under `data/source/nicf_fsp/`;
- planning notes under `planning/`; and
- no accepted compiled model package yet.

Do not describe this repository as a runnable model package until the roadmap
records rebuilt model inputs, Patchworks Matrix Builder output, direct artifact
inspection, and launch/scenario smoke evidence.

## Source Data Handling

- Keep raw source provenance explicit.
- Use lowercase names for new canonical tracked paths.
- Do not publish machine-specific personal paths.
- Do not treat zipped source payloads as usable FEMIC inputs until their
  contents have been inspected and extracted into stable source paths.
- Keep generated model outputs, runtime logs, and scratch artifacts out of git
  unless the roadmap explicitly accepts a compact release payload.

## Planning Workflow

This repo uses an agent-assisted roadmap and GitHub issue workflow, modeled on
`modelwright` and aligned with FEMIC parent-repo practice.

- Keep the current plan in `ROADMAP.md`.
- Keep the immediate edge of work in the `Current Next Steps` section of
  `ROADMAP.md`.
- Record completed deliverables in `CHANGE_LOG.md` with dated bullets.
- Use `planning/` for focused notes and contracts that are too detailed for the
  roadmap.
- Before non-trivial work, update or confirm the roadmap entry that governs it.
- Use GitHub issues with `gh` in tandem with the roadmap.
- Map every roadmap phase to one GitHub parent issue in this instance repo.
- Map every roadmap task to one linked child issue under that phase parent.
- Keep lightweight subtasks as checklist items in the task child issue body.
- Create third-level implementation issues only when a task is too large to
  manage as one child issue; do not use more than three issue levels:
  phase parent, task child, implementation subtask.
- Record issue numbers beside roadmap phases and tasks as soon as they exist.
- Keep roadmap, changelog, commits, and issue comments synchronized as task
  state changes.

## Strict Development Workflow

Use this workflow for active development from each phase boundary onward:

- One active roadmap phase should correspond to one GitHub parent issue and one
  feature branch unless the maintainer explicitly approves a parallel lane.
- Create or activate the phase parent issue before starting phase work.
- Create child issues for roadmap tasks under the parent issue before
  implementing those tasks.
- Link child issues from the parent issue body, and add a backlink comment from
  each child issue to the parent.
- Work child issues one at a time where practical, in roadmap order.
- Before closing a child issue, update every issue-body checklist item to
  checked, or rewrite the body to make superseded/deferred items explicit.
- Close a child issue only after its repo changes, documentation, checklist
  state, validation, and issue comment trail are complete.
- Keep `ROADMAP.md`, `CHANGE_LOG.md`, planning notes, commits, PRs, and issue
  comments synchronized when status changes.
- Open a PR from the phase branch back to `main` when the parent issue's child
  issues are complete or explicitly deferred.
- Treat phase closeout as the next required slice after the final child issue or
  phase gate completes. Do not advance to the next phase's first task until the
  current phase closeout checklist, parent issue state, PR state, roadmap,
  changelog, and issue comments are reconciled.
- Close the parent phase issue only after the phase PR has merged back to
  `main`, or after all child work is explicitly deferred with a recorded
  rationale.
- Do not open implementation work for the next phase until the current phase
  parent issue is closed or the maintainer explicitly approves a parallel lane.

## FEMIC/Patchworks Guardrails

- Preserve the FEMIC parent-repo Patchworks semantics:
  `managed` / `unmanaged` means treatment eligibility, while
  `natural` / `treated` means curve provenance.
- Regenerate Patchworks-facing XML before Matrix Builder whenever exporter,
  silviculture, seral, treatment, state, product, account, or curve semantics
  change.
- Do not report Patchworks success from command exit codes alone. Inspect the
  concrete rebuilt outputs that could reveal regressions.
- The K3Z repository is a template/reference, not a blind copy target. Any
  copied assumption must be checked against the NICF FSP source payload and the
  FRST 558 teaching mission.

## Verification

Bootstrap-level validation:

```bash
femic instance validate-spec --spec config/rebuild.spec.yaml
```

Later runnable-model milestones should add, at minimum:

```bash
femic prep validate-case --run-config config/run_profile.nicffsp.yaml --tipsy-config-dir config/tipsy
femic instance rebuild --run-config config/run_profile.nicffsp.yaml --spec config/rebuild.spec.yaml
sphinx-build -b html docs docs/_build/html -W
```

Only run broad rebuilds after the roadmap states the exact question being
answered and the required source inputs are materialized.
