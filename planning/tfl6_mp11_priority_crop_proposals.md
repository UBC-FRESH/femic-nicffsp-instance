# TFL 6 MP11 Priority Crop Proposals

## Purpose

This note records the first repeatable crop-proposal pass for the Phase 7
high-priority MP11 figure queue. The proposals are review aids for P7.3; they
are not accepted extraction crops and do not replace manual crop/calibration
review.

The proposal pass uses the instance-local script:

```bash
python scripts/build_p7_mp11_crop_proposals.py
```

## Inputs

- Priority queue:
  `planning/tfl6_mp11_priority_figure_crop_queue.csv`
- Preliminary full-content crops:
  `runtime/document_ingestion/tfl6-mp11-full-figures/crops/priority_high_preliminary/`

The preliminary crops remain ignored runtime artifacts.

## Outputs

Tracked compact summaries:

- `planning/tfl6_mp11_priority_crop_proposals.csv`
- `planning/tfl6_mp11_priority_crop_proposals.json`

Ignored proposed crop images:

- `runtime/document_ingestion/tfl6-mp11-full-figures/crops/priority_high_proposals/`

Each summary row records:

- figure ID and caption;
- chart-family and priority triage;
- preliminary crop path;
- proposed crop path;
- proposed bbox in preliminary-crop pixel coordinates;
- proposed crop dimensions;
- proposed crop SHA256; and
- proposal/review status.

## Method

The script detects saturated green/magenta chart marks while suppressing most
black body text, joins nearby chart marks with morphological operations, and
uses the union of retained connected components as the proposed crop bbox. This
works well enough to create a review queue for the clean MP11 PDF, but it is
not a general figure detector.

## Run Summary

- Priority rows processed: `36`
- Proposed crops written: `36`
- Missing preliminary crops: `0`
- Rows without colour bbox: `0`
- Review status assigned to all proposals: `needs_manual_crop_review`

The proposal contact sheet looked good enough for batch review, but several
rows still include surrounding explanatory text, tables, or multiple panels.
Those rows require manual trimming before deterministic extraction.

## Review Notes

Likely near-term deterministic extraction targets:

- `Figure 2`: simple harvest-level line/area chart; already piloted.
- `Figure 3`: multi-series growing-stock line chart.
- `Figure 14`, `Figure 15`, `Figure 51`, `Figure 52`: cedar inventory
  area/line charts.
- `Figure 23` through `Figure 39`: mostly single-axis sensitivity charts, many
  with related summary tables on the same page.
- `Figure 40`: AAC recommendation growing-stock line chart.

Likely manual or mixed extraction targets:

- `Figure 6`, `Figure 45`: multi-panel age-class histograms.
- `Figure 16` through `Figure 19` and `Figure 53` through `Figure 56`:
  multi-series old-seral proportion charts by landscape unit.
- `Figure 20` and `Figure 57`: waterfall/impact bar charts.
- `Figure 21` and `Figure 22`: table plus line-chart hybrids.

## Status

- Current status: `crop_proposals_generated`
- Downstream use classification: `not_yet_accepted`
- Next action: manually review and tighten the proposed bboxes, then create
  reviewed calibration specs for the first line-chart extraction batch.
