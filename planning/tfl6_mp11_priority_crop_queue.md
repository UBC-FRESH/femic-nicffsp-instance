# TFL 6 MP11 Priority Figure Crop Queue

## Purpose

This note records the first P7.3 crop/classification queue for the full MP11
figure-extraction test.

The queue is intentionally conservative. It creates preliminary full-content
crops for high-priority figures under ignored runtime paths, but it does not
claim that plot-area crop boxes or axis calibrations are accepted.

## Tracked Queue

- `planning/tfl6_mp11_priority_figure_crop_queue.csv`

The queue contains `36` high-priority figures from
`planning/tfl6_mp11_full_figure_inventory.csv`.

Each row records:

- corpus ID;
- figure ID;
- PDF page;
- caption;
- chart family;
- extraction priority;
- ignored runtime candidate manifest path;
- ignored runtime preliminary crop directory;
- crop-review status; and
- calibration status.

## Ignored Runtime Artifacts

Generated artifacts are under:

```text
runtime/document_ingestion/tfl6-mp11-full-figures/
  figure_candidates_priority_high.jsonl
  crops/priority_high_preliminary/
  crops/priority_high_preliminary_summary.json
```

These files remain ignored. They are useful for manual visual review and later
calibration work, but they are not accepted evidence.

## Current Status

- Candidate count:
  `36`
- Preliminary crop count:
  `36`
- Crop status:
  `needs_manual_crop_review`
- Calibration status:
  `not_started`

## Next Step

P7.3 remains open. The next bounded step is to inspect the preliminary crops,
replace full-content crop boxes with figure-specific plot-area crops for the
first extraction batch, and create calibration specs for the high-priority
line/bar charts selected for P7.4.
