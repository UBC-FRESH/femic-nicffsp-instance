# Change Log

## 2026-06-23 - Bootstrapped the NICF FSP FRST 558 instance repository

- created the FEMIC instance scaffold for `femic-tfl6-instance`;
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

- updated `config/run_profile.tfl6.yaml` so `selection.boundary_path` points
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
  `config/run_profile.tfl6.yaml`: subzone BEC grouping, two-species
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
- switched `config/run_profile.tfl6.yaml` to the accepted TFL 6 boundary
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

## 2026-06-23 - Created first future-phase child issues

- completed P1.8c by creating/linking first executable child task issues under
  each proposed future phase;
- opened P2.1 `#16` for resolving and materializing TFL 6 THLB source layers;
- reused existing cedar design issue `#8` as the first Phase 3 child task
  under Phase 3 parent `#13`;
- opened P4.1 `#17` for building the reviewed TFL 6 model-input bundle after
  Phase 2 and Phase 3 prerequisites are ready;
- opened P5.1 `#18` for deciding runtime artifact publication policy; and
- kept implementation follow-on issues `#8`, `#9`, and `#10` idle until P1.8d
  and P1.8e finish dependency-order and placement synchronization.

## 2026-06-23 - Recorded future-phase dependency order

- completed P1.8d by adding an explicit `Dependency Order` section to
  `ROADMAP.md`;
- recorded that Phase 2 source-layer/THLB work must precede Phase 3
  model-design assumptions, Phase 4 model-input/runtime-package work, and
  Phase 5 publication/teaching release work;
- recorded that cedar design `#8` and expansion design `#9` belong in the
  model-design dependency layer, while runtime-package follow-on `#10` is
  downstream of accepted inputs, THLB outputs, model design, and model-input
  bundle construction; and
- kept P1.8 open for P1.8e placement/defer synchronization of `#8`, `#9`, and
  `#10`.

## 2026-06-23 - Placed Phase 1 follow-on issues in future phases

- completed P1.8e by placing existing follow-on issues `#8`, `#9`, and `#10`
  into the future phase structure instead of leaving them as unsequenced work;
- placed cedar-signal design `#8` and expansion candidate-area design `#9`
  under Phase 3 parent `#13`;
- placed Patchworks runtime-package build/QA `#10` under Phase 4 parent `#14`,
  downstream of model-input bundle task `#17`;
- added a `Follow-on Issue Placement` section to `ROADMAP.md`;
- marked P1.8 complete in `ROADMAP.md`; and
- moved Current Next Steps to P2.1 `#16` while keeping Phase 3 and Phase 4
  implementation lanes idle until their dependencies are accepted or explicitly
  narrowed.

## 2026-06-23 - Tightened phase closeout workflow contract

- amended `AGENTS.md` to make phase closeout the required next slice after the
  final child issue or phase gate completes;
- clarified that agents must reconcile the phase parent issue, PR state,
  roadmap, changelog, and issue comments before advancing to the next phase's
  first task; and
- corrected `ROADMAP.md` Current Next Steps so Phase 1 closeout comes before
  P2.1 `#16`.

## 2026-06-23 - Started P2.1 source-layer dependency inventory

- created `feature/p2-source-layer-thlb-inputs` from merged instance `main`;
- added `planning/tfl6_source_layer_dependency_inventory.md` as the first P2.1
  dependency-resolution surface;
- separated accepted local TFL 6 AOI/VRI/VDYP inputs from R1/VDYP field-mapping
  blockers, missing public/reference spatial layers, and fallback-only rows;
- updated `ROADMAP.md` Current Next Steps to continue P2.1 authority/source
  resolution before downloads, recipe YAML, or THLB execution; and
- performed no source downloads, recipe execution, model-input generation, or
  Patchworks runtime work.

## 2026-06-23 - Resolved first roads/operability source candidates

- ran a metadata-only FEMIC BCDC resolver pass for TFL 6 roads and operability
  candidate layers;
- recorded Digital Road Atlas MPAR
  `WHSE_BASEMAPPING.DRA_DGTL_ROAD_ATLAS_MPAR_SP` as the first public authority
  candidate for current existing-road geometry;
- recorded 2025 CEF Integrated Roads as a secondary/reference candidate, not
  the accepted road authority;
- recorded that no public TFL 6-specific operability geometry was accepted from
  the first resolver pass, so operability remains a local-evidence/proxy
  decision; and
- updated `ROADMAP.md` Current Next Steps to move the next P2.1 resolver slice
  to hydrology/wetlands/shoreline and legal overlays before source
  materialization.

## 2026-06-23 - Resolved hydrology and legal overlay candidates

- ran metadata-only FEMIC BCDC resolver passes for Freshwater Atlas hydrology,
  shoreline/coastline, UWR, WHA, and OGMA candidate layers;
- recorded Freshwater Atlas streams, lakes, and wetlands as the first public
  hydrology materialization candidates;
- recorded approved UWR
  `WHSE_WILDLIFE_MANAGEMENT.WCP_UNGULATE_WINTER_RANGE_SP` and approved WHA
  `WHSE_WILDLIFE_MANAGEMENT.WCP_WILDLIFE_HABITAT_AREA_POLY` as the first
  legal-overlay materialization candidates, rejecting proposed layers for the
  reviewed lane;
- recorded current legal OGMA
  `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW` as the first established
  OGMA candidate, with current-vs-2011 vintage risk;
- kept current non-legal OGMA as a review clue only for the draft-OGMA row;
- kept shoreline/ocean handling unresolved because the clean public coastline
  candidates found in this pass are coarse NTS 1:250,000 layers; and
- updated `ROADMAP.md` Current Next Steps to move the next P2.1 resolver slice
  to recreation features and LU/RMZ/BEC strata before source materialization.

## 2026-06-23 - Resolved recreation and LU/BEC strata candidates

- ran metadata-only FEMIC BCDC resolver passes for recreation features,
  landscape units, BEC, and resource-management-zone candidate layers;
- recorded recreation polygons
  `WHSE_FOREST_TENURE.FTEN_RECREATION_POLY_SVW`, recreation trails
  `WHSE_FOREST_TENURE.FTEN_REC_TRAILS_SVW`, and recreation site points
  `WHSE_FOREST_TENURE.FTEN_REC_SITE_POINTS_SVW` as first public recreation
  materialization candidates;
- recorded recreation details/closures
  `WHSE_FOREST_TENURE.FTEN_REC_DTAILS_CLOSURES_SV` as attribution/context
  only;
- recorded Landscape Units of British Columbia
  `WHSE_LAND_USE_PLANNING.RMP_LANDSCAPE_UNIT_SVW` and BEC Map
  `WHSE_FOREST_VEGETATION.BEC_BIOGEOCLIMATIC_POLY` as first public strata
  candidates;
- kept Strategic Land and Resource Plans
  `WHSE_LAND_USE_PLANNING.RMP_STRGC_LAND_RSRCE_PLAN_SVW` as an RMZ review clue
  only, not an accepted TFL 6 RMZ source;
- rejected the generic `TFL 6 resource management zones` resolver hit because
  it returned an unrelated North Coast riparian-management-zone dataset; and
- updated `ROADMAP.md` Current Next Steps to point at historical/fallback
  decisions and source-materialization planning before any downloads.

## 2026-06-24 - Recorded P2.1 historical fallback decisions

- recorded provisional teaching fallback decisions for the remaining P2.1
  historical/fallback rows without downloading or materializing source layers;
- kept 1999 WFP operability as historical/local-source evidence only and
  accepted MP10 Table 8 / adjusted benchmark as an aspatial fallback until
  local operability geometry is found;
- preserved the MP10 40 m ocean-shoreline rule while keeping coarse NTS
  coastline as a teaching candidate requiring review;
- kept current non-legal OGMA as a review clue only and accepted MP10 Table 11
  / adjusted benchmark as the draft-OGMA fallback until historical geometry is
  found;
- accepted LU/BEC public candidates while keeping RMZ geometry/schema
  unresolved and recording MP10 Table 16 as a reviewed percent-by-stratum
  fallback;
- recorded MP10 Table 15 cultural heritage as an aspatial/proxy fallback and
  confirmed that sensitive TUS/CMT geometry should not be sought as public
  input; and
- updated `ROADMAP.md` Current Next Steps to point at a P2.1
  source-materialization plan before any downloads or THLB execution.

## 2026-06-24 - Split operability into its own P2.1a design lane

- opened `#20` as `P2.1a` for operability netdown proxy and sensitivity design;
- added `planning/tfl6_operability_netdown_proxy.md` with MP9/MP10 evidence for
  physical/economic operability, yarding-system logic, slope classes, minimum
  harvest criteria, and economic-access sensitivities;
- updated `planning/tfl6_source_layer_dependency_inventory.md` so MP10 Table 8
  / adjusted benchmarks remain calibration context rather than a final locked
  aspatial fallback;
- updated `ROADMAP.md` Current Next Steps so P2.1a design precedes the
  source-materialization plan; and
- performed no DEM materialization, slope-raster build, recipe YAML creation,
  THLB execution, model-input generation, or Patchworks runtime work.

## 2026-06-24 - Confirmed public current OGMA polygon authorities

- ran a metadata-only FEMIC BCDC resolver deep dive for legal, non-legal, and
  general OGMA layer candidates;
- confirmed `WHSE_LAND_USE_PLANNING.RMP_OGMA_LEGAL_CURRENT_SVW` as the public,
  WFS-queryable current legal OGMA polygon layer and first established-OGMA
  materialization candidate;
- confirmed `WHSE_LAND_USE_PLANNING.RMP_OGMA_NON_LEGAL_CURRENT_SVW` as the
  public, WFS-queryable current non-legal OGMA polygon layer and first
  materialization/review candidate for the draft-OGMA row;
- recorded non-materializing TFL 6 bbox WFS hit checks of `264` legal-current
  and `26` non-legal-current features;
- kept government-only `Legal - All` and `Non Legal - All` OGMA layers out of
  the public teaching source lane; and
- performed no OGMA download, clipping, recipe YAML creation, THLB execution,
  model-input generation, or Patchworks runtime work.

## 2026-06-24 - Recorded P2.1a DEM discovery for operability slope proxy

- ran metadata-only FEMIC BCDC resolver passes for DEM, LiDAR, CDED, TRIM
  contour, elevation, and slope-raster candidates;
- recorded LidarBC/open LiDAR as the preferred future high-resolution source
  route for a defensible TFL 6 stand-level slope surface, subject to AOI tile
  coverage and materialization planning;
- recorded CDED 1:250,000 as a coarse fallback or raster-pipeline smoke-test
  source, not the preferred operability proxy surface;
- recorded RESULTS openings slope/aspect/elevation as an attribute clue only,
  not a continuous DEM substitute;
