# Change Log

## 2026-06-23 - Bootstrapped the NICF FSP FRST 558 instance repository

- created the FEMIC instance scaffold for `femic-nicffsp-instance`;
- added modelwright-style workflow surfaces (`AGENTS.md`, `ROADMAP.md`,
  `CHANGE_LOG.md`, and `planning/`);
- tracked the initial NICF FSP AOI, LU, and FSP source payloads under lowercase
  repo-relative paths; and
- recorded the first build-plan boundary: source inspection and K3Z-template
  adaptation must happen before any Patchworks runtime success is claimed.

## 2026-06-23 - Split Phase 1 into task-wise GitHub issues

- narrowed `#1` to `P1.2` source-payload inspection and normalization;
- opened `#3` for the `P1.3` K3Z-to-NICF adaptation contract;
- opened `#2` for the `P1.4` cedar, expansion, and runtime-package follow-on
  issue split; and
- updated the roadmap so the active edge stays on `P1.2` source normalization
  before model design or compilation work starts.

## 2026-06-23 - Added the Phase 1 parent issue

- opened parent phase issue `#4` for Phase 1;
- linked child task issues `#1`, `#3`, and `#2` from the parent issue body;
- added child-issue backlinks to `#4`; and
- updated the roadmap so Phase 1 follows the modelwright parent/child issue
  workflow.

## 2026-06-23 - Hardened the agent issue-workflow contract

- amended `AGENTS.md` so future roadmap phase expansions must use one GitHub
  parent issue per phase and one linked child issue per phase task;
- documented the child backlink, issue-body checklist, closure, and PR/merge
  rules; and
- recorded that parallel phase lanes require explicit maintainer approval.

## 2026-06-23 - Inspected the NICF FSP amendment spatial payload

- inventoried `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip`;
- found one shapefile family, `NICF_FDU_2024`, with six valid EPSG:3005 polygon
  features labeled as FDU/LU records;
- recorded feature labels, CRS, bounds, geometry validity, and measured areas in
  `planning/source_inventory.md`; and
- kept the runtime AOI boundary undecided pending cross-check against the FSP
  document and separate LU boundary payload.

## 2026-06-23 - Inspected the BCGW landscape-unit clip payload

- inventoried `data/source/nicf_fsp/bcgw_lu_clip_2026_06.zip`;
- found one BCGW `RMP_LU_SVW_polygon` shapefile family with `27` valid EPSG:3005
  landscape-unit polygons;
- recorded LU names, CRS, bounds, validity, measured areas, and overlap with
  the `NICF_FDU_2024` AOI candidate in `planning/source_inventory.md`; and
- kept the relevant-LU decision open because the inspected spatial payloads show
  six FDU/LU overlaps, while the project note expected three relevant LUs.

## 2026-06-23 - Cross-checked the FSP PDF against the FDU/LU names

- extracted text from `data/source/nicf_fsp/nicf_forest_stewardship_plan_2020.pdf`;
- confirmed the 2020 FSP text identifies three proposed FDUs: Holberg, Keogh,
  and Marble;
- recorded that the additional 2024 amendment spatial names (`Nahwitti`,
  `Shushartie`, and `Tsulquate`) do not appear in the extracted 2020 FSP text;
  and
- kept the accepted runtime AOI undecided as a source-version choice between
  the 2020 FSP text and the 2024 amendment spatial payload.

## 2026-06-23 - Accepted the 2024 amendment FDU layer as bootstrap AOI source

- recorded `NICF_FDU_2024.shp` as the accepted bootstrap AOI source because the
  project request identifies the amendment spatial payload as the new AOI;
- preserved six FDU/LU features as canonical source semantics rather than
  treating a dissolved AOI polygon as source truth;
- kept the 2020 FSP three-FDU evidence as historical/context evidence; and
- left canonical extraction and runtime config wiring for a later bounded
  `P1.2` slice.

## 2026-06-23 - Extracted the canonical bootstrap AOI source layer

- extracted `NICF_FDU_2024` from the amendment zip into
  `data/source/nicf_fsp/aoi/nicf_fdu_2024.*`;
- verified the extracted shapefile reads as six valid EPSG:3005 polygon
  features with the same bounds and area recorded during raw-payload
  inspection;
- recorded file hashes and read-verification evidence in
  `planning/source_inventory.md`; and
