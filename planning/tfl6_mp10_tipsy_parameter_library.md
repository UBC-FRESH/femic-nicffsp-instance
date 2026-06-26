# TFL 6 MP10 TIPSY Parameter Library Review

## Purpose

This note records the P3.4a extraction of MP10 Tables 27, 28, and 29 into a reviewed planning parameter library. It is not executable BatchTIPSY configuration and does not crosswalk the new static TFL 6 AUs.

## Source

- PDF: `reference/tfl_6_mngment_plan_2011_ip.pdf`
- Extracted text: `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt`
- Structured artifact: `planning/tfl6_mp10_tipsy_parameter_library.json`
- CSV review artifact: `planning/tfl6_mp10_tipsy_parameter_library.csv`

## Extracted Tables

| Source table | MP10 context | Row count |
| --- | --- | ---: |
| `mp10_table_27` | Existing managed stands aged 11-50 years; Section 8.6.3; no genetic gain applied. | 60 |
| `mp10_table_28` | Existing managed stands aged 1-10 years; Section 8.6.4; genetic worth applied for Cw/Cy/Fd/Hw where listed. | 16 |
| `mp10_table_29` | Future managed stands; Section 8.6.6; future silviculture strategies with AU footnotes retained. | 14 |
| **Total** |  | **90** |

## Accepted Field Semantics

- `legacy_au_code` preserves the MP10 AU code as a parameter/provenance key only.
- `legacy_au_footnote_marker` preserves superscript-style AU footnote markers from Table 29 where the text extraction attaches the marker to the AU code.
- `legacy_age_band_context` records whether a row came from the 11-50 existing managed, 1-10 existing managed, or future managed lane.
- Species percentage fields normalize dashes to `0` because absent species components are zero-share components in the table.
- Genetic worth fields normalize dashes to `0`; Table 27 rows are all `0` because MP10 states no genetic gain was applied to existing managed stands aged 11-50.
- `oaf1_pct = 10`, `oaf2_pct = 5`, and `utilization_dbh_cm = 12.5` are carried from MP10 Section 8.3 and Section 8.2 for managed stands.
- Table 29 regeneration delay is recorded as a note because Section 8.6.5 distinguishes one-year planted and three-year natural regeneration delays rather than a single numeric value per row.

## Extraction Caveats

- Dash values in species percentage and genetic worth columns are normalized to 0 in numeric fields.
- Table 27 has no genetic worth columns; genetic worth fields are set to 0 because MP10 states no genetic gain was applied to stands aged 11-50.
- Known text-extraction artifact in Table 27 row 1221 was repaired from a split THLB area token before parsing.
- Footnote markers attached to Table 29 AU codes are retained in legacy_au_footnote_marker.
- This artifact is a reviewed parameter library for planning/crosswalk work, not final executable BatchTIPSY YAML.

## Validation Checks

| Source table | Row count | Row-summed THLB ha | Printed total THLB ha | Delta ha | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| `mp10_table_27` | 60 | 47658 | 47655 | 3 | `accepted_small_rounding_or_extraction_delta` |
| `mp10_table_28` | 16 | 9945 | 9947 | -2 | `accepted_small_rounding_or_extraction_delta` |
| `mp10_table_29` | 14 | 107810 | 107811 | -1 | `accepted_small_rounding_or_extraction_delta` |

The small THLB-area deltas are accepted for P3.4a because MP10 row areas are printed as rounded whole hectares and Table 27 also required one known text-extraction repair. P3.4b should use the structured row values for crosswalk evidence and keep these deltas visible in review notes.

## Review Summary

The extracted library is acceptable for P3.4b crosswalk planning. P3.4b must still map the locked static TFL 6 AU universe to these MP10 parameter rows with confidence flags and fallback reasons before any BatchTIPSY curves are generated.

## Row Inventory

