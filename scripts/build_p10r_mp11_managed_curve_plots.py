"""Build P10R MP11 managed-curve review overlays against Phase 5 curves."""

from __future__ import annotations

import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
MP11_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.csv"
PHASE5_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_managed_curves.csv"
COMPARISON_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.csv"
PLOTS_DIR = INSTANCE_ROOT / "plots" / "mp11_managed_curve_comparison"
MANIFEST_CSV_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.csv"
)
MANIFEST_JSON_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.json"
)
MANIFEST_MD_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.md"
)


PLOT_WIDTH = 8.5
PLOT_HEIGHT = 5.5
PLOT_DPI = 160


def _clean_identifier(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "unknown"


def _required_int(value: object, column: str) -> int:
    if pd.isna(value):
        raise RuntimeError(f"Missing required numeric value in {column}")
    return int(float(value))


def _required_float(value: object, column: str) -> float:
    if pd.isna(value):
        raise RuntimeError(f"Missing required numeric value in {column}")
    return float(value)


def _value_at_age(curve: pd.DataFrame, age: int, column: str) -> float:
    row = curve[curve["age"] == age]
    if row.empty:
        return float("nan")
    return round(float(row[column].iloc[0]), 3)


def _format_pct(value: object) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{float(value):+.1f}%"


def _format_delta(value: object) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{float(value):+.1f}"


def _plot_one(
    *,
    comparison_row: pd.Series,
    mp11_curve: pd.DataFrame,
    phase5_curve: pd.DataFrame,
    output_path: Path,
) -> None:
    fig, ax = plt.subplots(
        figsize=(PLOT_WIDTH, PLOT_HEIGHT),
        constrained_layout=True,
    )
    ax.plot(
        phase5_curve["age"],
        phase5_curve["treated_volume"],
        color="#4b5563",
        linewidth=2.0,
        linestyle="--",
        label=f"Phase 5 fallback: {comparison_row['phase5_au_id']}",
    )
    ax.plot(
        mp11_curve["age"],
        mp11_curve["treated_volume"],
        color="#0f766e",
        linewidth=2.2,
        marker="o",
        markersize=2.6,
        label=f"Phase 10R MP11: {comparison_row['mp11_au_code']}",
    )
    title = (
        f"MP11 Table 57 vs Phase 5 managed curve: "
        f"{comparison_row['mp11_au_code']} -> {comparison_row['phase5_au_id']}"
    )
    subtitle = (
        f"{comparison_row['comparison_class']} | "
        f"species overlap {float(comparison_row['species_overlap_ratio']):.3f} | "
        f"SI diff {float(comparison_row['mean_si_abs_diff']):.3f}"
    )
    ax.set_title(f"{title}\n{subtitle}", fontsize=11)
    ax.set_xlabel("Age")
    ax.set_ylabel("Merch volume")
    ax.set_xlim(0, 350)
    ymax = max(
        float(mp11_curve["treated_volume"].max()),
        float(phase5_curve["treated_volume"].max()),
    )
    ax.set_ylim(0, max(100.0, math.ceil(ymax / 100.0) * 100.0))
    ax.grid(True, color="#d7d7d7", linewidth=0.7, alpha=0.8)
    ax.legend(loc="best", fontsize=8)
    ax.text(
        0.01,
        0.02,
        (
            f"max delta {_format_delta(comparison_row['max_volume_delta'])} "
            f"({_format_pct(comparison_row['max_volume_pct_delta'])}); "
            f"age 100 delta "
            f"{_format_delta(comparison_row['volume_age_100_delta'])} "
            f"({_format_pct(comparison_row['volume_age_100_pct_delta'])})"
        ),
        transform=ax.transAxes,
        fontsize=8,
        color="#222222",
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": "#ffffff",
            "edgecolor": "#bbbbbb",
            "alpha": 0.9,
        },
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=PLOT_DPI)
    plt.close(fig)


