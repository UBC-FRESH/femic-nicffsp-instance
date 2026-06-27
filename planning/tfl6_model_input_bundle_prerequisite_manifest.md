# TFL 6 Model-Input Bundle Prerequisite Manifest

## Purpose

This P4.1a manifest records the accepted Phase 2/3 inputs for the first TFL 6
model-input bundle. It is a prerequisite inventory only. It does not write
model-input bundle tables, generate ForestModel XML, run Matrix Builder, or
assemble a Patchworks runtime package.

Machine-readable companion:
`planning/tfl6_model_input_bundle_prerequisite_manifest.json`.

Governing issue: `#17`.

## Accepted Metrics

The accepted Phase 2 THLB audit remains the benchmark source for the first
bundle handoff:

| Metric | Value |
| --- | ---: |
| GLB/current input proxy | `217042.719 ha` |
| AFLB checkpoint area | `196833.177 ha` |
| LHLB checkpoint area | `174768.947 ha` |
| Final THLB managed area | `144203.485 ha` |
| Benchmark status | accepted within teaching tolerance |

Source: `config/tsr/tfl6_thlb_smoke.audit.json` and
`config/tsr/thlb_reconstructed.status.md`.

## Present Prerequisites

The current checkout contains the tracked planning/config/data surfaces needed
to define the first bundle:

| Family | Primary paths |
| --- | --- |
| Run profile and source inputs | `config/run_profile.tfl6.yaml`, `data/input/tfl_6/input_layers_manifest.json`, `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`, `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet`, `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet` |
| THLB audit/status | `config/tsr/thlb_netdown.recipe.yaml`, `config/tsr/thlb_reconstructed.status.md`, `config/tsr/tfl6_thlb_smoke.audit.json` |
| AU and stand attribution | `planning/tfl6_au_yield_curve_contract.md`, `planning/tfl6_static_au_universe.csv`, `planning/tfl6_static_au_top_strata.csv`, `planning/tfl6_stand_to_au_review.csv` |
| Natural curves | `planning/tfl6_first_growth_au_curves.csv`, `planning/tfl6_first_growth_shape_diagnostics.csv`, `planning/tfl6_first_growth_au_remap_audit.csv` |
| Treated curves | `planning/tfl6_mp10_tipsy_parameter_library.csv`, `planning/tfl6_tipsy_parameter_crosswalk.csv`, `data/03_input-tfl6.csv`, `data/04_output-tfl6.csv`, `planning/tfl6_tipsy_managed_curves.csv`, `planning/tfl6_tipsy_managed_curve_diagnostics.csv` |
| Treatment and transition design | `planning/tfl6_treatment_option_contract.md`, `config/silviculture.tfl6.yaml`, `planning/tfl6_state_transition_contract.md` |
| Cedar and embedded identity design | `planning/tfl6_cedar_signal_design.md`, `planning/tfl6_nicf_embedded_identity.md` |

## Checkpoint Availability Gap

The Phase 2 THLB status report points at these generated checkpoint artifacts,
but they are not present in the current clean checkout:

| Expected checkpoint | Status | P4 implication |
| --- | --- | --- |
| `data/tsr/aflb_checkpoint.feather` | missing in checkout | needed only if P4 consumes AFLB restart geometry directly |
| `data/tsr/lhlb_checkpoint.feather` | missing in checkout | needed only if P4 consumes LHLB restart geometry directly |
| `data/tsr/tfl6_thlb_smoke_checkpoint.feather` | missing in checkout | must be rematerialized or regenerated before P4.1c consumes final THLB geometry |

This is not a Phase 2 result rejection. The accepted audit/status files and
benchmark tolerance remain valid. It is a Phase 4 implementation prerequisite:
the first bundle build needs a materialized final THLB geometry/checkpoint
surface at a stable path, or an explicit maintainer waiver selecting a
different source for the final schedulable geometry.

## P4.1b Handoff

P4.1b should define generated bundle paths and table roles before any bundle
outputs are written. It should also decide where the regenerated or
rematerialized THLB geometry will live as a P4 input and whether the bundle
uses Feather, GeoPackage, or both for checkpoint restart/readability.

P4.1a did not start:

- model-input bundle generation;
- outside-AOI expansion geometry materialization;
- ForestModel/XML generation;
- Matrix Builder; or
- Patchworks runtime-package work.
