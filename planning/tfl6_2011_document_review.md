# TFL 6 2011 Document Review

## Purpose

This note records the first reviewed `P1.7b` pass over the 2011 TFL 6
Management Plan 10 document family for land-base, source-layer, yield, and
THLB netdown assumptions. It is a planning surface only: no source-layer or
THLB recipe execution is accepted here.

Governing issue: `#7`.

## Source Documents Reviewed

Primary review sources:

| Role | Local reference path | Extracted-text path | Notes |
| --- | --- | --- | --- |
| Management Plan 10 | `reference/tfl_6_mngment_plan_10_2011.pdf` | `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt` | Combined management-plan package; contains the information package and analysis report as appendices. |
| Information package | `reference/tfl_6_mngment_plan_2011_ip.pdf` | `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt` | Primary source for land-base netdown, yield, and modelling-assumption tables. |
| Timber supply analysis report | `reference/tfl_6_mngment_plan_2011_analysis.pdf` | `reference/extracted_text/tfl_6_mngment_plan_2011_analysis.txt` | Primary source for base-case and sensitivity interpretation. |
| Chief Forester AAC rationale | `reference/6tfra12ra.pdf` | `reference/extracted_text/6tfra12ra.txt` | Later acceptance/context check for key information-package assumptions. |

The page anchors below use the source document's printed page number where the
extracted text exposes it, with the extracted-text page in parentheses when it
helps relocate the text quickly.

## High-Value Anchors

| Theme | Primary document anchor | Key reviewed content |
| --- | --- | --- |
| Current management assumptions | Information package Section 3.1, extracted page 10 | Operable conventional/non-conventional land base, economic exclusions, OGMA removals, UWR/WHA removals, riparian management, stand-level retention, VQO modelling, green-up, and deciduous-leading exclusion are named as base-case assumptions. |
| Land-base netdown summary | Information package Section 6.2, Table 4, printed page 12, extracted page 21 | Total landbase, productive forest, operability, ordered reductions, current THLB, future-road allowance, and long-term landbase. |
| Detailed land-base deductions | Information package Sections 6.3-6.16, Tables 5-17, printed pages 13-24, extracted pages 22-33 | Non-forest, existing roads, non-productive forest, inoperability, riparian management, UWR, OGMAs, WHAs, recreation, deciduous-leading stands, cultural heritage, stand-level retention, future roads, and karst treatment. |
| Growth and yield | Information package Section 8, Tables 23-29, printed pages 33-41, extracted pages 42-50 | Productivity groups, species site index, utilization standards, OAFs, VDYP/TIPSY lanes, fertilization, managed/unmanaged stand groups, and future stand assumptions. |
| Visual and adjacency constraints | Information package Section 10.2.1-10.2.2, Table 31, printed page 46, extracted page 55 | Established VQO classes, disturbance limits, visually effective green-up age, and adjacency proxy assumptions by RMZ. |
| Old seral constraints | Information package Section 10.2.3, Table 32, printed page 47, extracted page 56 | LU/BEC/BEO productive and THLB areas, OGMA first-rotation treatment, and second/third rotation old-seral targets. |
| Steep terrain constraints | Information package Section 10.2.4, Table 33, printed page 49, extracted page 58 | Watershed-level steep-terrain productive/THLB areas and ten-year harvest limits. |
| Minimum harvest criteria | Information package Section 10.3.1, Table 35, printed page 50, extracted page 59 | Minimum average DBH and age ranges by ground, cable, and heli harvest system. |
| Initial harvest rate | Information package Section 10.3.2, printed page 50, extracted page 59 | Initial harvest-rate derivation from current AAC and planned 7.6% reduction. |
| Sensitivity context | Analysis report Sections 4.1-4.14 | Base-case sensitivity to unstable terrain/heli landbase, natural and managed yields, SIBEC, fertilization, hemlock planting, heli constraint, VQO disturbance, OGMAs, and minimum DBH. |

## Land-Base Summary from Table 4

