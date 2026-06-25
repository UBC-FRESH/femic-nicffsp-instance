# TFL 6 THLB Netdown Steps

## Purpose

This note converts the TFL 6 Management Plan 10 information-package land-base
section into a reviewed, ordered THLB netdown planning table. It bridges
`planning/tfl6_2011_document_review.md` and a later non-executable recipe
skeleton.

Governing issue: `#7`.

No recipe YAML is created here and no netdown execution is authorized.

## Source Authority

Primary source:

- `reference/tfl_6_mngment_plan_2011_ip.pdf`
- extracted text: `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt`

Authoritative netdown backbone:

- Information Package Section 6.2, `Table 4 - Timber Harvesting Land Base for
  TFL 6`, printed page 12, extracted-text page 21.

Supporting detail:

- Section 6.3 / Table 5: non-forest.
- Section 6.4 / Table 6: existing roads.
- Section 6.5 / Table 7: non-productive forest.
- Section 6.6 / Table 8: operability.
- Section 6.7 / Table 9: riparian management.
- Section 6.8 / Table 10: ungulate winter ranges.
- Section 6.9 / Table 11: old growth management areas.
- Section 6.10 / Table 12: wildlife habitat areas.
- Section 6.11 / Table 13: recreation sites and trails.
- Section 6.12 / Table 14: deciduous-leading forest.
- Section 6.13 / Table 15: cultural heritage resources.
- Section 6.14.3 / Table 16: stand-level retention.
- Section 6.15 / Table 17: future roads.
- Section 6.16: caves and karst.

The information package says the detailed sections summarize the area deducted
from the land base in the order the categories appear in Table 4 and that
overlapping constraints are addressed in a hierarchy. That Table 4 order is the
governing order for this planning skeleton.

## Stage Mapping

TFL 6 MP10 does not use the TSA29 GLB/AFLB/LHLB/THLB labels directly. FEMIC
should preserve the literal MP10 Table 4 rows and add this tentative stage
interpretation for review:

| FEMIC stage | TFL 6 interpretation | Source-status note |
| --- | --- | --- |
| GLB | Total MP10 analysis landbase. | Source wording: `Total Landbase`. |
| GLB -> AFLB | Remove non-forest, existing roads, and non-productive forest to reach productive forest. | Review interpretation, not MP10 wording. |
| AFLB | Productive forest checkpoint. | Source wording: `Total Productive`. |
| AFLB -> LHLB | Remove inoperable/uneconomic area to reach operable landbase. | Review interpretation: MP10 calls this `Total Operable`, not LHLB. |
| LHLB | Operable landbase before ordered resource reductions. | Source wording: `Total Operable`. |
| LHLB -> THLB | Apply ordered operable reductions and stand-level retention to reach current THLB. | Review interpretation; literal source rows are the Table 4 reductions. |
| THLB | Current timber harvesting land base. | Source wording: `Current THLB`. |
| Long-term THLB/LHLB adjustment | Deduct future roads to reach long-term landbase. | Source wording: `Long-term Landbase`; not part of current THLB. |

This mapping should be revisited during P1.7c before any recipe schema is
promoted, because some deductions such as operability, future roads, and
stand-level retention do not fit perfectly into the TSA29 stage vocabulary.

## Ordered Cumulative Netdown Table

Area values are from MP10 Table 4. Reduction values are total-area reductions
unless otherwise noted. The cumulative remaining area follows the printed Table
4 checkpoint sequence.