- left BCGW LU canonical-reference and runtime config wiring decisions for
  later bounded `P1.2` slices.

## 2026-06-23 - Corrected the canonical FSP AOI to FDU 1-3 only

- corrected the bootstrap AOI convention after project clarification that only
  FDU 1 Holberg, FDU 2 Keogh, and FDU 3 Marble make up the FSP AOI;
- replaced the misleading six-feature canonical AOI extraction with
  `data/source/nicf_fsp/aoi/nicf_fsp_aoi.*`;
- verified the corrected canonical AOI reads as three valid EPSG:3005 polygon
  features with total measured area `147798.392 ha`; and
- kept the original amendment zip as raw provenance for all six amendment
  features.

## 2026-06-23 - Extracted the canonical LU reference context

- decided that the full 27-feature BCGW LU payload remains raw provenance while
  the canonical LU reference context is the FSP-relevant Holberg, Keogh, and
  Marble subset;
- extracted that subset to
  `data/source/nicf_fsp/lu_reference/nicf_lu_reference.*`;
- verified the LU reference layer reads as three valid EPSG:3005 polygon
  features with total measured area `165588.857 ha`; and
- marked `P1.2d` complete while leaving run-profile source-path wiring as the
  next bounded `P1.2` move.

## 2026-06-23 - Wired the NICF run profile to accepted source paths

- updated `config/run_profile.nicffsp.yaml` so `selection.boundary_path` points
  at `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp`;
- recorded the LU reference source at
  `selection.source_context.lu_reference_path` as
  `data/source/nicf_fsp/lu_reference/nicf_lu_reference.shp`;
- kept raw zip payloads out of runtime source-path wiring; and
- marked `P1.2` complete in the roadmap, leaving `P1.3` as the next active
  Phase 1 task.

## 2026-06-23 - Compared the K3Z template against the NICF scaffold

- recorded the `P1.3a` K3Z-to-NICF comparison in
  `planning/k3z_template_adaptation.md`;
- identified the K3Z surfaces that can provide structure but not accepted NICF
  semantics: run profile, rebuild spec, model-input bundle, treatment variants,
  Patchworks tracks, and runtime package layout;
- recorded that NICF does not yet have a model-input bundle or Patchworks
  package and that `config/patchworks.runtime.windows.yaml` remains a
  K3Z-shaped placeholder; and
- marked `P1.3a` complete while leaving run-profile boundary defaults and
  assumption review lists as the next `P1.3` moves.

## 2026-06-23 - Defined the first NICF run-profile boundary

- activated the first NICF stratification defaults in
  `config/run_profile.nicffsp.yaml`: subzone BEC grouping, two-species
  combinations, TM second-species fallback, and `0.90` area coverage;
- set first-compile runtime defaults to `resume: false`,
  `vdyp_sampling_mode: all`, `vdyp_two_pass_rebin: true`,
  `vdyp_min_stands_per_si_bin: 10`, and `managed_curve_mode: tipsy`;
- recorded the P1.3b decision in `planning/k3z_template_adaptation.md`; and
- marked `P1.3b` complete while keeping K3Z assumption review and minimum
  model-input surfaces as the next `P1.3` work.

## 2026-06-23 - Split K3Z carry-forward and review assumptions

- added the `P1.3c` carry-forward and FRST 558 review tables to
  `planning/k3z_template_adaptation.md`;
- accepted K3Z structure, run-profile mechanics, bundle table contracts, and
  package layout as structural carry-forward assumptions;
- marked K3Z TIPSY rules, treatment variants, cedar signals, expansion
  candidate rules, seral objectives, product/account targets, and baseline
  acceptance metrics as review-required before implementation; and
- marked `P1.3c` complete while leaving minimum source-derived model-input
  surfaces as the remaining `P1.3` planning move.

## 2026-06-23 - Accepted the first K3Z-to-NICF adaptation boundary

- recorded the minimum source-derived model-input surfaces required before
  Patchworks runtime-package work in `planning/k3z_template_adaptation.md`;
- defined the P1.4 handoff terms for cedar-signal, expansion-candidate, and
  runtime-package follow-on issue bodies;
- recorded P1.3 non-goals so no model-input bundle, K3Z tracks, cedar products,
  expansion logic, or runtime package work starts inside adaptation planning;
  and
