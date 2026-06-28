# TFL 6 MP11 Managed Curve Phase 5 Comparison

## Purpose

This P10R.4e artifact compares the generated MP11 Table 57 future-managed
candidate curves against the nearest available Phase 5 future-managed
fallback curves. It is a review surface only and does not promote any
curve to model input.

## Status

- MP11 candidate rows compared: `27`
- Phase 5 comparison matches: `27`
- Model-input status: `not_model_input`

## Method

Nearest Phase 5 future-managed comparison row selected by matching BEC zone/subzone first, then maximizing species overlap and minimizing weighted site-index difference.

## Comparison Classes

- `large_difference_review_required`: `13`
- `low_difference`: `3`
- `moderate_difference_review_required`: `11`

## Largest Absolute Max-Volume Differences

| mp11_au_code   | mp11_species_combo   | phase5_au_id   | phase5_species_combo   |   species_overlap_ratio |   mean_si_abs_diff |   mp11_max_volume |   phase5_max_volume |   max_volume_pct_delta | comparison_class                    |
|:---------------|:---------------------|:---------------|:-----------------------|------------------------:|-------------------:|------------------:|--------------------:|-----------------------:|:------------------------------------|
| Fvh103         | CW+YC+HW+BA+PL       | cwhvh1_cw_hw_l | CW+HW                  |                   0.4   |              3.739 |             220.3 |              1091.9 |                -79.824 | large_difference_review_required    |
| Fvm211         | HW+CW+YC+BA          | cwhvm1_hw_cw_l | HW+CW                  |                   0.5   |              0.226 |             830.4 |              1873.1 |                -55.667 | large_difference_review_required    |
| Fvm131         | CW+HW+DR+PL+SS       | cwhvm1_hw_dr_l | HW+DR                  |                   0.4   |              0.651 |            1044.5 |              1977.6 |                -47.183 | large_difference_review_required    |
| FMH22          | HW+BA+YC             | cwhvm2_hw_ba_l | HW+BA                  |                   0.667 |              0.44  |             769.4 |              1340.4 |                -42.599 | large_difference_review_required    |
| FMH01          | HW+BA+YC             | cwhvm2_hw_ba_l | HW+BA                  |                   0.667 |              0.44  |             783.1 |              1340.4 |                -41.577 | large_difference_review_required    |
| Fvm106s        | CW+HW                | cwhvm1_cw_hw_h | CW+HW                  |                   1     |              0.206 |            1462.2 |              1091.9 |                 33.913 | large_difference_review_required    |
| Fvm201         | HW+YC+BA+CW+FD       | cwhvm1_cw_hw_h | CW+HW                  |                   0.4   |              0.329 |            1459.3 |              1091.9 |                 33.648 | large_difference_review_required    |
| Fvh113         | CW+YC+HW+PL          | cwhvh1_cw_hw_m | CW+HW                  |                   0.5   |              0.279 |             750   |              1091.9 |                -31.312 | large_difference_review_required    |
| Fvm101s        | CW+HW                | cwhvm1_cw_hw_h | CW+HW                  |                   1     |              0.426 |            1429.6 |              1091.9 |                 30.928 | large_difference_review_required    |
| Fvh108         | SS+HW+CW+DR+BA       | cwhvh1_hw_cw_h | HW+CW                  |                   0.4   |              0.427 |            1305.9 |              1873.1 |                -30.281 | large_difference_review_required    |
| Fvh101         | CW+YC+HW             | cwhvh1_cw_hw_m | CW+HW                  |                   0.667 |              0.279 |             767.3 |              1091.9 |                -29.728 | large_difference_review_required    |
| Fvm103         | CW+FD+HW+YC          | cwhvm2_yc_hw_h | YC+HW                  |                   0.5   |              0.681 |             922   |              1233.4 |                -25.247 | large_difference_review_required    |
| Fvm105         | CW+FD+HW+SS          | cwhvm1_hw_ss_m | HW+SS                  |                   0.5   |              0.39  |            1494.9 |              1977.6 |                -24.408 | moderate_difference_review_required |
| Fvh106         | CW+YC+HW+SS+BA       | cwhvh1_hw_ba_h | HW+BA                  |                   0.4   |              0.888 |            1496.5 |              1977.6 |                -24.327 | moderate_difference_review_required |
| Fvm203         | HW+CW+BA+YC          | cwhvm2_cw_hw_m | CW+HW                  |                   0.5   |              0.138 |             827.6 |              1091.9 |                -24.206 | large_difference_review_required    |

