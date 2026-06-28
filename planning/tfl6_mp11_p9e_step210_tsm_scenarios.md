# TFL 6 MP11 P9E Step 210 Public TSM Scenarios

## Benchmark

- MP11 Step 210 target: `1993.000 ha`
- Source GPKG: `data/source/tfl_6/terrain/tsm_detailed_polygons_tfl6.gpkg`
- Step 200 surface: `planning/tfl6_mp11_p9rf_table12_step_200.gpkg`

## Accepted Public Proxy

- Scenario: `roads_v`
- Deduction: `1.425 ha`
- Delta: `-1991.575 ha`
- Percent delta: `-99.929%`

## Closest Numeric Diagnostic

- Scenario: `roads_p_iv_v_u`
- Deduction: `2.159 ha`
- Delta: `-1990.841 ha`
- Interpretation: retained for diagnostics only; it is broader than a strict Class V interpretation and still does not explain the MP11 Step 210 deduction.

## Scenario Table

| Scenario | Source features | Overlay area | Deduction | Delta | Percent delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| `roads_p_iv_v_u` | `41` | `36.977` | `2.159` | `-1990.841` | `-99.892%` |
| `roads_p_v_u` | `36` | `36.479` | `2.159` | `-1990.841` | `-99.892%` |
| `text_unstable_or_potentially` | `41` | `36.977` | `2.159` | `-1990.841` | `-99.892%` |
| `roads_iv_v_u` | `10` | `3.410` | `1.425` | `-1991.575` | `-99.929%` |
| `roads_v` | `5` | `2.912` | `1.425` | `-1991.575` | `-99.929%` |
| `roads_v_or_u` | `5` | `2.912` | `1.425` | `-1991.575` | `-99.929%` |
| `text_unstable` | `5` | `2.912` | `1.425` | `-1991.575` | `-99.929%` |
| `text_unstable_or_roads_v` | `5` | `2.912` | `1.425` | `-1991.575` | `-99.929%` |
| `text_unstable_or_roads_v_u` | `5` | `2.912` | `1.425` | `-1991.575` | `-99.929%` |
| `roads_p` | `31` | `33.567` | `0.734` | `-1992.266` | `-99.963%` |
| `text_potentially_unstable` | `36` | `34.065` | `0.734` | `-1992.266` | `-99.963%` |
| `roads_u` | `0` | `0.000` | `0.000` | `-1993.000` | `-100.000%` |

## Recommendation

Use `roads_v` as the strict public TSM Class V proxy for MP11 Step 210. Broader `P/IV/V/U` and text-based unstable/potentially unstable combinations are retained as diagnostics but should not be used to inflate the deduction because they are still nowhere near the MP11 benchmark and are less semantically direct.
