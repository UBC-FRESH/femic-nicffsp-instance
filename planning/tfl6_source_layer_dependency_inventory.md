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
| `tfl6_nd_020` | `existing_roads` | Primary candidate: Digital Road Atlas MPAR, `WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP`; secondary review candidate: 2025 CEF Integrated Roads archive | Existing-road line/polygon overlay and buffer exclusion | DRA MPAR materialized for review; road-width/class filtering still open | Review clipped road class/surface/type/name fields and decide MP10 existing-road width/buffer classes. Keep future-road allowance separate. |
| `tfl6_nd_030` | prior-step checkpoint | MP10 Table 4 | Report-only total forested checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_040` | `non_productive_attribute_map` from `vri_2025_r1_tfl6` and/or `vdyp7_2025_poly_tfl6` | Accepted 2025 VRI R1/VDYP7 fields | Attribute/productivity exclusion | Field mapping blocker | P2.2 profile productivity/ecosite/descriptive fields for CP, MH, MH1, S7, S8, PG5-style classes. |
| `tfl6_nd_050` | prior-step checkpoint | MP10 Table 4 / adjusted targets | Report-only productive/AFLB checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_060` | `operability` | Historical 1999 WFP/TFL physical and economic operability inventory if local geometry is found; generic public `Operable and Inoperable Areas SIR` is not accepted for TFL 6; see P2.1a issue `#20` and `planning/tfl6_operability_netdown_proxy.md` | Operability class exclusion for `I`, `Ocm`, `Ohm`, plus base-case/sensitivity treatment of yarding-system and economic-access assumptions | Separate design lane opened; no accepted public geometry; aspatial benchmark remains provisional only, not a final locked base-case rule | Complete P2.1a before source-materialization planning treats operability as resolved. Use MP10 Table 8 / adjusted benchmark as calibration context, and design a VRI/VDYP plus DEM-slope proxy lane before executable spatial logic is accepted. |
| `tfl6_nd_070` | prior-step checkpoint | MP10 Table 4 / adjusted targets | Report-only operable/LHLB checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_080` | `hydrography_streams`, `lakes_wetlands_shoreline` | Freshwater Atlas `WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP`, `WHSE_BASEMAPPING.FWA_LAKES_POLY`, and `WHSE_BASEMAPPING.FWA_WETLANDS_POLY`; coarse shoreline candidate `WHSE_BASEMAPPING.NTS_BC_COASTLINE_POLYS_125M` | Riparian management overlay or fallback, using operational RMA/RRZ/RMZ rules | FWA streams/lakes/wetlands materialized for review; MP10 40 m ocean-shoreline rule accepted, but coarse NTS coastline still requires review before precision use | Review FWA hydrology attributes, stream/lake/wetland classes, operational RMA/RRZ/RMZ buffer semantics, and overlap order before recipe use; keep the MP10 40 m ocean-shoreline reserve as the teaching rule and review whether NTS coastline is adequate for approximate clipping. |
| `tfl6_nd_090` | `uwr_orders` | Approved UWR, `WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP` | UWR overlay exclusion for `U-1-010` and small `U-1-011` overlap | Approved UWR materialized for review | Review clipped UWR IDs, areas, overlap treatment, and MP10 consistency before executable exclusion. |
| `tfl6_nd_100` | `ogma_established` | Legal current OGMA, `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW` | Established OGMA overlay exclusion | Current legal OGMA materialized for review; current-vs-2011 vintage risk remains | Review clipped legal OGMA IDs, areas, dates, landscape units/proxies, overlap treatment, and MP10 established-OGMA consistency before executable exclusion. |
| `tfl6_nd_110` | `ogma_draft_2011` | Current non-legal OGMA, `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW`, plus historical/local draft OGMA geometry if found | Draft OGMA overlay or benchmark-calibrated fallback | Current non-legal OGMA materialized for review as a proxy candidate only; current-vs-2011 draft-state risk remains high | Review clipped non-legal OGMA IDs, dates, areas, and MP10 Table 11 consistency. Do not automatically treat this tiny current non-legal intersection as the 2011 draft OGMA deduction. |
| `tfl6_nd_120` | `wha_orders` | Approved WHA, `WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY` | WHA overlay exclusion for listed WHA IDs | Approved WHA materialized for review | Review clipped WHA IDs, areas, overlap treatment, and MP10 consistency before executable exclusion. |
| `tfl6_nd_130` | `recreation_features` | Recreation polygons `WHSE_FOREST_TENURE.FTEN_RECREATION_POLY_SVW`, recreation trails `WHSE_FOREST_TENURE.FTEN_REC_TRAILS_SVW`, recreation site points `WHSE_FOREST_TENURE.FTEN_REC_SITE_POINTS_SVW`, plus details/closures `WHSE_FOREST_TENURE.FTEN_REC_DTAILS_CLOSURES_SV` as attribution context | Recreation feature overlay with 10 m buffer | Recreation polygons, trails, site points, and details/closures materialized for review; geometry/rule review still open | Review clipped feature IDs/classes/status fields and decide which geometry classes receive MP10 recreation netdown treatment or 10 m buffers before executable use. |
| `tfl6_nd_140` | `deciduous_leading_signal` from `vri_2025_r1_tfl6` and/or `vdyp7_2025_layer_tfl6` | Accepted 2025 VRI R1/VDYP7 species fields | Deciduous-leading attribute exclusion | Field mapping blocker | P2.2 define leading-species rule and deciduous/conifer species-code handling. |
| `tfl6_nd_150` | `cultural_heritage_proxy` | Sensitive/local TUS/CMT data not expected as public source; MP10 Table 15 supports EFZ plus 1 km ocean-proximity proxy/aspatial treatment | Aspatial/proxy deduction | Reviewed fallback accepted; no sensitive public geometry search | Do not seek sensitive TUS/CMT geometry; use MP10 Table 15 / adjusted benchmark deduction unless a reviewed EFZ plus 1 km ocean-proximity proxy is explicitly implemented later. |
| `tfl6_nd_160` | prior-step checkpoint | MP10 Table 4 | Report-only total operable reductions checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_170` | prior-step checkpoint | MP10 Table 4 | Report-only reduced landbase checkpoint | No source needed | Keep as validation row only. |
| `tfl6_nd_180` | `stand_level_retention_aspatial` | MP10 Table 16 / adjusted current-AOI benchmark; LU/BEC materialized for review; Strategic Land and Resource Plans `WHSE_LAND_USE_PLANNING.RMP_STRGC_LAND_RSRCE_PLAN_SVW` is retained only as non-materialized review evidence | Stand-level retention aspatial deduction | Accepted as aspatial fallback for this teaching instance: use MP10 `5686 ha` historical deduction or scaled current-AOI `7198.423 ha` validation target until strategic RMZ geometry is supplied and reviewed | Encode the first executable recipe as an aspatial Table 16 stand-level-retention deduction. Do not block P2.1 on strategic RMZ geometry; keep any future strategic RMZ spatial implementation as an enhancement/sensitivity path. |
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
| Draft OGMA | `Old Growth Management Areas - Non Legal - Current`, object `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW`, exact object-name hit | First-pass decision was review clue only; superseded by the OGMA deep-dive below, which accepts the current non-legal layer as the first materialization/review candidate while still requiring 2011-vintage consistency review. |

