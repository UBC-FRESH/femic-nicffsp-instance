# TFL 6 MP11 Cedar Inventory Extraction Batch

## Purpose

This note records the Phase 7 extraction batch for MP11 cedar inventory
stacked-area charts.

The batch targets:

- `Figure 14`: Base Case Cedar Inventory in Productive Forests
- `Figure 15`: Base Case Old Cedar Inventory in Productive Forests
- `Figure 51`: AAC Recommendation Cedar Inventory in Productive Forest
- `Figure 52`: AAC Recommendation Old Cedar Inventory in Productive Forest

These figures are relevant to MP11 cedar-signal comparison and later review of
cedar-specific model-design assumptions.

## Outputs

Tracked compact summaries:

- `planning/tfl6_mp11_cedar_inventory_extraction_summary.csv`
- `planning/tfl6_mp11_cedar_inventory_extraction_summary.json`
- `planning/tfl6_mp11_cedar_inventory_series_summary.csv`

Ignored runtime outputs:

- `runtime/document_ingestion/tfl6-mp11-full-figures/recovered/cedar_inventory_batch/`
- `runtime/document_ingestion/tfl6-mp11-full-figures/overlays/cedar_inventory_batch/`

Script:

```bash
python scripts/build_p7_mp11_cedar_inventory_extractions.py
```

## Method

The extraction uses manual panel bounds and deterministic stacked-area boundary
sampling.

For each panel, the script recovers:

- THLB cedar volume from the top edge of the bright green fill;
- total productive cedar volume from the top edge of the combined green plus
  dark fill; and
- implied NCLB cedar volume as `total - THLB`.

Figures `14` and `51` have two panels:

- yellow cedar;
- western red cedar.

Figures `15` and `52` have one old-cedar panel.

## QA

The main numeric sanity check is that total cedar volume should not fall below
THLB cedar volume.

Results:

- `Figure 14`
  - panels: `2`
  - series: `6`
  - total points: `408`
  - minimum `total - THLB`: `937,500 m3`
- `Figure 15`
  - panels: `1`
  - series: `3`
  - total points: `474`
  - minimum `total - THLB`: `2,756,637 m3`
- `Figure 51`
  - panels: `2`
  - series: `6`
  - total points: `408`
  - minimum `total - THLB`: `1,250,000 m3`
- `Figure 52`
  - panels: `1`
  - series: `3`
  - total points: `474`
  - minimum `total - THLB`: `3,871,681 m3`

The overlay contact sheet shows recovered points tracking the intended stacked
area boundaries after separate total-boundary and THLB-boundary y-bands were
added to avoid legend/axis contamination.

## Review Status

- Current status: `raw_extraction`
- Downstream use classification: `not_yet_accepted`
- Recommended next status after reviewer inspection:
  `reviewed_for_planning` or `accepted_for_comparison`
- Model-input status: `not_model_input`

These figures do not have adjacent table values for an independent exact
cross-check. The current evidence is appropriate for review and planning, but a
maintainer should inspect full-resolution overlays before promoting the batch
to Phase 6 comparison evidence.

The batch was subsequently reviewed in:

- `planning/tfl6_mp11_cedar_inventory_review_manifest.md`
- `planning/tfl6_mp11_cedar_inventory_review_manifest.csv`
- `planning/tfl6_mp11_cedar_inventory_review_manifest.json`

All four figures were promoted to `reviewed_for_planning` with downstream use
`phase6_mp11_cedar_planning_only`, while remaining explicitly
`not_model_input`. They were not promoted to `accepted_for_comparison`.
