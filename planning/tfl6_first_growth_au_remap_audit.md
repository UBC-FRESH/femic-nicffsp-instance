# TFL 6 First-Growth AU Remap Audit

## Purpose

Record the P3.4 natural/untreated curve cardinality contract: build curves
only for the selected top-area AU set, then remap non-AU source stratum bins onto
that selected canonical curve universe using the established FEMIC
lexicographic stratum-name matching pattern.

## Counts

- Source stratum bins: `384`
- Canonical top-N AUs with curves: `77`
- Non-AU source stratum bins requiring remap/imputation: `307`
- Non-AU source stratum bins with an alias different from source: `307`

## Contract

- `canonical_curve_au_id` is the curve key to use for Phase 4 natural/
  untreated curve lookup.
- selected top-area AUs map to themselves.
- non-AU source stratum bins map to the closest selected AU by the FEMIC
  lexicographic alias rule, weighted by selected-area support when ties
  occur.
- non-AU source stratum bins are not published as separate canonical natural curve
  families.

## Largest Non-Selected Remaps

| source_au_id    | canonical_curve_au_id   | source_stratum_code   | canonical_stratum_code   |   area_ha | lexmatch_alias_used   |
|:----------------|:------------------------|:----------------------|:-------------------------|----------:|:----------------------|
| cwhvm1_hw_yc_m  | cwhvm1_cw_yc_m          | CWHvm1_HW+YC          | CWHvm1_CW+YC             |   311.914 | True                  |
| mhmm1_hw_ba_h   | cwhvm1_hw_ba_h          | MHmm1_HW+BA           | CWHvm1_HW+BA             |   267.225 | True                  |
| cwhvm1_yc_pl_l  | cwhvm1_yc_hw_l          | CWHvm1_YC+PL          | CWHvm1_YC+HW             |   262.208 | True                  |
| cwhvm2_cw_yc_l  | cwhvm1_cw_yc_l          | CWHvm2_CW+YC          | CWHvm1_CW+YC             |   261.488 | True                  |
| cwhvm2_hw_h     | cwhvm1_hw_h             | CWHvm2_HW             | CWHvm1_HW                |   253.224 | True                  |
| cwhvm1_fd_hw_l  | cwhvm1_cw_hw_l          | CWHvm1_FD+HW          | CWHvm1_CW+HW             |   242.25  | True                  |
| mhmm1_yc_hw_l   | cwhvm1_yc_hw_l          | MHmm1_YC+HW           | CWHvm1_YC+HW             |   226.956 | True                  |
| cwhvm2_hm_yc_l  | cwhvm2_hw_yc_l          | CWHvm2_HM+YC          | CWHvm2_HW+YC             |   221.379 | True                  |
| cwhvm2_hw_l     | cwhvm1_hw_l             | CWHvm2_HW             | CWHvm1_HW                |   220.855 | True                  |
| cwhvm1_fd_hw_h  | cwhvm1_cw_hw_h          | CWHvm1_FD+HW          | CWHvm1_CW+HW             |   217.755 | True                  |
| cwhvm2_yc_hm_l  | cwhvm2_yc_hw_l          | CWHvm2_YC+HM          | CWHvm2_YC+HW             |   213.343 | True                  |
| mhmm1_hw_ba_m   | cwhvm1_hw_ba_m          | MHmm1_HW+BA           | CWHvm1_HW+BA             |   209.003 | True                  |
| cwhvm2_hm_yc_m  | cwhvm2_hw_yc_m          | CWHvm2_HM+YC          | CWHvm2_HW+YC             |   193.712 | True                  |
| cwhvm2_yc_hm_m  | cwhvm2_yc_hw_m          | CWHvm2_YC+HM          | CWHvm2_YC+HW             |   181.464 | True                  |
| cwhvm1_cw_pl_m  | cwhvm1_cw_hw_m          | CWHvm1_CW+PL          | CWHvm1_CW+HW             |   180.574 | True                  |
| cwhvm2_yc_hm_h  | cwhvm2_yc_hw_h          | CWHvm2_YC+HM          | CWHvm2_YC+HW             |   179.119 | True                  |
| cwhvm2_hw_m     | cwhvm1_hw_m             | CWHvm2_HW             | CWHvm1_HW                |   173.739 | True                  |
| cwhvm1_cw_pl_l  | cwhvm1_cw_hw_l          | CWHvm1_CW+PL          | CWHvm1_CW+HW             |   171.751 | True                  |
| cwhvm1_fdc_hw_h | cwhvm1_dr_hw_h          | CWHvm1_FDC+HW         | CWHvm1_DR+HW             |   160.44  | True                  |
| cwhvm1_hw_yc_l  | cwhvm1_cw_yc_l          | CWHvm1_HW+YC          | CWHvm1_CW+YC             |   153.912 | True                  |
| cwhvm1_fd_hw_m  | cwhvm1_cw_hw_m          | CWHvm1_FD+HW          | CWHvm1_CW+HW             |   151.545 | True                  |
| cwhvm1_cw_pl_h  | cwhvm1_cw_hw_h          | CWHvm1_CW+PL          | CWHvm1_CW+HW             |   146.582 | True                  |
| cwhvm1_yc_hm_h  | cwhvm1_yc_hw_h          | CWHvm1_YC+HM          | CWHvm1_YC+HW             |   137.789 | True                  |
| cwhvh1_cw_h     | cwhvm1_cw_h             | CWHvh1_CW             | CWHvm1_CW                |   137.57  | True                  |
| mhmm1_hw_ba_l   | cwhvm1_hw_ba_l          | MHmm1_HW+BA           | CWHvm1_HW+BA             |   135.846 | True                  |
| mhmm1_ba_hw_l   | cwhvm1_ba_hw_l          | MHmm1_BA+HW           | CWHvm1_BA+HW             |   128.504 | True                  |
| cwhvm1_cw_ss_l  | cwhvm1_hw_ss_l          | CWHvm1_CW+SS          | CWHvm1_HW+SS             |   127.086 | True                  |
| cwhvm2_hm_yc_h  | cwhvm2_hw_yc_h          | CWHvm2_HM+YC          | CWHvm2_HW+YC             |   124.558 | True                  |
| cwhvm2_yc_cw_m  | cwhvm1_yc_cw_m          | CWHvm2_YC+CW          | CWHvm1_YC+CW             |   124.452 | True                  |
| cwhvm2_cw_yc_h  | cwhvm1_cw_yc_h          | CWHvm2_CW+YC          | CWHvm1_CW+YC             |   123.128 | True                  |

## Artifacts

- `planning/tfl6_first_growth_au_remap_audit.csv`
- `planning/tfl6_first_growth_au_remap_audit.md`
