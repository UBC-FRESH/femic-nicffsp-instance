# TFL 6 MP11 Phase 13 Candidate Runtime Positioning

This note starts Phase 13 comparison documentation from the Phase 12 smoke-tested MP11 candidate runtime. It records the initial maintainer interpretation after a local interactive Patchworks run with maximize-even-flow harvest volume and maintain-initial-growing-stock targets active.

## Interpretation

The MP11 candidate runtime is now a solid base model to build on. A local interactive Patchworks run produced an even-flow harvest level of approximately `1.15 million m3/year` with the current candidate inputs and a basic target set. This is close to, but above, the WFP MP11 base-case harvest trajectory shown in `Figure 2 Base Case Harvest Level`.

The MP11 text around Figure 2 reports the base case as a decrease of `300,400 m3/year` from the current AAC of `1,362,000 m3/year`, implying an MP11 base-case level of approximately `1,061,600 m3/year`. It also reports an adjusted long-run sustained yield comparison value of `1,182,900 m3/year`. The candidate runtime's approximately `1.15 million m3/year` interactive result is therefore in the same general range as the MP11 base-case/LRSY evidence, but it should not be described as an exact replication.

## Why A Higher Candidate Result Is Plausible

The candidate runtime does not yet include every constraint WFP likely included in the MP11 base case. It also carries a public-data THLB scaffold that is slightly larger than the MP11 declared THLB. Those two facts make a somewhat higher even-flow result plausible without treating the model as wrong or as a different conceptual model.

Phase 9RF records the candidate current THLB at `122,763.421 ha` versus the MP11 declared `120,099 ha`, a difference of `2,664.421 ha` or about `2.2%`. That is close enough to support the working interpretation that the candidate runtime is plausibly near the MP11 model family, while still requiring explicit Phase 13 comparison QA before any release or replacement claim.

## Evidence Status

The local Patchworks screenshot is useful maintainer evidence, but it is not a tracked model-output artifact. Phase 13 should use it as a prompt for formal comparison work, not as a release QA record. Tracked Phase 13 evidence should come from reproducible scenario exports, target summaries, schedule tables, runtime manifests, and documented comparison tables.

The tracked Phase 12 evidence remains the current auditable base:

- `planning/tfl6_mp11_phase12_runtime_closeout.{csv,json,md}`;
- `planning/tfl6_mp11_scenario_smoke_qa.{csv,json,md}`;
- `planning/tfl6_mp11_direct_launch_qa.{csv,json,md}`;
- `planning/tfl6_mp11_matrix_builder_tracks_qa.{csv,json,md}`;
- `planning/tfl6_mp11_runtime_package_manifest.{csv,json,md}`; and
- `models/tfl6_patchworks_model_mp11_candidate/lineage_registry.yaml`.

## Phase 13 Positioning Boundary

Recommended wording for Phase 13:

> The MP11 candidate runtime is a plausible public-data reconstruction of the MP11 model structure and produces harvest-flow behavior in the same broad range as the MP11 base-case evidence. It remains a candidate model until Phase 13 comparison documentation, release QA, archive materialization, and baseline replacement/supplement decisions pass.

Avoid wording that claims:

- exact replication of WFP's unpublished model;
- approved AAC equivalence;
- final release readiness;
- replacement of the Phase 5 teaching/runtime baseline before Phase 13 QA; or
- use of screenshot-only evidence as an auditable model-output record.
