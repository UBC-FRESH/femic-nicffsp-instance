# TFL 6 MP11 Phase 15 Publication And Replacement-Candidate Plan

## Purpose

Phase 15 publishes and validates the Phase 14 MP11 harvest-system candidate
runtime as a replacement-candidate QA lane. It uses the existing TFL 6
`arbutus-s3` git-annex publication workflow, proves no-credential
clean-checkout materialization, unpacks the materialized archive, reruns direct
launch plus all-system and no-heli scenario smoke from the archive payload, and
records whether the runtime is ready for replacement review.

Phase 15 does not silently replace Phase 5. Passing P15 means
`replacement_candidate_ready_for_review`; Phase 5 remains the accepted public
teaching/runtime baseline until a later explicit replacement acceptance decision.

## Issue Tree

- `#147`: Phase 15 parent issue.
- `#148`: P15.1 launch MP11 harvest-system publication and
  replacement-candidate plan.
- `#149`: P15.2 build MP11 harvest-system runtime archive and manifest.
- `#150`: P15.3 annex and publish archive through `arbutus-s3`.
- `#151`: P15.4 prove no-credential clean-checkout materialization.
- `#152`: P15.5 run direct launch and scenario smoke from materialized archive.
- `#153`: P15.6 document publication, caveats, and replacement-candidate status.
- `#154`: P15.7 decide replacement-candidate readiness and close Phase 15.

## Source Runtime

P15 consumes the completed Phase 14 harvest-system runtime:

- runtime config:
  `config/patchworks.runtime.mp11_harvest_system_candidate.windows.yaml`;
- ForestModel XML/fragments:
  `output/patchworks_tfl6_mp11_harvest_system_candidate/`;
- runtime package:
  `models/tfl6_patchworks_model_mp11_harvest_system_candidate/`;
- all-system tracks:
  `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/`;
- no-heli tracks:
  `models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks_no_heli/`;
- launch surfaces:
  `analysis/base.pin` and `analysis/no_heli.pin`; and
- P14.7 smoke evidence:
  `planning/tfl6_mp11_phase14_scenario_smoke_qa.{csv,json,md}`.

P15 does not publish the older P13 archive as the replacement candidate. The
P13 archive is useful historical evidence for the pre-harvest-system MP11
candidate, but the P15 payload must come from Phase 14.

## Publication Artifacts

Canonical P15 artifacts:

- `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2.zip`;
- `releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml`.

Expected P15 planning outputs:

- `planning/tfl6_mp11_phase15_archive_publication_qa.{csv,json,md}`;
- `planning/tfl6_mp11_phase15_materialization_qa.{csv,json,md}`;
- `planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.{csv,json,md}`;
- `planning/tfl6_mp11_phase15_replacement_candidate_decision.{csv,json,md}`.

## Status Vocabulary

Phase 15 uses these release-status labels:

- `local_archive_built_not_published`;
- `published_materialization_pending`;
- `materialized_smoke_pending`;
- `replacement_candidate_ready_for_review`;
- `replacement_candidate_blocked`.

## Validation Gates

Hard gates:

- archive ZIP integrity passes;
- archive SHA256 matches the manifest;
- manifest member count matches included files;
- archive and manifest are annexed and copied to `arbutus-s3`;
- `git annex whereis` shows local and `arbutus-s3` copies;
- no-credential clean-checkout materialization fetches both artifacts;
- materialized archive SHA256 matches the manifest;
- direct launch smoke from the unpacked archive passes;
- all-system 200,000-iteration smoke from the unpacked archive passes and
  schedules `CC_GROUND`, `CC_CABLE`, and `CC_HELI`;
- no-heli 200,000-iteration smoke from the unpacked archive passes and
  schedules `CC_GROUND` and `CC_CABLE` only; and
- tracked docs/planning files contain no personal local paths.

Soft caveats that do not block `replacement_candidate_ready_for_review`:

- WFP LBB remains unavailable/private.
- Harvest-system classes remain public-proxy assignments.
- Phase 5 remains the accepted public baseline until a later replacement
  acceptance decision.
- The P15 decision is replacement-candidate readiness, not an approved AAC claim.

## Non-Goals

- Do not rebuild THLB, AU/yield curves, ForestModel XML, Matrix Builder tracks,
  or Patchworks blocks in P15.
- Do not alter the Phase 14 runtime model logic.
- Do not claim WFP-model equivalence.
- Do not mark Phase 5 replaced during P15.

