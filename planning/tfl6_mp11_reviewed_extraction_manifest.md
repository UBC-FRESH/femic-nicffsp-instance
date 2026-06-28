# TFL 6 MP11 Reviewed Extraction Manifest

## Purpose

This note records the first Phase 7 review decision for recovered MP11 figure
data. It promotes only the first six simple harvest-sensitivity extractions to
comparison-ready evidence for Phase 6 MP11 planning.

The promotion is deliberately narrow:

- accepted for MP11 comparison planning;
- not accepted as model input;
- not a general acceptance of all high-priority figure crops; and
- subject to maintainer override if full-resolution overlay review finds an
  issue later.

## Reviewed Inputs

Raw extraction batch:

- `planning/tfl6_mp11_harvest_sensitivity_extraction_summary.md`
- `planning/tfl6_mp11_harvest_sensitivity_extraction_summary.csv`
- `planning/tfl6_mp11_harvest_sensitivity_series_summary.csv`

Reviewed manifest:

- `planning/tfl6_mp11_reviewed_extraction_manifest.csv`
- `planning/tfl6_mp11_reviewed_extraction_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The first review pass used the following criteria:

- deterministic extraction, not VLM-estimated values;
- runtime result JSON, recovered-point CSV, overlay PNG, and metrics JSON
  artifacts exist for each figure;
- overlay contact sheet shows recovered series aligned with the intended chart
  lines;
- adjacent MP11 table cross-check error is less than or equal to `1.0%`; and
- recovered values are intended only for Phase 6 comparison planning.

## Review Outcome

- Figures reviewed: `6`
- Figures accepted for comparison: `6`
- Figures accepted for model input: `0`
- Maximum absolute percent error against MP11 table values: `0.503%`
- Review status assigned: `accepted_for_comparison`
- Downstream use assigned: `phase6_mp11_comparison_only`
- Model-input status assigned: `not_model_input`

Accepted comparison figures:

- `Figure 29`: Harvest Levels with Adjusted ITI Stand Yields
- `Figure 30`: Harvest Levels with ITI adjusted volumes and LiDAR-derived
  Height and Site Index
- `Figure 31`: Harvest Levels with ITI adjusted volumes, LiDAR-derived Height
  and Site Index, and reduced OAF1
- `Figure 35`: Harvest Levels with MHA Increased by 10 Years
- `Figure 36`: Harvest Levels with MHA Decreased by 10 Years
- `Figure 39`: Harvest Levels with 10% THLB Decreases

## Phase 6 Handoff

These six figures can be used as Phase 6 comparison evidence for MP11
sensitivity assumptions and model-overhaul planning. They should be treated as
published-plan evidence, not as new FEMIC scenario outputs.

They are relevant primarily to:

- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#47`: model behavior, sensitivity, AAC recommendation, and KPI comparison;
  and
- `#48`: MP11-aligned implementation roadmap.

No raw recovered point table should be copied into model-input surfaces without
a later maintainer review and explicit status promotion to
`accepted_for_model_input`.

## Remaining Work

The review does not cover:

- `Figure 2` pilot review;
- multi-series growing-stock charts;
- cedar inventory charts;
- old-seral landscape-unit charts;
- age-class bar charts;
- waterfall/impact charts; or
- table-plus-chart hybrid figures.

Those remain under P7.4/P7.5 follow-on extraction and review.
