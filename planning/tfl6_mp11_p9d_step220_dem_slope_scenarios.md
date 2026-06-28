# TFL 6 MP11 P9D Step 220 Public DEM Slope Scenarios

## Purpose

Compare public CDED steep-slope rules against MP11 Table 12 Step 220 before deciding whether a public DEM proxy can replace the current zero-deduction placeholder.

## Benchmark

- MP11 Step 220 target deduction: `1820.000 ha`
- Step 210 source area: `129208.678 ha`

## Best Whole-Fragment Candidate

- Scenario: `slope_ge_70_prop_ge_0.75_whole_fragment`
- Deduction: `1801.705 ha`
- Delta to MP11 Step 220: `-18.295 ha`
- Percent delta: `-1.005%`

## Best Partial-Area Diagnostic

- Scenario: `slope_ge_90_prop_ge_0.25_partial_area_diagnostic`
- Deduction: `2445.433 ha`
- Delta to MP11 Step 220: `625.433 ha`

## Top Whole-Fragment Scenarios

| Scenario | Deduction | Delta | Percent delta | Fragments |
| --- | ---: | ---: | ---: | ---: |
| `slope_ge_70_prop_ge_0.75_whole_fragment` | `1801.705` | `-18.295` | `-1.005%` | `931` |
| `slope_ge_60_prop_ge_0.9_whole_fragment` | `1909.484` | `89.484` | `4.917%` | `1340` |
| `slope_ge_80_prop_ge_0.5_whole_fragment` | `1915.000` | `95.000` | `5.220%` | `811` |
| `slope_ge_90_prop_ge_0.25_whole_fragment` | `2608.887` | `788.887` | `43.345%` | `801` |
| `slope_ge_90_prop_ge_0.5_whole_fragment` | `631.379` | `-1188.621` | `-65.309%` | `342` |
| `slope_ge_70_prop_ge_0.9_whole_fragment` | `486.185` | `-1333.815` | `-73.287%` | `604` |
| `slope_ge_80_prop_ge_0.75_whole_fragment` | `410.320` | `-1409.680` | `-77.455%` | `375` |
| `slope_ge_60_prop_ge_1_whole_fragment` | `335.251` | `-1484.749` | `-81.580%` | `960` |

## Interpretation

Prefer whole-fragment scenarios for the resultant-fragment netdown. The partial-area rows are diagnostics only because the production P9RF lane physically removes resultant fragments.

CDED-derived thresholds are public-data proxies. A lower CDED slope threshold may be defensible because coarse DEM smoothing suppresses local LiDAR-grade slopes, but this must be recorded as a proxy rule, not as WFP LiDAR equivalence.

Final Current THLB and Long-term Land Base deltas must come from rerunning the P9RF resultant-fragment netdown with the selected Step 220 rule physically applied.
