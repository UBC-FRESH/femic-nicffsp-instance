# TFL 6 MP11 Managed Curve Rebuild Status

## Purpose

This P10R.4 artifact records whether MP11 managed curve generation can 
run from the P10R.3 handoff candidates. When FEMIC BTC output is 
available, it also records parsed generated-curve summaries while 
keeping every row review-gated as `not_model_input`.

## Status

- Handoff candidate rows: `25`
- Blocked or review rows outside handoff: `116`
- Curve-generation status: `generated_curve_output_inspected`
- Found executables/runners: `1`
- BTC manifest status: `ok`
- BTC manifest exit code: `0`
- BTC error rows: `0`
- Parsed curve rows: `900`
- Parsed curve feature count: `25`

## Toolchain Finding

FEMIC BTC generated real MP11 candidate outputs from the P10R.3 handoff. The parsed curves are retained as review surfaces only; they are not model inputs and have not yet been compared against Phase 5 fallback curves.

## Searched Paths

- `explicit --btc-exe / FEMIC_BATCHTIPSY_EXE`
- `C:\Program Files\TIPSY 4.7\BTC\TIPSYbtc.exe`

## Runtime Evidence

- BTC output CSV: `runtime\mp11_yield\p10r_mp11_candidate_04_output.csv`
- BTC error CSV: `runtime\mp11_yield\p10r_mp11_candidate_04_error.csv`
- BTC manifest: `runtime\mp11_yield\logs\btc_manifest-p10r_mp11_candidate.json`
- Parsed curve table: `planning/tfl6_mp11_managed_curves.csv`
- Parsed curve JSON: `planning/tfl6_mp11_managed_curves.json`

## Candidate Row Status

| feature_id | mp11_au_code | curve_lane | curve_generation_status | output_curve_rows | max_treated_volume | age_at_max_treated_volume |
| --- | --- | --- | --- | --- | --- | --- |
| 611143 | Fvh101 | future_managed | generated_curve_output_inspected | 36 | 767.3 | 270 |
| 611153 | Fvh103 | future_managed | generated_curve_output_inspected | 36 | 542.1 | 330 |
| 611163 | Fvh104 | future_managed | generated_curve_output_inspected | 36 | 1334.4 | 300 |
| 611173 | Fvh104s | future_managed | generated_curve_output_inspected | 36 | 1135.9 | 260 |
| 611183 | Fvh106 | future_managed | generated_curve_output_inspected | 36 | 1574.5 | 280 |
| 611193 | Fvh108 | future_managed | generated_curve_output_inspected | 36 | 1382.2 | 310 |
| 611203 | Fvh113 | future_managed | generated_curve_output_inspected | 36 | 750.0 | 270 |
| 611213 | Fvm101 | future_managed | generated_curve_output_inspected | 36 | 1678.0 | 330 |
| 611223 | Fvm101s | future_managed | generated_curve_output_inspected | 36 | 1414.9 | 260 |
| 611233 | Fvm103 | future_managed | generated_curve_output_inspected | 36 | 1016.8 | 290 |
| 611243 | Fvm104 | future_managed | generated_curve_output_inspected | 36 | 1645.8 | 350 |
| 611253 | Fvm105 | future_managed | generated_curve_output_inspected | 36 | 1662.7 | 290 |
| 611263 | Fvm106 | future_managed | generated_curve_output_inspected | 36 | 1623.3 | 310 |
| 611273 | Fvm106s | future_managed | generated_curve_output_inspected | 36 | 1414.9 | 260 |
| 611283 | Fvm107 | future_managed | generated_curve_output_inspected | 36 | 1791.7 | 260 |
| 611293 | Fvm109 | future_managed | generated_curve_output_inspected | 36 | 1582.7 | 310 |
| 611303 | Fvm111 | future_managed | generated_curve_output_inspected | 36 | 1711.7 | 320 |
| 611313 | Fvm114 | future_managed | generated_curve_output_inspected | 36 | 1128.3 | 260 |
| 611323 | Fvm131 | future_managed | generated_curve_output_inspected | 36 | 1077.1 | 260 |
| 611333 | Fvm133 | future_managed | generated_curve_output_inspected | 36 | 935.4 | 260 |
| 611343 | Fvm201 | future_managed | generated_curve_output_inspected | 36 | 1404.5 | 350 |
| 611353 | Fvm203 | future_managed | generated_curve_output_inspected | 36 | 861.8 | 350 |
| 611373 | Fvm207 | future_managed | generated_curve_output_inspected | 36 | 1688.1 | 350 |
| 611383 | Fvm208 | future_managed | generated_curve_output_inspected | 36 | 1688.1 | 350 |
| 611393 | Fvm211 | future_managed | generated_curve_output_inspected | 36 | 847.5 | 350 |

## Representative Curve Inspection

|   feature_id | mp11_au_code   |   max_treated_volume |   age_at_max_treated_volume |   treated_volume_age_40 |   treated_volume_age_60 |   treated_volume_age_80 |   treated_volume_age_100 |   terminal_treated_volume_age_350 |
|-------------:|:---------------|---------------------:|----------------------------:|------------------------:|------------------------:|------------------------:|-------------------------:|----------------------------------:|
|       611283 | Fvm107         |               1791.7 |                         260 |                   433.6 |                   796.5 |                  1049.2 |                   1258.5 |                            1709.6 |
|       611303 | Fvm111         |               1711.7 |                         320 |                   370.7 |                   715.3 |                   985.2 |                   1193.2 |                            1685.3 |
|       611373 | Fvm207         |               1688.1 |                         350 |                   275.4 |                   577.1 |                   843.1 |                   1044.5 |                            1688.1 |
|       611383 | Fvm208         |               1688.1 |                         350 |                   275.4 |                   577.1 |                   843.1 |                   1044.5 |                            1688.1 |
|       611213 | Fvm101         |               1678   |                         330 |                   329.3 |                   649   |                   921.5 |                   1117.2 |                            1675.7 |
|       611253 | Fvm105         |               1662.7 |                         290 |                   371.1 |                   708.9 |                   987.1 |                   1190.4 |                            1633.1 |
|       611243 | Fvm104         |               1645.8 |                         350 |                   252.7 |                   538.8 |                   792   |                    987.6 |                            1645.8 |
|       611263 | Fvm106         |               1623.3 |                         310 |                   281.6 |                   585   |                   852.7 |                   1059.8 |                            1616.3 |
|       611293 | Fvm109         |               1582.7 |                         310 |                   307.4 |                   612.3 |                   862.7 |                   1053.6 |                            1581   |
|       611183 | Fvh106         |               1574.5 |                         280 |                   280.7 |                   582.2 |                   847.3 |                   1064.1 |                            1546.7 |

## Required Next Action

Compare the parsed P10R.4 candidate curves against Phase 5 fallback curves where useful, then keep any promotion decision review-gated.

## Use Boundary

These artifacts are review surfaces. They are generated MP11 candidate curves, but they remain not_model_input until reviewed and explicitly accepted.