- marked `P1.3` complete in the roadmap.

## 2026-06-23 - Queued 2025 VRI source-data collection for Phase 1

- opened `#5` as `P1.5` for materializing the latest 2025 provincial VRI R1
  and VDYP7 polygon/layer source packages before NICF base AOI inventory
  extraction depends on them;
- added `planning/vri_2025_data_collection.md` with package ids, expected
  source package names, public-data target paths, and acceptance criteria;
- updated the Phase 1 roadmap and parent issue so the new data-collection task
  is a linked child issue; and
- kept the task boundary to source materialization and verification, with no
  model-input bundle or Patchworks runtime-package build started.

## 2026-06-23 - Recorded 2025 VRI package metadata

- recorded the official BCDC titles, package ids, package UUIDs, resource ids,
  resource names, modified timestamps, formats, and direct package URLs for the
  2025 R1 and VDYP7 polygon/layer source packages in
  `planning/vri_2025_data_collection.md`;
- marked `P1.5a` complete in the roadmap; and
- kept package size, checksum, read-smoke, and public-data publication status
  open until the archives are actually materialized.

## 2026-06-23 - Materialized the 2025 VRI source archives

- downloaded the 2025 R1 and VDYP7 polygon/layer source archives into
  `external/femic-public-data/data/bc/vri/2025/`;
- validated both archives with a zip CRC pass before accepting them as
  materialized local sources;
- annex-added and pushed the public-data commit
  `348d9b60529e3a0160672048fc33e4083f2128fb`; and
- marked `P1.5b` complete while leaving geodatabase read-smoke, CRS, and
  public-remote publication evidence open.

## 2026-06-23 - Added the TFL 6 MP10 information-package reference

- found the BC-hosted copy of the TFL 6 Management Plan 10 timber supply
  analysis information package;
- downloaded it to
  `data/source/nicf_fsp/reference/tfl_6_management_plan_10_information_package_2011.pdf`;
- verified the PDF page count, checksum, and title text; and
- recorded source provenance in `planning/source_inventory.md`.

## 2026-06-23 - Queued the TFL 6 AOI pivot and TSR recipe lanes

- opened `#6` for the active AOI pivot to TFL 6 and the TFL 6-clipped 2025 VRI
  input-layer build;
- opened `#7` for translating the 2011 TFL 6 management plan and information
  package into FEMIC-style source-layer and THLB netdown recipe planning;
- added `planning/tfl6_aoi_pivot_and_input_layers.md` and
  `planning/tfl6_thlb_recipe_extraction.md`; and
- updated the roadmap so the original FDU 1/2/3 boundary remains provenance but
  is superseded for active model extraction.

## 2026-06-23 - Reconciled pre-pivot AOI planning surfaces

- updated the README, quickstart, run-profile comments, and older planning
  notes so TFL 6 is consistently described as the active target AOI;
- preserved the current `selection.boundary_path` value as a temporary
  pre-pivot bootstrap path until `P1.6a` materializes the TFL 6 boundary; and
- clarified that FDU 1/2/3 source layers remain valid provenance, not the active
  model extraction boundary.

## 2026-06-23 - Materialized the TFL 6 boundary

- fetched `WHSE_ADMIN_BOUNDARIES.FADM_TFL` where `FOREST_FILE_ID='TFL6'`;
- wrote the normalized boundary to
  `data/source/tfl_6/aoi/tfl_6_boundary.gpkg`;
- verified 182 EPSG:3005 features, `217042.719 ha` union area, matching bounds,
  and valid geometries after repairing one source ring self-intersection; and
- switched `config/run_profile.nicffsp.yaml` to the accepted TFL 6 boundary
  path and marked `P1.6a` complete.

## 2026-06-23 - Indexed the TFL 6 reference corpus

- added the locally copied TFL 6 reference corpus under `reference/`;
- generated `reference/tfl6_reference_index.json` and
  `reference/tfl6_reference_index.md`;
- extracted searchable text for all readable PDFs under
  `reference/extracted_text/`;
- indexed 18 files: 17 PDFs and one image, including AAC rationale, licence
  maps, instrument, annual reports, Management Plan 9/10 files, analysis report,
  and information package documents; and
- marked `P1.7a` complete.

