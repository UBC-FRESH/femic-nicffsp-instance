# TFL 6 MP11 Phase 15 Replacement-Candidate Decision

P15.7 records whether the published MP11 harvest-system candidate runtime is ready for replacement review.

## Decision

- decision: `replacement_candidate_ready_for_review`
- phase5_baseline_status: `accepted_public_runtime_baseline_retained`
- replace_phase5: `False`
- wfp_model_equivalence: `False`

The P15 runtime is ready for replacement review because archive publication, no-credential materialization, checksum validation, direct launch, all-system scenario smoke, no-heli scenario smoke, and publication documentation have passed. Phase 5 remains the accepted baseline until a later explicit replacement acceptance decision.

## Gate Results

| Gate | Status | Evidence | Rationale |
| --- | --- | --- | --- |
| `planning_note` | `pass` | planning/tfl6_mp11_phase15_publication_replacement_candidate_plan.md | required P15 evidence surface is present |
| `archive_qa` | `pass` | planning/tfl6_mp11_phase15_archive_publication_qa.json | required P15 evidence surface is present |
| `archive_manifest` | `pass` | releases/tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml | required P15 evidence surface is present |
| `materialization_qa` | `pass` | planning/tfl6_mp11_phase15_materialization_qa.json | required P15 evidence surface is present |
| `materialized_runtime_smoke_qa` | `pass` | planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json | required P15 evidence surface is present |
| `phase15_docs` | `pass` | docs/phase15-mp11-runtime-publication.rst | required P15 evidence surface is present |
| `archive_published` | `pass` | planning/tfl6_mp11_phase15_archive_publication_qa.json | archive and manifest were annexed, copied to arbutus-s3, and verified before materialization |
| `archive_checksum` | `pass` | planning/tfl6_mp11_phase15_materialization_qa.json | materialized archive SHA256 matches the tracked manifest |
| `public_no_credential_materialization` | `pass` | planning/tfl6_mp11_phase15_materialization_qa.json | clean checkout fetched archive and manifest from arbutus-s3 with credentials cleared |
| `direct_launch_from_archive` | `pass` | planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json | materialized archive direct launch returned success |
| `all_system_scenario_from_archive` | `pass` | planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json | all-system 200k smoke scheduled cable, ground, and heli lanes |
| `no_heli_scenario_from_archive` | `pass` | planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json | no-heli 200k smoke scheduled cable and ground lanes only and did not trip missing heli account startup errors |
| `phase15_decision` | `replacement_candidate_ready_for_review` | P15.1-P15.6 hard-gate evidence | all publication, materialization, checksum, launch, scenario, and documentation hard gates pass |
| `phase5_baseline` | `accepted_baseline_retained` | Phase 5 release remains unchanged | P15 creates a replacement candidate for review; it does not silently replace Phase 5 |
| `wfp_model_equivalence` | `not_claimed` | docs/phase15-mp11-runtime-publication.rst | WFP LBB is unavailable and harvest-system lanes remain public proxy assignments |

## Caveats

- WFP LBB remains unavailable and private.
- Ground, cable, and heli assignments are public proxies.
- The candidate is not WFP-model equivalent.
- The candidate is not an approved AAC decision.
- Phase 5 remains the accepted public teaching/runtime baseline until replacement is explicitly accepted.
