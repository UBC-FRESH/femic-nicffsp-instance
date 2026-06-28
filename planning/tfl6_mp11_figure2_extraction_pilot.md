# TFL 6 MP11 Figure 2 Extraction Pilot

## Purpose

This note records the first `figrecover` extraction pilot from the TFL 6
Management Plan 11 figure-extraction test. It is a compact, public-safe
planning record, not an accepted model-input table.

The pilot verifies that a high-quality MP11 line/area chart can be manually
cropped, calibrated, digitized, and reviewed through the ignored runtime
artifact convention before the broader Phase 7 extraction batch proceeds.

## Source Figure

- Corpus ID: `tfl6-mp11-full-figures`
- Figure ID: `Figure 2`
- Caption: `Base Case Harvest Level`
- Report component: `Appendix A Timber Supply Analysis`
- Report page: `18`
- PDF page: `82`
- Source URL:
  `https://www.westernforest.com/wp-content/uploads/2026/06/TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf`
- Source SHA256:
  `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- Inventory row:
  `planning/tfl6_mp11_full_figure_inventory.csv`

## Runtime Artifacts

The generated files remain ignored under:

```text
runtime/document_ingestion/tfl6-mp11-full-figures/
```

Pilot artifact paths:

- Manual plot crop:
  `runtime/document_ingestion/tfl6-mp11-full-figures/crops/calibrated_pilot/figure-2-plot.png`
- Raw extraction JSON:
  `runtime/document_ingestion/tfl6-mp11-full-figures/recovered/pilot/figure-2-result.json`
- Raw recovered points CSV:
  `runtime/document_ingestion/tfl6-mp11-full-figures/recovered/pilot/figure-2-points.csv`
- QA overlay:
  `runtime/document_ingestion/tfl6-mp11-full-figures/overlays/pilot/figure-2-overlay.png`
- QA metrics:
  `runtime/document_ingestion/tfl6-mp11-full-figures/overlays/pilot/figure-2-metrics.json`

## Crop And Calibration

The pilot used a manual crop from the rendered PDF page image:

- Source rendered page:
  `runtime/document_ingestion/tfl6-mp11-full-figures/pages/TFL6_MP_11_202606_w_Appendices_Web-compressed-p0082.png`
- Page-image crop bbox: `(155, 145, 1115, 682)`
- Crop image size: `960 x 537` pixels
- Plot frame within crop:
  - left: `128`
  - right: `935`
  - top: `18`
  - bottom: `471`
- X-axis calibration: `0` to `300` years, linear
- Y-axis calibration: `0` to `1,400,000` cubic metres per year, linear,
  inverted pixel axis

The crop and calibration were manually estimated from the rendered page. They
are acceptable as a first pilot but still require reviewer confirmation before
downstream use.

## Extraction Settings

- Tool: `figrecover.digitize`
- Tool version: `0.1.0a1`
- Series name: `base_case_green_top_edge`
- Series colour: `#4cff00`
- Mode: `line`
- Colour tolerance: `80`
- Sample spacing: `5` pixels
- Line aggregation: `min`

The extraction intentionally follows the top edge of the green filled chart
area rather than treating the fill as a polygonal area series.

## Raw Result Summary

- Series count: `1`
- Recovered point count: `161`
- X range: `1.49` to `298.88`
- Y range: `1,047,682` to `1,056,954`
- Mean Y value: `1,056,896`
- Mean point confidence: `1.0`
- Metrics review priority: `low`
- Metrics diagnostics by level: `{"info": 1}`

The recovered values are consistent with the visual reading of the chart: a
near-flat base-case harvest level of approximately `1.06 million m3/year` over
the planning horizon.

## Review Status

- Current status: `raw_extraction`
- Downstream use classification: `not_yet_accepted`
- Required next review:
  - confirm crop excludes caption and unrelated page text;
  - confirm plot-frame bounds against tick marks;
  - confirm axis units and horizon length against MP11 text/tables;
  - inspect QA overlay for edge-tracking artifacts; and
  - decide whether the output can be promoted to `reviewed_for_planning` or
    `accepted_for_comparison`.

This pilot must not be used as model input until it receives explicit review
status, reviewer provenance, and Phase 6 handoff classification.
