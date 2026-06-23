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
