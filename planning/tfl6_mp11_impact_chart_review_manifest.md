# TFL 6 MP11 Impact Chart Review Manifest

## Purpose

This note records the review decision for the MP11 timber-supply impact
waterfall chart extraction batch. It promotes Figures `20` and `57` to
comparison-accepted evidence for MP10-to-MP11 planning, while keeping
them out of model-input surfaces.

## Reviewed Inputs

Raw extraction batch:

- `planning/tfl6_mp11_impact_chart_extraction_summary.md`
- `planning/tfl6_mp11_impact_chart_extraction_summary.csv`
- `planning/tfl6_mp11_impact_chart_rows.csv`

Reviewed manifest:

- `planning/tfl6_mp11_impact_chart_review_manifest.csv`
- `planning/tfl6_mp11_impact_chart_review_manifest.json`

Review helper:

```bash
python scripts/build_p7_mp11_impact_chart_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z
```

## Review Criteria

The review used the following criteria:

- extracted values are printed chart labels, not VLM estimates;
- deterministic coloured-component geometry identifies the matching bars;
- runtime per-figure step CSV and overlay PNG artifacts exist;
- waterfall arithmetic residual is zero; and
- maximum geometry-vs-label residual is below the review threshold.

## Review Outcome

- Figures reviewed: `2`
- Status counts: `accepted_for_comparison`: `2`
- Figures accepted for comparison: `2`
- Figures accepted for model input: `0`
- Downstream use assigned: `phase6_mp11_comparison_only`
- Model-input status assigned: `not_model_input`

Accepted comparison figures:

- `Figure 20`: Timber Supply Impacts since MP #10 to Base Case
  - accepted printed endpoint: `1,061,600 m3/year`
  - arithmetic residual: `0 m3/year`
  - maximum geometry-vs-label residual: `4,609 m3/year`
- `Figure 57`: Updated Timber Supply Impacts Since MP #10
  - accepted printed endpoint: `1,252,700 m3/year`
  - arithmetic residual: `0 m3/year`
  - maximum geometry-vs-label residual: `6,261 m3/year`

## Phase 6 Handoff

These figures can support MP10-to-MP11 comparison planning and narrative
checks around the base-case and AAC-recommendation bridge. They should
not be copied into model-input bundles without explicit later review.

They are relevant primarily to:

- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#46`: inventory, yield, operability, and harvest-system assumptions; and
- `#47`: model behavior, sensitivities, AAC, and KPI comparison.

## Remaining Work

The review does not cover old-seral landscape-unit charts or remaining
table-plus-chart hybrid figures.
