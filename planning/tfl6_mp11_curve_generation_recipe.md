# TFL 6 MP11 Curve Generation Recipe

## Purpose

This note locks the reproducible Phase 10R managed-curve generation recipe for
MP11 Table 57 future-managed candidates.

The recipe is a review surface only. It does not promote any generated curve to
model input. All generated rows remain `not_model_input` until a later
maintainer decision explicitly accepts them for the next model lane.

## Locked Recipe Runner

Run the full managed-curve recipe from the parent FEMIC checkout:

```powershell
& .\.venv\Scripts\python.exe external/femic-tfl6-instance/scripts/run_p10r_mp11_curve_generation_recipe.py
```

The runner executes the following sequence:

1. `external/femic-tfl6-instance/scripts/build_p10r_mp11_tipsy_handoff.py`
2. `python -m femic tipsy run-btc planning/tfl6_mp11_tipsy_handoff.csv ...`
3. `external/femic-tfl6-instance/scripts/build_p10r_mp11_managed_curve_rebuild_blocker.py`
4. `external/femic-tfl6-instance/scripts/build_p10r_mp11_managed_curve_comparison.py`
5. clean stale `plots/mp11_managed_curve_comparison/*.png`
6. `external/femic-tfl6-instance/scripts/build_p10r_mp11_managed_curve_plots.py`
7. clean stale `plots/mp11_tipsy_vdyp_diagnostics/*.png`
8. `external/femic-tfl6-instance/scripts/build_p10r_mp11_tipsy_vdyp_diagnostics.py`

The runner writes the reproducibility lock manifest:

- `planning/tfl6_mp11_curve_generation_recipe_lock.json`

That JSON records the command sequence, validation results, and SHA-256 hashes
for the primary handoff, BTC, parsed-curve, comparison, and diagnostic manifest
artifacts.

## Locked Input Policy

Candidate generation is limited to MP11 rows that map to canonical top-N TFL 6
AUs:

- accepted AUs are only the L/M/H site-index class splits of the top-N strata;
- candidate rows must match canonical AU BEC zone/subzone;
- candidate rows must have species overlap with the canonical AU species combo;
- rows with no canonical top-N AU BEC match remain blocked; and
- blocked rows are not emitted to the BTC handoff.

TIPSY site index is locked to the VRI-derived canonical AU median SI:

- `tipsy_input_si` is copied from `tfl6_static_au_universe.csv:median_si`;
- every positive planted-species SI column in the BTC input row must equal
  `tipsy_input_si`;
- parsed MP11 per-species SI values are retained as
  `mp11_parsed_weighted_si` provenance only; and
- generated curves remain review surfaces, not accepted model contracts.

## Runtime Boundary

The BTC execution step uses FEMIC's parent-package command surface:

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

Do not hand-build BatchTIPSY command syntax outside FEMIC's BTC runner for this
lane.

## Validation Gates

The recipe runner fails if any of these checks fail:

- BTC manifest status is not `ok`;
- BTC exit code is not `0`;
- BTC error output has any rows;
- handoff candidate count differs from the candidate map count;
- any BTC handoff candidate uses `MH/mm`;
- any managed curve, comparison, or diagnostic row contains blocked `FMH*`
  curves;
- any positive planted-species SI column differs from `tipsy_input_si`;
- any expected managed-curve comparison PNG is missing or empty;
- any plotted TIPSY-vs-VDYP comparison has a BEC prefix mismatch; or
- any expected diagnostic PNG is missing or empty.

## Current Locked Outcome

The locked Phase 10R recipe currently emits:

- `25` BTC handoff candidate rows;
- `25` BTC output rows with `0` BTC error rows;
- `900` managed-curve rows across `25` feature IDs;
- `25` managed-curve comparison plots;
- `25` TIPSY-vs-VDYP diagnostic plots;
- no `MH/mm` handoff candidates;
- no plotted BEC mismatches; and
- one remaining substantially-below-VDYP diagnostic row, `Fvh103`.
