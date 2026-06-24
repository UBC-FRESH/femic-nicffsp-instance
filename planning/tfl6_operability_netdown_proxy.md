# TFL 6 Operability Netdown Proxy and Sensitivity Lane

## Purpose

Governing issue: `#20`.

This note records the P2.1a operability design lane. It is planning-only: no
DEM data is materialized, no slope raster is built, no recipe YAML is created,
and no THLB netdown is executed.

Operability should not be treated as a hidden, permanently locked aspatial
deduction. The base-case teaching model still needs rationale-backed
assumptions, but operability is also a strong candidate for student sensitivity
work because it controls which stands enter or leave the THLB through physical
access, economic access, terrain, yarding-system, and timber-value assumptions.

## Source Evidence

### MP10 Information Package

The MP10 information package defines TFL 6 operability classes as a function of
harvesting system, timber quality, terrain stability, and economic
accessibility. The 1999 reclassification was approved by the MoFR Port McNeill
Forest District in September 1998. It separated physically inaccessible areas
from economically marginal conventional and heli areas
(`Ocm`/`Ohm`). The MP10 deduction from productive forest was `12,438 ha`, made
up of `11,600 ha` physically inoperable, `424 ha` marginal conventional, and
`415 ha` marginal heli. The operable subtotal was `134,621 ha`, including
`129,221 ha` conventional and `5,400 ha` heli.

Local extracted-text anchors:

- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:655`
- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:678`

MP10 also says there was no additional terrain-stability netdown beyond areas
identified as inoperable. Class IV and V terrain remained in the THLB in
material proportions, and spatial logging history records showed harvesting had
occurred in both classes. This means "unstable terrain" was not a simple
standalone exclusion in the base-case landbase; it was partly embedded in the
operability inventory and partly handled as sensitivity/context.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:694`

The MP10 analysis dataset assigned logging system from operability class plus
slope class: conventionally operable areas with slope from `0%` to `30%` were
assumed ground-based, conventionally operable areas on steeper slopes were
assumed cable, and heli-operable areas occurred across all slope classes.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_2011_ip.txt:2502`

MP10 minimum-harvest criteria were also tied to harvesting system. The analysis
report says minimum criteria included average stand DBH by harvest system plus
minimum volume per hectare; ground-based stands used `30 cm`, while cable and
heli criteria were higher and were explicitly tested in sensitivity analysis.

Local extracted-text anchors:

- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:9723`
- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:10019`

MP10 Section 5.3 identifies economic access as a major uncertainty. It says the
dataset used a broad economic-operability allowance based on inventory
information rather than detailed cost/value modelling, and that low-volume
mature forest in lower height and stocking classes classified with economic
constraints was excluded in the base case.

Local extracted-text anchors:

- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:9940`
- `reference/extracted_text/tfl_6_mngment_plan_10_2011.txt:9997`

### MP9 Information Package

MP9 Appendix III gives stronger stand-level clues for reconstructing a teaching
proxy. It describes operability classes using the same general factors:
harvesting system, timber quality, terrain stability, and economic
accessibility. It also reports a 1999 operability reclassification and a
deduction of `12,579 ha` from productive forest, split between physically
inoperable and economically constrained classes.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_9_01_appendix_1_7.txt:1267`

The MP9 yarding-system forest-cover constraints are the most useful proxy
evidence found so far:

- conventional operability included height class `4+`, height class `3` with
  cedar, cypress, Douglas-fir, or spruce as primary species, and nearby height
  class `3` hemlock/balsam types;
- conventional-economic classes included height class `3` hemlock/balsam not
  near better conventional types, stocking class `3` with preferred species,
  and deciduous stands based on local knowledge;
- heli classes used similar height/species/proximity logic for non-conventional
  yarding;
- heli-economic classes included height class `3` preferred species away from
  better heli/conventional types, but excluded some stocking-class `3`
  combinations and pure hemlock/balsam height class `3` stands;
- economically inoperable forest included mature height classes `1` and `2`,
  pure hemlock/balsam height class `3` stocking class `3` open stands, and
  pine-dominant stands; and
- physically inoperable lands included non-productive types, major land-feature
  limitations, and extreme terrain or distance/access constraints.

Local extracted-text anchor:

- `reference/extracted_text/tfl_6_mngment_plan_9_01_appendix_1_7.txt:4993`

## Available Current Inputs

The accepted current-AOI inventory surfaces already provide several useful
attributes for a proxy design:

- 2025 VRI R1 clipped polygon layer:
  `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`.
- 2025 VDYP7 polygon table:
  `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet`.
- 2025 VDYP7 layer table:
  `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet`.

Candidate VRI/VDYP fields observed during previous read-smoke and field
inspection include:

- height: `proj_height_class_cd_1`, `proj_height_class_cd_2`,
  `est_height_spp1`, `est_height_spp2`, `lorey_height_75`;
- species: `species_cd_1` through `species_cd_6`,
  `species_pct_1` through `species_pct_6`, `line_3_tree_species`;
- stand structure and productivity clues: `crown_closure_class_cd`,
  `proj_age_class_cd_1`, `proj_age_class_cd_2`, `line_4_classes_indexes`,
  `site_index`;
- volume: `live_stand_volume_125`, `live_stand_volume_175`,
  `live_stand_volume_225`, `ws_vol_per_ha_75`, `ws_vol_per_ha_125`,
  `cu_vol_per_ha_125`; and
- join key: `feature_id`.

These surfaces do not carry the historical WFP operability polygons, terrain
stability classes, road-cost model, or yarding-system class directly. A proxy
therefore needs to combine inventory attributes with derived GIS evidence and
benchmark calibration.

## Proxy Design Direction

### Base-Case Lane

The base-case lane should remain benchmark-aware but not purely aspatial. A
reasonable first design is:

1. Treat recovered 1999 WFP operability geometry, if found, as preferred
   evidence.
2. If geometry is not found, build a VRI/VDYP-informed candidate exclusion
   surface using MP9/MP10 inventory clues:
   - low height classes;
   - hemlock/balsam-dominated low/open stands;
   - pine-dominant stands;
   - low volume per hectare;
   - stocking/open-stand proxy from VRI class fields; and
   - harvest-system cost pressure derived from slope and possibly access.
3. Calibrate the base-case removal against the MP10 Table 8 / adjusted
   current-AOI benchmark deduction, while documenting any mismatch.
4. Keep the calibrated proxy explicitly provisional for a teaching model, not
   a claim that the historical WFP operability inventory has been reproduced.

### Sensitivity Lane

The sensitivity lane should expose one or more parameters that students can
vary to move stands into or out of THLB. Candidate parameters include:

- minimum height class for economic operability;
- species group handling for hemlock/balsam, cedar/cypress/Douglas-fir/spruce,
  pine, and deciduous-leading stands;
- minimum volume per hectare by harvest-system proxy;
- threshold for classifying a stand as steep/cable-pressure based on DEM
  slope;
- threshold for classifying a stand as heli/high-cost candidate;
- whether marginal economic classes are included, excluded, or partially
  discounted; and
- whether heli stands are included with a harvest-flow constraint, excluded, or
  treated as a separate scenario lane.

This matches the TSR pattern where THLB netdown and timber-supply sensitivity
analysis commonly tests landbase, operability, volume, and minimum-harvest
assumptions rather than locking all uncertainty into one base-case surface.

## DEM and Slope Workflow

A later implementation issue should use FEMIC's data-layer discovery functions
to resolve and materialize an appropriate DEM source. The intended workflow is:

1. Resolve a public DEM authority and record publication/version metadata.
2. Materialize only the TFL 6 AOI subset or a minimal AOI-plus-buffer subset.
3. Reproject/align to the accepted EPSG:3005 TFL 6 working CRS as needed.
4. Derive a percent-slope raster clipped to the TFL 6 AOI.
5. Compute zonal statistics by VRI stand polygon, keyed by `feature_id`.
6. Store stand-level metrics such as:
   - mean slope;
   - maximum slope;
   - `p_slope_ge_30`;
   - `p_slope_ge_50`; and
   - optional area-weighted slope-bin proportions.
7. Test rules of the form:
   - `p_slope_ge_X >= Y` for steep/cable-pressure classification;
   - `p_slope_ge_X >= Y` plus low volume or low preferred-species signal for
     marginal economic classification; and
   - alternate `X` and `Y` values as student sensitivity inputs.

No DEM or slope artifact is accepted by this planning note.

## Open Decisions

- Whether the first executable base-case proxy should be a calibrated marginal
  removal, an explicit rule-only removal, or a hybrid.
- How to parse `line_4_classes_indexes` into a defensible stocking/open-stand
  signal.
- How to express the MP9 "near better operability types" concept. Possible
  proxies include adjacency, distance to higher-quality stands, distance to
  roads, or no first-lane implementation.
- Whether road distance/access should be part of P2.1a or a later source-layer
  enhancement after Digital Road Atlas materialization.
- How closely the adjusted Table 8 benchmark should constrain the teaching
  base case when the active current AOI includes post-2011 TFL 6 boundary
  additions.

## Non-Goals

- No DEM fetch or clipping.
- No slope raster or zonal-stat computation.
- No recipe YAML.
- No THLB execution.
- No model-input, ForestModel/XML, Matrix Builder, or Patchworks runtime work.