## 2026-06-23 - Prepared the instance rename to femic-tfl6-instance

- updated visible instance naming in README, quickstart, AGENTS, roadmap, and
  generated corpus metadata ahead of the GitHub/local submodule rename.

## 2026-06-23 - Clipped the 2025 R1 VRI source to TFL 6

- read the provincial 2025 R1 polygon source from the FEMIC public-data mirror;
- bbox-filtered `42297` R1 features to the TFL 6 boundary extent;
- exact-clipped `26959` intersecting features to the dissolved TFL 6 boundary;
- wrote `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg` and
  `data/input/tfl_6/vri_2025_r1_poly_tfl6_clip_manifest.json`;
- verified `26959` valid EPSG:3005 MultiPolygon features with
  `217042.718950 ha` clipped area; and
- identified `feature_id` as the preferred VDYP join-key candidate for `P1.6c`.

## 2026-06-23 - Filtered the 2025 VDYP7 tables to TFL 6

- filtered `VEG_COMP_VDYP7_INPUT_POLY` and `VEG_COMP_VDYP7_INPUT_LAYER` to the
  `26959` clipped TFL 6 R1 feature IDs;
- wrote `data/input/tfl_6/vdyp7_input_poly_2025_tfl6.parquet`,
  `data/input/tfl_6/vdyp7_input_layer_2025_tfl6.parquet`, and
  `data/input/tfl_6/vdyp7_input_2025_tfl6_filter_manifest.json`;
- retained `26833` VDYP7 polygon rows and `25585` VDYP7 layer rows;
- verified that retained VDYP7 polygon rows have no feature IDs outside the
  clipped R1 set and that retained VDYP7 layer rows have no feature IDs outside
  the retained VDYP7 polygon table; and
- recorded missing R1-to-VDYP diagnostics for downstream inventory and THLB
  recipe work.

## 2026-06-23 - Accepted the TFL 6 input-layer manifest

- wrote `data/input/tfl_6/input_layers_manifest.json` as the accepted input
  manifest for the active TFL 6 AOI;
- recorded the accepted TFL 6 boundary, clipped 2025 R1 polygon layer,
  filtered 2025 VDYP7 polygon table, and filtered 2025 VDYP7 layer table;
- updated source-inventory and K3Z adaptation notes so the original FDU 1/2/3
  AOI is historical provenance only, not the active model extraction boundary;
- marked `P1.6` complete in the roadmap; and
- unblocked reviewed source-layer and THLB netdown recipe planning under `#7`
  without starting recipe execution or Patchworks runtime-package work.

## 2026-06-23 - Reviewed 2011 TFL 6 documents for recipe planning

- added `planning/tfl6_2011_document_review.md` as the first reviewed P1.7b
  extraction note;
- anchored the land-base review to the 2011 information package Section 6 and
  Tables 4-17;
- recorded first-pass source-layer, THLB netdown, yield, visual, old-seral,
  steep-terrain, and minimum-harvest assumption candidates;
- noted the MP10 historical Table 4 total landbase/THLB benchmarks separately
  from the current P1.6 2025 TFL 6 input-layer surface; and
- marked P1.7b complete without creating or executing recipe YAML.

## 2026-06-23 - Added the TFL 6 THLB netdown backbone

- added `planning/tfl6_thlb_netdown_steps.md` as the ordered MP10 Table 4
  THLB netdown planning surface;
- preserved the literal TFL 6 information-package order from total landbase to
  current THLB and long-term landbase;
- added tentative GLB/AFLB/LHLB/THLB stage mapping for FEMIC review;
- recorded per-step input-layer and GIS overlay/readiness notes; and
- kept recipe YAML creation and netdown execution blocked pending P1.7c
  adaptation review and P1.7d skeleton drafting.

## 2026-06-23 - Scraped post-2011 TFL 6 instrument evidence

- scraped the Province of British Columbia TFL 6 page for instrument links with
  displayed dates from 2011 onward;
- retained `reference/tfl-06-inst-101-january-1-2015.pdf` as the relevant
  post-2011 instrument document;
- excluded Instrument 10 after visual review confirmed it is a 1957 amendment
  despite the misleading current source-page date label;
- extracted page images under `reference/extracted_images/` because the
  retained PDF is an image-backed scan with no useful searchable text layer;
