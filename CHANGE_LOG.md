# Change Log

## 2026-06-23 - Bootstrapped the NICF FSP FRST 558 instance repository

- created the FEMIC instance scaffold for `femic-nicffsp-instance`;
- added modelwright-style workflow surfaces (`AGENTS.md`, `ROADMAP.md`,
  `CHANGE_LOG.md`, and `planning/`);
- tracked the initial NICF FSP AOI, LU, and FSP source payloads under lowercase
  repo-relative paths; and
- recorded the first build-plan boundary: source inspection and K3Z-template
  adaptation must happen before any Patchworks runtime success is claimed.

## 2026-06-23 - Split Phase 1 into task-wise GitHub issues

- narrowed `#1` to `P1.2` source-payload inspection and normalization;
- opened `#3` for the `P1.3` K3Z-to-NICF adaptation contract;
- opened `#2` for the `P1.4` cedar, expansion, and runtime-package follow-on
  issue split; and
- updated the roadmap so the active edge stays on `P1.2` source normalization
  before model design or compilation work starts.

## 2026-06-23 - Added the Phase 1 parent issue

- opened parent phase issue `#4` for Phase 1;
- linked child task issues `#1`, `#3`, and `#2` from the parent issue body;
- added child-issue backlinks to `#4`; and
- updated the roadmap so Phase 1 follows the modelwright parent/child issue
  workflow.
