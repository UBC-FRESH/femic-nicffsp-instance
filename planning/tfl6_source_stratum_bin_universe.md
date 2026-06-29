# TFL 6 Source Stratum-Bin Universe Review

## Purpose

This archived note records the source stratum-bin universe used for P3.4b remap provenance. Source stratum bins outside the selected top-area set are not analysis units. It compiles candidate AU identities from the accepted current
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
| BEC grouping | zone plus subzone plus variant plus phase where present; current R1 phase is null for all rows |
| Species combo | top two non-null VDYP primary-layer species by percentage/listed order, rendered as `species1+species2` |
| Top-area threshold | select the smallest ranked stratum set whose cumulative area reaches at least `90%` of the yieldable review universe |
| SI class | stratum-local `estimated_site_index` p35/p65 breakpoints into `L`, `M`, and `H` review bins |
| AU key | `bec_zone + bec_subzone + bec_variant + bec_phase + species_combo + si_class` |

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
| Static strata | `174` |
| Selected top-area strata | `26` |
| Selected top-area coverage | `90.397%` |
| Source stratum-bin count | `384` |
| Canonical top-N AU count | `77` |

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
by the K3Z and MKRF instance examples. The SI axis is widened for TFL 6 because
site indexes are high in this productive coastal rainforest area.

| Plot field | Value |
| --- | ---: |
| PNG | `plots/strata-tfl6.png` |
| PDF | `plots/strata-tfl6.pdf` |
| Selected strata plotted | `26` |
| SI axis window | `0.0-55.0` |
| Total plotted-candidate points | `15290` |
| In-window points | `15290` |
| Sampled strip points plotted | `3000` |
| High-SI points clipped from view | `0` |

## Top Strata By Area

|   area_rank | stratum_code   | bec_group   | species_combo   |   stand_count |   area_ha | area_share   | cumulative_area_share   | selected_top_90   |
|------------:|:---------------|:------------|:----------------|--------------:|----------:|:-------------|:------------------------|:------------------|
|           1 | CWHvm1_HW+BA   | CWHvm1      | HW+BA           |          2705 |   25748.6 | 18.976%      | 18.976%                 | yes               |
|           2 | CWHvm1_HW+CW   | CWHvm1      | HW+CW           |          3063 |   24593.8 | 18.125%      | 37.100%                 | yes               |
|           3 | CWHvm1_CW+HW   | CWHvm1      | CW+HW           |          2212 |   16277.5 | 11.996%      | 49.096%                 | yes               |
|           4 | CWHvm2_HW+BA   | CWHvm2      | HW+BA           |          1078 |    9090.5 | 6.699%       | 55.795%                 | yes               |
|           5 | CWHvm1_HW      | CWHvm1      | HW              |          1046 |    7366.4 | 5.429%       | 61.224%                 | yes               |
|           6 | CWHvm1_HW+SS   | CWHvm1      | HW+SS           |           772 |    7304.3 | 5.383%       | 66.607%                 | yes               |
|           7 | CWHvh1_CW+HW   | CWHvh1      | CW+HW           |           435 |    3106.1 | 2.289%       | 68.896%                 | yes               |
|           8 | CWHvm1_HW+DR   | CWHvm1      | HW+DR           |           432 |    3090.1 | 2.277%       | 71.174%                 | yes               |
|           9 | CWHvm2_HW+CW   | CWHvm2      | HW+CW           |           387 |    2739.7 | 2.019%       | 73.193%                 | yes               |
|          10 | CWHvm1_CW      | CWHvm1      | CW              |           442 |    2626.1 | 1.935%       | 75.128%                 | yes               |
|          11 | CWHvm1_HW+FDC  | CWHvm1      | HW+FDC          |           161 |    2177.7 | 1.605%       | 76.733%                 | yes               |
|          12 | CWHvm1_CW+YC   | CWHvm1      | CW+YC           |           189 |    2064.5 | 1.521%       | 78.254%                 | yes               |
|          13 | CWHvh1_HW+CW   | CWHvh1      | HW+CW           |           291 |    1947.7 | 1.435%       | 79.690%                 | yes               |
|          14 | CWHvm1_HW+FD   | CWHvm1      | HW+FD           |           182 |    1892.1 | 1.394%       | 81.084%                 | yes               |
|          15 | CWHvm1_SS+HW   | CWHvm1      | SS+HW           |           157 |    1638.1 | 1.207%       | 82.291%                 | yes               |
|          16 | CWHvm1_DR+HW   | CWHvm1      | DR+HW           |           325 |    1437.8 | 1.060%       | 83.351%                 | yes               |
|          17 | CWHvm2_BA+HW   | CWHvm2      | BA+HW           |           157 |    1433.5 | 1.056%       | 84.407%                 | yes               |
|          18 | CWHvm2_CW+HW   | CWHvm2      | CW+HW           |           160 |    1200.4 | 0.885%       | 85.292%                 | yes               |
|          19 | CWHvh1_HW+BA   | CWHvh1      | HW+BA           |           172 |     981   | 0.723%       | 86.015%                 | yes               |
|          20 | CWHvm2_HW+YC   | CWHvm2      | HW+YC           |           149 |     934.9 | 0.689%       | 86.704%                 | yes               |

