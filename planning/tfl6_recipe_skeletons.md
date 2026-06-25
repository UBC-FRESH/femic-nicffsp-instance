# TFL 6 Recipe Skeletons

## Purpose

This note drafts non-executable source-layer and THLB netdown recipe skeleton
planning tables for TFL 6.

Governing issue: `#7`.

This is a P1.7d planning surface. It proposes future recipe destinations and
review rows only. It does not create recipe YAML, download new source layers, or
run THLB netdown.

## Proposed Future Recipe Destinations

Use TFL/general-FMU successor paths instead of writing directly to the current
TSA-oriented `config/tsr/` recipe paths:

| Future path | Role | Status |
| --- | --- | --- |
| `config/tfl6/source_layers.recipe.yaml` | Future reviewed source-layer recipe for TFL 6. | Proposed only; not created in P1.7d. |
| `config/tfl6/thlb_netdown.recipe.yaml` | Future reviewed THLB netdown recipe for TFL 6. | Proposed only; not created in P1.7d. |
| `config/tfl6/overlay.yaml` | Future TFL/general-FMU reviewed assumption overlay, if FEMIC generalizes the current TSR overlay schema. | Proposed only; not created in P1.7d. |
| `config/tfl6/source_layer_overrides.yaml` | Future escape hatch for reviewed source-layer acquisition overrides. | Proposed only; not created in P1.7d. |

The existing TSA29 paths remain the implementation pattern:

- `config/tsr/source_layers.recipe.yaml`
- `config/tsr/thlb_netdown.recipe.yaml`
- `config/tsr/overlay.yaml`
- `config/tsr/source_layer_overrides.yaml`

Do not write TFL 6 YAML into `config/tsr/` unless FEMIC first generalizes those
schemas beyond TSA identity assumptions.

## Source-Layer Skeleton

| Source ID | Supports steps | Source role | Candidate acquisition strategy | Candidate query or path | Status for P1.7d |
| --- | --- | --- | --- | --- | --- |
| `tfl6_aoi_current` | all current-AOI steps | Active current TFL 6 boundary. | accepted local input | `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`, layer `tfl_6_boundary` | accepted from P1.6 |
| `vri_2025_r1_tfl6` | `tfl6_nd_010`, `tfl6_nd_040`, `tfl6_nd_140` | Current-AOI inventory polygon attributes. | accepted local input | `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` | accepted from P1.6; field mapping still reviewed/unlocked |
| `vdyp7_2025_poly_tfl6` | inventory/yield joins, deciduous-leading review | Current-AOI VDYP7 polygon attributes. | accepted local input | `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet` | accepted from P1.6 |
| `vdyp7_2025_layer_tfl6` | inventory/yield joins, species-leading review | Current-AOI VDYP7 layer/species attributes. | accepted local input | `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` | accepted from P1.6 |
| `non_forest_attribute_map` | `tfl6_nd_010` | Attribute mapping from R1/VRI fields to MP10 non-forest classes. | reviewed field mapping | `vri_2025_r1_tfl6` fields to be profiled | draft skeleton only |
| `non_productive_attribute_map` | `tfl6_nd_040` | Attribute mapping from R1/VRI fields to MP10 non-productive and low-productivity classes. | reviewed field mapping | `vri_2025_r1_tfl6` fields to be profiled | draft skeleton only |
| `deciduous_leading_signal` | `tfl6_nd_140` | Attribute signal for deciduous-leading stands. | reviewed field mapping | R1/VDYP leading-species fields | draft skeleton only |
| `existing_roads` | `tfl6_nd_020` | Existing classified road lines/polygons and road-width assumptions. | BCDC/FEMIC resolve or reviewed local source | queries: `roads`, `forest service roads`, `digital road atlas`, `TFL 6 roads` | missing source layer |
| `future_roads_allowance` | `tfl6_nd_200` | Future branch-road model-time allowance. | aspatial fallback from MP10 Table 17 unless projected-road geometry is accepted | MP10 assumes 1,947 km at 10 m width | context/fallback only |
| `operability` | `tfl6_nd_060` | Operability classes `I`, `Ocm`, `Ohm`, and related conventional/heli/economic classes. | reviewed local source or proxy | candidate query: `TFL 6 operability` | missing source layer |
| `hydrography_streams` | `tfl6_nd_080` | Classified streams for riparian RMA/RRZ/RMZ buffers. | BCDC/FEMIC resolve | queries: `Freshwater Atlas streams`, `FWA streams` | missing source layer |
| `lakes_wetlands_shoreline` | `tfl6_nd_080` | Lakes, wetlands, and ocean shoreline for riparian RMA/RRZ/RMZ buffers. | BCDC/FEMIC resolve plus shoreline decision | queries: `Freshwater Atlas lakes`, `wetlands`, `shoreline` | missing source layer |
| `uwr_orders` | `tfl6_nd_090` | Ungulate winter range polygons and order IDs. | BCDC/FEMIC resolve | queries: `Ungulate Winter Range U-1-010`, `U-1-011` | missing source layer |
| `ogma_established` | `tfl6_nd_100` | Established OGMA polygons. | BCDC/FEMIC resolve with vintage warning | query: `Old Growth Management Areas` | missing source layer; vintage risk |
| `ogma_draft_2011` | `tfl6_nd_110` | MP10 draft OGMA polygons. | historical/local source or aspatial fallback | Holberg, Keogh, Mahatta, Neroutsos draft OGMAs | missing historical source |
| `wha_orders` | `tfl6_nd_120` | Wildlife habitat area polygons and IDs. | BCDC/FEMIC resolve | queries: `Wildlife Habitat Area`, listed WHA IDs | missing source layer |
| `recreation_features` | `tfl6_nd_130` | Recreation sites and trails with 10 m buffer. | BCDC/FEMIC resolve | queries: `recreation sites`, `recreation trails` | missing source layer |
| `cultural_heritage_proxy` | `tfl6_nd_150` | EFZ/ocean-proximity proxy or reviewed aspatial deduction. | reviewed proxy/aspatial fallback | no public sensitive-source assumption | fallback only |
| `stand_level_retention_aspatial` | `tfl6_nd_180`, constraints | Aspatial stand-level-retention deduction from MP10 Table 16 / adjusted current-AOI benchmark. | reviewed aspatial fallback | MP10 `5686 ha`; scaled current-AOI `7198.423 ha` | accepted fallback for teaching instance |
| `instrument_101_context` | validation only | Boundary-vintage explanation for current-AOI scaling. | accepted planning context | `planning/tfl6_instrument_boundary_reconciliation.md` | not recipe input |
| `adjusted_benchmarks` | validation only | Approximate current-AOI validation targets. | accepted planning context | `planning/tfl6_adjusted_thlb_benchmarks.json` | not recipe input |

