# P11.3c MP11 Candidate Provenance Review

This review locks the provenance and fallback-policy status for each P11.3 model-input candidate table role before P11.4 begins XML provenance audit work.

P11.3c does not generate model-input tables, ForestModel XML, Matrix Builder outputs, or Patchworks runtime artifacts.

## Inputs And Outputs

- Input manifest: `planning/tfl6_mp11_model_input_candidate_manifest.csv`
- Review CSV: `planning/tfl6_mp11_model_input_candidate_provenance_review.csv`
- Review JSON: `planning/tfl6_mp11_model_input_candidate_provenance_review.json`

## Summary

- Candidate table roles reviewed: `13`
- Blocked roles: `0`
- P11.3c unlock status: `p11_4a_audit_eligible`
- Model-input generation: `not_performed`
- ForestModel XML generation: `not_performed`
- Matrix Builder: `not_performed`
- Runtime bundle generation: `not_performed`

## Decision Counts

| Decision | Count |
| --- | ---: |
| `deferred_non_blocking` | 1 |
| `pass_candidate_scaffold` | 12 |

## Table-Role Review

| Table role | Action | Sources | Missing | Decision | P11.4a requirement |
| --- | --- | ---: | ---: | --- | --- |
| `stand_table` | `replace` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `au_table` | `extend` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `curve_table` | `replace` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `curve_points_table` | `replace` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `stand_au_assignment` | `extend` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `stand_origin_assignment` | `reuse` | 1 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `treatment_table` | `reuse` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `transition_table` | `reuse` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `harvest_system_table` | `defer` | 1 | 0 | `deferred_non_blocking` | Carry as deferred comparison metadata only; do not generate a table. |
| `group_table` | `extend` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `cedar_signal_table` | `extend` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `embedded_identity_table` | `reuse` | 1 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |
| `export_compat_bridge` | `replace` | 2 | 0 | `pass_candidate_scaffold` | Verify candidate output role during P11.4a XML provenance audit. |

## Candidate Boundary

All passing roles remain candidate-scaffold roles only. The single deferred role, `harvest_system_table`, remains comparison metadata and must not become a generated model-input table unless a later phase separately promotes stand-level harvest-system logic.

P11.4a may audit candidate XML provenance against this review, but P11.4a must still avoid writing ForestModel XML. XML generation is reserved for P11.4c after the P11.4a/P11.4b audit and generation contract checks pass.
