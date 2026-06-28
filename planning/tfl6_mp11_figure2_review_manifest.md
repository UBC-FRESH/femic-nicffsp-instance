# TFL 6 MP11 Figure 2 Review Manifest

## Purpose

This note records the review decision for the MP11 Figure 2 base-case
harvest-level extraction pilot. It promotes the pilot to
`accepted_for_comparison` while keeping it out of model-input surfaces.

## Reviewed Inputs

Raw pilot:

- `planning/tfl6_mp11_figure2_extraction_pilot.md`
- `planning/tfl6_mp11_figure2_extraction_pilot.json`

Reviewed manifest:

- `planning/tfl6_mp11_figure2_review_manifest.csv`
- `planning/tfl6_mp11_figure2_review_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_figure2_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The review used the following criteria:

- deterministic extraction, not VLM-estimated values;
- runtime point CSV, extraction JSON, overlay PNG, and metrics JSON exist;
- overlay review confirms extracted points track the flat top edge of the
  plotted harvest-level series;
- mean recovered harvest level is cross-checked against the MP11 base-case
  reference value; and
- reviewed rows remain excluded from model-input surfaces.

## Review Outcome

- Figures reviewed: `1`
- Status counts: `accepted_for_comparison`: `1`
- Figures accepted for comparison: `1`
- Figures accepted for model input: `0`
- Downstream use assigned: `phase6_mp11_comparison_only`
- Model-input status assigned: `not_model_input`

Accepted comparison figure:

- `Figure 2`: Base Case Harvest Level
  - point count: `161`
  - mean recovered value: `1,056,896 m3/year`
  - reference value: `1,061,600 m3/year`
  - mean absolute percent error: `0.44%`

## Phase 6 Handoff

Figure 2 can support MP11 base-case comparison context and should be
handled with the other comparison-only harvest-flow evidence. It should
not be copied into model-input bundles without explicit later review and
promotion.
