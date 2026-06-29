# TFL 6 MP11 Phase 12 Runtime Closeout

This note closes the Phase 12 MP11 candidate Patchworks runtime-smoke lane and hands the candidate runtime package to Phase 13 comparison documentation and release QA. Phase 12 built and smoke-tested a candidate runtime; it did not perform release QA, publish a release archive, calibrate an AAC recommendation, or claim equivalence with Western Forest Products' internal model.

## Summary

- closeout_status: `candidate_runtime_smoke_pass_phase13_ready`
- parent_issue: `#69`
- child_issue: `#119`
- matrix_run_id: `tfl6_mp11_candidate_p12_2_matrix_build`
- direct_launch_run_id: `tfl6_mp11_candidate_p12_4_launch0`
- scenario_run_id: `tfl6_mp11_candidate_p12_5_harvest_smoke200k`
- release_qa: `not_performed`
- phase13_handoff: `ready`

## Runtime Evidence

| Surface | Evidence | Status |
| --- | --- | --- |
| Matrix Builder tracks | `13` track files; `86574` feature rows; `823` account rows; `26085` product rows; `0` message rows | `matrix_builder_tracks_generated_inspection_pass` |
| Runtime blocks/topology | `24879` block rows; `191168.566447` ha; `170759` topology rows | `candidate_runtime_package_assembled` |
| Direct launch smoke | `3359` saved-stage files | `direct_launch_smoke_pass` |
| Scenario smoke | `200000` iterations; `76726` scheduled rows; `MANAGED` / `CC` | `scenario_smoke_pass` |

## Scenario Target Evidence

- The base harvested-volume target used a linear penalty shape and a `20,000,000` per-period minimum.
- The scheduler primed harvested volume before even-flow activation, as recorded in `planning/tfl6_mp11_scenario_smoke_qa.json`.
- The even-flow target retained the default non-linear penalty shape with min/max weights `10,000` for all periods.
- The final-period base harvested-volume current value was `14104784.0`.

## Hard Checks

| Check | Result |
| --- | --- |
| `matrix_builder_tracks` | `True` |
| `runtime_package_manifest` | `True` |
| `direct_launch_smoke` | `True` |
| `scenario_smoke` | `True` |
| `scenario_trace_order` | `True` |
| `scenario_saved_outputs` | `True` |
| `generated_runtime_outputs` | `True` |
| `no_logged_warning_error_matches` | `True` |

## Phase 13 Inputs

| Input | Path | Status |
| --- | --- | --- |
| `candidate_runtime_package` | `models/tfl6_patchworks_model_mp11_candidate/` | `candidate_smoke_passed` |
| `matrix_builder_tracks_qa` | `planning/tfl6_mp11_matrix_builder_tracks_qa.{csv,json,md}` | `matrix_builder_tracks_generated_inspection_pass` |
| `runtime_package_manifest` | `planning/tfl6_mp11_runtime_package_manifest.{csv,json,md}` | `candidate_runtime_package_assembled_pending_launch_smoke` |
| `direct_launch_qa` | `planning/tfl6_mp11_direct_launch_qa.{csv,json,md}` | `direct_launch_smoke_pass` |
| `scenario_smoke_qa` | `planning/tfl6_mp11_scenario_smoke_qa.{csv,json,md}` | `scenario_smoke_pass` |
| `lineage_registry` | `models/tfl6_patchworks_model_mp11_candidate/lineage_registry.yaml` | `updated_for_phase12_closeout` |

## Caveats

- Phase 12 proves candidate runtime buildability and smoke behavior, not final MP11 release readiness.
- The Phase 5 stand universe and treatment/transition scaffold remain reused.
- P9RF source/THLB caveats remain visible until a later public-source rebuild resolves or replaces them.
- Tables 54/55 remain excluded until a public-safe AU-code mapping exists.
- Harvest-system assignment remains deferred comparison metadata, not a stand-level treatment classifier.
- Release archive QA, documentation publication, scenario comparison, and Phase 5 replacement decisions are Phase 13 work.
- WFP model equivalence and approved AAC claims are out of scope for Phase 12.

## Phase 13 Boundary

Phase 13 should consume this candidate runtime as a smoke-tested rebuild artifact and decide whether it is suitable for comparison documentation, release packaging, teaching updates, and replacement/supplement positioning relative to the completed Phase 5 runtime baseline. Phase 13 must keep the Phase 5 baseline preserved until release QA and publication decisions explicitly pass.