- recorded that no useful ready-made public provincial slope-raster candidate
  was found by the resolver queries; and
- performed no DEM download, raster clipping, slope derivation, zonal
  statistics, recipe YAML creation, THLB execution, model-input generation, or
  Patchworks runtime work.

## 2026-06-24 - Drafted P2.1a operability parameter contract

- added a base-case-versus-sensitivity parameter table to
  `planning/tfl6_operability_netdown_proxy.md`;
- separated base-case design stance from student-tunable sensitivity knobs for
  height class, species group, stocking/open-stand signal, volume threshold,
  slope threshold, proportion-of-stand slope threshold, heli inclusion,
  marginal economic classes, and road/access pressure;
- added later DEM materialization-plan requirements covering LidarBC tile-index
  selection, AOI buffering, tile count/volume estimates, public-data suitability,
  CDED smoke-test sequencing, canonical paths, and QA checks;
- updated `ROADMAP.md` Current Next Steps so P2.1a is now ready for maintainer
  review/closeout or targeted edits before any source downloads start; and
- performed no source download, DEM materialization, slope derivation, zonal
  statistics, recipe YAML creation, THLB execution, model-input generation, or
  Patchworks runtime work.

## 2026-06-24 - Closed P2.1a operability design lane

- audited P2.1a acceptance against `planning/tfl6_operability_netdown_proxy.md`,
  `planning/tfl6_source_layer_dependency_inventory.md`, `ROADMAP.md`, and issue
  comments;
- marked P2.1a complete in `ROADMAP.md`;
- moved Current Next Steps back to P2.1 source-materialization planning, with
  operability proxy/DEM slope kept as a later reviewed dependency rather than
  an immediate download;
- closed GitHub issue `#20` after posting a final closeout comment; and
- performed no source download, DEM materialization, slope derivation, zonal
  statistics, recipe YAML creation, THLB execution, model-input generation, or
  Patchworks runtime work.

## 2026-06-24 - Drafted P2.1 source-materialization plan

- added a source-materialization plan to
  `planning/tfl6_source_layer_dependency_inventory.md`;
- separated safe-to-clip-first public candidates from review/fallback-only rows;
- listed planned output paths for FWA hydrology, approved UWR/WHA, legal and
  non-legal current OGMAs, recreation features, landscape units, BEC, and DRA
  roads;
- kept operability proxy/DEM slope, shoreline precision, RMZ schema, cultural
  heritage, future roads, historical WFP operability geometry, and
  government-only OGMA `All` layers out of the first materialization pass;
- added provenance manifest requirements and first-pass QA checks for future
  materialized layers;
- updated `ROADMAP.md` Current Next Steps so source downloads remain blocked
  until the materialization plan is accepted; and
- performed no source download, clipping, recipe YAML creation, THLB execution,
  model-input generation, or Patchworks runtime work.

## 2026-06-24 - Accepted P2.1 source-materialization plan

- marked the source-materialization plan in
  `planning/tfl6_source_layer_dependency_inventory.md` as accepted for the first
  bounded P2.1 materialization pass;
- clarified that acceptance authorizes only safe-to-clip-first rows and does
  not accept any materialized layer as executable THLB recipe logic;
- kept review/fallback-only rows out of scope for the first materialization
  pass;
- updated `ROADMAP.md` Current Next Steps to the first approved
  source-materialization pass; and
- performed no source download, clipping, recipe YAML creation, THLB execution,
  model-input generation, or Patchworks runtime work.

## 2026-06-24 - Materialized FWA hydrology sources for review

- materialized the first approved P2.1 source family: FWA streams, lakes, and
  wetlands clipped to the accepted TFL 6 AOI;
- wrote curated review artifacts under `data/source/tfl_6/hydrology/`;
- recorded provenance, source authority, transient fetch details, clipped
  feature counts, area/length summaries, SHA-256 hashes, and read-smoke
  evidence in `data/source/tfl_6/hydrology/hydrology_source_manifest.json`;
- recorded `12078` clipped stream features with `4748715.276 m` total line
  length, `599` clipped lake polygons with `3243.849 ha`, and `572` clipped
  wetland polygons with `982.424 ha`;
- updated `planning/tfl6_source_layer_dependency_inventory.md` and
  `ROADMAP.md` so the next P2.1 materialization pass remains bounded to another
  safe-to-clip source family; and
- accepted no riparian recipe semantics, created no recipe YAML, ran no THLB
  netdown, generated no model inputs, and performed no Patchworks runtime work.

## 2026-06-24 - Materialized approved wildlife overlays for review

- materialized the approved UWR and WHA public wildlife overlay candidates
  clipped to the accepted TFL 6 AOI;
- wrote curated review artifacts under `data/source/tfl_6/wildlife/`;
- recorded provenance, source authority, transient fetch details, clipped
  feature counts, area summaries, SHA-256 hashes, and read-smoke evidence in
  `data/source/tfl_6/wildlife/wildlife_source_manifest.json`;
- recorded `22` clipped UWR polygons with `2365.514 ha` total area and `45`
  clipped WHA polygons with `2942.796 ha` total area;
- updated `planning/tfl6_source_layer_dependency_inventory.md` and
  `ROADMAP.md` so the next P2.1 materialization pass remains bounded to another
  safe-to-clip source family, preferably current legal/non-legal OGMA overlays;
  and
- accepted no wildlife netdown semantics, created no recipe YAML, ran no THLB
  netdown, generated no model inputs, and performed no Patchworks runtime work.

## 2026-06-24 - Materialized current OGMA overlays for review

- materialized the current legal and current non-legal public OGMA overlay
  candidates clipped to the accepted TFL 6 AOI;
- wrote curated review artifacts under `data/source/tfl_6/ogma/`;
- recorded provenance, source authority, transient fetch details, clipped
  feature counts, area summaries, rule-critical fields, date summaries,
  SHA-256 hashes, and read-smoke evidence in
  `data/source/tfl_6/ogma/ogma_source_manifest.json`;
- recorded `165` clipped legal-current OGMA polygons with `16131.032 ha`
  total area and `2` clipped non-legal-current OGMA multipolygons with
  `0.687 ha` total area;
- preserved the current-vs-2011 vintage warning: current non-legal OGMA is a
  proxy candidate only and should not be treated as the MP10 draft-OGMA row
  without recipe-readiness review against MP10 Table 11 and the adjusted
  benchmark;
- updated `planning/tfl6_source_layer_dependency_inventory.md` and
  `ROADMAP.md` so the next P2.1 materialization pass remains bounded to another
  safe-to-clip source family, preferably recreation features or LU/BEC strata;
  and
- accepted no established-OGMA or draft-OGMA netdown semantics, created no
  recipe YAML, ran no THLB netdown, generated no model inputs, and performed no
  Patchworks runtime work.

## 2026-06-24 - Materialized recreation sources for review

- materialized public recreation polygons, recreation trails, recreation site
  points, and recreation details/closures clipped or filtered to the accepted
  TFL 6 AOI;
- wrote curated review artifacts under `data/source/tfl_6/recreation/`;
- recorded provenance, source authority, transient fetch details, clipped or
  filtered feature counts, area/length/count summaries, rule-critical fields,
  date summaries, SHA-256 hashes, and read-smoke evidence in
  `data/source/tfl_6/recreation/recreation_source_manifest.json`;
- recorded `26` clipped recreation polygon features with `187.868 ha`, `3`
  clipped recreation trail features with `1737.285 m`, `10` filtered site
  points, and `13` filtered details/closures points;
- preserved the review-only boundary: recreation class selection,
  retirement/status handling, point/line/polygon overlap order, and the MP10
  10 m buffer rule remain unaccepted;
- updated `planning/tfl6_source_layer_dependency_inventory.md` and
  `ROADMAP.md` so the next P2.1 materialization pass remains bounded to another
  safe-to-clip source family, preferably LU/BEC strata; and
- accepted no recreation netdown semantics, created no recipe YAML, ran no THLB
  netdown, generated no model inputs, and performed no Patchworks runtime work.

## 2026-06-24 - Materialized LU/BEC strata sources for review

- materialized public landscape-unit and BEC strata candidates clipped to the
  accepted TFL 6 AOI;
- wrote curated review artifacts under `data/source/tfl_6/strata/`;
- recorded provenance, source authority, transient fetch details, clipped
  feature counts, area summaries, LU names, BEC labels, rule-critical fields,
  date summaries, SHA-256 hashes, and read-smoke evidence in
  `data/source/tfl_6/strata/strata_source_manifest.json`;
- recorded `13` clipped landscape-unit features and `107` clipped BEC features,
  both summing to `217042.719 ha` because they partition the accepted AOI;
- preserved the review-only boundary: LU/BEC can support OGMA, RMZ, and Table
  16 review, but neither layer is a netdown by itself, and RMZ/Table 16
  executable semantics remain blocked;
- updated `planning/tfl6_source_layer_dependency_inventory.md` and
  `ROADMAP.md` so the next P2.1 materialization pass remains bounded to another
  safe-to-clip source family, preferably DRA existing roads; and
- accepted no RMZ or Table 16 netdown semantics, created no recipe YAML, ran no
  THLB netdown, generated no model inputs, and performed no Patchworks runtime
  work.

## 2026-06-24 - Materialized DRA existing-road source for review

- materialized the Digital Road Atlas MPAR public road-line candidate clipped
  to the accepted TFL 6 AOI;
- wrote the curated review artifact under `data/source/tfl_6/roads/`;
- recorded provenance, source authority, transient fetch details, WFS paging,
  clipped feature count, line-length summary, road class/surface/type fields,
  date summaries, SHA-256 hash, and read-smoke evidence in
  `data/source/tfl_6/roads/roads_source_manifest.json`;
- recorded `10706` clipped DRA road features with `4255862.907 m` clipped
  geometry length;
- preserved the review-only boundary: road class filtering, road-width/buffer
  rules, overlap order, and treatment of trails/bridges/virtual records remain
  unaccepted;
- preserved the future-road boundary: MP10 Table 17 future-road allowance stays
  separate from the current existing-road overlay unless a later scenario
  decision accepts it; and
- updated `planning/tfl6_source_layer_dependency_inventory.md` and
  `ROADMAP.md` so the next P2.1 slice is a source-materialization
  closeout/review pass rather than another download.

## 2026-06-24 - Clarified RMZ terminology in Phase 2 planning

- split operational riparian RMA/RRZ/RMZ language for `tfl6_nd_080` from
  strategic Resource Management Zone language for `tfl6_nd_180`;
- clarified that MP10 Table 16 stand-level retention needs strategic
  Resource Management Zone/LU/BEC attribution or an explicit
  percent-by-stratum fallback, not streamside riparian RMZ geometry;
