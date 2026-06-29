# TFL 6 MP11 Natural-Curve Diagnostics

## Purpose

This P10.4 artifact repackages the accepted Phase 3/5 public VDYP
first-growth evidence as an MP11 natural-curve diagnostic surface.
It does not rerun VDYP, change curve values, generate managed curves,
or promote any row to model-input status.

## Files

- `planning/tfl6_mp11_natural_curve_diagnostics.md`
- `planning/tfl6_mp11_natural_curve_diagnostics.csv`
- `planning/tfl6_mp11_natural_curve_diagnostics.json`

## Status

- Diagnostic rows: `384`
- Canonical AU count: `384`
- Selected top-90 rows: `77`
- Existing plot references: `77`
- Model-input status: `not_model_input`

## Natural Curve Status Counts

- `remapped_to_selected_curve_family`: `307`
- `selected_curve_family_available`: `77`

## Use Boundary

- The `77` selected top-area AU curve families remain the Phase 5 public
  natural-curve baseline for MP11 comparison.
- Non-AU source stratum bins remain remapped through the existing lexicographic
  remap audit rather than becoming new hidden curve families.
- Missing/raw-not-selected statuses are diagnostics for review, not model
  input failures by themselves.
- Phase 11 must explicitly promote any natural-curve surface before model
  input or XML rebuild work consumes it.

## High-Area Diagnostic Rows

| au_id | area_ha | species_combo | si_class | natural_curve_status | canonical_curve_au_id | max_volume | plot_count |
| --- | ---: | --- | --- | --- | --- | ---: | ---: |
| `cwhvm1_hw_cw_m` | 14576.474 | `HW+CW` | `M` | `selected_curve_family_available` | `cwhvm1_hw_cw_m` | 1049.390 | 1 |
| `cwhvm1_hw_ba_m` | 13083.871 | `HW+BA` | `M` | `selected_curve_family_available` | `cwhvm1_hw_ba_m` | 1085.130 | 1 |
| `cwhvm1_hw_cw_l` | 7117.880 | `HW+CW` | `L` | `selected_curve_family_available` | `cwhvm1_hw_cw_l` | 833.555 | 1 |
| `cwhvm1_hw_ba_h` | 6336.709 | `HW+BA` | `H` | `selected_curve_family_available` | `cwhvm1_hw_ba_h` | 1140.602 | 1 |
| `cwhvm1_hw_ba_l` | 6328.041 | `HW+BA` | `L` | `selected_curve_family_available` | `cwhvm1_hw_ba_l` | 896.690 | 1 |
| `cwhvm1_cw_hw_h` | 6154.404 | `CW+HW` | `H` | `selected_curve_family_available` | `cwhvm1_cw_hw_h` | 943.689 | 1 |
| `cwhvm1_cw_hw_l` | 6107.944 | `CW+HW` | `L` | `selected_curve_family_available` | `cwhvm1_cw_hw_l` | 783.068 | 1 |
| `cwhvm1_hw_m` | 4138.939 | `HW` | `M` | `selected_curve_family_available` | `cwhvm1_hw_m` | 961.763 | 1 |
| `cwhvm1_hw_ss_l` | 4135.639 | `HW+SS` | `L` | `selected_curve_family_available` | `cwhvm1_hw_ss_l` | 1057.283 | 1 |
| `cwhvm1_cw_hw_m` | 4015.120 | `CW+HW` | `M` | `selected_curve_family_available` | `cwhvm1_cw_hw_m` | 830.562 | 1 |
| `cwhvm2_hw_ba_h` | 3577.020 | `HW+BA` | `H` | `selected_curve_family_available` | `cwhvm2_hw_ba_h` | 1110.072 | 1 |
| `cwhvm2_hw_ba_l` | 3095.371 | `HW+BA` | `L` | `selected_curve_family_available` | `cwhvm2_hw_ba_l` | 920.312 | 1 |
| `cwhvm1_hw_cw_h` | 2899.431 | `HW+CW` | `H` | `selected_curve_family_available` | `cwhvm1_hw_cw_h` | 1191.464 | 1 |
| `cwhvm2_hw_ba_m` | 2418.082 | `HW+BA` | `M` | `selected_curve_family_available` | `cwhvm2_hw_ba_m` | 1005.364 | 1 |
| `cwhvm1_hw_ss_h` | 2240.218 | `HW+SS` | `H` | `selected_curve_family_available` | `cwhvm1_hw_ss_h` | 1185.820 | 1 |
| `cwhvm1_hw_h` | 1645.047 | `HW` | `H` | `selected_curve_family_available` | `cwhvm1_hw_h` | 1022.038 | 1 |
| `cwhvm1_hw_l` | 1582.405 | `HW` | `L` | `selected_curve_family_available` | `cwhvm1_hw_l` | 736.515 | 1 |
| `cwhvm1_cw_h` | 1331.281 | `CW` | `H` | `selected_curve_family_available` | `cwhvm1_cw_h` | 964.985 | 1 |
| `cwhvm1_cw_yc_l` | 1293.870 | `CW+YC` | `L` | `selected_curve_family_available` | `cwhvm1_cw_yc_l` | 808.724 | 1 |
| `cwhvm1_hw_fdc_l` | 1288.935 | `HW+FDC` | `L` | `selected_curve_family_available` | `cwhvm1_hw_fdc_l` | 1153.231 | 1 |
| `cwhvm1_hw_dr_m` | 1157.285 | `HW+DR` | `M` | `selected_curve_family_available` | `cwhvm1_hw_dr_m` | 841.233 | 1 |
| `cwhvm2_hw_cw_h` | 1136.408 | `HW+CW` | `H` | `selected_curve_family_available` | `cwhvm2_hw_cw_h` | 988.679 | 1 |
| `cwhvh1_cw_hw_l` | 1104.143 | `CW+HW` | `L` | `selected_curve_family_available` | `cwhvh1_cw_hw_l` | 613.123 | 1 |
| `cwhvh1_cw_hw_h` | 1076.780 | `CW+HW` | `H` | `selected_curve_family_available` | `cwhvh1_cw_hw_h` | 797.605 | 1 |
| `cwhvm1_hw_dr_l` | 983.327 | `HW+DR` | `L` | `selected_curve_family_available` | `cwhvm1_hw_dr_l` | 740.151 | 1 |
