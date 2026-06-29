"""Build P15.5 materialized runtime smoke QA."""

from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "planning" / "tfl6_mp11_phase15_materialized_runtime_smoke_qa.csv"
OUT_JSON = ROOT / "planning" / "tfl6_mp11_phase15_materialized_runtime_smoke_qa.json"
OUT_MD = ROOT / "planning" / "tfl6_mp11_phase15_materialized_runtime_smoke_qa.md"

SCENARIO_TARGET = "product.HarvestedVolume.managed.Total.CC"
FLOW_TARGET = f"flow.even.{SCENARIO_TARGET}"

RUNS: dict[str, dict[str, Any]] = {
    "direct_launch": {
        "run_id": "tfl6_mp11_harvest_system_p15_5_archive_launch0",
        "stage_label": "p15_5_archive_launch0",
        "expected_iterations": 0,
        "scenario_mode": "none",
        "expected_treatments": [],
        "forbidden_treatments": [],
    },
    "all_system": {
        "run_id": "tfl6_mp11_harvest_system_p15_5_archive_all_system_200k",
        "stage_label": "p15_5_archive_all_system_200k",
        "expected_iterations": 200000,
        "scenario_mode": "max-even-flow-smoke",
        "expected_treatments": ["CC_CABLE", "CC_GROUND", "CC_HELI"],
        "forbidden_treatments": [],
    },
    "no_heli": {
        "run_id": "tfl6_mp11_harvest_system_p15_5_archive_no_heli_200k",
        "stage_label": "p15_5_archive_no_heli_200k",
        "expected_iterations": 200000,
        "scenario_mode": "max-even-flow-smoke",
        "expected_treatments": ["CC_CABLE", "CC_GROUND"],
        "forbidden_treatments": ["CC_HELI"],
    },
}


