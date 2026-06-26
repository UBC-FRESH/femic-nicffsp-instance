# TFL 6 Static AU Universe Review

## Purpose

This note completes the P3.4b review surface for the first static TFL 6 AU and
stratum universe. It compiles candidate AU identities from the accepted current
TFL 6 R1 geometry and VDYP7 primary-layer attributes, and it produces the same
strata distribution diagnostic used in the other FEMIC instance examples before
MP10 TIPSY parameter crosswalk work.

This is a review-only artifact. It does not write `data/model_input_bundle`,
generate VDYP or BatchTIPSY curves, execute a TIPSY crosswalk, or encode THLB,
operability, treatment eligibility, cedar status, or NICF expansion status into
AU identity.

## Inputs

| Input | Path | Role |
| --- | --- | --- |
| R1 geometry | `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` | current TFL 6 geometry, area, BEC, and reporting attributes |
| VDYP7 layer | `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` | primary-layer species, site index, age, height, and density attributes |

## Static AU Policy Used Here

| Component | Review policy |
| --- | --- |
| BEC grouping | zone plus subzone, matching `stratification.bec_grouping: subzone` |
| Species combo | top two non-null VDYP primary-layer species by percentage/listed order |
| Top-area threshold | select the smallest ranked stratum set whose cumulative area reaches at least `90%` of the yieldable review universe |
| SI class | stratum-local `estimated_site_index` p35/p65 breakpoints into `L`, `M`, and `H` review bins |
| AU key | `bec_group + species_combo + si_class` |

The SI split is intentionally review-oriented. P3.4d/P3.4f still own the final
curve-bin policy, sparse-bin rescue, and curve-selection diagnostics.

## Counts

| Metric | Value |
| --- | ---: |
| R1 rows | `26959` |
| R1 area | `217,042.719 ha` |
| VDYP7 layer rows | `25585` |
| VDYP primary feature rows | `25356` |
| R1 rows without VDYP primary layer | `1603` |
| Yieldable review rows | `17223` |
| Yieldable review area | `135,692.628 ha` |
| Excluded review area | `81,350.091 ha` |
| Static strata | `136` |
| Selected top-area strata | `18` |
| Selected top-area coverage | `90.267%` |
| All review AU count | `297` |
| Selected top-area AU count | `53` |

## Exclusion Diagnostics

| Diagnostic | Rows |
| --- | ---: |
| Missing VDYP primary layer | `1603` |
| Missing species combo | `1765` |
| Missing or zero estimated site index | `9625` |
| Missing or zero area | `0` |

These diagnostics overlap. They are intended to guide review, not to sum to a
single exclusion total.

## Strata Distribution Plot

The P3.4b diagnostic uses `femic.pipeline.plots.render_strata_distribution_plot`,
the same horizontal relative-abundance plus site-index violin specification used
by the K3Z and MKRF instance examples.

| Plot field | Value |
| --- | ---: |
| PNG | `plots/strata-tfl6.png` |
| PDF | `plots/strata-tfl6.pdf` |
| Selected strata plotted | `18` |
| SI axis window | `0.0-30.0` |
| Total plotted-candidate points | `15131` |
| In-window points | `14042` |
| Sampled strip points plotted | `3000` |
| High-SI points clipped from view | `1089` |

## Top Strata By Area

|   area_rank | stratum_code   | bec_group   | species_combo   |   stand_count |   area_ha | area_share   | cumulative_area_share   | selected_top_90   |
|------------:|:---------------|:------------|:----------------|--------------:|----------:|:-------------|:------------------------|:------------------|
|           1 | CWHVM_HW_BA    | CWHvm       | HW_BA           |          3783 |   34839.1 | 25.675%      | 25.675%                 | yes               |
|           2 | CWHVM_HW_CW    | CWHvm       | HW_CW           |          3450 |   27333.5 | 20.144%      | 45.819%                 | yes               |
|           3 | CWHVM_CW_HW    | CWHvm       | CW_HW           |          2372 |   17477.9 | 12.880%      | 58.699%                 | yes               |
|           4 | CWHVM_HW       | CWHvm       | HW              |          1185 |    8014.2 | 5.906%       | 64.605%                 | yes               |
|           5 | CWHVM_HW_SS    | CWHvm       | HW_SS           |           777 |    7339.9 | 5.409%       | 70.015%                 | yes               |
|           6 | CWHVM_HW_DR    | CWHvm       | HW_DR           |           452 |    3264   | 2.405%       | 72.420%                 | yes               |
|           7 | CWHVH_CW_HW    | CWHvh       | CW_HW           |           435 |    3106.1 | 2.289%       | 74.709%                 | yes               |
|           8 | CWHVM_CW       | CWHvm       | CW              |           475 |    2757.6 | 2.032%       | 76.741%                 | yes               |
|           9 | CWHVM_CW_YC    | CWHvm       | CW_YC           |           236 |    2555.4 | 1.883%       | 78.625%                 | yes               |
|          10 | CWHVM_HW_FDC   | CWHvm       | HW_FDC          |           167 |    2232.7 | 1.645%       | 80.270%                 | yes               |
|          11 | CWHVM_BA_HW    | CWHvm       | BA_HW           |           268 |    2135.1 | 1.573%       | 81.844%                 | yes               |
|          12 | CWHVM_HW_FD    | CWHvm       | HW_FD           |           194 |    2055.5 | 1.515%       | 83.358%                 | yes               |
|          13 | CWHVH_HW_CW    | CWHvh       | HW_CW           |           291 |    1947.7 | 1.435%       | 84.794%                 | yes               |
|          14 | CWHVM_YC_HW    | CWHvm       | YC_HW           |           193 |    1741.4 | 1.283%       | 86.077%                 | yes               |
|          15 | CWHVM_SS_HW    | CWHvm       | SS_HW           |           159 |    1649.5 | 1.216%       | 87.293%                 | yes               |
|          16 | CWHVM_DR_HW    | CWHvm       | DR_HW           |           334 |    1476.1 | 1.088%       | 88.380%                 | yes               |
|          17 | CWHVM_HW_YC    | CWHvm       | HW_YC           |           212 |    1406.6 | 1.037%       | 89.417%                 | yes               |
|          18 | CWHVM_YC_CW    | CWHvm       | YC_CW           |           148 |    1153.9 | 0.850%       | 90.267%                 | yes               |
|          19 | CWHVH_HW_BA    | CWHvh       | HW_BA           |           172 |     981   | 0.723%       | 90.990%                 | no                |
|          20 | CWHVH_HW_SS    | CWHvh       | HW_SS           |           123 |     887.8 | 0.654%       | 91.645%                 | no                |