## THLB Netdown Skeleton

| Step ID | Future recipe action | Linked source IDs | Draft execution class | Execution status | Validation target |
| --- | --- | --- | --- | --- | --- |
| `tfl6_nd_000` | Declare active current-AOI boundary and historical MP10 GLB. | `tfl6_aoi_current`, `instrument_101_context`, `adjusted_benchmarks` | `reference_target` | report only | current AOI `217042.719 ha`; MP10 GLB `171441 ha` |
| `tfl6_nd_010` | Exclude reviewed non-forest attribute classes from current-AOI inventory. | `vri_2025_r1_tfl6`, `non_forest_attribute_map` | `drop_from_universe` | blocked on field mapping review | scaled cumulative `199973.366 ha` |
| `tfl6_nd_020` | Exclude existing roads using accepted road geometry and MP10 width rules. | `existing_roads` | `spatial_overlay_buffer_exclusion` | blocked on source layer | scaled cumulative `194991.692 ha` |
| `tfl6_nd_030` | Report total forested checkpoint. | prior steps | `reference_target` | report only | scaled cumulative `194991.692 ha` |
| `tfl6_nd_040` | Exclude non-productive/low-productivity forest classes. | `vri_2025_r1_tfl6`, `non_productive_attribute_map` | `drop_from_universe` | blocked on field mapping review | scaled cumulative `186175.333 ha` |
| `tfl6_nd_050` | Report productive forest/AFLB-style checkpoint. | prior steps, `adjusted_benchmarks` | `reference_target` | report only | scaled cumulative `186175.333 ha` |
| `tfl6_nd_060` | Exclude inoperable and uneconomic operability classes. | `operability` | `drop_from_universe` | blocked on source/proxy decision | scaled cumulative `170428.940 ha` |
| `tfl6_nd_070` | Report operable/LHLB-style checkpoint. | prior steps, `adjusted_benchmarks` | `reference_target` | report only | scaled cumulative `170428.940 ha` |
| `tfl6_nd_080` | Apply riparian reserve/management reductions using stream/lake/wetland/shoreline rules. | `hydrography_streams`, `lakes_wetlands_shoreline` | `spatial_overlay_buffer_or_fallback` | blocked on source/rule decision | scaled cumulative `156968.926 ha` |
| `tfl6_nd_090` | Exclude UWR order areas in MP10 hierarchy order. | `uwr_orders` | `spatial_overlay_exclusion` | blocked on source-layer resolution | scaled cumulative `155306.680 ha` |
| `tfl6_nd_100` | Exclude established OGMAs with vintage warning. | `ogma_established` | `spatial_overlay_exclusion` | blocked on vintage/source review | scaled cumulative `150559.215 ha` |
| `tfl6_nd_110` | Deduct draft OGMAs from historical/local geometry or fallback deduction. | `ogma_draft_2011` | `spatial_overlay_or_aspatial_fallback` | blocked on historical source/fallback decision | scaled cumulative `146167.493 ha` |
| `tfl6_nd_120` | Exclude WHA order areas after prior overlaps. | `wha_orders` | `spatial_overlay_exclusion` | blocked on source-layer resolution | scaled cumulative `146163.695 ha` |
| `tfl6_nd_130` | Exclude recreation sites/trails with 10 m buffer. | `recreation_features` | `spatial_overlay_buffer_exclusion` | blocked on source-layer resolution | scaled cumulative `146100.396 ha` |
| `tfl6_nd_140` | Exclude deciduous-leading stands. | `deciduous_leading_signal` | `attribute_exclusion` | blocked on field mapping review | scaled cumulative `143854.528 ha` |
| `tfl6_nd_150` | Apply cultural heritage proxy/aspatial deduction. | `cultural_heritage_proxy` | `aspatial_or_proxy_deduction` | fallback review required | scaled cumulative `143687.417 ha` |
| `tfl6_nd_160` | Report total operable reductions. | prior steps | `reference_target` | report only | scaled cumulative `143686.151 ha` |
| `tfl6_nd_170` | Report reduced landbase before stand-level retention. | prior steps | `reference_target` | report only | scaled cumulative `143686.151 ha` |
| `tfl6_nd_180` | Apply stand-level retention as an aspatial MP10 Table 16 deduction. | `stand_level_retention_aspatial` | `aspatial_fixed_deduction` | accepted fallback for teaching instance | scaled cumulative `136487.728 ha`; scaled reduction `7198.423 ha` |
| `tfl6_nd_190` | Report current THLB. | prior steps, `adjusted_benchmarks` | `reference_target` | report only | scaled current THLB `136487.728 ha` |
| `tfl6_nd_200` | Apply future-road allowance only for long-term landbase context. | `future_roads_allowance` | `future_model_time_context` | keep out of current THLB execution | scaled cumulative `134598.870 ha` |
| `tfl6_nd_210` | Report long-term landbase. | prior steps, `adjusted_benchmarks` | `reference_target` | report only | scaled long-term `134598.870 ha` |

