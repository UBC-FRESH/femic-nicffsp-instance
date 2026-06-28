# TFL 6 MP11 Ingestion And Model-Overhaul Planning

## Purpose

Phase 6 opens the planning lane for ingesting Western Forest Products' June
2026 TFL 6 Management Plan 11 package and comparing its public timber-supply
evidence against the completed Phase 5 FEMIC/Patchworks teaching prototype.

The current Phase 5 package remains the baseline prototype. It was built from
the public MP10-era planning record, 2025 public inventory inputs, reviewed
TFL 6 source-layer/THLB contracts, and the first teaching Patchworks runtime
release. Phase 6 does not retroactively invalidate that package. It creates the
reviewed evidence base needed before a future MP11-aligned overhaul can begin.

## Source Package

- Source URL:
  `https://www.westernforest.com/wp-content/uploads/2026/06/TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf`
- Public-release context: June 2026 WFP TFL 6 Management Plan 11 package.
- Source-access smoke on 2026-06-27: the public PDF responded as an
  `application/pdf` and reported 475 pages. P6.1 still needs the local
  source/provenance manifest, checksum, and extraction-readiness record.
- P6.1 source/provenance manifest:
  `planning/tfl6_mp11_source_package_manifest.md`
- Machine-readable source/provenance record:
  `planning/tfl6_mp11_source_package_manifest.json`
- Document-component table:
  `planning/tfl6_mp11_document_components.csv`
- Extraction-manifest field contract:
  `planning/tfl6_mp11_extraction_manifest_fields.csv`
- Verified source facts on 2026-06-28:
  - page count: `475`;
  - byte size: `9147004`;
  - SHA256:
    `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`;
  - checksum status: `passed`;
  - PDF producer: `Pdftools SDK`; and
  - PyMuPDF inspection version: `1.27.2.3`.
- Expected document layers, to be verified in the P6.1/P6.2 extraction
  manifest:
  - Management Plan front matter;
  - Appendix A: Timber Supply Analysis report; and
  - Appendix B: Information Package.
- Governance caveat: treat the package as a public planning and AAC-analysis
  source. Do not describe its AAC analysis as a final Chief Forester AAC
  determination unless a separate approved decision is located and reviewed.

## Issue Tree

- Parent: `#42` Phase 6: ingest MP11 and plan TFL6 model overhaul.
- `#43` P6.1: archive MP11 source package and extraction manifest.
- `#44` P6.2: extract MP11 tables, figures, sections, assumptions, and
  metadata.
- `#45` P6.3: compare MP11 land base and THLB assumptions against the Phase 5
  prototype.
- `#46` P6.4: compare MP11 inventory, LiDAR/ITI, yield, operability, and
  harvest-system assumptions.
- `#47` P6.5: compare MP11 model behavior, sensitivities, AAC recommendation,
  and KPI outputs.
- `#48` P6.6: write the Phase 7+ implementation roadmap for the MP11-aligned
  model overhaul.

## Extraction Scope

The extraction inventory must cover the full PDF package, not only the headline
AAC discussion. Every extracted claim must carry enough provenance to be
auditable later:

- document layer;
- section heading;
- page anchor;
- table or figure number where available;
- extracted text or normalized structured value;
- extraction method;
- manual-review status;
- comparison target in the Phase 5 prototype, if applicable; and
- adoption status: raw extraction, reviewed evidence, accepted model contract,
  rejected/deferred, or unresolved.

The first P6.2 raw extraction inventory is:

- `planning/tfl6_mp11_extraction_inventory.csv`
- `planning/tfl6_mp11_extraction_inventory_summary.json`
- `planning/tfl6_mp11_extraction_inventory_summary.md`

It contains `1870` raw candidate rows:

- `245` heading candidates;
- `287` table candidates;
- `244` figure candidates; and
- `1094` high-priority claim candidates.

The rows are intentionally conservative: `review_status` is `raw_extraction`,
downstream use is `phase6_inventory_triage_only`, and `model_input_status` is
`not_model_input`. Table-of-contents/list entries and repeated references may
appear in this queue; those are expected to be filtered during the next
P6.2/P6.3-P6.5 review and crosswalk passes.

At minimum, P6.2 should inventory:

- section headings and appendices;
- tables, figures, maps, references, and footnotes;
- land-base and THLB assumptions;
- source-layer descriptions;
- inventory, LiDAR, and individual-tree-inventory inputs;
- operability, economic operability, terrain, karst, roads, riparian,
  OGMA/WHA, retention, and biodiversity assumptions;
- analysis-unit definitions;
- natural and managed yield assumptions;
- OAF, utilization, non-recoverable loss, and silvicultural-system rules;
- forest-cover constraints, minimum harvest age, harvest scheduling rules, and
  harvest-flow objectives;
- base-case outputs, alternate harvest flows, sensitivity analyses, and AAC
  recommendation evidence; and
- cedar, old-cedar, species-composition, age-class, volume-class,
  elevation-band, harvest-system, and other reported KPI outputs.

## Initial Review Targets

The following items are high-priority targets for extraction and crosswalk.
They are not accepted model facts until P6.2/P6.3 records page anchors and
review status:

- total TFL area;
- productive forest area;
- timber harvesting land base;
- non-contributing land base;
- changed land-base netdown categories relative to the MP10-derived prototype;
- VRI/LiDAR/ITI input vintage and usage;
- analysis-unit and growth-and-yield changes;
- base-case harvest flow and AAC recommendation;
- sensitivity-analysis structure and reported effects; and
- cedar, old-cedar, harvest-system, elevation-band, and species-composition
  outputs that can be compared with or added to the Patchworks teaching
  reporting surface.

## Phase 5 Baseline Surfaces

Phase 6 comparisons should start from the accepted Phase 5 surfaces, including:

- `planning/tfl6_thlb_benchmark_tolerance.md`;
- `planning/tfl6_source_layer_recipe_contracts.md`;
- `planning/tfl6_au_yield_curve_contract.md`;
- `planning/tfl6_cedar_signal_design.md`;
- `planning/tfl6_nicf_embedded_identity.md`;
- `planning/tfl6_model_input_bundle_qa.md`;
- `planning/tfl6_runtime_package_p44.md`;
- `planning/tfl6_runtime_release_archive_manifest.md`;
- `planning/tfl6_phase5_release_qa.md`;
- `docs/phase5-runtime-release.rst`;
- `docs/phase5-rebuild-provenance.rst`; and
- the accepted Phase 5 release archive and manifest.

## Non-Goals

Phase 6 must not perform model overhaul implementation. Specifically, do not:

- rerun THLB;
- regenerate VDYP or TIPSY yield curves;
- rewrite model-input bundle contracts;
- regenerate ForestModel XML;
- run Matrix Builder;
- rebuild or republish the Patchworks runtime archive;
- claim equivalence to WFP's unpublished forest estate model; or
- replace the Phase 5 teaching release before reviewed MP11 deltas have been
  extracted, crosswalked, and scoped into Phase 7+ implementation work.

## Expected Phase 6 Output

The phase should end with:

- a source/provenance manifest for the MP11 package;
- structured extraction artifacts with page anchors and review status;
- a land-base/THLB crosswalk against the Phase 5 prototype;
- an inventory/yield/operability/harvest-system assumption crosswalk;
- a model-behavior, sensitivity, AAC, and KPI comparison memo; and
- a Phase 7+ roadmap with parent/child issue structure for any accepted
  MP11-aligned implementation overhaul.
