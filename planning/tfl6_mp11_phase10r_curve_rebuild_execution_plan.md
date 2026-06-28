# TFL 6 MP11 Phase 10R Curve-Rebuild Execution Plan

## Purpose

This P10R.1 plan launches Phase 10R: MP11 curve parser and curve rebuild.
Phase 10R is the first phase that is allowed to claim actual AU/yield curve
rebuild work after the Phase 10 readiness review.

Phase 10R exists because Phase 10 did not rebuild all AUs/yield curves and did
not update curve plots. Phase 10 produced parameter evidence, AU/curve-lane
crosswalks, and diagnostics that showed the required next work: parse the large
MP11 per-AU TIPSY tables, build reviewed curve-generation handoff inputs, run
and parse managed curve generation where supported, and regenerate reviewable
curve plots.

This plan does not generate model-input tables, ForestModel XML, Matrix Builder
outputs, Patchworks runtime artifacts, or scenario outputs.

## Branch And Issue Tree

- Branch: `feature/p10r-curve-rebuild-roadmap-correction`
- Parent issue: `#92`
- Child issues:
  - P10R.1 launch MP11 curve-rebuild execution plan: `#93`;
  - P10R.2 parse MP11 Tables 54, 55, and 57 per-AU TIPSY rows: `#94`;
  - P10R.3 QA managed-yield rows and build BatchTIPSY handoff inputs: `#95`;
  - P10R.4 run and parse MP11 managed curve generation: `#96`;
  - P10R.5 regenerate natural and managed curve plots and overlays: `#97`;
  - P10R.6 close curve-rebuild phase and hand off accepted curve candidates:
    `#98`.

## Governing Inputs

Phase 10R starts from these public-safe Phase 10 surfaces:

- `planning/tfl6_mp11_phase10_execution_plan.md`;
- `planning/tfl6_mp11_phase10_closeout.md`;
- `planning/tfl6_mp11_managed_yield_parameter_library.*`;
- `planning/tfl6_mp11_au_curve_lane_crosswalk.*`;
- `planning/tfl6_mp11_natural_curve_diagnostics.*`;
- `planning/tfl6_mp11_managed_curve_diagnostics.*`.

Phase 10R also uses these governing contracts:

- `planning/tfl6_mp11_baseline_and_promotion_contract.md`;
- `planning/tfl6_mp11_au_yield_strategy_contract.md`;
- `planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md`;
- `planning/tfl6_mp11_kpi_qa_reporting_contract.md`;
- `planning/tfl6_mp11_phase9_closeout.md`.

## Artifact Layout

Tracked planning and compact QA outputs:

- `planning/tfl6_mp11_phase10r_curve_rebuild_execution_plan.md`;
- `planning/tfl6_mp11_tipsy_row_parse.*`;
- `planning/tfl6_mp11_tipsy_handoff.*`;
- `planning/tfl6_mp11_managed_curve_rebuild.*`;
- `planning/tfl6_mp11_curve_plot_manifest.*`;
- `planning/tfl6_mp11_phase10r_closeout.md`.

Potential compact public-safe plots may be tracked only if they are review
artifacts or Sphinx documentation inputs:

- `plots/mp11_yield/`;
- `docs/_static/mp11_yield/`.

Generated runtime-scale outputs should remain ignored unless explicitly
accepted:

- `runtime/mp11_yield/`;
- `runtime/logs/mp11_yield/`;
- `output/mp11_yield/`;
- generated BatchTIPSY scratch files;
- temporary extraction or OCR files.

## Execution Gates

Phase 10R must proceed through these gates:

1. P10R.1 corrects the roadmap boundary and launches this execution plan.
2. P10R.2 parses MP11 Tables 54, 55, and 57 into reviewed per-AU TIPSY rows.
3. P10R.3 joins parsed rows to AU/curve lanes and emits BatchTIPSY/TIPSY
   handoff inputs.
4. P10R.4 runs and parses managed curve generation, or writes a blocker
   package if required tools or reviewed inputs are unavailable.
5. P10R.5 regenerates natural and managed curve plots and overlays where
   accepted inputs exist.
6. P10R.6 closes the phase and hands accepted curve candidates, or an explicit
   blocker package, to Phase 11.

No step may silently substitute MP10/Phase 5 curves as MP11 rebuilt curves.

## P10R.2 Parser Closeout

P10R.2 is complete as a parser-candidate gate, not as model-input promotion.
The implemented parser is
`scripts/build_p10r_mp11_tipsy_row_parse.py`, which reads the public MP11 PDF
from an ignored source-input location and emits:

- `planning/tfl6_mp11_tipsy_row_parse.csv`;
- `planning/tfl6_mp11_tipsy_row_parse.json`;
- `planning/tfl6_mp11_tipsy_row_parse.md`.

The parser extracted `141` per-AU TIPSY rows:

- Table 54 early managed rows: `79`;
- Table 55 recent managed rows: `34`;
- Table 57 future managed rows: `28`.

The QA split is `132` high-confidence parser candidates and `9`
review-required rows. Review-required rows include seven species-percentage
totals above 100 in the visible table text and two known page-break repairs
(`R301` and `Fvm205`). These rows remain `not_model_input`; P10R.3 must join
the parsed rows to AU/curve lanes and either accept, repair, or explicitly
quarantine review-required rows before handoff generation.

## Plot-Refresh Requirement

P10R.5 is the task that updates curve plots. Plot outputs must distinguish:

- newly regenerated MP11 managed curve plots;
- refreshed natural curve review plots;
- Phase 5 baseline comparison plots;
- blocked or missing curve families; and
- curves that remain comparison-only or `not_model_input`.

The plot manifest must record source tables, curve-generation command
provenance, plot paths, review status, and model-input eligibility.

## Phase 11 Blocker

Phase 11 is planned and blocked until Phase 10R closes. Phase 11 may proceed
only after one of these outcomes:

- Phase 10R produces accepted curve candidates and refreshed review plots; or
- the maintainer explicitly accepts a blocker path that allows Phase 11 to
  build only stop reports or comparison manifests.

Phase 11 must not promote Phase 10 readiness outputs as accepted MP11 curve
inputs.

## Minimum Validation

Every Phase 10R child issue must run, at minimum:

```bash
python -m ruff check .
```

Tasks that touch docs must also run:

```bash
sphinx-build -b html docs docs/_build/html -W
```

Implementation tasks must also run their relevant parser, handoff, curve, or
plot generation scripts before closeout.

## Private-Data Hygiene

Phase 10R must not commit private WFP source layers, proprietary LEFI/ITI/LiDAR
attributes, private curve files, generated scratch outputs, unpublished
recovered tables, model-input bundles, ForestModel XML, Matrix Builder outputs,
Patchworks runtime artifacts, or private prompt logs. Public-safe planning
surfaces must preserve provenance and explicitly mark outputs as review
candidates until a later promotion gate accepts them.
