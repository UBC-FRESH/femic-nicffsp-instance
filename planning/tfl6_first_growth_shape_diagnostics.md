# TFL 6 First-Growth Curve Shape Diagnostics

## Purpose

Classify the current P3.4d natural/untreated first-growth curve shapes
for the selected top-area AU set before changing smoothing parameters,
borrowing rules, or Phase 4 bundle inputs. This report is diagnostic
only: it does not alter
`planning/tfl6_first_growth_au_curves.csv`.

## Summary Counts

- Selected top-area AU diagnostic rows: `77`
- Accepted curve rows assessed: `77`
- OK shape rows: `23`
- Review shape rows: `54`
- Critical shape rows: `0`
- Insufficient-source rows: `0`

## Flag Counts

- `large_single_year_drop`: `16`
- `lmh_order_violation`: `54`
- `wobbly_multi_extrema`: `1`

## Recommended Action Counts

- `accept_shape`: `23`
- `increase_smoothing_or_shape_constraint`: `16`
- `review_lmh_order_or_borrowing`: `38`

## Critical Cases

Critical cases are accepted curves that appear unusable without a
replacement rule, especially curves that stay effectively zero until
old ages and then jump upward.

No critical accepted-curve shape cases were flagged.

## Review Cases

Review cases are softer warnings: terminal upticks, wobbly multi-extrema
behavior, large one-year drops, or L/M/H ordering violations.

| au_id          |   source_stand_count | shape_flags                                                     |   terminal_uptick_from_post_peak_min |   last_20_gain |   sign_change_count | recommended_action                     |
|:---------------|---------------------:|:----------------------------------------------------------------|-------------------------------------:|---------------:|--------------------:|:---------------------------------------|
| cwhvm1_yc_cw_m |                   61 | large_single_year_drop;lmh_order_violation                      |                             24.9212  |       3.05399  |                   2 | increase_smoothing_or_shape_constraint |
| cwhvm1_dr_l    |                  115 | lmh_order_violation                                             |                             14.0738  |      -0.571954 |                   2 | review_lmh_order_or_borrowing          |
| cwhvm2_yc_hw_h |                   71 | lmh_order_violation                                             |                              1.45284 |       1.10142  |                   3 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_ba_l |                  461 | lmh_order_violation                                             |                              1.28    |      -7.65369  |                   2 | review_lmh_order_or_borrowing          |
| cwhvm2_yc_hw_m |                   49 | large_single_year_drop;lmh_order_violation                      |                              1.02068 |      -0.463552 |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_yc_hw_l |                   96 | large_single_year_drop;lmh_order_violation                      |                              1       |      -9.37169  |                   2 | increase_smoothing_or_shape_constraint |
| cwhvh1_cw_hw_m |                  118 | lmh_order_violation                                             |                              0       |      -1.97234  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_dr_hw_l |                  142 | lmh_order_violation                                             |                              0       |      -2.92133  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_dr_m    |                   51 | lmh_order_violation                                             |                              0       |      -3.19911  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_yc_m |                   64 | lmh_order_violation                                             |                              0       |      -3.35801  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_hw_h |                   52 | lmh_order_violation                                             |                              0       |      -3.83692  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_ba_hw_m |                   69 | lmh_order_violation                                             |                              0       |      -7.37624  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_dr_h    |                   81 | lmh_order_violation                                             |                              0       |      -7.55222  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_yc_l |                   98 | large_single_year_drop;lmh_order_violation                      |                              0       |      -7.72986  |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm2_cw_hw_h |                   52 | lmh_order_violation                                             |                              0       |      -9.33469  |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_hw_cw_l |                  124 | lmh_order_violation                                             |                              0       |      -9.86987  |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_dr_hw_m |                  119 | lmh_order_violation                                             |                              0       |     -10.1718   |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_cw_hw_h |                  141 | lmh_order_violation                                             |                              0       |     -10.2946   |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_hw_cw_m |                   69 | lmh_order_violation                                             |                              0       |     -10.7231   |                   1 | review_lmh_order_or_borrowing          |
| cwhvh1_hw_cw_h |                  100 | lmh_order_violation                                             |                              0       |     -11.0265   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_dr_hw_h |                  124 | lmh_order_violation                                             |                              0       |     -11.1907   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_ba_hw_h |                   42 | lmh_order_violation                                             |                              0       |     -11.294    |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_cw_l |                  140 | lmh_order_violation                                             |                              0       |     -11.3401   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_ba_hw_h |                   51 | lmh_order_violation                                             |                              0       |     -11.9816   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_yc_h |                   82 | lmh_order_violation                                             |                              0       |     -12.1508   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_yc_l |                  222 | large_single_year_drop;lmh_order_violation                      |                              0       |     -12.7099   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvh1_cw_hw_l |                  175 | lmh_order_violation                                             |                              0       |     -13.0344   |                   3 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_cw_m |                  116 | lmh_order_violation                                             |                              0       |     -13.2596   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_hw_l |                  957 | lmh_order_violation                                             |                              0       |     -13.4575   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_ba_hw_l |                   73 | lmh_order_violation                                             |                              0       |     -13.9882   |                   3 | review_lmh_order_or_borrowing          |
| cwhvm1_ba_hw_m |                   37 | lmh_order_violation                                             |                              0       |     -15.0672   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_fd_l |                   70 | lmh_order_violation                                             |                              0       |     -15.5108   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_hw_m |                  600 | lmh_order_violation                                             |                              0       |     -15.7946   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_ba_hw_l |                   73 | lmh_order_violation                                             |                              0       |     -15.9211   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_cw_h |                  126 | lmh_order_violation                                             |                              0       |     -15.9353   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_fd_m |                   60 | lmh_order_violation                                             |                              0       |     -16.1148   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_ba_m |                  317 | lmh_order_violation                                             |                              0       |     -16.365    |                   1 | review_lmh_order_or_borrowing          |
| cwhvm2_hw_ba_h |                  330 | lmh_order_violation                                             |                              0       |     -16.7296   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_yc_cw_l |                   76 | large_single_year_drop;lmh_order_violation                      |                              0       |     -16.8139   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_ss_hw_m |                   73 | lmh_order_violation                                             |                              0       |     -17.1214   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_hw_h |                  741 | lmh_order_violation                                             |                              0       |     -18.0558   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_ss_hw_l |                   74 | lmh_order_violation                                             |                              0       |     -19.437    |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_hw_fd_h |                   59 | lmh_order_violation                                             |                              0       |     -20.4815   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_yc_h |                  126 | lmh_order_violation                                             |                              0       |     -22.5046   |                   1 | review_lmh_order_or_borrowing          |
| cwhvm1_cw_l    |                  175 | large_single_year_drop;lmh_order_violation                      |                              0       |     -24.0274   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm2_cw_hw_m |                   44 | large_single_year_drop;lmh_order_violation                      |                              0       |     -25.6406   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_yc_m |                   98 | large_single_year_drop;lmh_order_violation                      |                              0       |     -27.3793   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_h    |                  155 | large_single_year_drop;lmh_order_violation                      |                              0       |     -31.5065   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_yc_cw_h |                   44 | large_single_year_drop;lmh_order_violation                      |                              0       |     -33.2298   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm1_cw_m    |                  161 | large_single_year_drop;lmh_order_violation                      |                              0       |     -46.9102   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm1_ss_hw_h |                   69 | large_single_year_drop;lmh_order_violation                      |                              0       |     -50.3983   |                   1 | increase_smoothing_or_shape_constraint |
| cwhvm1_yc_hw_m |                   42 | large_single_year_drop;lmh_order_violation                      |                              0       |     -58.4251   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm2_cw_hw_l |                   63 | large_single_year_drop;lmh_order_violation                      |                              0       |     -72.8011   |                   3 | increase_smoothing_or_shape_constraint |
| cwhvm1_yc_hw_l |                  103 | wobbly_multi_extrema;large_single_year_drop;lmh_order_violation |                              0       |     -84.5848   |                   5 | increase_smoothing_or_shape_constraint |

