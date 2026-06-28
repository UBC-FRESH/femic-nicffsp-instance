# TFL 6 MP11 Harvest Sensitivity Extraction Batch

## Purpose

This note records the first repeatable Phase 7 extraction batch beyond the
single Figure 2 pilot. It targets simple two-series MP11 harvest-level
sensitivity charts that have adjacent MP11 summary table values for QA.

The batch remains `raw_extraction` evidence. It is useful for testing the
workflow and planning MP11 comparison surfaces, but it is not accepted model
input.

## Batch Scope

Figures extracted:

- `Figure 29`: Harvest Levels with Adjusted ITI Stand Yields
- `Figure 30`: Harvest Levels with ITI adjusted volumes and LiDAR-derived
  Height and Site Index
- `Figure 31`: Harvest Levels with ITI adjusted volumes, LiDAR-derived Height
  and Site Index, and reduced OAF1
- `Figure 35`: Harvest Levels with MHA Increased by 10 Years
- `Figure 36`: Harvest Levels with MHA Decreased by 10 Years
- `Figure 39`: Harvest Levels with 10% THLB Decreases

Tracked summary outputs:

- `planning/tfl6_mp11_harvest_sensitivity_extraction_summary.csv`
- `planning/tfl6_mp11_harvest_sensitivity_extraction_summary.json`
- `planning/tfl6_mp11_harvest_sensitivity_series_summary.csv`

Ignored runtime outputs:

- `runtime/document_ingestion/tfl6-mp11-full-figures/recovered/harvest_sensitivity_batch/`
- `runtime/document_ingestion/tfl6-mp11-full-figures/overlays/harvest_sensitivity_batch/`

## Method

The batch uses:

```bash
python scripts/build_p7_mp11_harvest_sensitivity_extractions.py
```

The script applies manual plot-frame calibrations to the proposed crop images,
then samples only the dominant long colour component for each series. This
excludes legend swatches and body text from the numeric extraction while still
using deterministic image evidence rather than VLM-estimated values.

Manual calibration assumptions:

- X axis: `0` to `300` years
- Y axis: `0` to `1,400,000 m3/year`
- Series:
  - bright green `base_case`
  - dark green/black scenario line
- Status: `raw_extraction`

## QA Against MP11 Tables

The extracted mean values were compared against the adjacent MP11 table value
for each series.

- Figures processed: `6`
- Series processed: `12`
- Maximum absolute percent error against table values: `0.503%`
- Mean base-case extraction error range: approximately `0.07%` to `0.31%`
- Scenario extraction error range: approximately `0.10%` to `0.50%`

The largest error is for `Figure 29` adjusted ITI volume, where the extracted
scenario mean is approximately `5,428 m3/year` below the MP11 table value.

## Review Status

- Current status: `raw_extraction`
- Downstream use classification: `not_yet_accepted`
- Required next review:
  - inspect full-resolution overlays;
  - verify plot-frame bounds against tick marks;
  - confirm series labels and table cross-check values;
  - decide whether these six figures can be promoted to
    `reviewed_for_planning` or `accepted_for_comparison`; and
  - record reviewer provenance before Phase 6 handoff.

No recovered table from this batch should be used as model input until Phase 7
review promotes it explicitly.