Current decision:

- FWA streams, lakes, and wetlands have first-pass public authority candidates.
- Approved UWR, approved WHA, and current legal OGMA have first-pass public
  authority candidates.
- Proposed UWR/WHA layers are explicitly rejected for this reviewed netdown
  lane unless later review narrows a separate scenario.
- Shoreline/ocean handling remains a review item because the clean public
  coastline candidates found here are coarse NTS 1:250,000 layers.
- Draft OGMA remained unresolved after the first pass, but the later OGMA
  deep-dive section below upgrades current non-legal OGMA to the first public
  materialization/review candidate for the draft-OGMA row.

## OGMA Deep-Dive Resolver Evidence

This resolver/schema slice was metadata-only. It did not download or
materialize source layers.

Commands:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'Old Growth Management Areas Legal Current' `
  'Old Growth Management Areas Non Legal Current' `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW' `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW' `
  'RMP_OGMA' `
  'Legal Old Growth Management Areas Current' `
  'Non Legal Old Growth Management Areas Current' `
  'OGMA polygons' `
  'Old Growth Management Area polygons' `
  'Landscape Unit old growth management areas' `
  --limit 10 `
  --summary-csv runtime\logs\p2_1_ogma_deep_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1_ogma_deep_bcdc_manifest.json

..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW' `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --plan-only
```

Resolver findings:

| Candidate | Object | Public/access status | WFS/schema evidence | TFL 6 bbox hit check | Decision |
| --- | --- | --- | --- | --- | --- |
| Old Growth Management Areas - Legal - Current | `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW` | Public; Open Government Licence - British Columbia; BCGW custom download plus OpenMaps WFS service | WFS typename `pub:WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW`; fields include `LEGAL_OGMA_INTERNAL_ID`, `LEGAL_OGMA_PROVID`, `OGMA_TYPE`, `OGMA_PRIMARY_REASON`, `LEGALIZATION_FRPA_DATE`, `LEGALIZATION_OGAA_DATE`, `LAST_AMENDMENT_DATE`, `ENABLING_DOCUMENT_TITLE`, `ENABLING_DOCUMENT_URL`, and `FEATURE_AREA_SQM` | WFS `resultType=hits` against the TFL 6 bbox returned `264` matches | Accept as the first materialization target for established/current legal OGMA geometry. |
| Old Growth Management Areas - Non Legal - Current | `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW` | Public; Open Government Licence - British Columbia; BCGW custom download plus OpenMaps WFS service | WFS typename `pub:WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW`; fields include `NON_LEGAL_OGMA_INTERNAL_ID`, `NON_LEGAL_OGMA_PROVID`, `OGMA_TYPE`, `OGMA_PRIMARY_REASON`, `ORIGINAL_DECISION_DATE`, `LAST_AMENDMENT_DATE`, `ASSOCIATED_ACT_NAME`, and `FEATURE_AREA_SQM` | WFS `resultType=hits` against the TFL 6 bbox returned `26` matches | Accept as the first materialization/review target for draft/non-legal OGMA proxy geometry, but require 2011-vintage consistency review before using it as the MP10 draft OGMA row. |
| Old Growth Management Areas - Legal - All | `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_ALL_SVW` | Government audience; Access Only | BCGW custom download only in resolver evidence | Not tested | Do not use in the public teaching source lane unless access policy changes or the maintainer supplies a local copy. |
| Old Growth Management Areas - Non Legal - All | `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_ALL_SVW` | Government audience; Access Only | BCGW custom download only in resolver evidence | Not tested | Do not use in the public teaching source lane unless access policy changes or the maintainer supplies a local copy. |

Current decision:

- There are up-to-date public spatial polygon OGMA layers.
- The current legal OGMA layer is accepted as the established-OGMA
  materialization candidate.
- The current non-legal OGMA layer is accepted as the first public
  materialization/review candidate for the draft-OGMA row, replacing the
  earlier "review clue only" status.
- The non-legal layer still must not be blindly substituted for the 2011 MP10
  draft OGMAs. After clipping, compare landscape units, original decision or
  amendment dates, `OGMA_TYPE`, `OGMA_PRIMARY_REASON`, and area totals against
  MP10 Table 11 before accepting the row as executable.
- The `All` legal/non-legal OGMA layers appear to be government-only access
  surfaces and are out of scope for the public teaching data lane unless a
  reviewed local copy is supplied.

## Recreation and Strata Resolver Evidence

This resolver slice was metadata-only. It did not download or materialize
source layers.

Commands:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'Recreation Sites and Trails BC sites' `
  'Recreation Sites and Trails BC trails' `
  'forest recreation sites' `
  'forest recreation trails' `
  'WHSE_FOREST_TENURE.FTEN_RECREATION_POLY_SVW' `
  'WHSE_FOREST_TENURE.FTEN_RECREATION_LINE_SVW' `
  'WHSE_FOREST_TENURE.FTEN_RECREATION_POINTS_SVW' `
  'Landscape Units of British Columbia' `
  'WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW' `
  'Biogeoclimatic ecosystem classification' `
  'WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY' `
  'resource management zones Vancouver Island' `
  'resource management zones' `
  'land use plan resource management zones' `
  --summary-csv runtime\logs\p2_1_recreation_strata_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1_recreation_strata_bcdc_manifest.json

..\..\.venv\Scripts\python.exe -m femic data bcdc-resolve `
  'WHSE_FOREST_TENURE.FTEN_REC_TRAILS_SVW' `
  'WHSE_FOREST_TENURE.FTEN_REC_SITE_POINTS_SVW' `
  'WHSE_FOREST_TENURE.FTEN_REC_DTAILS_CLOSURES_SV' `
  'WHSE_FOREST_TENURE.FTEN_RECREATION_POLY_SVW' `
  'Strategic Land and Resource Plans Current' `
  'WHSE_LAND_USE_PLANNING.RMP_STRGC_LAND_RSRCE_PLAN_SVW' `
  'Vancouver Island land use plan' `
  'TFL 6 resource management zones' `
  --summary-csv runtime\logs\p2_1_recreation_strata_targeted_bcdc_summary.csv `
  --manifest-path runtime\logs\p2_1_recreation_strata_targeted_bcdc_manifest.json
```

Resolver findings:

