# TFL 6 TSR and THLB Recipe Extraction Plan

## Purpose

This note queues the follow-on planning lane for translating the TFL 6
Management Plan 10 timber supply assumptions into FEMIC-style reviewed
source-layer and THLB netdown recipe surfaces.

Governing issue: `#7`.

## Source Documents

Primary source documents:

- TFL 6 Management Plan 10:
  `https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-tenures/tree-farm-licence/management-plans/tfl_6_mngment_plan_10_2011.pdf`
- TFL 6 Management Plan 10 Information Package:
  `https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-tenures/tree-farm-licence/management-plans/tfl_6_mngment_plan_2011_ip.pdf`

Local reference already added:

- `data/source/nicf_fsp/reference/tfl_6_management_plan_10_information_package_2011.pdf`

Indexed local reference corpus:

- corpus index: `reference/tfl6_reference_index.json`
- corpus summary: `reference/tfl6_reference_index.md`
- extracted searchable text: `reference/extracted_text/`

The local corpus index covers 18 locally copied TFL 6 reference files from the
Province of British Columbia TFL 6 page: 17 PDFs and one PNG. Document families
include the Chief Forester AAC rationale, licence maps, an instrument, annual
reports, Management Plan 9 and appendices, Management Plan 10, the Management
Plan 10 timber supply analysis report, and the Management Plan 10 information
package.

Each indexed document records repo-relative path, bytes, SHA-256, source page,
page count or image dimensions, extracted-text path where applicable,
document-family classification, candidate dates/titles, keyword counts, content
flags, and page-level text excerpts. This satisfies the P1.7a local source-copy
and verification prerequisite for later reviewed source-layer and THLB
extraction work.

## FEMIC Workflow Pattern

The closest existing pattern is the TSA29 TSR workflow:

- canonical discovery/fact extraction;
- reviewed instance-local overlay;
- reviewed source-layer recipe;
- reviewed THLB netdown recipe;
- optional workbench and locked/reconstructed execution surfaces.

Relevant command/document surfaces in FEMIC:

- `femic tsr recipe-init`
- `femic tsr source-layers-build`
- `femic tsr source-layers-run`
- `femic tsr thlb-netdown-build`
- `femic tsr thlb-netdown-workbench-build`
- `femic tsr thlb-netdown-workbench-lock`
- `femic tsr thlb-netdown-run`
- `docs/guides/tsr-intelligence-workflow.rst`
- `docs/reference/cli.rst`
- `docs/reference/api/femic-tsr-catalog.rst`

Important gap:

- The current built-in TSR discovery/fetch/fact workflow is TSA-oriented.
  TFL 6 recipe work should not pretend it is a TSA workflow. The first recipe
  planning pass must explicitly identify what can be reused and what needs a
  TFL/general-FMU adaptation.

## Planned Review Outputs

Use planning tables first, then promote reviewed decisions into recipe YAML only
after the source assumptions are accepted.

Planned planning outputs:

- `planning/tfl6_2011_document_review.md`
- `planning/tfl6_thlb_netdown_steps.md`
- `planning/tfl6_source_layer_candidates.md`

Possible later recipe/config outputs:

- `config/tsr/source_layers.recipe.yaml` or a TFL/general-FMU successor path
- `config/tsr/thlb_netdown.recipe.yaml` or a TFL/general-FMU successor path
- `config/tsr/overlay.yaml` only if the current overlay schema is generalized
  beyond TSA identity assumptions

## Extraction Questions

The `#7` review should answer:

- Which tables/sections in the 2011 information package define the gross land
  base, productive forest, operable area, THLB exclusions, and residual THLB?
- Which assumptions are spatial source-layer deductions versus aspatial/model
  assumptions?
- Which public BCDC layers can support each spatial deduction?
- Which deductions require local source data, management-plan assumptions, or
  reviewed aspatial treatment because no public layer is available?
- Which yield/source assumptions affect VDYP/TIPSY inputs but are not THLB
  netdown steps?
- What execution stage each THLB step belongs to:
  - source acquisition;
  - initial land-base classification;
  - exact spatial overlay;
  - checkpoint-attribute exclusion;
  - aspatial benchmark deduction; or
  - review-only/manual note.

## Dependency

`#6` accepted the active TFL 6 input-layer dependency in `P1.6d`:

- TFL 6 AOI boundary;
- clipped 2025 R1 polygon input;
- filtered 2025 VDYP7 polygon table;
- filtered 2025 VDYP7 layer table; and
- input-layer manifest.

Accepted input manifest:
`data/input/tfl_6/input_layers_manifest.json`

Reviewed source-layer and THLB netdown recipe planning can now start under
`#7`. Recipe execution remains out of scope until reviewed assumptions and
recipe surfaces exist.

## P1.7b Review Snapshot

The first reviewed document-mining pass is recorded in
`planning/tfl6_2011_document_review.md`.

That note anchors the first extraction pass to the 2011 information package,
management plan, analysis report, and Chief Forester AAC rationale. The
information package is the primary source for source-layer and THLB planning:
Section 6 / Tables 4-17 define the land-base netdown sequence, Section 8 /
Tables 23-29 define yield assumptions, and Section 10 / Tables 31-35 define
visual, old-seral, steep-terrain, minimum-harvest, and initial-harvest
modelling assumptions.

P1.7c and P1.7d should now split the documented candidates into reusable TSA29
workflow patterns, TFL/general-FMU adaptation gaps, and non-executable recipe
skeletons.

## THLB Netdown Backbone

The ordered TFL 6 THLB netdown backbone is now recorded in
`planning/tfl6_thlb_netdown_steps.md`.

That note preserves the literal MP10 Table 4 order and adds a tentative FEMIC
stage mapping onto `GLB -> AFLB`, `AFLB -> LHLB`, and `LHLB -> THLB`. The stage
labels are review metadata, not source wording, because the TFL 6 information
package uses `Total Landbase`, `Total Productive`, `Total Operable`,
`Current THLB`, and `Long-term Landbase` rather than the TSA29 ladder names.

## Non-Goals

- Do not auto-adopt extracted candidate facts as model truth.
- Do not run THLB netdown before source layers and reviewed assumptions exist.
- Do not start Patchworks runtime-package compilation in this planning lane.
