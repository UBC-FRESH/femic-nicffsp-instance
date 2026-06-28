# TFL 6 MP11 Growing-Stock Review Manifest

## Purpose

This note records the review decision for the MP11 growing-stock extraction
batch. It promotes Figures `3` and `40` to comparison-ready evidence for
Phase 6 MP11 model-behaviour planning.

The promotion is limited:

- accepted for MP11 comparison planning;
- not accepted as model input;
- based on overlay inspection plus internal component-sum consistency; and
- not a substitute for the stronger adjacent-table cross-check used by the
  harvest-sensitivity batch.

## Reviewed Inputs

Raw extraction batch:

- `planning/tfl6_mp11_growing_stock_extraction_summary.md`
- `planning/tfl6_mp11_growing_stock_extraction_summary.csv`
- `planning/tfl6_mp11_growing_stock_series_summary.csv`

Reviewed manifest:

- `planning/tfl6_mp11_growing_stock_review_manifest.csv`
- `planning/tfl6_mp11_growing_stock_review_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_growing_stock_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The review used the following criteria:

- deterministic extraction, not VLM-estimated values;
- runtime result JSON, recovered-point CSV, overlay PNG, and metrics JSON
  artifacts exist for each figure;
- overlay contact sheet shows recovered points aligned with the intended three
  growing-stock curves;
- internal component-sum residual is less than or equal to `1.0%`; and
- recovered values are intended only for Phase 6 comparison planning.

The internal residual is:

```text
abs((THLB GS <= 120 years + THLB GS > 120 years) - THLB GS total)
/ THLB GS total * 100
```

## Review Outcome

- Figures reviewed: `2`
- Figures accepted for comparison: `2`
- Figures accepted for model input: `0`
- Review status assigned: `accepted_for_comparison`
- Downstream use assigned: `phase6_mp11_comparison_only`
- Model-input status assigned: `not_model_input`

Accepted comparison figures:

- `Figure 3`: Base Case THLB Growing Stock By 1-120 Years Old And 120+ Years
  Old Categories
  - mean absolute component-sum residual: `0.268%`
  - maximum absolute component-sum residual: `0.838%`
- `Figure 40`: AAC Recommendation THLB Growing Stock By 1-120 Years Old
  Categories
  - mean absolute component-sum residual: `0.180%`
  - maximum absolute component-sum residual: `0.743%`

## Phase 6 Handoff

These two figures can be used as Phase 6 comparison evidence for MP11
growing-stock dynamics and base-case versus AAC-recommendation behaviour. They
should be treated as published-plan evidence, not as FEMIC scenario outputs.

They are relevant primarily to:

- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#47`: model behavior, sensitivity, AAC recommendation, and KPI comparison;
  and
- `#48`: MP11-aligned implementation roadmap.

No recovered point table should be copied into model-input surfaces without a
later maintainer review and explicit status promotion to
`accepted_for_model_input`.

## Remaining Work

The review does not cover:

- `Figure 2` pilot review;
- cedar inventory charts;
- old-seral landscape-unit charts;
- age-class bar charts;
- waterfall/impact charts; or
- table-plus-chart hybrid figures.