| Dependency | Resolver result | Resolution decision |
| --- | --- | --- |
| Recreation polygons | `Recreation Polygons`, object `WHSE_FOREST_TENURE.FTEN_RECREATION_POLY_SVW`, exact object-name hit | Accept as a public polygon candidate for recreation feature materialization. |
| Recreation trails | `Recreation Trails Subset - Information Purposes Only`, object `WHSE_FOREST_TENURE.FTEN_REC_TRAILS_SVW`, exact object-name hit | Accept as the first public trail-line materialization candidate. |
| Recreation site points | `Recreation Sites Subset - Information Purposes Only`, object `WHSE_FOREST_TENURE.FTEN_REC_SITE_POINTS_SVW`, exact object-name hit | Accept as the first public site-point materialization candidate. |
| Recreation attribution context | `Recreation Sites, Reserves, and Interpretive Forests Details and Closures`, object `WHSE_FOREST_TENURE.FTEN_REC_DTAILS_CLOSURES_SV`, exact object-name hit | Keep as an attribution/context candidate, not a replacement for point/line/polygon geometry. |
| Landscape units | `Landscape Units of British Columbia - Current`, object `WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW`, exact object-name hit | Accept as the first public LU materialization candidate. |
| BEC | `BEC Map`, object `WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY`, exact object-name hit | Accept as the first public BEC materialization candidate. |
| Strategic Resource Management Zones / land-use zones | `Strategic Land and Resource Plans - Current`, object `WHSE_LAND_USE_PLANNING.RMP_STRGC_LAND_RSRCE_PLAN_SVW`, exact object-name hit; generic `TFL 6 resource management zones` returned an unrelated North Coast riparian-management-zone dataset | Keep Strategic Land and Resource Plans as a review clue only. No TFL 6-specific strategic RMZ geometry/schema is accepted yet. The rejected North Coast hit is a false positive for this TFL 6 Resource Management Zone need, not evidence for MP10 Table 16. |

Current decision:

- Recreation feature geometry has first-pass public authority candidates for
  polygons, trails, and site points.
- Landscape unit and BEC attribution have first-pass public authority
  candidates.
- Strategic RMZ remains unresolved. For MP10 Table 16, RMZ should be treated as
  strategic Resource Management Zone attribution, likely EFZ/GMZ/SMZ-style
  land-use-plan strata, not as the operational riparian management zone used in
  stream/lake/wetland buffering. The Table 16 stand-level retention row should
  not execute until strategic RMZ type/schema handling is reviewed against
  local MP10/MP9 evidence or converted to a reviewed aspatial fallback.
- The generic `TFL 6 resource management zones` resolver hit was rejected
  because it returned a North Coast riparian-management-zone dataset rather
  than TFL 6/Vancouver Island strategic Resource Management Zone geometry.

## Historical and Fallback Decision Pass

This pass records provisional teaching-model decisions for rows where the
original MP10 spatial sources have not been recovered. These decisions are not
claims that the historical geometry exists locally or has been accepted.

| Dependency | Decision | Rationale |
| --- | --- | --- |
| Operability | Split to P2.1a issue `#20`: use MP10 Table 8 / adjusted benchmark as calibration context only, while designing a VRI/VDYP-informed and DEM-slope-capable proxy/sensitivity lane until local 1999 WFP physical/economic operability geometry is found and reviewed. | Public resolver work found no accepted TFL 6-specific operability geometry, but MP9/MP10 provide enough inventory, terrain, economic-access, and yarding-system clues that operability should not be swept into a permanently locked aspatial fallback. |
| Shoreline / ocean | Preserve the MP10 40 m ocean-shoreline reserve rule; keep NTS 1:250,000 coastline as a coarse teaching candidate requiring review. | FWA streams/lakes/wetlands are accepted first candidates, but shoreline discovery found only coarse NTS coastline and ShoreZone context layers. The rule is source-supported; precision geometry remains unresolved. |
| Draft OGMAs | Materialize and review current non-legal OGMA geometry as the first public draft-OGMA proxy candidate; keep MP10 Table 11 / adjusted benchmark as the fallback until clipped areas, landscape units, dates, and OGMA attributes are compared against 2011 assumptions. | Current non-legal OGMA is public and WFS-queryable, but MP10 draft OGMAs are historical planning state and should not be replaced automatically by current non-legal OGMAs without consistency review. |
| Strategic RMZ / Table 16 stand-level retention | Accept LU and BEC as public candidates, but use reviewed MP10 Table 16 percent-by-stratum/aspatial fallback until strategic Resource Management Zone geometry/schema is accepted. | Public LU and BEC sources resolved cleanly. Strategic RMZ did not: Strategic Land and Resource Plans is only a review clue, and the TFL 6 RMZ query returned an unrelated riparian dataset. |
| Cultural heritage | Use MP10 Table 15 / adjusted benchmark as an aspatial fallback; do not seek sensitive TUS/CMT geometry. | MP10 supports a 1% incremental netdown where EFZ and 1 km ocean-proximity overlap. Sensitive cultural-source geometry is not expected as a public input for this teaching instance. |

These fallback decisions are sufficient to move from resolver discovery to a
source-materialization plan. They are not sufficient to execute the final THLB
lane without later review of the resulting recipe behavior and benchmark
tolerances.

## Strategic RMZ Recheck and Teaching Fallback Decision

After the RMZ terminology correction, a targeted resolver recheck was run using
the current FEMIC BCDC resolver, including the Phase 75 free-text improvements.
The query set covered Vancouver Island Land Use Plan, VILUP, strategic Resource
Management Zones, EFZ/GMZ/SMZ, TFL 6 resource management zones, and the exact
object name `WHSE_LAND_USE_PLANNING.RMP_STRGC_LAND_RSRCE_PLAN_SVW`.

Runtime-only evidence:

- `runtime/logs/p2_1_strategic_rmz_queries.txt`
- `runtime/logs/p2_1_strategic_rmz_bcdc_summary.csv`
- `runtime/logs/p2_1_strategic_rmz_bcdc_manifest.json`
- `runtime/bcdc_fetch/p2_1_strategic_rmz/rmp_strgc_land_rsrce_plan_svw_loader.kml`
- `runtime/bcdc_fetch/p2_1_strategic_rmz/rmp_strgc_land_rsrce_plan_svw.kml`

Findings:

- The only plausible public object-name hit remains `Strategic Land and
  Resource Plans - Current`, object
  `WHSE_LAND_USE_PLANNING.RMP_STRGC_LAND_RSRCE_PLAN_SVW`.
- The EFZ/GMZ/SMZ free-text queries returned no better catalogue match.
- The generic `TFL 6 resource management zones` query still returns the
  unrelated North Coast riparian-management-zone dataset and remains rejected.
- `femic data bcdc-fetch --plan-only` identified a possible WFS fetch, but the
  actual fetch failed because the package does not expose a WFS-queryable
  resource for this object.
