# TFL 6 MP11 P9RF mp11_t12_220 Terrain Stability - LiDAR 90% + Slope

## Result

- Step kind: `deduction_proxy`
- Source area: `129,208.678 ha`
- Deducted area: `1,801.705 ha`
- Retained area: `127,406.973 ha`
- MP11 comparison target: `1,820.000 ha`
- Delta to MP11: `-18.295 ha` (`-1.0052%`)
- Input fragments: `43,531`
- Active fragments: `42,600`
- Deducted fragments: `931`
- Balance error: `-0.000000000 ha`
- Checkpoint status: `locked_p9rf_step220_public_cded_steep_slope_proxy`

## Notes

Accepted public CDED steep-slope proxy for MP11 Step 220. The rule deducts true Step 210 resultant fragments where at least 75% of valid CDED pixels are >=70% slope, based on `planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.csv` and scenario report `planning/tfl6_mp11_p9d_step220_dem_slope_scenarios.md`. CDED is coarser and smoother than LiDAR, so this is a public-data teaching/research proxy, not WFP LiDAR equivalence.

## Artifact

- GeoPackage: `planning/tfl6_mp11_p9rf_table12_step_220.gpkg`
- Layers: `active_fragments`, `deducted_fragments`
