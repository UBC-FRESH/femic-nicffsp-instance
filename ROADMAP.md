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

## Current Next Steps

1. Start `P1.4` / `#2`: open the cedar-signal design follow-on issue with the
   source-boundary and minimum-model-input terms from `P1.3`.
2. Continue `P1.4` / `#2`: open the K3Z expansion candidate-area design issue.
3. Continue `P1.4` / `#2`: open the Patchworks runtime-package build/QA issue
   after the cedar and expansion issue boundaries are recorded.