| Step ID | MP10 row / action | FEMIC stage | Reduction ha | Cumulative ha | Source anchor | Implementation/readiness note |
| --- | --- | --- | ---: | ---: | --- | --- |
| tfl6_nd_000 | Total landbase | reference_target / GLB | 0 | 171441 | Table 4 | Historical MP10 analysis boundary. Current P1.6 FADM TFL 6 boundary is larger, so direct area benchmarking needs boundary reconciliation. |
| tfl6_nd_010 | Less non-forest | glb_to_aflb | 13483 | 157958 | Table 4; Table 5 | Candidate attribute exclusion from 2025 R1 BCLCS/non-forest/non-vegetated fields; verify category mapping to alpine, rock/slides, water/wetlands, dumps/camps/sorts, utility RoW, brush, and other. |
| tfl6_nd_020 | Less existing roads | glb_to_aflb | 3935 | 154023 | Table 4; Table 6 | Spatial line/polygon overlay candidate. MP10 used classified road polygons plus buffered unclassified road lines: highway 30 m, mainline 12 m, branch 10 m, spur/stub 8 m. Source road layer still needs resolution. |
| tfl6_nd_030 | Total forested | reference_target | 0 | 154023 | Table 4 | Milestone only, not a deduction. |
| tfl6_nd_040 | Less non-productive forest | glb_to_aflb | 6964 | 147059 | Table 4; Table 7 | Candidate VRI descriptor/productivity/ecosite exclusion. MP10 Table 7 includes non-productive and low-productivity ecosites CP, MH, MH1, S7, S8 / PG5. |
| tfl6_nd_050 | Total productive forest | reference_target / AFLB | 0 | 147059 | Table 4 | Proposed AFLB-style productive-forest checkpoint for FEMIC review. |
| tfl6_nd_060 | Less inoperable, including uneconomic | aflb_to_lhlb | 12438 | 134621 | Table 4; Table 8 | Requires operability class source. MP10 classes include physical inoperable `I` and marginal/economic classes `Ocm` and `Ohm`; no additional terrain-stability netdown was applied beyond inoperability. |
| tfl6_nd_070 | Total operable | reference_target / LHLB | 0 | 134621 | Table 4 | Proposed LHLB-style operable checkpoint for FEMIC review. |
| tfl6_nd_080 | Riparian management | lhlb_to_thlb | 10632 | 123989 | Table 4; Table 9 | Spatial overlay/buffer candidate. MP10 applies FRPA-style riparian management area logic, including RRZ widths plus operational RMZ retention by stream/lake/wetland class and a 40 m ocean shoreline reserve. Requires hydrography, lakes/wetlands, shoreline, class fields, and horizontal-distance buffer rules. |
| tfl6_nd_090 | Ungulate winter ranges | lhlb_to_thlb | 1313 | 122676 | Table 4; Table 10 | Spatial overlay candidate from UWR order data. MP10 references U-1-010 plus 5.3 ha from U-1-011 inside TFL 6 analysis boundary. |
| tfl6_nd_100 | Established OGMAs | lhlb_to_thlb | 3750 | 118926 | Table 4; Table 11 | Spatial overlay candidate. MP10 established OGMAs: Marble and San Josef. Current legal OGMA layer may differ from 2011 analysis state. |
| tfl6_nd_110 | Draft OGMAs | lhlb_to_thlb | 3469 | 115457 | Table 4; Table 11 | Historical/local source likely required. MP10 draft OGMAs: Holberg, Keogh, Mahatta, Neroutsos. Current public legal layers may not include 2011 draft geometry. |
| tfl6_nd_120 | Wildlife habitat areas | lhlb_to_thlb | 3 | 115454 | Table 4; Table 12 | Spatial overlay candidate from WHA layer. MP10 WHAs include 1-089, 1-106, 1-107, 1-199, 1-200, 1-201, and 1-202; most area overlaps prior OGMAs. |
| tfl6_nd_130 | Recreation sites and trails | lhlb_to_thlb | 50 | 115404 | Table 4; Table 13 | Spatial overlay/buffer candidate. MP10 says significant recreation features are netted out by applying a 10 m buffer. |
| tfl6_nd_140 | Deciduous-leading forest | lhlb_to_thlb | 1774 | 113630 | Table 4; Table 14 | Attribute exclusion candidate from R1/VDYP species-leading fields. MP10 excludes deciduous-leading stands while retaining deciduous volume components in conifer-leading stands. |
| tfl6_nd_150 | Cultural heritage resources | lhlb_to_thlb | 132 | 113498 | Table 4; Table 15 | Likely reviewed/aspatial or proxy spatial deduction. MP10 uses a 1% incremental netdown for TFL 6 area both within an EFZ and within 1 km of ocean; detailed TUS/CMT data are not normally public. |
| tfl6_nd_160 | Total operable reductions | reference_target | 21124 | 113497 | Table 4 | Milestone/check row. Small one-hectare discrepancy from sequential rounded reductions is from Table 4 rounding. |
| tfl6_nd_170 | Reduced landbase | reference_target | 0 | 113497 | Table 4 | Pre-stand-level-retention checkpoint. |
| tfl6_nd_180 | Less allowance for stand-level retention | lhlb_to_thlb | 5686 | 107811 | Table 4; Table 16 | Aspatial percent deduction by strategic Resource Management Zone/LU/BEC stratum. MP10 distributes a 5.0% area-weighted THLB reduction rather than applying one uniform factor. Requires strategic RMZ, LU, BEC attribution and Table 16 percentages. Do not confuse this strategic RMZ use with operational riparian RMZ buffers in `tfl6_nd_080`. |
| tfl6_nd_190 | Current THLB | reference_target / THLB | 0 | 107811 | Table 4 | Current MP10 THLB benchmark. |
| tfl6_nd_200 | Less future roads | context / long_term_adjustment | 1491 | 106319 | Table 4; Table 17 | Future/model-time deduction. MP10 assumes 1,947 km of future branch road at 10 m width, reducing area as polygons are harvested. |
| tfl6_nd_210 | Long-term landbase | reference_target | 0 | 106319 | Table 4 | Long-term benchmark after future roads; do not confuse with current THLB. |

## Input Data Layer Requirements

