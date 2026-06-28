# TFL 6 MP11 P9RF mp11_t12_300 Less future roads

## Result

- Step kind: `deduction_proxy`
- Source area: `122,764.836 ha`
- Deducted area: `1,426.797 ha`
- Retained area: `121,338.039 ha`
- MP11 comparison target: `1,427.000 ha`
- Delta to MP11: `-0.203 ha` (`-0.0142%`)
- Input fragments: `40,528`
- Active fragments: `23,245`
- Deducted fragments: `17,283`
- Balance error: `0.000000000 ha`
- Checkpoint status: `locked_p9rf_step300_aspatial_future_roads_proxy`

## Notes

Future roads are long-term land-base context, not current THLB. Because future road alignments are unknown, P9RF implements this row as an aspatial area netdown proxy using smallest-current resultant fragments to approximate the MP11 net deduction. The deducted fragments are an area accounting placeholder and must not be interpreted as predicted future road locations.

## Artifact

- GeoPackage: `planning/tfl6_mp11_p9rf_table12_step_300.gpkg`
- Layers: `active_fragments`, `deducted_fragments`