| Source table | Legacy AU | Footnote | Age/context | Initial SPH | Spaced SPH | THLB area ha | Notes |
| --- | ---: | --- | --- | ---: | ---: | ---: | --- |
| `mp10_table_27` | `0210` |  | `existing_managed_aged_11_50` | 900 |  | 178 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `0220` |  | `existing_managed_aged_11_50` | 900 |  | 184 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `0250` |  | `existing_managed_aged_11_50` | 900 |  | 772 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `0252` |  | `existing_managed_aged_11_50` | 1600 | 900 | 66 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `0260` |  | `existing_managed_aged_11_50` | 900 |  | 481 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `0262` |  | `existing_managed_aged_11_50` | 1600 | 900 | 50 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1210` |  | `existing_managed_aged_11_50` | 900 |  | 567 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1211` |  | `existing_managed_aged_11_50` | 900 |  | 45 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1220` |  | `existing_managed_aged_11_50` | 900 |  | 475 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1221` |  | `existing_managed_aged_11_50` | 900 |  | 430 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1230` |  | `existing_managed_aged_11_50` | 900 |  | 29 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1240` |  | `existing_managed_aged_11_50` | 900 |  | 256 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1241` |  | `existing_managed_aged_11_50` | 900 |  | 109 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1242` |  | `existing_managed_aged_11_50` | 1600 | 900 | 143 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1250` |  | `existing_managed_aged_11_50` | 900 |  | 17840 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1251` |  | `existing_managed_aged_11_50` | 900 |  | 1925 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1252` |  | `existing_managed_aged_11_50` | 1600 | 900 | 3660 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1260` |  | `existing_managed_aged_11_50` | 900 |  | 472 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `1262` |  | `existing_managed_aged_11_50` | 1600 | 900 | 58 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `2270` |  | `existing_managed_aged_11_50` | 900 |  | 128 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `3210` |  | `existing_managed_aged_11_50` | 900 |  | 103 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `3220` |  | `existing_managed_aged_11_50` | 900 |  | 150 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `3221` |  | `existing_managed_aged_11_50` | 900 |  | 167 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `3250` |  | `existing_managed_aged_11_50` | 900 |  | 2382 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `3251` |  | `existing_managed_aged_11_50` | 900 |  | 190 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `3252` |  | `existing_managed_aged_11_50` | 1600 | 900 | 229 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `3270` |  | `existing_managed_aged_11_50` | 900 |  | 71 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `4240` |  | `existing_managed_aged_11_50` | 900 |  | 120 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `4241` |  | `existing_managed_aged_11_50` | 900 |  | 59 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `4250` |  | `existing_managed_aged_11_50` | 900 |  | 104 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `5210` |  | `existing_managed_aged_11_50` | 900 |  | 626 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `5220` |  | `existing_managed_aged_11_50` | 900 |  | 204 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `5221` |  | `existing_managed_aged_11_50` | 900 |  | 42 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `5230` |  | `existing_managed_aged_11_50` | 900 |  | 168 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `5250` |  | `existing_managed_aged_11_50` | 900 |  | 2758 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `5251` |  | `existing_managed_aged_11_50` | 900 |  | 69 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `5252` |  | `existing_managed_aged_11_50` | 1600 | 900 | 263 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6210` |  | `existing_managed_aged_11_50` | 1200 |  | 47 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6220` |  | `existing_managed_aged_11_50` | 1200 |  | 2637 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6221` |  | `existing_managed_aged_11_50` | 1200 |  | 3398 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6230` |  | `existing_managed_aged_11_50` | 1200 |  | 68 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6240` |  | `existing_managed_aged_11_50` | 1200 |  | 43 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6250` |  | `existing_managed_aged_11_50` | 1200 |  | 1270 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6251` |  | `existing_managed_aged_11_50` | 1200 |  | 977 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6261` |  | `existing_managed_aged_11_50` | 1200 |  | 22 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `6270` |  | `existing_managed_aged_11_50` | 1200 |  | 54 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7220` |  | `existing_managed_aged_11_50` | 800 |  | 730 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7221` |  | `existing_managed_aged_11_50` | 800 |  | 715 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7250` |  | `existing_managed_aged_11_50` | 800 |  | 999 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7251` |  | `existing_managed_aged_11_50` | 800 |  | 266 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7252` |  | `existing_managed_aged_11_50` | 1600 | 900 | 64 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7260` |  | `existing_managed_aged_11_50` | 800 |  | 72 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7261` |  | `existing_managed_aged_11_50` | 800 |  | 36 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `7270` |  | `existing_managed_aged_11_50` | 800 |  | 95 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `8250` |  | `existing_managed_aged_11_50` | 800 |  | 129 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `8270` |  | `existing_managed_aged_11_50` | 800 |  | 48 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `9220` |  | `existing_managed_aged_11_50` | 800 |  | 108 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `9221` |  | `existing_managed_aged_11_50` | 800 |  | 35 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `9250` |  | `existing_managed_aged_11_50` | 800 |  | 256 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_27` | `9270` |  | `existing_managed_aged_11_50` | 800 |  | 16 | No genetic gain applied to stands in this age range; Table 27 row values are area-weighted averages by legacy AU. |
| `mp10_table_28` | `0110` |  | `existing_managed_aged_1_10` | 1100 |  | 194 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `0150` |  | `existing_managed_aged_1_10` | 1100 |  | 44 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `1110` |  | `existing_managed_aged_1_10` | 1100 |  | 24 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `1120` |  | `existing_managed_aged_1_10` | 1100 |  | 154 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `1150` |  | `existing_managed_aged_1_10` | 1100 |  | 5815 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `2120` |  | `existing_managed_aged_1_10` | 1100 |  | 15 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `3150` |  | `existing_managed_aged_1_10` | 1100 |  | 876 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `4140` |  | `existing_managed_aged_1_10` | 1100 |  | 384 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `5110` |  | `existing_managed_aged_1_10` | 1100 |  | 755 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `5150` |  | `existing_managed_aged_1_10` | 1100 |  | 153 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `6120` |  | `existing_managed_aged_1_10` | 1500 |  | 1078 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `6150` |  | `existing_managed_aged_1_10` | 1500 |  | 56 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `7120` |  | `existing_managed_aged_1_10` | 1000 |  | 304 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `7150` |  | `existing_managed_aged_1_10` | 1000 |  | 24 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `8170` |  | `existing_managed_aged_1_10` | 1000 |  | 21 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_28` | `9150` |  | `existing_managed_aged_1_10` | 1000 |  | 48 | Genetic worth values from table; Hw values reduced per table footnote where applicable. |
| `mp10_table_29` | `0500` |  | `future_managed` | 1100 |  | 3384 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `1500` | 2 | `future_managed` | 1100 |  | 41399 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `1510` |  | `future_managed` | 3000 |  | 17743 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `2500` |  | `future_managed` | 1100 |  | 276 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `3500` |  | `future_managed` | 1100 |  | 9375 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `4500` |  | `future_managed` | 1100 |  | 2619 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `5500` | 2 | `future_managed` | 1100 |  | 6742 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `5510` |  | `future_managed` | 2000 |  | 2889 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `6500` | 3 | `future_managed` | 1500 |  | 7810 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `6501` |  | `future_managed` | 1500 |  | 7810 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `7500` |  | `future_managed` | 1000 |  | 6109 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `8500` |  | `future_managed` | 1000 |  | 615 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `9500` | 2 | `future_managed` | 1000 |  | 727 | Future managed stand row; footnote markers on AU code retained where present. |
| `mp10_table_29` | `9510` |  | `future_managed` | 2000 |  | 312 | Future managed stand row; footnote markers on AU code retained where present. |
