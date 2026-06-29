"""Build P12.5 MP11 scenario-smoke QA."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_ID = "tfl6_mp11_candidate_p12_5_harvest_smoke200k"
DEFAULT_STAGE_LABEL = "p12_5_harvest_smoke200k"
DEFAULT_SCENARIO_TARGET = "product.HarvestedVolume.managed.Total.CC"
DEFAULT_FLOW_TARGET = f"flow.even.{DEFAULT_SCENARIO_TARGET}"
DEFAULT_STAGE_DIR = (
    INSTANCE_ROOT
    / "models"
    / "tfl6_patchworks_model_mp11_candidate"
    / "analysis"
    / DEFAULT_STAGE_LABEL
)
DEFAULT_MANIFEST_PATH = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_manifest-{DEFAULT_RUN_ID}.json"
)
DEFAULT_STDOUT_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_stdout-{DEFAULT_RUN_ID}.log"
)
DEFAULT_STDERR_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_stderr-{DEFAULT_RUN_ID}.log"
)
DEFAULT_TRACE_LOG = (
    INSTANCE_ROOT
    / "runtime"
    / "logs"
    / f"patchworks_headless_trace-{DEFAULT_RUN_ID}.log"
)
DEFAULT_DIRECT_LAUNCH_QA_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_direct_launch_qa.json"
)
DEFAULT_OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_scenario_smoke_qa.csv"
DEFAULT_OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_scenario_smoke_qa.json"
DEFAULT_OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_scenario_smoke_qa.md"


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required scenario-smoke input missing: {_repo_relative(path)}"
        )
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"Required scenario-smoke log missing: {_repo_relative(path)}"
        )
    return path.read_text(encoding="utf-8", errors="replace")


def _log_scan(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    lowered = text.lower()
    return {
        "path": _repo_relative(path),
        "bytes": path.stat().st_size,
        "error": lowered.count("error"),
        "warning": lowered.count("warning"),
        "exception": lowered.count("exception"),
        "failed": lowered.count("failed"),
    }


def _read_stage_csv(stage_dir: Path, name: str) -> pd.DataFrame:
    path = stage_dir / "scenario" / name
    if not path.exists():
        raise FileNotFoundError(
            f"Required scenario CSV missing: {_repo_relative(path)}"
        )
    return pd.read_csv(path)


def _stage_file_count(stage_dir: Path) -> int:
    if not stage_dir.exists():
        raise FileNotFoundError(
            f"Saved-stage directory missing: {_repo_relative(stage_dir)}"
        )
    return sum(1 for path in stage_dir.rglob("*") if path.is_file())


def _target_status(status: pd.DataFrame, target: str) -> dict[str, Any]:
    rows = status[status["TARGET"] == target]
    if rows.empty:
        raise ValueError(f"Target status not found: {target}")
    row = rows.iloc[0]
    return {
        "target": target,
        "periods": int(row["PERIODS"]),
        "active": bool(row["ACTIVE"]),
        "minactive": bool(row["MINACTIVE"]),
        "maxactive": bool(row["MAXACTIVE"]),
        "linear": bool(row["LINEAR"]),
        "premultiply": bool(row["PREMULTIPLY"]),
    }


def _target_summary(summary: pd.DataFrame, target: str) -> pd.DataFrame:
    rows = summary[summary["TARGET"] == target].copy()
    if rows.empty:
        raise ValueError(f"Target summary not found: {target}")
    return rows


def _sanitize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
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
            "stage_label": manifest.get("inputs", {}).get("stage_label"),
            "iterations": manifest.get("inputs", {}).get("iterations"),
            "scenario_mode": manifest.get("inputs", {}).get("scenario_mode"),
            "scenario_target": manifest.get("inputs", {}).get("scenario_target"),
            "scenario_min_annual": manifest.get("inputs", {}).get(
                "scenario_min_annual"
            ),
        },
        "outputs": {
            "stage_dir": _repo_relative(
                Path(manifest.get("outputs", {}).get("stage_dir"))
            ),
            "saved_file_count": manifest.get("outputs", {}).get("saved_file_count"),
        },
    }


def _write_outputs(
    *,
    payload: dict[str, Any],
    output_csv: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for key, value in payload["summary"].items():
            writer.writerow({"metric": key, "value": value})
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    lines = [
        "# P12.5 MP11 Scenario Smoke QA",
        "",
        "This QA record inspects the representative MP11 candidate scenario-smoke",
        "run after direct launch passed.",
        "",
        "The run uses a high base harvested-volume target to seed the schedule,",
        "then activates the even-flow target for the long scheduler run.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            "",
            "## Target Configuration",
            "",
            "- Base harvested-volume target is active, minimum-active, linear, and",
            "  configured at `20,000,000` per period.",
            "- The base target carries nonzero final-period current volume.",
            "- Even-flow target is active, min/max active, non-linear, and uses",
            "  min/max weights `10,000` for all periods.",
            "- Trace log records base-target priming before even-flow activation.",
            "",
            "## Schedule Signal",
            "",
            "- `schedule.csv` is non-empty.",
            "- Scheduled rows are all `MANAGED` / `CC` in this candidate scaffold.",
            "- Scenario smoke remains a runtime feasibility check, not an AAC",
            "  calibration or WFP-model-equivalence claim.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_qa(
    *,
    stage_dir: Path = DEFAULT_STAGE_DIR,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    stdout_log: Path = DEFAULT_STDOUT_LOG,
    stderr_log: Path = DEFAULT_STDERR_LOG,
    trace_log: Path = DEFAULT_TRACE_LOG,
    direct_launch_qa_json: Path = DEFAULT_DIRECT_LAUNCH_QA_JSON,
    scenario_target: str = DEFAULT_SCENARIO_TARGET,
    flow_target: str = DEFAULT_FLOW_TARGET,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    direct_launch_qa = _load_json(direct_launch_qa_json)
    trace_text = _read_text(trace_log)
    stdout_scan = _log_scan(stdout_log)
    stderr_scan = _log_scan(stderr_log)
    status = _read_stage_csv(stage_dir, "targetStatus.csv")
    summary_table = _read_stage_csv(stage_dir, "targetSummary.csv")
    schedule = _read_stage_csv(stage_dir, "schedule.csv")
    stage_file_count = _stage_file_count(stage_dir)

    base_status = _target_status(status, scenario_target)
    flow_status = _target_status(status, flow_target)
    base_summary = _target_summary(summary_table, scenario_target)
    flow_summary = _target_summary(summary_table, flow_target)
    final_base = base_summary.sort_values("PERIOD").iloc[-1]
    base_minimum_all_20m = bool((base_summary["MINIMUM"] == 20000000.0).all())
    flow_weights_all_10000 = bool(
        (flow_summary["MINWEIGHT"] == 10000.0).all()
        and (flow_summary["MAXWEIGHT"] == 10000.0).all()
    )
    trace_has_base_config = "configured base harvest target=" in trace_text
    trace_has_priming = "base harvest target priming completed" in trace_text
    trace_has_evenflow = "configured even-flow target=" in trace_text
    trace_order_ok = (
        trace_text.find("configured base harvest target=")
        < trace_text.find("base harvest target priming completed")
        < trace_text.find("configured even-flow target=")
    )
    scheduled_types = sorted(schedule["TYPE"].astype(str).unique().tolist())
    scheduled_treatments = sorted(schedule["TREATMENT"].astype(str).unique().tolist())
    no_log_errors = all(
        scan[key] == 0
        for scan in (stdout_scan, stderr_scan)
        for key in ("error", "warning", "exception", "failed")
    )

    qa_status = (
        "scenario_smoke_pass"
        if all(
            [
                direct_launch_qa["summary"]["qa_status"] == "direct_launch_smoke_pass",
                manifest.get("returncode") == 0,
                manifest.get("raw_returncode") == 0,
                manifest.get("headless_automation", {}).get("terminal_state")
                == "success",
                manifest.get("headless_automation", {}).get("detected_marker")
                == "[FEMIC headless] saveStage completed",
                manifest.get("inputs", {}).get("iterations") == 200000,
                manifest.get("inputs", {}).get("scenario_min_annual") == 20000000.0,
                base_status["active"],
                base_status["minactive"],
                not base_status["maxactive"],
                base_status["linear"],
                base_minimum_all_20m,
                float(final_base["CURRENT"]) > 0.0,
                flow_status["active"],
                flow_status["minactive"],
                flow_status["maxactive"],
                not flow_status["linear"],
                flow_weights_all_10000,
                trace_has_base_config,
                trace_has_priming,
                trace_has_evenflow,
                trace_order_ok,
                len(schedule) > 0,
                scheduled_types == ["MANAGED"],
                scheduled_treatments == ["CC"],
                no_log_errors,
                stage_file_count == manifest.get("outputs", {}).get("saved_file_count"),
            ]
        )
        else "scenario_smoke_needs_review"
    )

    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "qa_status": qa_status,
        "run_id": manifest["run_id"],
        "raw_returncode": manifest.get("raw_returncode"),
        "returncode": manifest.get("returncode"),
        "terminal_state": manifest.get("headless_automation", {}).get("terminal_state"),
        "detected_marker": manifest.get("headless_automation", {}).get(
            "detected_marker"
        ),
        "scenario_mode": manifest.get("inputs", {}).get("scenario_mode"),
        "scenario_target": scenario_target,
        "flow_target": flow_target,
        "iterations": manifest.get("inputs", {}).get("iterations"),
        "scenario_min_annual": manifest.get("inputs", {}).get("scenario_min_annual"),
        "stage_dir": _repo_relative(stage_dir),
        "saved_file_count": manifest.get("outputs", {}).get("saved_file_count"),
        "stage_file_count": stage_file_count,
        "target_status_rows": int(len(status)),
        "target_summary_rows": int(len(summary_table)),
        "schedule_rows": int(len(schedule)),
        "scheduled_types": ",".join(scheduled_types),
        "scheduled_treatments": ",".join(scheduled_treatments),
        "base_target_active": base_status["active"],
        "base_target_minactive": base_status["minactive"],
        "base_target_maxactive": base_status["maxactive"],
        "base_target_linear": base_status["linear"],
        "base_minimum_all_20m": base_minimum_all_20m,
        "base_final_period_current": round(float(final_base["CURRENT"]), 6),
        "flow_target_active": flow_status["active"],
        "flow_target_minactive": flow_status["minactive"],
        "flow_target_maxactive": flow_status["maxactive"],
        "flow_target_linear": flow_status["linear"],
        "flow_weights_all_10000": flow_weights_all_10000,
        "trace_order_ok": trace_order_ok,
        "stdout_error_count": stdout_scan["error"],
        "stderr_error_count": stderr_scan["error"],
        "stdout_warning_count": stdout_scan["warning"],
        "stderr_warning_count": stderr_scan["warning"],
        "release_qa": "not_performed",
    }
    payload = {
        "summary": summary,
        "manifest": _sanitize_manifest(manifest),
        "target_status": {"base": base_status, "flow": flow_status},
        "target_summary": {
            "base_final_period": final_base.to_dict(),
            "base_minimum_unique": sorted(base_summary["MINIMUM"].unique().tolist()),
            "flow_minweight_unique": sorted(
                flow_summary["MINWEIGHT"].unique().tolist()
            ),
            "flow_maxweight_unique": sorted(
                flow_summary["MAXWEIGHT"].unique().tolist()
            ),
        },
        "schedule": {
            "rows": int(len(schedule)),
            "types": scheduled_types,
            "treatments": scheduled_treatments,
        },
        "trace_checks": {
            "base_config": trace_has_base_config,
            "priming": trace_has_priming,
            "evenflow": trace_has_evenflow,
            "order_ok": trace_order_ok,
        },
        "log_scan": {"stdout": stdout_scan, "stderr": stderr_scan},
        "source_manifests": {
            "headless_manifest": _repo_relative(manifest_path),
            "direct_launch_qa": _repo_relative(direct_launch_qa_json),
        },
    }
    _write_outputs(
        payload=payload,
        output_csv=output_csv,
        output_json=output_json,
        output_md=output_md,
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage-dir", type=Path, default=DEFAULT_STAGE_DIR)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--stdout-log", type=Path, default=DEFAULT_STDOUT_LOG)
    parser.add_argument("--stderr-log", type=Path, default=DEFAULT_STDERR_LOG)
    parser.add_argument("--trace-log", type=Path, default=DEFAULT_TRACE_LOG)
    parser.add_argument(
        "--direct-launch-qa-json", type=Path, default=DEFAULT_DIRECT_LAUNCH_QA_JSON
    )
    parser.add_argument("--scenario-target", default=DEFAULT_SCENARIO_TARGET)
    parser.add_argument("--flow-target", default=DEFAULT_FLOW_TARGET)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_qa(
        stage_dir=args.stage_dir,
        manifest_path=args.manifest_path,
        stdout_log=args.stdout_log,
        stderr_log=args.stderr_log,
        trace_log=args.trace_log,
        direct_launch_qa_json=args.direct_launch_qa_json,
        scenario_target=args.scenario_target,
        flow_target=args.flow_target,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
