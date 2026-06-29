# TFL 6 MP11 Phase 14 Model-Input And XML Build Summary

This P14.5 output rebuilds an ignored MP11 harvest-system candidate model-input bundle and ForestModel XML/fragments package with public-proxy ground, cable, and heli clearcut lanes. It does not run Matrix Builder, assemble a Patchworks runtime, or run scenarios.

## Summary

- generated_at_utc: `2026-06-29T06:33:41+00:00`
- candidate_bundle_root: `data/mp11_harvest_system_model_input_bundle`
- patchworks_output_root: `output/patchworks_tfl6_mp11_harvest_system_candidate`
- forestmodel_xml: `output/patchworks_tfl6_mp11_harvest_system_candidate/forestmodel.xml`
- fragments_path: `output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.shp`
- stand_table_rows: `25019`
- stand_clearcut_eligible_rows: `22614`
- harvest_system_eligible_rows: `22614`
- harvest_system_group_rows: `25019`
- checkpoint_rows: `25019`
- fragment_rows: `24879`
- fragment_area_ha: `191168.566447`
- xml_root: `ForestModel`
- xml_select_nodes: `5698`
- xml_treatment_nodes: `2442`
- managed_cc_selects_replaced: `814`
- split_managed_selects: `2442`
- product_cc_selects_replaced: `814`
- split_product_selects: `2442`
- hvsys_selects: `2442`
- matrix_builder: `not_performed`
- runtime_bundle_generation: `not_performed`
- scenario_smoke: `not_performed`

## Treatment Labels

| Label | Count |
| --- | ---: |
| `CC_CABLE` | `814` |
| `CC_GROUND` | `814` |
| `CC_HELI` | `814` |

## Fragment Harvest-System Counts

| HVSYS | Rows | Area ha |
| --- | ---: | ---: |
| `CABLE` | `9008` | `72242.879` |
| `GROUND` | `12830` | `101533.092` |
| `HELI` | `652` | `4282.000` |
| `NOT_APPLICABLE` | `2389` | `13110.596` |

## Boundary

- WFP LBB remains unavailable; `HVSYS` is a P14.4 public-proxy field.
- XML split lanes expose `CC_GROUND`, `CC_CABLE`, and `CC_HELI` while retaining aggregate `.CC` product labels for all-system reporting.
- Matrix Builder, runtime assembly, all-system smoke, no-heli smoke, and release QA remain downstream Phase 14 tasks.

## Files

- `data/mp11_harvest_system_model_input_bundle/`
- `output/patchworks_tfl6_mp11_harvest_system_candidate/forestmodel.xml`
- `output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.shp`
- `planning/tfl6_mp11_phase14_model_input_xml_build_summary.csv`
- `planning/tfl6_mp11_phase14_model_input_xml_build_summary.json`
- `planning/tfl6_mp11_phase14_model_input_xml_build_summary.md`
