# TFL 6 MP11 Growing-Stock Extraction Batch

## Purpose

This note records the first Phase 7 extraction batch for multi-series THLB
growing-stock charts in the MP11 timber-supply appendix.

The batch targets:

- `Figure 3`: Base Case THLB Growing Stock By 1-120 Years Old And 120+ Years
  Old Categories
- `Figure 40`: AAC Recommendation THLB Growing Stock By 1-120 Years Old
  Categories

These charts are important for MP10-to-MP11 model-behaviour comparison because
they describe the planning-horizon growing-stock dynamics behind the base case
and AAC recommendation.

## Outputs

Tracked compact summaries:

- `planning/tfl6_mp11_growing_stock_extraction_summary.csv`
- `planning/tfl6_mp11_growing_stock_extraction_summary.json`
- `planning/tfl6_mp11_growing_stock_series_summary.csv`

Ignored runtime outputs:

- `runtime/document_ingestion/tfl6-mp11-full-figures/recovered/growing_stock_batch/`
- `runtime/document_ingestion/tfl6-mp11-full-figures/overlays/growing_stock_batch/`

Script:

```bash
python scripts/build_p7_mp11_growing_stock_extractions.py
```

## Method

The extraction uses manual plot-frame calibration and deterministic
colour/y-band sampling:

- X axis: `0` to `300` years
- Y axis: `0` to `45,000,000 m3`
- Series:
  - black: `THLB GS total`
  - bright green: `THLB GS <= 120 years`
  - dark green: `THLB GS > 120 years`

The sampler uses per-series vertical bands and nearest-y continuity tracking to
avoid axis lines, grid marks, and legend swatches. This was necessary because
the dark-green series is close enough to black that a naive colour mask can
pick up plot axes, and the bright-green series can otherwise pick up legend
marks.

## QA

The available numeric QA check is internal consistency:

```text
THLB GS total ~= THLB GS <= 120 years + THLB GS > 120 years
```

Results:

- `Figure 3`
  - series: `3`
  - total points: `478`
  - mean absolute component-sum residual: `0.268%`
  - maximum absolute component-sum residual: `0.838%`
- `Figure 40`
  - series: `3`
  - total points: `476`
  - mean absolute component-sum residual: `0.180%`
  - maximum absolute component-sum residual: `0.743%`

The overlay contact sheet shows the recovered points tracking the intended
three chart lines after the y-band/continuity corrections.

## Review Status

- Current status: `raw_extraction`
- Downstream use classification: `not_yet_accepted`
- Recommended next status after reviewer inspection:
  `reviewed_for_planning` or `accepted_for_comparison`
- Model-input status: `not_model_input`

Unlike the first harvest-sensitivity batch, these figures do not have adjacent
table values for an independent exact cross-check. The internal residuals are
strong enough to justify review, but a maintainer should inspect full-resolution
overlays before promoting the batch to Phase 6 comparison evidence.

The batch was subsequently reviewed in:

- `planning/tfl6_mp11_growing_stock_review_manifest.md`
- `planning/tfl6_mp11_growing_stock_review_manifest.csv`
- `planning/tfl6_mp11_growing_stock_review_manifest.json`

Both figures were promoted to `accepted_for_comparison` with downstream use
`phase6_mp11_comparison_only`, while remaining explicitly `not_model_input`.