- The KML resources are WMS ground-overlay wrappers. They include a
  `Vancouver_Island_Land_Use_Plan_Boundary` overlay, but do not provide
  vector strategic RMZ polygons or EFZ/GMZ/SMZ attributes that can be clipped to
  TFL 6.

Decision for this teaching instance:

- Do not block P2.1 or the first executable THLB lane on strategic RMZ geometry.
- Implement `tfl6_nd_180` as an aspatial stand-level-retention deduction using
  MP10 Table 16 / Table 4 evidence.
- Use `5686 ha` for historical MP10 reporting and `7198.423 ha` as the scaled
  current-AOI validation deduction from
  `planning/tfl6_adjusted_thlb_benchmarks.json`.
- Treat any later strategic RMZ spatial implementation as an enhancement or
  sensitivity lane, not as a prerequisite for the base teaching model.

## Priority for Next P2.1 Slice

The next P2.1 slice should move from authority discovery to materialization
planning in this order:

1. Source-materialization plan: decide which accepted candidates are safe to
   clip first, and which need maintainer review before download/materialization.
2. Recipe-readiness review: separate exact spatial overlays from accepted
   aspatial/proxy fallbacks before any THLB execution.

P2.2 should run in parallel only after maintainer approval, because the
accepted local R1/VDYP7 field-mapping rows are separable from missing public
source-layer acquisition.

## Source-Materialization Plan

This section defines the first materialization plan for public/reference source
layers.

Plan status: accepted for the first materialization pass under P2.1 on
2026-06-24. This acceptance authorizes a later bounded materialization pass for
the safe-to-clip-first rows only. It does not accept any materialized layer as
executable THLB recipe logic, and it does not authorize download of the
review/fallback-only rows.

The first materialization pass should use the accepted TFL 6 AOI boundary as
the clip/filter boundary:

- path: `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`;
- layer: `tfl_6_boundary`;
- CRS: EPSG:3005;
- union area: `217042.718950 ha`.

### Safe-To-Clip First

These layers have enough source authority and public access evidence to enter
the first source-materialization pass. "Safe-to-clip" means safe to fetch/clip
for review, not automatically accepted as executable THLB recipe logic.

| Source ID | Authority / object | Planned output path | First QA/read-smoke | Review before executable use |
| --- | --- | --- | --- | --- |
| `fwa_stream_networks_tfl6` | Freshwater Atlas Stream Network, `WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP` | `data/source/tfl_6/hydrology/fwa_stream_networks_tfl6.gpkg` | verify nonzero feature count after AOI bbox/clip; CRS EPSG:3005 or documented reprojection; line geometry; bounds intersect TFL 6 | map stream classes to MP10 riparian rules and decide which features receive reserve/management buffers. |
| `fwa_lakes_tfl6` | Freshwater Atlas Lakes, `WHSE_BASEMAPPING.FWA_LAKES_POLY` | `data/source/tfl_6/hydrology/fwa_lakes_tfl6.gpkg` | verify nonzero feature count; polygon geometry; valid geometries; clipped area summary | decide lake/riparian reserve treatment and overlap order with wetlands/streams. |
| `fwa_wetlands_tfl6` | Freshwater Atlas Wetlands, `WHSE_BASEMAPPING.FWA_WETLANDS_POLY` | `data/source/tfl_6/hydrology/fwa_wetlands_tfl6.gpkg` | verify nonzero feature count; polygon geometry; valid geometries; clipped area summary | decide wetland/riparian reserve treatment and whether FWA wetlands overlap VRI non-forest/non-productive classes. |
| `uwr_approved_tfl6` | Ungulate Winter Range - Approved, `WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP` | `data/source/tfl_6/wildlife/uwr_approved_tfl6.gpkg` | verify listed UWR IDs are present or explicitly absent; polygon geometry; valid geometries; clipped area summary | compare clipped IDs/areas against MP10 UWR assumptions before executable exclusion. |
| `wha_approved_tfl6` | Wildlife Habitat Areas - Approved, `WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY` | `data/source/tfl_6/wildlife/wha_approved_tfl6.gpkg` | verify listed WHA IDs are present or explicitly absent; polygon geometry; valid geometries; clipped area summary | compare clipped IDs/areas against MP10 WHA assumptions before executable exclusion. |
| `ogma_legal_current_tfl6` | Old Growth Management Areas - Legal - Current, `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW` | `data/source/tfl_6/ogma/ogma_legal_current_tfl6.gpkg` | verify nonzero feature count; fields include `OGMA_TYPE`, `OGMA_PRIMARY_REASON`, legal dates, enabling-document fields, `FEATURE_AREA_SQM`; clipped area summary | compare landscape units, dates, and areas against MP10 established OGMA Table 11 before executable use. |
| `ogma_non_legal_current_tfl6` | Old Growth Management Areas - Non Legal - Current, `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW` | `data/source/tfl_6/ogma/ogma_non_legal_current_tfl6.gpkg` | verify nonzero feature count; fields include `OGMA_TYPE`, `OGMA_PRIMARY_REASON`, `ORIGINAL_DECISION_DATE`, `LAST_AMENDMENT_DATE`, `FEATURE_AREA_SQM`; clipped area summary | treat as draft-OGMA proxy candidate only until dates/LU/area consistency are compared against MP10 Table 11. |
| `recreation_polygons_tfl6` | Recreation Polygons, `WHSE_FOREST_TENURE.FTEN_RECREATION_POLY_SVW` | `data/source/tfl_6/recreation/recreation_polygons_tfl6.gpkg` | verify polygon geometry; clipped feature count/area; key recreation identifiers retained | decide which polygon classes receive MP10 recreation netdown treatment. |
| `recreation_trails_tfl6` | Recreation Trails, `WHSE_FOREST_TENURE.FTEN_REC_TRAILS_SVW` | `data/source/tfl_6/recreation/recreation_trails_tfl6.gpkg` | verify line geometry; clipped feature count/length; trail identifiers retained | decide trail classes and whether the MP10 10 m buffer applies. |
| `recreation_site_points_tfl6` | Recreation Sites, `WHSE_FOREST_TENURE.FTEN_REC_SITE_POINTS_SVW` | `data/source/tfl_6/recreation/recreation_site_points_tfl6.gpkg` | verify point geometry; clipped feature count; site identifiers retained | decide point-buffer rules and relation to polygon recreation features. |
| `recreation_details_closures_tfl6` | Recreation details/closures, `WHSE_FOREST_TENURE.FTEN_REC_DTAILS_CLOSURES_SV` | `data/source/tfl_6/recreation/recreation_details_closures_tfl6.gpkg` | verify point geometry; row count; join keys to recreation points/trails/polygons if present | attribution/context only unless a joinable contract is reviewed. |
| `landscape_units_tfl6` | Landscape Units of British Columbia - Current, `WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW` | `data/source/tfl_6/strata/landscape_units_tfl6.gpkg` | verify Holberg, Keogh, Mahatta, Marble, Neroutsos, San Josef, or other intersecting LU names as applicable; clipped areas | use for OGMA, strategic RMZ, and BEC stratification review, not as a netdown by itself. |
| `bec_tfl6` | BEC Map, `WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY` | `data/source/tfl_6/strata/bec_tfl6.gpkg` | verify BEC zone/subzone/variant fields; clipped areas by BEC unit; valid polygons | use for Table 16 and old-seral strata review. |
| `dra_roads_tfl6` | Digital Road Atlas MPAR, `WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP` | `data/source/tfl_6/roads/dra_roads_tfl6.gpkg` | verify line geometry; clipped feature count/length; road class/status fields retained | decide MP10 existing-road width/buffer classes and keep future roads separate. |

