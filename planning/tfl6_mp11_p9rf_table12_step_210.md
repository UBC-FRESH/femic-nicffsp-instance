# TFL 6 MP11 P9RF mp11_t12_210 Terrain Stability - Class 5

## Result

- Step kind: `deduction_proxy`
- Source area: `129,210.103 ha`
- Deducted area: `1.425 ha`
- Retained area: `129,208.678 ha`
- MP11 comparison target: `1,993.000 ha`
- Delta to MP11: `-1,991.575 ha` (`-99.9285%`)
- Input fragments: `43,530`
- Active fragments: `43,531`
- Deducted fragments: `10`
- Balance error: `0.000000000 ha`
- Checkpoint status: `locked_p9rf_step210_public_tsm_class_v_proxy_with_coverage_gap`

## Notes

Accepted strict public TSM Class V proxy for MP11 Step 210 using `data/source/tfl_6/terrain/tsm_detailed_polygons_tfl6.gpkg`, filtered to `slope_stability_class_w_roads == 'V'`. This applies the newly identified public terrain-stability source instead of skipping the row. The resulting deduction is much smaller than MP11, so the residual remains an explicit public-source coverage/semantic gap rather than a WFP DTSM equivalence claim.

## Artifact

- GeoPackage: `planning/tfl6_mp11_p9rf_table12_step_210.gpkg`
- Layers: `active_fragments`, `deducted_fragments`
