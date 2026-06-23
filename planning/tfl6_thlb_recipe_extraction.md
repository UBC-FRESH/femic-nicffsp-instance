# TFL 6 TSR and THLB Recipe Extraction Plan

## Purpose

This note queues the follow-on planning lane for translating the TFL 6
Management Plan 10 timber supply assumptions into FEMIC-style reviewed
source-layer and THLB netdown recipe surfaces.

Governing issue: `#7`.

## Source Documents

Primary source documents:

- TFL 6 Management Plan 10:
  `https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-tenures/tree-farm-licence/management-plans/tfl_6_mngment_plan_10_2011.pdf`
- TFL 6 Management Plan 10 Information Package:
  `https://www2.gov.bc.ca/assets/gov/farming-natural-resources-and-industry/forestry/timber-tenures/tree-farm-licence/management-plans/tfl_6_mngment_plan_2011_ip.pdf`

Local reference already added:

- `data/source/nicf_fsp/reference/tfl_6_management_plan_10_information_package_2011.pdf`

The management-plan PDF still needs a local source copy and checksum before
recipe extraction work begins.

## FEMIC Workflow Pattern

The closest existing pattern is the TSA29 TSR workflow:

- canonical discovery/fact extraction;
- reviewed instance-local overlay;
- reviewed source-layer recipe;
- reviewed THLB netdown recipe;
- optional workbench and locked/reconstructed execution surfaces.

Relevant command/document surfaces in FEMIC:

- `femic tsr recipe-init`
- `femic tsr source-layers-build`
- `femic tsr source-layers-run`
- `femic tsr thlb-netdown-build`
- `femic tsr thlb-netdown-workbench-build`
- `femic tsr thlb-netdown-workbench-lock`
- `femic tsr thlb-netdown-run`
- `docs/guides/tsr-intelligence-workflow.rst`
- `docs/reference/cli.rst`
- `docs/reference/api/femic-tsr-catalog.rst`

Important gap:

- The current built-in TSR discovery/fetch/fact workflow is TSA-oriented.
  TFL 6 recipe work should not pretend it is a TSA workflow. The first recipe
  planning pass must explicitly identify what can be reused and what needs a
  TFL/general-FMU adaptation.

## Planned Review Outputs

Use planning tables first, then promote reviewed decisions into recipe YAML only
after the source assumptions are accepted.

Planned planning outputs:

- `planning/tfl6_source_layer_candidates.md`
- `planning/tfl6_thlb_netdown_steps.md`

Possible later recipe/config outputs:

- `config/tsr/source_layers.recipe.yaml` or a TFL/general-FMU successor path
- `config/tsr/thlb_netdown.recipe.yaml` or a TFL/general-FMU successor path
- `config/tsr/overlay.yaml` only if the current overlay schema is generalized
  beyond TSA identity assumptions

## Extraction Questions

The `#7` review should answer:

- Which tables/sections in the 2011 information package define the gross land
  base, productive forest, operable area, THLB exclusions, and residual THLB?
- Which assumptions are spatial source-layer deductions versus aspatial/model
  assumptions?
- Which public BCDC layers can support each spatial deduction?
- Which deductions require local source data, management-plan assumptions, or
  reviewed aspatial treatment because no public layer is available?
- Which yield/source assumptions affect VDYP/TIPSY inputs but are not THLB
  netdown steps?
- What execution stage each THLB step belongs to:
  - source acquisition;
  - initial land-base classification;
  - exact spatial overlay;
  - checkpoint-attribute exclusion;
  - aspatial benchmark deduction; or
  - review-only/manual note.

## Dependency

Do not execute THLB recipe steps until `#6` has accepted:

- TFL 6 AOI boundary;
- clipped 2025 R1 polygon input;
- filtered 2025 VDYP7 polygon table;
- filtered 2025 VDYP7 layer table; and
- input-layer manifest.

## Non-Goals

- Do not auto-adopt extracted candidate facts as model truth.
- Do not run THLB netdown before source layers and reviewed assumptions exist.
- Do not start Patchworks runtime-package compilation in this planning lane.
