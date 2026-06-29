# TFL 6 P10R MP11 Managed Curve Plot Manifest

## Purpose

This artifact indexes regenerated Phase 10R MP11 Table 57 managed-curve
review plots against the matched Phase 5 fallback managed curves. The PNG
plot library is written under ignored `plots/` space; this manifest is the
tracked review surface.

These plots are comparison evidence only. They do not promote any recovered
or regenerated value into model input contracts.

## Summary

- generated plots: `25`
- plot directory: `plots/mp11_managed_curve_comparison`
- generated UTC: `2026-06-29T01:24:30+00:00`

| comparison_class                    |   plot_count |
|:------------------------------------|-------------:|
| large_difference_review_required    |           11 |
| low_difference                      |            3 |
| moderate_difference_review_required |           11 |

## Review Index

| mp11_au_code   | phase5_au_id    | comparison_class                    |   max_volume_pct_delta |   volume_age_100_pct_delta | plot_path                                                                     |
|:---------------|:----------------|:------------------------------------|-----------------------:|---------------------------:|:------------------------------------------------------------------------------|
| Fvh101         | cwhvh1_cw_hw_m  | large_difference_review_required    |                -29.728 |                    -26.199 | plots/mp11_managed_curve_comparison/mp11-fvh101_vs_phase5-cwhvh1-cw-hw-m.png  |
| Fvh103         | cwhvh1_hw_cw_l  | large_difference_review_required    |                -71.059 |                    -74.049 | plots/mp11_managed_curve_comparison/mp11-fvh103_vs_phase5-cwhvh1-hw-cw-l.png  |
| Fvh104         | cwhvh1_hw_ss_m  | large_difference_review_required    |                 -0.448 |                     25.235 | plots/mp11_managed_curve_comparison/mp11-fvh104_vs_phase5-cwhvh1-hw-ss-m.png  |
| Fvh108         | cwhvh1_hw_cw_h  | large_difference_review_required    |                -26.208 |                    -10.241 | plots/mp11_managed_curve_comparison/mp11-fvh108_vs_phase5-cwhvh1-hw-cw-h.png  |
| Fvh113         | cwhvh1_cw_hw_m  | large_difference_review_required    |                -31.312 |                    -27.644 | plots/mp11_managed_curve_comparison/mp11-fvh113_vs_phase5-cwhvh1-cw-hw-m.png  |
| Fvm101s        | cwhvm1_cw_hw_h  | large_difference_review_required    |                 29.581 |                     51.572 | plots/mp11_managed_curve_comparison/mp11-fvm101s_vs_phase5-cwhvm1-cw-hw-h.png |
| Fvm106s        | cwhvm1_cw_hw_h  | large_difference_review_required    |                 29.581 |                     51.572 | plots/mp11_managed_curve_comparison/mp11-fvm106s_vs_phase5-cwhvm1-cw-hw-h.png |
| Fvm131         | cwhvm1_hw_dr_l  | large_difference_review_required    |                -45.535 |                    -39.368 | plots/mp11_managed_curve_comparison/mp11-fvm131_vs_phase5-cwhvm1-hw-dr-l.png  |
| Fvm201         | cwhvm1_cw_hw_h  | large_difference_review_required    |                 28.629 |                     33.82  | plots/mp11_managed_curve_comparison/mp11-fvm201_vs_phase5-cwhvm1-cw-hw-h.png  |
| Fvm203         | cwhvm1_hw_cw_l  | large_difference_review_required    |                -53.991 |                    -60.58  | plots/mp11_managed_curve_comparison/mp11-fvm203_vs_phase5-cwhvm1-hw-cw-l.png  |
| Fvm211         | cwhvm1_hw_cw_l  | large_difference_review_required    |                -54.754 |                    -60.673 | plots/mp11_managed_curve_comparison/mp11-fvm211_vs_phase5-cwhvm1-hw-cw-l.png  |
| Fvm101         | cwhvm2_ba_hw_h  | low_difference                      |                 -8.7   |                      8.203 | plots/mp11_managed_curve_comparison/mp11-fvm101_vs_phase5-cwhvm2-ba-hw-h.png  |
| Fvm207         | cwhvm2_hw_cw_h  | low_difference                      |                 -9.877 |                     -2.846 | plots/mp11_managed_curve_comparison/mp11-fvm207_vs_phase5-cwhvm2-hw-cw-h.png  |
| Fvm208         | cwhvm2_hw_cw_h  | low_difference                      |                 -9.877 |                     -2.846 | plots/mp11_managed_curve_comparison/mp11-fvm208_vs_phase5-cwhvm2-hw-cw-h.png  |
| Fvh104s        | cwhvh1_cw_hw_h  | moderate_difference_review_required |                  4.03  |                     13.798 | plots/mp11_managed_curve_comparison/mp11-fvh104s_vs_phase5-cwhvh1-cw-hw-h.png |
| Fvh106         | cwhvh1_hw_ba_h  | moderate_difference_review_required |                -20.383 |                     -3.675 | plots/mp11_managed_curve_comparison/mp11-fvh106_vs_phase5-cwhvh1-hw-ba-h.png  |
| Fvm103         | cwhvm2_yc_hw_h  | moderate_difference_review_required |                -17.561 |                     -0.159 | plots/mp11_managed_curve_comparison/mp11-fvm103_vs_phase5-cwhvm2-yc-hw-h.png  |
| Fvm104         | cwhvm2_ba_hw_m  | moderate_difference_review_required |                -10.452 |                     -4.349 | plots/mp11_managed_curve_comparison/mp11-fvm104_vs_phase5-cwhvm2-ba-hw-m.png  |
| Fvm105         | cwhvm1_hw_ss_m  | moderate_difference_review_required |                -15.923 |                      7.758 | plots/mp11_managed_curve_comparison/mp11-fvm105_vs_phase5-cwhvm1-hw-ss-m.png  |
| Fvm106         | cwhvm2_ba_hw_m  | moderate_difference_review_required |                -11.676 |                      2.644 | plots/mp11_managed_curve_comparison/mp11-fvm106_vs_phase5-cwhvm2-ba-hw-m.png  |
| Fvm107         | cwhvm1_hw_fdc_h | moderate_difference_review_required |                 -9.4   |                     13.922 | plots/mp11_managed_curve_comparison/mp11-fvm107_vs_phase5-cwhvm1-hw-fdc-h.png |
| Fvm109         | cwhvm1_hw_fdc_l | moderate_difference_review_required |                -19.969 |                     -4.626 | plots/mp11_managed_curve_comparison/mp11-fvm109_vs_phase5-cwhvm1-hw-fdc-l.png |
| Fvm111         | cwhvm1_hw_ss_m  | moderate_difference_review_required |                -13.446 |                      8.011 | plots/mp11_managed_curve_comparison/mp11-fvm111_vs_phase5-cwhvm1-hw-ss-m.png  |
| Fvm114         | cwhvm2_yc_hw_h  | moderate_difference_review_required |                 -8.521 |                     14.524 | plots/mp11_managed_curve_comparison/mp11-fvm114_vs_phase5-cwhvm2-yc-hw-h.png  |
| Fvm133         | cwhvm1_cw_hw_m  | moderate_difference_review_required |                -14.333 |                     -5.065 | plots/mp11_managed_curve_comparison/mp11-fvm133_vs_phase5-cwhvm1-cw-hw-m.png  |
