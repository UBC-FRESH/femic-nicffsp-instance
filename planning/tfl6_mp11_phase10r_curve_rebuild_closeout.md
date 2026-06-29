# TFL 6 MP11 Phase 10R Curve Rebuild Closeout

## Purpose

This note closes Phase 10R: MP11 curve parser and curve rebuild. Phase 10R
parsed the public MP11 managed-yield TIPSY row tables, built a conservative
BatchTIPSY handoff, generated supported future-managed candidate curves through
FEMIC's parent-package BTC runner, regenerated managed and natural comparison
plots, and locked a reproducible curve-generation recipe.

Phase 10R does not promote any generated curve to model input. All generated
curves, comparisons, and diagnostics remain `not_model_input` until a later
maintainer decision explicitly accepts them into a model-contract lane.

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

## Locked Recipe

The reproducible curve-generation recipe is locked in:

- `scripts/run_p10r_mp11_curve_generation_recipe.py`;
- `planning/tfl6_mp11_curve_generation_recipe.md`; and
- `planning/tfl6_mp11_curve_generation_recipe_lock.json`.

Run it from the parent FEMIC checkout:

```powershell
& .\.venv\Scripts\python.exe external/femic-tfl6-instance/scripts/run_p10r_mp11_curve_generation_recipe.py
```

The recipe uses FEMIC's supported BTC command surface:

```powershell
& .\.venv\Scripts\python.exe -m femic tipsy run-btc `
  planning/tfl6_mp11_tipsy_handoff.csv `
  --output-csv runtime/mp11_yield/p10r_mp11_candidate_04_output.csv `
  --error-csv runtime/mp11_yield/p10r_mp11_candidate_04_error.csv `
  --scratch-dir runtime/mp11_yield/scratch `
  --log-dir runtime/mp11_yield/logs `
  --run-id p10r_mp11_candidate `
  --instance-root external/femic-tfl6-instance
```

Do not hand-build BatchTIPSY command syntax for this lane.

## Locked Input Policy

The active handoff emits only MP11 rows that map to canonical top-N TFL 6 AUs:

- accepted AUs are the L/M/H site-index class splits of the top-N strata;
- candidate rows must match canonical AU BEC zone/subzone;
- candidate rows must have species overlap with the canonical AU species combo;
- rows with no canonical top-N AU BEC match remain blocked; and
- blocked rows are not emitted to the BTC handoff.

TIPSY site index is locked to the VRI-derived canonical AU median SI:

- `tipsy_input_si` is copied from `tfl6_static_au_universe.csv:median_si`;
- every positive planted-species SI column in the BTC input row must equal
  `tipsy_input_si`; and
- parsed MP11 per-species SI values are retained as
  `mp11_parsed_weighted_si` provenance only.

## Rebuilt Outputs

The locked recipe currently validates:

| Surface | Output | Current result |
| --- | --- | --- |
| Parsed MP11 TIPSY rows | `planning/tfl6_mp11_tipsy_row_parse.{csv,json,md}` | `141` parsed rows from Tables 54, 55, and 57. |
| BTC handoff | `planning/tfl6_mp11_tipsy_handoff.{csv,json,md}` | `25` supported Table 57 candidate rows. |
| Handoff map | `planning/tfl6_mp11_tipsy_handoff_map.csv` | `25` candidates, `105` Tables 54/55 blocked rows, `2` Table 57 `MH/mm` rows blocked, and `9` parser-review rows. |
| Raw BTC output | `runtime/mp11_yield/p10r_mp11_candidate_04_output.csv` | `25` output rows, retained under ignored runtime space. |
| Raw BTC errors | `runtime/mp11_yield/p10r_mp11_candidate_04_error.csv` | `0` error rows. |
| Parsed managed curves | `planning/tfl6_mp11_managed_curves.{csv,json}` | `900` age-by-curve rows across `25` feature IDs. |
| Managed curve comparison | `planning/tfl6_mp11_managed_curve_comparison.{csv,json,md}` | `25` supported comparison rows. |
| Managed plot manifest | `planning/tfl6_mp11_managed_curve_plot_manifest.{csv,json,md}` | `25` managed Phase 10R-vs-Phase 5 review plots. |
| TIPSY-vs-VDYP diagnostics | `planning/tfl6_mp11_tipsy_vdyp_diagnostic_manifest.{csv,json,md}` | `25` AU-wise diagnostic plots. |
| Reproducibility lock | `planning/tfl6_mp11_curve_generation_recipe_lock.json` | Command sequence, validation, and artifact hashes. |

The PNG plot libraries are intentionally under ignored runtime/review space:

- `plots/mp11_managed_curve_comparison/`;
- `plots/mp11_tipsy_vdyp_diagnostics/`.

## Blocked Rows

Tables 54 and 55 remain blocked for curve generation because their existing and
recent managed AU codes do not carry enough public BEC/site-series information
for direct BatchTIPSY handoff. They require a public-safe MP11 AU-code to
BEC/site-series mapping before they can enter this recipe.

Two Table 57 rows are blocked before BTC handoff:

- `FMH01`;
- `FMH22`.

Both decode to `MH/mm`, and there is no matching canonical top-N `MH/mm` AU in
the active TFL 6 AU universe. They are not BTC inputs, not parsed managed
curves, not comparison rows, and not plotted diagnostic rows in the locked
recipe.

## Remaining Diagnostic Caveat

`Fvh103` remains the only substantially-below-VDYP diagnostic row after the
canonical-top-N and VRI-median-SI repair. It is retained as review evidence but
is not accepted as model input.

The current TIPSY-vs-VDYP diagnostic class counts are:

| Diagnostic class | Row count |
| --- | ---: |
| `tipsy_substantially_above_vdyp` | `17` |
| `tipsy_vdyp_moderate_difference` | `5` |
| `tipsy_vdyp_close` | `2` |
| `tipsy_substantially_below_vdyp` | `1` |

## Validation

The locked recipe validation reports:

- BTC manifest status: `ok`;
- BTC exit code: `0`;
- BTC error rows: `0`;
- handoff rows: `25`;
- candidate rows: `25`;
- managed curve features: `25`;
- managed curve rows: `900`;
- managed plot rows: `25`;
- diagnostic plot rows: `25`;
- BEC mismatch count: `0`; and
- SI mismatch count: `0`.

Focused closeout checks also confirmed:

- obsolete rejected-curve audit artifacts were removed from the active surface;
- obsolete hard-coded review-marker scripts were removed;
- active planning and script surfaces no longer carry the old three-row failed
  review state;
- the new recipe and lock surfaces contain no personal local path fragments;
  and
- the active recipe/generator scripts pass Ruff.

## Phase 11 Boundary

Phase 10R closes with a blocker handoff, not accepted model-input curves. Phase
11 may proceed only to launch and promotion-readiness audit work from the locked
Phase 10R review surfaces. The supported `25` Table 57 future-managed curves can
be used for planning and comparison work, but they remain `not_model_input`.

Before any Phase 11 model-input or ForestModel/XML promotion:

- decide whether `Fvh103` is accepted, repaired, substituted, or excluded;
- decide whether Tables 54/55 are deferred or supplied with a public-safe
  AU-code to BEC/site-series mapping;
- keep `FMH01` and `FMH22` blocked unless a canonical top-N AU mapping is
  explicitly reviewed and added; and
- record any promotion decision in the model-contract surface, not only in
  plot manifests or chat.

P11.1/P11.2 may audit those blockers and write a promotion-readiness decision.
P11.3+ model-input bundle construction and ForestModel XML generation remain
blocked until that audit explicitly accepts, repairs, substitutes, or defers the
open curve cases.