- preserved the rejected North Coast riparian-management-zone resolver hit as a
  false positive for the TFL 6 strategic RMZ need; and
- kept both riparian-rule execution and Table 16 stand-level-retention
  execution blocked until recipe-readiness review accepts the required schema
  or fallback treatments.

## 2026-06-24 - Accepted aspatial Table 16 stand-level-retention fallback

- ran a targeted strategic RMZ resolver recheck using the current FEMIC BCDC
  resolver against VILUP, Vancouver Island strategic Resource Management Zone,
  EFZ/GMZ/SMZ, TFL 6 resource-management-zone, and exact-object queries;
- confirmed the only plausible public candidate remains
  `WHSE_LAND_USE_PLANNING.RMP_STRGC_LAND_RSRCE_PLAN_SVW`, which exposes WMS,
  KML ground-overlay, and custom-download resources but no usable WFS/direct
  vector geometry for the automated P2.1 lane;
- confirmed the KML path contains WMS overlays, including a Vancouver Island
  Land Use Plan boundary overlay, but no materializable EFZ/GMZ/SMZ or
  strategic RMZ vector polygons for TFL 6; and
- accepted `tfl6_nd_180` as an aspatial MP10 Table 16 stand-level-retention
  deduction for the teaching base case: `5686 ha` historical MP10 or
  `7198.423 ha` scaled current-AOI validation target, with any later strategic
  RMZ spatial treatment deferred to an enhancement/sensitivity lane.

## 2026-06-24 - Added strategic RMZ student-challenge docs note

- added the first minimal Sphinx docs tree under `docs/`;
- documented an advanced student challenge to locate strategic RMZ polygon
  areas, replace the aspatial `tfl6_nd_180` fallback with a geometry-backed
  RMZ/LU/BEC overlay, rebuild the model, and rerun scenarios; and
- kept the challenge scoped as an enhancement/sensitivity exercise rather than
  a base-case prerequisite.

## 2026-06-24 - Added full Sphinx docs requirement to Phase 5 roadmap

- tightened P5.3 so the release phase requires full Sphinx teaching
  documentation modeled on `femic-k3z-instance` and `femic-tsa29-instance`;
- listed the expected docs scope: quickstart, rebuild workflow, source-data
  provenance, THLB validation notes, scenario teaching workflows, advanced
  student challenges, known limitations, and warning-clean Sphinx build
  evidence; and
- kept the minimal current `docs/` tree as an early seed, not the final Phase 5
  documentation deliverable.

## 2026-06-24 - Created Phase 5 full-docs child issue

- opened P5.3 child issue `#21` for building the full Sphinx teaching
  documentation package;
- linked `#21` from the Phase 5 roadmap task and Phase 5 parent issue `#15`;
- scoped the docs package to K3Z/TSA29-style coverage, including student
  quickstart, rebuild workflow, source provenance, THLB validation, scenario
  teaching workflows, advanced challenges, known limitations, and
  warning-clean Sphinx build evidence; and
- kept the issue explicitly downstream of Phase 4 runtime/package QA rather
  than active Phase 2 work.

## 2026-06-24 - Closed P2.1 source-materialization review

- audited the accepted local TFL 6 AOI/VRI/VDYP inputs and the materialized
  hydrology, wildlife, OGMA, recreation, LU/BEC strata, and DRA roads source
  manifests;
- added a P2.1 closeout-review table to
  `planning/tfl6_source_layer_dependency_inventory.md` classifying each MP10
  netdown dependency as accepted local input, materialized-for-review source,
  P2.2 field-mapping work, accepted aspatial fallback, context-only row, or
  deferred enhancement/sensitivity lane;
- marked P2.1 complete in `ROADMAP.md`;
- opened P2.2 child issue `#22` for accepted 2025 R1/VDYP7 field profiling and
  linked it from the roadmap; and
- preserved the boundary that no THLB recipe YAML, THLB execution, model input,
  XML, Matrix Builder, or Patchworks runtime work was started.

## 2026-06-24 - Promoted Phase 2 from proposed to active

- updated `ROADMAP.md` so Phase 2 is no longer described as proposed now that
  P2.1 source-layer and THLB-input work is active under parent issue `#12`;
- left later Phase 3 through Phase 5 sections as proposed/future until their
  dependency gates open; and
- preserved older changelog wording about the original P1.8 proposal step as
  historical provenance.

## 2026-06-24 - Profiled accepted R1 and VDYP7 field surfaces

- added `planning/tfl6_r1_vdyp_field_profile.md` as the P2.2a schema and
  join-coverage profile for accepted 2025 TFL 6 R1 and VDYP7 inputs;
- recorded `feature_id` join integrity across `26959` R1 rows, `26833` VDYP7
  polygon rows, and `25585` VDYP7 layer rows;
- summarized area-weighted candidate fields for non-forest, non-productive,
  deciduous-leading, productivity, BEC, and operability-proxy review;
- updated `ROADMAP.md` so P2.2b is the next bounded slice for candidate field
  mappings and gross-area diagnostics; and
- accepted no executable THLB recipe logic, fetched no new source layers, and
  started no DEM/slope, model-input, XML, Matrix Builder, or Patchworks runtime
  work.

## 2026-06-24 - Drafted P2.2b candidate field-mapping diagnostics

- extended `planning/tfl6_r1_vdyp_field_profile.md` with candidate mapping and
  gross-area diagnostics for `tfl6_nd_010`, `tfl6_nd_040`, `tfl6_nd_140`, and
  operability-proxy review;
- compared candidate gross areas against the scaled current-AOI benchmark
  deductions while keeping gross-vs-marginal accounting explicit;
- flagged `for_mgmt_land_base_ind == N` as a useful QA cross-check rather than
  a clean single-step non-forest rule because it absorbs explicit
  non-productive rows;
- recorded missing VDYP7 layer coverage as a P2.3 QA/mapping item; and
- kept P2.2 open for a short review/acceptance handoff contract before P2.3,
  with no source fetch, recipe YAML, THLB execution, model-input generation,
  XML, Matrix Builder, or Patchworks runtime work started.

## 2026-06-24 - Closed P2.2 R1 and VDYP7 field profiling

- added a P2.2c field-mapping handoff contract to
  `planning/tfl6_r1_vdyp_field_profile.md`;
- accepted BCLCS/non-vegetated/land-cover, explicit non-productive codes plus
  reviewed productivity thresholds, leading-species deciduous signals, BEC
  attribution, and R1/VDYP join diagnostics as suitable surfaces for P2.3
  source-layer recipe-contract drafting;
- kept `for_mgmt_land_base_ind == N` as QA-only because it absorbs explicit
  non-productive rows;
- kept operability-proxy fields as QA/sensitivity support only until the P2.1a
  design constraints and later slope/aspatial decisions are incorporated; and
- marked P2.2 complete in `ROADMAP.md` without fetching source layers, creating
  recipe YAML, executing THLB netdown, building DEM/slope products, generating
  model inputs, or starting XML, Matrix Builder, or Patchworks runtime work.

## 2026-06-24 - Started P2.3 source-layer recipe-contract planning

- opened child issue `#23` for P2.3 under Phase 2 parent `#12`;
- added `planning/tfl6_source_layer_recipe_contracts.md` as the first
  source-layer recipe-contract table for MP10 Table 4 rows;
- classified each row as contract-draft-ready, review-required,
  aspatial-fallback, QA-only, deferred-sensitivity, or context-only;
- recorded P2.4 handoff boundaries for future executable recipe work; and
- kept this slice planning-only, with no source fetch, executable recipe YAML,
  THLB execution, DEM/slope materialization, model-input generation, XML,
  Matrix Builder, or Patchworks runtime work.

## 2026-06-24 - Closed P2.3 source-layer recipe-contract planning

- accepted `planning/tfl6_source_layer_recipe_contracts.md` as the P2.4
  smoke-lane handoff contract;
- defined which rows P2.4 may encode first as inventory-derived rules,
  provisional spatial overlays, aspatial fallbacks, QA-only diagnostics, or
  context-only checkpoints;
- required the first P2.4 smoke report to keep gross area, ordered marginal
  area, cumulative checkpoints, fallback rows, provisional rows, and scaled
  benchmark comparisons visible;
- preserved unresolved road, riparian, vintage, draft-OGMA, operability, and
  strategic-RMZ items as provisional, fallback, or sensitivity-bound rather
  than final semantics; and
- marked P2.3 complete in `ROADMAP.md` without fetching source layers,
  creating executable recipe YAML, executing THLB netdown, building DEM/slope
  products, generating model inputs, or starting XML, Matrix Builder, or
  Patchworks runtime work.

## 2026-06-25 - Started P2.4 THLB smoke-lane planning

- opened child issue `#24` for P2.4 under Phase 2 parent `#12`;
- added `planning/tfl6_thlb_smoke_lane_plan.md` with the first executable
  recipe/scaffold and smoke-run boundary;
- selected the existing FEMIC `config/tsr/` reviewed recipe convention for the
  first TFL 6 smoke lane until a dedicated TFL/general-FMU wrapper exists;
- split P2.4 into bounded subtasks for recipe scaffold creation, scaffold
  validation, exact smoke-run command/stop-line definition, bounded execution,
  and artifact inspection; and
- kept this slice planning-only, with no recipe YAML creation, THLB execution,
  source fetch, DEM/slope materialization, model-input generation, XML, Matrix
  Builder, or Patchworks runtime work.

## 2026-06-25 - Added P2.4c THLB recipe scaffold

- added `config/tsr/source_layers.recipe.yaml` as the companion source-layer
  scaffold for already-materialized TFL 6 inputs;
- added `config/tsr/thlb_netdown.recipe.yaml` with one parent row and one
  scaffolded step for every MP10 Table 4 row from `tfl6_nd_000` through
  `tfl6_nd_210`;
- preserved the P2.3/P2.4 statuses for attribute rules, provisional spatial
  overlays, aspatial fallbacks, context rows, and deferred sensitivity rows;
- verified both scaffold files parse and load through FEMIC's TSR recipe
  loaders without executing THLB logic; and
- updated `ROADMAP.md` and `planning/tfl6_thlb_smoke_lane_plan.md` so P2.4d
  validation/readiness is the next bounded slice.

## 2026-06-25 - Recorded GeoPackage checkpoint support for P2.4d

- updated `planning/tfl6_thlb_smoke_lane_plan.md` to record that parent FEMIC
  issue `#203` supports explicit GeoPackage/vector THLB checkpoint inputs;
- preserved the historical rationale for Feather checkpoints as a TSA29
  restart/debug speed convention rather than a raw-input requirement; and
- recorded the future P2.4e smoke-run command using the accepted R1 GeoPackage
  as the explicit checkpoint/accounting surface, while keeping P2.4d
  validation/readiness non-executing.

