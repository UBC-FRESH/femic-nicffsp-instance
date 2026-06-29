"""Build the P10.4 MP11 natural-curve diagnostic surface."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_au_curve_lane_crosswalk.csv"
CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_curves.csv"
FIT_DIAGNOSTICS_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_fit_diagnostics.csv"
)
REMAP_PATH = INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_remap_audit.csv"
PLOT_MANIFEST_PATH = INSTANCE_ROOT / "planning" / "tfl6_first_growth_plot_manifest.csv"

OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_natural_curve_diagnostics.md"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_natural_curve_diagnostics.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_natural_curve_diagnostics.json"


def build_diagnostics() -> pd.DataFrame:
    crosswalk = pd.read_csv(CROSSWALK_PATH)
    natural = crosswalk[crosswalk["curve_lane"] == "natural_unmanaged"].copy()
    curves = pd.read_csv(CURVES_PATH)
    fit = pd.read_csv(FIT_DIAGNOSTICS_PATH)
    remap = pd.read_csv(REMAP_PATH)
    plots = pd.read_csv(PLOT_MANIFEST_PATH)

    curve_stats = (
        curves.groupby("au_id")
        .agg(
            curve_point_count=("age", "count"),
            curve_age_min=("age", "min"),
            curve_age_max=("age", "max"),
            max_volume=("volume", "max"),
            age_at_max_volume=(
                "age",
                lambda s: int(s.iloc[curves.loc[s.index, "volume"].argmax()]),
            ),
        )
        .reset_index()
    )
    plot_counts = (
        plots.groupby("au_id")
        .agg(
            plot_count=("path", "count"),
            plot_paths=("path", lambda values: ";".join(sorted(map(str, values)))),
        )
        .reset_index()
    )
    diag = natural.merge(curve_stats, on="au_id", how="left")
    diag = diag.merge(
        fit[
            [
                "au_id",
                "source_stand_count",
                "source_row_count",
                "observed_bin_count",
                "sparse_warning",
                "selected_path",
                "rmse",
                "mape",
                "tail_rmse",
                "accepted",
            ]
        ],
        on="au_id",
        how="left",
    )
    diag = diag.merge(
        remap[
            [
                "source_au_id",
                "canonical_curve_au_id",
                "lexmatch_alias_used",
                "canonical_selected_area_ha",
            ]
        ].rename(columns={"source_au_id": "au_id"}),
        on="au_id",
        how="left",
    )
    diag = diag.merge(plot_counts, on="au_id", how="left")

    def status(row: pd.Series) -> str:
        if bool(row["selected_top_90_stratum"]) and bool(row.get("accepted", False)):
            return "selected_curve_family_available"
        if (
            pd.notna(row.get("canonical_curve_au_id"))
            and row["canonical_curve_au_id"] != row["au_id"]
        ):
            return "remapped_to_selected_curve_family"
        if pd.notna(row.get("curve_point_count")):
            return "raw_curve_available_not_selected"
        return "natural_curve_missing_review_required"

    diag["natural_curve_status"] = diag.apply(status, axis=1)
    diag["plot_count"] = diag["plot_count"].fillna(0).astype(int)
    diag["curve_point_count"] = diag["curve_point_count"].fillna(0).astype(int)
    diag["model_input_status"] = "not_model_input"
    diag["downstream_use"] = "phase10_natural_curve_diagnostics_only"
    diag["review_status"] = diag["natural_curve_status"].map(
        {
            "selected_curve_family_available": "reviewed_phase5_curve_candidate",
            "remapped_to_selected_curve_family": "reviewed_remap_candidate",
            "raw_curve_available_not_selected": "reviewed_raw_curve_not_selected",
            "natural_curve_missing_review_required": "review_required",
        }
    )
    return diag.sort_values(
        ["selected_top_90_stratum", "area_ha"], ascending=[False, False]
    )


def write_outputs(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_CSV, index=False)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "row_count": int(len(df)),
        "au_count": int(df["au_id"].nunique()),
        "status_counts": df["natural_curve_status"]
        .value_counts()
        .sort_index()
        .to_dict(),
        "review_status_counts": df["review_status"]
        .value_counts()
        .sort_index()
        .to_dict(),
        "selected_top_90_rows": int(df["selected_top_90_stratum"].sum()),
        "total_area_ha": float(df["area_ha"].sum()),
        "selected_top_90_area_ha": float(
            df.loc[df["selected_top_90_stratum"], "area_ha"].sum()
        ),
        "plot_count": int(df["plot_count"].sum()),
        "model_input_status_counts": df["model_input_status"]
        .value_counts()
        .sort_index()
        .to_dict(),
    }
    OUTPUT_JSON.write_text(
        json.dumps({**summary, "records": df.to_dict(orient="records")}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# TFL 6 MP11 Natural-Curve Diagnostics",
        "",
        "## Purpose",
        "",
        "This P10.4 artifact repackages the accepted Phase 3/5 public VDYP",
        "first-growth evidence as an MP11 natural-curve diagnostic surface.",
        "It does not rerun VDYP, change curve values, generate managed curves,",
        "or promote any row to model-input status.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_natural_curve_diagnostics.md`",
        "- `planning/tfl6_mp11_natural_curve_diagnostics.csv`",
        "- `planning/tfl6_mp11_natural_curve_diagnostics.json`",
        "",
        "## Status",
        "",
        f"- Diagnostic rows: `{summary['row_count']}`",
        f"- Canonical AU count: `{summary['au_count']}`",
        f"- Selected top-90 rows: `{summary['selected_top_90_rows']}`",
        f"- Existing plot references: `{summary['plot_count']}`",
        "- Model-input status: `not_model_input`",
        "",
        "## Natural Curve Status Counts",
        "",
    ]
    for key, value in summary["status_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "- The `77` selected top-area AU curve families remain the Phase 5 public",
            "  natural-curve baseline for MP11 comparison.",
            "- Non-AU source stratum bins remain remapped through the existing lexicographic",
            "  remap audit rather than becoming new hidden curve families.",
            "- Missing/raw-not-selected statuses are diagnostics for review, not model",
            "  input failures by themselves.",
            "- Phase 11 must explicitly promote any natural-curve surface before model",
            "  input or XML rebuild work consumes it.",
            "",
            "## High-Area Diagnostic Rows",
            "",
            "| au_id | area_ha | species_combo | si_class | natural_curve_status | canonical_curve_au_id | max_volume | plot_count |",
            "| --- | ---: | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for _, row in df.head(25).iterrows():
        max_volume = (
            "" if pd.isna(row["max_volume"]) else f"{float(row['max_volume']):.3f}"
        )
        lines.append(
            f"| `{row['au_id']}` | {float(row['area_ha']):.3f} | "
            f"`{row['species_combo']}` | `{row['si_class']}` | "
            f"`{row['natural_curve_status']}` | `{row['canonical_curve_au_id']}` | "
            f"{max_volume} | {int(row['plot_count'])} |"
        )
    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_outputs(build_diagnostics())


if __name__ == "__main__":
    main()
