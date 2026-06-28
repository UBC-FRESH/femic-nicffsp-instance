# TFL 6 MP11 Old-Seral Extraction Summary

## Purpose

This note records the raw extraction batch for MP11 old-seral
landscape-unit projection charts. The batch covers base-case Figures
`16`-`19` and AAC recommendation Figures `53`-`56`.

The extraction is deterministic and colour-based, but the outputs remain
raw until overlay review confirms that projected actual series were
sampled instead of target lines or axes.

## Outputs

- `planning/tfl6_mp11_old_seral_extraction_summary.csv`
- `planning/tfl6_mp11_old_seral_extraction_summary.json`
- `planning/tfl6_mp11_old_seral_series_summary.csv`
- `planning/tfl6_mp11_old_seral_points.csv`

Ignored runtime detail files are under:

```text
runtime/document_ingestion/tfl6-mp11-full-figures/recovered/old_seral_batch/
runtime/document_ingestion/tfl6-mp11-full-figures/overlays/old_seral_batch/
```

## Current Status

- Figures extracted: `8`
- Series extracted: `30`
- Recovered points: `3542`
- Review status: `raw_extraction`
- Downstream use: `needs_p7_5_review`
- Model-input status: not accepted for model input

## Final-Point Snapshot

- `Figure 16` `CWHvm1 in GMZ/CWHvh1` final: `39.3%`
- `Figure 16` `Other CWHvm1/CWHvm1` final: `27.2%`
- `Figure 16` `CWHvm2` final: `28.3%`
- `Figure 16` `MHmm1` final: `71.9%`
- `Figure 17` `CWHvm1 in GMZ/CWHvh1` final: `31.6%`
- `Figure 17` `Other CWHvm1/CWHvm1` final: `28.3%`
- `Figure 17` `CWHvm2` final: `29.5%`
- `Figure 17` `MHmm1` final: `47.8%`
- `Figure 18` `CWHvm1 in GMZ/CWHvh1` final: `63.7%`
- `Figure 18` `Other CWHvm1/CWHvm1` final: `36.8%`
- `Figure 18` `CWHvm2` final: `39.3%`
- `Figure 18` `MHmm1` final: `64.6%`
- `Figure 19` `Other CWHvm1/CWHvm1` final: `42.3%`
- `Figure 19` `CWHvm2` final: `38.3%`
- `Figure 19` `MHmm1` final: `68.5%`
- `Figure 53` `CWHvm1 in GMZ/CWHvh1` final: `37.5%`
- `Figure 53` `Other CWHvm1/CWHvm1` final: `26.2%`
- `Figure 53` `CWHvm2` final: `27.6%`
- `Figure 53` `MHmm1` final: `72.1%`
- `Figure 54` `CWHvm1 in GMZ/CWHvh1` final: `13.4%`
- `Figure 54` `Other CWHvm1/CWHvm1` final: `27.7%`
- `Figure 54` `CWHvm2` final: `28.6%`
- `Figure 54` `MHmm1` final: `43.4%`
- `Figure 55` `CWHvm1 in GMZ/CWHvh1` final: `64.2%`
- `Figure 55` `Other CWHvm1/CWHvm1` final: `36.1%`
- `Figure 55` `CWHvm2` final: `39.6%`
- `Figure 55` `MHmm1` final: `65.1%`
- `Figure 56` `Other CWHvm1/CWHvm1` final: `41.8%`
- `Figure 56` `CWHvm2` final: `37.3%`
- `Figure 56` `MHmm1` final: `69.5%`

## Next Step

P7.5 should inspect per-figure overlays before promoting these outputs.
Given the lack of adjacent source tables, the expected promotion ceiling is
`reviewed_for_planning` unless a maintainer supplies a stronger validation
basis.