## 2026-06-25 - Completed P2.4d THLB smoke scaffold readiness validation

- validated that the THLB and source-layer recipe scaffolds parse as YAML and
  that the THLB scaffold loads through FEMIC's recipe loader;
- confirmed the scaffold contains `22` parent rows and `22` step records from
  `tfl6_nd_000_reference` through `tfl6_nd_210_long_term_landbase`;
- confirmed every source-layer artifact listed by
  `config/tsr/source_layers.recipe.yaml` exists locally, including the accepted
  R1 GeoPackage checkpoint input;
- recorded that output, audit, and status parent directories are either already
  present or created by the FEMIC THLB runner; and
- moved the roadmap edge to P2.4e, the first bounded serial reconstructed smoke
  run, without executing THLB netdown in this slice.

## 2026-06-25 - Completed P2.4e first THLB smoke run

- executed the bounded serial reconstructed THLB smoke command against the
  accepted TFL 6 R1 GeoPackage checkpoint input;
- recorded tracked run evidence in `config/tsr/tfl6_thlb_smoke.audit.json` and
  `config/tsr/thlb_reconstructed.status.md`;
- inspected the generated checkpoint/status products and recorded the smoke
  area signals: `217042.719 ha` GLB proxy, `196833.177 ha` AFLB checkpoint,
  `174768.947 ha` LHLB checkpoint, and `144203.485 ha` final THLB;
- confirmed the smoke run had `12` applied rows, `2` applied no-op rows, and
  `8` unsupported milestone/reference rows, with no blocked exact-overlay
  transformation rows;
- kept bulky `data/tsr/` checkpoints and `runtime/logs/tsr/` products out of
  normal tracked Git content for this closeout; and
- marked P2.4 complete in `ROADMAP.md`, moving the next bounded slice to P2.5
  benchmark/tolerance comparison without starting model-input generation, XML,
  Matrix Builder, or Patchworks runtime work.

## 2026-06-25 - Locked P2.5 THLB benchmark tolerance

- opened P2.5 child issue `#25` and recorded the benchmark/tolerance lock in
  `planning/tfl6_thlb_benchmark_tolerance.md`;
- accepted the P2.4e final current-THLB result of `144203.485 ha` against the
  approximate scaled current-AOI benchmark of `136487.728 ha`;
- recorded the `+7715.757 ha` / `+5.65%` gap as acceptable for the base
  teaching lane because the scaled benchmark depends on the unverifiable
  assumption that the post-2011 extension area has the same mean THLB netdown
  rate as the pre-extension MP10 landbase;
- updated `planning/tfl6_adjusted_thlb_benchmarks.md` with the same tolerance
  lock and caveat;
- marked P2.5 and Phase 2 complete in `ROADMAP.md`; and
- moved the roadmap edge to Phase 3 model-design assumptions, with P3.1 cedar
  signal design as the next default child lane unless the maintainer chooses
  P3.2 expansion design first.

## 2026-06-25 - Restored explicit Phase 2 closeout gate

- reopened Phase 2 parent issue `#12` because the branch/PR lifecycle closeout
  must happen before Phase 3 implementation starts;
- opened P2.6 child issue `#26` for the Phase 2 branch/PR closeout;
- updated `ROADMAP.md` so P2.6 is the active Current Next Step and Phase 3 is
  proposed until the Phase 2 closeout PR path is reconciled; and
- kept the P2.5 THLB tolerance lock intact while correcting the lifecycle
  sequencing mistake.

## 2026-06-25 - Added Phase 2 THLB Sphinx closeout documentation

- added `docs/phase2-thlb-netdown.rst` to document the Phase 2 THLB base lane
  for future maintainers and student users;
- covered the current-AOI versus MP10 historical-boundary rationale, scaled
  benchmark tolerance, accepted `+5.65%` THLB gap, fallback rows, and audit
  trail artifacts;
- linked the new page from `docs/index.rst`;
- updated `ROADMAP.md` so P2.6 explicitly includes Phase 2 THLB Sphinx
  documentation before PR merge; and
- kept full final teaching documentation under later P5.3, after runtime and
  publication surfaces exist.

## 2026-06-25 - Started Phase 3 cedar-signal design

- created branch `feature/p3-model-design-assumptions` from merged instance
  `main`;
- promoted Phase 3 to active in `ROADMAP.md` after Phase 2 closeout;
- split P3.1 cedar-signal design into P3.1a evidence/design note, P3.1b field
  and derived-signal review, and P3.1c Patchworks-facing product/account/report
  requirements;
- added `planning/tfl6_cedar_signal_design.md` with first-pass source evidence
  for cultural cedar, Cw/Cy composition, Cw productivity/yield context, K3Z
  carry-forward boundaries, candidate cedar signals, cultural-reserve behavior,
  utility-pole product questions, treatment/yield implications, and
  Patchworks-facing requirements; and
- kept this slice planning/design only, with no model-input generation,
  ForestModel XML, Matrix Builder, or Patchworks runtime work.

## 2026-06-25 - Added P3.3 AU and yield-curve assignment contract

- opened P3.3 child issue `#28` under Phase 3 parent `#13`;
- added `planning/tfl6_au_yield_curve_contract.md` to define static TFL 6 AU
  identity, yield-curve lanes, MP10 TIPSY parameter extraction/crosswalk
  boundaries, and treatment/operability eligibility interactions;
- recorded that MP10 age-at-time-0 AU splits are rejected as canonical
  Patchworks AU identity, while MP10 Tables 27-29 remain accepted TIPSY
  parameter evidence;
- incorporated MKRF as an additional curve-smoothing and selected-AU/remap
  design reference alongside TSA29, and recorded parent FEMIC issue `#187` as
  the governing shared/default `smoothed_bin_pchip` decision trail; and
- moved the roadmap edge to P3.3 review while keeping cedar P3.1 open but
  paused and avoiding model-input generation, XML, Matrix Builder, and
  Patchworks runtime work.

## 2026-06-25 - Moved AU/yield contract to top Phase 3 priority

- reordered `ROADMAP.md` so P3.3 / `#28` appears first in the Phase 3 stack;
- retained the `P3.3` identifier to preserve the already-created issue,
  comments, and commit audit trail; and
- recorded that cedar P3.1 and expansion P3.2 remain open but downstream of
  the AU/yield contract review.

## 2026-06-25 - Added explicit pre-Phase-4 yield and transition tasks

- opened P3.4 child issue `#29` for building and QAing the actual TFL 6
  natural/untreated VDYP and treated/managed BatchTIPSY yield curves before
  Phase 4 model-input bundle generation;
- opened P3.5 child issue `#30` for defining treatment options, eligibility
  filters, products/accounts/reporting hooks, and state-transition logic before
  Phase 4;
- shifted the run-profile/model-input contract update to P3.6 so it remains
  downstream of the AU/yield, curve-build, and transition-logic locks; and
- updated roadmap dependency text to make P3.3, P3.4, and P3.5 explicit
  prerequisites for P4.1.

## 2026-06-25 - Reordered Phase 3 around base model mechanics

- narrowed P3.5 / `#30` to treatment options and opened P3.6 / `#31` for
  state-transition logic;
- reordered Phase 3 so the execution stack is AU contract, yield curves,
  treatment options, transition logic, then cedar details and expansion
  options;
- moved the run-profile/model-input contract update to P3.7; and
- updated Current Next Steps so cedar and expansion remain open but paused
  until the base AU/yield/treatment/transition mechanics are locked.

## 2026-06-25 - Added embedded NICF/K3Z identity contract

- added `planning/tfl6_nicf_embedded_identity.md` to require the original
  K3Z/NICF core and expansion candidate areas to remain separately auditable
  inside the larger TFL 6 model;
- updated P3.2 / `#9` roadmap scope so embedded identity supports Patchworks
  group accounts, matching targets, scenario toggles, and reports;
- recorded that embedded NICF/K3Z and expansion-candidate identities are
  stand/group attributes, not AU identity fields; and
- kept P3.2 downstream of the base AU/yield/treatment/transition mechanics.

## 2026-06-25 - Added NICF/WFP stakeholder framing

- added `planning/tfl6_stakeholder_context.md` to record that NICF cedar and
  expansion interests should be modeled alongside WFP-facing fibre supply,
  fibre value, and delivered-cost implications;
- updated cedar planning so cedar reserve or cedar-priority scenarios must
  report broader TFL 6/WFP supply-chain tradeoffs where available;
- updated embedded identity planning so K3Z/NICF core and expansion candidate
  reports can be compared against whole-TFL and TFL 6 remainder outcomes; and
- updated roadmap text so P3.1 and P3.2 carry stakeholder-comparison reporting
  requirements into later model-input and Patchworks surfaces.

## 2026-06-25 - Clarified student-facing stakeholder KPI purpose

- expanded `planning/tfl6_stakeholder_context.md` so the purpose of student
  projects is explicitly framed as multi-perspective scenario tradeoff
  exploration using stakeholder-valued KPI proxies;
- added a `Multi-Perspective Scenario Tradeoffs` section to the Sphinx teaching
  challenges page; and
- updated Phase 3 and Phase 5 roadmap text so cedar, expansion, and final
  teaching docs carry the multi-perspective KPI interpretation requirement.

## 2026-06-25 - Locked the P3.3 AU and yield-curve assignment contract

- added a P3.3b accepted-contract lock to
  `planning/tfl6_au_yield_curve_contract.md`;
- accepted K3Z-style static AU identity while rejecting age, THLB status,
  operability, treatment eligibility, curve provenance, cedar, retention, and
  expansion fields as canonical AU identity fields;
- locked MP10 Tables 27-29 as TFL 6 TIPSY parameter evidence only, with legacy
  AU codes preserved as provenance/parameter keys;
- locked the natural/untreated VDYP curve lane to the shared FEMIC
  `smoothed_bin_pchip` default governed by `UBC-FRESH/femic#187`, with MKRF
  as evidence and TSA29 as adoption evidence;
- locked treated/managed curves to a reviewed TFL 6 BatchTIPSY parameter
  crosswalk; and
- marked P3.3 complete in `ROADMAP.md` and moved Current Next Steps to P3.4
  actual yield-curve build/QA without building model inputs or runtime files.

## 2026-06-25 - Extracted MP10 TIPSY parameter tables for P3.4a

- scraped MP10 Information Package Tables 27, 28, and 29 into reviewed planning
  artifacts under `planning/tfl6_mp10_tipsy_parameter_library.{md,json,csv}`;
- captured 90 legacy parameter rows: 60 from Table 27, 16 from Table 28, and
  14 from Table 29;
