# TFL 6 MP11 Phase 13 KPI And Caveat Comparison Report

This report broadens the Phase 13 comparison beyond harvest flow. It consolidates tracked MP11 evidence, candidate-runtime evidence, source/THLB caveats, reviewed figure evidence, and runtime build evidence into one release-decision surface.

## Summary

- report_status: `kpi_caveat_report_built`
- row_count: `42`
- release_qa: `not_performed`
- release_decision: `pending_p13_5`

## Blocker And Caveat Counts

| Status | Count |
| --- | ---: |
| `caveated_not_blocking` | `7` |
| `comparison_context_only` | `11` |
| `needs_archive_materialization_qa` | `1` |
| `needs_reproducible_base_export` | `1` |
| `not_blocking` | `10` |
| `release_caveat` | `8` |
| `scenario_smoke_only` | `4` |

## KPI Family Counts

| Family | Count |
| --- | ---: |
| `aac_recommendation` | `1` |
| `base_case` | `1` |
| `harvest_flow` | `9` |
| `kpi` | `3` |
| `land_base` | `9` |
| `reviewed_figure_evidence` | `6` |
| `runtime_build` | `2` |
| `sensitivity` | `2` |
| `source_thlb_constraints` | `9` |

## High-Signal Rows

| ID | Family | Metric | Evidence | Blocker Status | Release Implication |
| --- | --- | --- | --- | --- | --- |
| `scenario_candidate_p12_5_runtime_mean` | `harvest_flow` | P12.5 tracked runtime smoke mean annual harvest | `tracked_runtime_output` | `scenario_smoke_only` | Shows runtime capability and order of magnitude, not release-calibrated base-case behavior. |
| `scenario_candidate_p12_5_runtime_min` | `harvest_flow` | P12.5 tracked runtime smoke minimum annual harvest | `tracked_runtime_output` | `scenario_smoke_only` | Useful runtime diagnostic only. |
| `scenario_candidate_p12_5_runtime_max` | `harvest_flow` | P12.5 tracked runtime smoke maximum annual harvest | `tracked_runtime_output` | `scenario_smoke_only` | Useful runtime diagnostic only. |
| `scenario_candidate_p12_5_runtime_final` | `harvest_flow` | P12.5 tracked runtime smoke final-period annual harvest | `tracked_runtime_output` | `scenario_smoke_only` | Useful runtime diagnostic only. |
| `scenario_candidate_maintainer_interactive_context` | `harvest_flow` | Maintainer interactive basic scenario context | `maintainer_context` | `needs_reproducible_base_export` | Motivates formal reproducible scenario export before release decisions. |
| `netdown_research_psp_big_tree_karst` | `source_thlb_constraints` | Additional land-base values: research, PSPs, big trees, karst | `tracked_mp11_table_or_text` | `release_caveat` | Follow-up lane P6.3/P6.4; keep visible in Phase 13 caveats. |
| `netdown_inoperable` | `source_thlb_constraints` | Inoperable | `tracked_mp11_table_or_text` | `release_caveat` | Follow-up lane P6.4; keep visible in Phase 13 caveats. |
| `netdown_terrain_stability_lidar_slope` | `source_thlb_constraints` | Terrain stability and LiDAR 90%+ slope | `tracked_mp11_table_or_text` | `release_caveat` | Follow-up lane P6.4; keep visible in Phase 13 caveats. |
| `behavior_alternate_harvest_flows` | `harvest_flow` | alternate_harvest_flows | `tracked_mp11_table_or_text` | `release_caveat` | Add explicit harvest-flow scenario definitions and QA metrics after MP11 model inputs are rebuilt. |
| `behavior_policy_and_constraint_sensitivities` | `sensitivity` | policy_and_constraint_sensitivities | `tracked_mp11_table_or_text` | `release_caveat` | Prioritize MHA, harvest-system exclusion, THLB adjustment, and genetic-gain sensitivities because their MP11 effects are numerically clear. |
| `behavior_aac_recommendation_bridge` | `aac_recommendation` | aac_recommendation_bridge | `tracked_mp11_table_or_text` | `release_caveat` | Treat the AAC recommendation as a high-level target for a future MP11-aligned scenario, gated on inventory/yield and flow-policy decisions. |
| `behavior_growing_stock_dynamics` | `kpi` | growing_stock_dynamics | `tracked_mp11_table_or_text` | `release_caveat` | Add comparable growing-stock reports once MP11-aligned Patchworks outputs exist. |
| `behavior_harvest_system_and_operational_kpis` | `kpi` | harvest_system_and_operational_kpis | `tracked_mp11_table_or_text` | `release_caveat` | Create public-data harvest-system proxies before attempting MP11-style operational KPI reports. |
| `runtime_matrix_builder_tracks` | `runtime_build` | Matrix Builder track generation | `tracked_runtime_output` | `needs_archive_materialization_qa` | Supports runtime buildability; archive/materialization QA remains P13.4. |

## Interpretation

The candidate runtime has enough evidence to proceed with Phase 13 documentation and archive QA, but this report still carries release caveats. The strongest positive signals are the close candidate THLB context, the smoke-tested runtime package, and harvest-flow behavior in the right broad range. The main blockers or caveats are reproducible export of the maintainer basic scenario, unresolved WFP/private constraint surfaces, harvest-system/MHA/scenario-policy gaps, and public-safe archive/materialization decisions.

This report does not decide release status. P13.5 must decide whether the MP11 candidate replaces Phase 5, supplements Phase 5, or remains experimental after docs and archive QA complete.
