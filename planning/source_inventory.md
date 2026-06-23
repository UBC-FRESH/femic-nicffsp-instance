# Source Inventory

## Initial Payloads

| Tracked path | Original uploaded filename | SHA-256 | Notes |
| --- | --- | --- | --- |
| `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` | `NICF FSP amend #3 spatial.zip` | `de3776cda77d056390ffdee03aed6e3a914501a4c2c8adc34ba8481e02bbabcc` | Raw provenance for the pre-pivot FSP AOI extraction. |
| `data/source/nicf_fsp/bcgw_lu_clip_2026_06.zip` | `BCGW_LU_Clip_06-2026.zip` | `03477133df626104a60e07699fdb6025a712af1a0a6a710ca5958d44792c0a47` | Raw provenance for the accepted LU reference extraction. |
| `data/source/nicf_fsp/nicf_forest_stewardship_plan_2020.pdf` | `NICF-Forest-Stewardship-Plan-2020-2.pdf` | `9bccd37a9666b4b1262f54afcb152bbbe9ec0475435cdc53434656194bdc3895` | FSP document used to interpret AOI/LU context and management constraints. |

## Interpretation Boundary

These files are raw source payloads only. The accepted extracted source layers
are tracked separately under stable lowercase paths.

As of the TFL 6 AOI pivot, this source inventory is provenance for the original
NICF FSP bootstrap lane. The active target AOI is TFL 6 and is governed by
`P1.6`.

Do not point FEMIC runtime config at zip payloads as if they were ready-to-use
case inputs.

## NICF FSP Amendment Spatial Zip Inventory

Inspection date: 2026-06-23

Source:
`data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip`

Zip contents:

| Path in zip | Size bytes | Notes |
| --- | ---: | --- |
| `NICF FSP Shapefiles/NICF_FDU_2024.dbf` | 7148 | Attribute table |
| `NICF FSP Shapefiles/NICF_FDU_2024.prj` | 466 | Projection metadata |
| `NICF FSP Shapefiles/NICF_FDU_2024.sbn` | 204 | Spatial index |
| `NICF FSP Shapefiles/NICF_FDU_2024.sbx` | 132 | Spatial index |
| `NICF FSP Shapefiles/NICF_FDU_2024.shp` | 686436 | Polygon geometry |
| `NICF FSP Shapefiles/NICF_FDU_2024.shx` | 148 | Shape index |

Layer summary:

- Candidate layer: `NICF FSP Shapefiles/NICF_FDU_2024.shp`
- Feature count: `6`
- Geometry type: `Polygon`
- CRS: `EPSG:3005`
- Bounds: `(849931.438, 580387.812, 928536.312, 653037.313)`
- Geometry validity: `6` valid, `0` invalid
- Total measured area in EPSG:3005: `204162.510 ha`

Feature labels and measured area:

| Label | Landscape unit name | Biodiversity emphasis | Area ha |
| --- | --- | --- | ---: |
| `FDU  1 Holberg LU` | Holberg | Low | 41649.362 |
| `FDU 2 Keogh LU` | Keogh | Low | 50693.492 |
| `FDU 3 Marble LU` | Marble | Intermediate | 55455.538 |
| `FDU 4 Nahwitti LU` | Nahwitti | Intermediate | 17477.455 |
| `FDU 5 Tsulquate LU` | Tsulquate | Intermediate | 23205.472 |
| `FDU 6 Shushartie LU` | Shushartie | High | 15681.191 |

Interpretation:

- This zip contains a single shapefile family, but that shapefile is not a
  single dissolved AOI polygon. It is a six-feature FDU/LU-style layer.
- Treat `NICF_FDU_2024.shp` as the raw amendment source for the pre-pivot
  three-FDU FSP AOI extraction documented below.
- Do not point runtime config directly at the raw zip payload.

## BCGW Landscape Unit Clip Zip Inventory

Inspection date: 2026-06-23

Source:
`data/source/nicf_fsp/bcgw_lu_clip_2026_06.zip`

Order notes:

- Order ID: `2572861`
- Order date: `20260623`
- Feature type: `Landscape Units of British Columbia - Current`
- Source directory noted by order file: `RMP_LU_SVW`

Zip contents:

| Path in zip | Size bytes | Notes |
| --- | ---: | --- |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.cpg` | 5 | Encoding metadata |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.dbf` | 25774 | Attribute table |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.prj` | 489 | Projection metadata |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.shp` | 2122796 | Polygon geometry |
| `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.shx` | 316 | Shape index |
| `Contents of Order.txt` | 303 | DataBC order summary |
| `README.txt` | 426 | DataBC download/licence notice |
| `licence.txt` | 275 | BC Data Catalogue licence notice |
| `WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW_metadata.json` | 9494 | BCGW metadata |
| `WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW_metadata.html` | 15194 | BCGW metadata |