- updated `reference/tfl6_reference_index.json` and
  `reference/tfl6_reference_index.md` with instrument metadata and
  boundary-reconciliation evidence;
- added `planning/tfl6_instrument_boundary_reconciliation.md`; and
- recorded Instrument 101 as strong evidence that Jan. 1, 2015 additions from
  TFL 39 Block 4 plausibly explain most or all of the gap between the `171441
  ha` MP10 historical GLB and the `217042.718950 ha` current FADM-derived AOI.

## 2026-06-23 - Added scaled current-AOI THLB benchmarks

- added `planning/tfl6_adjusted_thlb_benchmarks.md` and
  `planning/tfl6_adjusted_thlb_benchmarks.json`;
- scaled the 2011 MP10 Table 4 netdown values by
  `217042.718950 / 171441 = 1.265990742879`;
- recorded provisional current-AOI validation targets, including `186175.333
  ha` productive forest, `170428.940 ha` operable landbase, `136487.728 ha`
  current THLB, and `134598.870 ha` long-term landbase; and
- kept the scaled targets explicitly non-authoritative until spatial current
  AOI recipe outputs supersede them.

## 2026-06-23 - Clarified adjusted benchmark residual-delta caveat

- recorded that Instrument 101 is close enough to use as the working
  explanation for current-AOI benchmark scaling in the teaching instance;
- noted that the remaining GLB-area mismatch may reflect smaller net-outs,
  parcel cleanup, boundary-vintage differences, or other post-MP10 tenure
  changes; and
- recorded a possible K3Z/community-forest carve-out as an unverified candidate
  only, not as accepted boundary evidence.

## 2026-06-23 - Added TFL 6 recipe adaptation contract

- added `planning/tfl6_recipe_adaptation_contract.md` as the P1.7c
  classification surface;
- classified each MP10 Table 4 netdown row as TSA29 carry-forward,
  TFL/general-FMU adaptation, missing-source work, aspatial fallback candidate,
  or reference target only;
- recorded source-layer priority for P1.7d skeleton drafting;
- classified Instrument 101 and adjusted current-AOI benchmark tables as
  validation context, not recipe inputs; and
- marked P1.7c complete without creating recipe YAML or running THLB netdown.

## 2026-06-23 - Drafted TFL 6 recipe skeleton planning tables

- added `planning/tfl6_recipe_skeletons.md` as the P1.7d non-executable
  skeleton surface;
- proposed future TFL/general-FMU recipe destinations under `config/tfl6/`
  while keeping the current `config/tsr/` paths as TSA29 pattern references;
- listed source-layer candidates and acquisition strategies where known;
- drafted the ordered THLB netdown skeleton table with source IDs, execution
  classes, blocked-execution status, and validation targets;
- kept all missing-source and fallback rows blocked from execution; and
- marked P1.7 complete without creating recipe YAML or running THLB netdown.

## 2026-06-23 - Recorded 2025 VRI source-package read smoke

- updated `planning/vri_2025_data_collection.md` with direct zipped
  file-geodatabase read-smoke evidence for the 2025 VRI source packages;
- verified `VEG_COMP_LYR_R1_POLY` as an EPSG:3005 `MultiPolygon` layer with
  `7154522` features;
- verified `VEG_COMP_VDYP7_INPUT_POLY` and `VEG_COMP_VDYP7_INPUT_LAYER` as
  non-spatial tables with `7104182` and `7608054` rows, respectively;
- recorded first-field checks for R1, VDYP7 polygon, and VDYP7 layer surfaces;
  and
- marked P1.5c complete while leaving public-data remote publication status
  open for P1.5d.

## 2026-06-23 - Audited 2025 VRI public-data publication status

- updated `planning/vri_2025_data_collection.md` with the `arbutus-s3`
  publication audit for the 2025 VRI source archives;
- confirmed the public-data special remote is configured with `public: yes` and
  the expected public URL;
- confirmed both 2025 VRI archive keys are still local-only and are returned by
  `git annex find --not --in arbutus-s3`;
- recorded that a fresh environment cannot yet be expected to materialize these
  two archives through the normal public-data workflow; and
- left P1.5 open for remote key copy, `git-annex` publication-state push, and
  public-read materialization smoke.

## 2026-06-23 - Published 2025 VRI source archives to public data