### Review/Fallback Only For Now

These rows should not be downloaded or executed in the first source pass unless
the maintainer explicitly narrows or changes the scope.

| Dependency | Current status | Why it stays out of first materialization |
| --- | --- | --- |
| Operability proxy / DEM slope | P2.1a design is complete; LidarBC/open LiDAR is preferred for future slope metrics, CDED is a coarse smoke-test fallback | DEM tile selection, size, storage, public-data suitability, slope processing, and zonal-stat QA need their own materialization plan before downloads. |
| Shoreline / ocean precision | MP10 40 m ocean-shoreline rule is accepted as a teaching rule; public discovery found coarse NTS coastline candidates | precision and coastline geometry choice need maintainer review before a shoreline layer is treated as authoritative. |
| Strategic RMZ schema | LU and BEC are materialized review candidates; strategic Resource Management Zone geometry/schema was rechecked and remains non-materialized | no accepted TFL 6 strategic RMZ vector geometry exists; Table 16 is accepted as an aspatial stand-level-retention fallback for the teaching instance. |
| Cultural heritage | MP10 Table 15 / adjusted benchmark fallback accepted; sensitive TUS/CMT geometry should not be sought | public sensitive-source geometry is inappropriate for this teaching instance. |
| Future roads | MP10 Table 17 is a long-term/aspatial assumption | keep separate from current existing-road overlay and out of current THLB lane unless long-term scenario work is opened. |
| 1999 WFP operability geometry | preferred historical evidence if supplied locally | no reviewed local geometry has been materialized; do not fetch generic/non-local operability layers. |
| Government-only OGMA `All` layers | resolver evidence found `RMP_OGMA_LEGAL_ALL_SVW` and `RMP_OGMA_NON_LEGAL_ALL_SVW` as access-only/government surfaces | out of scope for the public teaching source lane unless a reviewed local copy or public access path is supplied. |

### Provenance Manifest Requirements

Each materialized source layer should have a manifest entry, either in a
single source-layer manifest or in per-layer sidecar JSON, recording:

- source ID and THLB dependency row(s);
- BCDC title, package name, package URL, object name, organization, licence,
  and download/access method;
- fetch command or DWDS/order metadata;
- AOI boundary path, layer, CRS, and bounds used for clipping/filtering;
- output path, layer/table name, format, CRS, geometry type, feature count,
  bounds, and area/length summary where applicable;
- field list or a compact field digest for rule-critical attributes;
- checksum for downloaded archives or generated output where practical;
- read-smoke command and result;
- review status: `materialized_for_review`, `accepted_for_recipe`,
  `fallback_only`, or `rejected`; and
- caveats, especially current-vs-2011 vintage risks.

### First-Pass QA Checks

The first materialization pass should run these checks before any source is
accepted for recipe use:

1. All outputs are readable from a clean Python/geopandas session.
2. Vector outputs have expected geometry type and valid geometries or a
   documented repair step.
3. Output CRS is EPSG:3005 or a documented source CRS with a reproducible
   reprojection plan.
4. Output bounds intersect the accepted TFL 6 AOI and do not obviously include
   unbounded provincial geometry after clipping.
5. Area or length summaries are recorded for each overlay source.
6. Rule-critical fields are present, especially IDs, dates, type/status/class
   fields, and area fields for OGMA/UWR/WHA/recreation/LU/BEC/roads.
7. Current-vs-2011 vintage warnings are preserved for OGMA, recreation, roads,
   LU/BEC, and any other current public layer used to approximate MP10 state.
8. No output is wired into recipe YAML until the recipe-readiness review
   accepts its semantics.

## First Hydrology Materialization Pass

This pass materialized the FWA hydrology trio for source review only. It did
not accept riparian RMA/RRZ/RMZ recipe semantics, create recipe YAML, or run
THLB netdown.

Commands used:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP' `
  'WHSE_BASEMAPPING.FWA_LAKES_POLY' `
  'WHSE_BASEMAPPING.FWA_WETLANDS_POLY' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --download-root runtime\bcdc_fetch\p2_1_hydrology `
  --manifest-path runtime\logs\p2_1_hydrology_bcdc_fetch_manifest.json `
  --allow-bulk

..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'Freshwater Atlas Wetlands' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --download-root runtime\bcdc_fetch\p2_1_hydrology `
  --manifest-path runtime\logs\p2_1_wetlands_bcdc_fetch_manifest.json `
  --allow-bulk
```

Notes:

- The first combined fetch succeeded for streams and lakes, then stopped at the
  exact wetlands object because the resolver selected a direct-download path
  without a WFS resource. The title query `Freshwater Atlas Wetlands` resolved
  the WFS service and was used for the wetlands fetch.
- Runtime WFS outputs were used as transient cache only. They were clipped to
  the exact TFL 6 AOI, written to curated source paths, read-smoked, and then
  removed from `runtime/`.
- Curated output manifest:
  `data/source/tfl_6/hydrology/hydrology_source_manifest.json`.

| Source ID | Curated output | Raw bbox features | TFL 6 clipped features | Metric | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `fwa_stream_networks_tfl6` | `data/source/tfl_6/hydrology/fwa_stream_networks_tfl6.gpkg`, layer `fwa_stream_networks_tfl6` | `25069` | `12078` | `4748715.276 m` line length | materialized for review |
| `fwa_lakes_tfl6` | `data/source/tfl_6/hydrology/fwa_lakes_tfl6.gpkg`, layer `fwa_lakes_tfl6` | `1365` | `599` | `3243.849 ha` polygon area | materialized for review |
| `fwa_wetlands_tfl6` | `data/source/tfl_6/hydrology/fwa_wetlands_tfl6.gpkg`, layer `fwa_wetlands_tfl6` | `1099` | `572` | `982.424 ha` polygon area | materialized for review |

Read-smoke and QA:

