# TFL 6 MP11 Age-Class Extraction Batch

## Purpose

This note records the Phase 7 extraction batch for MP11 age-class distribution
stacked bar charts.

The batch targets:

- `Figure 6`: Base Case Age Class Distribution of Productive Forest Area
  (`187,425 ha`)
- `Figure 45`: AAC Recommendation Age Class Distribution of Productive Forest
  Area (`187,425 ha`)

These figures are relevant to MP11 base-case versus AAC-recommendation
inventory structure and long-horizon age-class dynamics.

## Outputs

Tracked compact summaries:

- `planning/tfl6_mp11_age_class_extraction_summary.csv`
- `planning/tfl6_mp11_age_class_extraction_summary.json`
- `planning/tfl6_mp11_age_class_rows.csv`

Ignored runtime outputs:

- `runtime/document_ingestion/tfl6-mp11-full-figures/recovered/age_class_batch/`
- `runtime/document_ingestion/tfl6-mp11-full-figures/overlays/age_class_batch/`

Script:

```bash
python scripts/build_p7_mp11_age_class_extractions.py
```

## Method

The extraction uses fixed panel bounds and fixed age-class slots for each of
the six subplot years:

- `2023`
- `2073`
- `2123`
- `2173`
- `2223`
- `2273`

For each age-class slot, the script recovers:

- THLB area from the top of the bright green bar fill;
- total productive forest area from the top of the combined green plus dark
  stacked bar fill; and
- NCLB area as `total - THLB`.

The initial extraction picked up top panel borders and legend swatches in the
top-row plots. The final run adds a panel top-exclusion band for those top-row
subplots.

## QA

The primary numeric QA checks are:

- total area should not fall below THLB area; and
- per-panel total area should be close to the stated productive forest area of
  `187,425 ha`.

Results:

- `Figure 6`
  - panels: `6`
  - rows: `54`
  - minimum `total - THLB`: `0 ha`
  - maximum single age-class total: `64,683 ha`
  - panel total range: `183,315` to `200,983 ha`
  - maximum absolute panel-total deviation from `187,425 ha`: `7.23%`
- `Figure 45`
  - panels: `6`
  - rows: `54`
  - minimum `total - THLB`: `249 ha`
  - maximum single age-class total: `64,461 ha`
  - panel total range: `192,119` to `206,740 ha`
  - maximum absolute panel-total deviation from `187,425 ha`: `10.31%`

The overlay contact sheet shows recovered markers aligned with the stacked
bars after top-edge exclusion. The panel-total deviations are still large
enough that this batch should remain `raw_extraction` until a reviewer decides
whether the y-axis calibration and slotting are adequate for planning use.

## Review Status

- Current status: `raw_extraction`
- Downstream use classification: `not_yet_accepted`
- Recommended next status after reviewer inspection:
  `reviewed_for_planning`
- Model-input status: `not_model_input`

These figures should not be accepted for comparison or model input without a
stronger manual review because the chart contains many small stacked bars,
rotated age-class labels, and top-row legends inside the panel area.

The batch was subsequently reviewed in:

- `planning/tfl6_mp11_age_class_review_manifest.md`
- `planning/tfl6_mp11_age_class_review_manifest.csv`
- `planning/tfl6_mp11_age_class_review_manifest.json`

Both figures were promoted to `reviewed_for_planning` with downstream use
`phase6_mp11_age_class_planning_only`, while remaining explicitly
`not_model_input`. They were not promoted to `accepted_for_comparison`.
