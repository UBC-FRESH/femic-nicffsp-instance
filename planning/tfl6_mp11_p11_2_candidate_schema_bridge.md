# TFL 6 MP11 P11.2 Candidate Schema Bridge

## Purpose

This P11.2 bridge defines the table-role decisions that allow P11.3 to build a
candidate model-input manifest. It reuses the Phase 5 bundle family as the
scaffold shape, but does not generate model-input tables.

Companion structured files:

- `planning/tfl6_mp11_p11_2_candidate_schema_bridge.csv`
- `planning/tfl6_mp11_p11_2_candidate_schema_bridge.json`

## Bridge Policy

P11.3 must assign every candidate table role one of these actions:

- `reuse`: use the Phase 5 table family as a scaffold/reference shape;
- `replace`: replace the Phase 5 source for candidate planning with an MP11
  candidate source;
- `extend`: preserve Phase 5 structure but add MP11 candidate provenance or QA
  fields; or
- `defer`: keep the role out of model-input generation until later review.

Candidate outputs must use the MP11 roots from
`planning/tfl6_mp11_phase11_artifact_layout.md`. Accepted Phase 5 paths must
not be overwritten.

## Candidate Table Roles

| Table role | Bridge action | P11.3 candidate source |
| --- | --- | --- |
| `stand_table` | `replace` | P9RF resultant-fragment source/THLB candidate contract |
| `au_table` | `extend` | Phase 5 AU scaffold plus accepted Phase 10R curve-handoff targets |
| `curve_table` | `replace` | accepted 27 Phase 10R Table 57 managed curves plus retained natural curves |
| `curve_points_table` | `replace` | accepted Phase 10R managed curve points and retained natural curve points |
| `stand_au_assignment` | `extend` | Phase 5 assignment scaffold plus MP11 candidate provenance fields |
| `stand_origin_assignment` | `reuse` | Phase 5 origin scaffold until MP11 source review replaces it |
| `treatment_table` | `reuse` | Phase 5 defaults with MP11 rule gaps marked deferred |
| `transition_table` | `reuse` | Phase 5 defaults with MP11 transition gaps marked deferred |
| `harvest_system_table` | `defer` | no accepted MP11 stand-level harvest-system classifier yet |
| `group_table` | `extend` | Phase 5 reporting scaffold plus P9RF/MP11 candidate caveat groups |
| `cedar_signal_table` | `extend` | Phase 5 cedar-reporting scaffold plus MP11 comparison/provenance fields |
| `embedded_identity_table` | `reuse` | preserve Phase 5 embedded identity scaffold |
| `export_compat_bridge` | `replace` | new MP11 candidate bridge if P11.3 later emits generated tables |

## P11.3 Manifest Requirement

P11.3 must emit
`planning/tfl6_mp11_model_input_candidate_manifest.{csv,json,md}` before any
generated candidate tables are written. The manifest must record:

- table role;
- bridge action;
- source artifact;
- candidate output path if generation is later authorized;
- required caveat fields;
- downstream status; and
- whether the role is eligible for table generation, deferred, or blocked.

This bridge resolves `p11_gate_07_schema_bridge` only for candidate-manifest
work. It does not authorize ForestModel XML, Matrix Builder, or runtime work.
