# TFL 6 P10R MP11 TIPSY-vs-VDYP Diagnostic Manifest

## Purpose

This artifact builds AU-wise diagnostic overlays between the tentatively
passed MP11 Table 57 TIPSY managed curves and the matching public VDYP
natural curves from the existing FEMIC `smoothed_bin_pchip` first-growth
curve table.

The VDYP curves are a P10R review slice from the accepted public VDYP
curve surface, not a model-input promotion. Every row remains
`not_model_input`.

## Summary

- diagnostic rows: `27`
- VDYP curve-slice rows: `8073`
- unique MP11 TIPSY candidates: `27`
- unique VDYP natural AUs: `20`
- plot directory: `plots/mp11_tipsy_vdyp_diagnostics`
- review status: `p10r5_tipsy_vdyp_diagnostic_review_required`
- model-input status: `not_model_input`

| diagnostic_class               |   row_count |
|:-------------------------------|------------:|
| tipsy_substantially_above_vdyp |          13 |
| tipsy_substantially_below_vdyp |           4 |
| tipsy_vdyp_close               |           2 |
| tipsy_vdyp_moderate_difference |           8 |

## Review Index

| mp11_au_code   | vdyp_au_id      | diagnostic_class               |   tipsy_to_vdyp_max_ratio |   tipsy_to_vdyp_age_100_ratio |   common_age_rmse | plot_path                                                                       |
|:---------------|:----------------|:-------------------------------|--------------------------:|------------------------------:|------------------:|:--------------------------------------------------------------------------------|
| FMH01          | cwhvm2_hw_ba_l  | tipsy_substantially_below_vdyp |                     0.851 |                         0.418 |           294.635 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fmh01_tipsy-vs-vdyp-cwhvm2-hw-ba-l.png   |
| FMH22          | cwhvm2_hw_ba_l  | tipsy_substantially_below_vdyp |                     0.836 |                         0.372 |           317.305 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fmh22_tipsy-vs-vdyp-cwhvm2-hw-ba-l.png   |
| Fvh101         | cwhvh1_cw_hw_m  | tipsy_vdyp_moderate_difference |                     1.168 |                         0.967 |           101.369 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh101_tipsy-vs-vdyp-cwhvh1-cw-hw-m.png  |
| Fvh103         | cwhvh1_cw_hw_l  | tipsy_substantially_below_vdyp |                     0.359 |                         0.152 |           336.857 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh103_tipsy-vs-vdyp-cwhvh1-cw-hw-l.png  |
| Fvh104         | cwhvh1_hw_ss_m  | tipsy_vdyp_moderate_difference |                     1.306 |                         1.068 |           250.429 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh104_tipsy-vs-vdyp-cwhvh1-hw-ss-m.png  |
| Fvh104s        | cwhvh1_cw_hw_h  | tipsy_substantially_above_vdyp |                     1.478 |                         1.219 |           287.486 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh104s_tipsy-vs-vdyp-cwhvh1-cw-hw-h.png |
| Fvh106         | cwhvh1_hw_ba_h  | tipsy_substantially_above_vdyp |                     1.4   |                         1.193 |           387.909 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh106_tipsy-vs-vdyp-cwhvh1-hw-ba-h.png  |
| Fvh108         | cwhvh1_hw_cw_h  | tipsy_vdyp_moderate_difference |                     1.255 |                         1.091 |           252.236 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh108_tipsy-vs-vdyp-cwhvh1-hw-cw-h.png  |
| Fvh113         | cwhvh1_cw_hw_m  | tipsy_vdyp_close               |                     1.142 |                         0.948 |            91.89  | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh113_tipsy-vs-vdyp-cwhvh1-cw-hw-m.png  |
| Fvm101         | cwhvm2_ba_hw_h  | tipsy_vdyp_moderate_difference |                     1.287 |                         1.094 |           233.398 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm101_tipsy-vs-vdyp-cwhvm2-ba-hw-h.png  |
| Fvm101s        | cwhvm1_cw_hw_h  | tipsy_substantially_above_vdyp |                     1.515 |                         1.309 |           367.948 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm101s_tipsy-vs-vdyp-cwhvm1-cw-hw-h.png |
| Fvm103         | cwhvm2_yc_hw_h  | tipsy_vdyp_close               |                     1.107 |                         0.907 |            88.501 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm103_tipsy-vs-vdyp-cwhvm2-yc-hw-h.png  |
| Fvm104         | cwhvm1_ss_hw_l  | tipsy_substantially_above_vdyp |                     1.475 |                         1.092 |           323.892 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm104_tipsy-vs-vdyp-cwhvm1-ss-hw-l.png  |
| Fvm105         | cwhvm1_hw_ss_m  | tipsy_vdyp_moderate_difference |                     1.253 |                         1.196 |           253.463 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm105_tipsy-vs-vdyp-cwhvm1-hw-ss-m.png  |
| Fvm106         | cwhvm1_hw_ss_l  | tipsy_substantially_above_vdyp |                     1.447 |                         1.185 |           335.933 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm106_tipsy-vs-vdyp-cwhvm1-hw-ss-l.png  |
| Fvm106s        | cwhvm1_cw_hw_h  | tipsy_substantially_above_vdyp |                     1.549 |                         1.342 |           395.184 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm106s_tipsy-vs-vdyp-cwhvm1-cw-hw-h.png |
| Fvm107         | cwhvm1_hw_cw_h  | tipsy_substantially_above_vdyp |                     1.381 |                         1.262 |           353.175 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm107_tipsy-vs-vdyp-cwhvm1-hw-cw-h.png  |
| Fvm109         | cwhvm1_hw_fdc_l | tipsy_substantially_above_vdyp |                     1.353 |                         1.16  |           288.659 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm109_tipsy-vs-vdyp-cwhvm1-hw-fdc-l.png |
| Fvm111         | cwhvm1_hw_ss_m  | tipsy_substantially_above_vdyp |                     1.39  |                         1.258 |           349.988 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm111_tipsy-vs-vdyp-cwhvm1-hw-ss-m.png  |
| Fvm114         | cwhvm2_yc_hw_h  | tipsy_vdyp_moderate_difference |                     1.315 |                         1.068 |           201.979 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm114_tipsy-vs-vdyp-cwhvm2-yc-hw-h.png  |
| Fvm131         | cwhvm1_hw_dr_l  | tipsy_substantially_above_vdyp |                     1.411 |                         1.077 |           265.282 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm131_tipsy-vs-vdyp-cwhvm1-hw-dr-l.png  |
| Fvm133         | cwhvm1_cw_hw_m  | tipsy_vdyp_moderate_difference |                     1.188 |                         0.996 |           136.572 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm133_tipsy-vs-vdyp-cwhvm1-cw-hw-m.png  |
| Fvm201         | cwhvm1_cw_hw_h  | tipsy_substantially_above_vdyp |                     1.546 |                         1.185 |           323.779 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm201_tipsy-vs-vdyp-cwhvm1-cw-hw-h.png  |
| Fvm203         | cwhvm2_cw_hw_m  | tipsy_vdyp_moderate_difference |                     1.188 |                         0.812 |           136.396 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm203_tipsy-vs-vdyp-cwhvm2-cw-hw-m.png  |
| Fvm207         | cwhvm1_hw_cw_m  | tipsy_substantially_above_vdyp |                     1.627 |                         1.293 |           434.432 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm207_tipsy-vs-vdyp-cwhvm1-hw-cw-m.png  |
| Fvm208         | cwhvm1_hw_cw_m  | tipsy_substantially_above_vdyp |                     1.627 |                         1.293 |           434.432 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm208_tipsy-vs-vdyp-cwhvm1-hw-cw-m.png  |
| Fvm211         | cwhvm1_hw_cw_l  | tipsy_substantially_below_vdyp |                     0.996 |                         0.649 |           148.808 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm211_tipsy-vs-vdyp-cwhvm1-hw-cw-l.png  |

## Maintainer Plot Review

- Passed TIPSY-vs-VDYP sanity rows: `24`
- Failed TIPSY-vs-VDYP sanity rows: `3`
- Failed AU codes: `FMH01`, `FMH22`, `Fvh103`
- Failed review status: `failed_tipsy_below_vdyp_sanity_review`
- Passed review status: `passed_tipsy_vdyp_sanity_review`
- Model-input status: `not_model_input`
- Review timestamp UTC: `2026-06-28T23:13:35+00:00`
- Failed-row rationale: Maintainer plot review rejected this generated TIPSY curve because plantation yield should meet or beat the matched natural VDYP curve; observed TIPSY is substantially below VDYP.

## Use Boundary

- TIPSY-vs-VDYP differences are diagnostic evidence for review, not
  automatic rejection or acceptance.
- The MP11 TIPSY curves remain only tentatively passed for sequencing.
- Phase 11 must explicitly promote curve surfaces before model-input or
  ForestModel XML work consumes them.