- preserved MP10 legacy AU codes, Table 29 footnote markers, age-band context,
  SPH, species percentages, species site indexes, genetic worth, OAF,
  utilization, regeneration-delay notes, THLB area evidence, and raw row text;
- recorded accepted extraction caveats, including dash normalization, Table 27
  genetic-worth handling, a repaired row-1221 text-extraction artifact, and
  small accepted THLB-area deltas against printed totals; and
- marked P3.4a complete in `ROADMAP.md` and moved Current Next Steps to P3.4b
  static-AU-to-MP10-parameter crosswalk planning without generating curves.

## 2026-06-25 - Compiled the first static AU review universe for P3.4b

- compiled a review-only static TFL 6 AU/stratum universe from accepted R1
  geometry and VDYP7 primary-layer attributes under
  `planning/tfl6_static_au_universe.{md,json,csv}`;
- wrote the stand-level review assignment table to
  `planning/tfl6_stand_to_au_review.csv` and the top-strata summary to
  `planning/tfl6_static_au_top_strata.csv`;
- generated the standard FEMIC strata distribution diagnostic at
  `plots/strata-tfl6.{png,pdf}` using
  `femic.pipeline.plots.render_strata_distribution_plot`, matching the K3Z and
  MKRF instance plot specification, with the SI axis widened to `0-55` for the
  high-productivity TFL 6 coastal rainforest source data;
- recorded 17,223 yieldable review rows, 174 static strata, 26 selected
  top-area strata covering 90.397% of the yieldable review area, 384 total
  review AU bins, and 77 selected top-area AU bins;
- kept AU identity limited to BEC/subzone/variant/phase group, top-two species
  combo, and L/M/H site-index review class, without encoding THLB,
  operability, treatment eligibility, cedar, retention, or NICF expansion
  state; and
- marked P3.4b complete in `ROADMAP.md` and moved Current Next Steps to P3.4c
  MP10 TIPSY parameter crosswalk work without writing the model-input bundle or
  generating curves.

## 2026-06-25 - Crosswalked static TFL 6 AUs to MP10 TIPSY rows for P3.4c

- added the P3.4c planning crosswalk under
  `planning/tfl6_tipsy_parameter_crosswalk.{md,json,csv}`;
- matched each of the `384` refined static TFL 6 AU bins to three MP10 TIPSY
  parameter lanes: existing managed stands aged 11-50, existing managed stands
  aged 1-10, and future managed stands;
- produced `1,152` crosswalk rows, including separate confidence flags,
  species-share distance, weighted-SI difference, zero-padded MP10 legacy AU
  codes, and non-numeric `mp10_au_####` provenance keys;
- recorded selected top-area AU confidence counts by lane: for
  existing-managed 11-50, `34` high, `23` medium, `8` low, and `12` fallback;
  for existing-managed 1-10, `19` high, `32` medium, `15` low, and `11`
  fallback; and for future-managed, `11` high, `36` medium, `19` low, and `11`
  fallback;
- kept low-confidence and fallback rows explicit for maintainer review before
  executable BatchTIPSY use; and
- marked P3.4c complete in `ROADMAP.md` and moved Current Next Steps to P3.4d
  natural/untreated VDYP curve generation and QA without writing the
  model-input bundle.

## 2026-06-25 - Planned the P3.4d natural VDYP curve-generation run

- added `planning/tfl6_vdyp_curve_generation_plan.md` to define the bounded
  P3.4d execution path for natural/untreated VDYP curve generation;
- confirmed the shared selector authority is
  `femic.pipeline.au_first_growth.select_au_first_growth_curve` with the
  `smoothed_bin_pchip` path governed by parent FEMIC issue `#187`;
- recorded that the current TFL 6 instance has accepted R1 geometry, VDYP7
  source attribute parquet files, the static AU universe, and the stand-to-AU
  review table, but does not yet have the stand-level
  `FEATURE_ID`/`PRJ_TOTAL_AGE`/`PRJ_VOL_DWB` VDYP yield time-series required by
  the first-growth selector;
- defined review-only output paths under `planning/` and `plots/`, explicitly
  keeping P3.4d out of `data/model_input_bundle/`;
- listed QA gates for missing-curve rationales, sparse-support diagnostics,
  L/M/H envelope plots, fit diagnostics, and Patchworks semantics guardrails;
  and
- updated `ROADMAP.md` Current Next Steps so the next bounded P3.4d move is to
  materialize or adapt the stand-level VDYP yield time-series before fitting
  natural curves.

## 2026-06-25 - Re-centered P3.4d on the standard FEMIC Stage 01a VDYP lane

- removed the instance-local VDYP materializer draft and re-centered P3.4d on
  the established FEMIC Stage 01a workflow used by K3Z, TSA29, and MKRF:
  `femic prep validate-case` followed by `femic run`;
- renamed the active runtime profile and TIPSY/silviculture configs from the
  stale NICF FSP code to TFL6 (`config/run_profile.tfl6.yaml`,
  `config/tipsy/tfl6.yaml`, and `config/silviculture.tfl6.yaml`);
- updated `config/rebuild.spec.yaml`, `QUICKSTART.md`, `AGENTS.md`, and the
  rebuild runbook to use the TFL6 run profile and `--tsa tfl6` handoff code;
- kept `runtime/` ignored so Stage 01a scratch/log output does not become a
  tracked planning artifact; and
- updated `planning/tfl6_vdyp_curve_generation_plan.md` and `ROADMAP.md` so the
  next P3.4d move is to validate `config/run_profile.tfl6.yaml`, then run the
  standard `femic run --run-config config/run_profile.tfl6.yaml --run-id
  tfl6_stage01a` lane and inspect its VDYP curve/log artifacts.

## 2026-06-25 - Ran P3.4d AFLB feature-ID VDYP first-growth curves

- ran VDYP against the AU-assigned TFL 6 AFLB feature IDs from
  `planning/tfl6_stand_to_au_review.csv` using the clipped 2025 VDYP polygon
  and layer parquet inputs under `data/input/tfl_6/`;
- generated `3,220,953` stand-level VDYP yield rows for `16,659` of the
  `17,223` AU-assigned AFLB feature IDs;
- promoted review artifacts to `planning/tfl6_first_growth_au_curves.csv`,
  `planning/tfl6_first_growth_au_fit_diagnostics.csv`, and
  `planning/tfl6_first_growth_vdyp_run_summary.md`;
- produced `276` raw accepted AU natural/untreated first-growth curve
  candidates using the shared `smoothed_bin_pchip` selector and flagged `104`
  raw AUs as insufficient-source candidates, while retaining only the selected
  top-area AU set as canonical curve families for publication/review; and
- kept the large stand-level VDYP yield time series and VDYP run logs under
  ignored `runtime/derived/p3_4_aflb_vdyp_first_growth_run2/` for local audit
  and did not write Phase 4 model-input bundle outputs.

## 2026-06-25 - Added AU-wise first-growth curve review plots

- added `scripts/build_p3_4_first_growth_plots.py` to regenerate the TFL 6
  natural/untreated first-growth review plots from the P3.4d VDYP run outputs;
- generated `26` `plots/vdyp_lmh_tfl6-*.png` selected-AU-family comparison
  plots using the same L/M/H visual review pattern as the other FEMIC instance
  examples;
- generated `77` `plots/vdyp_fitdiag_tfl6-*.png` selected-AU fit-diagnostic
  plots with raw VDYP curves, 5-year observed medians/interquartile bands,
  selected fits, and residual panels;
- wrote `planning/tfl6_first_growth_plot_manifest.{csv,md}` with repo-relative
  plot paths for review and downstream documentation; and
- updated `planning/tfl6_first_growth_vdyp_run_summary.md` and `ROADMAP.md` so
  P3.4d explicitly references the AU-wise plot artifacts while keeping
  treated/managed TIPSY curves and Phase 4 model-input bundle generation out of
  this slice.

## 2026-06-25 - Added P3.4f first-growth curve shape diagnostics

- added `scripts/build_p3_4_first_growth_shape_diagnostics.py` to classify
  selected-AU natural/untreated first-growth curve shapes before changing the
  accepted P3.4d curve table;
- wrote `planning/tfl6_first_growth_shape_diagnostics.{csv,md}` with one row
  per selected top-area AU diagnostic case;
- confirmed the selected curve set has `77` accepted curves, no
  insufficient-source selected AUs, no critical selected curves, `45` review
  rows, and `32` OK rows;
- added `scripts/build_p3_4_first_growth_au_remap_audit.py` and
  `planning/tfl6_first_growth_au_remap_audit.{csv,md}` to map `307`
  non-selected AU bins onto the `77` selected canonical curve families using
  FEMIC's established lexicographic stratum-name matching pattern; and
- updated `ROADMAP.md` so P3.4f explicitly covers selected-set
  shape-pathology review and remap QA before any smoothing/tail-cleanup
  parameter changes are locked.

## 2026-06-26 - Deferred optional VDYP smoothing cleanup after P3.4f review

- updated `ROADMAP.md` to mark P3.4f complete and record that the selected
  top-area VDYP first-growth curves are good enough to proceed with the rest of
  Phase 3;
- kept the `45` selected-set review flags visible in
  `planning/tfl6_first_growth_shape_diagnostics.md`, but reframed smoothing,
  tail-constraint, and L/M/H ordering cleanup as an optional pre-bundle revisit
  rather than a blocker for P3.4e, P3.5, or P3.6; and
- left the selected canonical curve set at `77` AU bins with `26` L/M/H review
  panels and the `307` non-selected AU remaps documented in
  `planning/tfl6_first_growth_au_remap_audit.{csv,md}`.

## 2026-06-26 - Built the P3.4e TFL 6 BatchTIPSY handoff

- added `scripts/build_p3_4e_tipsy_handoff.py` to convert the selected
  top-area AU/MP10 TIPSY crosswalk into an executable BTC input handoff;
- wrote `data/03_input-tfl6.csv` with `231` rows: `77` selected AU bins across
  the three managed lanes `existing_managed_11_50`, `existing_managed_1_10`,
  and `future_managed`;
- wrote `planning/tfl6_tipsy_btc_curve_id_map.csv` plus
  `planning/tfl6_tipsy_btc_handoff_manifest.{json,md}` so synthetic BTC
  feature IDs, OAF conversion, regen-delay defaults, confidence counts, and
  the `9` MP10 `other`-species rows encoded as `Dr` remain reviewable; and
- updated `ROADMAP.md` so P3.4e1 is complete while P3.4e2 remains the next
  bounded step: run BTC/BatchTIPSY from `data/03_input-tfl6.csv`, parse
  `04_output-tfl6.csv`, and generate treated/managed curve QA overlays.

## 2026-06-26 - Ran and QAed P3.4e treated/managed BatchTIPSY curves

