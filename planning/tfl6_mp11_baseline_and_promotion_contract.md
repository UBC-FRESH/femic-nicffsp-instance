# TFL 6 MP11 Baseline And Evidence-Promotion Contract

## Purpose

This P8.1 contract preserves the Phase 5 teaching runtime as the accepted
baseline and defines how MP11 evidence can move from public planning material
to future model contracts. It prevents accidental promotion of extracted MP11
values, recovered figure data, or non-public WFP assumptions into model inputs.

This contract does not rebuild source layers, THLB, yield curves, model-input
bundles, ForestModel XML, Matrix Builder outputs, or Patchworks runtime
artifacts.

## Accepted Baseline

The active accepted baseline remains the Phase 5 TFL 6 teaching release.

Baseline artifacts:

- runtime archive: `releases/tfl6_patchworks_runtime_p5_2.zip`;
- runtime manifest:
  `releases/tfl6_patchworks_runtime_p5_2_manifest.yaml`;
- public annex remote: `arbutus-s3`;
- runtime launch file:
  `models/tfl6_patchworks_model/analysis/base.pin`;
- release QA note: `planning/tfl6_phase5_release_qa.md`;
- release archive contract:
  `planning/tfl6_runtime_release_archive_manifest.md`;
- runtime documentation:
  - `docs/phase5-runtime-release.rst`;
  - `docs/phase5-runtime-quickstart.rst`;
  - `docs/phase5-rebuild-provenance.rst`;
  - `docs/phase5-scenario-teaching-workflows.rst`;
  - `docs/phase5-known-limitations-release-readiness.rst`.

Accepted Phase 5 QA evidence:

- public archive materialization passed from a no-credential clone;
- archive SHA and ZIP-member checks passed;
- direct Patchworks launch smoke passed;
- scenario smoke `tfl6_p44d_harvest_smoke200` passed;
- the scenario smoke produced nonzero managed `CC` harvested-volume,
  treated-area, managed/unmanaged area, and managed/unmanaged yield signals;
- Sphinx docs built warning-clean and the published Pages surface was checked.

The Phase 5 runtime is a teaching baseline, not an MP11-equivalent forecast.
It remains accepted until a future MP11-aligned replacement passes direct
source, model-input, XML, Matrix Builder, runtime, documentation, and
scenario-output QA.

## MP11 Evidence Inventory

The current MP11 evidence surfaces are:

- `planning/tfl6_mp11_source_package_manifest.md`;
- `planning/tfl6_mp11_extraction_inventory.csv`;
- `planning/tfl6_mp11_land_base_crosswalk.md`;
- `planning/tfl6_mp11_netdown_delta_crosswalk.md`;
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.md`;
- `planning/tfl6_mp11_model_behavior_crosswalk.md`;
- `planning/tfl6_mp11_model_behavior_scenario_endpoints.csv`;
- `planning/tfl6_mp11_figure_extraction_closeout.md`.

Current status summary:

- P6.3 land-base rows: `8` reviewed evidence rows, all `not_model_input`;
- P6.4 assumption rows: `14` reviewed evidence rows, all `not_model_input`;
- P6.5 behavior rows: `8` reviewed evidence rows, all `not_model_input`;
- Phase 7 figure inventory rows: `61`, all `not_model_input`;
- Phase 7 comparison-ready figures: `22`;
- Phase 7 planning-only figures: `14`;
- Phase 7 deferred figures: `20`;
- Phase 7 qualitative context figures: `5`.

These surfaces are enough to plan Phase 8 contracts. They are not enough to
replace model inputs or runtime outputs.

## Promotion States

All MP11-derived values, tables, figures, and assumptions must carry one of the
following states when referenced by implementation work:

| State | Meaning | May drive model input? |
| --- | --- | --- |
| `planning_only` | Useful for scoping, design, or identifying future work. | No |
| `comparison_target` | Accepted as a benchmark for comparing future outputs, with known validation strength. | No |
| `implementation_candidate` | Candidate for a future model contract, pending source review and QA. | No |
| `accepted_model_contract` | Explicitly reviewed and accepted as a model contract by a later implementation issue. | Yes |
| `accepted_model_input` | Materialized in a generated input table or recipe output with provenance and QA. | Yes |
| `rejected` | Reviewed and intentionally not used. | No |
| `deferred` | Valid topic but postponed with rationale. | No |
| `unavailable_non_public` | Requires WFP/private model data or assumptions unavailable from public sources. | No |

Promotion is monotonic only after review. A value can move backward from
`implementation_candidate` to `deferred`, `rejected`, or
`unavailable_non_public` if source review fails.

## Evidence Classes

Implementation issues must identify the evidence class before promotion:

| Evidence class | Examples | Minimum promotion requirement |
| --- | --- | --- |
| `source_text_claim` | MP11 narrative values or methods. | Page anchor, quotation/paraphrase, reviewer, and model relevance. |
| `source_table_value` | MP11 table values. | Table number, page anchor, extraction method, row/column labels, and arithmetic checks where possible. |
| `source_figure_recovery` | Values recovered from figures. | Review manifest, calibration/overlay evidence, validation strength, and independent table/text check if available. |
| `public_spatial_layer` | FADM, public VRI/R1/VDYP, public reserve layers. | Source URL/package, checksum or materialization proof, schema profile, and geometry/area QA. |
| `public_proxy` | DEM/slope proxy for inaccessible LBB or operability logic. | Explicit proxy rationale, comparison target, sensitivity bounds, and caveat. |
| `generated_model_output` | Future THLB outputs, curves, XML, Matrix Builder tracks, scenario outputs. | Reproducible command, artifact manifest, QA checks, and comparison report. |
| `non_public_reference` | WFP LBB, ITI, LEFI, objective weights, or unpublished source tables. | Must remain `unavailable_non_public` or be represented by an explicit public proxy/sensitivity lane. |

## Promotion Requirements

### To `comparison_target`

A value may become a comparison target only when:

- the source is public-safe;
- the page/table/figure anchor is recorded;
- the extraction or transcription method is recorded;
- the validation strength is stated;
- the intended comparison surface is clear; and
- `model_input_status` remains `not_model_input`.

Examples:

- MP11 Base Case harvest level `1,061,600 m3/year`;
- MP11 AAC recommendation evidence `1,252,700 m3/year`;
- MP11 THLB `120,099 ha`;
- Phase 7 comparison-accepted harvest/sensitivity figures.

### To `implementation_candidate`

A value or rule may become an implementation candidate only when:

- it has already been reviewed as planning evidence or a comparison target;
- a future issue identifies the target artifact it would affect;
- public-data reproducibility is classified;
- non-public dependencies are named; and
- the responsible child issue records acceptance and rollback checks.

### To `accepted_model_contract`

A value or rule may become an accepted model contract only when:

- a child issue explicitly promotes it;
- the promotion is recorded in `planning/`;
- upstream source and evidence class are listed;
- affected model artifacts are named;
- validation checks are defined before implementation; and
- the issue closeout states whether the contract replaces, extends, or
  supplements the Phase 5 baseline.

### To `accepted_model_input`

A value may become accepted model input only when:

- it is generated or materialized by a reviewed script, recipe, or table;
- the generated artifact has a manifest or QA summary;
- direct parse/schema checks pass;
- relevant area/curve/scenario checks pass;
- downstream runtime effects are either tested or explicitly deferred; and
- the roadmap, changelog, and issue closeout name the artifact.

## Figure-Evidence Rules

Recovered figure data require extra caution:

- `accepted_for_comparison` figure rows may be used as comparison targets only.
- `reviewed_for_planning` figure rows may guide report design or future
  extraction work only.
- `deferred_not_extracted` figure rows may not be cited as quantitative
  evidence.
- Figure-derived values require a stronger manual review before they can move
  beyond `comparison_target`.
- No figure-derived value can become `accepted_model_input` without a separate
  source-table check, manually reviewed extraction table, or explicit
  maintainer decision that the chart is the best available public source.

## Non-Public Data Rules

The following MP11 dependencies must not be silently reconstructed from
published summary values:

- WFP Land Base Blocking physical operability geometry;
- WFP LiDAR-derived ITI and LEFI attribute surfaces;
- WFP Patchworks objective weights and model internals;
- flight-distance/access surfaces for helicopter economic operability;
- unpublished full source tables behind several KPI figures.

Allowed treatments:

- mark as `unavailable_non_public`;
- design a public proxy with explicit caveats;
- design a sensitivity lane; or
- defer until a public source is available.

Disallowed treatments:

- invent stand-level values from aggregate MP11 summaries;
- force public THLB outputs to match MP11 by unexplained scaling;
- hide non-public dependencies inside scripts or configuration;
- imply WFP model equivalence from public-summary alignment alone.

## Replacement And Rollback Rules

The Phase 5 runtime remains accepted until a future replacement passes all
required QA. A future MP11-aligned package may replace Phase 5 only after:

- source-layer and THLB contracts are reviewed;
- AU/yield contracts are reviewed;
- model-input bundle QA passes;
- ForestModel XML is regenerated and inspected;
- Matrix Builder outputs are regenerated and inspected;
- Patchworks launch smoke passes;
- at least one scenario smoke passes;
- MP11 comparison/KPI reports are generated and caveated;
- Sphinx docs build warning-clean; and
- the release archive and manifest are materializable.

If a future rebuild fails any replacement gate:

- keep Phase 5 as the published baseline;
- mark the failed artifact as experimental or rejected;
- record the failure and rollback reason in `planning/` and issue comments;
- do not republish the runtime archive; and
- do not close the replacement phase as successful.

## Required Issue Closeout Language

Any issue that promotes MP11 evidence must state:

- source evidence class;
- source page/table/figure/layer;
- previous state;
- new state;
- affected artifact;
- validation performed;
- private-data caveat, if any; and
- rollback or deferral rule.

## P8.1 Acceptance

P8.1 is complete when:

- this contract is tracked in `planning/`;
- `ROADMAP.md` marks P8.1 complete;
- `CHANGE_LOG.md` records the contract;
- issue `#59` is closed with validation evidence; and
- no MP11 value has been promoted to model input.
