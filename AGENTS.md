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
- Before phase closeout, update all relevant user-facing Sphinx documentation
  and any affected Python API docstrings. This is mandatory for every roadmap
  phase, including phases that primarily produce planning, source-layer,
  geospatial, model-input, runtime, or QA artifacts. If no Python API docstrings
  are affected, say so explicitly in the closeout evidence. If user-facing docs
  are not updated, the phase is not closed.
- Phase PRs must include full QA/QC evidence: local validation commands,
  Sphinx warning-clean build when docs exist or are touched, issue/roadmap/
  changelog synchronization, and a clear statement of generated artifacts that
  remain intentionally untracked.
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

## Critical Model-Building Quality Gates

Some tasks control the credibility of every downstream model result. THLB
netdown, AFLB/THLB/NTHLB area accounting, AU assignment, yield-curve generation,
model-input bundle construction, ForestModel XML generation, Matrix Builder
execution, and Patchworks runtime smoke are critical gates. Treat these as
engineering and scientific accountability points, not as paperwork milestones.

For critical gates:

- Work one auditable step at a time unless the maintainer explicitly approves a
  broader batch run.
- State the checkpoint target, tolerance, source inputs, rule being applied,
  and stop condition before running the step.
- Emit compact evidence for each step: input paths, rule text, feature counts,
  gross area, ordered/overlap-adjusted deduction, cumulative area, residual
  against target, model-input status, and interpretation.
- Prefer partial-area/resultant-fragment accounting for spatial deductions.
  Never drop whole stands because they intersect a road, stream, reserve, or
  buffer unless the governing rule explicitly requires whole-polygon removal.
- Separate diagnostic scenarios from accepted deductions. Name scenarios as
  `review_only`, `proposed`, `locked_for_current_run`, or `accepted`, and do
  not blur those states.
- Do not close a critical task as successful when the output misses its
  checkpoint materially. Close it only as a failed diagnostic or blocker, and
  immediately record the repair task/phase before advancing.
- Do not advance to the next roadmap phase after a failed critical gate by
  leaving a caveat in a note. A failed critical gate blocks downstream work
  unless the maintainer explicitly accepts a blocker path.
- If a result is benchmark-calibrated, say so plainly, document the rationale,
  and keep it out of model-input status until it passes review.
- When a result looks implausible, stop and diagnose the method before
  producing more downstream artifacts.
- Progress reporting must surface failed or questionable critical-gate results
  immediately, with numbers. Do not bury them in closeout prose.

The expected standard is the Step 0/10/10b/20/30 P9R THLB workflow: isolate one
rule, compute a reviewable result, compare it to the published checkpoint,
explain the residual, correct the method if needed, and stop before the next
deduction until the current gate is defensible.

## Real Blockers And Stop Conditions

When a required external executable, proprietary runtime, private input, source
layer, credential, maintainer decision, or benchmark-defining assumption is
missing, that is a real blocker. Do not convert a real blocker into adjacent
make-work, speculative downstream tasks, placeholder artifacts, or roadmap
progress.

For real blockers:

- Stop the affected task at the blocker boundary.
- State exactly what is missing, where it was searched for, why it is required,
  and what work remains impossible without it.
- Commit only useful pre-blocker work: parsers, manifests, diagnostics,
  validation evidence, issue/roadmap/changelog synchronization, and a concise
  handoff package.
- Ask the maintainer for the missing input or an explicit decision before doing
  more work downstream of the blocker.
- Do not advance the roadmap edge, close the issue as successful, open
  downstream implementation tasks, or produce substitute artifacts unless the
  maintainer explicitly approves a blocker path.
- If the next useful action belongs in another environment, write a handoff note
  with exact branch, commit, paths, commands, expected inputs, expected outputs,
  and validation checks.

For TIPSY, VDYP, Patchworks, Matrix Builder, or other non-public/proprietary
toolchain steps, executable absence is a stop condition. A coding agent may
record the blocker and prepare handoff instructions, but must not claim model
input, yield curve, Matrix Builder, or Patchworks progress until the appropriate
runtime has actually been supplied and its outputs have been inspected.

## Verification

Bootstrap-level validation:

```bash
femic instance validate-spec --spec config/rebuild.spec.yaml
```

Later runnable-model milestones should add, at minimum:

```bash
femic prep validate-case --run-config config/run_profile.tfl6.yaml --tipsy-config-dir config/tipsy
femic instance rebuild --run-config config/run_profile.tfl6.yaml --spec config/rebuild.spec.yaml
sphinx-build -b html docs docs/_build/html -W
```

Only run broad rebuilds after the roadmap states the exact question being
answered and the required source inputs are materialized.
