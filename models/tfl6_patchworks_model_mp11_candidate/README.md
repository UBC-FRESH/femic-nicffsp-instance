# TFL 6 MP11 Candidate Patchworks Runtime Package

This directory is the active MP11 candidate Patchworks runtime-package root for
the Phase 12 build lane.

Current scope:

- `tracks/` is the generated Matrix Builder track-table surface from P12.2.
- `blocks/` is the generated block/topology surface from P12.3.
- `analysis/` contains the candidate `base.pin` launch surface and shared
  headless helper scripts copied from the accepted Phase 5 runtime pattern.
- `lineage_registry.yaml` records package inputs, generation commands,
  validation status, caveats, and the Phase 12/13 handoff boundary.

Current modeling boundary:

- This is an MP11 candidate scaffold, not a final release model.
- The Phase 5 stand universe and treatment/transition scaffold are reused.
- P9RF source/THLB caveats remain visible until a later source-layer rebuild.
- Generic `CC` remains the only accepted treatment lane in the candidate tracks.
- Harvest-system assignment remains deferred comparison metadata, not a
  stand-level treatment classifier.
- Direct launch smoke and representative scenario smoke passed in Phase 12.
- Release QA, comparison documentation, publication, and baseline replacement
  decisions remain downstream Phase 13 work.

Generated blocks, tracks, saved-stage outputs, logs, and package scratch files
remain ignored in Git. Tracked planning manifests carry compact provenance and
QA summaries.
