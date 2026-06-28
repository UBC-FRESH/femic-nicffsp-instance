# TFL 6 MP11 Figure Extraction Phase 7 Closeout

## Purpose

This note closes the bounded Phase 7 `figrecover` deployment test against
the public TFL 6 Management Plan 11 PDF. It joins the full 61-row figure
inventory to every reviewed extraction manifest and records what is ready
for Phase 6 comparison planning, what remains planning-only, and what was
deferred.

## Source And Inventory

- Source: public TFL 6 Management Plan 11 PDF
- Source SHA256:
  `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`
- Inventory: `planning/tfl6_mp11_full_figure_inventory.csv`
- Inventory rows: `61`
- Priority counts: `{'excluded_context': 5, 'high': 36, 'medium': 20}`

## Closeout Files

- `planning/tfl6_mp11_figure_extraction_closeout.md`
- `planning/tfl6_mp11_figure_extraction_closeout.csv`
- `planning/tfl6_mp11_figure_extraction_closeout.json`

## Reviewed Evidence Surface

- Accepted for Phase 6 comparison planning: `22` figures
- Reviewed for planning only: `14` figures
- Deferred after inventory/crop triage: `20` figures
- Inventory context only: `5` figures
- Model-input status counts: `{'not_model_input': 61}`

Accepted comparison figures:

- Figures `2, 3, 20, 21, 22, 23, 24, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 57`

Planning-only reviewed figures:

- Figures `6, 14, 15, 16, 17, 18, 19, 45, 51, 52, 53, 54, 55, 56`

Deferred figures:

- Figures `4, 5, 7, 8, 9, 10, 11, 12, 13, 27, 28, 41, 42, 43, 44, 46, 47, 48, 49, 50`

Context-only figures:

- Figures `1, 58, 59, 60, 61`

## Interpretation

Phase 7 completed the high-priority test target: all `36` high-priority
figures now have explicit reviewed status. Of those, `22` are accepted
for comparison planning and `14` are planning-only. No recovered figure
table is accepted as model input.

The `20` deferred figures are medium-priority stacked, grouped, mixed, or
method-explanation charts. They are useful future stress tests for
`figrecover`, but they are not required before Phase 6 can use the
reviewed comparison evidence to plan the MP10-to-MP11 model-overhaul
work.

## Phase 6 Handoff

Use comparison-accepted figures only for narrative and quantitative
comparison planning in Phase 6. Treat planning-only figures as qualitative
or approximate context unless a later task supplies stronger independent
validation. Do not copy recovered rows into model-input bundles without a
new maintainer review and explicit promotion to `accepted_for_model_input`.

Primary Phase 6 consumers:

- `#44`: MP11 extraction inventory and metadata;
- `#46`: inventory, yield, operability, and harvest-system assumptions;
- `#47`: model behavior, sensitivities, AAC, and KPI comparison; and
- `#48`: MP11-aligned implementation roadmap.

## Validation

Final closeout validation should confirm:

- reviewed manifests remain JSON/CSV readable;
- runtime pages, crops, overlays, raw result JSON, and recovered point CSV
  files remain ignored;
- docs build if the Phase 7 Sphinx page is updated; and
- GitHub issues and roadmap checkboxes match this closeout state.
