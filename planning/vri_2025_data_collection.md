# 2025 VRI Data Collection Plan

## Purpose

Phase 1 now includes a source-data collection task for the latest provincial
VRI packages needed before the NICF FSP base AOI inventory can be generated.
The original extraction mask was the accepted FSP AOI: FDU 1 Holberg, FDU 2
Keogh, and FDU 3 Marble from `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp`.
As of the TFL 6 AOI pivot, that boundary remains provenance only; the active
2025 VRI extraction handoff is governed by `#6`.

This task is tracked as `P1.5` in issue `#5`.

## Existing FEMIC Convention

FEMIC already uses vintage-keyed provincial VRI paths under the public-data
mirror:

- `external/femic-public-data/data/bc/vri/2019/`
- `external/femic-public-data/data/bc/vri/2024/`

The core FEMIC docs and bootstrap code use the same package family for 2024:

- `VEG_COMP_LYR_R1_POLY_2024.gdb.zip`
- `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2024.gdb.zip`

The NICF 2025 collection task should preserve that convention with a new
`2025` vintage directory rather than inventing an instance-local source cache.

## 2025 Source Packages

| Role | BCDC package id | Expected package |
| --- | --- | --- |
| Provincial VRI layer 1 rank 1 polygon source | `vri-2025-forest-vegetation-composite-rank-1-layer-r1-` | `VEG_COMP_LYR_R1_POLY_2025.gdb.zip` |
| Provincial VDYP7 input polygon/layer source | `vri-2025-variable-density-yield-projection-7-vdyp7-input-polygon` | `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip` |

## Official Metadata Snapshot

Metadata retrieval date: 2026-06-23.

| Role | BCDC title | BCDC package UUID | Metadata modified | Resource name | Resource UUID | Format |
| --- | --- | --- | --- | --- | --- | --- |
| R1 polygon source | `VRI - 2025 - Forest Vegetation Composite Rank 1 Layer (R1)` | `2ebb35d8-c82f-4a17-9c96-612ac3532d55` | `2026-05-27T12:40:42.561633` | `veg_comp_lyr_r1_poly_2025.gdb.zip` | `d91bf7df-7c5f-49e0-b206-d3a87bc354f9` | `fgdb` |
| VDYP7 polygon/layer source | `VRI - 2025 - Variable Density Yield Projection 7 (VDYP7) Input  Polygon` | `57513aaa-c0a6-41a9-b2a8-b980b1604ee6` | `2026-05-26T15:39:40.666083` | `veg_comp_VDYP7_input_poly_and_layer_2025.gdb.zip` | `f95d6f4d-3b93-4adc-a81e-6e38b06ca0de` | `other` |

Both BCDC packages are managed by the Forest Analysis and Inventory Branch.
The R1 package records BCDC license id `2`; the VDYP7 polygon package records
BCDC license id `22`. Package size and file checksum metadata were not present
in the BCDC API response and must be recorded after materialization.

Expected direct package URLs:

- `https://pub.data.gov.bc.ca/datasets/02dba161-fdb7-48ae-a4bb-bd6ef017c36d/current/VEG_COMP_LYR_R1_POLY_2025.gdb.zip`
- `https://pub.data.gov.bc.ca/datasets/02dba161-fdb7-48ae-a4bb-bd6ef017c36d/current/VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip`

## Target Materialization Paths

Accepted target paths for the source archives:

- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb.zip`
- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip`

## Materialization Snapshot

Materialization date: 2026-06-23.

Public-data commit: `348d9b60529e3a0160672048fc33e4083f2128fb`.

| Package | Size bytes | Annex key checksum | Zip entries | Zip root | CRC test |
| --- | ---: | --- | ---: | --- | --- |
| `VEG_COMP_LYR_R1_POLY_2025.gdb.zip` | `4168172794` | `MD5E-s4168172794--8d53ec1653390dcd1f035d8c011af9e0.gdb.zip` | `46` | `VEG_COMP_LYR_R1_POLY_2025.gdb` | passed |
| `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip` | `403304406` | `MD5E-s403304406--48cbbb4577aa0ae52a71d9470d4a4205.gdb.zip` | `48` | `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb` | passed |

