# P11.4a MP11 ForestModel XML Provenance Audit

This audit records the Phase 5 ForestModel XML/fragments provenance and the MP11 candidate bridge treatment before P11.4b builds an XML readiness manifest or stop report.

P11.4a does not generate model-input tables, ForestModel XML, Matrix Builder outputs, or Patchworks runtime artifacts.

## Outputs

- Audit CSV: `planning/tfl6_mp11_phase11_xml_provenance_audit.csv`
- Audit JSON: `planning/tfl6_mp11_phase11_xml_provenance_audit.json`

## Baseline XML Evidence

- Baseline XML: `output/patchworks_tfl6_validated/forestmodel.xml`
- SHA256: `f95a7e29b95a9fcfabdd77036e3ac19611041e704a0aeef6257def190b2ff6a4`
- Root: `ForestModel`
- Year / horizon: `2026` / `300`
- Fragment sidecar files: `5`

## Required Notes

| Note | Present |
| --- | --- |
| `phase5_export_bridge_note` | `true` |
| `phase5_export_blocker_note` | `true` |
| `artifact_layout_note` | `true` |

## Summary

- XML/component families audited: `8`
- P11.4b-required families: `7`
- Non-blocking deferred families: `1`
- P11.4a unlock status: `p11_4b_readiness_eligible`
- Model-input generation: `not_performed`
- ForestModel XML generation: `not_performed`
- Matrix Builder: `not_performed`
- Runtime bundle generation: `not_performed`

## Component Audit

| Component | Source role | Action | Blocker status | P11.4b check |
| --- | --- | --- | --- | --- |
| `stand_universe_fragments` | `stand_table` | `replace_after_readiness` | `p11_4b_required` | Confirm candidate stand universe, THLB/NTHLB state, retained area, managed/unmanaged area, and group caveats before fragment export. |
| `export_compat_bridge` | `export_compat_bridge` | `replace_after_readiness` | `p11_4b_required` | Require deterministic AU/curve ID bridge and accepted candidate bundle paths before XML generation. |
| `curve_definitions` | `curve_table; curve_points_table` | `replace_after_readiness` | `p11_4b_required` | Map every candidate curve ID to XML curve definitions and verify Tables 54/55 remain excluded. |
| `au_selects_and_assignments` | `au_table; stand_au_assignment; stand_origin_assignment` | `extend_or_reuse_after_readiness` | `p11_4b_required` | Verify candidate AU, origin, and stand-AU assignment fields can produce complete XML selects without unmapped stands. |
| `treatments` | `treatment_table` | `reuse_with_caveats` | `p11_4b_required` | Confirm generic treatment reuse is explicit and MP11 MHA, harvest-system, and scenario rules remain deferred metadata. |
| `transitions` | `transition_table` | `reuse_with_caveats` | `p11_4b_required` | Confirm transition reuse is explicit and any MP11 transition fields remain deferred unless separately promoted. |
| `harvest_system_rules` | `harvest_system_table` | `defer_not_xml_input` | `non_blocking_deferred` | Verify no candidate XML treatment or report depends on stand-level harvest-system assignments. |
| `reporting_groups` | `group_table; cedar_signal_table; embedded_identity_table` | `extend_after_readiness` | `p11_4b_required` | Verify which reporting groups are XML-facing, which remain Matrix/QA-facing, and which MP11 cedar/caveat signals are metadata only. |

## Boundary

P11.4b may now build an XML readiness manifest from these audited component families. P11.4a itself does not authorize XML writes. Candidate XML generation remains reserved for P11.4c after P11.4b confirms the component readiness and generation contract.
