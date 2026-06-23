# 2025 VRI Data Collection Plan

## Purpose

Phase 1 now includes a source-data collection task for the latest provincial
VRI packages needed before the NICF FSP base AOI inventory can be generated.
The extraction mask remains the accepted FSP AOI: FDU 1 Holberg, FDU 2 Keogh,
and FDU 3 Marble from `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp`.

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

Expected direct package URLs:

- `https://pub.data.gov.bc.ca/datasets/02dba161-fdb7-48ae-a4bb-bd6ef017c36d/current/VEG_COMP_LYR_R1_POLY_2025.gdb.zip`
- `https://pub.data.gov.bc.ca/datasets/02dba161-fdb7-48ae-a4bb-bd6ef017c36d/current/VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip`

## Target Materialization Paths

Accepted target paths for the source archives:

- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb.zip`
- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip`

If downstream FEMIC code requires extracted geodatabases instead of zip inputs,
the extracted directories should stay under the same vintage directory:

- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb/`
- `external/femic-public-data/data/bc/vri/2025/VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb/`

## Acceptance Boundary

`P1.5` is complete when:

- official 2025 R1 and VDYP7 package metadata is recorded;
- both source archives are materialized under the accepted public-data
  convention or an explicitly documented successor convention;
- file size and checksum metadata is recorded for both packages;
- a read smoke records geodatabase/layer names, feature counts or equivalent
  read evidence, CRS, and any extraction/runtime path decision;
- DataLad/git-annex publication status is recorded so a fresh environment can
  materialize the same files; and
- the downstream FDU 1/2/3 cookie-cutter extraction boundary is documented.

No model-input bundle, Patchworks runtime package, or cedar/expansion design
work should start inside this data-collection task.
