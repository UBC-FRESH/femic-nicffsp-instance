# TFL 6 MP11 Phase 14 Harvest-System Classification

This P14.4 output classifies the MP11 candidate stands into public-proxy harvest-system lanes and compares aggregate area/volume against MP11 Table 20/Table 73 targets. It does not generate model-input tables, ForestModel XML, Matrix Builder outputs, Patchworks runtime artifacts, or scenario outputs.

## Summary

- status: `harvest_system_proxy_classification_built`
- row_count: `25019`
- managed_current_thlb_rows: `22614`
- managed_current_thlb_area_ha: `139995.798`
- managed_current_thlb_volume_m3: `45043117.375`

## Managed Current THLB By Candidate System

| System | Rows | Area ha | Volume m3 |
| --- | ---: | ---: | ---: |
| `cable` | `9055` | `56677.061` | `20342940.218` |
| `ground` | `12905` | `80241.389` | `22778489.535` |
| `heli` | `654` | `3077.349` | `1921687.622` |

## MP11 Table 73 QA

| System | Candidate area ha | MP11 area ha | Area share residual pp | Candidate volume m3 | MP11 volume m3 | Volume share residual pp |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ground` | `80241.389` | `68845.000` | `0.017` | `22778489.535` | `19216294.000` | `-2.830` |
| `cable` | `56677.061` | `47524.000` | `0.885` | `20342940.218` | `14563331.000` | `4.663` |
| `heli` | `3077.349` | `3730.000` | `-0.902` | `1921687.622` | `2223221.000` | `-1.934` |

## Classification Rules

- not_applicable for stands outside managed current THLB
- heli when MP11 Tables 27-29 economic proxy passes and the stand has nearest-DRA-road distance >= 1000 m or P9D slope p90 >= 80%
- cable when public CDED mean slope >= 30%
- cable low-confidence fallback when slope is missing and DRA distance > 1500 m
- ground when public CDED mean slope < 30%
- ground low-confidence fallback when slope is missing and DRA distance <= 1500 m

## Boundary

- WFP LBB geometry is unavailable; these are public proxy assignments.
- CDED slope is not WFP LiDAR slope.
- DRA road distance is not MP11 helicopter flight distance.
- Public VRI volume is not WFP ITI volume.
- P14.5 may use these classifications as candidate inputs only after reviewing the QA residuals and caveats.

## Files

- `planning/tfl6_mp11_phase14_harvest_system_classification.csv`
- `planning/tfl6_mp11_phase14_harvest_system_classification_qa.csv`
- `planning/tfl6_mp11_phase14_harvest_system_classification.json`
- `planning/tfl6_mp11_phase14_harvest_system_classification.md`