- ran BTC/BatchTIPSY from the TFL 6 handoff `data/03_input-tfl6.csv` and wrote
  the cleaned output `data/04_output-tfl6.csv` plus `data/04_error-tfl6.csv`;
- fixed the P3.4e handoff builder so MP10 `other` species rows encoded as `Dr`
  use the static TFL 6 AU mean SI when the matched MP10 row has no usable
  deciduous/other SI value, removing the initial BTC `Dr` site-index errors;
- added `scripts/build_p3_4e_tipsy_qa.py`, parsed `8316` treated-curve rows to
  `planning/tfl6_tipsy_managed_curves.csv`, and wrote
  `planning/tfl6_tipsy_managed_curve_diagnostics.{csv,md}`;
- generated `77` treated-vs-natural overlay plots with the manifest in
  `planning/tfl6_tipsy_vdyp_overlay_manifest.{csv,md}`;
- recorded that the cleaned BTC error file has `0` error rows and complete
  coverage of the `231` selected AU/lane handoff rows; and
- marked P3.4 complete in `ROADMAP.md`, with the remaining treated-curve caveat
  limited to small fallback `CWHvm1_DR` rows that show high treated-to-natural
  max-volume ratios and should remain visible during later bundle QA.

## 2026-06-26 - Published Phase 3 AU and yield-curve docs

- added `docs/phase3-au-yield-curves.rst` and linked it from
  `docs/index.rst` so students and maintainers can find the Phase 3 AU
  definition contract, strata diagnostic, natural VDYP plots, and
  treated TIPSY-vs-VDYP overlays from the standalone docs;
- added `scripts/build_docs_phase3_au_yield_curves.py` to regenerate the docs
  gallery from checked-in plot artifacts;
- documented the accepted static AU policy, the `174` static strata, `26`
  selected top-area strata, `384` total AU bins, and `77` selected AU bins;
- surfaced the `plots/strata-tfl6.png` diagnostic, `26`
  `vdyp_lmh_tfl6-*.png` panels, `77` `vdyp_fitdiag_tfl6-*.png` panels, and
  `77` `tipsy_vdyp_tfl6-*.png` treated-overlay panels; and
- kept the optional VDYP smoothing revisit and small fallback `CWHvm1_DR`
  treated-curve caveats visible in the docs before P3.5 treatment-option work.

## 2026-06-26 - Locked the P3.5 treatment-option vocabulary

- added `planning/tfl6_treatment_option_contract.md` to define the first TFL 6
  treatment catalogue, eligibility filters, product/account/reporting hooks,
  and deferred treatment blockers before transition logic;
- updated `config/silviculture.tfl6.yaml` from the copied scaffold into a
  TFL 6 planning contract while keeping legacy FEMIC CT/PCT/fertilization knobs
  disabled until a later implementation lane explicitly activates them;
- accepted `cc` as the only base scheduled treatment, `grow` as implicit state
  behavior, `regen_plant` as the default managed post-harvest transition
  target, and `regen_natural` as a deferred/fallback transition target; and
- recorded that managed/unmanaged treatment eligibility remains separate from
  natural/treated curve provenance, with cedar and NICF expansion treatment
  details deferred behind P3.1/P3.2 review blockers.

## 2026-06-26 - Refined P3.5 treatment scope for NICF-focused CT/fertilization

- revised the P3.5 treatment contract so the only whole-TFL 6 base scheduled
  treatment is `clearcut_and_plant`, combining harvest and planted
  regeneration into the base treatment vocabulary consumed by P3.6;
- updated `config/silviculture.tfl6.yaml` to replace the separate `cc` and
  `regen_plant` planning entries with `clearcut_and_plant`; and
- retained CT and fertilization as group-gated scenario treatments eligible
  only inside the K3Z/NICF core block and future accepted NICF expansion
  blocks, with response, residual-state, transition, product, and account
  blockers still requiring review before activation.

## 2026-06-26 - Added TFL-wide harvest-system classes to P3.5

- updated the P3.5 treatment contract so ground-based, cable-yarding, and
  heli-logging systems are explicit stand-level operational attributes carried
  throughout the TFL 6 AOI;
- added harvest-system eligibility and reporting hooks to
  `config/silviculture.tfl6.yaml`; and
- recorded that harvest system affects treatment eligibility, delivered-cost
  proxies, scenario controls, and teaching reports, but is not part of AU
  identity and does not create separate yield-curve families by itself.

## 2026-06-26 - Added P3.6a state-class contract

- added `planning/tfl6_state_transition_contract.md` with the first TFL 6
  state-class contract for initial managed/unmanaged natural/treated states,
  retained/unmanaged states, post-clearcut planted state, NICF-focused CT/fert
  candidate states, and deferred special teaching states;
- locked the semantic field separation for P3.6/P4: `IFM` is treatment
  eligibility, `ORIGIN` is curve provenance, `SILV_STATE` is the state path,
  `RETENTION` is retention status/fraction, `HARVEST_SYSTEM` carries
  ground/cable/heli operational class, and `TFL6_GROUP` carries reporting
  identity; and
- updated `ROADMAP.md` so P3.6a is complete and P3.6b is the next bounded
  tranche for transition-row definitions without starting Phase 4.

## 2026-06-26 - Added P3.6b transition-row contract

- extended `planning/tfl6_state_transition_contract.md` with reviewed
  transition rows for grow/no-action behavior, `clearcut_and_plant`, retained
  or unmanaged movement, operability masking, origin-provenance handling,
  K3Z/NICF-gated CT/fertilization hooks, and cedar/expansion hook points;
- recorded that `clearcut_and_plant` is the only accepted base transition that
  changes `ORIGIN`, moving harvested managed stands to the treated/managed
  BatchTIPSY curve lane after planted regeneration; and
- marked P3.6b complete in `ROADMAP.md`, leaving P3.6c as the next bounded
  verification step before any Phase 4 model-input generation.

## 2026-06-26 - Verified P3.6c treatment-semantics consistency

- added a P3.6c verification table to
  `planning/tfl6_state_transition_contract.md` comparing transition rows
  against the P3.5 treatment vocabulary;
- confirmed that transition rows use only accepted P3.5 treatment IDs/triggers,
  keep `clearcut_and_plant` as the only whole-TFL 6 base scheduled treatment,
  retain CT/fertilization as K3Z/NICF-gated hooks, preserve `IFM` as treatment
  eligibility and `ORIGIN` as curve provenance, and keep harvest system as
  operational/reporting context; and
- marked P3.6c complete in `ROADMAP.md`, leaving P3.6d cedar/expansion hook
  point recording as the next bounded tranche.

## 2026-06-26 - Recorded P3.6d cedar and expansion hook points

- extended `planning/tfl6_state_transition_contract.md` with P3.6d cedar hook
  fields that preserve P3.1 cedar signals through grow, harvest, retention,
  and operability transitions without creating cedar-specific base treatments
  or AU identities;
- added embedded NICF/K3Z and expansion-candidate hook fields from P3.2 so
  Phase 4 can carry group identities, candidate pools, screen status, and
  scenario-group fields through transition/account/report surfaces; and
- marked P3.6d complete in `ROADMAP.md`, leaving P3.6e deferred-transition
  blocker lock as the next bounded tranche.

## 2026-06-26 - Locked P3.6e deferred transition semantics

- expanded `planning/tfl6_state_transition_contract.md` with the P3.6e
  deferred-transition lock for CT residual-state transitions, fertilization
  response transitions, cedar-specific transitions, NICF expansion scenario
  transitions, harvest-system reassignment, operability state movement,
  natural-regeneration alternatives, and cedar/cultural reserve scenario
  exclusions;
- recorded the current base behavior, blocker/review need, and owner lane for
  each deferred transition item; and
- marked P3.6 and P3.6e complete in `ROADMAP.md`, leaving the remaining Phase
  3 design work to P3.1 cedar source-field/signal review, P3.2 embedded
  K3Z/NICF identity, and P3.7 run-profile/model-input contract reconciliation.

## 2026-06-26 - Locked P3.1b cedar source fields and signals

- updated `planning/tfl6_cedar_signal_design.md` to lock cedar source fields
  against the accepted `planning/tfl6_stand_to_au_review.csv` surface, using
  `species_cd_1..6`, `species_pct_1..6`, age proxy fields, BEC/reporting
  fields, and AU/yield support fields without adding cedar to AU identity;
- accepted `CW` and `YC` leading/component cedar signals, the first
  `cedar_present >= 20%` threshold, and the `old_cedar >= 141` age proxy, with
  gross review diagnostics for cedar-leading, cedar-present, and old-cedar
  area; and
- marked P3.1b complete in `ROADMAP.md`, leaving P3.1c as the next bounded
  cedar design tranche for Patchworks-facing cedar products, accounts,
  treatment hooks, stakeholder-comparison signals, and report requirements.

## 2026-06-26 - Closed P3.1 cedar Patchworks-facing design

- extended `planning/tfl6_cedar_signal_design.md` with the P3.1c
  Patchworks-facing contract for cedar product hooks, feature/account families,
  report/target families, treatment-hook boundaries, yield-curve boundaries,
  and Phase 4 cedar handoff fields;
- accepted generic cedar/CW/YC reporting products and account/report surfaces
  while keeping utility-pole grade, cedar-specific base treatments, hard cedar
  reserve targets, and cedar-only yield-curve families deferred; and
- marked P3.1 and P3.1c complete in `ROADMAP.md`, moving the next bounded
  Phase 3 tranche to P3.2b embedded K3Z/NICF core AOI overlay identity.

## 2026-06-26 - Locked P3.2b K3Z/NICF core overlay identity

- updated `planning/tfl6_nicf_embedded_identity.md` to distinguish the original
  K3Z tenure source from the broader pre-pivot FDU 1/2/3 FSP planning context
  and from the active current TFL 6 AOI;
- recorded non-mutating EPSG:3005 overlay diagnostics showing the K3Z tenure
  is `2391.511 ha`, but only `0.072 ha` intersects the current FADM-derived
  TFL 6 AOI, so the first bundle must not silently label broad current-AOI
  stands as `nicf_k3z_core`; and
- marked P3.2b complete in `ROADMAP.md`, leaving P3.2c as the next bounded
  identity-contract tranche for expansion candidate, rejected-candidate, and
  TFL 6 remainder classes.

## 2026-06-26 - Locked P3.2c expansion and remainder identity classes

- extended `planning/tfl6_nicf_embedded_identity.md` with accepted
  `embedded_area_class` values for `wfp_tfl6_remainder`,
  `nicf_expansion_candidate`, `nicf_expansion_rejected`,
  `nicf_expansion_pool_unreviewed`, and `nicf_k3z_core_reference`;