## Largest Selected AU Bins

| au_id          | stratum_code   | si_class   |   stand_count |   area_ha |   mean_si |   median_si |
|:---------------|:---------------|:-----------|--------------:|----------:|----------:|------------:|
| cwhvm_hw_ba_m  | CWHVM_HW_BA    | M          |          1727 |   17626.9 |      25.9 |        27   |
| cwhvm_hw_cw_m  | CWHVM_HW_CW    | M          |          1827 |   16323.1 |      26   |        28   |
| cwhvm_hw_ba_l  | CWHVM_HW_BA    | L          |          1476 |   10048.7 |      16   |        16   |
| cwhvm_hw_cw_l  | CWHVM_HW_CW    | L          |          1265 |    8056.1 |      15.4 |        16   |
| cwhvm_hw_ba_h  | CWHVM_HW_BA    | H          |           580 |    7163.5 |      31.1 |        30   |
| cwhvm_cw_hw_l  | CWHVM_CW_HW    | L          |          1024 |    6683.8 |      13.3 |        14   |
| cwhvm_cw_hw_h  | CWHVM_CW_HW    | H          |           747 |    6537.6 |      23.8 |        23   |
| cwhvm_hw_m     | CWHVM_HW       | M          |           524 |    4569.6 |      26   |        27   |
| cwhvm_cw_hw_m  | CWHVM_CW_HW    | M          |           601 |    4256.5 |      18.6 |        19   |
| cwhvm_hw_ss_l  | CWHVM_HW_SS    | L          |           468 |    4171.2 |      24.4 |        27   |
| cwhvm_hw_cw_h  | CWHVM_HW_CW    | H          |           358 |    2954.3 |      30.8 |        30   |
| cwhvm_hw_ss_h  | CWHVM_HW_SS    | H          |           236 |    2240.2 |      32.4 |        32   |
| cwhvm_hw_l     | CWHVM_HW       | L          |           435 |    1786.8 |      15.4 |        16   |
| cwhvm_hw_h     | CWHVM_HW       | H          |           226 |    1657.8 |      31.4 |        30.5 |
| cwhvm_cw_h     | CWHVM_CW       | H          |           166 |    1556.9 |      20.8 |        19   |
| cwhvm_hw_fdc_l | CWHVM_HW_FDC   | L          |           116 |    1343.9 |      27.1 |        28   |
| cwhvm_cw_yc_m  | CWHVM_CW_YC    | M          |            80 |    1286.4 |      13   |        12.5 |
| cwhvm_hw_dr_m  | CWHVM_HW_DR    | M          |           154 |    1199.8 |      27.5 |        27   |
| cwhvh_cw_hw_l  | CWHVH_CW_HW    | L          |           175 |    1104.1 |      12.2 |        13   |
| cwhvh_cw_hw_h  | CWHVH_CW_HW    | H          |           138 |    1076.8 |      20.7 |        20   |
| cwhvm_hw_dr_l  | CWHVM_HW_DR    | L          |           160 |    1052.4 |      19.3 |        20.5 |
| cwhvm_hw_dr_h  | CWHVM_HW_DR    | H          |           138 |    1011.8 |      31.7 |        31   |
| cwhvm_ba_hw_m  | CWHVM_BA_HW    | M          |            99 |     974.7 |      25   |        26   |
| cwhvm_yc_hw_l  | CWHVM_YC_HW    | L          |            75 |     930.3 |       8.2 |         9   |
| cwhvm_hw_ss_m  | CWHVM_HW_SS    | M          |            73 |     928.5 |      29   |        29   |

## Downstream Use

P3.4c should use this AU universe as the review surface for mapping static TFL 6
AUs to MP10 Tables 27-29 TIPSY parameter rows or explicit fallbacks. P3.4d and
P3.4e should generate the untreated VDYP and treated BatchTIPSY curve lanes only
after the AU review surface and crosswalk are accepted.
