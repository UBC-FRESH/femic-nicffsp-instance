# TFL 6 MP11 Cedar Inventory Review Manifest

## Purpose

This note records the review decision for the MP11 cedar inventory extraction
batch. It promotes Figures `14`, `15`, `51`, and `52` to planning-reviewed
evidence for Phase 6 cedar-assumption review, but does not promote them to
comparison-accepted evidence.

The conservative status is intentional. These stacked-area charts have clean
overlays after sampler correction, but they do not have adjacent table values
or an internal component-sum identity as strong as the growing-stock charts.

## Reviewed Inputs

Raw extraction batch:

- `planning/tfl6_mp11_cedar_inventory_extraction_summary.md`
- `planning/tfl6_mp11_cedar_inventory_extraction_summary.csv`
- `planning/tfl6_mp11_cedar_inventory_series_summary.csv`

Reviewed manifest:

- `planning/tfl6_mp11_cedar_inventory_review_manifest.csv`
- `planning/tfl6_mp11_cedar_inventory_review_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_cedar_inventory_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The review used the following criteria:

- deterministic extraction, not VLM-estimated values;
- runtime result JSON, recovered-point CSV, overlay PNG, and metrics JSON
  artifacts exist for each figure;
- overlay contact sheet shows recovered points aligned with stacked-area
  boundaries after total-boundary and THLB-boundary y-band correction;
- total cedar volume remains greater than or equal to THLB cedar volume for
  each figure summary; and
- recovered values are intended only for Phase 6 cedar planning.

## Review Outcome

- Figures reviewed: `4`
- Figures assigned `reviewed_for_planning`: `4`
- Figures accepted for comparison: `0`
- Figures accepted for model input: `0`
- Downstream use assigned: `phase6_mp11_cedar_planning_only`
- Model-input status assigned: `not_model_input`

Reviewed planning figures:

- `Figure 14`: Base Case Cedar Inventory in Productive Forests
  - minimum `total - THLB`: `937,500 m3`
- `Figure 15`: Base Case Old Cedar Inventory in Productive Forests
  - minimum `total - THLB`: `2,756,637 m3`
- `Figure 51`: AAC Recommendation Cedar Inventory in Productive Forest
  - minimum `total - THLB`: `1,250,000 m3`
- `Figure 52`: AAC Recommendation Old Cedar Inventory in Productive Forest
  - minimum `total - THLB`: `3,871,681 m3`

## Phase 6 Handoff

These four figures can support Phase 6 cedar planning, especially comparison
of base-case and AAC-recommendation cedar trajectories and later decisions
about cedar-specific model-design assumptions.

They are relevant primarily to:

- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#46`: inventory, yield, operability, and harvest-system assumptions; and
- `#48`: MP11-aligned implementation roadmap.

They should not be treated as comparison-accepted quantitative evidence until
a stronger review is completed. No recovered point table should be copied into
model-input surfaces without a later maintainer review and explicit promotion
to `accepted_for_model_input`.

## Remaining Work

The review does not cover:

- `Figure 2` pilot review;
- old-seral landscape-unit charts;
- age-class bar charts;
- waterfall/impact charts; or
- table-plus-chart hybrid figures.
