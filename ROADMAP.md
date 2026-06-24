# Roadmap

## Phase 1: Bootstrap Repository and Build Plan (`#4`)

- [x] P1.1 Create the standalone `femic-tfl6-instance` repository scaffold.
  - [x] P1.1a Initialize the FEMIC instance skeleton.
  - [x] P1.1b Add modelwright-style workflow surfaces:
    `AGENTS.md`, `ROADMAP.md`, `CHANGE_LOG.md`, and `planning/`.
  - [x] P1.1c Add the uploaded AOI, LU, and FSP source payloads under stable
    lowercase tracked paths.
- [x] P1.2 Inspect and normalize source payloads (`#1`).
  - [x] P1.2a Unzip and inspect the NICF FSP amendment spatial payload.
  - [x] P1.2b Identify the authoritative AOI layer, geometry type, CRS, and
    expected area.
  - [x] P1.2c Inspect the LU clip payload and identify the three relevant LU
    boundaries referenced by the FSP.
  - [x] P1.2d Decide which extracted layers become tracked canonical source
    files and which remain regenerated scratch.
- [x] P1.3 Define the first K3Z-to-NICF adaptation contract (`#3`).
  - [x] P1.3a Compare K3Z config, model-input bundle, docs, and Patchworks
    package structure against the NICF FSP requirements.
  - [x] P1.3b Define the first `run_profile.nicffsp.yaml` boundary after AOI
    extraction.
  - [x] P1.3c Identify which K3Z teaching assumptions can carry forward and
    which need explicit FRST 558 review.
  - [x] P1.3d Identify the minimum source-derived model-input surfaces needed
    before Patchworks runtime-package work.
  - [x] P1.3e Record the accepted adaptation boundary and keep implementation
    in follow-on tasks.
- [x] P1.4 Split model-design work into follow-on issues (`#2`).
  - [x] P1.4a Open a cedar-signal design issue covering Cw cultural reserve,
    utility-pole-grade products, treatments, yield curves, accounts, and
    reporting outputs (`#8`).
  - [x] P1.4b Open a K3Z expansion candidate-area issue covering unallocated
    candidate-area pool construction, productivity screening, and AAC uplift
    constraints (`#9`).
  - [x] P1.4c Open a Patchworks runtime-package issue once source normalization
    and model-design boundaries are accepted (`#10`).
- [x] P1.5 Materialize 2025 VRI source datasets for NICF base inventory (`#5`).
  - [x] P1.5a Record official 2025 R1 and VDYP7 polygon/layer package metadata.
  - [x] P1.5b Materialize the 2025 provincial source packages under the
    accepted `external/femic-public-data/data/bc/vri/2025/` convention.
  - [x] P1.5c Record file size, checksum, read-smoke, CRS, and layer-name
    evidence for both materialized packages.
  - [x] P1.5d Record DataLad/git-annex/public-data publication status and the
    downstream extraction handoff to the accepted active AOI issue, then publish
    any missing remote keys before closing P1.5.
- [x] P1.6 Pivot active AOI to TFL 6 and clip 2025 VRI inputs (`#6`).
  - [x] P1.6a Fetch and normalize the authoritative TFL 6 boundary from
    `WHSE_ADMIN_BOUNDARIES.FADM_TFL`.
  - [x] P1.6b Clip the 2025 VRI R1 polygon source to TFL 6 and record geometry
    QA.
  - [x] P1.6c Filter the 2025 VDYP7 polygon and layer tables to the TFL 6
    feature-id set and verify key integrity.
  - [x] P1.6d Record the accepted TFL 6 input-layer manifest and mark the
    original FDU 1/2/3 AOI as superseded for active model extraction.
- [x] P1.7 Plan TFL 6 source-layer and THLB netdown recipes from 2011 documents
  (`#7`).
  - [x] P1.7a Add/verify local source copies of the TFL 6 Management Plan 10 and
    information package PDFs, plus the broader TFL 6 reference corpus index.
  - [x] P1.7b Review the 2011 documents for land-base, source-layer, yield, and
    THLB netdown assumptions.
  - [x] P1.7b1 Record the ordered Management Plan 10 Table 4 THLB netdown
    backbone in `planning/tfl6_thlb_netdown_steps.md`, including tentative
    `GLB -> AFLB -> LHLB -> THLB` mapping, cumulative benchmarks, and
    per-step input-layer/GIS-operation readiness notes.
  - [x] P1.7b2 Scrape post-2011 TFL 6 instrument links and record boundary
    reconciliation evidence in
    `planning/tfl6_instrument_boundary_reconciliation.md`.
  - [x] P1.7b3 Scale MP10 Table 4 values to provisional current-AOI validation
    targets in `planning/tfl6_adjusted_thlb_benchmarks.md` and
    `planning/tfl6_adjusted_thlb_benchmarks.json`.
  - [x] P1.7c Separate TSA29 workflow carry-forward assumptions from
    TFL/general-FMU adaptation gaps.
  - [x] P1.7d Draft source-layer and THLB netdown recipe skeletons or planning
    tables without executing recipes.