- all three curated outputs read successfully with geopandas;
- all three outputs are EPSG:3005;
- stream geometry type is `MultiLineString`;
- lake and wetland geometry types are `MultiPolygon`;
- all curated output geometries are valid after clipping;
- output bounds are inside the accepted TFL 6 AOI bbox; and
- each output has a SHA-256 hash recorded in
  `data/source/tfl_6/hydrology/hydrology_source_manifest.json`.

Recipe boundary:

- These layers are source-review artifacts only.
- Riparian reserve/management buffer rules, stream/lake/wetland class handling,
  overlap order, shoreline/ocean handling, and final netdown semantics remain
  unaccepted until recipe-readiness review.

## First Wildlife Materialization Pass

This pass materialized the approved UWR and approved WHA public wildlife
overlay candidates for source review only. It did not accept wildlife netdown
semantics, create recipe YAML, or run THLB netdown.

Command used:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP' `
  'WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --download-root runtime\bcdc_fetch\p2_1_wildlife `
  --manifest-path runtime\logs\p2_1_wildlife_bcdc_fetch_manifest.json
```

Notes:

- The bbox fetch returned `41` raw UWR features and `90` raw WHA features.
- Runtime WFS outputs were used as transient cache only. They were clipped to
  the exact TFL 6 AOI, written to curated source paths, read-smoked, and then
  removed from `runtime/`.
- Curated output manifest:
  `data/source/tfl_6/wildlife/wildlife_source_manifest.json`.

| Source ID | Curated output | Raw bbox features | TFL 6 clipped features | Metric | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `uwr_approved_tfl6` | `data/source/tfl_6/wildlife/uwr_approved_tfl6.gpkg`, layer `uwr_approved_tfl6` | `41` | `22` | `2365.514 ha` polygon area | materialized for review |
| `wha_approved_tfl6` | `data/source/tfl_6/wildlife/wha_approved_tfl6.gpkg`, layer `wha_approved_tfl6` | `90` | `45` | `2942.796 ha` polygon area | materialized for review |

Read-smoke and QA:

- both curated outputs read successfully with geopandas;
- both outputs are EPSG:3005;
- both outputs contain polygon and multipolygon geometries;
- all curated output geometries are valid after clipping;
- output bounds are inside the accepted TFL 6 AOI bbox; and
- each output has a SHA-256 hash recorded in
  `data/source/tfl_6/wildlife/wildlife_source_manifest.json`.

Recipe boundary:

- These layers are source-review artifacts only.
- UWR/WHA ID selection, overlap order, current-vs-2011 interpretation, and
  final wildlife netdown semantics remain unaccepted until recipe-readiness
  review.

## First OGMA Materialization Pass

This pass materialized the current legal and current non-legal public OGMA
overlay candidates for source review only. It did not accept established-OGMA
or draft-OGMA netdown semantics, create recipe YAML, or run THLB netdown.

Command used:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW' `
  'WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --download-root runtime\bcdc_fetch\p2_1_ogma `
  --manifest-path runtime\logs\p2_1_ogma_bcdc_fetch_manifest.json
```

Notes:

- The bbox fetch returned `264` raw legal-current OGMA features and `26` raw
  non-legal-current OGMA features.
- Runtime WFS outputs were used as transient cache only. They were clipped to
  the exact TFL 6 AOI, written to curated source paths, read-smoked, and then
  removed from `runtime/`.
- Curated output manifest:
  `data/source/tfl_6/ogma/ogma_source_manifest.json`.
- The non-legal-current clipped result is only `0.687 ha`. That is a strong
  warning that the current non-legal layer is not a drop-in replacement for
  the MP10 2011 draft-OGMA deduction without a separate review against MP10
  Table 11 and the adjusted benchmark.

| Source ID | Curated output | Raw bbox features | TFL 6 clipped features | Metric | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `ogma_legal_current_tfl6` | `data/source/tfl_6/ogma/ogma_legal_current_tfl6.gpkg`, layer `ogma_legal_current_tfl6` | `264` | `165` | `16131.032 ha` polygon area | materialized for review |
| `ogma_non_legal_current_tfl6` | `data/source/tfl_6/ogma/ogma_non_legal_current_tfl6.gpkg`, layer `ogma_non_legal_current_tfl6` | `26` | `2` | `0.687 ha` polygon area | materialized for review as proxy candidate only |

Read-smoke and QA:

- both curated outputs read successfully with geopandas;
- both outputs are EPSG:3005;
- both legal-current and non-legal-current OGMA outputs read back as
  multipolygon geometries;
- all curated output geometries are valid after clipping;
- output bounds are inside the accepted TFL 6 AOI bbox; and
- each output has a SHA-256 hash recorded in
  `data/source/tfl_6/ogma/ogma_source_manifest.json`.

Rule-critical field notes:

- legal-current OGMA retained `LEGAL_OGMA_PROVID`, `OGMA_TYPE`,
  `OGMA_PRIMARY_REASON`, `LEGALIZATION_FRPA_DATE`,
  `LEGALIZATION_OGAA_DATE`, `LAST_AMENDMENT_DATE`,
  `ENABLING_DOCUMENT_TITLE`, and `FEATURE_AREA_SQM`;
- legal-current clipped records include parseable `LEGALIZATION_FRPA_DATE`
  values from `2005-10-26` to `2016-10-13` and parseable
  `LAST_AMENDMENT_DATE` values from `2010-03-17` to `2018-06-05`; and
- non-legal-current OGMA retained `NON_LEGAL_OGMA_PROVID`, `OGMA_TYPE`,
  `OGMA_PRIMARY_REASON`, `ORIGINAL_DECISION_DATE`, `LAST_AMENDMENT_DATE`,
  and `FEATURE_AREA_SQM`, but the clipped features have no non-null original
  decision or amendment dates.

Recipe boundary:

- These layers are source-review artifacts only.
- Current legal OGMA dates, current-vs-2011 vintage handling, landscape-unit
  consistency, overlap order, and established-OGMA semantics remain unaccepted.
- Current non-legal OGMA remains a draft-OGMA proxy candidate only; the tiny
  clipped intersection should not be treated as the MP10 draft-OGMA row without
  explicit recipe-readiness review.

## First Recreation Materialization Pass

This pass materialized the public recreation geometry and attribution/context
candidates for source review only. It did not accept recreation buffer rules,
create recipe YAML, or run THLB netdown.

Command used:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'WHSE_FOREST_TENURE.FTEN_RECREATION_POLY_SVW' `
  'WHSE_FOREST_TENURE.FTEN_REC_TRAILS_SVW' `
  'WHSE_FOREST_TENURE.FTEN_REC_SITE_POINTS_SVW' `
  'WHSE_FOREST_TENURE.FTEN_REC_DTAILS_CLOSURES_SV' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --download-root runtime\bcdc_fetch\p2_1_recreation `
  --manifest-path runtime\logs\p2_1_recreation_bcdc_fetch_manifest.json
```

