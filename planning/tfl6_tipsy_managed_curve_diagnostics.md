# TFL 6 P3.4e Treated Curve Diagnostics

## Purpose

This artifact records the first BTC/BatchTIPSY run and treated-vs-natural
curve QA for the selected top-area TFL 6 AU set. It is still a review
surface; it does not write `data/model_input_bundle`, ForestModel XML,
Matrix Builder inputs, or a Patchworks runtime package.

## Run Summary

- BTC input: `data/03_input-tfl6.csv`
- BTC output: `data/04_output-tfl6.csv`
- BTC error rows: `0`
- Parsed treated curve rows: `8316`
- Selected AUs with overlay plots: `77`

## Confidence Counts

| curve_lane             |   fallback_review_required |   high |   low |   medium |
|:-----------------------|---------------------------:|-------:|------:|---------:|
| existing_managed_11_50 |                         12 |     34 |     8 |       23 |
| existing_managed_1_10  |                         11 |     19 |    15 |       32 |
| future_managed         |                         11 |     11 |    19 |       36 |

## Treated-to-Natural Max-Volume Ratio Summary

| curve_lane             |   count |   min |   median |   max |
|:-----------------------|--------:|------:|---------:|------:|
| existing_managed_11_50 |      77 | 1.078 |    1.716 | 3.556 |
| existing_managed_1_10  |      77 | 1.031 |    1.725 | 8.282 |
| future_managed         |      77 | 1.157 |    1.657 | 8.283 |

## High-Ratio Review Flags

| au_id       | curve_lane            |   area_ha |   matched_legacy_au_code | match_confidence         |   max_treated_volume |   natural_max_volume |   treated_to_natural_max_ratio |   other_species_pct_encoded_as_dr |
|:------------|:----------------------|----------:|-------------------------:|:-------------------------|---------------------:|---------------------:|-------------------------------:|----------------------------------:|
| cwhvm1_dr_l | future_managed        |   342.369 |                     0500 | fallback_review_required |               1919   |              231.689 |                          8.283 |                                 0 |
| cwhvm1_dr_l | existing_managed_1_10 |   342.369 |                     0110 | fallback_review_required |               1918.8 |              231.689 |                          8.282 |                                 0 |
| cwhvm1_dr_m | future_managed        |   138.341 |                     0500 | fallback_review_required |               1919   |              334.2   |                          5.742 |                                 0 |
| cwhvm1_dr_m | existing_managed_1_10 |   138.341 |                     0110 | fallback_review_required |               1918.8 |              334.2   |                          5.741 |                                 0 |

## Largest Review Rows

| au_id          | curve_lane             |   area_ha |   matched_legacy_au_code | match_confidence   |   max_treated_volume |   natural_max_volume |   treated_to_natural_max_ratio |   other_species_pct_encoded_as_dr |
|:---------------|:-----------------------|----------:|-------------------------:|:-------------------|---------------------:|---------------------:|-------------------------------:|----------------------------------:|
| cwhvm1_hw_cw_m | existing_managed_1_10  |  14576.5  |                     7150 | medium             |               1315.9 |             1049.39  |                          1.254 |                                 0 |
| cwhvm1_hw_ba_m | existing_managed_1_10  |  13083.9  |                     6150 | medium             |               1330.6 |             1085.13  |                          1.226 |                                 0 |
| cwhvm1_cw_hw_h | future_managed         |   6154.4  |                     7500 | medium             |               1091.9 |              943.689 |                          1.157 |                                 0 |
| cwhvm1_cw_hw_l | existing_managed_11_50 |   6107.94 |                     6220 | medium             |               1127   |              783.068 |                          1.439 |                                 0 |
| cwhvm1_cw_hw_l | future_managed         |   6107.94 |                     7500 | medium             |               1091.9 |              783.068 |                          1.394 |                                 0 |
| cwhvm1_hw_m    | existing_managed_1_10  |   4138.94 |                     6150 | medium             |               1330.6 |              961.763 |                          1.384 |                                 0 |
| cwhvm1_hw_m    | future_managed         |   4138.94 |                     1510 | medium             |               1977.6 |              961.763 |                          2.056 |                                 0 |
| cwhvm1_hw_ss_l | existing_managed_1_10  |   4135.64 |                     6150 | medium             |               1330.6 |             1057.28  |                          1.259 |                                 0 |
| cwhvm1_hw_ss_l | future_managed         |   4135.64 |                     1510 | medium             |               1977.6 |             1057.28  |                          1.87  |                                 0 |
| cwhvm1_cw_hw_m | existing_managed_1_10  |   4015.12 |                     1120 | medium             |               1634.1 |              830.562 |                          1.967 |                                 0 |
| cwhvm1_cw_hw_m | future_managed         |   4015.12 |                     7500 | medium             |               1091.9 |              830.562 |                          1.315 |                                 0 |
| cwhvm2_hw_ba_l | existing_managed_11_50 |   3095.37 |                     9250 | medium             |               1359.8 |              920.312 |                          1.478 |                                 0 |
| cwhvm2_hw_ba_l | existing_managed_1_10  |   3095.37 |                     6150 | medium             |               1330.6 |              920.312 |                          1.446 |                                 0 |
| cwhvm2_hw_ba_l | future_managed         |   3095.37 |                     9510 | medium             |               1340.4 |              920.312 |                          1.456 |                                 0 |
| cwhvm1_hw_cw_h | future_managed         |   2899.43 |                     1500 | medium             |               1873.1 |             1191.46  |                          1.572 |                                 0 |
| cwhvm1_hw_ss_h | existing_managed_1_10  |   2240.22 |                     0150 | medium             |               2082.2 |             1185.82  |                          1.756 |                                 0 |
| cwhvm1_hw_ss_h | future_managed         |   2240.22 |                     1510 | medium             |               1977.6 |             1185.82  |                          1.668 |                                 0 |
| cwhvm1_hw_h    | existing_managed_1_10  |   1645.05 |                     0150 | medium             |               2082.2 |             1022.04  |                          2.037 |                                 0 |
| cwhvm1_hw_h    | future_managed         |   1645.05 |                     1510 | medium             |               1977.6 |             1022.04  |                          1.935 |                                 0 |
| cwhvm1_hw_l    | existing_managed_1_10  |   1582.41 |                     6150 | medium             |               1330.6 |              736.515 |                          1.807 |                                 0 |

## Review Notes

- BTC returned a complete row set for the selected AU/lane handoff.
- `other` MP10 species shares remain explicitly flagged where they were
  encoded as `Dr` for executable review.
- The high-ratio review flags are concentrated in small `CWHvm1_DR`
  fallback rows and should be treated as a row-level caveat rather than
  a broad failure of the dominant TFL 6 treated-curve handoff.
- These diagnostics support P3.4e curve review only. P3.5 treatment
  options and P3.6 transition logic should not start until the maintainer
  accepts or narrows any treated-curve review caveats.
