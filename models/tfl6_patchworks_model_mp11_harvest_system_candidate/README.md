# TFL 6 MP11 Harvest-System Candidate Patchworks Runtime Package

This directory is the active Phase 14 harvest-system candidate Patchworks runtime-package root for the MP11 supplement.

Current scope:

- `tracks/` is the generated Matrix Builder track-table surface from P14.6.
- `blocks/` is the generated block/topology surface from P14.6.
- `analysis/` contains the candidate `base.pin` launch surface and shared headless helper scripts copied from the Phase 12 MP11 candidate runtime pattern.
- `lineage_registry.yaml` records package inputs, generation commands, validation status, caveats, and the Phase 14 handoff boundary.

Current modeling boundary:

- This is an MP11 harvest-system candidate scaffold, not a final release model.
- WFP LBB geometry remains unavailable; `HVSYS` is a public-proxy field from P14.4.
- The runtime exposes split `CC_GROUND`, `CC_CABLE`, and `CC_HELI` treatment lanes.
- Aggregate `.CC` product labels are retained for all-system harvest-flow reporting.
- Matrix Builder and block/topology assembly passed in P14.6.
- Direct launch smoke, all-system scenario smoke, no-heli scenario smoke, documentation, and closeout remain downstream Phase 14 tasks.

Generated blocks, tracks, saved-stage outputs, logs, and package scratch files remain ignored in Git. Tracked planning manifests carry compact provenance and QA summaries.
