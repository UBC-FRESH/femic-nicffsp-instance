# TFL 6 AOI Pivot and 2025 VRI Input Layers

## Purpose

The active NICF teaching-case AOI has pivoted from the original FDU 1/2/3
bootstrap boundary to Tree Farm Licence 6. This note defines the planned input
layer work before any THLB netdown or Patchworks model compilation depends on
the new AOI.

Governing issue: `#6`.

## AOI Decision

The active model AOI is now TFL 6.

The earlier FDU 1 Holberg, FDU 2 Keogh, and FDU 3 Marble boundary remains
tracked source provenance for the initial FRST 558/NICF FSP bootstrap lane, but
it is superseded as the active inventory extraction boundary.

## Boundary Source

Authoritative candidate:

- BCDC / OpenMaps object: `WHSE_ADMIN_BOUNDARIES.FADM_TFL`
- WFS type name: `pub:WHSE_ADMIN_BOUNDARIES.FADM_TFL`
- Selection filter: `FOREST_FILE_ID='TFL6'`

Exploratory query evidence from 2026-06-23:

- Returned feature count: `182`
- CRS: `EPSG:3005`
- Total union area: `217042.719 ha`
- Bounds: `(841375.750, 580345.507, 928480.824, 639356.277)`
- Effective date: `2020-03-01`
- Updated date: `2020-04-15`
- Retirement date: none returned

The planned tracked boundary output is:

- `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`
- layer: `tfl_6_boundary`

Materialized boundary snapshot from `P1.6a`:

- Retrieval/materialization date: 2026-06-23
- Source service:
  `https://delivery.maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_whse_admin_boundaries/MapServer/30`
- Source query:
  `FOREST_FILE_ID='TFL6'`, `outSR=3005`
- Catalogue metadata caveat: the BCDC package record exposes a metadata-created
  timestamp and service/resource modified timestamps, but no clean
  `date_published` value was found in the package JSON during planning. Treat
  the layer as current service data with feature-level dates recorded below.
- Tracked output: `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`
- Layer: `tfl_6_boundary`
- SHA-256:
  `b581b378f16ed168e918699b6abc34a38fda7c2aa13e27c944aa2eeb78561d42`
- Feature count: `182`
- CRS: `EPSG:3005`
- Geometry validity after normalization: `182` valid, `0` invalid
- Source invalid geometry normalization: `make_valid` applied to one source
  feature, `feature_id=309`, `objectid=19345`; union area change rounded to
  `0.000 ha`
- Total union area: `217042.719 ha`
- Bounds: `(841375.750, 580345.507, 928480.824, 639356.277)`
- Effective date: `2020-03-01T00:00:00Z`
- Updated date: `2020-04-15T14:17:42Z`
- Retirement date: none returned
- Field normalization: source fields lowercased; ArcGIS `GEOMETRY.AREA` and
  `GEOMETRY.LEN` stored as `geometry_area` and `geometry_len`
- Run-profile boundary path switched to this GeoPackage in
  `config/run_profile.nicffsp.yaml`

## Provincial 2025 Inputs

The source archives already materialized under `external/femic-public-data` are:

- `data/bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb.zip`
- `data/bc/vri/2025/VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip`

Read-smoke observations:

- `VEG_COMP_LYR_R1_POLY_2025.gdb.zip`
  - layer: `VEG_COMP_LYR_R1_POLY`
  - geometry type: `MultiPolygon`
  - CRS: `EPSG:3005`
  - provincial feature count reported by GDAL: `7154522`
- `VEG_COMP_VDYP7_INPUT_POLY_AND_LAYER_2025.gdb.zip`
  - table: `VEG_COMP_VDYP7_INPUT_POLY`
  - table: `VEG_COMP_VDYP7_INPUT_LAYER`
  - GDAL reports these as non-spatial tables in the FileGDB package.

## Planned TFL 6 Input Layer Outputs

Store instance-local clipped/filter-ready inputs under:

