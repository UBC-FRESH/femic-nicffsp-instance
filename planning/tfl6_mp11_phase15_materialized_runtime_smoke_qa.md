# TFL 6 MP11 Phase 15 Materialized Runtime Smoke QA

This P15.5 report inspects Patchworks runs launched from the materialized P15 archive payload, not from the source working tree.

## Summary

- generated_at_utc: `2026-06-29T07:31:40+00:00`
- qa_status: `materialized_runtime_smoke_pass`
- materialized_root_class: `temp_clean_checkout_runtime_p15_materialized_archive`
- log_dir_class: `temp_materialized_archive_log_dir`
- direct_launch_status: `pass`
- all_system_status: `pass`
- no_heli_status: `pass`
- all_system_schedule_rows: `76693`
- no_heli_schedule_rows: `75023`
- all_system_treatments: `CC_CABLE,CC_GROUND,CC_HELI`
- no_heli_treatments: `CC_CABLE,CC_GROUND`
- no_heli_forbidden_present: `none`
- replacement_candidate_decision: `pending_p15_7`

## Runs

| Run | Status | Schedule Rows | Treatments | Forbidden Present |
| --- | --- | ---: | --- | --- |
| `direct_launch` | `pass` | 0 | `` | `none` |
| `all_system` | `pass` | 76693 | `CC_CABLE,CC_GROUND,CC_HELI` | `none` |
| `no_heli` | `pass` | 75023 | `CC_CABLE,CC_GROUND` | `none` |

## Boundary

- P15.5 proves archive-derived runtime launch and scenario feasibility.
- Paths are recorded as temp path classes, not personal absolute paths.
- Replacement-candidate readiness remains a P15.7 decision.
- Phase 5 remains the accepted public baseline until a later replacement acceptance decision.
