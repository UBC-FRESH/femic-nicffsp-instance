# TFL 6 P10R MP11 Managed Curve Plot Manifest

## Purpose

This artifact indexes regenerated Phase 10R MP11 Table 57 managed-curve
review plots against the matched Phase 5 fallback managed curves. The PNG
plot library is written under ignored `plots/` space; this manifest is the
tracked review surface.

These plots are comparison evidence only. They do not promote any recovered
or regenerated value into model input contracts.

## Summary

- generated plots: `27`
- plot directory: `plots/mp11_managed_curve_comparison`
- generated UTC: `2026-06-28T22:53:13+00:00`

| comparison_class                    |   plot_count |
|:------------------------------------|-------------:|
| large_difference_review_required    |           13 |
| low_difference                      |            3 |
| moderate_difference_review_required |           11 |

## Review Decision

- Review status: `tentatively_passed_review`
- Model-input status: `not_model_input`
- Decision timestamp UTC: `2026-06-28T23:00:09+00:00`
- Decision note: Maintainer requested tentative review pass so P10R can proceed to updated VDYP curve generation and AU-wise TIPSY-vs-VDYP diagnostics. This does not promote curves to model-input status.

## Review Index

| mp11_au_code   | phase5_au_id    | comparison_class                    |   max_volume_pct_delta |   volume_age_100_pct_delta | plot_path                                                                     |
|:---------------|:----------------|:------------------------------------|-----------------------:|---------------------------:|:------------------------------------------------------------------------------|
| FMH01          | cwhvm2_hw_ba_l  | large_difference_review_required    |                -41.577 |                    -52.841 | plots/mp11_managed_curve_comparison/mp11-fmh01_vs_phase5-cwhvm2-hw-ba-l.png   |
| FMH22          | cwhvm2_hw_ba_l  | large_difference_review_required    |                -42.599 |                    -57.942 | plots/mp11_managed_curve_comparison/mp11-fmh22_vs_phase5-cwhvm2-hw-ba-l.png   |
| Fvh101         | cwhvh1_cw_hw_m  | large_difference_review_required    |                -29.728 |                    -26.199 | plots/mp11_managed_curve_comparison/mp11-fvh101_vs_phase5-cwhvh1-cw-hw-m.png  |
| Fvh103         | cwhvh1_cw_hw_l  | large_difference_review_required    |                -79.824 |                    -88.869 | plots/mp11_managed_curve_comparison/mp11-fvh103_vs_phase5-cwhvh1-cw-hw-l.png  |
| Fvh108         | cwhvh1_hw_cw_h  | large_difference_review_required    |                -30.281 |                    -15.98  | plots/mp11_managed_curve_comparison/mp11-fvh108_vs_phase5-cwhvh1-hw-cw-h.png  |
| Fvh113         | cwhvh1_cw_hw_m  | large_difference_review_required    |                -31.312 |                    -27.644 | plots/mp11_managed_curve_comparison/mp11-fvh113_vs_phase5-cwhvh1-cw-hw-m.png  |
| Fvm101s        | cwhvm1_cw_hw_h  | large_difference_review_required    |                 30.928 |                     53.668 | plots/mp11_managed_curve_comparison/mp11-fvm101s_vs_phase5-cwhvm1-cw-hw-h.png |
| Fvm103         | cwhvm2_yc_hw_h  | large_difference_review_required    |                -25.247 |                     -4.497 | plots/mp11_managed_curve_comparison/mp11-fvm103_vs_phase5-cwhvm2-yc-hw-h.png  |
| Fvm106s        | cwhvm1_cw_hw_h  | large_difference_review_required    |                 33.913 |                     57.558 | plots/mp11_managed_curve_comparison/mp11-fvm106s_vs_phase5-cwhvm1-cw-hw-h.png |
| Fvm131         | cwhvm1_hw_dr_l  | large_difference_review_required    |                -47.183 |                    -40.364 | plots/mp11_managed_curve_comparison/mp11-fvm131_vs_phase5-cwhvm1-hw-dr-l.png  |
| Fvm201         | cwhvm1_cw_hw_h  | large_difference_review_required    |                 33.648 |                     39.171 | plots/mp11_managed_curve_comparison/mp11-fvm201_vs_phase5-cwhvm1-cw-hw-h.png  |
| Fvm203         | cwhvm2_cw_hw_m  | large_difference_review_required    |                -24.206 |                    -35.996 | plots/mp11_managed_curve_comparison/mp11-fvm203_vs_phase5-cwhvm2-cw-hw-m.png  |
| Fvm211         | cwhvm1_hw_cw_l  | large_difference_review_required    |                -55.667 |                    -61.631 | plots/mp11_managed_curve_comparison/mp11-fvm211_vs_phase5-cwhvm1-hw-cw-l.png  |
| Fvm133         | cwhvm1_cw_hw_m  | low_difference                      |                 -9.653 |                      2.525 | plots/mp11_managed_curve_comparison/mp11-fvm133_vs_phase5-cwhvm1-cw-hw-m.png  |
| Fvm207         | cwhvm1_hw_cw_m  | low_difference                      |                 -8.846 |                     -2.111 | plots/mp11_managed_curve_comparison/mp11-fvm207_vs_phase5-cwhvm1-hw-cw-m.png  |
| Fvm208         | cwhvm1_hw_cw_m  | low_difference                      |                 -8.846 |                     -2.111 | plots/mp11_managed_curve_comparison/mp11-fvm208_vs_phase5-cwhvm1-hw-cw-m.png  |
| Fvh104         | cwhvh1_hw_ss_m  | moderate_difference_review_required |                 -4.648 |                     18.18  | plots/mp11_managed_curve_comparison/mp11-fvh104_vs_phase5-cwhvh1-hw-ss-m.png  |
| Fvh104s        | cwhvh1_cw_hw_h  | moderate_difference_review_required |                  7.977 |                     19.784 | plots/mp11_managed_curve_comparison/mp11-fvh104s_vs_phase5-cwhvh1-cw-hw-h.png |
| Fvh106         | cwhvh1_hw_ba_h  | moderate_difference_review_required |                -24.327 |                     -8.002 | plots/mp11_managed_curve_comparison/mp11-fvh106_vs_phase5-cwhvh1-hw-ba-h.png  |
| Fvm101         | cwhvm2_ba_hw_h  | moderate_difference_review_required |                -16.116 |                      3.429 | plots/mp11_managed_curve_comparison/mp11-fvm101_vs_phase5-cwhvm2-ba-hw-h.png  |
| Fvm104         | cwhvm1_ss_hw_l  | moderate_difference_review_required |                 -2.747 |                    -21.644 | plots/mp11_managed_curve_comparison/mp11-fvm104_vs_phase5-cwhvm1-ss-hw-l.png  |
| Fvm105         | cwhvm1_hw_ss_m  | moderate_difference_review_required |                -24.408 |                      3.286 | plots/mp11_managed_curve_comparison/mp11-fvm105_vs_phase5-cwhvm1-hw-ss-m.png  |
| Fvm106         | cwhvm1_hw_ss_l  | moderate_difference_review_required |                -22.644 |                    -11.849 | plots/mp11_managed_curve_comparison/mp11-fvm106_vs_phase5-cwhvm1-hw-ss-l.png  |
| Fvm107         | cwhvm1_hw_cw_h  | moderate_difference_review_required |                -12.156 |                     11.487 | plots/mp11_managed_curve_comparison/mp11-fvm107_vs_phase5-cwhvm1-hw-cw-h.png  |
| Fvm109         | cwhvm1_hw_fdc_l | moderate_difference_review_required |                -21.106 |                     -5.323 | plots/mp11_managed_curve_comparison/mp11-fvm109_vs_phase5-cwhvm1-hw-fdc-l.png |
| Fvm111         | cwhvm1_hw_ss_m  | moderate_difference_review_required |                -16.136 |                      8.663 | plots/mp11_managed_curve_comparison/mp11-fvm111_vs_phase5-cwhvm1-hw-ss-m.png  |
| Fvm114         | cwhvm2_yc_hw_h  | moderate_difference_review_required |                -11.189 |                     12.538 | plots/mp11_managed_curve_comparison/mp11-fvm114_vs_phase5-cwhvm2-yc-hw-h.png  |

## Maintainer Plot Review

- Passed TIPSY-vs-VDYP sanity rows: `24`
- Failed TIPSY-vs-VDYP sanity rows: `3`
- Failed AU codes: `FMH01`, `FMH22`, `Fvh103`
- Failed review status: `failed_tipsy_below_vdyp_sanity_review`
- Passed review status: `passed_tipsy_vdyp_sanity_review`
- Model-input status: `not_model_input`
- Review timestamp UTC: `2026-06-28T23:13:35+00:00`
- Failed-row rationale: Maintainer plot review rejected this generated TIPSY curve because plantation yield should meet or beat the matched natural VDYP curve; observed TIPSY is substantially below VDYP.
