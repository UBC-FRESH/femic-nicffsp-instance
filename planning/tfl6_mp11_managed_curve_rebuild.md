# TFL 6 MP11 Managed Curve Rebuild Status

## Purpose

This P10R.4 artifact records whether MP11 managed curve generation can 
run from the P10R.3 handoff candidates. It is a toolchain status and 
blocker package, not a generated curve output.

## Status

- Handoff candidate rows: `27`
- Blocked or review rows outside handoff: `114`
- Curve-generation status: `ready_for_manual_tool_execution_review`
- Found executables/runners: `1`

## Toolchain Finding

FEMIC resolved a BatchTIPSY/TIPSY executable. This script does not invoke it automatically; P10R.4 curve generation must use the existing FEMIC BTC runner so command construction, scratch/log layout, report-template handling, and provenance stay on the supported parent-package contract.

## Searched Paths

- `explicit --btc-exe / FEMIC_BATCHTIPSY_EXE`
- `C:\Program Files\TIPSY 4.7\BTC\TIPSYbtc.exe`

## Candidate Row Status

| feature_id | mp11_au_code | curve_lane | curve_generation_status | output_curve_rows |
| --- | --- | --- | --- | --- |
| 611143 | Fvh101 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611153 | Fvh103 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611163 | Fvh104 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611173 | Fvh104s | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611183 | Fvh106 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611193 | Fvh108 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611203 | Fvh113 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611213 | Fvm101 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611223 | Fvm101s | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611233 | Fvm103 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611243 | Fvm104 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611253 | Fvm105 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611263 | Fvm106 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611273 | Fvm106s | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611283 | Fvm107 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611293 | Fvm109 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611303 | Fvm111 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611313 | Fvm114 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611323 | Fvm131 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611333 | Fvm133 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611343 | Fvm201 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611353 | Fvm203 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611373 | Fvm207 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611383 | Fvm208 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611393 | Fvm211 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611403 | FMH01 | future_managed | ready_for_manual_tool_execution_review | 0 |
| 611413 | FMH22 | future_managed | ready_for_manual_tool_execution_review | 0 |

## Required Next Action

Run P10R.4 through FEMIC's existing BTC runner, e.g. `python -m femic tipsy run-btc <candidate-input.csv> --run-id p10r_mp11_candidate --instance-root .`, then inspect the generated 04_output/04_error CSVs and BTC manifest before parsing or promoting curve outputs.

## Use Boundary

This artifact is a blocker package. It does not contain generated curves and must not be treated as an MP11 managed-curve rebuild.
