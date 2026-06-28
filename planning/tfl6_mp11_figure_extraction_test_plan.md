# TFL 6 MP11 Figure Extraction Test Plan

## Purpose

Phase 7 runs a full, auditable figure-extraction test on the public TFL 6
Management Plan 11 PDF package before any MP10-to-MP11 model-upgrade work
starts.

The test uses `figrecover` and FEMIC provenance/review gates to decide which
published MP11 figures can produce useful approximate tables, which figures
should remain qualitative context, and which outputs are strong enough for
later comparison or model-upgrade planning.

## Source Package

- Source URL:
  `https://www.westernforest.com/wp-content/uploads/2026/06/TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf`
- Local working copy convention:
  keep a source copy under ignored runtime or download/cache space and verify it
  against the public URL and SHA256 before extraction.
- SHA256:
  `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- PyMuPDF page count:
  `475`

Portable handoff should use the public URL, checksum, and ignored runtime
source-copy convention rather than machine-specific local paths.

## Initial Inventory

The first tracked inventory is:

- `planning/tfl6_mp11_full_figure_inventory.csv`

It contains the `61` figures listed in Appendix A's list of figures, with:

- corpus ID;
- source URL and SHA256;
- report component;
- report page and calculated PDF page;
- figure ID;
- caption;
- chart-family triage;
- extraction-priority tier;
- initial review status;
- downstream relevance; and
- Phase 6 alignment.

The first inventory is a triage surface. It does not contain crops,
calibrations, recovered values, overlays, or accepted model evidence.

## Corpus Preparation

The compact P7.2 runtime-corpus summary is:

- `planning/tfl6_mp11_figrecover_corpus_summary.md`
- `planning/tfl6_mp11_figrecover_corpus_summary.json`

The ignored runtime corpus is:

- `runtime/document_ingestion/tfl6-mp11-full-figures/`

It renders the `58` unique PDF pages referenced by the `61` figure inventory
rows at `150` DPI with `figrecover 0.1.0a1` and PyMuPDF `1.27.2.3`.

## Priority Crop Queue

The compact P7.3 priority crop queue is:

- `planning/tfl6_mp11_priority_crop_queue.md`
- `planning/tfl6_mp11_priority_figure_crop_queue.csv`

It creates ignored preliminary full-content crops for the `36` high-priority
figures. These crops are marked `needs_manual_crop_review`, and calibration is
explicitly `not_started`. They are a review queue, not accepted plot-area crops
or recovered data.

## Runtime Artifact Boundary

Generated figure-recovery artifacts belong under ignored runtime paths such as:

```text
runtime/document_ingestion/tfl6-mp11-full-figures/
  source_manifest.yaml
  pages/
  figure_candidates.csv
  crops/
  calibration/
  recovered/
  overlays/
  review_manifest.jsonl
  accepted/
```

These generated artifacts should not be committed unless explicitly sanitized
and approved. Tracked planning files should remain compact and public-safe.

## Review Status Contract

Recovered values must remain separate from accepted model evidence. The
expected status vocabulary mirrors the FEMIC `figrecover` integration:

- `raw_extraction`;
- `needs_calibration_review`;
- `needs_value_review`;
- `reviewed_for_planning`;
- `accepted_for_comparison`;
- `accepted_for_model_input`;
- `rejected`; and
- `superseded`.

Accepted statuses require reviewer and timestamp provenance. No raw recovered
table should enter MP11 model-upgrade work without review status, extraction
method, calibration, checksums, and downstream-use classification.

## Phase 6 Handoff

Phase 7 is linked to the existing MP11 ingestion issue tree:

- `#42`: Phase 6 MP11 ingestion parent;
- `#43`: MP11 source package and extraction manifest;
- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;
- `#45`: land base and THLB comparison;
- `#46`: inventory, yield, operability, and harvest-system assumptions; and
- `#47`: model behavior, sensitivity, AAC recommendation, and KPI comparison.

The figure-extraction test should hand off reviewed comparison-ready evidence
to the relevant Phase 6 comparison lanes. It should not itself rebuild the
model or change accepted model inputs.

## First Extraction Priorities

High-priority classes in the initial inventory include:

- harvest-flow line charts;
- THLB/growing-stock time-series charts;
- age-class distribution charts;
- cedar and old-seral indicator charts;
- timber-supply impact summaries; and
- AAC recommendation/scenario comparison charts.

Context figures such as overview maps, orthophotos, LiDAR images, gap diagrams,
and inventory-polygon examples are retained in the inventory but marked as
non-digitization targets unless a later task needs them for qualitative
documentation.

## Validation Expectations

Before Phase 7 closes:

- run `figrecover` and FEMIC optional-dependency preflights;
- validate inventory and review manifests for required fields;
- inspect overlays for any accepted/comparison-ready recovered tables;
- confirm generated runtime artifacts remain ignored;
- update Phase 6 handoff issues with reviewed outputs; and
- document limitations and next model-upgrade entry conditions.
