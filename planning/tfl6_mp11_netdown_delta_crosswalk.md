# TFL 6 MP11 Netdown And Source-Layer Delta Crosswalk

## Purpose

This P6.3 note records the MP11 land-base/netdown categories that differ
from the MP10-derived Phase 5 prototype basis and classifies whether each
delta is likely reproducible from public layers, requires a proxy, or is
better treated as a model-parameter/constraint rebuild.

## Files

- `planning/tfl6_mp11_netdown_delta_crosswalk.md`
- `planning/tfl6_mp11_netdown_delta_crosswalk.csv`
- `planning/tfl6_mp11_netdown_delta_crosswalk.json`

## Status

- Rows: `9`
- Reproducibility classes: `{'mixed_public_proxy_or_confidential': 1, 'model_constraint_rebuild': 1, 'model_parameter_rebuild': 1, 'partially_public_spatial_layer_rebuild': 1, 'partly_aspatial_policy_parameter': 1, 'public_dem_proxy_plus_lidar_gap': 1, 'public_dem_proxy_plus_wfp_operability_gap': 1, 'public_hydrography_lidar_proxy': 1, 'public_inventory_and_lidar_proxy': 1}`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_land_base_comparison_only`
- Model-input status: `not_model_input`

## Delta Table

| Category | PDF pages | Source | Old THLB net ha | MP11 THLB net ha | Delta ha | Reproducibility | Follow-up |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| Legal/proposed OGMAs and WHAs | 76 | Appendix A Table 6 |  |  |  | `partially_public_spatial_layer_rebuild` | `P6.3/P6.4` |
| Additional land-base values: research, PSPs, big trees, karst | 76-77 | Appendix A Table 7 | 0 | 3,910 | 3,910 | `mixed_public_proxy_or_confidential` | `P6.3/P6.4` |
| Non-productive and low sites | 77-78 | Appendix A Table 8 | 14,703 | 18,735 | 4,032 | `public_inventory_and_lidar_proxy` | `P6.3/P6.4` |
| Inoperable | 77-78 | Appendix A Table 8 | 12,810 | 21,193 | 8,383 | `public_dem_proxy_plus_wfp_operability_gap` | `P6.4` |
| Riparian management | 77-78 | Appendix A Table 8 | 13,956 | 5,479 | -8,477 | `public_hydrography_lidar_proxy` | `P6.3/P6.4` |
| Terrain stability and LiDAR 90%+ slope | 77-78 | Appendix A Table 8 | 1,304 | 3,812 | 2,508 | `public_dem_proxy_plus_lidar_gap` | `P6.4` |
| Existing and future WTRAs | 79-80 | Appendix A Table 9 | 6,887 | 7,577 | 690 | `partly_aspatial_policy_parameter` | `P6.3/P6.4` |
| 95% CMAI minimum harvest age plus 350 m3/ha minimum volume | 80 | Appendix A section 2.2.3 item 3 |  |  |  | `model_parameter_rebuild` | `P6.4/P6.5` |
| VQO, ECA, adjacency/green-up, and Patchworks spatial modelling | 78-82 | Appendix A sections 2.2.2-2.2.3 and 2.3 |  |  |  | `model_constraint_rebuild` | `P6.5/P6.6` |

## Interpretation

- MP11's lower THLB is not explained by one category. It reflects a mix of
  expanded conservation, new additional values, LiDAR-supported
  productivity/operability/riparian/terrain interpretation, revised WTRA
  treatment, and model constraints that do not directly reduce THLB.
- Public-layer rebuilds are plausible for several categories, but some
  MP11 assumptions rely on WFP-specific LiDAR/ITI, land-base blocking,
  proposed conservation, research/PSP locations, or model policy choices.
- Future implementation should split reproducible source-layer changes from
  proxy/sensitivity lanes and model-constraint lanes.

## Use Boundary

These rows are reviewed comparison evidence only. They are not model input
and do not authorize rerunning THLB or changing the Phase 5 teaching
runtime package.
