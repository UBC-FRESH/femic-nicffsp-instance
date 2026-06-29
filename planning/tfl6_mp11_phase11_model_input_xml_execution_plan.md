# TFL 6 MP11 Phase 11 Model-Input/XML Execution Plan

## Purpose

This note launches Phase 11: MP11 model-input bundle and ForestModel XML
rebuild. Phase 11 promotes only accepted MP11 public-data rebuild surfaces into
explicit model-input and XML contracts before any Matrix Builder or Patchworks
runtime work starts.

Phase 11 does not build the Patchworks runtime bundle. Runtime-bundle build
ownership starts in Phase 12 (`#69`), after Phase 11 has produced an accepted
model-input/XML handoff or a blocker package.

This P11.1 launch note records the governing handoff audit. It does not
generate model-input tables, ForestModel XML, Matrix Builder outputs, or
runtime artifacts.

## Branch And Issue Tree

- Branch: `feature/p11-model-input-xml-rebuild-plan`
- Parent issue: `#68`
- Child issues:
  - P11.1 launch MP11 model-input/XML rebuild execution plan: `#86`;
  - P11.2 audit MP11 model-input promotion readiness: `#87`;
  - P11.3 build MP11 model-input candidate manifest or stop report: `#88`;
  - P11.4 generate MP11 ForestModel XML candidate or stop report: `#89`;
  - P11.5 define Phase 12 runtime-build handoff or blocker package: `#90`;
  - P11.6 close Phase 11 and hand off model-input/XML status: `#91`.

## Governing Accepted Handoffs

Phase 11 starts from these accepted or promotion-candidate surfaces:

| Surface | Primary artifact | Phase 11 treatment |
| --- | --- | --- |
| MP11 evidence-promotion rules | `planning/tfl6_mp11_baseline_and_promotion_contract.md` | Governs when extracted or generated evidence may become model-input evidence. |
| MP11 public source-layer and THLB rebuild contract | `planning/tfl6_mp11_source_layer_thlb_rebuild_contract.md` | Governs public/proxy/private source-layer boundaries. |
| P9RF resultant-fragment THLB checkpoints | `planning/tfl6_mp11_p9rf_table12_resultant_vs_p9r_comparison.md` | Current public-data THLB promotion candidate after P9D/P9E repairs. |
| P9RF Current THLB endpoint | `planning/tfl6_mp11_p9rf_table12_step_290.md` | Current THLB checkpoint: `122,763.421 ha`, `+2,664.421 ha` versus MP11. |
| P9RF Long-term Land Base endpoint | `planning/tfl6_mp11_p9rf_table12_step_310.md` | Long-term land-base checkpoint: `121,336.593 ha`, `+2,664.593 ha` versus MP11. |
| MP11 AU/yield strategy | `planning/tfl6_mp11_au_yield_strategy_contract.md` | Governs top-N AU identity and yield-curve promotion boundary. |
| Phase 10R curve closeout | `planning/tfl6_mp11_phase10r_curve_rebuild_closeout.md` | Accepts all `27` MP11 Table 57 future-managed curves for the Phase 11 curve handoff. |
| Locked curve recipe | `planning/tfl6_mp11_curve_generation_recipe.md` | Defines reproducible TIPSY/BTC generation and validation policy. |
| Curve recipe lock | `planning/tfl6_mp11_curve_generation_recipe_lock.json` | Records command provenance, validation results, and artifact hashes. |
| Managed curve comparison | `planning/tfl6_mp11_managed_curve_comparison.md` | Confirms `27` comparison rows accepted for Phase 11 handoff. |
| TIPSY-vs-VDYP diagnostics | `planning/tfl6_mp11_tipsy_vdyp_diagnostic_manifest.md` | Supplies AU-wise diagnostic context; rows remain `not_model_input` until Phase 11 materializes model tables. |
| Operability, harvest-system, MHA, and scenario rules | `planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md` | Governs deferred and proxy rule treatment. |
| KPI, QA, and reporting targets | `planning/tfl6_mp11_kpi_qa_reporting_contract.md` | Governs report and validation target families. |

