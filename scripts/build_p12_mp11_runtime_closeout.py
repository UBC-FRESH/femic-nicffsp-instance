"""Build the TFL 6 MP11 Phase 12 runtime-smoke closeout manifests."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "planning"

MATRIX_QA = PLANNING / "tfl6_mp11_matrix_builder_tracks_qa.json"
RUNTIME_PACKAGE = PLANNING / "tfl6_mp11_runtime_package_manifest.json"
DIRECT_LAUNCH_QA = PLANNING / "tfl6_mp11_direct_launch_qa.json"
SCENARIO_QA = PLANNING / "tfl6_mp11_scenario_smoke_qa.json"

OUT_JSON = PLANNING / "tfl6_mp11_phase12_runtime_closeout.json"
OUT_CSV = PLANNING / "tfl6_mp11_phase12_runtime_closeout.csv"
OUT_MD = PLANNING / "tfl6_mp11_phase12_runtime_closeout.md"


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _bool_status(value: bool) -> str:
    return "present" if value else "missing"


def build_closeout() -> dict[str, Any]:
    matrix = _read_json(MATRIX_QA)
    package = _read_json(RUNTIME_PACKAGE)
    launch = _read_json(DIRECT_LAUNCH_QA)
    scenario = _read_json(SCENARIO_QA)

    matrix_summary = matrix["summary"]
    package_summary = package["summary"]
    launch_summary = launch["summary"]
    scenario_summary = scenario["summary"]

    stage_paths = [
        ROOT / scenario_summary["stage_dir"] / "scenario" / "schedule.csv",
        ROOT / scenario_summary["stage_dir"] / "scenario" / "targetStatus.csv",
        ROOT / scenario_summary["stage_dir"] / "scenario" / "targetSummary.csv",
        ROOT / launch_summary["stage_dir"] / "scenario" / "targetStatus.csv",
        ROOT / launch_summary["stage_dir"] / "scenario" / "targetSummary.csv",
    ]
    generated_paths = [
        ROOT / "models/tfl6_patchworks_model_mp11_candidate/tracks/features.csv",
        ROOT / "models/tfl6_patchworks_model_mp11_candidate/tracks/accounts.csv",
        ROOT / "models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.shp",
        ROOT
        / "models/tfl6_patchworks_model_mp11_candidate/blocks/topology_blocks_200r.csv",
    ]

    hard_checks = {
        "matrix_builder_tracks": matrix_summary["qa_status"]
        == "matrix_builder_tracks_generated_inspection_pass",
        "runtime_package_manifest": package_summary["runtime_package_status"]
        == "candidate_runtime_package_assembled_pending_launch_smoke",
        "direct_launch_smoke": launch_summary["qa_status"]
        == "direct_launch_smoke_pass",
        "scenario_smoke": scenario_summary["qa_status"] == "scenario_smoke_pass",
        "scenario_trace_order": bool(scenario_summary["trace_order_ok"]),
        "scenario_saved_outputs": all(path.exists() for path in stage_paths),
        "generated_runtime_outputs": all(path.exists() for path in generated_paths),
        "no_logged_warning_error_matches": (
            scenario_summary["stdout_error_count"] == 0
            and scenario_summary["stderr_error_count"] == 0
            and scenario_summary["stdout_warning_count"] == 0
            and scenario_summary["stderr_warning_count"] == 0
            and launch_summary["stdout_error_count"] == 0
            and launch_summary["stderr_error_count"] == 0
            and launch_summary["stdout_warning_count"] == 0
            and launch_summary["stderr_warning_count"] == 0
        ),
    }

    closeout_status = (
        "candidate_runtime_smoke_pass_phase13_ready"
        if all(hard_checks.values())
        else "candidate_runtime_smoke_blocked"
    )

    phase13_inputs = [
        {
            "name": "candidate_runtime_package",
            "path": "models/tfl6_patchworks_model_mp11_candidate/",
            "status": "candidate_smoke_passed",
        },
        {
            "name": "matrix_builder_tracks_qa",
            "path": "planning/tfl6_mp11_matrix_builder_tracks_qa.{csv,json,md}",
            "status": matrix_summary["qa_status"],
        },
        {
            "name": "runtime_package_manifest",
            "path": "planning/tfl6_mp11_runtime_package_manifest.{csv,json,md}",
            "status": package_summary["runtime_package_status"],
        },
        {
            "name": "direct_launch_qa",
            "path": "planning/tfl6_mp11_direct_launch_qa.{csv,json,md}",
            "status": launch_summary["qa_status"],
        },
        {
            "name": "scenario_smoke_qa",
            "path": "planning/tfl6_mp11_scenario_smoke_qa.{csv,json,md}",
            "status": scenario_summary["qa_status"],
        },
        {
            "name": "lineage_registry",
            "path": "models/tfl6_patchworks_model_mp11_candidate/lineage_registry.yaml",
            "status": "updated_for_phase12_closeout",
        },
    ]

    caveats = [
        "Phase 12 proves candidate runtime buildability and smoke behavior, not final MP11 release readiness.",
        "The Phase 5 stand universe and treatment/transition scaffold remain reused.",
        "P9RF source/THLB caveats remain visible until a later public-source rebuild resolves or replaces them.",
        "Tables 54/55 remain excluded until a public-safe AU-code mapping exists.",
        "Harvest-system assignment remains deferred comparison metadata, not a stand-level treatment classifier.",
        "Release archive QA, documentation publication, scenario comparison, and Phase 5 replacement decisions are Phase 13 work.",
        "WFP model equivalence and approved AAC claims are out of scope for Phase 12.",
    ]

    return {
        "summary": {
            "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "phase": "P12.6",
            "closeout_status": closeout_status,
            "parent_issue": "#69",
            "child_issue": "#119",
            "matrix_run_id": matrix_summary["run_id"],
            "matrix_qa_status": matrix_summary["qa_status"],
            "track_file_count": matrix_summary["track_file_count"],
            "features_rows": matrix_summary["features_rows"],
            "accounts_rows": matrix_summary["accounts_rows"],
            "products_rows": matrix_summary["products_rows"],
            "matrix_messages_rows": matrix_summary["messages_rows"],
            "runtime_model_root": package_summary["model_root"],
            "block_rows": package_summary["block_rows"],
            "block_area_ha": package_summary["block_area_ha"],
            "topology_rows": package_summary["topology_rows"],
            "direct_launch_run_id": launch_summary["run_id"],
            "direct_launch_status": launch_summary["qa_status"],
            "direct_launch_saved_file_count": launch_summary["saved_file_count"],
            "scenario_run_id": scenario_summary["run_id"],
            "scenario_status": scenario_summary["qa_status"],
            "scenario_iterations": scenario_summary["iterations"],
            "scenario_schedule_rows": scenario_summary["schedule_rows"],
            "scenario_scheduled_types": scenario_summary["scheduled_types"],
            "scenario_scheduled_treatments": scenario_summary["scheduled_treatments"],
            "scenario_base_target_linear": scenario_summary["base_target_linear"],
            "scenario_base_minimum_all_20m": scenario_summary["base_minimum_all_20m"],
            "scenario_base_final_period_current": scenario_summary[
                "base_final_period_current"
            ],
            "scenario_flow_target_linear": scenario_summary["flow_target_linear"],
            "scenario_flow_weights_all_10000": scenario_summary[
                "flow_weights_all_10000"
            ],
            "release_qa": "not_performed",
            "phase13_handoff": "ready" if all(hard_checks.values()) else "blocked",
        },
        "hard_checks": hard_checks,
        "output_presence": {
            str(path.relative_to(ROOT)).replace("\\", "/"): _bool_status(path.exists())
            for path in [*generated_paths, *stage_paths]
        },
        "phase13_inputs": phase13_inputs,
        "caveats": caveats,
    }


def write_json(data: dict[str, Any]) -> None:
    with OUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def write_csv(data: dict[str, Any]) -> None:
    rows = [{"key": key, "value": value} for key, value in data["summary"].items()]
    rows.extend(
        {"key": f"hard_check.{key}", "value": value}
        for key, value in data["hard_checks"].items()
    )
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value"])
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(data: dict[str, Any]) -> None:
    summary = data["summary"]
    checks = data["hard_checks"]
    lines = [
        "# TFL 6 MP11 Phase 12 Runtime Closeout",
        "",
        "This note closes the Phase 12 MP11 candidate Patchworks runtime-smoke lane and hands the candidate runtime package to Phase 13 comparison documentation and release QA. Phase 12 built and smoke-tested a candidate runtime; it did not perform release QA, publish a release archive, calibrate an AAC recommendation, or claim equivalence with Western Forest Products' internal model.",
        "",
        "## Summary",
        "",
        f"- closeout_status: `{summary['closeout_status']}`",
        f"- parent_issue: `{summary['parent_issue']}`",
        f"- child_issue: `{summary['child_issue']}`",
        f"- matrix_run_id: `{summary['matrix_run_id']}`",
        f"- direct_launch_run_id: `{summary['direct_launch_run_id']}`",
        f"- scenario_run_id: `{summary['scenario_run_id']}`",
        f"- release_qa: `{summary['release_qa']}`",
        f"- phase13_handoff: `{summary['phase13_handoff']}`",
        "",
        "## Runtime Evidence",
        "",
        "| Surface | Evidence | Status |",
        "| --- | --- | --- |",
        f"| Matrix Builder tracks | `{summary['track_file_count']}` track files; `{summary['features_rows']}` feature rows; `{summary['accounts_rows']}` account rows; `{summary['products_rows']}` product rows; `{summary['matrix_messages_rows']}` message rows | `{summary['matrix_qa_status']}` |",
        f"| Runtime blocks/topology | `{summary['block_rows']}` block rows; `{summary['block_area_ha']}` ha; `{summary['topology_rows']}` topology rows | `candidate_runtime_package_assembled` |",
        f"| Direct launch smoke | `{summary['direct_launch_saved_file_count']}` saved-stage files | `{summary['direct_launch_status']}` |",
        f"| Scenario smoke | `{summary['scenario_iterations']}` iterations; `{summary['scenario_schedule_rows']}` scheduled rows; `{summary['scenario_scheduled_types']}` / `{summary['scenario_scheduled_treatments']}` | `{summary['scenario_status']}` |",
        "",
        "## Scenario Target Evidence",
        "",
        "- The base harvested-volume target used a linear penalty shape and a `20,000,000` per-period minimum.",
        "- The scheduler primed harvested volume before even-flow activation, as recorded in `planning/tfl6_mp11_scenario_smoke_qa.json`.",
        "- The even-flow target retained the default non-linear penalty shape with min/max weights `10,000` for all periods.",
        f"- The final-period base harvested-volume current value was `{summary['scenario_base_final_period_current']}`.",
        "",
        "## Hard Checks",
        "",
        "| Check | Result |",
        "| --- | --- |",
    ]
    lines.extend(f"| `{key}` | `{value}` |" for key, value in checks.items())
    lines.extend(
        [
            "",
            "## Phase 13 Inputs",
            "",
            "| Input | Path | Status |",
            "| --- | --- | --- |",
        ]
    )
    lines.extend(
        f"| `{item['name']}` | `{item['path']}` | `{item['status']}` |"
        for item in data["phase13_inputs"]
    )
    lines.extend(["", "## Caveats", ""])
    lines.extend(f"- {caveat}" for caveat in data["caveats"])
    lines.extend(
        [
            "",
            "## Phase 13 Boundary",
            "",
            "Phase 13 should consume this candidate runtime as a smoke-tested rebuild artifact and decide whether it is suitable for comparison documentation, release packaging, teaching updates, and replacement/supplement positioning relative to the completed Phase 5 runtime baseline. Phase 13 must keep the Phase 5 baseline preserved until release QA and publication decisions explicitly pass.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = build_closeout()
    write_json(data)
    write_csv(data)
    write_markdown(data)
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"closeout_status={data['summary']['closeout_status']}")


if __name__ == "__main__":
    main()
