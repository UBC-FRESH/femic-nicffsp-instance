# TFL 6 MP11 Phase 10 AU/Yield Rebuild Execution Plan

## Purpose

This P10.1 plan launches Phase 10 and turns the accepted MP11 AU/yield
strategy contract into an executable rebuild sequence. It defines the issue
tree, branch, artifact layout, curve-lane gates, parameter-library gates,
generated-output hygiene, and validation expectations before any new
MP11-aligned curves are generated.

This plan does not generate natural curves, managed curves, model-input
bundles, ForestModel XML, Matrix Builder outputs, or Patchworks runtime
artifacts.

## Branch And Issue Tree

- Branch: `feature/p10-mp11-au-yield-curve-rebuild`
- Parent issue: `#67`
- Child issues:
  - P10.1 launch MP11 AU/yield rebuild execution plan: `#79`;
  - P10.2 extract MP11 managed-yield parameter library: `#80`;
  - P10.3 refresh MP11 AU and curve-lane crosswalk: `#81`;
  - P10.4 regenerate MP11 natural curve diagnostics: `#82`;
  - P10.5 generate MP11 managed curve diagnostics: `#83`;
  - P10.6 close Phase 10 and hand off curve artifacts: `#84`.

## Governing Contracts

Phase 10 executes these accepted planning contracts:

- `planning/tfl6_mp11_baseline_and_promotion_contract.md`;
- `planning/tfl6_mp11_au_yield_strategy_contract.md`;
- `planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md`;
- `planning/tfl6_mp11_kpi_qa_reporting_contract.md`;
- `planning/tfl6_mp11_phase9_closeout.md`.

The central Phase 10 rule is that curve artifacts may become reviewed
implementation candidates, but they do not become accepted model inputs until a
later model-input/XML phase explicitly promotes them through the Phase 8
evidence-promotion contract.

## Existing Curve And AU Surfaces

Phase 10 starts from the Phase 3/5 teaching-runtime curve surfaces:

| Surface | Path | Phase 10 treatment |
| --- | --- | --- |
| AU/yield contract | `planning/tfl6_au_yield_curve_contract.md` | Audit for carry-forward assumptions and MP11 gaps. |
| Static AU universe | `planning/tfl6_static_au_universe.*` | Reuse where canonical AU identity remains valid. |
| Stand-to-AU review | `planning/tfl6_stand_to_au_review.csv` | Re-profile if MP11 curve-lane fields require additional flags. |
| Natural VDYP curves | `planning/tfl6_first_growth_au_curves.csv` | Use as Phase 5 comparison baseline and possible script input. |
| Natural diagnostics | `planning/tfl6_first_growth_*` | Reuse or regenerate after P10.3 gates pass. |
| MP10 TIPSY library | `planning/tfl6_mp10_tipsy_parameter_library.*` | Preserve as legacy fallback/comparison evidence only. |
| MP10 TIPSY crosswalk | `planning/tfl6_tipsy_parameter_crosswalk.*` | Preserve as legacy fallback/comparison evidence only. |
| Treated curves | `planning/tfl6_tipsy_managed_curves.csv` | Use as Phase 5 managed-curve comparison baseline. |
| Treated diagnostics | `planning/tfl6_tipsy_managed_curve_diagnostics.*` | Use as Phase 5 managed-curve comparison baseline. |
| TIPSY config | `config/tipsy/tfl6.yaml` | Reuse only after MP11-specific parameter and handoff surfaces are reviewed. |

## Artifact Layout

Tracked planning and compact QA outputs:

- `planning/tfl6_mp11_phase10_execution_plan.md`;
- `planning/tfl6_mp11_managed_yield_parameter_library.*`;
- `planning/tfl6_mp11_au_curve_lane_crosswalk.*`;
- `planning/tfl6_mp11_natural_curve_diagnostics.*`;
- `planning/tfl6_mp11_managed_curve_diagnostics.*`;
- `planning/tfl6_mp11_phase10_closeout.md`.

Potential plot outputs may be tracked only if they are compact, public-safe,
and directly used in docs or QA notes:

- `plots/mp11_yield/`.

