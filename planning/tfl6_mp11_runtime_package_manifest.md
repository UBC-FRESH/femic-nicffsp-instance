# P12.3 MP11 Runtime Package Manifest

This manifest records the assembled MP11 candidate Patchworks runtime
package after Matrix Builder tracks and block/topology surfaces were
generated.

P12.3 does not run direct Patchworks launch smoke, run scenarios, publish
a release archive, or replace the accepted Phase 5 teaching/runtime
baseline.

## Summary

- generated_at_utc: `2026-06-29T04:32:04+00:00`
- runtime_package_status: `candidate_runtime_package_assembled_pending_launch_smoke`
- model_root: `models/tfl6_patchworks_model_mp11_candidate`
- runtime_config: `config/patchworks.runtime.mp11_candidate.windows.yaml`
- tracked_package_file_count: `6`
- track_file_count: `13`
- block_file_count: `6`
- block_rows: `24879`
- block_area_ha: `191168.566447`
- block_crs: `EPSG:3005`
- block_geometry_valid: `True`
- topology_rows: `170759`
- tracks_qa_status: `matrix_builder_tracks_generated_inspection_pass`
- tracks_features_rows: `86574`
- tracks_accounts_rows: `823`
- tracks_products_rows: `26085`
- tracks_messages_rows: `0`
- direct_launch_smoke: `not_performed`
- scenario_smoke: `not_performed`
- release_qa: `not_performed`

## Tracked Package Files

| Path | Bytes |
| --- | ---: |
| `models/tfl6_patchworks_model_mp11_candidate/README.md` | 1304 |
| `models/tfl6_patchworks_model_mp11_candidate/lineage_registry.yaml` | 5958 |
| `models/tfl6_patchworks_model_mp11_candidate/analysis/base.pin` | 156 |
| `models/tfl6_patchworks_model_mp11_candidate/analysis/base_variant_common.bsh` | 3785 |
| `models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runtime_common.bsh` | 9182 |
| `models/tfl6_patchworks_model_mp11_candidate/scripts/targets/flowtargets.bsh` | 2187 |

## Generated Runtime Inputs

- Matrix Builder tracks remain under the ignored `tracks/` root.
- Block/topology files remain under the ignored `blocks/` root.
- Launch smoke and scenario smoke are still `not_performed`.

## Boundary

This is a candidate runtime package ready for P12.4 direct launch smoke.
It is not a release package and does not supersede the accepted Phase 5
teaching/runtime baseline.
