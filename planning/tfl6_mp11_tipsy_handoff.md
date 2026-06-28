# TFL 6 MP11 TIPSY Handoff Candidates

## Purpose

This P10R.3 artifact converts P10R.2 parser rows into conservative 
BatchTIPSY handoff candidates and row-level blocker diagnostics. It does 
not run curve-generation tools and does not promote any row to model input.

## Summary

- Parsed input rows: `141`
- Handoff candidate rows: `27`
- Handoff CSV: `planning\tfl6_mp11_tipsy_handoff.csv`
- Handoff map CSV: `planning\tfl6_mp11_tipsy_handoff_map.csv`

## Status Counts

| source_table | handoff_status | row_count |
| --- | --- | --- |
| Table 54 | blocked_missing_public_au_to_bec_mapping | 73 |
| Table 54 | review_required_parser_warning | 6 |
| Table 55 | blocked_missing_public_au_to_bec_mapping | 32 |
| Table 55 | review_required_parser_warning | 2 |
| Table 57 | candidate_for_curve_generation | 27 |
| Table 57 | review_required_parser_warning | 1 |

## Candidate Policy

- OAF: MP11 narrative OAF defaults: OAF1=15% and OAF2=5%, emitted as BTC factors 0.85 and 0.95.
- Regeneration delay: Future managed candidate rows use one-year regeneration delay from MP11 Section 8.2.7.1.
- Join boundary: Table 57 rows can produce standalone future-managed curve-generation candidates. Tables 54/55 remain blocked pending a public MP11 existing/recent AU-code to BEC/site-series mapping before BatchTIPSY handoff.

## Candidate Rows

| feature_id | mp11_au_code | curve_lane | bec_zone | bec_subzone | sph | species_percent_total | thlb_area_ha | handoff_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 611143 | Fvh101 | future_managed | CWH | vh | 1200 | 100 | 1604 | candidate_for_curve_generation |
| 611153 | Fvh103 | future_managed | CWH | vh | 1200 | 100 | 294 | candidate_for_curve_generation |
| 611163 | Fvh104 | future_managed | CWH | vh | 1200 | 100 | 3871 | candidate_for_curve_generation |
| 611173 | Fvh104s | future_managed | CWH | vh | 1200 | 100 | 2751 | candidate_for_curve_generation |
| 611183 | Fvh106 | future_managed | CWH | vh | 1200 | 100 | 781 | candidate_for_curve_generation |
| 611193 | Fvh108 | future_managed | CWH | vh | 1200 | 100 | 57 | candidate_for_curve_generation |
| 611203 | Fvh113 | future_managed | CWH | vh | 1200 | 100 | 508 | candidate_for_curve_generation |
| 611213 | Fvm101 | future_managed | CWH | vm | 1200 | 100 | 62618 | candidate_for_curve_generation |
| 611223 | Fvm101s | future_managed | CWH | vm | 1200 | 100 | 11015 | candidate_for_curve_generation |
| 611233 | Fvm103 | future_managed | CWH | vm | 1200 | 100 | 3659 | candidate_for_curve_generation |
| 611243 | Fvm104 | future_managed | CWH | vm | 1200 | 100 | 298 | candidate_for_curve_generation |
| 611253 | Fvm105 | future_managed | CWH | vm | 1200 | 100 | 10206 | candidate_for_curve_generation |
| 611263 | Fvm106 | future_managed | CWH | vm | 1200 | 100 | 125 | candidate_for_curve_generation |
| 611273 | Fvm106s | future_managed | CWH | vm | 1200 | 100 | 336 | candidate_for_curve_generation |
| 611283 | Fvm107 | future_managed | CWH | vm | 1200 | 100 | 1298 | candidate_for_curve_generation |
| 611293 | Fvm109 | future_managed | CWH | vm | 1200 | 100 | 388 | candidate_for_curve_generation |
| 611303 | Fvm111 | future_managed | CWH | vm | 1200 | 100 | 75 | candidate_for_curve_generation |
| 611313 | Fvm114 | future_managed | CWH | vm | 1200 | 100 | 3158 | candidate_for_curve_generation |
| 611323 | Fvm131 | future_managed | CWH | vm | 800 | 100 | 75 | candidate_for_curve_generation |
| 611333 | Fvm133 | future_managed | CWH | vm | 800 | 100 | 49 | candidate_for_curve_generation |
| 611343 | Fvm201 | future_managed | CWH | vm | 1200 | 100 | 14134 | candidate_for_curve_generation |
| 611353 | Fvm203 | future_managed | CWH | vm | 1200 | 100 | 890 | candidate_for_curve_generation |
| 611373 | Fvm207 | future_managed | CWH | vm | 1200 | 100 | 70 | candidate_for_curve_generation |
| 611383 | Fvm208 | future_managed | CWH | vm | 1200 | 100 | 192 | candidate_for_curve_generation |
| 611393 | Fvm211 | future_managed | CWH | vm | 1200 | 100 | 245 | candidate_for_curve_generation |
| 611403 | FMH01 | future_managed | MH | mm | 1200 | 100 | 939 | candidate_for_curve_generation |
| 611413 | FMH22 | future_managed | MH | mm | 800 | 100 | 216 | candidate_for_curve_generation |

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