## Insufficient-Source Cases

`0` selected top-area AUs still require borrowing/fallback review.

## Parameter-Tuning Implications

- Curves with `near_zero_to_old_age_then_jump` should not be accepted from
  the current fit. Prefer borrowing from an adjacent SI class or similar
  base AU until a support threshold or source-filter problem is resolved.
- Curves with `old_age_terminal_uptick`, `last_20_year_gain`, or
  `last_50_year_gain` need a tail constraint. Candidate tweaks include a
  no-upturn-after-terminal-decline rule, a terminal cap after the last
  reliable observed age bin, or a stronger old-age tail penalty.
- Curves with `wobbly_multi_extrema` or `large_single_year_drop` need
  stronger smoothing or a shape-constrained post-process before they are
  eligible for model-input bundle use.
- L/M/H order violations should be reviewed at the base-AU family level.
  If the low or medium SI curve crosses a higher SI curve materially,
  either borrow from the better-supported adjacent SI class or apply a
  family-level ordering constraint.

## Artifacts

- `planning/tfl6_first_growth_shape_diagnostics.csv`
- `planning/tfl6_first_growth_shape_diagnostics.md`
- Non-selected AU imputation is audited separately in
  `planning/tfl6_first_growth_au_remap_audit.csv`.
- Inputs: `planning/tfl6_first_growth_au_curves.csv` and
  `planning/tfl6_first_growth_au_fit_diagnostics.csv`