## Largest Canonical Top-N AU Rows

| au_id           | stratum_code   | si_class   |   stand_count |   area_ha |   mean_si |   median_si |
|:----------------|:---------------|:-----------|--------------:|----------:|----------:|------------:|
| cwhvm1_hw_cw_m  | CWHvm1_HW+CW   | M          |          1602 |   14576.5 |      26.4 |        28   |
| cwhvm1_hw_ba_m  | CWHvm1_HW+BA   | M          |          1222 |   13083.9 |      26.3 |        27   |
| cwhvm1_hw_cw_l  | CWHvm1_HW+CW   | L          |          1112 |    7117.9 |      16   |        16   |
| cwhvm1_hw_ba_h  | CWHvm1_HW+BA   | H          |           531 |    6336.7 |      31.2 |        31   |
| cwhvm1_hw_ba_l  | CWHvm1_HW+BA   | L          |           952 |    6328   |      17.1 |        17   |
| cwhvm1_cw_hw_h  | CWHvm1_CW+HW   | H          |           717 |    6154.4 |      23.8 |        23   |
| cwhvm1_cw_hw_l  | CWHvm1_CW+HW   | L          |           927 |    6107.9 |      13.4 |        14   |
| cwhvm1_hw_m     | CWHvm1_HW      | M          |           448 |    4138.9 |      26.4 |        27   |
| cwhvm1_hw_ss_l  | CWHvm1_HW+SS   | L          |           463 |    4135.6 |      24.5 |        27   |
| cwhvm1_cw_hw_m  | CWHvm1_CW+HW   | M          |           568 |    4015.1 |      18.6 |        19   |
| cwhvm2_hw_ba_h  | CWHvm2_HW+BA   | H          |           326 |    3577   |      27.7 |        28   |
| cwhvm2_hw_ba_l  | CWHvm2_HW+BA   | L          |           448 |    3095.4 |      13.8 |        14   |
| cwhvm1_hw_cw_h  | CWHvm1_HW+CW   | H          |           349 |    2899.4 |      30.8 |        30   |
| cwhvm2_hw_ba_m  | CWHvm2_HW+BA   | M          |           304 |    2418.1 |      20.1 |        20   |
| cwhvm1_hw_ss_h  | CWHvm1_HW+SS   | H          |           236 |    2240.2 |      32.4 |        32   |
| cwhvm1_hw_h     | CWHvm1_HW      | H          |           223 |    1645   |      31.4 |        30   |
| cwhvm1_hw_l     | CWHvm1_HW      | L          |           375 |    1582.4 |      16   |        16   |
| cwhvm1_cw_h     | CWHvm1_CW      | H          |           131 |    1331.3 |      21.7 |        22   |
| cwhvm1_cw_yc_l  | CWHvm1_CW+YC   | L          |            93 |    1293.9 |      10.1 |        11   |
| cwhvm1_hw_fdc_l | CWHvm1_HW+FDC  | L          |           110 |    1288.9 |      27.4 |        28   |
| cwhvm1_hw_dr_m  | CWHvm1_HW+DR   | M          |           148 |    1157.3 |      27.5 |        27.5 |
| cwhvm2_hw_cw_h  | CWHvm2_HW+CW   | H          |           131 |    1136.4 |      25.9 |        26   |
| cwhvh1_cw_hw_l  | CWHvh1_CW+HW   | L          |           175 |    1104.1 |      12.2 |        13   |
| cwhvh1_cw_hw_h  | CWHvh1_CW+HW   | H          |           138 |    1076.8 |      20.7 |        20   |
| cwhvm1_hw_dr_l  | CWHvm1_HW+DR   | L          |           151 |     983.3 |      19.4 |        20   |

## Downstream Use

P3.4c should use this AU universe as the review surface for mapping static TFL 6
AUs to MP10 Tables 27-29 TIPSY parameter rows or explicit fallbacks. P3.4d and
P3.4e should generate the untreated VDYP and treated BatchTIPSY curve lanes only
after the AU review surface and crosswalk are accepted.