- loaded the local Arbutus credential environment and copied only the two 2025
  VRI source archive annex keys to the `arbutus-s3` public-data remote;
- merged and pushed the `external/femic-public-data` `git-annex` publication
  branch after the upload;
- verified `git annex find --not --in arbutus-s3` no longer returns either
  2025 VRI archive path;
- verified a fresh no-credentials clone of `UBC-FRESH/femic-public-data` can
  download both 2025 VRI archives from `arbutus-s3` and pass checksum
  verification;
- updated `planning/vri_2025_data_collection.md` with the final publication
  and public-read smoke evidence; and
- marked P1.5 complete.

## 2026-06-23 - Opened cedar-signal design follow-on issue

- opened `#8` as the P1.4a cedar-signal design follow-on issue;
- scoped `#8` to Cw cultural reserve behavior, utility-pole-grade product
  requirements, treatment implications, yield-curve implications, and
  Patchworks-facing account/reporting outputs;
- kept model-input bundle generation and Patchworks runtime-package compilation
  out of the issue scope; and
- updated `ROADMAP.md` so P1.4a is complete and P1.4b is the next Phase 1 edge.

## 2026-06-23 - Opened expansion candidate-area design follow-on issue

- opened `#9` as the P1.4b expansion candidate-area design follow-on issue;
- scoped `#9` to unallocated candidate-area pool semantics, K3Z carry-forward
  review, source-derived productivity screening, AAC uplift constraints, and
  dependency boundaries;
- kept candidate-area geometry, THLB/model-input edits, and Patchworks runtime
  compilation out of the issue scope; and
- updated `ROADMAP.md` so P1.4b is complete and P1.4c is the next Phase 1 edge.

## 2026-06-23 - Opened Patchworks runtime-package follow-on issue

- opened `#10` as the P1.4c Patchworks runtime-package build/QA follow-on
  issue;
- scoped `#10` to runtime-package prerequisites, ForestModel/XML generation
  boundaries, Matrix Builder expectations, tracks/features/accounts QA,
  representative Patchworks launch smoke, and artifact policy;
- linked runtime-package work to dependencies on accepted TFL 6 inputs, source
  and THLB recipe planning, cedar design `#8`, and expansion design `#9`;
- kept XML generation, Matrix Builder execution, and Patchworks launch out of
  the issue split; and
- marked P1.4 complete in `ROADMAP.md`.

## 2026-06-23 - Added P1.8 next-phase planning gate

- opened `#11` as the P1.8 roadmap phase-planning gate;
- added P1.8 to `ROADMAP.md` before Phase 1 closeout;
- required proposed Phase 2 through at least Phase 5 roadmap sections, one
  parent issue per proposed phase, and linked child task issues for first
  executable tasks;
- required explicit dependency ordering across source-layer/THLB work, cedar
  design, expansion design, model-input generation, Patchworks runtime build,
  QA/publication, and teaching docs; and
- kept follow-on implementation issues `#8`, `#9`, and `#10` idle until P1.8
  places them into the planned phase structure or the maintainer explicitly
  approves a parallel lane.

## 2026-06-23 - Drafted proposed Phase 2 through Phase 5 roadmap sections

- completed P1.8a by adding proposed Phase 2 through Phase 5 sections to
  `ROADMAP.md`;
- proposed Phase 2 for reviewed source layers and THLB netdown;
- proposed Phase 3 for model-design assumptions, including cedar design `#8`
  and expansion design `#9`;
- proposed Phase 4 for model inputs and Patchworks runtime-package build/QA,
  including runtime follow-on `#10`;
- proposed Phase 5 for publication, teaching docs, and release QA; and
- kept P1.8 open for parent phase issue creation, child task issue creation,
  and final dependency/placement synchronization.

## 2026-06-23 - Created Phase 2 through Phase 5 parent issues

- completed P1.8b by opening one GitHub parent issue per proposed future phase:
  Phase 2 `#12`, Phase 3 `#13`, Phase 4 `#14`, and Phase 5 `#15`;
- updated `ROADMAP.md` so each proposed phase heading references its parent
  issue number;
- moved Current Next Steps to P1.8c child task issue creation and P1.8d
  dependency-order recording; and
- kept implementation follow-on issues `#8`, `#9`, and `#10` idle until P1.8
  links the full phase/child issue tree.
