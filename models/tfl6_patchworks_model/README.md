# TFL 6 Patchworks Runtime Package

This directory is the active TFL 6 Patchworks runtime-package root for the
Phase 4 build lane.

Current scope:

- `tracks/` is the generated Matrix Builder track-table surface from P4.3.
- `blocks/` is the generated block/topology surface from P4.4a.
- `analysis/` contains the baseline `base.pin` launch surface and shared
  headless helper scripts.
- `lineage_registry.yaml` records the current package inputs, generation
  commands, and validation status.

Current modeling boundary:

- AFLB is the fragment/block universe.
- THLB is represented as a managed-share state inside the AFLB universe.
- NTHLB remains forested AFLB area with full retention / unmanaged Patchworks
  eligibility and untreated growth.
- Generic `CC` is the accepted first-pass clearcut-and-plant treatment lane.
- Ground/cable/heli harvest-system assignment is deferred to a later
  operability refinement.

Generated blocks, tracks, and saved-stage smoke outputs are currently ignored
in Git. Phase 5 publication policy will decide which runtime artifacts are
tracked, annexed, published, or regenerated.
