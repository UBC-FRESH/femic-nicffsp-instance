# TFL 6 MP11 Model-Input Candidate Manifest

## Purpose

This P11.3b manifest defines candidate model-input table roles, source
artifacts, output paths, caveat fields, and fallback policies. It does
not generate model-input tables, ForestModel XML, Matrix Builder outputs,
or Patchworks runtime artifacts.

## Summary

- Rows: `13`
- Status: `candidate_manifest_ready`
- Readiness unlock status: `candidate_manifest_eligible`
- Blocked hard gates: `0`
- Generation eligibility counts: `{"deferred_not_eligible": 1, "eligible_for_later_generated_scaffold": 12}`

## Candidate Table Roles

| table_role | bridge_action | generation_eligibility | downstream_status | candidate_output_path |
| --- | --- | --- | --- | --- |
| stand_table | replace | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/stand_table.csv |
| au_table | extend | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/au_table.csv |
| curve_table | replace | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/curve_table.csv |
| curve_points_table | replace | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/curve_points_table.csv |
| stand_au_assignment | extend | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/stand_au_assignment.csv |
| stand_origin_assignment | reuse | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/stand_origin_assignment.csv |
| treatment_table | reuse | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/treatment_table.csv |
| transition_table | reuse | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/transition_table.csv |
| harvest_system_table | defer | deferred_not_eligible | deferred_not_model_input |  |
| group_table | extend | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/group_table.csv |
| cedar_signal_table | extend | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/cedar_signal_table.csv |
| embedded_identity_table | reuse | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/embedded_identity_table.csv |
| export_compat_bridge | replace | eligible_for_later_generated_scaffold | candidate_manifest_only | data/mp11_model_input_bundle/export_compat/bridge_manifest.json |

## Required Caveats

- P9RF source/THLB is candidate-scaffold evidence only.
- Tables 54/55 remain excluded without a public-safe AU-code mapping.
- Figure-derived values remain excluded from model-input fields.
- MP11 MHA, harvest-system assignment, helicopter economic operability,
  and scenario policy remain deferred unless separately promoted.
- WFP private dependencies remain unavailable, proxy-only,
  sensitivity-only, or deferred.

## Use Boundary

- This manifest may support a later P11.3 generated scaffold decision.
- It does not itself authorize generated model-input tables.
- It does not authorize ForestModel XML generation.
- Matrix Builder and Patchworks runtime remain out of scope.
