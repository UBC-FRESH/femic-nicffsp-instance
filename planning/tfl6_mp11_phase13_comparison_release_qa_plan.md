# TFL 6 MP11 Phase 13 Comparison And Release QA Plan

## Purpose

Phase 13 turns the Phase 12 smoke-tested MP11 candidate runtime into documented comparison evidence and a release decision. It must answer a practical question: whether the MP11 candidate runtime should replace, supplement, or remain experimental relative to the completed Phase 5 teaching/runtime baseline.

Phase 13 is not another model rebuild phase. It should not rerun THLB, regenerate yield curves, rebuild ForestModel XML, rerun Matrix Builder, or recalibrate Patchworks unless a later child issue explicitly authorizes a narrow repair. The starting point is the candidate runtime package closed in P12.6.

## Governing Issues

- Parent: `#70` Phase 13 MP11 comparison documentation and release QA.
- `#127` P13.1b: build reproducible MP11 scenario comparison tables.
- `#128` P13.2: build MP11 KPI and caveat comparison report.
- `#129` P13.3: update MP11 Sphinx docs and teaching guidance.
- `#130` P13.4: prepare MP11 candidate runtime archive and materialization QA.
- `#131` P13.5: decide MP11 release status and Phase 5 baseline relationship.

## Starting Inputs

The auditable Phase 13 input set is:

- `planning/tfl6_mp11_phase12_runtime_closeout.{csv,json,md}`;
- `planning/tfl6_mp11_phase13_candidate_runtime_positioning.md`;
- `planning/tfl6_mp11_scenario_smoke_qa.{csv,json,md}`;
- `planning/tfl6_mp11_direct_launch_qa.{csv,json,md}`;
- `planning/tfl6_mp11_matrix_builder_tracks_qa.{csv,json,md}`;
- `planning/tfl6_mp11_runtime_package_manifest.{csv,json,md}`;
- `planning/tfl6_mp11_model_behavior_crosswalk.{csv,json,md}`;
- `planning/tfl6_mp11_land_base_crosswalk.{csv,json,md}`;
- `planning/tfl6_mp11_netdown_delta_crosswalk.{csv,json,md}`;
- `planning/tfl6_mp11_reviewed_extraction_manifest.{csv,json,md}`;
- `models/tfl6_patchworks_model_mp11_candidate/lineage_registry.yaml`; and
- generated local runtime outputs under `models/tfl6_patchworks_model_mp11_candidate/`, when present.

The maintainer screenshot of the local interactive Patchworks run is context only. It supports the P13.1 positioning note but is not a tracked release QA artifact.

## Execution Sequence

### P13.1b Scenario Comparison Tables

Build reproducible tracked comparison tables from Phase 12 runtime outputs. The first table must compare:

- WFP MP11 Figure 2 base-case harvest trajectory;
- MP11 Table 11 or nearby text values where available;
- adjusted LRSY context;
- Phase 12 candidate runtime smoke output;
- maintainer interactive target context; and
- evidence-strength labels.

This step should produce `planning/tfl6_mp11_phase13_scenario_comparison.{csv,json,md}` or a similarly named surface.

### P13.2 KPI And Caveat Comparison Report

Broaden comparison beyond harvest flow. Required surfaces include land base, THLB, source-layer caveats, yield/curve caveats, growing stock, age/seral context, cedar/old-cedar evidence, harvest-system caveats, and selected MP11 sensitivity evidence where tracked sources already exist.

Every comparison row must carry:

- MP11 source anchor;
- candidate-runtime source anchor;
- validation-strength label;
- whether the value is model output, model input, planning-only evidence, or maintainer context;
- caveat text; and
- release-decision implication.

### P13.3 Docs And Teaching Guidance

Update Sphinx documentation so public readers understand:

- the Phase 5 baseline status;
- the MP11 candidate runtime status;
- what the public-data reconstruction does and does not claim;
- how to launch or inspect the candidate runtime when artifacts are available;
- how to interpret MP11 comparison tables; and
- which caveats are blockers versus teaching discussion points.

Docs must build warning-clean with `-W`.

### P13.4 Runtime Archive And Materialization QA

Decide whether and how the MP11 candidate runtime can be published. This includes archive contents, checksums, ignored/generated surfaces, public-safe materialization steps, and a clean-checkout test or documented blocker.

Generated tracks, blocks, saved stages, logs, and archives must remain excluded unless explicitly promoted by this step.

### P13.5 Release Decision

Close Phase 13 with one of three decisions:

- `replace_phase5`: MP11 candidate becomes the recommended runtime package.
- `supplement_phase5`: MP11 candidate is published as a caveated companion while Phase 5 remains the default.
- `experimental_only`: MP11 candidate remains a development artifact pending later model repair or QA.

The decision must cite P13.1-P13.4 evidence and explain any blockers that prevent replacement.

## Required Evidence Labels

Use these labels consistently:

- `tracked_runtime_output`;
- `tracked_model_input`;
- `tracked_mp11_table_or_text`;
- `reviewed_mp11_figure_extraction`;
- `planning_only_figure_extraction`;
- `maintainer_context`;
- `deferred_constraint`;
- `release_blocker`; and
- `not_release_evidence`.

## Non-Goals

- Do not claim exact WFP model replication.
- Do not claim approved AAC equivalence.
- Do not treat screenshot-only values as release QA.
- Do not rebuild source layers, THLB, yields, XML, Matrix Builder tracks, or Patchworks runtime in Phase 13 unless a later child issue explicitly authorizes a narrow repair.
- Do not publish private WFP assumptions, private documents, prompt logs, or local scratch artifacts.

## Initial Working Interpretation

The current candidate runtime is plausibly in the same broad model family as the WFP MP11 base-case evidence. The approximately `1.15 million m3/year` interactive candidate result is above the implied WFP MP11 base-case level of approximately `1.0616 million m3/year`, but the candidate runtime also lacks some WFP constraints and carries a slightly larger public-data THLB scaffold. That makes the current result encouraging, not conclusive.

Phase 13 should formalize that interpretation with reproducible tables before any release or replacement decision.
