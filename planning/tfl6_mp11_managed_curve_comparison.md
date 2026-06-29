# TFL 6 MP11 Managed Curve Phase 5 Comparison

## Purpose

This P10R.4e artifact compares the generated MP11 Table 57 future-managed
candidate curves against the nearest available Phase 5 future-managed
fallback curves. It is a review surface only and does not promote any
curve to model input.

## Status

- MP11 candidate rows compared: `25`
- Phase 5 comparison matches: `25`
- Model-input status: `not_model_input`

## Method

Nearest Phase 5 future-managed comparison row selected only from the same BEC zone/subzone. Rows without a same-BEC/subzone comparison are blocked rather than falling back across BEC boundaries.

## Comparison Classes

- `large_difference_review_required`: `11`
- `low_difference`: `3`
- `moderate_difference_review_required`: `11`

## Largest Absolute Max-Volume Differences

| mp11_au_code   | mp11_species_combo   | phase5_au_id    | phase5_species_combo   |   species_overlap_ratio |   mean_si_abs_diff |   mp11_max_volume |   phase5_max_volume |   max_volume_pct_delta | comparison_class                    |
|:---------------|:---------------------|:----------------|:-----------------------|------------------------:|-------------------:|------------------:|--------------------:|-----------------------:|:------------------------------------|
| Fvh103         | CW+YC+HW+BA+PL       | cwhvh1_hw_cw_l  | HW+CW                  |                   0.4   |              0.368 |             542.1 |              1873.1 |                -71.059 | large_difference_review_required    |
| Fvm211         | HW+CW+YC+BA          | cwhvm1_hw_cw_l  | HW+CW                  |                   0.5   |              0.006 |             847.5 |              1873.1 |                -54.754 | large_difference_review_required    |
| Fvm203         | HW+CW+BA+YC          | cwhvm1_hw_cw_l  | HW+CW                  |                   0.5   |              0.006 |             861.8 |              1873.1 |                -53.991 | large_difference_review_required    |
| Fvm131         | CW+HW+DR+PL+SS       | cwhvm1_hw_dr_l  | HW+DR                  |                   0.4   |              0.629 |            1077.1 |              1977.6 |                -45.535 | large_difference_review_required    |
| Fvh113         | CW+YC+HW+PL          | cwhvh1_cw_hw_m  | CW+HW                  |                   0.5   |              0.279 |             750   |              1091.9 |                -31.312 | large_difference_review_required    |
| Fvh101         | CW+YC+HW             | cwhvh1_cw_hw_m  | CW+HW                  |                   0.667 |              0.279 |             767.3 |              1091.9 |                -29.728 | large_difference_review_required    |
| Fvm106s        | CW+HW                | cwhvm1_cw_hw_h  | CW+HW                  |                   1     |              0.791 |            1414.9 |              1091.9 |                 29.581 | large_difference_review_required    |
| Fvm101s        | CW+HW                | cwhvm1_cw_hw_h  | CW+HW                  |                   1     |              0.791 |            1414.9 |              1091.9 |                 29.581 | large_difference_review_required    |
| Fvm201         | HW+YC+BA+CW+FD       | cwhvm1_cw_hw_h  | CW+HW                  |                   0.4   |              0.791 |            1404.5 |              1091.9 |                 28.629 | large_difference_review_required    |
| Fvh108         | SS+HW+CW+DR+BA       | cwhvh1_hw_cw_h  | HW+CW                  |                   0.4   |              0.773 |            1382.2 |              1873.1 |                -26.208 | large_difference_review_required    |
| Fvh106         | CW+YC+HW+SS+BA       | cwhvh1_hw_ba_h  | HW+BA                  |                   0.4   |              0.288 |            1574.5 |              1977.6 |                -20.383 | moderate_difference_review_required |
| Fvm109         | HW+CW+SS+DR+FD       | cwhvm1_hw_fdc_l | HW+FDC                 |                   0.4   |              0.364 |            1582.7 |              1977.6 |                -19.969 | moderate_difference_review_required |
| Fvm103         | CW+FD+HW+YC          | cwhvm2_yc_hw_h  | YC+HW                  |                   0.5   |              0.351 |            1016.8 |              1233.4 |                -17.561 | moderate_difference_review_required |
| Fvm105         | CW+FD+HW+SS          | cwhvm1_hw_ss_m  | HW+SS                  |                   0.5   |              0     |            1662.7 |              1977.6 |                -15.923 | moderate_difference_review_required |
| Fvm133         | CW+PL+HW+SS          | cwhvm1_cw_hw_m  | CW+HW                  |                   0.5   |              0.414 |             935.4 |              1091.9 |                -14.333 | moderate_difference_review_required |

