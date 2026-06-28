# TFL 6 MP11 P9E Public TSM Source Manifest

## Source

- Catalogue URL: `https://catalogue.data.gov.bc.ca/dataset/terrain-stability-mapping-tsm-detailed-polygons-with-short-attribute-table-spatial-view`
- ArcGIS layer URL: `https://delivery.maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_whse_terrestrial_ecology/MapServer/18`
- Feature class: `WHSE_TERRESTRIAL_ECOLOGY.STE_TER_STABILITY_POLYS_SVW`
- Output GPKG: `data/source/tfl_6/terrain/tsm_detailed_polygons_tfl6.gpkg`

## Materialization

- Raw bbox features: `1433`
- TFL6-clipped features: `274`
- TFL6-clipped area: `21852.484 ha`

## Key Field Counts

### `slope_stability_class_txt`

- `Stable: low landslide potential`: `96`
- `Stable: negligible landslide potential`: `82`
- `NULL`: `55`
- `Potentially unstable`: `36`
- `Unstable`: `5`

### `slope_stability_class_w_roads`

- `III`: `96`
- `I`: `82`
- `NULL`: `55`
- `P`: `31`
- `IV`: `5`
- `V`: `5`

### `polygon_stability_class_type`

- `D`: `188`
- `NULL`: `55`
- `R`: `31`

### `project_name`

- `NorthIsland Terrain`: `188`
- `Fpc 21 Campbell River FD`: `48`
- `Fpc 22 Campbell River FD`: `22`
- `Fpc 19 Campbell River FD`: `16`

## Caveat

This public TSM layer is a provincial terrain-stability mapping source. It is not guaranteed to match WFP's private DTSM/Patchworks processing, but it is a real public candidate for MP11 Table 12 Step 210 and must not be treated as unavailable.