Layer summary:

- Candidate layer: `RMP_LANDSCAPE_UNIT_SVW/RMP_LU_SVW_polygon.shp`
- Feature count: `27`
- Geometry type: `Polygon`
- CRS: `EPSG:3005`
- Bounds: `(778342.188, 528411.500, 990334.625, 680314.312)`
- Geometry validity: `27` valid, `0` invalid
- Total measured area in EPSG:3005: `1489608.005 ha`

Landscape unit names and measured area:

| LU name | Biodiversity emphasis | Area ha |
| --- | --- | ---: |
| Artlish | Intermediate | 16207.928 |
| Bonanza | Intermediate | 45710.608 |
| Brooks | Low | 38203.204 |
| Broughton | Low | 87908.649 |
| Eliza | Low | 56765.240 |
| Gilford | Low | 92764.025 |
| Holberg | Low | 45020.737 |
| Kaouk | Intermediate | 29656.299 |
| Kashutl | Low | 91834.101 |
| Keogh | Low | 64281.620 |
| Klaskish | High | 28848.336 |
| Lower Nimpkish | Low | 82079.594 |
| Mahatta | Low | 59062.085 |
| Malcolm | Low | 41731.272 |
| Marble | Intermediate | 56286.499 |
| Nahwitti | Intermediate | 43172.007 |
| Nasparti | Low | 21213.956 |
| Neroutsos | Low | 31079.820 |
| Nigei | Low | 46468.310 |
| San Josef | Intermediate | 195967.476 |
| Shushartie | High | 20285.114 |
| Tahsish | Intermediate | 28772.463 |
| Tsitika | High | 35910.103 |
| Tsulquate | Intermediate | 25638.715 |
| Upper Nimpkish | Intermediate | 120083.281 |
| Walker | NA | 64856.499 |
| Zeballos | Low | 19800.065 |

Overlap with the `NICF_FDU_2024` AOI candidate:

| FDU candidate name | Matching BCGW LU | FDU candidate area ha | Full LU area ha | Difference ha |
| --- | --- | ---: | ---: | ---: |
| Holberg | Holberg | 41649.362 | 45020.737 | 3371.375 |
| Keogh | Keogh | 50693.492 | 64281.620 | 13588.129 |
| Marble | Marble | 55455.538 | 56286.499 | 830.961 |
| Nahwitti | Nahwitti | 17477.455 | 43172.007 | 25694.552 |
| Shushartie | Shushartie | 15681.191 | 20285.114 | 4603.923 |
| Tsulquate | Tsulquate | 23205.472 | 25638.715 | 2433.244 |

Interpretation:

- The LU zip is a broader BCGW landscape-unit clip with `27` full LU features,
  not a narrow three-LU package.
- The pre-pivot canonical LU reference context for this instance is the three
  BCGW LU records named by the FSP: Holberg, Keogh, and Marble.
- The remaining 24 BCGW LU records stay in the raw zip as provenance/context,
  not as tracked canonical runtime inputs.
- Each pre-pivot FSP AOI feature is equal to or smaller than its corresponding
  full BCGW LU, so the FDU surface was treated as the bootstrap modelling
  boundary and the LU reference subset as context for FSP interpretation.

## FSP PDF Cross-Check

Inspection date: 2026-06-23

Source:
`data/source/nicf_fsp/nicf_forest_stewardship_plan_2020.pdf`

Text extraction:

- Tool: `pypdf`
- Page count: `29`
- Search terms: `FDU`, `Forest Development Unit`, `Holberg`, `Keogh`,
  `Marble`, `Nahwitti`, `Shushartie`, `Tsulquate`, `K3Z`

Key PDF evidence:

| PDF page | Evidence |
| ---: | --- |
| 8 | The FSP applies to Community Forest Agreement `K3Z` and says there are three proposed FDUs. It also says FDUs are meant to follow Landscape Unit boundaries where they overlap the tenure boundary and form a logical planning area. |
| 9 | The FSP lists the three proposed FDUs as `FDU 1 - Holberg Landscape Unit`, `FDU 2 - Keogh Landscape Unit`, and `FDU 3 - Marble Landscape Unit`. |
| 13 | Enhanced Forestry Zone applicability is stated for `FDU 1 (Holberg)` and `FDU 2 (Keogh)`. |
| 14 | Old-growth/objective text references `FDU 3 (Marble)` and draft OGMAs for Holberg and Keogh. |
| 15 | Marble LU OGMAs are referenced as applying within the FSP. |
| 22 | Community watershed text references `FDU #1 (Holberg Landscape Unit)`. |

PDF term counts:

