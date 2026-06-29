# P11.5 Phase 12 Runtime Handoff

This handoff packages the generated MP11 candidate model-input/XML surfaces for Phase 12 Matrix Builder and runtime smoke work.

P11.5 does not run Matrix Builder, assemble a Patchworks runtime, run scenario smoke, or publish a release archive.

## Summary

- generated_at_utc: `2026-06-29T04:08:38+00:00`
- handoff_status: `phase12_runtime_handoff_ready`
- candidate_bundle_root: `data/mp11_model_input_bundle`
- active_mp11_curve_count: `18`
- duplicate_mp11_rows_deferred_by_canonical_au: `9`
- xml_readiness_ready_count: `7`
- xml_readiness_blocked_count: `0`
- xml_path: `output/patchworks_tfl6_mp11_candidate/forestmodel.xml`
- xml_curve_nodes: `13197`
- fragment_rows: `24879`
- fragment_area_ha: `191168.566447`
- matrix_builder: `not_performed`
- runtime_bundle_generation: `not_performed`
- scenario_smoke: `not_performed`
- release_qa: `not_performed`

## Phase 12 Inputs

| Item | Path | Phase 12 owner | Status | Caveat |
| --- | --- | --- | --- | --- |
| `matrix_builder_input_xml` | `output/patchworks_tfl6_mp11_candidate/forestmodel.xml` | `P12.2` | `ready_for_matrix_builder_candidate` | Candidate scaffold XML; not final MP11 release truth. |
| `matrix_builder_fragments` | `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp` | `P12.2` | `ready_for_matrix_builder_candidate` | Fragments inherit Phase 5 stand universe and P9RF/source caveats. |
| `candidate_bundle` | `data/mp11_model_input_bundle/` | `P12.1` | `generated_candidate_scaffold` | Generated and ignored; tracked summaries carry compact provenance. |
| `candidate_export_bridge` | `data/mp11_model_input_bundle/export_compat/` | `P12.2` | `ready_for_exporter_runtime_bridge` | Bridge is deterministic numeric compatibility surface for FEMIC exporter. |
| `matrix_builder_tracks_root` | `models/tfl6_patchworks_model_mp11_candidate/tracks/` | `P12.2` | `not_started_phase12` | Do not create until Matrix Builder runs in Phase 12. |
| `runtime_package_root` | `models/tfl6_patchworks_model_mp11_candidate/` | `P12.3` | `not_started_phase12` | Runtime assembly, launch surfaces, and topology are Phase 12 work. |
| `scenario_smoke` | `models/tfl6_patchworks_model_mp11_candidate/analysis/` | `P12.4-P12.5` | `not_started_phase12` | Direct launch and scenario smoke must follow Matrix Builder/runtime assembly. |

## Required Phase 12 Sequence

1. Launch P12.1 with child issues for Matrix Builder, runtime assembly, direct launch smoke, scenario smoke, and closeout.
2. Run Matrix Builder from `output/patchworks_tfl6_mp11_candidate/forestmodel.xml` and `output/patchworks_tfl6_mp11_candidate/fragments/`.
3. Inspect generated tracks before runtime claims: accounts, protoaccounts, features, products, curves, blocks, and treatment/group signals.
4. Assemble the candidate runtime under `models/tfl6_patchworks_model_mp11_candidate/`.
5. Run direct launch smoke and representative scenario smoke before any Phase 13 release/docs QA claim.

## Candidate Caveats

- This is a candidate scaffold, not a final MP11 release model.
- The Phase 5 stand universe and treatment/transition scaffold are reused.
- P9RF source/THLB caveats remain visible until a later source-layer rebuild replaces the scaffold.
- The accepted 27 Phase 10R Table 57 rows materialize as 18 active MP11 candidate curves because duplicate rows map to already-selected canonical AU identities.
- Tables 54/55 remain excluded until a public-safe AU-code mapping exists.
- Harvest-system assignment remains deferred comparison metadata, not a stand-level treatment classifier.
