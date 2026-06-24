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
