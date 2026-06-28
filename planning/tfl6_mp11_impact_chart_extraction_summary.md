# TFL 6 MP11 Timber-Supply Impact Extraction Summary

## Purpose

This note records the raw extraction batch for the MP11 waterfall-style
timber-supply impact charts. The batch covers Figures `20` and `57`,
which summarize the transition from MP10/current AAC assumptions to the
MP11 base case and AAC recommendation.

The extracted values are printed chart labels checked against
deterministic coloured-component geometry. They are not model inputs.

## Outputs

- `planning/tfl6_mp11_impact_chart_extraction_summary.csv`
- `planning/tfl6_mp11_impact_chart_extraction_summary.json`
- `planning/tfl6_mp11_impact_chart_rows.csv`

Ignored runtime detail files are under:

```text
runtime/document_ingestion/tfl6-mp11-full-figures/recovered/impact_batch/
runtime/document_ingestion/tfl6-mp11-full-figures/overlays/impact_batch/
```

## Current Status

- Figures extracted: `2`
- Review status: `raw_extraction`
- Downstream use: `needs_p7_5_review`
- Model-input status: not accepted for model input
- Printed endpoint totals: Figure 20: 1,061,600, Figure 57: 1,252,700
- Maximum geometry-vs-label residual: `6,261 m3/year`

## Next Step

P7.5 should review the overlays and decide whether these figures can be
promoted to `accepted_for_comparison` or should remain planning-only.
