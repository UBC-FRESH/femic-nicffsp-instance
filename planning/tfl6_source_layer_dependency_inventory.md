# TFL 6 Source Layer Dependency Inventory

## Purpose

This note starts P2.1 by turning the Phase 1 THLB skeleton into a dependency
inventory for the first executable TFL 6 THLB netdown lane.

Governing issue: `#16`.

This is a dependency-resolution slice only. It does not download source layers,
materialize new data, create recipe YAML, or run THLB netdown.

## Accepted Local Inputs

These inputs are already accepted by the Phase 1 manifest and can be treated as
materialized dependencies for later P2.1/P2.2 work.

| Source ID | Role | Accepted path | Contract status | First use |
| --- | --- | --- | --- | --- |
| `tfl6_aoi_current` | Active current TFL 6 AOI boundary | `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`, layer `tfl_6_boundary` | Accepted by P1.6; EPSG:3005; union area `217042.718950 ha` | all current-AOI steps |
| `vri_2025_r1_tfl6` | Current-AOI VRI R1 inventory polygon | `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`, layer `vri_2025_r1_poly_tfl6` | Accepted by P1.6; `26959` clipped features; `feature_id` join key | `tfl6_nd_010`, `tfl6_nd_040`, `tfl6_nd_140` |
| `vdyp7_2025_poly_tfl6` | Current-AOI VDYP7 polygon table | `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet` | Accepted by P1.6; `26833` retained feature IDs | inventory/yield joins |
| `vdyp7_2025_layer_tfl6` | Current-AOI VDYP7 layer/species table | `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` | Accepted by P1.6; `25356` unique feature IDs | species-leading review |
| `adjusted_benchmarks` | Approximate current-AOI validation targets | `planning/tfl6_adjusted_thlb_benchmarks.json` | Validation target only; not executable source data | milestone comparison |

## First-Lane Dependency Table

This table records the source-layer status for the first executable netdown
lane in MP10 Table 4 order. "Accepted local" means the dependency is already
materialized. "Field mapping" means no new external source is required, but
P2.2 must review source fields before execution. "Missing source" means P2.1
still has to resolve an authority/path. "Fallback" means the row may need a
reviewed aspatial or proxy treatment instead of public geometry.

