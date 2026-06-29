# TFL 6 MP11 TIPSY Handoff Candidates

## Purpose

This P10R.3 artifact converts P10R.2 parser rows into conservative 
BatchTIPSY handoff candidates and row-level blocker diagnostics. It does 
not run curve-generation tools and does not promote any row to model input.

## Summary

- Parsed input rows: `141`
- Handoff candidate rows: `25`
- Handoff CSV: `planning\tfl6_mp11_tipsy_handoff.csv`
- Handoff map CSV: `planning\tfl6_mp11_tipsy_handoff_map.csv`

## Status Counts

| source_table | handoff_status | row_count |
| --- | --- | --- |
| Table 54 | blocked_missing_public_au_to_bec_mapping | 73 |
| Table 54 | review_required_parser_warning | 6 |
| Table 55 | blocked_missing_public_au_to_bec_mapping | 32 |
| Table 55 | review_required_parser_warning | 2 |
| Table 57 | blocked_no_canonical_top_n_au_for_bec | 2 |
| Table 57 | candidate_for_curve_generation | 25 |
| Table 57 | review_required_parser_warning | 1 |

## Candidate Policy

- OAF: MP11 narrative OAF defaults: OAF1=15% and OAF2=5%, emitted as BTC factors 0.85 and 0.95.
- Regeneration delay: Future managed candidate rows use one-year regeneration delay from MP11 Section 8.2.7.1.
- Site index: Candidate BTC rows use the matched canonical top-N AU VRI median SI as the TIPSY site-index input for every planted species SI column. Parsed MP11 per-species SI values are retained only as provenance.
- Join boundary: Table 57 rows can produce standalone future-managed curve-generation candidates. They must first map to a canonical top-N FEMIC AU. Tables 54/55 remain blocked pending a public MP11 existing/recent AU-code to BEC/site-series mapping before BatchTIPSY handoff.

## Candidate Rows