- [ ] P1.8 Plan next roadmap phases and issue tree (`#11`).
  - [x] P1.8a Draft proposed Phase 2 through at least Phase 5 sections in this
    roadmap.
  - [x] P1.8b Create one GitHub parent issue per proposed phase.
  - [x] P1.8c Create linked child task issues for the first executable tasks in
    each proposed phase.
  - [ ] P1.8d Record dependency order across source-layer/THLB work, cedar
    design, expansion design, model-input generation, Patchworks runtime build,
    QA/publication, and teaching docs.
  - [ ] P1.8e Place existing follow-on issues `#8`, `#9`, and `#10` into the
    planned phase structure or explicitly defer them.

## Proposed Phase 2: Reviewed Source Layers and THLB Netdown (`#12`)

Goal: turn the TFL 6 source-layer and THLB planning surfaces into reviewed,
executable FEMIC source-layer and netdown recipes before model-input generation
starts.

- [ ] P2.1 Resolve and materialize public/reference source layers needed by the
  TFL 6 THLB skeleton (`#16`).
- [ ] P2.2 Profile accepted 2025 R1 and VDYP7 fields for non-forest,
  non-productive, deciduous-leading, productivity, and join-key assumptions.
- [ ] P2.3 Define reviewed current-AOI source-layer recipe contracts under the
  future TFL/general-FMU recipe path.
- [ ] P2.4 Implement and smoke-test the first executable THLB netdown recipe
  lane against the accepted TFL 6 input surfaces.
- [ ] P2.5 Compare GLB/AFLB/LHLB/THLB milestones against the adjusted current-AOI
  benchmark targets and record accepted teaching tolerances.

## Proposed Phase 3: Model Design Assumptions (`#13`)

Goal: define the reviewed model-design assumptions that depend on the accepted
source-layer and THLB surfaces, without compiling a Patchworks package.

- [ ] P3.1 Complete cedar-signal design (`#8`) for Cw cultural reserve,
  utility-pole-grade products, treatments, yield implications, accounts, and
  reporting outputs.
- [ ] P3.2 Complete expansion candidate-area design (`#9`) for unallocated
  candidate pools, productivity screening, and AAC uplift constraints.
- [ ] P3.3 Define yield-source, treatment, seral/objective, and account/report
  assumptions that must exist before model-input bundle generation.
- [ ] P3.4 Update the TFL 6 run-profile/model-input contract with reviewed
  design decisions and explicit rejected/deferred assumptions.

## Proposed Phase 4: Model Inputs and Patchworks Runtime Package (`#14`)

Goal: generate, inspect, and QA the first runnable TFL 6 Patchworks teaching
package only after the reviewed source-layer, THLB, and model-design contracts
exist.

- [ ] P4.1 Build the reviewed model-input bundle from accepted TFL 6 source
  layers, THLB outputs, and model-design assumptions (`#17`).
- [ ] P4.2 Generate ForestModel/XML and inspect the semantics that affect
  Patchworks treatment eligibility, curve provenance, products, accounts, and
  targets.
- [ ] P4.3 Execute Matrix Builder and QA tracks, features, accounts,
  protoaccounts, products, targets, and reports.
- [ ] P4.4 Complete Patchworks runtime-package build/QA (`#10`) with
  representative launch and scenario-smoke checks.

## Proposed Phase 5: Publication, Teaching Docs, and Release QA (`#15`)

Goal: make the teaching instance reproducible and usable by students/instructors
after the runtime package has passed direct artifact and launch smoke checks.

- [ ] P5.1 Decide which compact runtime artifacts are tracked, annexed,
  published, or regenerated (`#18`).
- [ ] P5.2 Publish required data/runtime artifacts through the accepted FEMIC
  public-data workflow and prove fresh-environment materialization.
- [ ] P5.3 Write teaching workflow docs, quickstart instructions, validation
  notes, and known-limitations notes.
- [ ] P5.4 Run final release QA across source materialization, instance rebuild,
  Patchworks launch smoke, and documentation checks.

## Current Next Steps

1. Continue `P1.8d` / `#11`: record dependency order across source-layer/THLB
   work, cedar design, expansion design, model-input generation, Patchworks
   runtime build, QA/publication, and teaching docs.
2. Continue `P1.8e` / `#11`: place existing follow-on issues `#8`, `#9`, and
   `#10` into the planned phase structure or explicitly defer them.
3. Keep follow-on implementation issues `#8`, `#9`, and `#10` open but idle
   until P1.8 places them into the planned phase structure or the maintainer
   explicitly approves a parallel lane.