def _load_json(path: Path) -> dict[str, Any]:
    if not _exists(path):
        raise FileNotFoundError(f"Missing manifest: {path}")
    with open(_fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def _read_text(path: Path) -> str:
    if not _exists(path):
        raise FileNotFoundError(f"Missing log: {path}")
    with open(_fs_path(path), encoding="utf-8", errors="replace") as handle:
        return handle.read()


def _csv(path: Path) -> pd.DataFrame:
    if not _exists(path):
        raise FileNotFoundError(f"Missing CSV: {path}")
    return pd.read_csv(_fs_path(path))


def _file_count(path: Path) -> int:
    if not _exists(path):
        raise FileNotFoundError(f"Missing stage directory: {path}")
    count = 0
    for _dirpath, _dirnames, filenames in os.walk(_fs_path(path)):
        count += len(filenames)
    return count


def _fs_path(path: Path) -> str:
    text = str(path.resolve())
    if os.name == "nt" and not text.startswith("\\\\?\\"):
        return "\\\\?\\" + text
    return text


def _exists(path: Path) -> bool:
    return os.path.exists(_fs_path(path))


def _log_scan(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    lowered = text.lower()
    return {
        "path_class": "temp_materialized_archive_log",
        "bytes": os.stat(_fs_path(path)).st_size,
        "error": lowered.count("error"),
        "warning": lowered.count("warning"),
        "exception": lowered.count("exception"),
        "failed": lowered.count("failed"),
    }


def _target_status(status: pd.DataFrame, target: str) -> dict[str, Any]:
    rows = status[status["TARGET"] == target]
    if rows.empty:
        return {"target": target, "present": False}
    row = rows.iloc[0]
    return {
        "target": target,
        "present": True,
        "periods": int(row["PERIODS"]),
        "active": bool(row["ACTIVE"]),
        "minactive": bool(row["MINACTIVE"]),
        "maxactive": bool(row["MAXACTIVE"]),
        "linear": bool(row["LINEAR"]),
    }


def _target_summary(summary: pd.DataFrame, target: str) -> dict[str, Any]:
    rows = summary[summary["TARGET"] == target].copy()
    if rows.empty:
        return {"target": target, "present": False}
    last = rows.sort_values("PERIOD").iloc[-1]
    return {
        "target": target,
        "present": True,
        "rows": int(len(rows)),
        "minimum_unique": sorted(float(value) for value in rows["MINIMUM"].unique()),
        "minweight_unique": sorted(float(value) for value in rows["MINWEIGHT"].unique()),
        "maxweight_unique": sorted(float(value) for value in rows["MAXWEIGHT"].unique()),
        "final_period_current": round(float(last["CURRENT"]), 6),
    }


def _inspect_run(materialized_root: Path, log_dir: Path, name: str, config: dict[str, Any]) -> dict[str, Any]:
    run_id = config["run_id"]
    stage_dir = (
        materialized_root
        / "models"
        / "tfl6_patchworks_model_mp11_harvest_system_candidate"
        / "analysis"
        / config["stage_label"]
    )
    manifest_path = log_dir / f"patchworks_headless_manifest-{run_id}.json"
    stdout_log = log_dir / f"patchworks_headless_stdout-{run_id}.log"
    stderr_log = log_dir / f"patchworks_headless_stderr-{run_id}.log"
    trace_log = log_dir / f"patchworks_headless_trace-{run_id}.log"

    manifest = _load_json(manifest_path)
    status = _csv(stage_dir / "scenario" / "targetStatus.csv")
    summary = _csv(stage_dir / "scenario" / "targetSummary.csv")
    schedule = _csv(stage_dir / "scenario" / "schedule.csv")
    stdout_scan = _log_scan(stdout_log)
    stderr_scan = _log_scan(stderr_log)
    trace_text = _read_text(trace_log)

    scheduled_treatments = (
        sorted(schedule["TREATMENT"].astype(str).unique().tolist())
        if len(schedule)
        else []
    )
    treatment_counts = (
        {
            str(key): int(value)
            for key, value in schedule["TREATMENT"].value_counts().sort_index().items()
        }
        if len(schedule)
        else {}
    )
    forbidden_present = sorted(
        treatment
        for treatment in config["forbidden_treatments"]
        if treatment in scheduled_treatments
    )
    no_log_errors = all(
        scan[key] == 0
        for scan in (stdout_scan, stderr_scan)
        for key in ("error", "warning", "exception", "failed")
    )
    stage_file_count = _file_count(stage_dir)
    base_status = _target_status(status, SCENARIO_TARGET)
    flow_status = _target_status(status, FLOW_TARGET)
    base_summary = _target_summary(summary, SCENARIO_TARGET)
    flow_summary = _target_summary(summary, FLOW_TARGET)
    expected_treatments = sorted(config["expected_treatments"])

    run_pass = all(
        [
            manifest.get("returncode") == 0,
            manifest.get("raw_returncode") == 0,
            manifest.get("headless_automation", {}).get("terminal_state") == "success",
            manifest.get("headless_automation", {}).get("detected_marker")
            == "[FEMIC headless] saveStage completed",
            manifest.get("inputs", {}).get("iterations") == config["expected_iterations"],
            manifest.get("inputs", {}).get("scenario_mode") == config["scenario_mode"],
            stage_file_count >= manifest.get("outputs", {}).get("saved_file_count", 0),
            no_log_errors,
            scheduled_treatments == expected_treatments,
            not forbidden_present,
        ]
    )
    if config["expected_iterations"] > 0:
        run_pass = run_pass and all(
            [
                len(schedule) > 0,
                base_status.get("present") is True,
                base_status.get("active") is True,
                base_status.get("minactive") is True,
                base_status.get("linear") is True,
                base_summary.get("minimum_unique") == [20000000.0],
                base_summary.get("final_period_current", 0.0) > 0.0,
                flow_status.get("present") is True,
                flow_status.get("active") is True,
                flow_status.get("minactive") is True,
                flow_status.get("maxactive") is True,
                flow_status.get("linear") is False,
                flow_summary.get("minweight_unique") == [10000.0],
                flow_summary.get("maxweight_unique") == [10000.0],
                "base harvest target priming completed" in trace_text,
            ]
        )
    else:
        run_pass = run_pass and len(schedule) == 0

    return {
        "name": name,
        "qa_status": "pass" if run_pass else "needs_review",
        "run_id": run_id,
        "stage_label": config["stage_label"],
        "stage_path_class": "temp_materialized_archive_stage",
        "raw_returncode": manifest.get("raw_returncode"),
        "returncode": manifest.get("returncode"),
        "terminal_state": manifest.get("headless_automation", {}).get("terminal_state"),
        "detected_marker": manifest.get("headless_automation", {}).get("detected_marker"),
        "iterations": manifest.get("inputs", {}).get("iterations"),
        "scenario_mode": manifest.get("inputs", {}).get("scenario_mode"),
        "scenario_target": manifest.get("inputs", {}).get("scenario_target"),
        "scenario_min_annual": manifest.get("inputs", {}).get("scenario_min_annual"),
        "stage_file_count": stage_file_count,
        "target_status_rows": int(len(status)),
        "target_summary_rows": int(len(summary)),
        "schedule_rows": int(len(schedule)),
        "scheduled_treatments": scheduled_treatments,
        "treatment_counts": treatment_counts,
        "forbidden_treatments_present": forbidden_present,
        "target_status": {"base": base_status, "flow": flow_status},
        "target_summary": {"base": base_summary, "flow": flow_summary},
        "log_scan": {"stdout": stdout_scan, "stderr": stderr_scan},
    }


def _write_outputs(payload: dict[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    for run in payload["runs"]:
        rows.extend(
            [
                {"run": run["name"], "metric": "qa_status", "value": run["qa_status"]},
                {"run": run["name"], "metric": "schedule_rows", "value": run["schedule_rows"]},
                {
                    "run": run["name"],
                    "metric": "scheduled_treatments",
                    "value": ",".join(run["scheduled_treatments"]),
                },
                {
                    "run": run["name"],
                    "metric": "forbidden_treatments_present",
                    "value": ",".join(run["forbidden_treatments_present"]) or "none",
                },
            ]
        )
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["run", "metric", "value"])
        writer.writeheader()
        writer.writerows(rows)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    lines = [
        "# TFL 6 MP11 Phase 15 Materialized Runtime Smoke QA",
        "",
        "This P15.5 report inspects Patchworks runs launched from the materialized P15 archive payload, not from the source working tree.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Runs",
            "",
            "| Run | Status | Schedule Rows | Treatments | Forbidden Present |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for run in payload["runs"]:
        lines.append(
            "| `{}` | `{}` | {} | `{}` | `{}` |".format(
                run["name"],
                run["qa_status"],
                run["schedule_rows"],
                ",".join(run["scheduled_treatments"]),
                ",".join(run["forbidden_treatments_present"]) or "none",
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- P15.5 proves archive-derived runtime launch and scenario feasibility.",
            "- Paths are recorded as temp path classes, not personal absolute paths.",
            "- Replacement-candidate readiness remains a P15.7 decision.",
            "- Phase 5 remains the accepted public baseline until a later replacement acceptance decision.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def build(materialized_root: Path, log_dir: Path) -> dict[str, Any]:
    runs = [
        _inspect_run(materialized_root, log_dir, name, config)
        for name, config in RUNS.items()
    ]
    all_pass = all(run["qa_status"] == "pass" for run in runs)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "qa_status": "materialized_runtime_smoke_pass" if all_pass else "materialized_runtime_smoke_needs_review",
        "materialized_root_class": "temp_clean_checkout_runtime_p15_materialized_archive",
        "log_dir_class": "temp_materialized_archive_log_dir",
        "direct_launch_status": runs[0]["qa_status"],
        "all_system_status": runs[1]["qa_status"],
        "no_heli_status": runs[2]["qa_status"],
        "all_system_schedule_rows": runs[1]["schedule_rows"],
        "no_heli_schedule_rows": runs[2]["schedule_rows"],
        "all_system_treatments": ",".join(runs[1]["scheduled_treatments"]),
        "no_heli_treatments": ",".join(runs[2]["scheduled_treatments"]),
        "no_heli_forbidden_present": ",".join(runs[2]["forbidden_treatments_present"]) or "none",
        "replacement_candidate_decision": "pending_p15_7",
    }
    payload = {"summary": summary, "runs": runs}
    _write_outputs(payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materialized-root", type=Path, required=True)
    parser.add_argument("--log-dir", type=Path, required=True)
    args = parser.parse_args()
    payload = build(args.materialized_root, args.log_dir)
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
