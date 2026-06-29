# TFL 6 Static AU Universe Review

## Purpose

This artifact defines the canonical TFL 6 AU universe. In this instance, an
analysis unit is only an L/M/H site-index split of a selected top-area
stratum. Source strata outside the top-N selected set are not AUs; they are
source stratum bins that may be remapped to this canonical AU universe for
curve lookup or provenance.

## Counts

- Canonical AU rows: `77`
- Selected top-area strata: `26`
- Source stratum-bin rows preserved for remap provenance: `384`
- Non-AU source stratum-bin rows: `307`

## Artifacts

- Canonical AU universe: `planning/tfl6_static_au_universe.csv`
- Source stratum-bin universe: `planning/tfl6_source_stratum_bin_universe.csv`
- Top-strata summary: `planning/tfl6_static_au_top_strata.csv`

## Canonical AU Rows

| au_id           | stratum_code   | si_class   |   stand_count |    area_ha |   mean_si |   median_si |   min_si |   max_si | selected_top_90_stratum   |
|:----------------|:---------------|:-----------|--------------:|-----------:|----------:|------------:|---------:|---------:|:--------------------------|
| cwhvm1_hw_cw_m  | CWHvm1_HW+CW   | M          |          1602 | 14576.5    |  26.4057  |        28   |       22 |       28 | True                      |
| cwhvm1_hw_ba_m  | CWHvm1_HW+BA   | M          |          1222 | 13083.9    |  26.2782  |        27   |       22 |       28 | True                      |
| cwhvm1_hw_cw_l  | CWHvm1_HW+CW   | L          |          1112 |  7117.88   |  16.0063  |        16   |        3 |       21 | True                      |
| cwhvm1_hw_ba_h  | CWHvm1_HW+BA   | H          |           531 |  6336.71   |  31.1695  |        31   |       29 |       43 | True                      |
| cwhvm1_hw_ba_l  | CWHvm1_HW+BA   | L          |           952 |  6328.04   |  17.1429  |        17   |        7 |       21 | True                      |
| cwhvm1_cw_hw_h  | CWHvm1_CW+HW   | H          |           717 |  6154.4    |  23.7908  |        23   |       21 |       41 | True                      |
| cwhvm1_cw_hw_l  | CWHvm1_CW+HW   | L          |           927 |  6107.94   |  13.3635  |        14   |        2 |       16 | True                      |
| cwhvm1_hw_m     | CWHvm1_HW      | M          |           448 |  4138.94   |  26.3616  |        27   |       22 |       28 | True                      |
| cwhvm1_hw_ss_l  | CWHvm1_HW+SS   | L          |           463 |  4135.64   |  24.46    |        27   |        7 |       28 | True                      |
| cwhvm1_cw_hw_m  | CWHvm1_CW+HW   | M          |           568 |  4015.12   |  18.5863  |        19   |       17 |       20 | True                      |
| cwhvm2_hw_ba_h  | CWHvm2_HW+BA   | H          |           326 |  3577.02   |  27.7454  |        28   |       25 |       41 | True                      |
| cwhvm2_hw_ba_l  | CWHvm2_HW+BA   | L          |           448 |  3095.37   |  13.7902  |        14   |        7 |       16 | True                      |
| cwhvm1_hw_cw_h  | CWHvm1_HW+CW   | H          |           349 |  2899.43   |  30.7966  |        30   |       29 |       42 | True                      |
| cwhvm2_hw_ba_m  | CWHvm2_HW+BA   | M          |           304 |  2418.08   |  20.0559  |        20   |       17 |       24 | True                      |
| cwhvm1_hw_ss_h  | CWHvm1_HW+SS   | H          |           236 |  2240.22   |  32.3644  |        32   |       30 |       42 | True                      |
| cwhvm1_hw_h     | CWHvm1_HW      | H          |           223 |  1645.05   |  31.3632  |        30   |       29 |       42 | True                      |
| cwhvm1_hw_l     | CWHvm1_HW      | L          |           375 |  1582.41   |  15.9947  |        16   |        1 |       21 | True                      |
| cwhvm1_cw_h     | CWHvm1_CW      | H          |           131 |  1331.28   |  21.7405  |        22   |       17 |       42 | True                      |
| cwhvm1_cw_yc_l  | CWHvm1_CW+YC   | L          |            93 |  1293.87   |  10.129   |        11   |        4 |       12 | True                      |
| cwhvm1_hw_fdc_l | CWHvm1_HW+FDC  | L          |           110 |  1288.94   |  27.3636  |        28   |       22 |       28 | True                      |
| cwhvm1_hw_dr_m  | CWHvm1_HW+DR   | M          |           148 |  1157.28   |  27.5203  |        27.5 |       26 |       29 | True                      |
| cwhvm2_hw_cw_h  | CWHvm2_HW+CW   | H          |           131 |  1136.41   |  25.9008  |        26   |       22 |       33 | True                      |
| cwhvh1_cw_hw_l  | CWHvh1_CW+HW   | L          |           175 |  1104.14   |  12.2343  |        13   |        6 |       14 | True                      |
| cwhvh1_cw_hw_h  | CWHvh1_CW+HW   | H          |           138 |  1076.78   |  20.7246  |        20   |       17 |       31 | True                      |
| cwhvm1_hw_dr_l  | CWHvm1_HW+DR   | L          |           151 |   983.327  |  19.3709  |        20   |        5 |       25 | True                      |
| cwhvm1_hw_dr_h  | CWHvm1_HW+DR   | H          |           133 |   949.517  |  31.7669  |        31   |       30 |       37 | True                      |
| cwhvm1_hw_ss_m  | CWHvm1_HW+SS   | M          |            73 |   928.458  |  29       |        29   |       29 |       29 | True                      |
| cwhvh1_cw_hw_m  | CWHvh1_CW+HW   | M          |           122 |   925.173  |  15.7213  |        16   |       15 |       16 | True                      |
| cwhvm1_hw_fdc_h | CWHvm1_HW+FDC  | H          |            51 |   888.765  |  30.902   |        30   |       29 |       39 | True                      |
| cwhvm2_hw_cw_m  | CWHvm2_HW+CW   | M          |           117 |   876.654  |  18.3504  |        18   |       16 |       21 | True                      |
| cwhvh1_hw_cw_h  | CWHvh1_HW+CW   | H          |            97 |   858.725  |  27.2268  |        28   |       24 |       40 | True                      |
| cwhvm1_hw_fd_h  | CWHvm1_HW+FD   | H          |            56 |   812.542  |  34.5714  |        33   |       31 |       45 | True                      |
| cwhvh1_hw_cw_l  | CWHvh1_HW+CW   | L          |           125 |   749.479  |  13.368   |        14   |        5 |       16 | True                      |
| cwhvm2_ba_hw_m  | CWHvm2_BA+HW   | M          |            62 |   737.725  |  25.5     |        26   |       23 |       26 | True                      |
| cwhvm1_cw_m     | CWHvm1_CW      | M          |           149 |   736.057  |  13.7584  |        14   |       12 |       16 | True                      |
| cwhvm2_hw_cw_l  | CWHvm2_HW+CW   | L          |           139 |   726.649  |  12.2158  |        12   |        5 |       15 | True                      |
| cwhvm1_hw_fd_m  | CWHvm1_HW+FD   | M          |            59 |   678.283  |  27.7119  |        28   |       25 |       30 | True                      |
| cwhvm1_dr_hw_h  | CWHvm1_DR+HW   | H          |           101 |   620.53   |  31.8515  |        30   |       27 |       47 | True                      |
| cwhvm1_yc_hw_l  | CWHvm1_YC+HW   | L          |            35 |   585.006  |   7.25714 |         7   |        5 |        9 | True                      |
| cwhvm1_ss_hw_h  | CWHvm1_SS+HW   | H          |            52 |   576.664  |  38.1538  |        37   |       35 |       51 | True                      |
| cwhvm1_cw_l     | CWHvm1_CW      | L          |           162 |   558.8    |   7.75926 |         8   |        2 |       11 | True                      |
| cwhvm2_cw_hw_h  | CWHvm2_CW+HW   | H          |            52 |   548.519  |  22.0577  |        21   |       19 |       30 | True                      |
| cwhvm1_ss_hw_l  | CWHvm1_SS+HW   | L          |            56 |   541.879  |  25.375   |        26.5 |       14 |       29 | True                      |
| cwhvm1_ss_hw_m  | CWHvm1_SS+HW   | M          |            49 |   519.51   |  32.0816  |        32   |       30 |       34 | True                      |
| cwhvm1_cw_yc_h  | CWHvm1_CW+YC   | H          |            66 |   485.666  |  19.0303  |        18.5 |       16 |       30 | True                      |
| cwhvh1_hw_ba_l  | CWHvh1_HW+BA   | L          |            81 |   467.414  |  14.6914  |        15   |        7 |       17 | True                      |
| cwhvm1_dr_hw_l  | CWHvm1_DR+HW   | L          |           128 |   463.173  |  19.3203  |        21   |        9 |       22 | True                      |
| cwhvm2_cw_hw_l  | CWHvm2_CW+HW   | L          |            63 |   408.992  |  11.6667  |        12   |        6 |       13 | True                      |
| cwhvm1_hw_fd_l  | CWHvm1_HW+FD   | L          |            67 |   401.314  |  18.2388  |        18   |        8 |       24 | True                      |
| cwhvm2_yc_hw_l  | CWHvm2_YC+HW   | L          |            49 |   398.83   |   9.55102 |        10   |        5 |       11 | True                      |
| cwhvm2_hw_yc_h  | CWHvm2_HW+YC   | H          |            52 |   387.205  |  26.6538  |        28   |       19 |       30 | True                      |
| cwhvh1_hw_ss_h  | CWHvh1_HW+SS   | H          |            40 |   376.076  |  29.6     |        30   |       28 |       33 | True                      |
| cwhvm1_yc_cw_l  | CWHvm1_YC+CW   | L          |            50 |   373.09   |   7.46    |         8   |        5 |        9 | True                      |
| cwhvh1_hw_ba_h  | CWHvh1_HW+BA   | H          |            59 |   372.648  |  25.2881  |        25   |       21 |       33 | True                      |
| cwhvm1_dr_hw_m  | CWHvm1_DR+HW   | M          |            96 |   354.077  |  24.0417  |        24   |       23 |       26 | True                      |
| cwhvm2_yc_hw_h  | CWHvm2_YC+HW   | H          |            37 |   351.524  |  19.6486  |        20   |       15 |       28 | True                      |
| cwhvm2_ba_hw_h  | CWHvm2_BA+HW   | H          |            37 |   350.789  |  28.1892  |        28   |       27 |       31 | True                      |
| cwhvm2_ba_hw_l  | CWHvm2_BA+HW   | L          |            58 |   345.036  |  16.1552  |        16   |        8 |       22 | True                      |
| cwhvm1_dr_l     | CWHvm1_DR      | L          |           112 |   342.369  |  18.9821  |        20   |       11 |       22 | True                      |
| cwhvh1_hw_cw_m  | CWHvh1_HW+CW   | M          |            69 |   339.507  |  18.971   |        18   |       17 |       23 | True                      |
| cwhvm1_ba_hw_h  | CWHvm1_BA+HW   | H          |            36 |   311.257  |  30.0556  |        30   |       27 |       36 | True                      |
| cwhvm1_dr_h     | CWHvm1_DR      | H          |            74 |   308.752  |  29.7162  |        29   |       26 |       37 | True                      |
| cwhvm1_yc_cw_m  | CWHvm1_YC+CW   | M          |            28 |   300.492  |  10.8214  |        11   |       10 |       12 | True                      |
| cwhvm1_cw_yc_m  | CWHvm1_CW+YC   | M          |            30 |   285.012  |  14.2     |        14.5 |       13 |       15 | True                      |
| cwhvm2_hw_yc_l  | CWHvm2_HW+YC   | L          |            64 |   282.434  |  10.5469  |        11   |        1 |       12 | True                      |
| cwhvm2_hw_yc_m  | CWHvm2_HW+YC   | M          |            33 |   265.215  |  14.7273  |        15   |       13 |       17 | True                      |
| cwhvh1_hw_ss_l  | CWHvh1_HW+SS   | L          |            49 |   265.088  |  15.4898  |        16   |        9 |       18 | True                      |
| cwhvm1_ba_hw_l  | CWHvm1_BA+HW   | L          |            47 |   255.663  |  17.8936  |        18   |       12 |       21 | True                      |
| cwhvh1_hw_ss_m  | CWHvh1_HW+SS   | M          |            34 |   246.655  |  22.3529  |        22   |       19 |       27 | True                      |
| cwhvm2_cw_hw_m  | CWHvm2_CW+HW   | M          |            45 |   242.938  |  15.4222  |        15   |       14 |       18 | True                      |
| cwhvm1_yc_cw_h  | CWHvm1_YC+CW   | H          |            35 |   217.136  |  17.6571  |        17   |       13 |       24 | True                      |
| cwhvm1_yc_hw_m  | CWHvm1_YC+HW   | M          |            24 |   202.047  |  11.6667  |        12   |       10 |       13 | True                      |
| cwhvh1_hw_ba_m  | CWHvh1_HW+BA   | M          |            32 |   140.891  |  18.875   |        19   |       18 |       20 | True                      |
| cwhvm1_yc_hw_h  | CWHvm1_YC+HW   | H          |            27 |   138.595  |  18.2222  |        19   |       14 |       28 | True                      |
| cwhvm1_dr_m     | CWHvm1_DR      | M          |            49 |   138.341  |  24.0204  |        24   |       23 |       25 | True                      |
| cwhvm1_ba_hw_m  | CWHvm1_BA+HW   | M          |            28 |   134.661  |  24.8929  |        25.5 |       22 |       26 | True                      |
| cwhvm2_yc_hw_m  | CWHvm2_YC+HW   | M          |            21 |    65.4031 |  12.5714  |        12   |       12 |       14 | True                      |
