# TFL 6 MP11 Figrecover Deployment Feedback

## Purpose

This note records package-development feedback from the Phase 7 TFL 6 MP11
figure-extraction deployment test. It is intended to feed concrete requirements
back into the upstream `figrecover` development pipeline.

This is a public-safe planning note. It does not include rendered pages, figure
crops, overlays, raw runtime tables, private prompt logs, or any generated
artifacts from ignored runtime paths.

## Source Context

- FEMIC instance branch: `feature/p7-mp11-figure-extraction-test`
- Source document: TFL 6 Management Plan 11 PDF
- Source SHA256:
  `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- Figure inventory: `planning/tfl6_mp11_full_figure_inventory.csv`
- High-priority crop queue:
  `planning/tfl6_mp11_priority_figure_crop_queue.csv`
- Crop proposal summary:
  `planning/tfl6_mp11_priority_crop_proposals.md`

## Current Deployment Yield

The deployment has produced reviewed evidence from multiple chart families.
All reviewed rows remain explicitly `not_model_input`.

Accepted for comparison:

- harvest-sensitivity line charts: Figures `29`, `30`, `31`, `35`, `36`,
  and `39`;
- growing-stock multi-series line charts: Figures `3` and `40`; and
- impact/waterfall charts: Figures `20` and `57`.

Reviewed for planning only:

- cedar inventory stacked-area charts: Figures `14`, `15`, `51`, and `52`;
- age-class stacked bar charts: Figures `6` and `45`; and
- old-seral landscape-unit multi-series line charts: Figures `16`, `17`,
  `18`, `19`, `53`, `54`, `55`, and `56`.

This means the current reviewed figure evidence surface is:

- `10` figures accepted for comparison;
- `14` figures reviewed for planning only; and
- `0` figures accepted as model inputs.

## What Worked Well

### Deterministic line extraction with table cross-checks

The harvest-sensitivity batch was the strongest workflow. The figures had
simple flat line series and adjacent MP11 table values. The extraction could be
reviewed by comparing recovered mean values to source table values, with a
maximum absolute percent error of approximately `0.503%`.

Package implication:

- `figrecover` should treat adjacent-table cross-checks as a first-class QA
  pattern rather than a custom downstream script.

### Internal component-sum checks

The growing-stock charts were accepted for comparison using internal
component-sum consistency:

```text
THLB GS <= 120 years + THLB GS > 120 years ~= THLB GS total
```

Package implication:

- `figrecover` should support declared series relationships and residual
  checks in extraction/review manifests.

### Printed-label plus geometry checks

The impact/waterfall charts were accepted for comparison because printed chart
labels were visible, waterfall arithmetic residuals were zero, and deterministic
bar geometry confirmed the labelled components within a bounded tolerance.

Package implication:

- `figrecover` should support a chart-label extraction/review mode where
  printed labels are treated as the primary numeric source and bar geometry is
  used as an independent QA check.

### Overlay review as a decisive QA surface

Every promotion decision depended on runtime overlays, not only numeric
summary tables. Overlay inspection caught several real problems:

- cedar stacked-area boundary confusion between total and THLB bands;
- age-class panel-border and legend-swath contamination;
- old-seral tan-series contamination from gray gridlines; and
- multi-figure crop offsets on pages containing two chart panels.

Package implication:

- overlay rendering and contact sheets should remain core workflow outputs,
  not optional debug artifacts.

## Main Friction Points

### Crop proposals are useful but not accepted plot crops

The first crop proposal pass was useful for quickly creating reviewable
high-priority crops, but many crops included captions, neighbouring text, or
multiple figures on the same page. The extractor scripts still needed manual
panel-specific plot bounds.

Needed `figrecover` improvement:

- separate `figure_crop_bbox` from `plot_panel_bbox`;
- support multiple plot panels within one figure crop;
- track crop proposal status separately from reviewed plot-calibration status;
- generate plot-panel review sheets with axis/frame candidates overlaid.

### Calibration remains too manual

Most extraction scripts used hard-coded plot bounds, axis bounds, and special
case bands. This is acceptable for a prototype deployment, but it is not yet a
good user-facing package workflow.

Needed `figrecover` improvement:

- add a calibration specification record that can be stored, reviewed, reused,
  and edited independently from extraction code;
- support linear axis calibration from plot bounds plus visible tick labels;
- expose calibration proposal diagnostics, including axis-frame confidence;
- allow user-supplied calibration YAML/JSON for corpus runs.

### Chart-family-specific extractors are missing

The deployment needed bespoke scripts for each family:

- flat harvest-level lines;
- multi-series line charts with component-sum checks;
- stacked-area boundary extraction;
- fixed-slot stacked bars;
- printed-label waterfall charts; and
- old-seral multi-series line charts with target-line avoidance.

Needed `figrecover` improvement:

- provide reusable extractor classes for these families;
- expose explicit extraction strategies such as `top_edge_of_fill`,
  `median_line`, `component_series_sum`, `stacked_area_boundary`,
  `fixed_slot_stacked_bar`, and `waterfall_label_geometry`;
- keep family-specific assumptions in data records, not hidden in ad hoc
  scripts.

### Review-status vocabulary is essential

The distinction between `raw_extraction`, `reviewed_for_planning`,
`accepted_for_comparison`, and `accepted_for_model_input` prevented premature
use of weak evidence.

Needed `figrecover` improvement:

- formalize review statuses in public records;
- require downstream-use and model-input status fields in review manifests;
- make CLI summary commands report status counts by default.

### Validation strength must be explicit

Different chart families had very different validation strength:

- adjacent table cross-check: strongest;
- printed labels plus geometry: strong;
- component-sum identity: moderate;
- overlay plus nonnegative sanity check: planning only;
- overlay plus series coverage only: planning only.

Needed `figrecover` improvement:

- record `validation_strength` and `review_basis` in standardized fields;
- support structured QA checks such as adjacent table comparison, arithmetic
  residual, component-sum residual, nonnegative residual, and point-density
  thresholds;
- prevent a high point count from being mistaken for strong validation.

### Runtime artifact policy should be built into the package

The deployment repeatedly separated compact tracked summaries from ignored
runtime artifacts. This worked, but it depended on manual discipline.

Needed `figrecover` improvement:

- standardize artifact layout for pages, crops, overlays, tables, manifests,
  logs, and review bundles;
- provide a `public-safe-summary` export mode;
- ensure generated artifacts can be ignored by default while compact summaries
  are stable enough to track.

## Proposed Upstream Figrecover Backlog

### F1: Calibration and panel specification records

Add durable records for:

- source figure crop;
- plot panel bbox;
- x/y axis type and range;
- tick-label evidence;
- calibration reviewer;
- calibration status; and
- calibration diagnostics.

Priority: high.

Reason: every real extraction batch depended on manual calibration, and the
calibration needs to become reviewable data rather than script constants.

### F2: Table/label cross-check QA

Add QA helpers for:

- comparing recovered series means or endpoint values to adjacent tables;
- transcribing printed chart labels into review records;
- checking waterfall arithmetic residuals; and
- recording tolerance thresholds.

Priority: high.

Reason: the strongest accepted evidence came from explicit source-table or
printed-label checks.

### F3: Reusable chart-family extractors

Promote successful deployment patterns into reusable extractors:

- flat/step line charts;
- filled-area top-edge charts;
- multi-series line charts;
- stacked-area boundary charts;
- fixed-slot stacked bar charts;
- waterfall/bridge charts; and
- small-multiple/panelled charts.

Priority: high.

Reason: the current deployment used repeatable logic, but it lives in
instance-specific scripts.

### F4: Review manifest schema and CLI

Formalize:

- review status;
- downstream use;
- model-input status;
- validation strength;
- review basis;
- reviewer;
- reviewed timestamp;
- artifact references; and
- summary status counts.

Priority: high.

Reason: this prevented over-trust and made Phase 6 handoffs auditable.

### F5: Overlay contact sheets and low-friction visual QA

Add package-level helpers for:

- per-figure overlays;
- per-batch contact sheets;
- sampled-point colour legends;
- calibration frame overlays; and
- warning annotations.

Priority: medium-high.

Reason: visual QA caught errors that numeric summaries did not.

### F6: Corpus-run case-study summarizer

Add an exporter that summarizes a deployment run by:

- figure count;
- chart family;
- extraction status;
- review status;
- validation strength;
- downstream use;
- accepted/rejected counts; and
- unsupported reasons.

Priority: medium.

Reason: this is needed for Sphinx case-study docs, JOSS results, and large
technical-document workflows.

### F7: Public-safe artifact hygiene

Add command-line affordances for:

- writing detailed artifacts under ignored runtime roots;
- writing compact tracked summaries under planning/docs roots;
- checking for accidental raw PDF/page/crop/overlay/table tracking; and
- generating publication-safe case-study summaries.

Priority: medium.

Reason: the package should encode the hygiene pattern used manually in this
deployment.

## Concrete Test Fixtures To Add Upstream

The TFL6 run suggests synthetic fixtures for:

- a flat filled harvest-level chart with an adjacent expected value;
- a three-series growing-stock chart with component-sum identity;
- a stacked-area chart with total/THLB boundary separation;
- a fixed-slot stacked age-class chart with known panel totals;
- a waterfall chart with printed labels and known arithmetic residual;
- a two-panel page crop where each panel needs separate plot bounds;
- a multi-series line chart with target/dashed lines that should not be
  treated as actual series; and
- a chart where gridline colour is close to one series colour.

## Suggested Figrecover Issue Mapping

This feedback should inform the next `figrecover` development planning cycle,
especially:

- Phase 5 QA/review improvements;
- Phase 6 corpus pipeline refinements;
- Phase 7 FEMIC integration hardening;
- Phase 8 documentation/case-study examples; and
- Phase 9 v1.0.0 readiness and JOSS case-study results.

For the current public-alpha branch, the most actionable next issue is a
post-alpha/v1 readiness issue titled:

```text
Incorporate TFL6 MP11 deployment feedback into figrecover v1 roadmap
```

Minimum acceptance for that issue:

- this note is linked from `figrecover`;
- backlog items F1-F7 are triaged into concrete package issues;
- at least one synthetic fixture is created for each successful deployment
  chart family; and
- package docs explain review status, validation strength, and public-safe
  artifact handling using the TFL6 deployment as the motivating case.