- `data/input/tfl_6/`

Planned outputs:

| Role | Planned path | Method |
| --- | --- | --- |
| TFL 6 AOI boundary | `data/source/tfl_6/aoi/tfl_6_boundary.gpkg` | Fetch `WHSE_ADMIN_BOUNDARIES.FADM_TFL` where `FOREST_FILE_ID='TFL6'`; normalize to lowercase fields. |
| TFL 6 clipped 2025 R1 polygons | `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` | Read provincial R1 with TFL 6 bbox, exact-clip to dissolved TFL 6 geometry, preserve stand identifiers. |
| TFL 6 VDYP7 polygon table | `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet` | Filter `VEG_COMP_VDYP7_INPUT_POLY` to the clipped TFL 6 feature-id set. |
| TFL 6 VDYP7 layer table | `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` | Filter `VEG_COMP_VDYP7_INPUT_LAYER` to the same feature-id set. |
| Input-layer manifest | `data/input/tfl_6/input_layers_manifest.json` | Record source paths, source checksums/annex keys, row counts, CRS, bounds, area, and key-integrity checks. |

## Materialized 2025 R1 Clip

`P1.6b` materialized the TFL 6-clipped 2025 R1 polygon input.

Output:

- path: `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`
- layer: `vri_2025_r1_poly_tfl6`
- clip manifest: `data/input/tfl_6/vri_2025_r1_poly_tfl6_clip_manifest.json`
- SHA-256:
  `8146651b1a3d2c2edf7f433897f082e9016722116748d61056697e456b68f27c`
- file size: `52469760` bytes

Source and method:

- source archive:
  `external/femic-public-data/data/bc/vri/2025/VEG_COMP_LYR_R1_POLY_2025.gdb.zip`
- source layer: `VEG_COMP_LYR_R1_POLY`
- source feature count: `7154522`
- boundary: `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`,
  layer `tfl_6_boundary`
- method: bbox-read the provincial R1 source using the TFL 6 bounds, then exact
  intersection with the dissolved TFL 6 boundary

QA:

- bbox-read feature count: `42297`
- intersecting feature count before exact clip: `26959`
- output feature count: `26959`
- CRS: `EPSG:3005`
- geometry type after write/read: `MultiPolygon`
- geometry validity after write/read: `26959` valid, `0` invalid
- source geometry repairs before clipping: `33`
- non-polygonal intersections repaired: `0`
- clipped bounds: `(841375.750, 580345.507, 928480.824, 639356.277)`
- source intersecting area before exact clip: `298604.489813 ha`
- clipped output area: `217042.718950 ha`
- boundary area: `217042.718950 ha`

VDYP join-key handoff:

- `feature_id`: `26959` non-null, `26959` unique, `0` duplicates
- `map_id`: `26959` non-null, `30` unique
- `polygon_id`: `26959` non-null, `26955` unique
- preferred VDYP join-key candidate for `P1.6c`: `feature_id`

## Validation Requirements

The `#6` implementation should record:

- TFL 6 boundary feature count, CRS, bounds, area, effective date, and source
  filter;
- clipped R1 feature count, CRS, bounds, total area, and geometry validity;
  (complete for R1 clip)
- the exact feature-id field used to link R1 to the VDYP7 tables; (candidate:
  `feature_id`)
- row counts for the filtered VDYP7 polygon and layer tables;
- key-integrity checks:
  - every retained VDYP7 polygon row belongs to a retained TFL 6 R1 feature;
  - every retained VDYP7 layer row belongs to a retained VDYP7 polygon feature;
  - no duplicate records violate the expected source table keys;
- whether clipped outputs are tracked directly in the instance repo or moved to
  `external/femic-public-data` if they are too large for normal git.

## Non-Goals

- Do not delete the FDU 1/2/3 source files.
- Do not start THLB netdown recipe extraction inside the clipping issue.
- Do not start Patchworks runtime-package compilation from these inputs until
  the input-layer manifest has been accepted.
