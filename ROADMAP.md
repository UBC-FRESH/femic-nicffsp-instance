# Roadmap

## Phase 1: Bootstrap Repository and Build Plan

- [x] P1.1 Create the standalone `femic-nicffsp-instance` repository scaffold.
  - [x] P1.1a Initialize the FEMIC instance skeleton.
  - [x] P1.1b Add modelwright-style workflow surfaces:
    `AGENTS.md`, `ROADMAP.md`, `CHANGE_LOG.md`, and `planning/`.
  - [x] P1.1c Add the uploaded AOI, LU, and FSP source payloads under stable
    lowercase tracked paths.
- [ ] P1.2 Inspect and normalize source payloads (`#1`).
  - [ ] P1.2a Unzip and inspect the NICF FSP amendment spatial payload.
  - [ ] P1.2b Identify the authoritative AOI layer, geometry type, CRS, and
    expected area.
  - [ ] P1.2c Inspect the LU clip payload and identify the three relevant LU
    boundaries referenced by the FSP.
  - [ ] P1.2d Decide which extracted layers become tracked canonical source
    files and which remain regenerated scratch.
- [ ] P1.3 Define the first K3Z-to-NICF adaptation contract (`#1`).
  - [ ] P1.3a Compare K3Z config, model-input bundle, docs, and Patchworks
    package structure against the NICF FSP requirements.
  - [ ] P1.3b Define the first `run_profile.nicffsp.yaml` boundary after AOI
    extraction.
  - [ ] P1.3c Identify which K3Z teaching assumptions can carry forward and
    which need explicit FRST 558 review.
- [ ] P1.4 Split model-design work into follow-on issues.
  - [ ] P1.4a Open a cedar-signal design issue covering Cw cultural reserve,
    utility-pole-grade products, treatments, yield curves, accounts, and
    reporting outputs.
  - [ ] P1.4b Open a K3Z expansion candidate-area issue covering unallocated
    candidate-area pool construction, productivity screening, and AAC uplift
    constraints.
  - [ ] P1.4c Open a Patchworks runtime-package issue once source normalization
    and model-design boundaries are accepted.

## Current Next Steps

1. Inspect `data/source/nicf_fsp/nicf_fsp_amendment_3_spatial.zip` and record
   the layer inventory in `planning/source_inventory.md`.
2. Inspect `data/source/nicf_fsp/bcgw_lu_clip_2026_06.zip` and confirm the LU
   boundary names and CRS.
3. Update `config/run_profile.nicffsp.yaml` only after the authoritative AOI
   boundary has been extracted into a stable path.