| Term | Count |
| --- | ---: |
| `FDU` | 43 |
| `Forest Development Unit` | 1 |
| `Holberg` | 6 |
| `Keogh` | 5 |
| `Marble` | 10 |
| `Nahwitti` | 0 |
| `Shushartie` | 0 |
| `Tsulquate` | 0 |
| `K3Z` | 1 |

Interpretation:

- The 2020 FSP PDF supports the initial project-note expectation that the FSP
  references three relevant LUs: Holberg, Keogh, and Marble.
- The 2024 amendment spatial payload contains six FDU/LU labels:
  Holberg, Keogh, Marble, Nahwitti, Shushartie, and Tsulquate.
- The additional 2024 amendment names (`Nahwitti`, `Shushartie`, `Tsulquate`)
  do not appear in the 2020 PDF text extracted with `pypdf`.
- Project clarification resolves the modelling boundary as the provided
  amendment spatial boundary filtered to FDU 1 Holberg, FDU 2 Keogh, and
  FDU 3 Marble.

Current source-boundary status:

- Relevant LUs referenced by the 2020 FSP: Holberg, Keogh, Marble.
- Broader FDU names present in the 2024 amendment spatial payload:
  Holberg, Keogh, Marble, Nahwitti, Shushartie, Tsulquate.
- Pre-pivot runtime AOI: see bootstrap AOI convention below.

## Bootstrap AOI Convention

Decision date: 2026-06-23

Decision:

- Use `NICF_FDU_2024.shp` from
  `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` as the accepted
  pre-pivot bootstrap AOI source for the NICF FSP teaching instance.
- Filter the pre-pivot FSP AOI boundary to the FSP's three FDUs only:
  FDU 1 Holberg, FDU 2 Keogh, and FDU 3 Marble.
- Treat the remaining amendment-payload features (`Nahwitti`, `Shushartie`,
  and `Tsulquate`) as raw source provenance/reference records, not as part of
  the FSP AOI for this instance.
- Treat a dissolved whole-AOI polygon as a generated runtime helper only, not
  as the canonical source record.
- Treat the 2020 FSP PDF three-FDU scope as the governing pre-pivot FSP AOI
  interpretation for the provided amendment spatial boundary.

Accepted source candidate:

| Field | Value |
| --- | --- |
| Raw payload | `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` |
| Path in zip | `NICF FSP Shapefiles/NICF_FDU_2024.shp` |
| Canonical feature semantics | Three preserved FSP AOI polygons: Holberg, Keogh, Marble |
| CRS | `EPSG:3005` |
| Geometry type | `Polygon` |
| Feature count | `3` |
| Total measured area | `147798.392 ha` |
| Bounds | `(849931.438, 580387.812, 928536.312, 639356.250)` |

Rationale:

- The bootstrap project note says to scale up to the new AOI uploaded as the
  amendment spatial payload.
- The provided spatial payload contains the FSP AOI boundary records, but the
  FSP AOI is only FDU 1, FDU 2, and FDU 3.
- The 2020 FSP document identifies Holberg, Keogh, and Marble as the three
  proposed FDUs, and the project clarification confirms only FDU 1, FDU 2, and
  FDU 3 make up the FSP AOI.
- Preserving FDU/LU feature identity keeps the teaching model able to report and
  reason at the FDU/LU level while still allowing a dissolved whole-AOI runtime
  boundary to be generated later if needed.

Open normalization work:

- Source-path wiring is recorded in `config/run_profile.nicffsp.yaml`.

## Canonical Extracted AOI Source

Extraction date: 2026-06-23

Pivot status:

- This FDU 1/2/3 source inventory remains valid provenance for the original
  NICF FSP bootstrap lane.
- It is no longer the active model extraction AOI.
- `P1.6` now governs the active TFL 6 AOI contract, and `P1.6a` will
  materialize `data/source/tfl_6/aoi/tfl_6_boundary.gpkg` before the run
  profile boundary path is switched.

Accepted tracked source path:
`data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp`

Extracted shapefile family:

| Tracked path | SHA-256 |
| --- | --- |
| `data/source/nicf_fsp/aoi/nicf_fsp_aoi.cpg` | `3ad3031f5503a4404af825262ee8232cc04d4ea6683d42c5dd0a2f2a27ac9824` |
| `data/source/nicf_fsp/aoi/nicf_fsp_aoi.dbf` | `9970cc3252a4dfe25e96252b6f85e16e1467f7f5f81a635a71cb9e48ab85fdf5` |
| `data/source/nicf_fsp/aoi/nicf_fsp_aoi.prj` | `4dc6a252b4e1e9468f9489c04fc559230f6d8b3f6ad8a79f02ba365a593636f5` |
| `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp` | `8e3cef68c9e0375550f240839e1f64b20e7036c6bbca14b0f995245b66566e7c` |
| `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shx` | `eaa7753e86ece7adf025cae244d0677f9db3562aaea3f727b06ad74eb8081727` |

