# TFL 6 MP11 Remaining Harvest Scenario Review Manifest

## Purpose

This note records the review decision for the remaining MP11
harvest/scenario line-chart extraction batch. It promotes the batch to
comparison-accepted evidence while keeping every row out of model-input
surfaces.

## Reviewed Inputs

Raw extraction batch:

- `planning/tfl6_mp11_remaining_harvest_extraction_summary.md`
- `planning/tfl6_mp11_remaining_harvest_extraction_summary.csv`
- `planning/tfl6_mp11_remaining_harvest_series_summary.csv`
- `planning/tfl6_mp11_remaining_harvest_points.csv`

Reviewed manifest:

- `planning/tfl6_mp11_remaining_harvest_review_manifest.csv`
- `planning/tfl6_mp11_remaining_harvest_review_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_remaining_harvest_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The review used the following criteria:

- deterministic extraction, not VLM-estimated values;
- runtime per-figure CSV and overlay PNG artifacts exist;
- overlay review confirms line sampling follows the intended plotted series;
- endpoint values are cross-checked against visible table or narrative values;
- maximum endpoint absolute percent error is below threshold; and
- reviewed rows remain excluded from model-input surfaces.

## Review Outcome

- Figures reviewed: `11`
- Status counts: `accepted_for_comparison`: `11`
- Figures accepted for comparison: `11`
- Figures accepted for model input: `0`
- Downstream use assigned: `phase6_mp11_comparison_only`
- Model-input status assigned: `not_model_input`

Accepted comparison figures:

- `Figure 21`: Harvest Levels Maintaining Current AAC; max endpoint error `0.29%`
- `Figure 22`: Harvest Levels Maximizing Short-Term Harvest; max endpoint error `0.14%`
- `Figure 23`: Harvest Levels with Increased Natural Stand Yields; max endpoint error `0.14%`
- `Figure 24`: Harvest Levels with Decreased Natural Stand Yields; max endpoint error `0.14%`
- `Figure 25`: Harvest Levels with Increased Managed Stand Yields; max endpoint error `0.14%`
- `Figure 26`: Harvest Levels with Decreased Managed Stand Yields; max endpoint error `0.14%`
- `Figure 32`: Comparison of Harvest Scenarios: Base Case vs. Two Flows on ITI-Adjusted Volume with Reduced OAF1 Scenario; max endpoint error `0.14%`
- `Figure 33`: Harvest Levels with No Genetic Gain; max endpoint error `0.24%`
- `Figure 34`: Harvest Levels with Full NSOG Order Targets; max endpoint error `0.14%`
- `Figure 37`: Harvest Levels with Helicopter Operable Land Base Excluded; max endpoint error `0.14%`
- `Figure 38`: Harvest Levels with 10% THLB Increases; max endpoint error `0.14%`

## Phase 6 Handoff

These figures can support MP11 harvest-scenario comparison planning and
sensitivity interpretation. They should not be copied into model-input
bundles without explicit later review and promotion.

They are relevant primarily to:

- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#46`: inventory, yield, operability, and harvest-system assumptions; and
- `#47`: model behavior, sensitivities, AAC, and KPI comparison.

## Remaining Work

The review does not cover any lower-priority figures outside the Phase 7
high-priority queue.