- defined candidate-area pool semantics, source/provenance fields, and the
  first `expansion_screen_status` vocabulary without materializing candidate
  geometry or executing screening logic; and
- marked P3.2c complete in `ROADMAP.md`, leaving P3.2d as the next bounded
  tranche for Patchworks group accounts, matching targets, scenario toggles,
  and reports.

## 2026-06-26 - Corrected P3.2c expansion geography

- corrected `planning/tfl6_nicf_embedded_identity.md` so expansion candidates
  come from proximal/adjacent public forested land outside the current TFL 6
  AOI rather than from inside current-AOI TFL 6 stands;
- updated candidate/rejected/unreviewed class semantics, source/provenance
  fields, and screen-status vocabulary to include outside-AOI source
  membership, public-land/tenure availability, external THLB-equivalent
  eligibility, and proximity/adjacency review; and
- updated `ROADMAP.md` while preserving the boundary that no expansion
  geometry, screening execution, model-input bundle, XML, Matrix Builder, or
  runtime-package work starts in P3.2c.

## 2026-06-26 - Locked P3.2d Patchworks comparison surfaces

- extended `planning/tfl6_nicf_embedded_identity.md` with the P3.2d
  Patchworks-facing contract for embedded-area group dimensions, account
  families, matching targets, scenario toggles, and reports;
- required separate reporting for current-AOI WFP/TFL 6 remainder,
  K3Z/NICF reference identity, outside-AOI expansion candidates,
  rejected/unreviewed expansion pools, and whole-model teaching comparisons;
- defined WFP-facing fibre-supply, delivered-cost proxy, harvest-system,
  cedar/community, K3Z-continuity, and rejected-pool audit report families
  without creating hard base targets or schedulable rejected/unreviewed pools;
  and
- marked P3.2d complete in `ROADMAP.md`, leaving P3.2e as the next bounded
  handoff tranche before P3.2 can close.

## 2026-06-26 - Documented Phase 3 cedar and embedded NICF design

- added `docs/phase3-cedar-nicf-expansion.rst` to summarize P3.1 cedar
  signals, cedar product/account boundaries, P3.2 K3Z/NICF reference identity,
  outside-AOI expansion candidate classes, Patchworks comparison surfaces, and
  scenario toggles for students and maintainers;
- added the new page to the Sphinx toctree in `docs/index.rst`;
- updated `docs/teaching-challenges.rst` so outside-AOI NICF expansion source
  lands are clearly separated from current-AOI TFL 6 base geography; and
- rebuilt the instance Sphinx docs with warnings treated as errors.

## 2026-06-26 - Closed P3.2 embedded identity handoff

- added a P3.2e handoff section to
  `planning/tfl6_nicf_embedded_identity.md` defining the embedded identity
  fields that P3.7/P4.1 must carry into the run-profile and model-input
  contract;
- locked dependency boundaries showing that embedded identity may split
  accounts, targets, toggles, reports, treatment gates, harvest-system
  summaries, cedar outputs, and THLB-equivalent summaries, but must not become
  an AU key, curve-family key, or hidden THLB deduction;
- updated `docs/phase3-cedar-nicf-expansion.rst` with the P3.2e handoff field
  list for student and maintainer visibility; and
- marked P3.2e and P3.2 complete in `ROADMAP.md`, moving the next bounded
  Phase 3 tranche to P3.7 run-profile/model-input contract reconciliation.

## 2026-06-26 - Started P3.7 model-input contract reconciliation

- opened P3.7 child issue `#32` and linked it from `ROADMAP.md`;
- added `planning/tfl6_model_input_contract.md` to collect accepted Phase 2/3
  artifacts, required model-input field families, Phase 4 QA checks, and
  rejected/deferred assumptions before bundle generation starts;
- updated `config/run_profile.tfl6.yaml` with Phase 3 contract metadata,
  accepted artifact paths, required field families, and explicit P3.7
  non-goals;
- updated `config/tipsy/tfl6.yaml` so the reviewed P3.4 BTC handoff and
  managed-curve artifacts supersede the bootstrap fallback rule metadata; and
- added `docs/phase3-model-input-contract.rst` to the Sphinx toctree.

## 2026-06-26 - Locked P3.7 model-input contract

- marked P3.7 and its subtasks complete in `ROADMAP.md`, moving the next
  bounded tranche to Phase 3 closeout rather than Phase 4 implementation;
- recorded the P3.7 validation state in
  `planning/tfl6_model_input_contract.md`: YAML parsing and warning-clean
  Sphinx passed, while full `femic prep validate-case` remains blocked by
  local Arbutus/DataLad public-data materialization and auth state;
- preserved the Phase 4 boundary that no model-input bundle, outside-AOI
  expansion screening, ForestModel XML, Matrix Builder output, or runtime
  package is generated inside P3.7; and
- prepared issue `#32` and Phase 3 parent `#13` for final P3.7 status
  synchronization.

## 2026-06-26 - Closed Phase 3 model-design assumptions

- updated `planning/tfl6_model_input_contract.md` and `ROADMAP.md` to record
  that `femic prep validate-case` passes after loading the local Arbutus
  environment and materializing/unlocking the required public-data
  `FADM_TSA.gdb` payload;
- verified that Phase 3 child issues `#8`, `#9`, and `#28` through `#32` are
  closed and that Phase 3 parent issue `#13` has all child acceptance criteria
  complete;
- preserved the boundary that Phase 4 model-input generation, outside-AOI
  expansion screening, ForestModel XML, Matrix Builder, and runtime-package work
  have not started; and
- prepared the `feature/p3-model-design-assumptions` branch for the instance
  PR/merge workflow.

## 2026-06-26 - Added standalone docs publication workflow

- added `.github/workflows/docs-pages.yml` so the TFL 6 instance repository can
  publish its Sphinx docs to GitHub Pages;
- added `docs/requirements.txt` with the minimal Sphinx build dependency for
  the Pages workflow;
- marked P5.3a as complete in `ROADMAP.md` while keeping P5.3 and issue `#21`
  open for the later full teaching-docs expansion after Phase 4 runtime
  package evidence exists; and
- preserved the boundary that this publishes the current Phase 2/Phase 3 seed
  docs only and does not start Phase 4 model-input or runtime-package work.

## 2026-06-26 - Switched standalone docs to RTD theme

- updated `docs/conf.py` to use the same `sphinx_rtd_theme` configuration
  pattern as the K3Z and MKRF instance docs, with an Alabaster fallback only if
  the RTD theme package is unavailable;
- updated `docs/requirements.txt` to install `sphinx-rtd-theme`; and
- preserved the existing warning-clean Sphinx build and GitHub Pages
  publication workflow.

## 2026-06-26 - Started Phase 4 model-input bundle lane

- created the `feature/p4-model-input-bundle` branch from merged instance
  `main`;
- changed Phase 4 from proposed to active in `ROADMAP.md`;
- decomposed P4.1 / `#17` into prerequisite-manifest, bundle-path,
  first-bundle-build, and lightweight-QA subtasks; and
- moved the current executable edge to P4.1a while preserving the boundary that
  no ForestModel XML, Matrix Builder, or Patchworks runtime-package work starts
  inside the first model-input bundle slice.

## 2026-06-26 - Recorded P4.1a model-input prerequisites

- added `planning/tfl6_model_input_bundle_prerequisite_manifest.md` and
  `planning/tfl6_model_input_bundle_prerequisite_manifest.json` to inventory
  the accepted Phase 2/3 inputs for the first TFL 6 model-input bundle;
- confirmed the accepted run profile, clipped 2025 R1/VDYP inputs, THLB audit
  and status files, AU/curve tables, BatchTIPSY outputs, treatment and
  transition contracts, cedar contract, and embedded-identity contract are
  present in the current checkout;
- recorded the Phase 4 checkpoint availability gap: the generated
  `data/tsr/*checkpoint*` THLB checkpoint files referenced by the Phase 2
  status report are not present in the clean checkout and must be
  rematerialized, regenerated, or explicitly waived before P4.1c consumes final
  THLB geometry; and
- moved the current executable edge to P4.1b, preserving the boundary that no
  model-input bundle, ForestModel/XML, Matrix Builder output, or Patchworks
  runtime package was generated in P4.1a.

## 2026-06-26 - Defined P4.1b model-input bundle paths

- added `planning/tfl6_model_input_bundle_path_contract.md` and
  `planning/tfl6_model_input_bundle_path_contract.json` to define generated
  bundle paths and artifact roles before any model-input outputs are written;
- kept the cross-instance FEMIC convention that generated bundle tables live
  under `data/model_input_bundle/`, including `au_table.csv`,
  `curve_table.csv`, and `curve_points_table.csv`;
- reserved
  `data/model_input_bundle/input_geometry/thlb_current.feather`,
  `data/model_input_bundle/input_geometry/thlb_current.gpkg`, and
  `data/model_input_bundle/input_geometry/thlb_checkpoint_manifest.json` as
  the stable P4 input geometry handoff for regenerated or rematerialized final
  THLB geometry; and
- moved the current executable edge to P4.1c while preserving the boundary that
  P4.1b did not create `data/model_input_bundle/`, write bundle tables,
  generate ForestModel/XML, run Matrix Builder, or assemble a Patchworks
  runtime package.

## 2026-06-26 - Regenerated P4.1c THLB geometry handoff

- regenerated the final TFL 6 THLB geometry handoff from the accepted clipped
  2025 R1 VRI input and reviewed THLB recipe into
  `data/model_input_bundle/input_geometry/thlb_current.feather`;
- wrote the matching GeoPackage mirror and checkpoint manifest under
  `data/model_input_bundle/input_geometry/`;
- inspected both geometry formats and confirmed `29892` EPSG:3005
  `MultiPolygon` rows with weighted `thlb_fact` THLB area of
  `144203.485 ha`, matching the accepted Phase 2 benchmark;
- added `planning/tfl6_model_input_bundle_geometry_handoff.md` to preserve the
  command, artifact paths, inspection metrics, and fractional `thlb_fact`
  interpretation; and
- kept P4.1c open because no model-input bundle tables, ForestModel XML,
  Matrix Builder outputs, or Patchworks runtime package were generated in this
  handoff pass.

## 2026-06-26 - Clarified AFLB universe versus THLB managed-share contract

- amended instance model-input docs and planning metadata to state that the
  Patchworks stand universe is AFLB, not THLB area alone;
- documented that THLB is the managed subset of AFLB and that
  `NTHLB = AFLB - THLB` remains in the model as unmanaged/full-retention forest
  requiring untreated VDYP growth curves;
- updated the P4.1 bundle path contract so `aflb_current` is the future
  resultant-fragment handoff and `thlb_current` is the managed-share state
  surface used for `managed_share`, `thlb_fact`, `thlb_area_ha`, and
  `retention_share`; and
