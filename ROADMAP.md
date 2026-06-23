# Roadmap

## Phase 1: Bootstrap Repository and Build Plan (`#4`)

- [x] P1.1 Create the standalone `femic-nicffsp-instance` repository scaffold.
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
- [ ] P1.4 Split model-design work into follow-on issues (`#2`).
  - [ ] P1.4a Open a cedar-signal design issue covering Cw cultural reserve,
    utility-pole-grade products, treatments, yield curves, accounts, and
    reporting outputs.
  - [ ] P1.4b Open a K3Z expansion candidate-area issue covering unallocated
    candidate-area pool construction, productivity screening, and AAC uplift
    constraints.
  - [ ] P1.4c Open a Patchworks runtime-package issue once source normalization
    and model-design boundaries are accepted.
- [ ] P1.5 Materialize 2025 VRI source datasets for NICF base inventory (`#5`).
  - [x] P1.5a Record official 2025 R1 and VDYP7 polygon/layer package metadata.
  - [x] P1.5b Materialize the 2025 provincial source packages under the
    accepted `external/femic-public-data/data/bc/vri/2025/` convention.
  - [ ] P1.5c Record file size, checksum, read-smoke, CRS, and layer-name
    evidence for both materialized packages.
  - [ ] P1.5d Record DataLad/git-annex/public-data publication status and the
    downstream extraction handoff to the accepted active AOI issue.
- [ ] P1.6 Pivot active AOI to TFL 6 and clip 2025 VRI inputs (`#6`).
  - [ ] P1.6a Fetch and normalize the authoritative TFL 6 boundary from
    `WHSE_ADMIN_BOUNDARIES.FADM_TFL`.
  - [ ] P1.6b Clip the 2025 VRI R1 polygon source to TFL 6 and record geometry
    QA.
  - [ ] P1.6c Filter the 2025 VDYP7 polygon and layer tables to the TFL 6
    feature-id set and verify key integrity.
  - [ ] P1.6d Record the accepted TFL 6 input-layer manifest and mark the
    original FDU 1/2/3 AOI as superseded for active model extraction.
- [ ] P1.7 Plan TFL 6 source-layer and THLB netdown recipes from 2011 documents
  (`#7`).
  - [ ] P1.7a Add/verify local source copies of the TFL 6 Management Plan 10 and
    information package PDFs.
  - [ ] P1.7b Review the 2011 documents for land-base, source-layer, yield, and
    THLB netdown assumptions.
  - [ ] P1.7c Separate TSA29 workflow carry-forward assumptions from
    TFL/general-FMU adaptation gaps.
  - [ ] P1.7d Draft source-layer and THLB netdown recipe skeletons or planning
    tables without executing recipes.

## Current Next Steps

1. Start `P1.6` / `#6`: fetch and normalize the TFL 6 boundary, then clip the
   2025 VRI R1 and VDYP7 source inputs to the new active AOI.
2. Continue `P1.5` / `#5`: record public-data remote publication status for
   the provincial 2025 VRI source archives.
3. Start `P1.7` / `#7`: review the 2011 TFL 6 management plan and information
   package for source-layer and THLB netdown recipe candidates after the TFL 6
   input layers are accepted.