Notes:

- The bbox fetch returned `50` raw recreation polygon features, `3` raw trail
  features, `15` raw site-point features, and `18` raw details/closures
  features.
- Runtime WFS outputs were used as transient cache only. Polygon and line
  layers were clipped to the exact TFL 6 AOI; point layers were filtered to
  intersect the exact TFL 6 AOI. Curated outputs were written, read-smoked, and
  the transient cache was removed from `runtime/`.
- Curated output manifest:
  `data/source/tfl_6/recreation/recreation_source_manifest.json`.

| Source ID | Curated output | Raw bbox features | TFL 6 clipped/filtered features | Metric | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `recreation_polygons_tfl6` | `data/source/tfl_6/recreation/recreation_polygons_tfl6.gpkg`, layer `recreation_polygons_tfl6` | `50` | `26` | `187.868 ha` polygon area | materialized for review |
| `recreation_trails_tfl6` | `data/source/tfl_6/recreation/recreation_trails_tfl6.gpkg`, layer `recreation_trails_tfl6` | `3` | `3` | `1737.285 m` line length | materialized for review |
| `recreation_site_points_tfl6` | `data/source/tfl_6/recreation/recreation_site_points_tfl6.gpkg`, layer `recreation_site_points_tfl6` | `15` | `10` | `10` points | materialized for review |
| `recreation_details_closures_tfl6` | `data/source/tfl_6/recreation/recreation_details_closures_tfl6.gpkg`, layer `recreation_details_closures_tfl6` | `18` | `13` | `13` points | materialized for attribution/context review |

Read-smoke and QA:

- all four curated outputs read successfully with geopandas;
- all outputs are EPSG:3005;
- recreation polygons read back as multipolygon geometries;
- recreation trails read back as multiline geometries;
- site points and details/closures read back as point geometries;
- all curated output geometries are valid after clipping/filtering;
- output bounds are inside the accepted TFL 6 AOI bbox; and
- each output has a SHA-256 hash recorded in
  `data/source/tfl_6/recreation/recreation_source_manifest.json`.

Rule-critical field notes:

- polygon outputs retain `FOREST_FILE_ID`, `SECTION_ID`, `PROJECT_TYPE`,
  `MAP_LABEL`, `PROJECT_NAME`, `RECREATION_FEATURE_CODE`,
  `RESOURCE_FEATURE_IND`, `LIFE_CYCLE_STATUS_CODE`, `FILE_STATUS_CODE`,
  `RETIREMENT_DATE`, `PROJECT_ESTABLISHED_DATE`, `FEATURE_AREA_SQM`, and
  `FEATURE_LENGTH_M`;
- trail outputs retain `FOREST_FILE_ID`, `PROJECT_NAME`,
  `RECREATION_FEATURE_CODE`, `RESOURCE_FEATURE_IND`,
  `LIFE_CYCLE_STATUS_CODE`, `FILE_STATUS_CODE`, and `FEATURE_LENGTH_M`;
- site-point outputs retain `FOREST_FILE_ID`, `FEATURE_CODE`,
  `PROJECT_NAME`, `PROJECT_ESTABLISHED_DATE`, and activity/access/structure
  fields; and
- details/closures outputs retain `FOREST_FILE_ID`, `PROJECT_NAME`,
  `PROJECT_TYPE`, `CLOSURE_IND`, `CLOSURE_DATE`, `CLOSURE_TYPE`, and
  descriptive/context fields.

Recipe boundary:

- These layers are source-review artifacts only.
- Recreation class selection, retirement/status handling, point/line/polygon
  overlap order, and the MP10 10 m buffer rule remain unaccepted until
  recipe-readiness review.
- The details/closures layer is attribution/context only unless a later
  reviewed join or geometry rule accepts it for executable use.

## First LU/BEC Strata Materialization Pass

This pass materialized the landscape-unit and BEC public strata candidates for
source review only. It did not accept strategic Resource Management Zone or
Table 16 retention semantics, create recipe YAML, or run THLB netdown.

Command used:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW' `
  'WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --download-root runtime\bcdc_fetch\p2_1_strata `
  --manifest-path runtime\logs\p2_1_strata_bcdc_fetch_manifest.json
```

Notes:

- The bbox fetch returned `17` raw landscape-unit features and `146` raw BEC
  features.
- Runtime WFS outputs were used as transient cache only. Both layers were
  clipped to the exact TFL 6 AOI, written to curated source paths, read-smoked,
  and then removed from `runtime/`.
- Curated output manifest:
  `data/source/tfl_6/strata/strata_source_manifest.json`.
- Both curated layers sum to the accepted TFL 6 AOI area because they partition
  the AOI rather than remove landbase by themselves.

| Source ID | Curated output | Raw bbox features | TFL 6 clipped features | Metric | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `landscape_units_tfl6` | `data/source/tfl_6/strata/landscape_units_tfl6.gpkg`, layer `landscape_units_tfl6` | `17` | `13` | `217042.719 ha` polygon area | materialized for review |
| `bec_tfl6` | `data/source/tfl_6/strata/bec_tfl6.gpkg`, layer `bec_tfl6` | `146` | `107` | `217042.719 ha` polygon area | materialized for review |

Read-smoke and QA:

- both curated outputs read successfully with geopandas;
- both outputs are EPSG:3005;
- both outputs read back as multipolygon geometries;
- all curated output geometries are valid after clipping;
- output bounds are inside the accepted TFL 6 AOI bbox; and
- each output has a SHA-256 hash recorded in
  `data/source/tfl_6/strata/strata_source_manifest.json`.

Rule-critical field notes:

- clipped landscape units include `San Josef`, `Nahwitti`, `Lower Nimpkish`,
  `Marble`, `Neroutsos`, `Mahatta`, `Klaskish`, `Tahsish`, `Holberg`,
  `Tsulquate`, `Keogh`, `Nasparti`, and `Kashutl`;
- landscape-unit fields retain `LANDSCAPE_UNIT_ID`,
  `LANDSCAPE_UNIT_PROVID`, `LANDSCAPE_UNIT_NUMBER`,
  `LANDSCAPE_UNIT_NAME`, `BIODIVERSITY_EMPHASIS_OPTION`,
  `ORIGINAL_DECISION_DATE`, `LAST_AMENDMENT_DATE`,
  `ENABLING_DOCUMENT_TITLE`, and `FEATURE_AREA_SQM`;
- clipped BEC labels include `MH  mm 1`, `CWH vm 2`, `CWH vm 4`, `MH  mmp`,
  `CWH vm 3`, `CWH vh 2`, and `CWH vm 1`; and
- BEC fields retain `ZONE`, `SUBZONE`, `VARIANT`, `PHASE`,
  `NATURAL_DISTURBANCE`, `MAP_LABEL`, `BGC_LABEL`, `ZONE_NAME`,
  `SUBZONE_NAME`, `VARIANT_NAME`, `NATURAL_DISTURBANCE_NAME`, and
  `FEATURE_AREA_SQM`.

Recipe boundary:

- These layers are source-review artifacts only.
- LU/BEC can support OGMA, strategic RMZ, and Table 16 review, but neither
  layer is a netdown by itself.
- Strategic Resource Management Zone geometry/schema remains unresolved, but
  Table 16 execution is no longer blocked on it for the base teaching model:
  use the accepted aspatial stand-level-retention fallback, and reserve any
  strategic RMZ spatial treatment for a later enhancement/sensitivity lane.

## First DRA Roads Materialization Pass

This pass materialized the Digital Road Atlas MPAR public road-line candidate
for source review only. It did not accept existing-road class filters,
road-width buffers, future-road allowance treatment, recipe YAML, or THLB
netdown execution.

Command used:

```powershell
..\..\.venv\Scripts\python.exe -m femic data bcdc-fetch `
  'WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP' `
  --bbox '841375.750,580345.507,928480.824,639356.277' `
  --output-format gpkg `
  --download-root runtime\bcdc_fetch\p2_1_roads `
  --manifest-path runtime\logs\p2_1_roads_bcdc_fetch_manifest.json
```