Generated runtime-scale outputs should remain ignored until explicitly
accepted:

- `runtime/mp11_yield/`;
- `runtime/logs/mp11_yield/`;
- `output/mp11_yield/`;
- generated BatchTIPSY scratch files;
- temporary extraction or OCR files.

## Parameter-Library Gates

P10.2 must produce reviewed parameter rows before managed curves are generated.
Each row should record:

- source page, table, row, and extraction method;
- MP11 AU era or managed-stand class;
- BEC variant and site-series where available;
- leading species and species-percent assumptions;
- site-index value and site-index source;
- planting density, regeneration delay, genetic gain, fertilization, and
  spacing assumptions;
- OAF1/OAF2, VRAF, utilization, and NRL rule references where available;
- curve lane and intended generator;
- public/private dependency flags; and
- review status and confidence.

Rows with unavailable LEFI/ITI/LiDAR or private WFP dependencies must remain
`unavailable_non_public`, `sensitivity_only`, or `fallback_required` rather
than being silently filled.

## Curve-Lane Gates

P10.3 must separate these concerns before any curve generation:

- stable canonical FEMIC AU identity;
- MP11 AU era or managed-stand class;
- natural, existing managed, recent managed, future managed, fallback, and
  sensitivity curve lanes;
- public site-productivity and private/unavailable productivity dependencies;
- treatment markers and treatment eligibility;
- utilization/OAF/VRAF/NRL rule keys; and
- unsupported or low-confidence row status.

Treatment, operability, harvest-system, scenario membership, and THLB status
must not become hidden canonical AU key dimensions.

## Execution Gates

Phase 10 must proceed through these gates:

1. P10.1 execution plan and issue tree are synchronized.
2. P10.2 parameter extraction creates reviewed public-safe parameter surfaces.
3. P10.3 curve-lane crosswalks resolve supported, fallback, deferred, and
   unavailable mappings.
4. P10.4 natural curve diagnostics run only after P10.3 gates pass.
5. P10.5 managed curve diagnostics run only for supported reviewed parameter
   and crosswalk rows.
6. P10.6 closes the phase only after validation, PR merge, and Phase 11
   handoff notes.

No step may skip directly from MP11 summary prose to generated model-input
curves.

## No-Fabrication Rules

Disallowed in Phase 10:

- fabricating stand-level LEFI/ITI/LiDAR productivity values from aggregate
  MP11 text;
- embedding private WFP curves or unpublished parameter tables;
- hiding OAF, VRAF, utilization, genetic gain, fertilization, spacing, or NRL
  assumptions inside opaque curve IDs;
- replacing MP11 missing values with MP10 fallbacks without explicit fallback
  status;
- changing canonical AU identity to encode treatment or scenario semantics;
- writing model-input bundles, ForestModel XML, Matrix Builder outputs, or
  Patchworks runtime artifacts; and
- promoting generated curves to accepted model-input status inside Phase 10.

## Promotion Gates

Generated Phase 10 outputs can be assigned only these states until later
phases:

- `reviewed_parameter`;
- `generated_diagnostic`;
- `implementation_candidate`;
- `comparison_output`;
- `fallback_required`;
- `deferred`;
- `rejected`;
- `unavailable_non_public`.

No Phase 10 artifact becomes `accepted_model_input` until Phase 11 explicitly
promotes it through the Phase 8 promotion contract.

## Minimum Validation

Every Phase 10 child issue must run, at minimum:

```bash
python -m ruff check .
sphinx-build -b html docs docs/_build/html -W
```

Implementation issues must add parameter-library, crosswalk, natural-curve, or
managed-curve specific checks before closeout.

## P10.1 Acceptance

P10.1 is complete when:

- this plan is tracked in `planning/`;
- Phase 10 child issues are created and linked from the roadmap;
- `ROADMAP.md` marks Phase 10 active and P10.1 complete;
- `CHANGE_LOG.md` records the Phase 10 launch;
- issue `#79` is closed with validation evidence; and
- no new natural curve, managed curve, model-input, XML, Matrix Builder, or
  Patchworks runtime outputs are created or tracked.
