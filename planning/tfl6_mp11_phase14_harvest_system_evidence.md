# TFL 6 MP11 Phase 14 Harvest-System Evidence Inventory

This P14.2 inventory records MP11, historical, and public-source clues for the harvest-system operability classifier. It is evidence mining only: no classifier metrics, model-input tables, ForestModel XML, Matrix Builder outputs, Patchworks runtime artifacts, or scenario outputs are generated.

## Summary

- status: `harvest_system_evidence_inventory_built`
- row_count: `16`
- accepted public proxy input rows: `2`
- comparison target rows: `2`
- candidate rule rows: `3`
- private gap rows: `2`

## Decision Counts

| P14 decision | Count |
| --- | ---: |
| `accepted_public_proxy_context` | `1` |
| `accepted_public_proxy_input` | `2` |
| `adopt_vocabulary_not_geometry` | `1` |
| `boundary_condition` | `1` |
| `candidate_metric_after_review` | `1` |
| `candidate_proxy_clue` | `1` |
| `candidate_rule_after_metric_build` | `3` |
| `comparison_target_only` | `2` |
| `context_only_public_proxy` | `1` |
| `private_gap` | `1` |
| `reject_as_current_mp11_rule` | `1` |
| `unavailable_private_source` | `1` |

## Evidence Rows

| Evidence | Family | Role | Decision | Public/proxy use | Follow-up |
| --- | --- | --- | --- | --- | --- |
| `mp11_lbb_private_operability_source` | `physical_operability` | `unavailable_private_source` | `unavailable_private_source` | Do not use as a queryable source; record as private benchmark context. | Build public proxy assignments and label them as non-equivalent to WFP LBB. |
| `mp11_physical_operability_classes` | `physical_operability` | `classification_target` | `adopt_vocabulary_not_geometry` | Use class vocabulary and inoperable/non-conventional distinction. | Map public proxy rows to ground, cable, heli, not_applicable, or review-required. |
| `mp11_table20_thlb_area_distribution` | `comparison_target` | `aggregate_target` | `comparison_target_only` | Use as aggregate QA target only. | Report assigned-area residuals after public proxy classification. |
| `mp11_table73_area_volume_distribution` | `comparison_target` | `aggregate_target` | `comparison_target_only` | Use as area and volume QA target. | Compare proxy area and candidate inventory volume by harvest system. |
| `mp11_helicopter_economic_thresholds_near` | `economic_operability` | `explicit_rule_candidate` | `candidate_rule_after_metric_build` | Use if age, volume, species share, and flight/access proxy exist. | P14.3 must build species-share, volume, age, and access-distance proxy fields. |
| `mp11_helicopter_economic_thresholds_mid` | `economic_operability` | `explicit_rule_candidate` | `candidate_rule_after_metric_build` | Use if age, volume, species share, and flight/access proxy exist. | P14.3 must build species-share, volume, age, and access-distance proxy fields. |
| `mp11_helicopter_economic_thresholds_far` | `economic_operability` | `explicit_rule_candidate` | `candidate_rule_after_metric_build` | Use if age, volume, species share, and flight/access proxy exist. | P14.3 must build species-share, volume, age, and access-distance proxy fields. |
| `mp11_conventional_economic_assumption` | `economic_operability` | `rule_boundary` | `boundary_condition` | Do not add a broad conventional uneconomic exclusion in Phase 14. | Limit economic-operability rule work to heli/non-conventional sensitivity. |
| `mp11_no_current_system_dbh_mha` | `rule_rejection` | `do_not_use` | `reject_as_current_mp11_rule` | Do not use MP10 30/37/42 cm DBH rules as current MP11 criteria. | Keep MHA implementation separate from harvest-system classifier. |
| `mp10_slope_30_ground_cable_context` | `historical_context` | `proxy_clue` | `candidate_proxy_clue` | Use as a candidate proxy threshold to test, not as MP11 truth. | P14.3 should compute slope-threshold sensitivity metrics including 30%. |
| `p9d_public_cded_slope_stats` | `public_proxy_input` | `slope_metric` | `accepted_public_proxy_input` | Use as coarse public slope evidence for first classifier pass. | P14.3 must join or aggregate slope metrics onto candidate stands. |
| `p9d_step220_steep_slope_rule` | `public_proxy_input` | `slope_rule_context` | `accepted_public_proxy_context` | Use as high-steepness context for inoperable/high-cost flags. | Do not double-count Step 220 removed fragments as heli candidates. |
| `p9e_public_tsm_class_v` | `public_proxy_input` | `terrain_stability_context` | `context_only_public_proxy` | Use as terrain-stability caveat/context, not direct harvest-system class. | Carry terrain-stability status into classifier confidence/caveat fields. |
| `phase9_vri_inventory_metrics` | `public_proxy_input` | `inventory_metric` | `accepted_public_proxy_input` | Use for volume/ha, age, height, and species-share classifier metrics. | P14.3 must build Cw+Fd+Yc share and volume/age fields from candidate geometry. |
| `phase9_dra_roads` | `public_proxy_input` | `access_metric_candidate` | `candidate_metric_after_review` | Candidate access-distance input for heli economic proxy. | P14.3 should compute a distance-to-road/access proxy only after source path review. |
| `phase9_wfp_lbb_iti_lefi_manifest_gap` | `private_gap` | `do_not_materialize` | `private_gap` | Use only as a documented gap. | Keep private dependency gap visible in classifier QA and docs. |

## Key Interpretation

- WFP LBB is the governing MP11 source for harvest-system assignment, but it is not public/queryable in the current package.
- Public FEMIC work should use transparent proxy assignments with source, confidence, and caveat fields rather than claiming WFP LBB equivalence.
- MP11 Table 20 and Table 73 distributions are aggregate QA targets only.
- Helicopter economic-operability thresholds are explicit enough to become candidate rules after P14.3 builds age, volume, species-share, and access/flight-distance proxy metrics.
- The old MP10 DBH-by-harvest-system criteria are not current MP11 MHA rules and must not be used as Phase 14 classifier acceptance criteria.

## Files

- `planning/tfl6_mp11_phase14_harvest_system_evidence.csv`
- `planning/tfl6_mp11_phase14_harvest_system_evidence.json`
- `planning/tfl6_mp11_phase14_harvest_system_evidence.md`