| Step | Area or reduction ha | Notes for FEMIC planning |
| --- | ---: | --- |
| Total landbase | 171441 | Historical MP10 analysis boundary; differs from current P1.6 TFL 6 FADM boundary area and must be reconciled before benchmarking. |
| Less non-forest | 13483 | Table 5 detail: alpine, rock/slides, water/wetland classes, dumps/camps/sorts, utility RoW, brush, other. |
| Less existing roads | 3935 | Table 6 detail: highway, mainline, branch, spur/stub assumptions. |
| Total forested | 154023 | Intermediate checkpoint. |
| Less non-productive forest | 6964 | Table 7 detail includes low-productivity ecosites/PG5. |
| Total productive forest | 147059 | Productive-forest denominator for several later targets. |
| Less inoperable including uneconomic | 12438 | Table 8 detail: physical inoperability plus marginal conventional/heli economic classes. |
| Total operable | 134621 | Base before ordered operable reductions. |
| Riparian management | 10632 | Table 9 detail; includes stream/lake/wetland/ocean shoreline assumptions. |
| Ungulate winter ranges | 1313 | Table 10. |
| Established OGMAs | 3750 | Table 11; Marble and San Josef. |
| Draft OGMAs | 3469 | Table 11; Holberg, Keogh, Mahatta, Neroutsos. |
| Wildlife habitat areas | 3 | Table 12; marbled murrelet and northern goshawk WHAs. |
| Recreation sites and trails | 50 | Table 13. |
| Deciduous-leading forest | 1774 | Table 14. |
| Cultural heritage resources | 132 | Table 15; incremental EFZ/ocean-proximity netdown. |
| Total operable reductions | 21124 | Ordered deductions; overlapping constraints are handled by hierarchy. |
| Reduced landbase | 113497 | Pre-stand-level-retention checkpoint. |
| Stand-level retention allowance | 5686 | Table 16, distributed by RMZ/LU/BEC rather than uniform. |
| Current THLB | 107811 | Core current THLB benchmark for later recipe planning. |
| Future roads | 1491 | Table 17; future roads reduce future/long-term landbase when harvested. |
| Long-term landbase | 106319 | Long-term benchmark after future roads. |

The ordered THLB netdown interpretation of Table 4, including tentative
GLB/AFLB/LHLB/THLB stage mapping, candidate input layers, and GIS operation
notes, is recorded separately in `planning/tfl6_thlb_netdown_steps.md`.

## Candidate Source-Layer and Recipe Strategy

These are extraction candidates, not accepted recipe steps. P1.7c/P1.7d should
separate reusable TSA29 workflow patterns from TFL/general-FMU adaptation gaps
before any YAML recipe surface is promoted.

| Candidate | Source document anchor | Likely source-layer strategy | Initial recipe-stage classification |
| --- | --- | --- | --- |
| TFL 6 AOI | P1.6 accepted input manifest; MP10 Table 4 for historical benchmark | Use `data/source/tfl_6/aoi/tfl_6_boundary.gpkg` as current AOI; retain MP10 total area as historical benchmark only. | source acquisition / benchmark reconciliation |
| Non-forest | Information package Table 5 | Derive from 2025 R1 BCLCS/non-vegetated/non-forest attributes where possible; verify against source inventory semantics. | checkpoint-attribute exclusion |
| Existing roads | Information package Table 6 | Requires a road-line/source layer or VRI road polygons; existing-road width assumptions may require reproducible buffering. | exact spatial overlay or derived source layer |
| Non-productive forest | Information package Table 7 | Candidate VRI non-productive descriptor / productivity group / ecosite fields; needs mapping from MP10 ecosite/PG5 definitions to current data. | checkpoint-attribute exclusion |
| Operability/inoperability | Information package Table 8 | Needs operability class source. If no public equivalent is available, treat as local/reviewed source requirement. | source acquisition plus exact spatial/attribute exclusion |
| Terrain stability | Information package Section 6.6 and analysis Section 4.1 | Base case used no additional netdown except areas already classed inoperable; sensitivity considered Class V plus heli. | review-only baseline plus sensitivity candidate |
| Riparian management | Information package Table 9 | Requires stream/lake/wetland/ocean shoreline layers plus retention-width assumptions; likely reproducible overlay/buffer recipe. | exact spatial overlay plus aspatial retention factors |
| Ungulate winter range | Information package Table 10 | Public UWR spatial layer candidate. | exact spatial overlay |
| OGMAs | Information package Table 11 and Section 10.2.3 | Public/current OGMA layers plus historical established/draft distinction; MP10 draft OGMAs may not match current legal layers. | exact spatial overlay plus historical benchmark decision |
| Wildlife habitat areas | Information package Table 12 | Public WHA spatial layer candidate; verify species/order IDs. | exact spatial overlay |
| Recreation sites/trails | Information package Table 13 | Requires recreation feature/trail layer and 10 m buffer assumption. | exact spatial overlay |
| Deciduous-leading forest | Information package Table 14 | Derive from R1 species-leading fields or VDYP species table where possible. | checkpoint-attribute exclusion |
| Cultural heritage resources | Information package Table 15 | Likely not fully public; document says incremental 1% netdown applies within EFZ and within 1 km of ocean. | aspatial benchmark deduction or derived spatial proxy |
| Stand-level retention | Information package Table 16 | Distributed by RMZ type, LU, and BEC subzone; requires RMZ/LU/BEC attribution and percentage netdown. | aspatial percent deduction by stratum |
| Future roads | Information package Table 17 | Requires projected-road source or aspatial future-road allowance. | model-time/aspatial deduction |
| Karst | Information package Section 6.16 | Base case applied no additional karst netdown, assuming stand-level retention covers required reserves. | review-only/manual note |

