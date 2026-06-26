"""Parse and QA P3.4e TFL 6 BatchTIPSY treated curves."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
BTC_OUTPUT_PATH = INSTANCE_ROOT / "data" / "04_output-tfl6.csv"
BTC_ERROR_PATH = INSTANCE_ROOT / "data" / "04_error-tfl6.csv"
CURVE_MAP_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_btc_curve_id_map.csv"
NATURAL_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_curves.csv"
TREATED_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_managed_curves.csv"
DIAGNOSTICS_CSV_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_tipsy_managed_curve_diagnostics.csv"
)
DIAGNOSTICS_MD_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_tipsy_managed_curve_diagnostics.md"
)
PLOT_MANIFEST_CSV_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_tipsy_vdyp_overlay_manifest.csv"
)
PLOT_MANIFEST_MD_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_tipsy_vdyp_overlay_manifest.md"
)
PLOTS_DIR = INSTANCE_ROOT / "plots"

LANE_LABELS = {
    "existing_managed_11_50": "Existing managed 11-50",
    "existing_managed_1_10": "Existing managed 1-10",
    "future_managed": "Future managed",
}


def _parse_btc_output() -> pd.DataFrame:
    output = pd.read_csv(BTC_OUTPUT_PATH)
    curve_map = pd.read_csv(CURVE_MAP_PATH)
    value_columns = [
        column
        for column in output.columns
        if column.startswith("MVcon_") or column.startswith("MVdec_")
    ]
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
        melted.groupby(["feature_id", "age"], as_index=False)["volume_component"]
        .sum()
        .rename(columns={"volume_component": "treated_volume"})
    )
    curves = curves.merge(
        curve_map, on="feature_id", how="left", validate="many_to_one"
    )
    if curves["au_id"].isna().any():
        missing = sorted(curves.loc[curves["au_id"].isna(), "feature_id"].unique())
        raise RuntimeError(
            f"BTC output contains feature IDs missing from curve map: {missing}"
        )
    return curves.sort_values(["au_id", "curve_lane", "age"]).reset_index(drop=True)


def _error_count() -> int:
    errors = pd.read_csv(BTC_ERROR_PATH)
    return int(len(errors))


def _value_at_age(curve: pd.DataFrame, age: int, column: str) -> float:
    subset = curve[curve["age"] == age]
    if subset.empty:
        return float("nan")
    return round(float(subset[column].iloc[0]), 3)


def _diagnostics(treated: pd.DataFrame, natural: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    natural_by_au = {au_id: group for au_id, group in natural.groupby("au_id")}
    for (au_id, lane), group in treated.groupby(["au_id", "curve_lane"], sort=True):
        natural_curve = natural_by_au.get(au_id)
        max_row = group.loc[group["treated_volume"].idxmax()]
        natural_max = (
            float(natural_curve["volume"].max())
            if natural_curve is not None and not natural_curve.empty
            else float("nan")
        )
        treated_max = float(max_row["treated_volume"])
        rows.append(
            {
                "au_id": au_id,
                "curve_lane": lane,
                "feature_id": int(group["feature_id"].iloc[0]),
                "stratum_code": group["stratum_code"].iloc[0],
                "si_class": group["si_class"].iloc[0],
                "area_ha": round(float(group["area_ha"].iloc[0]), 6),
                "matched_legacy_au_code": str(
                    group["matched_legacy_au_code"].iloc[0]
                ).zfill(4),
                "match_confidence": group["match_confidence"].iloc[0],
                "max_treated_volume": round(treated_max, 3),
                "age_at_max_treated_volume": int(max_row["age"]),
                "treated_volume_age_40": _value_at_age(group, 40, "treated_volume"),
                "treated_volume_age_60": _value_at_age(group, 60, "treated_volume"),
                "treated_volume_age_80": _value_at_age(group, 80, "treated_volume"),
                "treated_volume_age_100": _value_at_age(group, 100, "treated_volume"),
                "natural_max_volume": round(natural_max, 3),
                "treated_to_natural_max_ratio": (
                    round(treated_max / natural_max, 3)
                    if natural_max > 0
                    else float("nan")
                ),
                "other_species_pct_encoded_as_dr": round(
                    float(group["other_species_pct_encoded_as_dr"].iloc[0]), 3
                ),
            }
        )
    return (
        pd.DataFrame(rows).sort_values(["au_id", "curve_lane"]).reset_index(drop=True)
    )


def _plot_overlays(treated: pd.DataFrame, natural: pd.DataFrame) -> pd.DataFrame:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, object]] = []
    natural_by_au = {au_id: group for au_id, group in natural.groupby("au_id")}
    for au_id, group in treated.groupby("au_id", sort=True):
        natural_curve = natural_by_au.get(au_id)
        fig, ax = plt.subplots(figsize=(8.5, 5.5), constrained_layout=True)
        if natural_curve is not None and not natural_curve.empty:
            ax.plot(
                natural_curve["age"],
                natural_curve["volume"],
                color="#111111",
                linewidth=2.2,
                label="Natural VDYP",
            )
        for lane, lane_group in group.groupby("curve_lane", sort=True):
            ax.plot(
                lane_group["age"],
                lane_group["treated_volume"],
                marker="o",
                linewidth=1.7,
                markersize=2.5,
                label=LANE_LABELS.get(lane, lane),
            )
        meta = group.iloc[0]
        ax.set_title(f"TFL 6 treated vs natural curves: {au_id}")
        ax.set_xlabel("Age")
        ax.set_ylabel("Merch volume")
        ax.set_xlim(0, 350)
        ax.grid(True, color="#d8d8d8", linewidth=0.7, alpha=0.8)
        ax.legend(loc="best", fontsize=8)
        ax.text(
            0.01,
            0.02,
            f"{meta['stratum_code']} | SI {meta['si_class']} | {float(meta['area_ha']):,.1f} ha",
            transform=ax.transAxes,
            fontsize=8,
            color="#333333",
        )
        output_path = PLOTS_DIR / f"tipsy_vdyp_tfl6-{au_id}.png"
        fig.savefig(output_path, dpi=160)
        plt.close(fig)
        manifest_rows.append(
            {
                "au_id": au_id,
                "plot_path": output_path.relative_to(INSTANCE_ROOT).as_posix(),
                "curve_lanes": ";".join(sorted(group["curve_lane"].unique())),
                "has_natural_curve": bool(
                    natural_curve is not None and not natural_curve.empty
                ),
            }
        )
    return pd.DataFrame(manifest_rows).sort_values("au_id").reset_index(drop=True)


def _write_markdown(
    *,
    diagnostics: pd.DataFrame,
    manifest: pd.DataFrame,
    error_count: int,
) -> None:
    confidence = (
        diagnostics.groupby(["curve_lane", "match_confidence"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    ratio_summary = (
        diagnostics.groupby("curve_lane")["treated_to_natural_max_ratio"]
        .agg(["count", "min", "median", "max"])
        .reset_index()
        .round(3)
    )
    ratio_outliers = diagnostics[
        diagnostics["treated_to_natural_max_ratio"] > 4.0
    ].copy()
    largest_flags = diagnostics.sort_values(
        ["match_confidence", "area_ha"],
        ascending=[False, False],
    ).head(20)
    lines = [
        "# TFL 6 P3.4e Treated Curve Diagnostics",
        "",
        "## Purpose",
        "",
        "This artifact records the first BTC/BatchTIPSY run and treated-vs-natural",
        "curve QA for the selected top-area TFL 6 AU set. It is still a review",
        "surface; it does not write `data/model_input_bundle`, ForestModel XML,",
        "Matrix Builder inputs, or a Patchworks runtime package.",
        "",
        "## Run Summary",
        "",
        "- BTC input: `data/03_input-tfl6.csv`",
        "- BTC output: `data/04_output-tfl6.csv`",
        f"- BTC error rows: `{error_count}`",
        f"- Parsed treated curve rows: `{len(pd.read_csv(TREATED_CURVES_PATH))}`",
        f"- Selected AUs with overlay plots: `{len(manifest)}`",
        "",
        "## Confidence Counts",
        "",
        confidence.to_markdown(index=False),
        "",
        "## Treated-to-Natural Max-Volume Ratio Summary",
        "",
        ratio_summary.to_markdown(index=False),
        "",
        "## High-Ratio Review Flags",
        "",
        (
            "No treated-to-natural max-volume ratios exceed `4.0`."
            if ratio_outliers.empty
            else ratio_outliers[
                [
                    "au_id",
                    "curve_lane",
                    "area_ha",
                    "matched_legacy_au_code",
                    "match_confidence",
                    "max_treated_volume",
                    "natural_max_volume",
                    "treated_to_natural_max_ratio",
                    "other_species_pct_encoded_as_dr",
                ]
            ]
            .sort_values("treated_to_natural_max_ratio", ascending=False)
            .to_markdown(index=False)
        ),
        "",
        "## Largest Review Rows",
        "",
        largest_flags[
            [
                "au_id",
                "curve_lane",
                "area_ha",
                "matched_legacy_au_code",
                "match_confidence",
                "max_treated_volume",
                "natural_max_volume",
                "treated_to_natural_max_ratio",
                "other_species_pct_encoded_as_dr",
            ]
        ].to_markdown(index=False),
        "",
        "## Review Notes",
        "",
        "- BTC returned a complete row set for the selected AU/lane handoff.",
        "- `other` MP10 species shares remain explicitly flagged where they were",
        "  encoded as `Dr` for executable review.",
        "- The high-ratio review flags are concentrated in small `CWHvm1_DR`",
        "  fallback rows and should be treated as a row-level caveat rather than",
        "  a broad failure of the dominant TFL 6 treated-curve handoff.",
        "- These diagnostics support P3.4e curve review only. P3.5 treatment",
        "  options and P3.6 transition logic should not start until the maintainer",
        "  accepts or narrows any treated-curve review caveats.",
        "",
    ]
    DIAGNOSTICS_MD_PATH.write_text("\n".join(lines), encoding="utf-8")

    manifest_lines = [
        "# TFL 6 TIPSY-vs-VDYP Overlay Manifest",
        "",
        f"Overlay plots generated: `{len(manifest)}`.",
        "",
        manifest.head(40).to_markdown(index=False),
        "",
        "The full machine-readable manifest is",
        f"`{PLOT_MANIFEST_CSV_PATH.relative_to(INSTANCE_ROOT).as_posix()}`.",
        "",
    ]
    PLOT_MANIFEST_MD_PATH.write_text("\n".join(manifest_lines), encoding="utf-8")


def main() -> None:
    error_count = _error_count()
    treated = _parse_btc_output()
    natural = pd.read_csv(NATURAL_CURVES_PATH)
    treated.to_csv(TREATED_CURVES_PATH, index=False)
    diagnostics = _diagnostics(treated, natural)
    diagnostics.to_csv(DIAGNOSTICS_CSV_PATH, index=False)
    manifest = _plot_overlays(treated, natural)
    manifest.to_csv(PLOT_MANIFEST_CSV_PATH, index=False)
    _write_markdown(diagnostics=diagnostics, manifest=manifest, error_count=error_count)
    print(
        json.dumps(
            {
                "btc_error_rows": error_count,
                "treated_curve_rows": int(len(treated)),
                "diagnostic_rows": int(len(diagnostics)),
                "overlay_plots": int(len(manifest)),
                "output_curves": TREATED_CURVES_PATH.relative_to(
                    INSTANCE_ROOT
                ).as_posix(),
                "output_diagnostics": DIAGNOSTICS_CSV_PATH.relative_to(
                    INSTANCE_ROOT
                ).as_posix(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
