"""Build P14.7 harvest-system scenario-smoke QA."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "tfl6_patchworks_model_mp11_harvest_system_candidate"
ANALYSIS_ROOT = MODEL_ROOT / "analysis"
LOG_ROOT = ROOT / "runtime" / "logs"

OUT_CSV = ROOT / "planning" / "tfl6_mp11_phase14_scenario_smoke_qa.csv"
OUT_JSON = ROOT / "planning" / "tfl6_mp11_phase14_scenario_smoke_qa.json"
OUT_MD = ROOT / "planning" / "tfl6_mp11_phase14_scenario_smoke_qa.md"

SCENARIO_TARGET = "product.HarvestedVolume.managed.Total.CC"
FLOW_TARGET = f"flow.even.{SCENARIO_TARGET}"

RUNS: dict[str, dict[str, Any]] = {
    "direct_launch": {
        "run_id": "tfl6_mp11_harvest_system_p14_7_launch0",
        "stage_label": "p14_7_launch0",
        "expected_iterations": 0,
        "expected_treatments": [],
        "forbidden_treatments": [],
        "scenario_mode": "none",
    },
    "all_system": {
        "run_id": "tfl6_mp11_harvest_system_p14_7_all_system_200k",
        "stage_label": "p14_7_all_system_200k",
        "expected_iterations": 200000,
        "expected_treatments": ["CC_CABLE", "CC_GROUND", "CC_HELI"],
        "forbidden_treatments": [],
        "scenario_mode": "max-even-flow-smoke",
    },
    "no_heli": {
        "run_id": "tfl6_mp11_harvest_system_p14_7_no_heli_200k",
        "stage_label": "p14_7_no_heli_200k",
        "expected_iterations": 200000,
        "expected_treatments": ["CC_CABLE", "CC_GROUND"],
        "forbidden_treatments": ["CC_HELI"],
        "scenario_mode": "max-even-flow-smoke",
    },
}


def _repo(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required manifest missing: {_repo(path)}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required log missing: {_repo(path)}")
    return path.read_text(encoding="utf-8", errors="replace")


def _csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required stage CSV missing: {_repo(path)}")
    return pd.read_csv(path)


def _file_count(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(f"Required stage directory missing: {_repo(path)}")
    return sum(1 for child in path.rglob("*") if child.is_file())


def _log_scan(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    lowered = text.lower()
    return {
        "path": _repo(path),
        "bytes": path.stat().st_size,
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


def _sanitize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    outputs = manifest.get("outputs", {})
    inputs = manifest.get("inputs", {})
    return {
        "run_id": manifest["run_id"],
        "raw_returncode": manifest.get("raw_returncode"),
        "returncode": manifest.get("returncode"),
        "mode": manifest.get("mode"),
        "failures": manifest.get("failures", []),
        "headless_automation": {
            "terminal_state": manifest.get("headless_automation", {}).get(
                "terminal_state"
            ),
            "detected_marker": manifest.get("headless_automation", {}).get(
                "detected_marker"
            ),
        },
        "inputs": {
            "stage_label": inputs.get("stage_label"),
            "iterations": inputs.get("iterations"),
            "scenario_mode": inputs.get("scenario_mode"),
            "scenario_target": inputs.get("scenario_target"),
            "scenario_min_annual": inputs.get("scenario_min_annual"),
        },
        "outputs": {
            "stage_dir": _repo(Path(outputs["stage_dir"])),
            "saved_file_count": outputs.get("saved_file_count"),
        },
    }


def _inspect_run(name: str, config: dict[str, Any]) -> dict[str, Any]:
    run_id = config["run_id"]
    stage_dir = ANALYSIS_ROOT / config["stage_label"]
    manifest_path = LOG_ROOT / f"patchworks_headless_manifest-{run_id}.json"
    stdout_log = LOG_ROOT / f"patchworks_headless_stdout-{run_id}.log"
    stderr_log = LOG_ROOT / f"patchworks_headless_stderr-{run_id}.log"
    trace_log = LOG_ROOT / f"patchworks_headless_trace-{run_id}.log"

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
            key: int(value)
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
    expected_present = sorted(config["expected_treatments"]) == scheduled_treatments
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

    run_pass = all(
        [
            manifest.get("returncode") == 0,
            manifest.get("raw_returncode") == 0,
            manifest.get("headless_automation", {}).get("terminal_state") == "success",
            manifest.get("headless_automation", {}).get("detected_marker")
            == "[FEMIC headless] saveStage completed",
            manifest.get("inputs", {}).get("iterations") == config["expected_iterations"],
            manifest.get("inputs", {}).get("scenario_mode") == config["scenario_mode"],
            stage_file_count == manifest.get("outputs", {}).get("saved_file_count"),
            no_log_errors,
            not forbidden_present,
            expected_present,
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
        "manifest": _sanitize_manifest(manifest),
        "stage_dir": _repo(stage_dir),
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
        "source_manifests": {
            "headless_manifest": _repo(manifest_path),
            "stdout_log": _repo(stdout_log),
            "stderr_log": _repo(stderr_log),
            "trace_log": _repo(trace_log),
        },
    }


def _write_outputs(payload: dict[str, Any]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for run in payload["runs"]:
        rows.extend(
            [
                {"run": run["name"], "metric": "qa_status", "value": run["qa_status"]},
                {
                    "run": run["name"],
                    "metric": "schedule_rows",
                    "value": run["schedule_rows"],
                },
                {
                    "run": run["name"],
                    "metric": "scheduled_treatments",
                    "value": ",".join(run["scheduled_treatments"]),
                },
                {
                    "run": run["name"],
                    "metric": "forbidden_treatments_present",
                    "value": ",".join(run["forbidden_treatments_present"]),
                },
                {
                    "run": run["name"],
                    "metric": "saved_file_count",
                    "value": run["manifest"]["outputs"]["saved_file_count"],
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
        "# TFL 6 MP11 Phase 14 Scenario Smoke QA",
        "",
        "This report inspects the P14.7 Patchworks harvest-system runtime smoke runs.",
        "It verifies direct launch, all-system scheduling, and a no-heli track variant.",
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
            "| `{name}` | `{status}` | {rows} | `{treatments}` | `{forbidden}` |".format(
                name=run["name"],
                status=run["qa_status"],
                rows=run["schedule_rows"],
                treatments=",".join(run["scheduled_treatments"]),
                forbidden=",".join(run["forbidden_treatments_present"]) or "none",
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- P14.7 is runtime smoke, not release QA.",
            "- The no-heli run uses generated ignored `tracks_no_heli/` tracks.",
            "- The all-system runtime keeps the P14.6 `tracks/` outputs intact.",
            "- These runs do not claim WFP-model equivalence or approved AAC status.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def build() -> dict[str, Any]:
    runs = [_inspect_run(name, config) for name, config in RUNS.items()]
    all_pass = all(run["qa_status"] == "pass" for run in runs)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "qa_status": "p14_7_smoke_pass" if all_pass else "p14_7_smoke_needs_review",
        "direct_launch_status": runs[0]["qa_status"],
        "all_system_status": runs[1]["qa_status"],
        "no_heli_status": runs[2]["qa_status"],
        "all_system_schedule_rows": runs[1]["schedule_rows"],
        "no_heli_schedule_rows": runs[2]["schedule_rows"],
        "all_system_treatments": ",".join(runs[1]["scheduled_treatments"]),
        "no_heli_treatments": ",".join(runs[2]["scheduled_treatments"]),
        "no_heli_forbidden_present": ",".join(
            runs[2]["forbidden_treatments_present"]
        )
        or "none",
        "release_qa": "not_performed",
    }
    payload = {"summary": summary, "runs": runs}
    _write_outputs(payload)
    return payload


def main() -> None:
    payload = build()
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