Notes:

- The bbox fetch returned `18825` raw DRA MPAR features. FEMIC paged the WFS
  response because the bbox result exceeded one request page.
- Runtime WFS outputs were used as transient cache only. The layer was clipped
  to the exact TFL 6 AOI, written to a curated source path, read-smoked, and
  then removed from `runtime/`.
- Curated output manifest:
  `data/source/tfl_6/roads/roads_source_manifest.json`.

| Source ID | Curated output | Raw bbox features | TFL 6 clipped features | Metric | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `dra_roads_tfl6` | `data/source/tfl_6/roads/dra_roads_tfl6.gpkg`, layer `dra_roads_tfl6` | `18825` | `10706` | `4255862.907 m` line length | materialized for review |

Read-smoke and QA:

- the curated output read successfully with geopandas;
- output CRS is EPSG:3005;
- output reads back as multiline geometry;
- all curated output geometries are valid after clipping;
- output bounds are inside the accepted TFL 6 AOI bbox; and
- the output has a SHA-256 hash recorded in
  `data/source/tfl_6/roads/roads_source_manifest.json`.

Rule-critical field notes:

- clipped DRA fields retain `DIGITAL_ROAD_ATLAS_LINE_ID`, `FEATURE_TYPE`,
  `HIGHWAY_ROUTE_NUMBER`, `ROAD_NAME_FULL`, `ROAD_NAME_ALIAS1`,
  `ROAD_NAME_ALIAS2`, `ROAD_SURFACE`, `ROAD_CLASS`, `NUMBER_OF_LANES`,
  `DATA_CAPTURE_DATE`, `SEGMENT_LENGTH_2D`, `SEGMENT_LENGTH_3D`, and
  `FEATURE_LENGTH_M`;
- clipped `ROAD_CLASS` values are dominated by `unclassified` and `resource`,
  with smaller `local`, `highway`, `collector`, `trail`, `service`,
  `recreation`, `yield`, `driveway`, and `water` classes;
- clipped `ROAD_SURFACE` values are dominated by `rough` and `loose`, with
  smaller `unknown`, `paved`, `overgrown`, and `boat` classes; and
- clipped `FEATURE_TYPE` values are dominated by `Road`, with smaller `Trail`,
  `Bridge`, and `Virtual` records.

Recipe boundary:

- This layer is a source-review artifact only.
- Existing-road class filtering, road-width/buffer rules, overlap order, and
  treatment of trails/bridges/virtual records remain unaccepted until
  recipe-readiness review.
- Future-road allowance remains a separate MP10 Table 17 aspatial/context row
  and must not be mixed into the current existing-road overlay without a later
  scenario decision.

## Non-Goals

- No THLB recipe semantics were accepted in this slice.
- No recipe YAML was created.
- No THLB netdown execution was run.
- No model-input, ForestModel/XML, Matrix Builder, or Patchworks runtime work
  was started.

## P2.1 Closeout Review

P2.1 is complete as a source-layer materialization and fallback-decision lane.
The first executable THLB lane now has each source dependency classified as one
of: accepted local input, materialized-for-review source, P2.2 field-mapping
work, accepted aspatial fallback, context-only row, or deferred enhancement.

Closeout classification:

| Step | Closeout classification | Next owner |
| --- | --- | --- |
| `tfl6_nd_000` | accepted local AOI input | later recipes |
| `tfl6_nd_010` | accepted local VRI input; field mapping required | P2.2 / `#22` |
| `tfl6_nd_020` | DRA roads materialized for review; width/class rules still unaccepted | recipe-readiness review after P2.2 |
| `tfl6_nd_040` | accepted local VRI/VDYP input; field mapping required | P2.2 / `#22` |
| `tfl6_nd_060` | operability design lane closed; no public TFL 6 operability geometry accepted | later recipe/proxy work from `#20` design |
| `tfl6_nd_080` | FWA streams/lakes/wetlands materialized for review; shoreline precision and RMA/RRZ/RMZ rules still unaccepted | recipe-readiness review |
| `tfl6_nd_090` | approved UWR materialized for review | recipe-readiness review |
| `tfl6_nd_100` | legal-current OGMA materialized for review, with vintage warning | recipe-readiness review |
| `tfl6_nd_110` | non-legal-current OGMA materialized as proxy candidate only; MP10 draft-OGMA fallback remains available | recipe-readiness review |
| `tfl6_nd_120` | approved WHA materialized for review | recipe-readiness review |
| `tfl6_nd_130` | recreation polygon/line/point/context layers materialized for review | recipe-readiness review |
| `tfl6_nd_140` | accepted local VRI/VDYP input; species-leading field mapping required | P2.2 / `#22` |
| `tfl6_nd_150` | accepted aspatial/proxy fallback; do not seek sensitive geometry | later recipe-readiness review |
| `tfl6_nd_180` | accepted aspatial MP10 Table 16 stand-level-retention fallback | later recipe-readiness review |
| `tfl6_nd_200` | context-only long-term future-road allowance | later scenario/model-time decision |

P2.1 does not need another source-download child issue before P2.2. Remaining
work is mapping, recipe-readiness review, and later enhancement/sensitivity
design:

- P2.2 / `#22` owns field profiling for the accepted 2025 R1 and VDYP7 inputs.
- Strategic RMZ spatial replacement is documented as an advanced student
  challenge and is not a base-lane blocker.
- DEM/slope materialization for operability remains a later planned
  materialization issue, not a P2.1 prerequisite.
- No source layer has been promoted into executable THLB recipe YAML by this
  closeout.