## Yield and Modelling Assumption Candidates

| Assumption | Source document anchor | FEMIC implication |
| --- | --- | --- |
| Productivity groups and site index | Information package Table 23 | TFL 6 used three productivity groups, species-specific SI values, and THLB area-weighted averages. Current 2025 inventory may require a new mapping from BEC/ecosite/productivity group to FEMIC strata. |
| Utilization | Information package Table 24 | Natural/unmanaged stands used 17.5 cm DBH; managed stands used 12.5 cm DBH. This affects yield-source comparability with current VDYP7/TIPSY surfaces. |
| TIPSY OAFs | Information package Section 8.3 | Managed-stand TIPSY used OAF1 10% and OAF2 5%. |
| Managed stand retention yield reduction | Information package Section 8.4.2 | Future managed stands had additional yield reductions by RMZ: 2% EFZ, 3% GMZ, 5% SMZ. |
| VDYP unmanaged lane | Information package Section 8.5 | Existing mature and unmanaged immature stands used VDYP-derived area-weighted yields by AU; current 2025 VDYP7 tables should be treated as a new source lane, not as proof that MP10 yields carry forward. |
| TIPSY managed lane | Information package Tables 27-29 | Existing and future managed stands used Batch TIPSY 4.1 with species composition, stocking, SI, genetic worth, fertilization, and regeneration-delay assumptions. |
| Fertilization | Information package Section 8.6.2 | Fertilization was incorporated into current/future yield tables; species-specific approach used next-higher productivity group for cedar/hemlock/spruce and default TIPSY increases for Douglas-fir. |
| Regeneration delay | Information package Section 8.6.5 | Planted future managed stands used one-year regeneration delay; naturally regenerated stands used three years. |
| Visual quality | Information package Table 31 | VQO classes M/PR/R used 25/15/5% disturbance limits and 15-year VEG surrogate. |
| Adjacency green-up | Information package Section 10.2.2 | Areas outside VQO polygons used 3 m/10-year green-up in GMZ/SMZ and 1.3 m/5-year green-up in EFZ with a 25% young-area proxy. |
| Old-seral constraints | Information package Table 32 | OGMAs satisfy first-rotation targets in some cases; 2/3 and full old-seral targets are phased by second and third rotations where needed. |
| Steep terrain harvest limits | Information package Table 33 | Specific watershed-level ten-year harvest caps were applied for steep terrain. |
| Minimum harvest criteria | Information package Table 35 | Minimum average DBH by harvest system: ground 30 cm, cable 37 cm, heli 42 cm; age ranges differ by productivity. |

## Benchmark Caveats

- The MP10 Table 4 total landbase is `171441 ha`; the current P1.6 TFL 6 FADM
  boundary area is about `217043 ha`. Future benchmarking must explain the
  boundary/date/source difference before treating MP10 THLB area as a direct
  target for the 2025 TFL 6 input set.
- MP10 uses 2009/2011-era inventory, operability, draft/legal OGMAs, VQO, UWR,
  WHA, and WFP local assumptions. Current public layers may not reproduce that
  historical state exactly.
- Several MP10 assumptions are explicitly model assumptions rather than source
  exclusions: stand-level retention percentages, future roads, karst as covered
  by retention, visual/adjacency constraints, heli harvest volume constraints,
  and managed-stand retention yield reductions.
- The information package is the extraction authority for source assumptions;
  the analysis report is best used to understand sensitivity and base-case
  consequence, not as the first source for defining the netdown sequence.

## P1.7c/P1.7d Handoff

Next planning slices should:

- split the table above into TSA29 carry-forward patterns versus TFL/general-FMU
  adaptation gaps;
- decide whether recipe skeletons live under the existing `config/tsr/` paths
  or a renamed/generalized TFL/FMUs recipe surface;
- draft initial source-layer and THLB netdown recipe tables without executing
  them;
- preserve MP10 historical benchmarks separately from current 2025 TFL 6 input
  areas; and
- identify which public BCDC layers must be resolved before any reproducible
  netdown recipe can run.