`git annex whereis` reports one local copy for each archive in the current
public-data checkout. Arbutus/publication status remains open until the next
publication check records whether these annex keys are available from the
public remote.

If downstream FEMIC code requires extracted geodatabases instead of zip inputs,
the extracted directories should stay under the same vintage directory:

- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb/`
- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb/`

## Read-Smoke Snapshot

Read-smoke date: 2026-06-23.

The source packages were inspected directly from the zipped file geodatabases
using `pyogrio` / GDAL virtual zip paths. No extracted geodatabase directories
were required for this smoke check.

| Package | Geodatabase root | Layer/table | Geometry type | CRS | Feature/row count | Field count | Read evidence |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| `VEG_COMP_LYR_R1_POLY_2025.gdb.zip` | `VEG_COMP_LYR_R1_POLY_2025.gdb` | `VEG_COMP_LYR_R1_POLY` | `MultiPolygon` | `EPSG:3005` | `7154522` | `192` | `pyogrio.list_layers`, `pyogrio.read_info`, and one-row read passed |
| `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip` | `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb` | `VEG_COMP_VDYP7_INPUT_POLY` | non-spatial table | n/a | `7104182` | `47` | `pyogrio.list_layers`, `pyogrio.read_info`, and one-row read passed |
| `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip` | `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb` | `VEG_COMP_VDYP7_INPUT_LAYER` | non-spatial table | n/a | `7608054` | `42` | `pyogrio.list_layers`, `pyogrio.read_info`, and one-row read passed |

First-field smoke:

- R1 layer first fields include `FEATURE_ID`, `MAP_ID`, `POLYGON_ID`,
  `OPENING_IND`, `FEATURE_CLASS_SKEY`, `POLYGON_AREA`,
  `NON_PRODUCTIVE_DESCRIPTOR_CD`, `NON_PRODUCTIVE_CD`, and `BCLCS_LEVEL_1`.
- VDYP7 polygon table first fields include `FEATURE_ID`, `MAP_ID`,
  `POLYGON_NUMBER`, `ORG_UNIT`, `TSA_NAME`, `TFL_NAME`,
  `INVENTORY_STANDARD_CODE`, `TSA_NUMBER`, `BEC_ZONE_CODE`, and
  `NON_PRODUCTIVE_DESCRIPTOR_CD`.
- VDYP7 layer table first fields include `FEATURE_ID`,
  `TREE_COVER_LAYER_ESTIMATED_ID`, `MAP_ID`, `POLYGON_NUMBER`,
  `LAYER_LEVEL_CODE`, `VDYP7_LAYER_CD`, `FOREST_COVER_RANK_CODE`,
  `SPECIES_CD_1`, `SPECIES_PCT_1`, `SPECIES_CD_2`, and `SPECIES_PCT_2`.

The accepted downstream TFL 6 AOI extraction is already recorded under `#6` and
uses the same source archives. `P1.5` still needs public-data remote
publication status before the source-data collection task can close.

## Acceptance Boundary

`P1.5` is complete when:

- official 2025 R1 and VDYP7 package metadata is recorded; (complete)
- both source archives are materialized under the accepted public-data
  convention or an explicitly documented successor convention; (complete)
- file size and checksum metadata is recorded for both packages; (complete)
- a read smoke records geodatabase/layer names, feature counts or equivalent
  read evidence, CRS, and any extraction/runtime path decision; (complete)
- DataLad/git-annex publication status is recorded so a fresh environment can
  materialize the same files; and
- the downstream active-AOI extraction handoff is documented; the earlier FDU
  1/2/3 cookie-cutter boundary is superseded by the TFL 6 pivot in `#6`.

No model-input bundle, Patchworks runtime package, or cedar/expansion design
work should start inside this data-collection task.
