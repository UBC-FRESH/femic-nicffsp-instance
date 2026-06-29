"""Record P10R managed-curve generation status and toolchain blockers."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from femic.pipeline.tipsy import (
    DEFAULT_BATCHTIPSY_EXE_ENV,
    DEFAULT_BATCHTIPSY_WINDOWS_EXE,
    resolve_btc_executable,
)


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
PARENT_REPO_ROOT = INSTANCE_ROOT.parents[1]
HANDOFF_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff.csv"
HANDOFF_MAP_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff_map.csv"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.json"
OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.md"
CURVES_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.csv"
CURVES_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.json"
BTC_OUTPUT_CSV = (
    INSTANCE_ROOT / "runtime" / "mp11_yield" / "p10r_mp11_candidate_04_output.csv"
)
BTC_ERROR_CSV = (
    INSTANCE_ROOT / "runtime" / "mp11_yield" / "p10r_mp11_candidate_04_error.csv"
)
BTC_MANIFEST_PATH = (
    INSTANCE_ROOT
    / "runtime"
    / "mp11_yield"
    / "logs"
    / "btc_manifest-p10r_mp11_candidate.json"
)


def _portable_path(path: str | Path) -> str:
    resolved = Path(path)
    try:
        return str(resolved.relative_to(INSTANCE_ROOT))
    except ValueError:
        try:
            return str(resolved.relative_to(PARENT_REPO_ROOT))
        except ValueError:
            return str(resolved)


def _existing_executables() -> list[str]:
    try:
        discovery = resolve_btc_executable()
    except FileNotFoundError:
        return []
    return [f"{_portable_path(discovery.executable_path)} ({discovery.source})"]


def _load_btc_manifest() -> dict[str, object] | None:
    if not BTC_MANIFEST_PATH.exists():
        return None
    return json.loads(BTC_MANIFEST_PATH.read_text(encoding="utf-8"))


def _btc_error_count() -> int | None:
    if not BTC_ERROR_CSV.exists():
        return None
    return int(len(pd.read_csv(BTC_ERROR_CSV)))


def _value_at_age(curve: pd.DataFrame, age: int, column: str) -> float:
    subset = curve[curve["age"] == age]
    if subset.empty:
        return float("nan")
    return round(float(subset[column].iloc[0]), 3)


def _parse_btc_output(candidate_map: pd.DataFrame) -> pd.DataFrame | None:
    if not BTC_OUTPUT_CSV.exists():
        return None
    output = pd.read_csv(BTC_OUTPUT_CSV)
    value_columns = [
        column
        for column in output.columns
        if column.startswith("MVcon_") or column.startswith("MVdec_")
    ]
    if "feature_id" not in output.columns or not value_columns:
        raise RuntimeError(
            f"BTC output is missing expected feature_id / MVcon_* / MVdec_* columns: "
            f"{BTC_OUTPUT_CSV}"
        )
    expected_features = set(candidate_map["feature_id"].astype(int))
    output_features = set(output["feature_id"].astype(int))
    missing = sorted(expected_features - output_features)
    extra = sorted(output_features - expected_features)
    if missing or extra:
        raise RuntimeError(
            "BTC output feature IDs do not match P10R.3 candidates: "
            f"missing={missing} extra={extra}"
        )

    melted = output.melt(
        id_vars=["feature_id"],
        value_vars=value_columns,
        var_name="metric_age",
        value_name="volume_component",
    )
    metric_age = melted["metric_age"].str.extract(
        r"^(?P<metric>MVcon|MVdec)_(?P<age>\d+)$"
    )
    melted["metric"] = metric_age["metric"]
    melted["age"] = metric_age["age"].astype(int)
    curves = (
        melted.pivot_table(
            index=["feature_id", "age"],
            columns="metric",
            values="volume_component",
            aggfunc="sum",
            fill_value=0.0,
        )
        .reset_index()
        .rename(
            columns={
                "MVcon": "merch_conifer_volume",
                "MVdec": "merch_deciduous_volume",
            }
        )
    )
    for column in ["merch_conifer_volume", "merch_deciduous_volume"]:
        if column not in curves.columns:
            curves[column] = 0.0
    curves["treated_volume"] = (
        curves["merch_conifer_volume"] + curves["merch_deciduous_volume"]
    )
    metadata_columns = [
        "feature_id",
        "row_id",
        "source_table",
        "curve_lane",
        "mp11_au_code",
        "bec_zone",
        "bec_subzone",
        "canonical_au_id",
        "canonical_stratum_code",
        "canonical_species_combo",
        "canonical_mean_si",
        "canonical_median_si",
        "mp11_parsed_weighted_si",
        "tipsy_input_si",
        "tipsy_input_si_source",
        "mp11_weighted_si",
        "canonical_mean_si_abs_diff",
        "canonical_median_si_abs_diff",
        "sph",
        "species_count",
        "species_percent_total",
        "thlb_area_ha",
        "parse_confidence",
        "source_anchor",
    ]
    curves = curves.merge(
        candidate_map[metadata_columns],
        on="feature_id",
        how="left",
        validate="many_to_one",
    )
    curves["model_input_status"] = "not_model_input"
    ordered_columns = [
        "feature_id",
        "mp11_au_code",
        "row_id",
        "source_table",
        "curve_lane",
        "age",
        "treated_volume",
        "merch_conifer_volume",
        "merch_deciduous_volume",
        "bec_zone",
        "bec_subzone",
        "canonical_au_id",
        "canonical_stratum_code",
        "canonical_species_combo",
        "canonical_mean_si",
        "canonical_median_si",
        "mp11_parsed_weighted_si",
        "tipsy_input_si",
        "tipsy_input_si_source",
        "mp11_weighted_si",
        "canonical_mean_si_abs_diff",
        "canonical_median_si_abs_diff",
        "sph",
        "species_count",
        "species_percent_total",
        "thlb_area_ha",
        "parse_confidence",
        "source_anchor",
        "model_input_status",
    ]
    return (
        curves[ordered_columns]
        .sort_values(["feature_id", "age"])
        .reset_index(drop=True)
    )


def build_blocker() -> tuple[pd.DataFrame, dict[str, object]]:
    handoff = pd.read_csv(HANDOFF_CSV)
    handoff_map = pd.read_csv(HANDOFF_MAP_CSV)
    found = _existing_executables()
    candidate_map = handoff_map[
        handoff_map["handoff_status"] == "candidate_for_curve_generation"
    ].copy()
    curves = _parse_btc_output(candidate_map)
    manifest = _load_btc_manifest()
    error_count = _btc_error_count()
    rows = []
    if curves is not None:
        status = "generated_curve_output_inspected"
        note = (
            "FEMIC BTC generated real MP11 candidate outputs from the P10R.3 "
            "handoff. The parsed curves are retained as review surfaces only; "
            "they are not model inputs and have not yet been compared against "
            "Phase 5 fallback curves."
        )
    elif found:
        status = "ready_for_manual_tool_execution_review"
        note = (
            "FEMIC resolved a BatchTIPSY/TIPSY executable. This script does not "
            "invoke it automatically; P10R.4 curve generation must use the "
            "existing FEMIC BTC runner so command construction, scratch/log "
            "layout, report-template handling, and provenance stay on the "
            "supported parent-package contract."
        )
    else:
        status = "blocked_missing_batchtipsy_executable"
        note = (
            "No accepted BatchTIPSY/TIPSY executable was found in configured "
            "public-safe local paths or PATH. Managed curve generation cannot "
            "be claimed until the executable/toolchain is supplied and command "
            "provenance is captured."
        )
    curves_by_feature = (
        {int(feature_id): group for feature_id, group in curves.groupby("feature_id")}
        if curves is not None
        else {}
    )
    for _, row in candidate_map.iterrows():
        feature_id = int(row["feature_id"])
        curve = curves_by_feature.get(feature_id)
        output_curve_rows = 0 if curve is None else int(len(curve))
        max_treated_volume = None
        age_at_max_treated_volume = None
        terminal_treated_volume_age_350 = None
        if curve is not None and not curve.empty:
            max_row = curve.loc[curve["treated_volume"].idxmax()]
            max_treated_volume = round(float(max_row["treated_volume"]), 3)
            age_at_max_treated_volume = int(max_row["age"])
            terminal_treated_volume_age_350 = _value_at_age(
                curve, 350, "treated_volume"
            )
        rows.append(
            {
                "feature_id": feature_id,
                "mp11_au_code": row["mp11_au_code"],
                "source_table": row["source_table"],
                "curve_lane": row["curve_lane"],
                "handoff_status": row["handoff_status"],
                "curve_generation_status": status,
                "curve_generation_note": note,
                "output_curve_rows": output_curve_rows,
                "max_treated_volume": max_treated_volume,
                "age_at_max_treated_volume": age_at_max_treated_volume,
                "treated_volume_age_40": (
                    None
                    if curve is None
                    else _value_at_age(curve, 40, "treated_volume")
                ),
                "treated_volume_age_60": (
                    None
                    if curve is None
                    else _value_at_age(curve, 60, "treated_volume")
                ),
                "treated_volume_age_80": (
                    None
                    if curve is None
                    else _value_at_age(curve, 80, "treated_volume")
                ),
                "treated_volume_age_100": (
                    None
                    if curve is None
                    else _value_at_age(curve, 100, "treated_volume")
                ),
                "terminal_treated_volume_age_350": terminal_treated_volume_age_350,
                "btc_error_rows": error_count,
                "model_input_status": "not_model_input",
            }
        )
    output = pd.DataFrame(rows)
    if curves is not None:
        curves.to_csv(CURVES_CSV, index=False)
        CURVES_JSON.write_text(
            json.dumps(
                {
                    "summary": {
                        "generated_at_utc": datetime.now(UTC).isoformat(),
                        "source_btc_output_csv": _portable_path(BTC_OUTPUT_CSV),
                        "source_btc_error_csv": _portable_path(BTC_ERROR_CSV),
                        "source_btc_manifest_path": _portable_path(BTC_MANIFEST_PATH),
                        "curve_rows": int(len(curves)),
                        "feature_count": int(curves["feature_id"].nunique()),
                        "model_input_status": "not_model_input",
                    },
                    "rows": curves.to_dict(orient="records"),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "input_handoff_csv": str(HANDOFF_CSV.relative_to(INSTANCE_ROOT)),
        "input_handoff_map_csv": str(HANDOFF_MAP_CSV.relative_to(INSTANCE_ROOT)),
        "handoff_candidate_count": int(len(handoff)),
        "blocked_or_review_rows": int(len(handoff_map) - len(handoff)),
        "searched_executable_candidates": [
            f"explicit --btc-exe / {DEFAULT_BATCHTIPSY_EXE_ENV}",
            str(DEFAULT_BATCHTIPSY_WINDOWS_EXE),
        ],
        "found_executables_or_runners": found,
        "curve_generation_status": status,
        "curve_generation_note": note,
        "btc_output_csv": _portable_path(BTC_OUTPUT_CSV)
        if BTC_OUTPUT_CSV.exists()
        else None,
        "btc_error_csv": _portable_path(BTC_ERROR_CSV)
        if BTC_ERROR_CSV.exists()
        else None,
        "btc_manifest_path": (
            _portable_path(BTC_MANIFEST_PATH) if BTC_MANIFEST_PATH.exists() else None
        ),
        "btc_manifest_status": None if manifest is None else manifest.get("status"),
        "btc_manifest_exit_code": None
        if manifest is None
        else manifest.get("exit_code"),
        "btc_error_rows": error_count,
        "parsed_curve_rows": 0 if curves is None else int(len(curves)),
        "parsed_curve_feature_count": (
            0 if curves is None else int(curves["feature_id"].nunique())
        ),
        "accepted_next_action": (
            "Compare the parsed P10R.4 candidate curves against Phase 5 fallback "
            "curves where useful, then keep any promotion decision review-gated."
        ),
        "use_boundary": (
            "These artifacts are review surfaces. They are generated MP11 "
            "candidate curves, but they remain not_model_input until reviewed "
            "and explicitly accepted."
        ),
    }
    return output, summary


def _markdown_table(df: pd.DataFrame, columns: list[str], *, max_rows: int = 30) -> str:
    display = df[columns].head(max_rows)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for _, row in display.iterrows():
        values = []
        for column in columns:
            value = "" if pd.isna(row[column]) else str(row[column]).replace("|", "\\|")
            values.append(value)
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows])


def write_outputs(output: pd.DataFrame, summary: dict[str, object]) -> None:
    output.to_csv(OUTPUT_CSV, index=False)
    OUTPUT_JSON.write_text(
        json.dumps(
            {"summary": summary, "rows": output.to_dict(orient="records")}, indent=2
        )
        + "\n",
        encoding="utf-8",
    )
    lines = [
        "# TFL 6 MP11 Managed Curve Rebuild Status",
        "",
        "## Purpose",
        "",
        "This P10R.4 artifact records whether MP11 managed curve generation can ",
        "run from the P10R.3 handoff candidates. When FEMIC BTC output is ",
        "available, it also records parsed generated-curve summaries while ",
        "keeping every row review-gated as `not_model_input`.",
        "",
        "## Status",
        "",
        f"- Handoff candidate rows: `{summary['handoff_candidate_count']}`",
        f"- Blocked or review rows outside handoff: `{summary['blocked_or_review_rows']}`",
        f"- Curve-generation status: `{summary['curve_generation_status']}`",
        f"- Found executables/runners: `{len(summary['found_executables_or_runners'])}`",
        f"- BTC manifest status: `{summary['btc_manifest_status']}`",
        f"- BTC manifest exit code: `{summary['btc_manifest_exit_code']}`",
        f"- BTC error rows: `{summary['btc_error_rows']}`",
        f"- Parsed curve rows: `{summary['parsed_curve_rows']}`",
        f"- Parsed curve feature count: `{summary['parsed_curve_feature_count']}`",
        "",
        "## Toolchain Finding",
        "",
        str(summary["curve_generation_note"]),
        "",
        "## Searched Paths",
        "",
        *[f"- `{path}`" for path in summary["searched_executable_candidates"]],
        "",
        "## Runtime Evidence",
        "",
        f"- BTC output CSV: `{summary['btc_output_csv']}`",
        f"- BTC error CSV: `{summary['btc_error_csv']}`",
        f"- BTC manifest: `{summary['btc_manifest_path']}`",
        "- Parsed curve table: `planning/tfl6_mp11_managed_curves.csv`",
        "- Parsed curve JSON: `planning/tfl6_mp11_managed_curves.json`",
        "",
        "## Candidate Row Status",
        "",
        _markdown_table(
            output,
            [
                "feature_id",
                "mp11_au_code",
                "curve_lane",
                "curve_generation_status",
                "output_curve_rows",
                "max_treated_volume",
                "age_at_max_treated_volume",
            ],
            max_rows=30,
        ),
        "",
        "## Representative Curve Inspection",
        "",
        output[
            [
                "feature_id",
                "mp11_au_code",
                "max_treated_volume",
                "age_at_max_treated_volume",
                "treated_volume_age_40",
                "treated_volume_age_60",
                "treated_volume_age_80",
                "treated_volume_age_100",
                "terminal_treated_volume_age_350",
            ]
        ]
        .sort_values("max_treated_volume", ascending=False, na_position="last")
        .head(10)
        .to_markdown(index=False),
        "",
        "## Required Next Action",
        "",
        str(summary["accepted_next_action"]),
        "",
        "## Use Boundary",
        "",
        str(summary["use_boundary"]),
    ]
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    output, summary = build_blocker()
    write_outputs(output, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
