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

- diagnostic rows: `25`
- plotted diagnostic rows: `25`
- blocked no-same-BEC rows: `0`
- VDYP curve-slice rows: `7475`
- unique MP11 TIPSY candidates: `25`
- unique VDYP natural AUs: `17`
- plot directory: `plots/mp11_tipsy_vdyp_diagnostics`
- review status: `p10r5_tipsy_vdyp_diagnostic_review_required`
- model-input status: `not_model_input`

| diagnostic_class               |   row_count |
|:-------------------------------|------------:|
| tipsy_substantially_above_vdyp |          17 |
| tipsy_substantially_below_vdyp |           1 |
| tipsy_vdyp_close               |           2 |
| tipsy_vdyp_moderate_difference |           5 |

## Review Index

| mp11_au_code   | vdyp_au_id     | diagnostic_class               |   tipsy_to_vdyp_max_ratio |   tipsy_to_vdyp_age_100_ratio |   common_age_rmse | plot_path                                                                       |
|:---------------|:---------------|:-------------------------------|--------------------------:|------------------------------:|------------------:|:--------------------------------------------------------------------------------|
| Fvh101         | cwhvh1_cw_hw_m | tipsy_vdyp_moderate_difference |                     1.168 |                         0.967 |           101.369 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh101_tipsy-vs-vdyp-cwhvh1-cw-hw-m.png  |
| Fvh103         | cwhvh1_cw_hw_l | tipsy_substantially_below_vdyp |                     0.882 |                         0.598 |           129.265 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh103_tipsy-vs-vdyp-cwhvh1-cw-hw-l.png  |
| Fvh104         | cwhvh1_hw_ss_m | tipsy_substantially_above_vdyp |                     1.364 |                         1.132 |           290.685 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh104_tipsy-vs-vdyp-cwhvh1-hw-ss-m.png  |
| Fvh104s        | cwhvh1_cw_hw_h | tipsy_substantially_above_vdyp |                     1.421 |                         1.13  |           250.931 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh104s_tipsy-vs-vdyp-cwhvh1-cw-hw-h.png |
| Fvh106         | cwhvh1_hw_ba_h | tipsy_substantially_above_vdyp |                     1.491 |                         1.279 |           450.307 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh106_tipsy-vs-vdyp-cwhvh1-hw-ba-h.png  |
| Fvh108         | cwhvh1_hw_cw_h | tipsy_vdyp_moderate_difference |                     1.328 |                         1.166 |           312.601 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh108_tipsy-vs-vdyp-cwhvh1-hw-cw-h.png  |
| Fvh113         | cwhvh1_cw_hw_m | tipsy_vdyp_close               |                     1.142 |                         0.948 |            91.89  | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvh113_tipsy-vs-vdyp-cwhvh1-cw-hw-m.png  |
| Fvm101         | cwhvm1_hw_cw_m | tipsy_substantially_above_vdyp |                     1.599 |                         1.373 |           454.92  | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm101_tipsy-vs-vdyp-cwhvm1-hw-cw-m.png  |
| Fvm101s        | cwhvm1_cw_hw_h | tipsy_substantially_above_vdyp |                     1.498 |                         1.284 |           355.398 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm101s_tipsy-vs-vdyp-cwhvm1-cw-hw-h.png |
| Fvm103         | cwhvm2_yc_hw_h | tipsy_vdyp_moderate_difference |                     1.247 |                         0.962 |           167.488 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm103_tipsy-vs-vdyp-cwhvm2-yc-hw-h.png  |
| Fvm104         | cwhvm1_ba_hw_m | tipsy_substantially_above_vdyp |                     1.558 |                         1.161 |           394.973 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm104_tipsy-vs-vdyp-cwhvm1-ba-hw-m.png  |
| Fvm105         | cwhvm1_hw_ss_m | tipsy_substantially_above_vdyp |                     1.421 |                         1.287 |           399.03  | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm105_tipsy-vs-vdyp-cwhvm1-hw-ss-m.png  |
| Fvm106         | cwhvm1_ba_hw_m | tipsy_substantially_above_vdyp |                     1.537 |                         1.246 |           428.471 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm106_tipsy-vs-vdyp-cwhvm1-ba-hw-m.png  |
| Fvm106s        | cwhvm1_cw_hw_h | tipsy_substantially_above_vdyp |                     1.498 |                         1.284 |           355.398 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm106s_tipsy-vs-vdyp-cwhvm1-cw-hw-h.png |
| Fvm107         | cwhvm1_hw_dr_h | tipsy_substantially_above_vdyp |                     1.998 |                         1.67  |           688.984 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm107_tipsy-vs-vdyp-cwhvm1-hw-dr-h.png  |
| Fvm109         | cwhvm1_hw_ss_l | tipsy_substantially_above_vdyp |                     1.518 |                         1.304 |           406.306 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm109_tipsy-vs-vdyp-cwhvm1-hw-ss-l.png  |
| Fvm111         | cwhvm1_hw_ss_m | tipsy_substantially_above_vdyp |                     1.462 |                         1.29  |           422.058 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm111_tipsy-vs-vdyp-cwhvm1-hw-ss-m.png  |
| Fvm114         | cwhvm2_yc_hw_h | tipsy_substantially_above_vdyp |                     1.383 |                         1.104 |           254.628 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm114_tipsy-vs-vdyp-cwhvm2-yc-hw-h.png  |
| Fvm131         | cwhvm1_hw_dr_l | tipsy_substantially_above_vdyp |                     1.475 |                         1.122 |           289.823 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm131_tipsy-vs-vdyp-cwhvm1-hw-dr-l.png  |
| Fvm133         | cwhvm1_cw_hw_m | tipsy_vdyp_close               |                     1.111 |                         0.913 |           104.963 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm133_tipsy-vs-vdyp-cwhvm1-cw-hw-m.png  |
| Fvm201         | cwhvm1_cw_hw_h | tipsy_substantially_above_vdyp |                     1.487 |                         1.134 |           293.76  | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm201_tipsy-vs-vdyp-cwhvm1-cw-hw-h.png  |
| Fvm203         | cwhvm1_hw_cw_l | tipsy_vdyp_moderate_difference |                     1.033 |                         0.667 |           143.692 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm203_tipsy-vs-vdyp-cwhvm1-hw-cw-l.png  |
| Fvm207         | cwhvm2_hw_cw_h | tipsy_substantially_above_vdyp |                     1.71  |                         1.37  |           473.49  | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm207_tipsy-vs-vdyp-cwhvm2-hw-cw-h.png  |
| Fvm208         | cwhvm2_hw_cw_h | tipsy_substantially_above_vdyp |                     1.71  |                         1.37  |           473.49  | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm208_tipsy-vs-vdyp-cwhvm2-hw-cw-h.png  |
| Fvm211         | cwhvm1_hw_cw_l | tipsy_vdyp_moderate_difference |                     1.016 |                         0.665 |           143.383 | plots/mp11_tipsy_vdyp_diagnostics/mp11-fvm211_tipsy-vs-vdyp-cwhvm1-hw-cw-l.png  |

## Use Boundary

- TIPSY-vs-VDYP differences are diagnostic evidence for review, not
  automatic rejection or acceptance.
- The MP11 TIPSY curves remain only tentatively passed for sequencing.
- Phase 11 must explicitly promote curve surfaces before model-input or
  ForestModel XML work consumes them.
