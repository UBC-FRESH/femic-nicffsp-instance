# TFL 6 MP11 Age-Class Review Manifest

## Purpose

This note records the review decision for the MP11 age-class distribution
extraction batch. It promotes Figures `6` and `45` to planning-reviewed
evidence, but does not promote them to comparison-accepted evidence.

The conservative status is intentional. These multi-panel stacked-bar figures
are useful for understanding MP11 age-class dynamics, but the recovered panel
totals deviate materially from the stated productive forest area.

## Reviewed Inputs

Raw extraction batch:

- `planning/tfl6_mp11_age_class_extraction_summary.md`
- `planning/tfl6_mp11_age_class_extraction_summary.csv`
- `planning/tfl6_mp11_age_class_rows.csv`

Reviewed manifest:

- `planning/tfl6_mp11_age_class_review_manifest.csv`
- `planning/tfl6_mp11_age_class_review_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_age_class_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The review used the following criteria:

- deterministic extraction, not VLM-estimated values;
- runtime per-figure CSV and overlay PNG artifacts exist for each figure;
- overlay contact sheet shows recovered markers aligned with stacked bars after
  panel-border and legend-swath corrections;
- total area remains greater than or equal to THLB area; and
- panel-total deviation from the stated `187,425 ha` productive forest area is
  recorded explicitly.

## Review Outcome

- Figures reviewed: `2`
- Figures assigned `reviewed_for_planning`: `2`
- Figures accepted for comparison: `0`
- Figures accepted for model input: `0`
- Downstream use assigned: `phase6_mp11_age_class_planning_only`
- Model-input status assigned: `not_model_input`
- Panel-total deviation status: `warning`

Reviewed planning figures:

- `Figure 6`: Base Case Age Class Distribution of Productive Forest Area
  - maximum panel-total deviation from `187,425 ha`: `7.23%`
  - minimum `total - THLB`: `0 ha`
- `Figure 45`: AAC Recommendation Age Class Distribution of Productive Forest
  Area
  - maximum panel-total deviation from `187,425 ha`: `10.31%`
  - minimum `total - THLB`: `249 ha`

## Phase 6 Handoff

These two figures can support qualitative and approximate Phase 6 planning
around age-class dynamics. They should not be used as accepted quantitative
comparison evidence without a stronger manual review or improved digitization.

They are relevant primarily to:

- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#46`: inventory, yield, operability, and harvest-system assumptions; and
- `#48`: MP11-aligned implementation roadmap.

No recovered point table should be copied into model-input surfaces without a
later maintainer review and explicit status promotion to
`accepted_for_model_input`.

## Remaining Work

The review does not cover:

- `Figure 2` pilot review;
- old-seral landscape-unit charts;
- waterfall/impact charts; or
- table-plus-chart hybrid figures.