| Step | Dependency | Source authority / likely source | Expected role | Status | Next action |
| --- | --- | --- | --- | --- | --- |
| `tfl6_nd_000` | `tfl6_aoi_current` | FADM TFL boundary, `WHSE_ADMIN_BOUNDARIES.FADM_TFL`, `FOREST_FILE_ID='TFL6'` | Active AOI universe | Accepted local | Use as report/input boundary. |
| `tfl6_nd_010` | `non_forest_attribute_map` from `vri_2025_r1_tfl6` | Accepted 2025 VRI R1 fields | Attribute exclusion for MP10 non-forest classes | Field mapping blocker | P2.2 profile R1 fields and map BCLCS/non-vegetated/water/wetland/brush classes. |
| `tfl6_nd_020` | `existing_roads` | Primary candidate: Digital Road Atlas MPAR, `WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP`; secondary review candidate: 2025 CEF Integrated Roads archive | Existing-road line/polygon overlay and buffer exclusion | Public authority candidate identified; materialization/rule review still open | Use DRA MPAR as first materialization target, review whether the full-province GDB or bbox WFS path is preferred, and keep future-road allowance separate. |
| `tfl6_nd_030` | prior-step checkpoint | MP10 Table 4 | Report-only total forested checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_040` | `non_productive_attribute_map` from `vri_2025_r1_tfl6` and/or `vdyp7_2025_poly_tfl6` | Accepted 2025 VRI R1/VDYP7 fields | Attribute/productivity exclusion | Field mapping blocker | P2.2 profile productivity/ecosite/descriptive fields for CP, MH, MH1, S7, S8, PG5-style classes. |
| `tfl6_nd_050` | prior-step checkpoint | MP10 Table 4 / adjusted targets | Report-only productive/AFLB checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_060` | `operability` | Historical WFP/TFL operability source if available; otherwise reviewed proxy; generic public `Operable and Inoperable Areas SIR` is not accepted for TFL 6 | Operability class exclusion for `I`, `Ocm`, `Ohm` semantics | No accepted public TFL 6 source found; proxy decision still open | Search the local/reference corpus for TFL 6 operability geometry or map evidence; otherwise record a reviewed teaching proxy or benchmark fallback. |
| `tfl6_nd_070` | prior-step checkpoint | MP10 Table 4 / adjusted targets | Report-only operable/LHLB checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_080` | `hydrography_streams`, `lakes_wetlands_shoreline` | Freshwater Atlas `WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP`, `WHSE_BASEMAPPING.FWA_LAKES_POLY`, and `WHSE_BASEMAPPING.FWA_WETLANDS_POLY`; coarse shoreline candidate `WHSE_BASEMAPPING.NTS_BC_COASTLINE_POLYS_125M` | Riparian reserve/management overlay or fallback | Public hydro candidates identified; shoreline/rule review still open | Use FWA as first hydrology materialization target; review whether coarse NTS coastline is good enough for teaching or whether MP10 shoreline/ocean handling should remain a rule/fallback. |
| `tfl6_nd_090` | `uwr_orders` | Approved UWR, `WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP` | UWR overlay exclusion for `U-1-010` and small `U-1-011` overlap | Public authority candidate identified | Materialize/clip approved UWR and confirm listed IDs within current TFL 6 AOI. |
| `tfl6_nd_100` | `ogma_established` | Legal current OGMA, `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW` | Established OGMA overlay exclusion | Public authority candidate identified; current-vs-2011 vintage risk | Materialize/clip current legal OGMAs and flag any mismatch against MP10 established OGMA assumptions. |
| `tfl6_nd_110` | `ogma_draft_2011` | Historical/local draft OGMA geometry if available; current non-legal OGMA candidate `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW` is only a review clue | Draft OGMA overlay or aspatial fallback | Missing historical source / fallback | Search reference/local corpus for 2011 draft OGMA geometry; do not substitute current non-legal OGMAs without review. |
| `tfl6_nd_120` | `wha_orders` | Approved WHA, `WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY` | WHA overlay exclusion for listed WHA IDs | Public authority candidate identified | Materialize/clip approved WHA and confirm listed IDs/overlaps. |
| `tfl6_nd_130` | `recreation_features` | Public recreation sites/trails candidates | Recreation feature overlay with 10 m buffer | Missing source | Resolve recreation site/trail layers and geometry type. |
| `tfl6_nd_140` | `deciduous_leading_signal` from `vri_2025_r1_tfl6` and/or `vdyp7_2025_layer_tfl6` | Accepted 2025 VRI R1/VDYP7 species fields | Deciduous-leading attribute exclusion | Field mapping blocker | P2.2 define leading-species rule and deciduous/conifer species-code handling. |
| `tfl6_nd_150` | `cultural_heritage_proxy` | Sensitive/local TUS/CMT data not expected as public source; possible EFZ/ocean-proximity proxy | Aspatial/proxy deduction | Fallback only | Do not seek sensitive public geometry; define reviewed teaching fallback. |
| `tfl6_nd_160` | prior-step checkpoint | MP10 Table 4 | Report-only total operable reductions checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_170` | prior-step checkpoint | MP10 Table 4 | Report-only reduced landbase checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_180` | `rmz_lu_bec_strata` | Landscape unit, resource management zone, and BEC attribution sources | Stand-level retention percent-by-stratum | Missing source/schema decision | Resolve LU/RMZ/BEC sources and Table 16 stratum schema; do not execute until reviewed. |
| `tfl6_nd_190` | prior-step checkpoint | MP10 Table 4 / adjusted targets | Report-only current THLB checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_200` | `future_roads_allowance` | MP10 Table 17 aspatial future-road assumption | Long-term landbase context only | Fallback/context only | Keep out of current THLB lane unless long-term scenario work is explicitly opened. |
| `tfl6_nd_210` | prior-step checkpoint | MP10 Table 4 / adjusted targets | Report-only long-term landbase checkpoint | No source needed | Keep as validation row only. |

## Roads and Operability Resolver Evidence

The first public-source resolver pass was metadata-only. It did not download
or materialize source layers.

Command:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'Digital Road Atlas' `
  'forest service roads' `
  'resource roads' `
  'road permit' `
  'TFL 6 operability' `
  'forest operability' `
  'timber operability' `
  --summary-csv runtime\logs\p2_1_roads_operability_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1_roads_operability_bcdc_manifest.json
```

Resolver findings:

| Query | Top result | Resolution decision |
| --- | --- | --- |
| `Digital Road Atlas` | `Digital Road Atlas (DRA) - Master Partially-Attributed Roads`, GeoBC, object `WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP` | Accept as the first public candidate for current existing-road geometry. Later materialization can use the full-province GDB download or a TFL 6 bbox-scoped WFS fetch. |
| `resource roads` | `BC Cumulative Effects Framework - Integrated Roads - Archived`, including 2025 data and methodology resources | Keep as a secondary/reference candidate. It may be useful as a compiled disturbance check, but it should not replace DRA as the initial road authority without review. |
| `forest service roads` | `Forest Service Road Safety Information Web Map Application - South Coast` | Treat as context only. It has a direct download candidate, but the resolver evidence does not establish it as a complete authoritative TFL 6 existing-road source. |
| `road permit` | `BCTS Cut Permit / Road Permit Regulation - Blocks`, object `WHSE_FOREST_TENURE.BCTS_BLOCKS_CPRP_SP` | Do not accept as the TFL 6 road-network source. It may be relevant only for BCTS-specific tenure/block context. |
| `TFL 6 operability` | `Riparian Management Zones Buffer - North Coast TSA - Skeena Region`, matched by no resolver text signal | Not relevant to the TFL 6 operability netdown row. |
| `forest operability` / `timber operability` | `Operable and Inoperable Areas SIR`, custom-download only, matched by no resolver text signal | Do not accept as a TFL 6 source. It remains a generic/non-local clue only unless later evidence shows applicability. |

Current decision:

