# TFL 6 MP11 P9D Public DEM Slope Zonal Statistics

## Inputs

- DEM: `runtime/dem/p9d_public_dem/processed/tfl6_cded_dem.tif`
- Slope raster: `runtime/dem/p9d_public_dem/processed/tfl6_cded_slope_pct.tif`
- Step 210 active fragments: `planning/tfl6_mp11_p9rf_table12_step_210.gpkg`
- Thresholds: `60.0, 70.0, 80.0, 90.0`

## Summary

- Fragment count: `43531`
- Fragments with valid DEM pixels: `39240`
- Fragments without valid DEM pixels: `4291`
- Source area: `129208.678 ha`
- Source area with valid pixels: `129141.076 ha`
- Source area without valid pixels: `67.602 ha`
- Maximum slope: `259.745%`

## Threshold Diagnostics

| Threshold | Area with any steep pixel | Area majority steep |
| ---: | ---: | ---: |
| `60%` | `72919.850 ha` | `12756.701 ha` |
| `70%` | `57741.851 ha` | `5646.183 ha` |
| `80%` | `43248.307 ha` | `1915.000 ha` |
| `90%` | `30371.681 ha` | `631.379 ha` |

## Caveat

Zonal statistics are derived from public CDED 1:250,000 DEM cells resampled to EPSG:3005. They are suitable as a public proxy test, not as a replacement for WFP LiDAR-derived terrain classes.
