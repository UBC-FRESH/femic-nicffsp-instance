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
