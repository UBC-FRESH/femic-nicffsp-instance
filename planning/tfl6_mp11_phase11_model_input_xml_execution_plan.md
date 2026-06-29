# TFL 6 MP11 Phase 11 Model-Input/XML Execution Plan

## Purpose

This note launches Phase 11: MP11 model-input bundle and ForestModel XML
rebuild. Phase 11 promotes only accepted MP11 public-data rebuild surfaces into
explicit model-input and XML contracts before any Matrix Builder or Patchworks
runtime work starts.

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
  - P11.4 build ForestModel XML readiness manifest or stop report: `#89`;
  - P11.5 define Phase 12 runtime handoff or blocker package: `#90`;
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
P11.2 accepts the promotion-readiness manifest. When generated, they should use
an explicit MP11 candidate namespace rather than overwriting the Phase 5
accepted runtime surfaces without a separate replacement decision.

## Next P11.1 Work

P11.1b should inventory the existing Phase 5 model-input bundle, ForestModel
XML, Matrix Builder, and runtime provenance surfaces so Phase 11 can define
what is being replaced, supplemented, or held as the accepted teaching
baseline.