def _build_manifest(
    *,
    comparison: pd.DataFrame,
    mp11_curves: pd.DataFrame,
    phase5_curves: pd.DataFrame,
) -> pd.DataFrame:
    manifest_rows: list[dict[str, object]] = []
    mp11_by_feature = {
        int(feature_id): group.sort_values("age")
        for feature_id, group in mp11_curves.groupby("feature_id")
    }
    phase5_by_feature = {
        int(feature_id): group.sort_values("age")
        for feature_id, group in phase5_curves.groupby("feature_id")
    }

    for _, row in comparison.sort_values(
        ["comparison_class", "mp11_au_code"]
    ).iterrows():
        mp11_feature_id = _required_int(row["mp11_feature_id"], "mp11_feature_id")
        phase5_feature_id = _required_int(row["phase5_feature_id"], "phase5_feature_id")
        mp11_curve = mp11_by_feature.get(mp11_feature_id)
        phase5_curve = phase5_by_feature.get(phase5_feature_id)
        if mp11_curve is None or mp11_curve.empty:
            raise RuntimeError(f"Missing MP11 curve for feature_id {mp11_feature_id}")
        if phase5_curve is None or phase5_curve.empty:
            raise RuntimeError(
                f"Missing Phase 5 curve for feature_id {phase5_feature_id}"
            )

        filename = (
            f"mp11-{_clean_identifier(row['mp11_au_code'])}"
            f"_vs_phase5-{_clean_identifier(row['phase5_au_id'])}.png"
        )
        output_path = PLOTS_DIR / filename
        _plot_one(
            comparison_row=row,
            mp11_curve=mp11_curve,
            phase5_curve=phase5_curve,
            output_path=output_path,
        )
        manifest_rows.append(
            {
                "mp11_au_code": row["mp11_au_code"],
                "mp11_feature_id": mp11_feature_id,
                "mp11_curve_lane": row["mp11_curve_lane"],
                "mp11_thlb_area_ha": _required_float(
                    row["mp11_thlb_area_ha"], "mp11_thlb_area_ha"
                ),
                "phase5_au_id": row["phase5_au_id"],
                "phase5_feature_id": phase5_feature_id,
                "phase5_stratum_code": row["phase5_stratum_code"],
                "phase5_match_confidence": row["phase5_match_confidence"],
                "species_overlap_ratio": _required_float(
                    row["species_overlap_ratio"], "species_overlap_ratio"
                ),
                "mean_si_abs_diff": _required_float(
                    row["mean_si_abs_diff"], "mean_si_abs_diff"
                ),
                "max_volume_pct_delta": _required_float(
                    row["max_volume_pct_delta"], "max_volume_pct_delta"
                ),
                "volume_age_100_pct_delta": _required_float(
                    row["volume_age_100_pct_delta"], "volume_age_100_pct_delta"
                ),
                "mp11_volume_age_100": _value_at_age(mp11_curve, 100, "treated_volume"),
                "phase5_volume_age_100": _value_at_age(
                    phase5_curve, 100, "treated_volume"
                ),
                "comparison_class": row["comparison_class"],
                "review_status": "p10r5_managed_plot_review_required",
                "model_input_status": row["model_input_status"],
                "plot_path": output_path.relative_to(INSTANCE_ROOT).as_posix(),
                "plot_exists": output_path.exists(),
                "plot_size_bytes": output_path.stat().st_size,
            }
        )

    return pd.DataFrame(manifest_rows).sort_values(["comparison_class", "mp11_au_code"])


def _write_markdown(manifest: pd.DataFrame) -> None:
    class_counts = (
        manifest.groupby("comparison_class")
        .size()
        .rename("plot_count")
        .reset_index()
        .sort_values("comparison_class")
    )
    review_rows = manifest[
        [
            "mp11_au_code",
            "phase5_au_id",
            "comparison_class",
            "max_volume_pct_delta",
            "volume_age_100_pct_delta",
            "plot_path",
        ]
    ].copy()
    review_rows["max_volume_pct_delta"] = review_rows["max_volume_pct_delta"].round(3)
    review_rows["volume_age_100_pct_delta"] = review_rows[
        "volume_age_100_pct_delta"
    ].round(3)
    lines = [
        "# TFL 6 P10R MP11 Managed Curve Plot Manifest",
        "",
        "## Purpose",
        "",
        "This artifact indexes regenerated Phase 10R MP11 Table 57 managed-curve",
        "review plots against the matched Phase 5 fallback managed curves. The PNG",
        "plot library is written under ignored `plots/` space; this manifest is the",
        "tracked review surface.",
        "",
        "These plots are comparison evidence only. They do not promote any recovered",
        "or regenerated value into model input contracts.",
        "",
        "## Summary",
        "",
        f"- generated plots: `{len(manifest)}`",
        f"- plot directory: `{PLOTS_DIR.relative_to(INSTANCE_ROOT).as_posix()}`",
        f"- generated UTC: `{datetime.now(UTC).isoformat(timespec='seconds')}`",
        "",
        class_counts.to_markdown(index=False),
        "",
        "## Review Index",
        "",
        review_rows.to_markdown(index=False),
        "",
    ]
    MANIFEST_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    comparison = pd.read_csv(COMPARISON_PATH)
    mp11_curves = pd.read_csv(MP11_CURVES_PATH)
    phase5_curves = pd.read_csv(PHASE5_CURVES_PATH)
    manifest = _build_manifest(
        comparison=comparison,
        mp11_curves=mp11_curves,
        phase5_curves=phase5_curves,
    )
    if len(manifest) != len(comparison):
        raise RuntimeError(
            f"Expected {len(comparison)} plot manifest rows, got {len(manifest)}"
        )
    if not manifest["plot_exists"].all():
        raise RuntimeError("At least one expected plot was not written")
    if (manifest["plot_size_bytes"] <= 0).any():
        raise RuntimeError("At least one expected plot is empty")

    MANIFEST_CSV_PATH.write_text(manifest.to_csv(index=False), encoding="utf-8")
    payload = {
        "source_artifacts": {
            "comparison_csv": COMPARISON_PATH.relative_to(INSTANCE_ROOT).as_posix(),
            "mp11_curves_csv": MP11_CURVES_PATH.relative_to(INSTANCE_ROOT).as_posix(),
            "phase5_curves_csv": PHASE5_CURVES_PATH.relative_to(
                INSTANCE_ROOT
            ).as_posix(),
        },
        "plot_directory": PLOTS_DIR.relative_to(INSTANCE_ROOT).as_posix(),
        "generated_plot_count": int(len(manifest)),
        "model_input_statuses": sorted(manifest["model_input_status"].unique()),
        "comparison_class_counts": manifest["comparison_class"]
        .value_counts()
        .sort_index()
        .to_dict(),
        "records": manifest.to_dict(orient="records"),
    }
    MANIFEST_JSON_PATH.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_markdown(manifest)

    print(
        "Generated "
        f"{len(manifest)} MP11-vs-Phase-5 managed curve plots under "
        f"{PLOTS_DIR.relative_to(INSTANCE_ROOT).as_posix()}"
    )


if __name__ == "__main__":
    main()
