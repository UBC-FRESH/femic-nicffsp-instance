"""Run the locked P10R MP11 managed-curve generation recipe."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
PARENT_REPO_ROOT = INSTANCE_ROOT.parents[1]
PLANNING_ROOT = INSTANCE_ROOT / "planning"
MANAGED_PLOT_DIR = INSTANCE_ROOT / "plots" / "mp11_managed_curve_comparison"
TIPSY_VDYP_PLOT_DIR = INSTANCE_ROOT / "plots" / "mp11_tipsy_vdyp_diagnostics"

HANDOFF = PLANNING_ROOT / "tfl6_mp11_tipsy_handoff.csv"
HANDOFF_MAP = PLANNING_ROOT / "tfl6_mp11_tipsy_handoff_map.csv"
MANAGED_CURVES = PLANNING_ROOT / "tfl6_mp11_managed_curves.csv"
COMPARISON = PLANNING_ROOT / "tfl6_mp11_managed_curve_comparison.csv"
MANAGED_PLOT_MANIFEST = PLANNING_ROOT / "tfl6_mp11_managed_curve_plot_manifest.csv"
DIAGNOSTIC_MANIFEST = PLANNING_ROOT / "tfl6_mp11_tipsy_vdyp_diagnostic_manifest.csv"
BTC_OUTPUT = (
    INSTANCE_ROOT / "runtime" / "mp11_yield" / "p10r_mp11_candidate_04_output.csv"
)
BTC_ERROR = (
    INSTANCE_ROOT / "runtime" / "mp11_yield" / "p10r_mp11_candidate_04_error.csv"
)
BTC_MANIFEST = (
    INSTANCE_ROOT
    / "runtime"
    / "mp11_yield"
    / "logs"
    / "btc_manifest-p10r_mp11_candidate.json"
)
LOCK_JSON = PLANNING_ROOT / "tfl6_mp11_curve_generation_recipe_lock.json"


def _repo_path(path: Path) -> str:
    try:
        return str(path.relative_to(INSTANCE_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path.relative_to(PARENT_REPO_ROOT)).replace("\\", "/")


def _sanitize_text(text: str) -> str:
    replacements = {
        str(PARENT_REPO_ROOT): "<femic_repo>",
        str(PARENT_REPO_ROOT).replace("\\", "\\\\"): "<femic_repo>",
        str(INSTANCE_ROOT): "<tfl6_instance>",
        str(INSTANCE_ROOT).replace("\\", "\\\\"): "<tfl6_instance>",
        str(Path(sys.executable)): "python",
        str(Path(sys.executable)).replace("\\", "\\\\"): "python",
    }
    sanitized = text
    for old, new in sorted(
        replacements.items(), key=lambda item: len(item[0]), reverse=True
    ):
        sanitized = sanitized.replace(old, new)
    return sanitized.replace("\\", "/")


def _display_command(command: list[str]) -> str:
    parts = ["python" if part == sys.executable else part for part in command]
    return _sanitize_text(" ".join(parts))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run(command: list[str], *, dry_run: bool = False) -> dict[str, Any]:
    display = _display_command(command)
    if dry_run:
        return {"command": display, "returncode": None, "dry_run": True}
    completed = subprocess.run(
        command,
        cwd=PARENT_REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Recipe command failed with exit code {completed.returncode}: {display}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return {
        "command": display,
        "returncode": completed.returncode,
        "stdout_tail": _sanitize_text(completed.stdout[-4000:]),
        "stderr_tail": _sanitize_text(completed.stderr[-4000:]),
    }


def _clean_plots(plot_dir: Path, *, dry_run: bool = False) -> dict[str, Any]:
    resolved_plot_dir = plot_dir.resolve()
    resolved_instance = INSTANCE_ROOT.resolve()
    if not str(resolved_plot_dir).lower().startswith(str(resolved_instance).lower()):
        raise RuntimeError(
            f"Refusing to clean outside instance root: {resolved_plot_dir}"
        )
    pngs = sorted(resolved_plot_dir.glob("*.png"))
    if not dry_run:
        for path in pngs:
            path.unlink()
    return {"plot_dir": _repo_path(plot_dir), "removed_png_count": len(pngs)}


def _validate() -> dict[str, Any]:
    handoff = pd.read_csv(HANDOFF)
    handoff_map = pd.read_csv(HANDOFF_MAP)
    curves = pd.read_csv(MANAGED_CURVES)
    comparison = pd.read_csv(COMPARISON)
    managed_plot_manifest = pd.read_csv(MANAGED_PLOT_MANIFEST)
    manifest = pd.read_csv(DIAGNOSTIC_MANIFEST)

    if not BTC_MANIFEST.exists():
        raise RuntimeError(f"Missing BTC manifest: {_repo_path(BTC_MANIFEST)}")
    btc_manifest = json.loads(BTC_MANIFEST.read_text(encoding="utf-8"))
    if (
        btc_manifest.get("status") != "ok"
        or int(btc_manifest.get("exit_code", -1)) != 0
    ):
        raise RuntimeError(f"BTC manifest is not clean: {btc_manifest}")

    error_rows = len(pd.read_csv(BTC_ERROR)) if BTC_ERROR.exists() else -1
    if error_rows != 0:
        raise RuntimeError(f"BTC error rows present: {error_rows}")

    candidate_map = handoff_map[
        handoff_map["handoff_status"].eq("candidate_for_curve_generation")
    ].copy()
    if len(handoff) != len(candidate_map):
        raise RuntimeError(
            f"Handoff row count {len(handoff)} does not match candidates {len(candidate_map)}"
        )
    if ((handoff["bec_zone"] == "MH") | (handoff["bec_subzone"] == "mm")).any():
        raise RuntimeError("BTC handoff contains MH/mm candidate rows")
    if curves["mp11_au_code"].astype(str).str.startswith("FMH").any():
        raise RuntimeError("Managed curves contain blocked FMH rows")
    if comparison["mp11_au_code"].astype(str).str.startswith("FMH").any():
        raise RuntimeError("Comparison contains blocked FMH rows")
    if managed_plot_manifest["mp11_au_code"].astype(str).str.startswith("FMH").any():
        raise RuntimeError("Managed plot manifest contains blocked FMH rows")
    if manifest["mp11_au_code"].astype(str).str.startswith("FMH").any():
        raise RuntimeError("Diagnostic manifest contains blocked FMH rows")

    si_mismatch_count = 0
    for _, map_row in candidate_map.iterrows():
        feature_id = int(map_row["feature_id"])
        btc_row = handoff[handoff["feature_id"].eq(feature_id)].iloc[0]
        expected_si = float(map_row["tipsy_input_si"])
        for column in [col for col in handoff.columns if col.endswith("_si")]:
            value = btc_row[column]
            if pd.isna(value) or str(value).strip() == "":
                continue
            numeric = float(value)
            if numeric > 0 and abs(numeric - expected_si) > 1e-9:
                si_mismatch_count += 1
    if si_mismatch_count:
        raise RuntimeError(
            f"Found {si_mismatch_count} positive SI columns not equal to tipsy_input_si"
        )

    check = comparison.merge(
        manifest[["mp11_au_code", "vdyp_au_id", "plot_exists", "plot_path"]],
        on="mp11_au_code",
        how="inner",
        validate="one_to_one",
    )
    expected_prefix = (
        check["mp11_bec_zone"].astype(str) + check["mp11_bec_subzone"].astype(str)
    ).str.lower()
    bec_ok = [
        str(au).lower().startswith(prefix)
        for au, prefix in zip(check["vdyp_au_id"], expected_prefix, strict=True)
    ]
    bec_mismatch_count = bec_ok.count(False)
    if bec_mismatch_count:
        raise RuntimeError(f"Found {bec_mismatch_count} plotted BEC mismatches")

    missing_managed_plots = []
    empty_managed_plots = []
    for rel_path in managed_plot_manifest.loc[
        managed_plot_manifest["plot_exists"].astype(bool), "plot_path"
    ]:
        path = INSTANCE_ROOT / str(rel_path)
        if not path.exists():
            missing_managed_plots.append(str(rel_path))
        elif path.stat().st_size <= 0:
            empty_managed_plots.append(str(rel_path))
    if missing_managed_plots or empty_managed_plots:
        raise RuntimeError(
            "Managed plot validation failed: "
            f"missing={missing_managed_plots} empty={empty_managed_plots}"
        )

    missing_plots = []
    empty_plots = []
    for rel_path in manifest.loc[manifest["plot_exists"].astype(bool), "plot_path"]:
        path = INSTANCE_ROOT / str(rel_path)
        if not path.exists():
            missing_plots.append(str(rel_path))
        elif path.stat().st_size <= 0:
            empty_plots.append(str(rel_path))
    if missing_plots or empty_plots:
        raise RuntimeError(
            f"Plot validation failed: missing={missing_plots} empty={empty_plots}"
        )

    return {
        "handoff_rows": int(len(handoff)),
        "candidate_rows": int(len(candidate_map)),
        "btc_manifest_status": btc_manifest.get("status"),
        "btc_exit_code": int(btc_manifest.get("exit_code", -1)),
        "btc_error_rows": int(error_rows),
        "curve_features": int(curves["feature_id"].nunique()),
        "curve_rows": int(len(curves)),
        "comparison_rows": int(len(comparison)),
        "managed_plot_manifest_rows": int(len(managed_plot_manifest)),
        "managed_plot_count": int(managed_plot_manifest["plot_exists"].sum()),
        "diagnostic_manifest_rows": int(len(manifest)),
        "diagnostic_plot_count": int(manifest["plot_exists"].sum()),
        "bec_mismatch_count": int(bec_mismatch_count),
        "si_mismatch_count": int(si_mismatch_count),
        "diagnostic_class_counts": {
            str(key): int(value)
            for key, value in manifest["diagnostic_class"]
            .value_counts()
            .sort_index()
            .items()
        },
    }


def _artifact_hashes() -> dict[str, str]:
    artifacts = [
        HANDOFF,
        HANDOFF_MAP,
        MANAGED_CURVES,
        COMPARISON,
        MANAGED_PLOT_MANIFEST,
        DIAGNOSTIC_MANIFEST,
        BTC_OUTPUT,
        BTC_ERROR,
        BTC_MANIFEST,
    ]
    return {_repo_path(path): _sha256(path) for path in artifacts if path.exists()}


def run_recipe(*, dry_run: bool = False) -> dict[str, Any]:
    commands = [
        [
            sys.executable,
            "external/femic-tfl6-instance/scripts/build_p10r_mp11_tipsy_handoff.py",
        ],
        [
            sys.executable,
            "-m",
            "femic",
            "tipsy",
            "run-btc",
            "planning/tfl6_mp11_tipsy_handoff.csv",
            "--output-csv",
            "runtime/mp11_yield/p10r_mp11_candidate_04_output.csv",
            "--error-csv",
            "runtime/mp11_yield/p10r_mp11_candidate_04_error.csv",
            "--scratch-dir",
            "runtime/mp11_yield/scratch",
            "--log-dir",
            "runtime/mp11_yield/logs",
            "--run-id",
            "p10r_mp11_candidate",
            "--instance-root",
            "external/femic-tfl6-instance",
        ],
        [
            sys.executable,
            "external/femic-tfl6-instance/scripts/build_p10r_mp11_managed_curve_rebuild_blocker.py",
        ],
        [
            sys.executable,
            "external/femic-tfl6-instance/scripts/build_p10r_mp11_managed_curve_comparison.py",
        ],
        [
            sys.executable,
            "external/femic-tfl6-instance/scripts/build_p10r_mp11_managed_curve_plots.py",
        ],
        [
            sys.executable,
            "external/femic-tfl6-instance/scripts/build_p10r_mp11_tipsy_vdyp_diagnostics.py",
        ],
    ]
    results = []
    results.append(_run(commands[0], dry_run=dry_run))
    results.append(_run(commands[1], dry_run=dry_run))
    results.append(_run(commands[2], dry_run=dry_run))
    results.append(_run(commands[3], dry_run=dry_run))
    managed_clean_result = _clean_plots(MANAGED_PLOT_DIR, dry_run=dry_run)
    results.append(
        {
            "command": "clean stale mp11_managed_curve_comparison PNGs",
            **managed_clean_result,
        }
    )
    results.append(_run(commands[4], dry_run=dry_run))
    tipsy_vdyp_clean_result = _clean_plots(TIPSY_VDYP_PLOT_DIR, dry_run=dry_run)
    results.append(
        {
            "command": "clean stale mp11_tipsy_vdyp_diagnostics PNGs",
            **tipsy_vdyp_clean_result,
        }
    )
    results.append(_run(commands[5], dry_run=dry_run))

    validation = {} if dry_run else _validate()
    lock = {
        "recipe_id": "p10r_mp11_managed_curve_generation",
        "recipe_version": 1,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "site_index_policy": (
            "Use the matched canonical top-N AU VRI median SI as the TIPSY input "
            "for every planted species SI column; retain parsed MP11 SI only as provenance."
        ),
        "au_policy": (
            "Generate only candidate rows that map to canonical top-N L/M/H AUs by "
            "BEC zone/subzone and species overlap. Rows without a canonical top-N "
            "BEC match remain blocked."
        ),
        "commands": results,
        "validation": validation,
        "artifact_sha256": {} if dry_run else _artifact_hashes(),
    }
    if not dry_run:
        LOCK_JSON.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    return lock


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Print recipe without executing."
    )
    args = parser.parse_args()
    lock = run_recipe(dry_run=args.dry_run)
    print(json.dumps(lock, indent=2))


if __name__ == "__main__":
    main()