## Handoff Decisions Already Locked

- Phase 10R accepted all `27` MP11 Table 57 future-managed curves for the
  Phase 11 curve handoff.
- The accepted handoff contains `25` BTC-generated curves and `2` canonical
  AU curve-reuse rows for `FMH01` and `FMH22`.
- TIPSY BEC and SI inputs are locked to the target canonical top-N AU VRI BEC
  and median VRI SI.
- The locked recipe validates `0` BEC mismatches, `0` target-BEC mismatches,
  and `0` SI-input mismatches.
- Tables 54 and 55 remain deferred unless a later public-safe existing/recent
  AU-code to BEC/site-series mapping is supplied.
- Phase 9D/P9E repaired the avoidable Step 220 and Step 210 public-proxy gaps
  before Phase 11 launch.
- The P9RF resultant-fragment lane is the current THLB promotion candidate;
  the earlier P9 diagnostic full-stand-intersection run is not a model-input
  source.

## Active Blockers And Stop Conditions

Phase 11 must stop before model-input/XML generation if any of these remain
unresolved in P11.2:

- the P9RF THLB promotion candidate is not explicitly classified by model-input
  table role and source/proxy caveat;
- accepted Phase 10R curves are not mapped to model-input curve IDs with
  deterministic provenance;
- any generated model-input table would consume Tables 54/55 without a reviewed
  public-safe AU-code mapping;
- any figure-derived value would enter model-input tables without an accepted
  promotion status;
- Phase 5 baseline model-input/XML provenance cannot be inventoried well enough
  to define replacement or supplement behavior; or
- generated outputs would land outside an ignored or explicitly tracked
  artifact boundary.

## Artifact Layout Policy

P11.1/P11.2 should define and audit before writing large rebuild outputs.

Planned tracked planning surfaces:

- `planning/tfl6_mp11_phase11_model_input_xml_execution_plan.md`;
- `planning/tfl6_mp11_model_input_promotion_readiness.{csv,json,md}`;
- `planning/tfl6_mp11_model_input_candidate_manifest.{csv,json,md}` or a
  blocked stop report;
- `planning/tfl6_mp11_forestmodel_xml_readiness.{csv,json,md}` or a blocked
  stop report; and
- final Phase 11 closeout and Phase 12/13 handoff notes.

Candidate generated model-input and XML outputs should not be written until
the relevant child gate passes. P11.3 owns the candidate model-input manifest
and any explicitly authorized generated scaffold. P11.4 owns the actual
ForestModel XML candidate generation task: if P11.4 readiness passes, it should
write `output/patchworks_tfl6_mp11_candidate/forestmodel.xml` and candidate
fragments under `output/patchworks_tfl6_mp11_candidate/fragments/`. It must not
run Matrix Builder or assemble a Patchworks runtime bundle; those belong to
Phase 12.

## Current Phase 11 Edge

P11.1 and P11.2 are complete. The Phase 5 provenance inventory, artifact
layout, promotion gates, candidate-scaffold decisions, schema bridge, and
readiness manifest define the entry contract for P11.3.

P11.3a consumed
`planning/tfl6_mp11_model_input_promotion_readiness.{csv,json,md}` and recorded
the candidate-manifest entry contract in
`planning/tfl6_mp11_p11_3_readiness_consumption.{json,md}`. The P11.2
readiness manifest reports `11` gates, `0` blocked hard gates, `2` deferred
soft gates, `9` passing gates, and P11.3 unlock status
`candidate_manifest_eligible`.

P11.3b emitted
`planning/tfl6_mp11_model_input_candidate_manifest.{csv,json,md}` from the
P11.2 readiness and schema-bridge inputs. The manifest records `13` table
roles: `12` are eligible for a later generated scaffold and `1` is deferred
not eligible (`harvest_system_table`).

