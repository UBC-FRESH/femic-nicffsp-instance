# Source Inventory

## Initial Payloads

| Tracked path | Original uploaded filename | SHA-256 | Notes |
| --- | --- | --- | --- |
| `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` | `NICF FSP amend #3 spatial.zip` | `de3776cda77d056390ffdee03aed6e3a914501a4c2c8adc34ba8481e02bbabcc` | Candidate source for the Forest Stewardship Plan amendment AOI. Contents still need layer-level inspection. |
| `data/source/nicf_fsp/bcgw_lu_clip_2026_06.zip` | `BCGW_LU_Clip_06-2026.zip` | `03477133df626104a60e07699fdb6025a712af1a0a6a710ca5958d44792c0a47` | Candidate source for the Landscape Unit boundaries referenced by the FSP. Contents still need layer-level inspection. |
| `data/source/nicf_fsp/nicf_forest_stewardship_plan_2020.pdf` | `NICF-Forest-Stewardship-Plan-2020-2.pdf` | `9bccd37a9666b4b1262f54afcb152bbbe9ec0475435cdc53434656194bdc3895` | FSP document used to interpret AOI/LU context and management constraints. |

## Interpretation Boundary

These files are raw source payloads only. The next task is to inspect the zip
contents, identify authoritative layers, record CRS and geometry properties,
and extract canonical source layers into stable lowercase paths.

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
- Treat `NICF_FDU_2024.shp` as the current authoritative AOI candidate only,
  pending cross-check against the FSP document and the separate LU boundary zip.
- Do not extract or wire this layer into `config/run_profile.nicffsp.yaml` until
  the accepted runtime boundary convention is decided: either a dissolved FSP
  AOI, selected FDU/LU features, or a preserved multi-feature FDU boundary.

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
- The six `NICF_FDU_2024` features align by name with six full BCGW LU records:
  Holberg, Keogh, Marble, Nahwitti, Shushartie, and Tsulquate.
- Each FDU candidate feature is equal to or smaller than its corresponding full
  BCGW LU, so `NICF_FDU_2024` appears to be a clipped FDU/AOI surface derived
  from LU boundaries rather than the full LU boundary layer.
- The initial project note mentions three relevant LUs, but the inspected
  spatial payloads currently expose six named FDU/LU overlaps. Do not close the
  relevant-LU decision until the FSP PDF is checked against these layer names.

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
- Treat this as a source-version decision, not a GIS error:
  - the 2020 FSP document describes a three-FDU scope;
  - the 2024 amendment spatial payload appears to define a six-FDU candidate
    surface; and
  - the model runtime AOI should not be accepted until the project decides
    whether the teaching instance follows the 2020 FSP text, the 2024 amendment
    spatial payload, or a documented subset/dissolve of the amendment payload.

Current source-boundary status:

- Relevant LUs referenced by the 2020 FSP: Holberg, Keogh, Marble.
- Broader FDU names present in the 2024 amendment spatial payload:
  Holberg, Keogh, Marble, Nahwitti, Shushartie, Tsulquate.
- Accepted runtime AOI: see bootstrap AOI convention below.

## Bootstrap AOI Convention

Decision date: 2026-06-23

Decision:

- Use `NICF_FDU_2024.shp` from
  `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` as the accepted
  bootstrap AOI source for the NICF FSP teaching instance.
- Preserve the six FDU/LU features as the canonical source geometry semantics:
  Holberg, Keogh, Marble, Nahwitti, Shushartie, and Tsulquate.
- Treat a dissolved whole-AOI polygon as a generated runtime helper only, not
  as the canonical source record.
- Treat the 2020 FSP PDF three-FDU scope as historical/context evidence for the
  original FSP, not as the current modelling boundary, because the project
  request explicitly identifies the 2024 amendment spatial payload as the AOI
  for the new teaching instance.

Accepted source candidate:

| Field | Value |
| --- | --- |
| Raw payload | `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` |
| Path in zip | `NICF FSP Shapefiles/NICF_FDU_2024.shp` |
| Canonical feature semantics | Six preserved FDU/LU polygons |
| CRS | `EPSG:3005` |
| Geometry type | `Polygon` |
| Feature count | `6` |
| Total measured area | `204162.510 ha` |
| Bounds | `(849931.438, 580387.812, 928536.312, 653037.313)` |

Rationale:

- The bootstrap project note says to scale up to the new AOI uploaded as the
  amendment spatial payload.
- The amendment payload is newer than the 2020 FSP PDF and explicitly carries
  `2024` in the shapefile name.
- The six amendment features are internally consistent with the broader BCGW LU
  layer: each overlaps a same-named BCGW LU and is equal to or smaller than the
  full LU.
- Preserving FDU/LU feature identity keeps the teaching model able to report and
  reason at the FDU/LU level while still allowing a dissolved whole-AOI runtime
  boundary to be generated later if needed.

Open normalization work:

- Decide whether the full 27-feature BCGW LU layer should also be extracted as
  canonical reference context, or remain raw payload plus documented evidence.
- Update `config/run_profile.nicffsp.yaml` only after the accepted extracted
  AOI path exists.

## Canonical Extracted AOI Source

Extraction date: 2026-06-23

Accepted tracked source path:
`data/source/nicf_fsp/aoi/nicf_fdu_2024.shp`

Extracted shapefile family:

| Tracked path | SHA-256 |
| --- | --- |
| `data/source/nicf_fsp/aoi/nicf_fdu_2024.dbf` | `2024cdf3db2733e77a3dc6a864ed1252e01f44b72359c349b2712a08f2b0267d` |
| `data/source/nicf_fsp/aoi/nicf_fdu_2024.prj` | `4dc6a252b4e1e9468f9489c04fc559230f6d8b3f6ad8a79f02ba365a593636f5` |
| `data/source/nicf_fsp/aoi/nicf_fdu_2024.sbn` | `453a0b065fc46e72bc0b8921f5b3c3e9bbd8f9f4371aecd0e0430e32dbba5914` |
| `data/source/nicf_fsp/aoi/nicf_fdu_2024.sbx` | `7837493e8e589f85a110b2ceba9fdb58e6f25389d1eff39aac878887381061c4` |
| `data/source/nicf_fsp/aoi/nicf_fdu_2024.shp` | `1dbe46b7d981453826182868068fd193b14033fc2a2efa651f5f0c88f50dfa4e` |
| `data/source/nicf_fsp/aoi/nicf_fdu_2024.shx` | `49d2d4d95dcb5eb9c9ab480254a690eeda12ce6273958c317ebfae294d36f695` |

Verification:

- Read path: `data/source/nicf_fsp/aoi/nicf_fdu_2024.shp`
- Feature count: `6`
- Geometry type: `Polygon`
- CRS: `EPSG:3005`
- Bounds: `(849931.438, 580387.812, 928536.312, 653037.313)`
- Geometry validity: `6` valid, `0` invalid
- Total measured area in EPSG:3005: `204162.510 ha`
- Feature names: Keogh, Tsulquate, Holberg, Marble, Nahwitti, Shushartie

Interpretation:

- This extracted lowercase shapefile family is the accepted canonical source
  path for the bootstrap NICF FSP AOI.
- The original zip remains tracked as raw provenance.
- `config/run_profile.nicffsp.yaml` is not updated yet; runtime config wiring
  should happen after the LU reference-context decision is recorded.