| feature_id | mp11_au_code | curve_lane | bec_zone | bec_subzone | canonical_au_id | canonical_median_si | mp11_parsed_weighted_si | tipsy_input_si | canonical_median_si_abs_diff | sph | species_percent_total | thlb_area_ha | handoff_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 611143 | Fvh101 | future_managed | CWH | vh | cwhvh1_cw_hw_m | 16.0 | 16.0 | 16.0 | 0.0 | 1200 | 100 | 1604 | candidate_for_curve_generation |
| 611153 | Fvh103 | future_managed | CWH | vh | cwhvh1_cw_hw_l | 13.0 | 8.495 | 13.0 | 4.505 | 1200 | 100 | 294 | candidate_for_curve_generation |
| 611163 | Fvh104 | future_managed | CWH | vh | cwhvh1_hw_ss_m | 22.0 | 21.6 | 22.0 | 0.4 | 1200 | 100 | 3871 | candidate_for_curve_generation |
| 611173 | Fvh104s | future_managed | CWH | vh | cwhvh1_cw_hw_h | 20.0 | 20.6 | 20.0 | 0.6 | 1200 | 100 | 2751 | candidate_for_curve_generation |
| 611183 | Fvh106 | future_managed | CWH | vh | cwhvh1_hw_ba_h | 25.0 | 24.4 | 25.0 | 0.6 | 1200 | 100 | 781 | candidate_for_curve_generation |
| 611193 | Fvh108 | future_managed | CWH | vh | cwhvh1_hw_cw_h | 28.0 | 26.8 | 28.0 | 1.2 | 1200 | 100 | 57 | candidate_for_curve_generation |
| 611203 | Fvh113 | future_managed | CWH | vh | cwhvh1_cw_hw_m | 16.0 | 16.0 | 16.0 | 0.0 | 1200 | 100 | 508 | candidate_for_curve_generation |
| 611213 | Fvm101 | future_managed | CWH | vm | cwhvm1_hw_cw_m | 28.0 | 28.015 | 28.0 | 0.015 | 1200 | 100 | 62618 | candidate_for_curve_generation |
| 611223 | Fvm101s | future_managed | CWH | vm | cwhvm1_cw_hw_h | 23.0 | 23.365 | 23.0 | 0.365 | 1200 | 100 | 11015 | candidate_for_curve_generation |
| 611233 | Fvm103 | future_managed | CWH | vm | cwhvm2_yc_hw_h | 20.0 | 20.33 | 20.0 | 0.33 | 1200 | 100 | 3659 | candidate_for_curve_generation |
| 611243 | Fvm104 | future_managed | CWH | vm | cwhvm1_ba_hw_m | 25.5 | 25.24 | 25.5 | 0.26 | 1200 | 100 | 298 | candidate_for_curve_generation |
| 611253 | Fvm105 | future_managed | CWH | vm | cwhvm1_hw_ss_m | 29.0 | 29.39 | 29.0 | 0.39 | 1200 | 100 | 10206 | candidate_for_curve_generation |
| 611263 | Fvm106 | future_managed | CWH | vm | cwhvm1_ba_hw_m | 25.5 | 24.385 | 25.5 | 1.115 | 1200 | 100 | 125 | candidate_for_curve_generation |
| 611273 | Fvm106s | future_managed | CWH | vm | cwhvm1_cw_hw_h | 23.0 | 23.585 | 23.0 | 0.585 | 1200 | 100 | 336 | candidate_for_curve_generation |
| 611283 | Fvm107 | future_managed | CWH | vm | cwhvm1_hw_dr_h | 31.0 | 30.675 | 31.0 | 0.325 | 1200 | 100 | 1298 | candidate_for_curve_generation |
| 611293 | Fvm109 | future_managed | CWH | vm | cwhvm1_hw_ss_l | 27.0 | 27.08 | 27.0 | 0.08 | 1200 | 100 | 388 | candidate_for_curve_generation |
| 611303 | Fvm111 | future_managed | CWH | vm | cwhvm1_hw_ss_m | 29.0 | 29.38 | 29.0 | 0.38 | 1200 | 100 | 75 | candidate_for_curve_generation |
| 611313 | Fvm114 | future_managed | CWH | vm | cwhvm2_yc_hw_h | 20.0 | 19.758 | 20.0 | 0.242 | 1200 | 100 | 3158 | candidate_for_curve_generation |
| 611323 | Fvm131 | future_managed | CWH | vm | cwhvm1_hw_dr_l | 20.0 | 20.022 | 20.0 | 0.022 | 800 | 100 | 75 | candidate_for_curve_generation |
| 611333 | Fvm133 | future_managed | CWH | vm | cwhvm1_cw_hw_m | 19.0 | 19.81 | 19.0 | 0.81 | 800 | 100 | 49 | candidate_for_curve_generation |
| 611343 | Fvm201 | future_managed | CWH | vm | cwhvm1_cw_hw_h | 23.0 | 24.12 | 23.0 | 1.12 | 1200 | 100 | 14134 | candidate_for_curve_generation |
| 611353 | Fvm203 | future_managed | CWH | vm | cwhvm1_hw_cw_l | 16.0 | 15.56 | 16.0 | 0.44 | 1200 | 100 | 890 | candidate_for_curve_generation |
| 611373 | Fvm207 | future_managed | CWH | vm | cwhvm2_hw_cw_h | 26.0 | 26.4 | 26.0 | 0.4 | 1200 | 100 | 70 | candidate_for_curve_generation |
| 611383 | Fvm208 | future_managed | CWH | vm | cwhvm2_hw_cw_h | 26.0 | 26.4 | 26.0 | 0.4 | 1200 | 100 | 192 | candidate_for_curve_generation |
| 611393 | Fvm211 | future_managed | CWH | vm | cwhvm1_hw_cw_l | 16.0 | 15.78 | 16.0 | 0.22 | 1200 | 100 | 245 | candidate_for_curve_generation |

## Blocked Or Review-Required Rows

| mp11_au_code | source_table | curve_lane | parse_confidence | handoff_status | handoff_note |
| --- | --- | --- | --- | --- | --- |
| E100 | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E101 | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E101F | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E103 | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E104 | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E104F | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E104S | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E104sc | Table 54 | early_managed | review_required | review_required_parser_warning | species_percent_total_not_near_100 |
| E104scF | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E104sh | Table 54 | early_managed | review_required | review_required_parser_warning | species_percent_total_not_near_100 |
| E104shF | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E106c | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E106h | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E106s | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E108 | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E110 | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E113 | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E113F | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E200 | Table 54 | early_managed | review_required | review_required_parser_warning | species_percent_total_not_near_100 |
| E200F | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201b | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201c | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201cF | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201d | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201f | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201fF | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201fS | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201h | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201hF | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |
| E201hFS | Table 54 | early_managed | high | blocked_missing_public_au_to_bec_mapping | Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff. |

## Use Boundary

- All rows remain `not_model_input`.
- P10R.4 may run only the candidate rows unless a maintainer accepts a 
  repair or mapping for blocked rows.
- Existing and recent managed rows require a public MP11 AU-code to 
  BEC/site-series mapping before curve generation.
