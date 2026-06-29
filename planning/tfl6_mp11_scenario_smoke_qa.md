# P12.5 MP11 Scenario Smoke QA

This QA record inspects the representative MP11 candidate scenario-smoke
run after direct launch passed.

The run uses a high base harvested-volume target to seed the schedule,
then activates the even-flow target for the long scheduler run.

## Summary

- generated_at_utc: `2026-06-29T04:52:48+00:00`
- qa_status: `scenario_smoke_pass`
- run_id: `tfl6_mp11_candidate_p12_5_harvest_smoke200k`
- raw_returncode: `0`
- returncode: `0`
- terminal_state: `success`
- detected_marker: `[FEMIC headless] saveStage completed`
- scenario_mode: `max-even-flow-smoke`
- scenario_target: `product.HarvestedVolume.managed.Total.CC`
- flow_target: `flow.even.product.HarvestedVolume.managed.Total.CC`
- iterations: `200000`
- scenario_min_annual: `20000000.0`
- stage_dir: `models/tfl6_patchworks_model_mp11_candidate/analysis/p12_5_harvest_smoke200k`
- saved_file_count: `3359`
- stage_file_count: `3359`
- target_status_rows: `824`
- target_summary_rows: `25544`
- schedule_rows: `76726`
- scheduled_types: `MANAGED`
- scheduled_treatments: `CC`
- base_target_active: `True`
- base_target_minactive: `True`
- base_target_maxactive: `False`
- base_target_linear: `True`
- base_minimum_all_20m: `True`
- base_final_period_current: `14104784.0`
- flow_target_active: `True`
- flow_target_minactive: `True`
- flow_target_maxactive: `True`
- flow_target_linear: `False`
- flow_weights_all_10000: `True`
- trace_order_ok: `True`
- stdout_error_count: `0`
- stderr_error_count: `0`
- stdout_warning_count: `0`
- stderr_warning_count: `0`
- release_qa: `not_performed`

## Target Configuration

- Base harvested-volume target is active, minimum-active, linear, and
  configured at `20,000,000` per period.
- The base target carries nonzero final-period current volume.
- Even-flow target is active, min/max active, non-linear, and uses
  min/max weights `10,000` for all periods.
- Trace log records base-target priming before even-flow activation.

## Schedule Signal

- `schedule.csv` is non-empty.
- Scheduled rows are all `MANAGED` / `CC` in this candidate scaffold.
- Scenario smoke remains a runtime feasibility check, not an AAC
  calibration or WFP-model-equivalence claim.
