# TFL 6 P3.4d AFLB VDYP First-Growth Run Summary

## Purpose

Materialize natural/untreated first-growth curve evidence for the static TFL 6
AU universe by running VDYP only for the VDYP records whose feature IDs match
stands in the AU-assigned AFLB review table.

This is narrower than a full Stage 01a rebuild. The accepted input surface for
this pass was:

- AU assignment: `planning/tfl6_stand_to_au_review.csv`
- VDYP polygon input: `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet`
- VDYP layer input: `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet`

The tracked run driver is
`scripts/run_p3_4_aflb_vdyp_first_growth.py`.

## Run Artifacts

Review artifacts promoted to `planning/`:

- `planning/tfl6_first_growth_au_curves.csv`
- `planning/tfl6_first_growth_au_fit_diagnostics.csv`
- `planning/tfl6_first_growth_plot_manifest.csv`
- `planning/tfl6_first_growth_plot_manifest.md`
- `planning/tfl6_first_growth_au_remap_audit.csv`
- `planning/tfl6_first_growth_au_remap_audit.md`

Visual review artifacts promoted to `plots/` using the same AU-wise review
families used by the other FEMIC instance examples:

- `plots/vdyp_lmh_tfl6-*.png`
- `plots/vdyp_fitdiag_tfl6-*.png`

Large runtime/audit artifacts remain under ignored runtime output:

- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_yield_timeseries.parquet`
- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_yield_timeseries.csv`
- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_runs.jsonl`
- `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/vdyp_stdout.log`

## Results

- AU-assigned AFLB feature IDs requested: `17,223`
- Feature IDs with VDYP yield evidence: `16,659`
- Stand-level VDYP yield rows generated: `3,220,953`
- AU diagnostics generated: `380`
- Raw accepted first-growth curve candidates: `276`
- Raw insufficient-source AU candidates: `104`
- Source stratum bins in the P3.4b review universe: `384`
- Canonical top-N L/M/H AUs retained as curve families: `77`
- Non-AU source stratum bins remapped/imputed to selected curve families: `307`
- Sparse-support diagnostic flags: `186`
- Selected accepted curve family: `smoothed_bin_pchip`
- L/M/H selected-AU-family comparison plots: `26`
- Selected AU fit diagnostic plots: `77`

## Notes

VDYP output tables used VDYP table/polygon identifiers rather than the source
feature IDs for some batches. The run therefore applied the same order-based
source-ID remap pattern used by the established FEMIC VDYP runner when output
table counts and requested feature counts align closely but output keys do not
match input feature IDs.

The raw first-growth selector produced more candidate curves than the canonical
selected top-area AU universe needs. Current P3.4 artifacts therefore publish
and visually review only the `77` selected top-area AU curves. Non-selected AU
bins are not separate natural-curve families; they are remapped to selected
curve families in `planning/tfl6_first_growth_au_remap_audit.csv` using the
established FEMIC lexicographic stratum-name matching pattern.
