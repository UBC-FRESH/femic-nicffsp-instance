# P11.4c MP11 Candidate Bundle Build Summary

This build materializes the generated MP11 candidate model-input bundle and export compatibility bridge under the ignored candidate root.

It does not generate ForestModel XML, Matrix Builder outputs, or Patchworks runtime artifacts.

## Generated Root

- Candidate bundle root: `data/mp11_model_input_bundle`
- Export compatibility bridge: `data/mp11_model_input_bundle/export_compat`

## Summary

- generated_at_utc: `2026-06-29T03:59:16+00:00`
- candidate_bundle_root: `data/mp11_model_input_bundle`
- active_mp11_curve_count: `18`
- accepted_phase10r_curve_rows: `27`
- duplicate_mp11_rows_deferred_by_canonical_au: `9`
- active_mp11_curve_point_rows: `648`
- affected_stand_rows: `8957`
- affected_au_rows: `83`
- export_compat_curve_rows: `172`
- export_compat_curve_point_rows: `30651`
- model_input_generation: `performed_candidate_scaffold`
- xml_generation: `not_performed`
- matrix_builder: `not_performed`
- runtime_bundle_generation: `not_performed`

## Record Counts

| Surface | Rows |
| --- | ---: |
| `au_table.csv` | 407 |
| `curve_table.csv` | 525 |
| `curve_points_table.csv` | 91488 |
| `stand_table.csv` | 25019 |
| `stand_au_assignment.csv` | 25019 |
| `stand_origin_assignment.csv` | 25019 |
| `treatment_table.csv` | 4 |
| `transition_table.csv` | 5 |
| `group_table.csv` | 125095 |
| `cedar_signal_table.csv` | 25019 |
| `embedded_identity_table.csv` | 25019 |
| `export_compat/au_table.csv` | 407 |
| `export_compat/curve_table.csv` | 172 |
| `export_compat/curve_points_table.csv` | 30651 |
| `export_compat/id_crosswalk.csv` | 579 |

## Caveats

- This is an MP11 candidate scaffold, not a final MP11 release model.
- The Phase 5 stand universe and treatment/transition scaffold are reused.
- Accepted Phase 10R Table 57 managed curves are injected where they map deterministically to canonical AU identities.
- Duplicate MP11 Table 57 rows mapping to the same canonical AU are not split into new stand AUs in this scaffold; the active row is selected by largest MP11 THLB area.
- P9RF source/THLB caveats remain model-contract caveats until a later source-layer rebuild replaces the scaffold.