## Review Rows

| mp11_au_code   | phase5_au_id   | phase5_match_confidence   |   max_volume_delta |   max_volume_pct_delta |   volume_age_100_delta |   volume_age_100_pct_delta |   age_curve_rmse | comparison_class                    |
|:---------------|:---------------|:--------------------------|-------------------:|-----------------------:|-----------------------:|---------------------------:|-----------------:|:------------------------------------|
| Fvm101s        | cwhvm1_cw_hw_h | medium                    |              323   |                 29.581 |                  324.8 |                     51.572 |          299.113 | large_difference_review_required    |
| Fvm106s        | cwhvm1_cw_hw_h | medium                    |              323   |                 29.581 |                  324.8 |                     51.572 |          299.113 | large_difference_review_required    |
| Fvm201         | cwhvm1_cw_hw_h | medium                    |              312.6 |                 28.629 |                  213   |                     33.82  |          239.088 | large_difference_review_required    |
| Fvh104         | cwhvh1_hw_ss_m | medium                    |               -6   |                 -0.448 |                  169.2 |                     25.235 |          117.464 | large_difference_review_required    |
| Fvh108         | cwhvh1_hw_cw_h | high                      |             -490.9 |                -26.208 |                 -110.1 |                    -10.241 |          290.692 | large_difference_review_required    |
| Fvh101         | cwhvh1_cw_hw_m | medium                    |             -324.6 |                -29.728 |                 -165   |                    -26.199 |          248.525 | large_difference_review_required    |
| Fvh113         | cwhvh1_cw_hw_m | medium                    |             -341.9 |                -31.312 |                 -174.1 |                    -27.644 |          262.005 | large_difference_review_required    |
| Fvm131         | cwhvm1_hw_dr_l | low                       |             -900.5 |                -45.535 |                 -434.9 |                    -39.368 |          617.484 | large_difference_review_required    |
| Fvm203         | cwhvm1_hw_cw_l | low                       |            -1011.3 |                -53.991 |                 -651.3 |                    -60.58  |          778.639 | large_difference_review_required    |
| Fvm211         | cwhvm1_hw_cw_l | low                       |            -1025.6 |                -54.754 |                 -652.3 |                    -60.673 |          784.456 | large_difference_review_required    |
| Fvh103         | cwhvh1_hw_cw_l | fallback_review_required  |            -1331   |                -71.059 |                 -796.1 |                    -74.049 |         1005.88  | large_difference_review_required    |
| Fvm101         | cwhvm2_ba_hw_h | medium                    |             -159.9 |                 -8.7   |                   84.7 |                      8.203 |           78.834 | low_difference                      |
| Fvm207         | cwhvm2_hw_cw_h | high                      |             -185   |                 -9.877 |                  -30.6 |                     -2.846 |           95.815 | low_difference                      |
| Fvm208         | cwhvm2_hw_cw_h | high                      |             -185   |                 -9.877 |                  -30.6 |                     -2.846 |           95.815 | low_difference                      |
| Fvh104s        | cwhvh1_cw_hw_h | medium                    |               44   |                  4.03  |                   86.9 |                     13.798 |           67.455 | moderate_difference_review_required |

## Use Boundary

- Phase 5 curves are comparison/fallback evidence, not MP11-equivalent
  curves.
- Generated MP11 curves remain `not_model_input` until reviewed and
  explicitly accepted.
- Downstream plots, model-input tables, ForestModel XML, and Patchworks
  packages must not consume these rows without a later promotion step.
