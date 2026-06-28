# TFL 6 MP11 AU And Curve-Lane Crosswalk

## Purpose

This P10.3 artifact maps the stable FEMIC canonical AU universe to MP11
curve lanes and parameter gates. It preserves AU identity while making
natural, early managed, recent managed, future managed, fallback, and
parser-review status explicit.

It does not generate curves or promote rows to model-input status.

## Files

- `planning/tfl6_mp11_au_curve_lane_crosswalk.md`
- `planning/tfl6_mp11_au_curve_lane_crosswalk.csv`
- `planning/tfl6_mp11_au_curve_lane_crosswalk.json`

## Status

- Crosswalk rows: `1536`
- Canonical AU count: `384`
- Selected-top-90 row count: `308`
- Model-input status: `not_model_input`

## Curve Lane Counts

- `early_managed`: `384`
- `future_managed`: `384`
- `natural_unmanaged`: `384`
- `recent_managed`: `384`

## MP11 Parameter Status Counts

- `natural_curve_missing`: `108`
- `parser_review_required`: `1152`
- `public_vdyp_curve_available`: `276`

## Selected Top-90 Lane Summary

| curve_lane | mp11_parameter_status | rows |
| --- | --- | ---: |
| `early_managed` | `parser_review_required` | 77 |
| `future_managed` | `parser_review_required` | 77 |
| `natural_unmanaged` | `public_vdyp_curve_available` | 77 |
| `recent_managed` | `parser_review_required` | 77 |

## Use Boundary

- Natural lanes are handed to P10.4 for public VDYP curve diagnostics.
- Managed lanes for Tables 54, 55, and 57 remain
  `parser_review_required` until a reviewed per-AU row parser exists.
- MP10 fallback confidence is retained as comparison/fallback evidence,
  not as an MP11 replacement parameter.
- Treatment, operability, THLB status, and scenario membership are not
  canonical AU key dimensions.
- All rows remain `not_model_input` until Phase 11 promotion review.

## High-Area Selected Rows

| au_id | curve_lane | area_ha | species_combo | si_class | mp11_parameter_status | mp10_fallback_confidence |
| --- | --- | ---: | --- | --- | --- | --- |
| `cwhvm1_hw_cw_m` | `natural_unmanaged` | 14576.474 | `HW+CW` | `M` | `public_vdyp_curve_available` | `not_applicable` |
| `cwhvm1_hw_cw_m` | `early_managed` | 14576.474 | `HW+CW` | `M` | `parser_review_required` | `high` |
| `cwhvm1_hw_cw_m` | `recent_managed` | 14576.474 | `HW+CW` | `M` | `parser_review_required` | `medium` |
| `cwhvm1_hw_cw_m` | `future_managed` | 14576.474 | `HW+CW` | `M` | `parser_review_required` | `high` |
| `cwhvm1_hw_ba_m` | `natural_unmanaged` | 13083.871 | `HW+BA` | `M` | `public_vdyp_curve_available` | `not_applicable` |
| `cwhvm1_hw_ba_m` | `early_managed` | 13083.871 | `HW+BA` | `M` | `parser_review_required` | `high` |
| `cwhvm1_hw_ba_m` | `recent_managed` | 13083.871 | `HW+BA` | `M` | `parser_review_required` | `medium` |
| `cwhvm1_hw_ba_m` | `future_managed` | 13083.871 | `HW+BA` | `M` | `parser_review_required` | `high` |
| `cwhvm1_hw_cw_l` | `natural_unmanaged` | 7117.880 | `HW+CW` | `L` | `public_vdyp_curve_available` | `not_applicable` |
| `cwhvm1_hw_cw_l` | `early_managed` | 7117.880 | `HW+CW` | `L` | `parser_review_required` | `low` |
| `cwhvm1_hw_cw_l` | `recent_managed` | 7117.880 | `HW+CW` | `L` | `parser_review_required` | `high` |
| `cwhvm1_hw_cw_l` | `future_managed` | 7117.880 | `HW+CW` | `L` | `parser_review_required` | `low` |
| `cwhvm1_hw_ba_h` | `natural_unmanaged` | 6336.709 | `HW+BA` | `H` | `public_vdyp_curve_available` | `not_applicable` |
| `cwhvm1_hw_ba_h` | `early_managed` | 6336.709 | `HW+BA` | `H` | `parser_review_required` | `high` |
| `cwhvm1_hw_ba_h` | `recent_managed` | 6336.709 | `HW+BA` | `H` | `parser_review_required` | `high` |
| `cwhvm1_hw_ba_h` | `future_managed` | 6336.709 | `HW+BA` | `H` | `parser_review_required` | `high` |
| `cwhvm1_hw_ba_l` | `natural_unmanaged` | 6328.041 | `HW+BA` | `L` | `public_vdyp_curve_available` | `not_applicable` |
| `cwhvm1_hw_ba_l` | `early_managed` | 6328.041 | `HW+BA` | `L` | `parser_review_required` | `high` |
| `cwhvm1_hw_ba_l` | `recent_managed` | 6328.041 | `HW+BA` | `L` | `parser_review_required` | `high` |
| `cwhvm1_hw_ba_l` | `future_managed` | 6328.041 | `HW+BA` | `L` | `parser_review_required` | `high` |
