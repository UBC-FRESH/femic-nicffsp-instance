# TFL 6 MP11 Phase 14 Scenario Smoke QA

This report inspects the P14.7 Patchworks harvest-system runtime smoke runs.
It verifies direct launch, all-system scheduling, and a no-heli track variant.

## Summary

- generated_at_utc: `2026-06-29T06:54:01+00:00`
- qa_status: `p14_7_smoke_pass`
- direct_launch_status: `pass`
- all_system_status: `pass`
- no_heli_status: `pass`
- all_system_schedule_rows: `76635`
- no_heli_schedule_rows: `75086`
- all_system_treatments: `CC_CABLE,CC_GROUND,CC_HELI`
- no_heli_treatments: `CC_CABLE,CC_GROUND`
- no_heli_forbidden_present: `none`
- release_qa: `not_performed`

## Runs

| Run | Status | Schedule Rows | Treatments | Forbidden Present |
| --- | --- | ---: | --- | --- |
| `direct_launch` | `pass` | 0 | `` | `none` |
| `all_system` | `pass` | 76635 | `CC_CABLE,CC_GROUND,CC_HELI` | `none` |
| `no_heli` | `pass` | 75086 | `CC_CABLE,CC_GROUND` | `none` |

## Boundary

- P14.7 is runtime smoke, not release QA.
- The no-heli run uses generated ignored `tracks_no_heli/` tracks.
- The all-system runtime keeps the P14.6 `tracks/` outputs intact.
- These runs do not claim WFP-model equivalence or approved AAC status.
