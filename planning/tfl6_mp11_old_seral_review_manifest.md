# TFL 6 MP11 Old-Seral Review Manifest

## Purpose

This note records the review decision for the MP11 old-seral
landscape-unit projection extraction batch. It promotes Figures `16`-`19`
and `53`-`56` to planning-reviewed evidence, but not to
comparison-accepted evidence.

The conservative status is intentional. These charts have useful visible
series trajectories, but no adjacent source tables or printed values for
strong numeric validation.

## Reviewed Inputs

Raw extraction batch:

- `planning/tfl6_mp11_old_seral_extraction_summary.md`
- `planning/tfl6_mp11_old_seral_extraction_summary.csv`
- `planning/tfl6_mp11_old_seral_series_summary.csv`
- `planning/tfl6_mp11_old_seral_points.csv`

Reviewed manifest:

- `planning/tfl6_mp11_old_seral_review_manifest.csv`
- `planning/tfl6_mp11_old_seral_review_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_old_seral_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The review used the following criteria:

- deterministic extraction, not VLM-estimated values;
- runtime per-figure CSV and overlay PNG artifacts exist;
- manual plot bounds align with the intended chart panel;
- sampled points visibly track projected actual series rather than axes;
- each figure has adequate per-series point coverage; and
- the lack of source-table cross-check keeps the status planning-only.

## Review Outcome

- Figures reviewed: `8`
- Status counts: `reviewed_for_planning`: `8`
- Figures assigned `reviewed_for_planning`: `8`
- Figures accepted for comparison: `0`
- Figures accepted for model input: `0`
- Downstream use assigned: `phase6_mp11_old_seral_planning_only`
- Model-input status assigned: `not_model_input`

Reviewed planning figures:

- `Figure 16`: Holberg `base_case`, `4` series, `496` points
- `Figure 17`: Keogh `base_case`, `4` series, `411` points
- `Figure 18`: Mahatta `base_case`, `4` series, `500` points
- `Figure 19`: Neroutsos `base_case`, `3` series, `373` points
- `Figure 53`: Holberg `aac_recommendation`, `4` series, `491` points
- `Figure 54`: Keogh `aac_recommendation`, `4` series, `397` points
- `Figure 55`: Mahatta `aac_recommendation`, `4` series, `499` points
- `Figure 56`: Neroutsos `aac_recommendation`, `3` series, `375` points

## Phase 6 Handoff

These figures can support qualitative and approximate Phase 6 planning
around old-seral landscape-unit dynamics under the base case and AAC
recommendation. They should not be used as accepted quantitative
comparison evidence without stronger validation.

They are relevant primarily to:

- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#46`: inventory, yield, operability, and harvest-system assumptions; and
- `#48`: MP11-aligned implementation roadmap.

No recovered point table should be copied into model-input surfaces
without later maintainer review and explicit status promotion.

## Remaining Work

The review does not cover remaining table-plus-chart hybrid figures.