Verification:

- Read path: `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp`
- Feature count: `3`
- Geometry type: `Polygon`
- CRS: `EPSG:3005`
- Bounds: `(849931.438, 580387.812, 928536.312, 639356.250)`
- Geometry validity: `3` valid, `0` invalid
- Total measured area in EPSG:3005: `147798.392 ha`
- Feature names: Holberg, Keogh, Marble

Interpretation:

- This extracted lowercase shapefile family is the accepted canonical source
  path for the pre-pivot bootstrap NICF FSP AOI.
- The original zip remains tracked as raw provenance for all six amendment
  features.
- `config/run_profile.nicffsp.yaml` still points `selection.boundary_path` at
  this pre-pivot source path only as a temporary bootstrap path until the TFL 6
  boundary is materialized under `P1.6a`.

## Canonical Extracted LU Reference Source

Extraction date: 2026-06-23

Decision:

- Track only the three FSP-relevant BCGW LU records as canonical reference
  context: Holberg, Keogh, and Marble.
- Keep the full 27-feature BCGW LU zip as raw provenance/context.
- Do not use the LU reference layer as the runtime AOI. The pre-pivot bootstrap
  AOI remains `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp` until `P1.6a`
  materializes the active TFL 6 boundary.

Accepted tracked source path:
`data/source/nicf_fsp/lu_reference/nicf_lu_reference.shp`

Extracted shapefile family:

| Tracked path | SHA-256 |
| --- | --- |
| `data/source/nicf_fsp/lu_reference/nicf_lu_reference.cpg` | `3ad3031f5503a4404af825262ee8232cc04d4ea6683d42c5dd0a2f2a27ac9824` |
| `data/source/nicf_fsp/lu_reference/nicf_lu_reference.dbf` | `1faa1c616eec6da8b7bdcdf0f97281e38f1b78eaacaedf65d6aaf20b3ecb2a16` |
| `data/source/nicf_fsp/lu_reference/nicf_lu_reference.prj` | `4dc6a252b4e1e9468f9489c04fc559230f6d8b3f6ad8a79f02ba365a593636f5` |
| `data/source/nicf_fsp/lu_reference/nicf_lu_reference.shp` | `580e33fd55390b93dc48d4b53fcd22df0fa11b6a03614bbf43d8ac5bc603d7ad` |
| `data/source/nicf_fsp/lu_reference/nicf_lu_reference.shx` | `0e098fb581d3c4337fd8d17f361007e92789a1294b292310867b181a2536d630` |

Verification:

- Read path: `data/source/nicf_fsp/lu_reference/nicf_lu_reference.shp`
- Feature count: `3`
- Geometry type: `Polygon`
- CRS: `EPSG:3005`
- Bounds: `(849931.438, 580387.813, 928536.312, 641215.125)`
- Geometry validity: `3` valid, `0` invalid
- Total measured area in EPSG:3005: `165588.857 ha`
- Feature names: Holberg, Keogh, Marble

Interpretation:

- This extracted lowercase shapefile family is the accepted canonical source
  path for LU reference context in the bootstrap NICF FSP instance.
- The raw BCGW LU zip remains tracked as provenance for the broader 27-feature
  clip.
- `config/run_profile.nicffsp.yaml` records this source as
  `selection.source_context.lu_reference_path`; the current FEMIC runtime
  consumes `selection.boundary_path` directly and carries LU reference context
  as provenance while TFL 6 becomes the active extraction AOI.

## TFL 6 Management Plan 10 Information Package Reference

Retrieval date: 2026-06-23

Purpose:

- Record a local reference copy of the TFL 6 timber supply analysis information
  package cited in the TFL 6 AAC rationale as accepted by FLNR Forest Analysis
  and Inventory Branch on March 3, 2011.
- This is contextual reference material for North Island/TFL 6 assumptions, not
  the active TFL 6 boundary artifact.

Tracked source path:
`data/source/nicf_fsp/reference/tfl_6_management_plan_10_information_package_2011.pdf`

Source URL:
`https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-tenures/tree-farm-licence/management-plans/tfl_6_mngment_plan_2011_ip.pdf`

Verification:

- File size: `2183218` bytes
- SHA-256:
  `302b4ce948a2cb765ec6a451157963422e9b8f102647d6b71864235e3bdb38e7`
- Page count: `126`
- Extracted text confirms:
  - `TFL 6`
  - `Management Plan #10`
  - `Timber Supply Analysis Information Package`
  - `February 2011`

Interpretation:

- The downloaded PDF is the BC-hosted copy titled in the file as Appendix A:
  Accepted Timber Supply Analysis Information Package, February 2011, for
  TFL 6 Management Plan #10.
- The repository-local filename is normalized to lowercase while preserving the
  original source URL for provenance.
