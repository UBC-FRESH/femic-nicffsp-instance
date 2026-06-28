# TFL 6 MP11 Managed Curve Rebuild Status

## Purpose

This P10R.4 artifact records whether MP11 managed curve generation can 
run from the P10R.3 handoff candidates. When FEMIC BTC output is 
available, it also records parsed generated-curve summaries while 
keeping every row review-gated as `not_model_input`.

## Status

- Handoff candidate rows: `27`
- Blocked or review rows outside handoff: `114`
- Curve-generation status: `generated_curve_output_inspected`
- Found executables/runners: `1`
- BTC manifest status: `ok`
- BTC manifest exit code: `0`
- BTC error rows: `0`
- Parsed curve rows: `972`
- Parsed curve feature count: `27`
- Review status: `passed_tipsy_vdyp_sanity_review` for `24` candidate curves; `failed_tipsy_below_vdyp_sanity_review` for `3` candidate curves (`FMH01`, `FMH22`, `Fvh103`).
- Model-input status: `not_model_input`

## Toolchain Finding

FEMIC BTC generated real MP11 candidate outputs from the P10R.3 handoff. The parsed curves are retained as review surfaces only. They have been tentatively passed for P10R sequencing after Phase 5 fallback comparison and plot review, but they remain `not_model_input`.

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
| 611153 | Fvh103 | future_managed | generated_curve_output_inspected | 36 | 220.3 | 350 |
| 611163 | Fvh104 | future_managed | generated_curve_output_inspected | 36 | 1278.1 | 320 |
| 611173 | Fvh104s | future_managed | generated_curve_output_inspected | 36 | 1179.0 | 260 |
| 611183 | Fvh106 | future_managed | generated_curve_output_inspected | 36 | 1496.5 | 260 |
| 611193 | Fvh108 | future_managed | generated_curve_output_inspected | 36 | 1305.9 | 310 |
| 611203 | Fvh113 | future_managed | generated_curve_output_inspected | 36 | 750.0 | 270 |
| 611213 | Fvm101 | future_managed | generated_curve_output_inspected | 36 | 1541.7 | 320 |
| 611223 | Fvm101s | future_managed | generated_curve_output_inspected | 36 | 1429.6 | 260 |
| 611233 | Fvm103 | future_managed | generated_curve_output_inspected | 36 | 922.0 | 270 |
| 611243 | Fvm104 | future_managed | generated_curve_output_inspected | 36 | 1621.4 | 350 |
| 611253 | Fvm105 | future_managed | generated_curve_output_inspected | 36 | 1494.9 | 250 |
| 611263 | Fvm106 | future_managed | generated_curve_output_inspected | 36 | 1529.8 | 310 |
| 611273 | Fvm106s | future_managed | generated_curve_output_inspected | 36 | 1462.2 | 260 |
| 611283 | Fvm107 | future_managed | generated_curve_output_inspected | 36 | 1645.4 | 230 |
| 611293 | Fvm109 | future_managed | generated_curve_output_inspected | 36 | 1560.2 | 330 |
| 611303 | Fvm111 | future_managed | generated_curve_output_inspected | 36 | 1658.5 | 280 |
| 611313 | Fvm114 | future_managed | generated_curve_output_inspected | 36 | 1095.4 | 260 |
| 611323 | Fvm131 | future_managed | generated_curve_output_inspected | 36 | 1044.5 | 260 |
| 611333 | Fvm133 | future_managed | generated_curve_output_inspected | 36 | 986.5 | 250 |
| 611343 | Fvm201 | future_managed | generated_curve_output_inspected | 36 | 1459.3 | 350 |
| 611353 | Fvm203 | future_managed | generated_curve_output_inspected | 36 | 827.6 | 350 |
| 611373 | Fvm207 | future_managed | generated_curve_output_inspected | 36 | 1707.4 | 330 |
| 611383 | Fvm208 | future_managed | generated_curve_output_inspected | 36 | 1707.4 | 330 |
| 611393 | Fvm211 | future_managed | generated_curve_output_inspected | 36 | 830.4 | 350 |
| 611403 | FMH01 | future_managed | generated_curve_output_inspected | 36 | 783.1 | 350 |
| 611413 | FMH22 | future_managed | generated_curve_output_inspected | 36 | 769.4 | 350 |

## Representative Curve Inspection

|   feature_id | mp11_au_code   |   max_treated_volume |   age_at_max_treated_volume |   treated_volume_age_40 |   treated_volume_age_60 |   treated_volume_age_80 |   treated_volume_age_100 |   terminal_treated_volume_age_350 |
|-------------:|:---------------|---------------------:|----------------------------:|------------------------:|------------------------:|------------------------:|-------------------------:|----------------------------------:|
|       611383 | Fvm208         |               1707.4 |                         330 |                   285.3 |                   589.3 |                   851.1 |                   1052.4 |                            1702.9 |
|       611373 | Fvm207         |               1707.4 |                         330 |                   285.3 |                   589.3 |                   851.1 |                   1052.4 |                            1702.9 |
|       611303 | Fvm111         |               1658.5 |                         280 |                   383.6 |                   733.3 |                   995.2 |                   1200.4 |                            1591.6 |
|       611283 | Fvm107         |               1645.4 |                         230 |                   413.7 |                   756.3 |                  1001.8 |                   1198.6 |                            1541.6 |
|       611243 | Fvm104         |               1621.4 |                         350 |                   241.1 |                   521.1 |                   769   |                    959   |                            1621.4 |
|       611293 | Fvm109         |               1560.2 |                         330 |                   308.6 |                   611.3 |                   854.8 |                   1045.9 |                            1559.3 |
|       611213 | Fvm101         |               1541.7 |                         320 |                   324.6 |                   631.4 |                   881.1 |                   1067.9 |                            1537.8 |
|       611263 | Fvm106         |               1529.8 |                         310 |                   247.1 |                   527   |                   767.8 |                    973.8 |                            1520.4 |
|       611183 | Fvh106         |               1496.5 |                         260 |                   262.9 |                   551.5 |                   801.4 |                   1016.3 |                            1468.8 |
|       611253 | Fvm105         |               1494.9 |                         250 |                   375.3 |                   699.7 |                   952.1 |                   1141   |                            1459.7 |

## Required Next Action

Compare the parsed P10R.4 candidate curves against Phase 5 fallback curves where useful, then keep any promotion decision review-gated.

## Use Boundary

These artifacts are review surfaces. They are generated MP11 candidate curves, but they remain not_model_input until reviewed and explicitly accepted.
