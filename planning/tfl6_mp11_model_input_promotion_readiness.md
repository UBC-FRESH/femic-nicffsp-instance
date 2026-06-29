# TFL 6 MP11 Model-Input Promotion Readiness

## Purpose

This P11.2 audit classifies whether MP11 source, THLB, curve, rule,
schema, reporting, private-data, XML, and runtime boundaries are ready
for model-input promotion. It is a planning manifest only.

## Summary

- Rows: `11`
- Decision counts: `{"deferred": 2, "pass": 9}`
- Blocked hard gates: `0`
- P11.3 unlock status: `candidate_manifest_eligible`

## Gate Decisions

| gate_id | gate_type | target_role | actual_promotion_state | decision | next_action_owner |
| --- | --- | --- | --- | --- | --- |
| p11_gate_01_baseline_protection | hard | all generated outputs | accepted_model_contract | pass | P11.3 candidate manifest |
| p11_gate_02_source_thlb | hard | stand universe and THLB/NTHLB state | accepted_candidate_scaffold_contract_with_caveats | pass | P11.3 candidate manifest source/THLB caveat fields |
| p11_gate_03_curve_handoff | hard | natural and managed curves | accepted_phase11_curve_handoff_not_model_input | pass | P11.3 curve table candidate manifest |
| p11_gate_04_deferred_tables_54_55 | hard | early/recent managed curves | deferred_missing_public_safe_au_mapping | pass | Future public-safe AU mapping issue |
| p11_gate_05_figure_evidence | hard | all numeric model fields | excluded_from_model_input | pass | P11.3 field-source filter |
| p11_gate_06_rule_contracts | hard | treatments transitions MHA harvest system operability scenarios | accepted_candidate_scaffold_with_deferred_rule_fields | pass | P11.3 candidate manifest rule-status fields |
| p11_gate_07_schema_bridge | hard | model-input tables and export compatibility | accepted_candidate_schema_bridge_manifest_only | pass | P11.3 candidate model-input manifest |
| p11_gate_08_private_data | hard | all promoted fields | unavailable_non_public_or_proxy_only | pass | P11.3 private-data exclusion check |
| p11_gate_09_kpi_reporting | soft | reporting and QA fields | comparison_and_reporting_contract_only | deferred | P11.3 candidate manifest non-blocking KPI deferral |
| p11_gate_10_xml_readiness | soft | ForestModel XML | deferred_until_p11_3_candidate_manifest | deferred | P11.4 XML readiness manifest |
| p11_gate_11_runtime_boundary | soft | Matrix Builder and Patchworks runtime | phase12_or_later | pass | Phase 12 runtime handoff |

## Blocked Hard Gates

- No hard gates are blocked.

## Use Boundary

- This manifest does not generate model-input bundle tables.
- This manifest does not generate ForestModel XML.
- This manifest does not run Matrix Builder or Patchworks runtime.
- P11.3 may start only if all hard gates pass after maintainer review.
