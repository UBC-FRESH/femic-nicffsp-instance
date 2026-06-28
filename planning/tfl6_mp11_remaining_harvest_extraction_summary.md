# TFL 6 MP11 Remaining Harvest Scenario Extraction Summary

## Purpose

This note records the raw extraction batch for high-priority MP11
harvest/scenario line charts that were not part of the first accepted
harvest-sensitivity tranche.

The batch extracts plotted lines and records endpoint checks against
visible table or narrative values where those values are unambiguous.
It remains raw until P7.5 overlay and value review.

## Outputs

- `planning/tfl6_mp11_remaining_harvest_extraction_summary.csv`
- `planning/tfl6_mp11_remaining_harvest_extraction_summary.json`
- `planning/tfl6_mp11_remaining_harvest_series_summary.csv`
- `planning/tfl6_mp11_remaining_harvest_points.csv`

Ignored runtime detail files are under:

```text
runtime/document_ingestion/tfl6-mp11-full-figures/recovered/remaining_harvest_batch/
runtime/document_ingestion/tfl6-mp11-full-figures/overlays/remaining_harvest_batch/
```

## Current Status

- Figures extracted: `11`
- Series extracted: `23`
- Recovered points: `4497`
- Review status: `raw_extraction`
- Downstream use: `needs_p7_5_review`
- Model-input status: not accepted for model input
- Maximum endpoint absolute percent error: `0.29%`

## Endpoint Snapshot

- `Figure 21` `MP11 Base Case` endpoint `1,064,680`; expected `1,061,600`; absolute error `0.29%`
- `Figure 21` `Maintaining Current AAC` endpoint `1,053,863`; expected `1,055,200`; absolute error `0.13%`
- `Figure 22` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 22` `Maximum short-term` endpoint `1,095,585`; expected `1,095,500`; absolute error `0.01%`
- `Figure 23` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 23` `Increased Natural Stand Yields` endpoint `1,075,497`; expected `1,075,300`; absolute error `0.02%`
- `Figure 24` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 24` `Decreased Natural Stand Yields` endpoint `1,035,320`; expected `1,036,600`; absolute error `0.12%`
- `Figure 25` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 25` `Increased Managed Stand Yields` endpoint `1,140,397`; expected `1,138,800`; absolute error `0.14%`
- `Figure 26` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 26` `Decreased Managed Stand Yields` endpoint `971,965`; expected `970,900`; absolute error `0.11%`
- `Figure 32` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 32` `Adjusted ITI and LiDAR reduced OAF1 even flow` endpoint `1,149,669`; expected `1,150,300`; absolute error `0.05%`
- `Figure 32` `Adjusted ITI and LiDAR reduced OAF1 max short-term` endpoint `1,165,121`; expected `1,164,200`; absolute error `0.08%`
- `Figure 33` `MP11 Base Case` endpoint `1,061,290`; expected `1,061,600`; absolute error `0.03%`
- `Figure 33` `No Genetic Gain` endpoint `1,006,452`; expected `1,004,000`; absolute error `0.24%`
- `Figure 34` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 34` `Full NSOG Order Targets` endpoint `1,049,227`; expected `1,049,400`; absolute error `0.02%`
- `Figure 37` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 37` `Helicopter Operable Land Base Excluded` endpoint `1,022,958`; expected `1,021,900`; absolute error `0.10%`
- `Figure 38` `MP11 Base Case` endpoint `1,063,135`; expected `1,061,600`; absolute error `0.14%`
- `Figure 38` `10% THLB Increases` endpoint `1,118,764`; expected `1,118,200`; absolute error `0.05%`

## Next Step

P7.5 should inspect overlays and endpoint residuals. Simple flat-line
figures with clean endpoint checks may be eligible for
`accepted_for_comparison`; stepped and multi-flow figures may need
planning-only handling unless the table rows are reviewed in more detail.
