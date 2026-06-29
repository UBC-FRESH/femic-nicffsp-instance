# P11.6 Phase 11 Closeout

Phase 11 is closed as a model-input and ForestModel XML build phase.
It built the MP11 candidate model-input bundle, export bridge,
ForestModel XML, and fragments needed by Phase 12.

Phase 11 did not run Matrix Builder, assemble a Patchworks runtime,
run scenarios, publish a release archive, or replace the accepted
Phase 5 teaching/runtime baseline.

## Summary

- generated_at_utc: `2026-06-29T04:08:39+00:00`
- phase11_status: `complete_model_input_xml_handoff`
- candidate_bundle_root: `data/mp11_model_input_bundle`
- candidate_xml: `output/patchworks_tfl6_mp11_candidate/forestmodel.xml`
- candidate_fragments: `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp`
- active_mp11_curve_count: `18`
- duplicate_mp11_rows_deferred_by_canonical_au: `9`
- xml_root: `ForestModel`
- xml_curve_nodes: `13197`
- fragment_rows: `24879`
- fragment_area_ha: `191168.566447`
- matrix_builder: `not_performed`
- runtime_bundle_generation: `not_performed`
- phase12_handoff_status: `phase12_runtime_handoff_ready`

## Closeout Items

| Item | Status | Path | Phase 11 result | Next owner |
| --- | --- | --- | --- | --- |
| `candidate_model_input_bundle` | `built` | `data/mp11_model_input_bundle/` | Generated candidate scaffold and export bridge. | `P12.1-P12.2` |
| `candidate_forestmodel_xml` | `built` | `output/patchworks_tfl6_mp11_candidate/forestmodel.xml` | Generated candidate ForestModel XML for Matrix Builder input. | `P12.2` |
| `candidate_fragments` | `built` | `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp` | Generated candidate fragments alongside XML. | `P12.2` |
| `phase5_baseline` | `preserved` | `data/model_input_bundle/ and output/patchworks_tfl6_validated/` | Accepted teaching/runtime baseline was not overwritten. | `Phase 13 release decision` |
| `matrix_builder_tracks` | `not_performed` | `models/tfl6_patchworks_model_mp11_candidate/tracks/` | Deliberately left for the runtime-build phase. | `P12.2` |
| `runtime_bundle` | `not_performed` | `models/tfl6_patchworks_model_mp11_candidate/` | Patchworks runtime assembly is not a Phase 11 output. | `P12.3` |
| `scenario_smoke` | `not_performed` | `models/tfl6_patchworks_model_mp11_candidate/analysis/` | Direct launch and scenario smoke wait for runtime assembly. | `P12.4-P12.5` |

## Caveats Carried Forward

- This is an MP11 candidate scaffold, not a final release model.
- The Phase 5 stand universe and treatment/transition scaffold are reused.
- P9RF source/THLB exclusions and sensitive-source caveats remain visible.
- The accepted 27 Phase 10R Table 57 rows materialize as 18 active MP11 candidate curves because duplicate rows map to canonical AU identities.
- Tables 54/55 remain excluded until a public-safe AU-code mapping exists.
- Harvest-system and MHA policy fields remain deferred comparison/QA metadata.

## Phase 12 Start Point

Phase 12 starts from these generated candidate inputs:

- `output/patchworks_tfl6_mp11_candidate/forestmodel.xml`
- `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp`
- `data/mp11_model_input_bundle/export_compat/bridge_manifest.json`

The next build step is P12.2 Matrix Builder. It must write tracks under `models/tfl6_patchworks_model_mp11_candidate/tracks/`, then inspect accounts, protoaccounts, features, products, curves, blocks, and treatment/group signals before any runtime success claim.
