# TFL 6 P3.4e BatchTIPSY Handoff Manifest

## Purpose

This P3.4e artifact converts the selected top-area TFL 6 AU/MP10 TIPSY
crosswalk into the canonical BTC `03_input-tfl6.csv` handoff. It does
not run `TIPSYbtc.exe`, parse `04_output`, write the model-input bundle,
or emit Patchworks runtime files.

## Outputs

- BTC input CSV: `data/03_input-tfl6.csv`
- Curve ID map: `planning/tfl6_tipsy_btc_curve_id_map.csv`
- Rows: `231`
- Selected AUs: `77`
- Curve lanes per AU: `3`

## Translation Policies

- Feature IDs: 600000 + selected_AU_area_rank * 10 + lane_code.
- OAF: MP10 percent reductions are converted to BTC factors.
- Regen delay: Use first numeric MP10 delay where present; otherwise existing-managed lanes use 0 and future-managed uses 1.
- Other species: MP10 other species share is encoded as Dr for this executable review handoff and flagged in the curve-id map. If the matched MP10 row has no deciduous/other site-index value, the static TFL 6 AU mean SI is used as the BTC Dr SI fallback.
- Planted percent: Rows are emitted as 100 percent planted/managed because the reviewed MP10 rows provide one managed species composition; the MP10 future row text is treated as delay context, not planted-area proportion.

## Confidence Counts

| curve_lane             |   fallback_review_required |   high |   low |   medium |
|:-----------------------|---------------------------:|-------:|------:|---------:|
| existing_managed_11_50 |                         12 |     34 |     8 |       23 |
| existing_managed_1_10  |                         11 |     19 |    15 |       32 |
| future_managed         |                         11 |     11 |    19 |       36 |

## Largest Handoff Rows

|   feature_id | au_id          | curve_lane             |   area_ha |   matched_legacy_au_code | match_confidence   |   other_species_pct_encoded_as_dr |
|-------------:|:---------------|:-----------------------|----------:|-------------------------:|:-------------------|----------------------------------:|
|       600013 | cwhvm1_hw_cw_m | future_managed         |  14576.5  |                     1500 | high               |                                 0 |
|       600011 | cwhvm1_hw_cw_m | existing_managed_11_50 |  14576.5  |                     6251 | high               |                                 0 |
|       600012 | cwhvm1_hw_cw_m | existing_managed_1_10  |  14576.5  |                     7150 | medium             |                                 0 |
|       600022 | cwhvm1_hw_ba_m | existing_managed_1_10  |  13083.9  |                     6150 | medium             |                                 0 |
|       600023 | cwhvm1_hw_ba_m | future_managed         |  13083.9  |                     1510 | high               |                                 0 |
|       600021 | cwhvm1_hw_ba_m | existing_managed_11_50 |  13083.9  |                     5250 | high               |                                 0 |
|       600031 | cwhvm1_hw_cw_l | existing_managed_11_50 |   7117.88 |                     6251 | low                |                                 0 |
|       600033 | cwhvm1_hw_cw_l | future_managed         |   7117.88 |                     1500 | low                |                                 0 |
|       600032 | cwhvm1_hw_cw_l | existing_managed_1_10  |   7117.88 |                     7150 | high               |                                 0 |
|       600041 | cwhvm1_hw_ba_h | existing_managed_11_50 |   6336.71 |                     5250 | high               |                                 0 |
|       600042 | cwhvm1_hw_ba_h | existing_managed_1_10  |   6336.71 |                     0150 | high               |                                 0 |
|       600043 | cwhvm1_hw_ba_h | future_managed         |   6336.71 |                     1510 | high               |                                 0 |
|       600051 | cwhvm1_hw_ba_l | existing_managed_11_50 |   6328.04 |                     9250 | high               |                                 0 |
|       600052 | cwhvm1_hw_ba_l | existing_managed_1_10  |   6328.04 |                     6150 | high               |                                 0 |
|       600053 | cwhvm1_hw_ba_l | future_managed         |   6328.04 |                     9510 | high               |                                 0 |
|       600063 | cwhvm1_cw_hw_h | future_managed         |   6154.4  |                     7500 | medium             |                                 0 |
|       600061 | cwhvm1_cw_hw_h | existing_managed_11_50 |   6154.4  |                     1220 | high               |                                 0 |
|       600062 | cwhvm1_cw_hw_h | existing_managed_1_10  |   6154.4  |                     1120 | high               |                                 0 |
|       600073 | cwhvm1_cw_hw_l | future_managed         |   6107.94 |                     7500 | medium             |                                 0 |
|       600071 | cwhvm1_cw_hw_l | existing_managed_11_50 |   6107.94 |                     6220 | medium             |                                 0 |

## Review Boundary

The handoff is executable input for BTC review, but it is not yet accepted
treated-yield output. P3.4e still needs the BTC run, parsed output,
TIPSY/VDYP overlay diagnostics, and row-level review of low-confidence or
`other`-species rows before Phase 3 can move from curve construction to
treatment-option design.
