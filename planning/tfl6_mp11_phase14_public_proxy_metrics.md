# TFL 6 MP11 Phase 14 Public Proxy Metrics

This P14.3 output builds stand-level public proxy metrics for later ground, cable, and heli assignment. It does not classify stands and does not generate model-input tables, ForestModel XML, Matrix Builder outputs, Patchworks runtime artifacts, or scenario outputs.

## Summary

- status: `public_proxy_metrics_built`
- row_count: `25019`
- managed_current_thlb_rows: `22614`
- managed_current_thlb_area_ha: `139995.798`
- rows_with_age: `24862`
- rows_with_volume: `21541`
- rows_with_slope: `17395`
- rows_with_road_distance: `25019`
- rows_with_cw_fd_yc: `25019`
- managed_rows_with_all_core_metrics: `13864`
- heli_proxy_pass_rows: `3326`
- heli_proxy_pass_managed_area_ha: `12048.363`
- high_steepness_context_rows: `438`
- high_steepness_context_managed_area_ha: `1365.621`

## Access Distance Proxy Bins

| Bin | Count |
| --- | ---: |
| `0_499_m` | `18087` |
| `1000_plus_m` | `4032` |
| `500_999_m` | `2900` |

## Helicopter Economic Metric Status

| Status | Count |
| --- | ---: |
| `age_not_gt_80` | `9693` |
| `missing_age_volume` | `157` |
| `missing_volume` | `3321` |
| `tested_0_499_m` | `7458` |
| `tested_1000_plus_m` | `2492` |
| `tested_500_999_m` | `1898` |

## Boundary

- Slope metrics use P9D public CDED source-polygon statistics and are not WFP LiDAR slope.
- Access metrics use nearest DRA road distance and are not MP11 helicopter flight distance.
- Species and volume metrics use public VRI attributes and are not WFP ITI or LBB attributes.
- P14.4 must decide how to classify stands from these metrics and compare the result against MP11 Table 20 and Table 73 targets.

## Files

- `planning/tfl6_mp11_phase14_public_proxy_metrics.csv`
- `planning/tfl6_mp11_phase14_public_proxy_metrics.json`
- `planning/tfl6_mp11_phase14_public_proxy_metrics.md`