P11.3c emitted
`planning/tfl6_mp11_model_input_candidate_provenance_review.{csv,json,md}`.
The review records `12` passing candidate-scaffold roles, `1` non-blocking
deferred comparison-metadata role, `0` blocked roles, and P11.4a unlock status
`p11_4a_audit_eligible`.

P11.3 is complete.

P11.4a emitted
`planning/tfl6_mp11_phase11_xml_provenance_audit.{csv,json,md}`. The audit
records `8` XML/component families, `7` families requiring P11.4b readiness
decisions, `1` non-blocking deferred harvest-system family, `0` missing
required Phase 5 notes, and P11.4b unlock status
`p11_4b_readiness_eligible`.

P11.4a generated no model-input tables, ForestModel XML, Matrix Builder
outputs, or Patchworks runtime artifacts. The next bounded move is P11.4b:
build the XML readiness manifest or stop report.

P11.4b emitted
`planning/tfl6_mp11_forestmodel_xml_readiness.{csv,json,md}` as a stop report.
The stop report evaluates `8` XML/component families: `0` are ready, `7` are
blocked on missing MP11 candidate model-input bundle/export-bridge outputs, and
`1` harvest-system family remains non-blocking deferred metadata. P11.4c
candidate XML generation is blocked with status
`blocked_missing_candidate_outputs`.

The stop report is evidence of the missing generated-input surface, not the
endpoint for Phase 11. Issue `#89` is reopened. P11.4 remains active, and the
next bounded move is P11.4c: build the generated MP11 candidate model-input
bundle and export compatibility bridge under `data/mp11_model_input_bundle/`,
then rerun XML readiness before attempting candidate ForestModel XML export.

P11.4c corrected the missing build surface. It added
`scripts/build_p11_mp11_candidate_bundle.py`, generated the ignored MP11
candidate scaffold under `data/mp11_model_input_bundle/`, and emitted
`planning/tfl6_mp11_candidate_bundle_build_summary.{csv,json,md}`. The build
injects `18` active accepted Phase 10R MP11 Table 57 managed curves across
`648` curve-point rows, affects `8,957` stand rows, defers `9` duplicate Table
57 rows that map to already-selected canonical AU identities, and regenerates
the export compatibility bridge with `172` curve rows and `30,651` curve-point
rows.

P11.4d reran `planning/tfl6_mp11_forestmodel_xml_readiness.{csv,json,md}` after
the generated candidate bundle existed. The readiness output now reports `7`
ready component families, `0` blocked, `1` non-blocking deferred harvest-system
family, and P11.4c generation status `eligible`.

P11.4e generated the MP11 candidate ForestModel package under
`output/patchworks_tfl6_mp11_candidate/`. P11.4f added
`scripts/build_p11_mp11_xml_generation_qa.py` and emitted
`planning/tfl6_mp11_forestmodel_xml_generation_qa.{csv,json,md}`. The QA record
confirms XML root `ForestModel`, `13,197` curve nodes, `2,442` select nodes,
`814` treatment nodes, `24,879` fragment rows, and `191,168.566447 ha`
fragment area.

P11.4 is complete. Matrix Builder, Patchworks runtime assembly, scenario smoke,
and release QA remain downstream. The next bounded move is P11.5: define the
Phase 12 runtime handoff package.

P11.5 emitted `planning/tfl6_mp11_phase12_runtime_handoff.{csv,json,md}` with
handoff status `phase12_runtime_handoff_ready`. The handoff points Phase 12 to
the generated MP11 candidate XML/fragments, records the generated candidate
bundle/export bridge roots, preserves candidate-scaffold caveats, and leaves
Matrix Builder, runtime assembly, scenario smoke, and release QA as downstream
work.

P11.5 is complete. The next bounded move is P11.6: close Phase 11 and hand off
model-input/XML status.