- Existing roads have a plausible public authority candidate, but no road layer
  has been accepted or clipped yet.
- Existing-road overlay design still needs MP10-specific width/class handling
  before execution.
- Future roads remain a separate aspatial Table 17 context row and must not be
  mixed into the current existing-road overlay.
- Operability remains unresolved: no public TFL 6-specific geometry was found
  by the first resolver pass.

## Hydrology, Shoreline, and Legal Overlay Resolver Evidence

This resolver slice was metadata-only. It did not download or materialize
source layers.

Commands:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'Freshwater Atlas streams' `
  'Freshwater Atlas lakes' `
  'Freshwater Atlas wetlands' `
  'shoreline' `
  'ocean coastline' `
  'Ungulate Winter Range' `
  'Wildlife Habitat Area' `
  'Old Growth Management Areas' `
  'legal old growth management areas' `
  --summary-csv runtime\logs\p2_1_hydro_legal_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1_hydro_legal_bcdc_manifest.json

..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP' `
  'WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY' `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW' `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW' `
  'FWA_STREAM_NETWORKS_SP' `
  'FWA_LAKES_POLY' `
  'FWA_WETLANDS_POLY' `
  --summary-csv runtime\logs\p2_1_hydro_legal_targeted_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1_hydro_legal_targeted_bcdc_manifest.json

..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'BC coastline' `
  'coastline polygon' `
  'coastline line' `
  'shorezone shoreline' `
  'physical shore-zone' `
  'TRIM coastline' `
  'Tantalis coastline' `
  --summary-csv runtime\logs\p2_1_shoreline_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1_shoreline_bcdc_manifest.json
```

Resolver findings:

| Dependency | Resolver result | Resolution decision |
| --- | --- | --- |
| Streams | `Freshwater Atlas Stream Network`, object `WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP`, WFS bbox strategy available | Accept as the first public stream-network materialization candidate. |
| Lakes | `Freshwater Atlas Lakes`, object `WHSE_BASEMAPPING.FWA_LAKES_POLY`, WFS bbox strategy available | Accept as the first public lake materialization candidate. |
| Wetlands | `Freshwater Atlas Wetlands`, object `WHSE_BASEMAPPING.FWA_WETLANDS_POLY`, exact-text result from the broad pass | Accept as the first public wetland materialization candidate. The later object-suffix targeted query returned a bad top hit, so do not use that targeted row as wetland evidence. |
| Shoreline / ocean boundary | `NTS BC Coastline Polygons 1:250,000`, object `WHSE_BASEMAPPING.NTS_BC_COASTLINE_POLYS_125M`; `NTS BC Coastline Lines 1:250,000`, object `WHSE_BASEMAPPING.NTS_BC_COASTLINE_LINES_125M`; ShoreZone results were monitoring/biobanding context, not a clean planning boundary | Keep as unresolved for rule review. The NTS coastline layers are plausible coarse teaching candidates, but MP10 shoreline/ocean handling may need a reviewed rule/fallback instead of a high-precision overlay. |
| UWR | `Ungulate Winter Range - Approved`, object `WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP`, exact object-name hit | Accept as the first public approved-UWR materialization candidate. Do not use the proposed UWR layer returned by generic search. |
| WHA | `Wildlife Habitat Areas - Approved`, object `WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY`, exact object-name hit | Accept as the first public approved-WHA materialization candidate. Do not use the proposed WHA layer returned by generic search. |
| Established OGMA | `Old Growth Management Areas - Legal - Current`, object `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW`, exact object-name hit | Accept as the first current legal OGMA materialization candidate, with an explicit current-vs-2011 vintage warning. |
| Draft OGMA | `Old Growth Management Areas - Non Legal - Current`, object `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW`, exact object-name hit | Keep as a review clue only. MP10 draft OGMA likely needs historical/local evidence or an aspatial fallback; do not substitute current non-legal OGMAs automatically. |

Current decision:

- FWA streams, lakes, and wetlands have first-pass public authority candidates.
- Approved UWR, approved WHA, and current legal OGMA have first-pass public
  authority candidates.
- Proposed UWR/WHA layers are explicitly rejected for this reviewed netdown
  lane unless later review narrows a separate scenario.
- Shoreline/ocean handling remains a review item because the clean public
  coastline candidates found here are coarse NTS 1:250,000 layers.
- Draft OGMA remains unresolved as historical/fallback work.

## Priority for Next P2.1 Slice

The next P2.1 slice should resolve public/reference authorities for the missing
source rows in this order:

1. Recreation features: sites/trails and 10 m buffer source.
2. Strata attribution: LU, RMZ, and BEC source/schema for stand-level retention.
3. Historical/fallback rows: shoreline rule choice, draft OGMAs, operability,
   and cultural heritage proxy/aspatial handling.

P2.2 should run in parallel only after maintainer approval, because the
accepted local R1/VDYP7 field-mapping rows are separable from missing public
source-layer acquisition.

## Non-Goals

- No source downloads or materialization were performed in this slice.
- No recipe YAML was created.
- No THLB netdown execution was run.
- No model-input, ForestModel/XML, Matrix Builder, or Patchworks runtime work
  was started.