The following input data surfaces need to be resolved or reviewed before an
executable TFL 6 netdown recipe can run.

| Requirement | MP10 step(s) | Expected layer type | Current status |
| --- | --- | --- | --- |
| Accepted TFL 6 AOI and 2025 inventory | tfl6_nd_000 onward | Polygon inventory with `feature_id` join to VDYP tables | Accepted by P1.6 in `data/input/tfl_6/input_layers_manifest.json`. |
| Non-forest and non-productive attributes | tfl6_nd_010, tfl6_nd_040 | R1/VDYP attributes | Candidate fields exist in the clipped R1 table, but MP10 class mapping is not reviewed. |
| Road network | tfl6_nd_020, tfl6_nd_200 | Road lines/polygons, widths, existing/future distinction | Missing source-layer decision. Existing roads and future roads likely need separate treatment. |
| Operability | tfl6_nd_060 | Polygon/attribute source for `Oce`, `Ohe`, `I`, `Ocm`, `Ohm` or successor classes | Missing source-layer decision; may require WFP/local source or reviewed proxy. |
| Hydrography, lakes, wetlands, shoreline | tfl6_nd_080 | Classified line/polygon features with stream/lake/wetland class and ocean shoreline | Missing source-layer decision; needs buffer/rule implementation. |
| UWR | tfl6_nd_090 | Legal/order polygon layer | Public BCDC candidate; not yet resolved for TFL 6 IDs. |
| OGMAs, including draft 2011 state | tfl6_nd_100, tfl6_nd_110 | Established and draft OGMA polygons | Established OGMAs likely public; draft 2011 OGMAs may require historical/local source or non-current benchmark handling. |
| WHA | tfl6_nd_120 | WHA polygons with order/species IDs | Public BCDC candidate; not yet resolved for listed IDs. |
| Recreation features | tfl6_nd_130 | Recreation site/trail features | Missing source-layer decision; requires 10 m buffer rule. |
| Deciduous-leading stand signal | tfl6_nd_140 | Inventory species-leading fields | Candidate R1/VDYP attributes; exact species-lead definition needs review. |
| Cultural heritage resource proxy | tfl6_nd_150 | EFZ/strategic RMZ plus 1 km ocean-proximity overlay, or reviewed aspatial deduction | Sensitive/local data likely unavailable; MP10 supports proxy/aspatial treatment. |
| Strategic RMZ, LU, BEC attribution | tfl6_nd_180 plus constraints | Polygons/attributes for strategic Resource Management Zone type, landscape unit, BEC subzone | Required for stand-level retention percentages and old-seral/green-up constraints. |

## Milestone Comparison Contract

For future FEMIC recipe skeletons, keep three separate area stories visible:

| Story | Meaning | Current value |
| --- | --- | ---: |
| MP10 historical GLB | MP10 Table 4 total analysis landbase | 171441 ha |
| Current P1.6 AOI | 2025 TFL 6 FADM boundary accepted by FEMIC | 217042.718950 ha |
| MP10 productive/AFLB-style checkpoint | MP10 Table 4 total productive forest | 147059 ha |
| MP10 operable/LHLB-style checkpoint | MP10 Table 4 total operable landbase | 134621 ha |
| MP10 current THLB | MP10 Table 4 current timber harvesting land base | 107811 ha |
| MP10 long-term landbase | MP10 current THLB less future roads | 106319 ha |

Do not compare a current 2025 reconstructed TFL 6 THLB directly against the
MP10 THLB until the boundary/date/source difference is explicitly reconciled.

Post-2011 boundary-change evidence is recorded in
`planning/tfl6_instrument_boundary_reconciliation.md`. The leading hypothesis
is that Instrument 101, effective January 1, 2015, added TFL 39 Block 4 lands
to TFL 6 and explains most or all of the difference between the `171441 ha`
MP10 historical GLB and the `217042.718950 ha` current FADM-derived AOI.

Provisional scaled current-AOI validation targets are recorded in
`planning/tfl6_adjusted_thlb_benchmarks.md` and
`planning/tfl6_adjusted_thlb_benchmarks.json`. These uniformly scale MP10 Table
4 by the current-AOI/MP10-GLB factor and should be used only as approximate
early validation targets until spatial current-AOI recipe outputs supersede
them.

The P1.7c adaptation classification is recorded in
`planning/tfl6_recipe_adaptation_contract.md`.

## P1.7c/P1.7d Handoff

P1.7c classified each row above into:

- TSA29 workflow pattern that carries forward directly;
- TFL/general-FMU adaptation needed before recipe YAML;
- blocked missing source layer;
- reviewed aspatial fallback candidate; or
- context/reference target only.

P1.7d should draft non-executable recipe skeletons from this table and
`planning/tfl6_recipe_adaptation_contract.md`. The resulting P1.7d skeleton
planning tables are recorded in `planning/tfl6_recipe_skeletons.md`.