## Blocked Execution Notes

The following blockers must remain visible in any later recipe YAML:

- no reviewed R1/VDYP field map yet exists for non-forest, non-productive, or
  deciduous-leading exclusions;
- no accepted existing-road source exists;
- no accepted operability source or proxy exists;
- no accepted hydrology/wetland/shoreline bundle and MP10 riparian
  RMA/RRZ/RMZ rule mapping exists;
- UWR, WHA, and established OGMA public-layer IDs/vintage still need BCDC/FEMIC
  resolution;
- draft OGMAs likely need historical/local geometry or a reviewed aspatial
  fallback;
- cultural heritage data are sensitive and should not be represented as public
  source geometry;
- strategic Resource Management Zone vector attribution is deferred; the base
  teaching lane uses accepted aspatial stand-level retention for `tfl6_nd_180`;
  and
- adjusted benchmark values are validation targets only, not executable source
  rows.

## P1.7 Closeout

This note completes the P1.7 planning lane:

- P1.7a indexed the source corpus;
- P1.7b reviewed the 2011 document assumptions;
- P1.7b1 recorded the ordered netdown backbone;
- P1.7b2 recorded Instrument 101 boundary context;
- P1.7b3 recorded adjusted current-AOI validation targets;
- P1.7c classified adaptation gaps; and
- P1.7d drafted non-executable skeleton planning tables.

The next implementation lane should be a new issue or follow-on task that
chooses one executable subset, starting with the accepted current-AOI inventory
attribute mapping before broader source acquisition or THLB execution.