## Review Rows

| mp11_au_code   | phase5_au_id   | phase5_match_confidence   |   max_volume_delta |   max_volume_pct_delta |   volume_age_100_delta |   volume_age_100_pct_delta |   age_curve_rmse | comparison_class                 |
|:---------------|:---------------|:--------------------------|-------------------:|-----------------------:|-----------------------:|---------------------------:|-----------------:|:---------------------------------|
| Fvm106s        | cwhvm1_cw_hw_h | medium                    |              370.3 |                 33.913 |                  362.5 |                     57.558 |          340.551 | large_difference_review_required |
| Fvm201         | cwhvm1_cw_hw_h | medium                    |              367.4 |                 33.648 |                  246.7 |                     39.171 |          277.123 | large_difference_review_required |
| Fvm101s        | cwhvm1_cw_hw_h | medium                    |              337.7 |                 30.928 |                  338   |                     53.668 |          313.24  | large_difference_review_required |
| Fvm203         | cwhvm2_cw_hw_m | medium                    |             -264.3 |                -24.206 |                 -226.7 |                    -35.996 |          247.697 | large_difference_review_required |
| Fvm103         | cwhvm2_yc_hw_h | medium                    |             -311.4 |                -25.247 |                  -28.3 |                     -4.497 |          191.935 | large_difference_review_required |
| Fvh101         | cwhvh1_cw_hw_m | medium                    |             -324.6 |                -29.728 |                 -165   |                    -26.199 |          248.525 | large_difference_review_required |
| Fvh108         | cwhvh1_hw_cw_h | high                      |             -567.2 |                -30.281 |                 -171.8 |                    -15.98  |          352.143 | large_difference_review_required |
| Fvh113         | cwhvh1_cw_hw_m | medium                    |             -341.9 |                -31.312 |                 -174.1 |                    -27.644 |          262.005 | large_difference_review_required |
| FMH01          | cwhvm2_hw_ba_l | medium                    |             -557.3 |                -41.577 |                 -354.3 |                    -52.841 |          430.23  | large_difference_review_required |
| FMH22          | cwhvm2_hw_ba_l | medium                    |             -571   |                -42.599 |                 -388.5 |                    -57.942 |          453.795 | large_difference_review_required |
| Fvm131         | cwhvm1_hw_dr_l | low                       |             -933.1 |                -47.183 |                 -445.9 |                    -40.364 |          642.079 | large_difference_review_required |
| Fvm211         | cwhvm1_hw_cw_l | low                       |            -1042.7 |                -55.667 |                 -662.6 |                    -61.631 |          796.976 | large_difference_review_required |
| Fvh103         | cwhvh1_cw_hw_l | medium                    |             -871.6 |                -79.824 |                 -559.7 |                    -88.869 |          709.247 | large_difference_review_required |
| Fvm207         | cwhvm1_hw_cw_m | high                      |             -165.7 |                 -8.846 |                  -22.7 |                     -2.111 |           85.29  | low_difference                   |
| Fvm208         | cwhvm1_hw_cw_m | high                      |             -165.7 |                 -8.846 |                  -22.7 |                     -2.111 |           85.29  | low_difference                   |

## Use Boundary

- Phase 5 curves are comparison/fallback evidence, not MP11-equivalent
  curves.
- Generated MP11 curves remain `not_model_input` until reviewed and
  explicitly accepted.
- Downstream plots, model-input tables, ForestModel XML, and Patchworks
  packages must not consume these rows without a later promotion step.
