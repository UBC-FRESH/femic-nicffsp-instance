# TFL 6 MP11 TIPSY Row Parse

## Purpose

This P10R.2 artifact parses the public MP11 per-AU TIPSY input tables 
needed before managed-curve handoff work. It is a parser-candidate 
surface only; rows remain `not_model_input` until later P10R gates 
join them to AU/curve lanes and generate/review curves.

## Source

- Source package: `tfl6_mp11_202606_public_pdf`
- Source SHA256: `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- Source tables: Table 54, Table 55, Table 57
- Method: PyMuPDF `find_tables()` plus conservative continuation-row assembly

## Summary

- Parsed rows: `141`
- `Table 54` (early_managed): `79` rows from PDF pages `358-364`
- `Table 55` (recent_managed): `34` rows from PDF pages `365-370`
- `Table 57` (future_managed): `28` rows from PDF pages `372-375`

## QA Status

Rows with `parse_confidence = review_required` need manual review before 
BatchTIPSY/TIPSY handoff. Common causes are PDF line wrapping, split 
species percentages, missing THLB area cells, or species percentages 
that do not sum near 100 after reconstruction.

### Confidence Counts

| source_table | parse_confidence | row_count |
| --- | --- | --- |
| Table 54 | high | 73 |
| Table 54 | review_required | 6 |
| Table 55 | high | 32 |
| Table 55 | review_required | 2 |
| Table 57 | high | 27 |
| Table 57 | review_required | 1 |

### Representative Rows

| source_table | au_code | sph | species_composition_raw | spp1_si | spp2_si | spp3_si | productive_area_ha | thlb_area_ha | parse_confidence | parser_warnings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Table 54 | E100 | 900 | hw55 ba17 ss10 dr10 cw8 | 26.1 |  |  | 8 | 5 | high |  |
| Table 54 | E101 | 900 | cw46 hw33 yc14 ba6 dr1 | 16.0 | 16.0 | 16.0 | 109 | 85 | high |  |
| Table 54 | E101F | 900 | cw67 hw20 yc12 ba1 | 16.0 | 16.0 | 16.0 | 132 | 119 | high |  |
| Table 54 | E103 | 900 | hw50 cw26 ss13 ba8 dr3 | 12.0 | 12.0 | 10.0 | 41 | 35 | high |  |
| Table 54 | E104 | 900 | hw63 cw17 ss9 ba8 dr3 fd2 | 24.0 | 20.0 | 24.0 | 1343 | 1067 | high |  |
| Table 54 | E104F | 900 | hw54 cw35 ba6 ss3 yc2 dr2 | 24.0 | 20.0 | 24.0 | 578 | 503 | high |  |
| Table 54 | E104S | 1600 | hw79 ss7 cw7 ba5 dr2 | 24.0 | 24.0 | 20.0 | 139 | 118 | high |  |
| Table 54 | E104sc | 900 | cw69 hw19 fd4 ss4 dr4 yc3 | 20.0 | 24.0 | 27.1 | 246 | 176 | review_required | species_percent_total_not_near_100 |
| Table 54 | E104scF | 900 | cw79 hw17 yc2 dr1 ss1 | 20.0 | 24.0 | 20.0 | 676 | 597 | high |  |
| Table 54 | E104sh | 900 | hw72 cw14 ss6 dr5 ba3 fd3 | 24.0 | 20.0 | 24.0 | 179 | 142 | review_required | species_percent_total_not_near_100 |
| Table 54 | E104shF | 900 | hw68 cw21 ss5 dr4 yc2 ba1 | 24.0 | 20.0 | 24.0 | 236 | 201 | high |  |
| Table 54 | E106c | 900 | cw78 hw15 ss5 yc1 ba1 | 24.0 | 24.0 | 32.0 | 113 | 69 | high |  |
| Table 54 | E106h | 900 | hw63 dr18 cw9 ba5 ss5 | 24.0 | 24.0 | 24.0 | 362 | 158 | high |  |
| Table 54 | E106s | 900 | ss64 hw24 cw8 ba3 dr1 | 32.0 | 24.0 | 24.0 | 111 | 69 | high |  |
| Table 54 | E108 | 900 | ss30 hw28 cw20 dr20 ba2 | 28.0 | 28.0 | 24.0 | 93 | 20 | high |  |
| Table 54 | E110 | 900 | dr49 hw37 cw7 ss7 | 21.2 |  |  | 24 | 1 | high |  |
| Table 54 | E113 | 900 | cw35 hw34 ss22 dr5 ba4 | 16.0 | 16.0 | 20.0 | 147 | 80 | high |  |
| Table 54 | E113F | 900 | cw63 hw25 ss9 dr2 ba1 | 16.0 | 16.0 | 20.0 | 100 | 70 | high |  |
| Table 54 | E200 | 900 | hw61 ba13 cw12 dr10 ss4 fd3 | 25.4 |  |  | 351 | 215 | review_required | species_percent_total_not_near_100 |
| Table 54 | E200F | 900 | hw46 ss35 cw9 fd9 ba1 | 28.3 |  |  | 14 | 10 | high |  |
| Table 54 | E201b | 900 | ba60 hw20 cw10 ss6 fd4 yc2 | 29.1 | 27.7 | 22.6 | 849 | 735 | high |  |
| Table 54 | E201c | 900 | cw69 hw24 fd4 ba2 yc1 dr1 | 22.6 | 27.7 | 35.8 | 1263 | 991 | high |  |
| Table 54 | E201cF | 900 | cw73 hw23 fd2 yc1 ba1 | 22.6 | 27.7 | 35.8 | 708 | 604 | high |  |
| Table 54 | E201d | 900 | dr86 hw12 ss1 cw1 | 23.2 | 27.7 | 30.8 | 491 | - | high |  |
| Table 54 | E201f | 900 | fd66 hw23 cw6 ss3 ba2 pl1 | 35.8 | 27.7 | 22.6 | 733 | 577 | high |  |

## Use Boundary

- Do not promote these rows directly to model inputs.
- P10R.3 must join rows to the AU/curve-lane crosswalk and resolve 
  parser warnings.
- P10R.4 must capture the curve-generation toolchain before any 
  generated curve can become an accepted candidate.