- kept P4.1c.2 open because this was a documentation/metadata correction only,
  with no bundle table generation, ForestModel XML, Matrix Builder output, or
  Patchworks runtime package.

## 2026-06-26 - Refined Patchworks resultant-fragment wording

- amended instance model-input docs and bundle-path metadata to state that
  accepted spatial netdown overlays intentionally produce AFLB resultant
  fragments for Patchworks;
- clarified that final THLB/NTHLB state is assigned to those resultant
  fragments rather than being a separate stand universe or an error condition;
  and
- kept P4.1c.2 open for actual core bundle-table generation from the AFLB
  resultant-fragment universe.

## 2026-06-26 - Materialized the AFLB resultant-fragment handoff

- rematerialized the accepted AFLB LU partition checkpoint into generated
  `data/model_input_bundle/input_geometry/aflb_current.feather` and
  `aflb_current.gpkg`;
- wrote `aflb_checkpoint_manifest.json` beside the generated geometry handoff;
- inspected the generated handoff and confirmed `26186` EPSG:3005
  `MultiPolygon` resultant-fragment rows, `196833.177 ha`, and zero
  null/empty/invalid geometries; and
- kept P4.1c.2 open because bundle CSV tables, ForestModel XML, Matrix Builder
  outputs, and Patchworks runtime packaging are still pending.

## 2026-06-26 - Invalidated the attempted AFLB handoff

- stopped P4.1c.2 bundle generation after direct inspection showed that the
  runner-labeled `aflb_checkpoint.6a351f3a223a` still contains non-treed and
  non-forested BCLCS rows;
- removed the generated `aflb_current.feather`, `aflb_current.gpkg`, and
  `aflb_checkpoint_manifest.json` outputs so downstream bundle code cannot use
  the invalid handoff accidentally;
- recorded that the GLB-to-AFLB non-forest/non-productive filter is too
  permissive for the Patchworks stand universe; and
- blocked core bundle CSV generation until the GLB-to-AFLB lane is corrected
  and rerun.

## 2026-06-26 - Repaired P4.1c GLB-to-AFLB filter and regenerated handoffs

- opened P4.1c blocker issue `#36` and linked it to Phase 4 parent `#14` and
  active model-input bundle issue `#17`;
- corrected `tfl6_nd_010_non_forest` so the executable rule removes BCLCS
  level 1 non-treed/unclassified rows as well as BCLCS level 2
  non-vegetated, water, or unreported rows, while keeping
  `for_mgmt_land_base_ind == N` as QA evidence only;
- reran the reconstructed THLB netdown from
  `data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg`;
- promoted the corrected AFLB handoff to
  `data/model_input_bundle/input_geometry/aflb_current.feather` and
  `aflb_current.gpkg`, with `25019` rows, `191168.597 ha`, zero invalid
  geometries, and `0.000 ha` of `bclcs_level_1 in {N, U}` contamination;
- regenerated the THLB handoff with weighted `thlb_fact` area
  `139995.798 ha`, `2.57%` above the scaled current-AOI benchmark and inside
  the accepted teaching tolerance; and
- marked P4.1c.2a complete in `ROADMAP.md`, leaving P4.1c.2 open for core
  model-input bundle CSV generation from the corrected AFLB/THLB handoff.

## 2026-06-26 - Generated P4.1c.2 core model-input bundle tables

- generated the first core model-input bundle tables under ignored
  `data/model_input_bundle/` output space from the corrected AFLB/THLB handoffs;
- recorded the tracked audit trail in
  `planning/tfl6_model_input_bundle_core_tables.md`;
- confirmed the generated bundle has `25019` AFLB stand rows,
  `191168.597 ha` AFLB, `139995.798 ha` THLB, and `51172.799 ha` NTHLB;
- confirmed all stand rows have non-null natural and treated curve assignments,
  including `136` rows / `749.396 ha` that use warning-only sparse TIPSY curve
  fallback; and
- kept ForestModel XML, Matrix Builder, Patchworks runtime packaging, and
  publication out of scope. P4.1d lightweight bundle QA is the next gate, with
  harvest-system assignment still explicitly deferred as
  `unassigned_review_required`.

## 2026-06-26 - Completed P4.1d model-input bundle QA

- added `planning/tfl6_model_input_bundle_qa.md` as the tracked QA audit for
  the first generated model-input bundle;
- confirmed required generated tables are readable, stand IDs are unique, area
  reconciliation passes, and all AU, natural-curve, and treated-curve mappings
  are non-null;
- confirmed every stand-level curve ID exists in `curve_table.csv`, every curve
  has point rows, cedar/embedded/harvest-system support tables match the stand
  count, and the bundle keeps the AFLB stand universe separate from THLB/NTHLB
  managed-share state;
- accepted warning-only gates for `136` sparse treated-curve fallback rows and
  deferred harvest-system assignment as `unassigned_review_required` for all
  stands; and
- marked P4.1 complete while keeping ForestModel XML, Matrix Builder,
  Patchworks runtime packaging, and publication out of scope. P4.2 is the next
  executable Phase 4 task.

## 2026-06-26 - Recorded first P4.2 ForestModel XML export blocker

- opened P4.2 child issue `#37` and linked it under Phase 4 parent `#14`;
- attempted the bounded `femic export patchworks --tsa tfl6` command against
  the refreshed P4.1 bundle and corrected AFLB checkpoint;
- confirmed the exporter failed before writing a usable XML package with
  `au_table.csv missing required column: tsa`;
- inspected the FMG adapter contract and recorded that the blocker is broader
  than one missing column because the current exporter expects legacy numeric
  AU/curve IDs, `si_level`, and `curve_points_table` columns `x`/`y`, while the
  reviewed TFL6 bundle uses string AU/curve IDs and audit-oriented columns; and
- added `planning/tfl6_forestmodel_xml_export_blocker.md` to preserve the
  command, error, root cause, and next targeted repair. No ForestModel XML,
  fragments, Matrix Builder output, Patchworks runtime package, or publication
  artifact was generated.

## 2026-06-26 - Built P4.2 exporter compatibility bridge and found treatment blocker

- generated an ignored exporter-compatible schema bridge under
  `data/model_input_bundle/export_compat/`, including numeric AU/curve tables,
  an ID crosswalk, a compatibility AFLB checkpoint, and a bridge manifest;
- preserved reviewed TFL6 bundle tables unchanged while mapping string AU and
  curve IDs to deterministic numeric IDs required by the current generic FMG
  exporter;
- reran `femic export patchworks --tsa tfl6` against the compatibility bridge
  and generated ignored `output/patchworks_tfl6_validated/forestmodel.xml` plus
  fragments sidecars;
- inspected the generated outputs and confirmed `373` XML curves, `2442`
  selects, `24879` fragments, `191168.566 ha` exported fragment area, `407`
  fragment AUs, and proportional IFM/RETENTION values derived from reviewed
  managed-share state; and
- recorded `planning/tfl6_forestmodel_xml_export_bridge.md` with the remaining
  semantic blocker: XML currently emits `814` `CC` treatment nodes even though
  harvest-system assignment is deferred and final clearcut-and-plant
  eligibility is blocked. Matrix Builder and runtime work remain blocked until
  P4.2 preserves that treatment-ineligibility state in XML.

## 2026-06-26 - Accepted generic clearcut treatment for first TFL6 XML

- updated the P4.2 interpretation so the `814` emitted `CC` treatment nodes are
  accepted as a generic Phase 4 clearcut-and-plant treatment lane rather than a
  blocker;
- preserved ground/cable/heli harvest-system assignment as a deferred
  operability, delivered-cost, and reporting refinement for later work after
  DEM and stand-inventory parsing logic is reviewed;
- marked P4.2 complete in `ROADMAP.md` and moved the next executable Phase 4
  lane to P4.3 Matrix Builder and track/account QA against the generated
  XML/fragments; and
- updated `planning/tfl6_forestmodel_xml_export_bridge.md` so the audit trail
  records the accepted generic-clearcut modeling assumption.

## 2026-06-26 - Opened P4.3 Matrix Builder QA lane

- opened child issue `#38` for P4.3 Matrix Builder execution and
  tracks/features/accounts QA under Phase 4 parent `#14`;
- linked P4.3 in `ROADMAP.md` and made it the active Phase 4 lane after P4.2
  closeout;
- defined the P4.3 inputs as the accepted P4.2 XML/fragments under ignored
  `output/patchworks_tfl6_validated/`; and
- kept runtime-package assembly, launch smoke, and publication downstream of
  P4.3.

## 2026-06-26 - Ran P4.3 Matrix Builder smoke and found account-output gap

- repaired `config/patchworks.runtime.windows.yaml` so TFL6 Matrix Builder
  points at `output/patchworks_tfl6_validated/forestmodel.xml`,
  `output/patchworks_tfl6_validated/fragments/fragments.dbf`, and
  `models/tfl6_patchworks_model/tracks`;
- passed Patchworks preflight against the TFL6 runtime config;
- found the first Matrix Builder attempt was invalid despite wrapper effective
  return code `0`, because raw Matrix Builder return code was `1`, core track
  CSVs were empty, and the log reported a succession-cycle failure from the
  generic `1000 -> 1000` pass-through rule;
- repaired the generic FEMIC FMG pass-through succession default to
  `breakup=999` and `renew=0`, regenerated TFL6 XML/fragments, and reran
  Matrix Builder;
- confirmed readable core tracks after the rerun: `33322` block rows, `55717`
  feature rows, `17173` group rows, `16379` product rows, `18447` strata rows,
  `9212` trackname rows, and `10703` treatment rows; and
- kept P4.3 open because `protoaccounts.csv` and `accounts.csv` are still
  missing from the generated tracks, leaving
  `accounts_sync: skipped_missing_protoaccounts`.

## 2026-06-26 - Closed P4.3 Matrix Builder QA after account promotion

- increased the TFL6 Windows Matrix Builder auto-close settle window to
  `20.0` seconds so Matrix Builder can finish writing `protoaccounts.csv`
  before FEMIC closes the spawned window;
- reran Matrix Builder with run id `tfl6_p43_matrix_accounts_wait20`;
- confirmed `accounts_sync: synced`, with `211` readable `protoaccounts.csv`
  rows and `211` promoted `accounts.csv` rows;
- confirmed final readable core tracks: `47218` block rows, `86574` feature
  rows, `24879` group rows, `26085` product rows, `28858` strata rows, `14429`
  trackname rows, and `17390` treatment rows;
- verified generic `product.Treated.managed.CC` and
  `product.HarvestedVolume.managed.Total.CC` account surfaces are present; and
- marked P4.3 complete in `ROADMAP.md`, leaving P4.4 runtime-package build/QA
  as the active Phase 4 lane.
