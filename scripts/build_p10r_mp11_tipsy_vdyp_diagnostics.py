"""Build P10R AU-wise MP11 TIPSY-vs-VDYP diagnostic plots."""

from __future__ import annotations

import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
MP11_TIPSY_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.csv"
MP11_COMPARISON_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.csv"
)
VDYP_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_curves.csv"
VDYP_FIT_PATH = INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_fit_diagnostics.csv"
VDYP_NATURAL_DIAGNOSTICS_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_natural_curve_diagnostics.csv"
)

PLOTS_DIR = INSTANCE_ROOT / "plots" / "mp11_tipsy_vdyp_diagnostics"
VDYP_SLICE_CSV_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_vdyp_natural_curve_slice.csv"
)
VDYP_SLICE_JSON_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_vdyp_natural_curve_slice.json"
)
MANIFEST_CSV_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_vdyp_diagnostic_manifest.csv"
)
MANIFEST_JSON_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_vdyp_diagnostic_manifest.json"
)
MANIFEST_MD_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_vdyp_diagnostic_manifest.md"
)

REVIEW_STATUS = "p10r5_tipsy_vdyp_diagnostic_review_required"
BLOCKED_REVIEW_STATUS = "blocked_bec_mismatch_no_valid_comparison"
BLOCKED_DIAGNOSTIC_CLASS = "no_same_bec_vdyp_comparison_available"
VDYP_REVIEW_STATUS = "p10r5_vdyp_curve_slice_for_diagnostic"
MODEL_INPUT_STATUS = "not_model_input"


def _clean_identifier(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "unknown"


def _expected_bec_prefix(row: pd.Series) -> str:
    zone = str(row["mp11_bec_zone"]).strip().lower()
    subzone = str(row["mp11_bec_subzone"]).strip().lower()
    return f"{zone}{subzone}"


def _assert_same_bec(row: pd.Series) -> None:
    vdyp_au_id = str(row["canonical_au_id"]).strip().lower()
    expected_prefix = _expected_bec_prefix(row)
    if not vdyp_au_id.startswith(expected_prefix):
        raise RuntimeError(
            "Refusing TIPSY-vs-VDYP plot with mismatched BEC: "
            f"mp11_au_code={row['mp11_au_code']} "
            f"tipsy_bec={row['mp11_bec_zone']}{row['mp11_bec_subzone']} "
            f"vdyp_au_id={row['canonical_au_id']}"
        )


def _value_at_age(curve: pd.DataFrame, age: int, column: str) -> float:
    row = curve[curve["age"] == age]
    if row.empty:
        return float("nan")
    return round(float(row[column].iloc[0]), 3)


def _curve_comparison_metrics(
    tipsy_curve: pd.DataFrame,
    vdyp_curve: pd.DataFrame,
) -> dict[str, float | int | str]:
    tipsy_max = float(tipsy_curve["treated_volume"].max())
    vdyp_max = float(vdyp_curve["volume"].max())
    tipsy_age_at_max = int(
        tipsy_curve.loc[tipsy_curve["treated_volume"].idxmax(), "age"]
    )
    vdyp_age_at_max = int(vdyp_curve.loc[vdyp_curve["volume"].idxmax(), "age"])
    common = tipsy_curve[["age", "treated_volume"]].merge(
        vdyp_curve[["age", "volume"]], on="age", how="inner"
    )
    common = common[(common["age"] >= 10) & (common["age"] <= 290)].copy()
    if common.empty:
        rmse = float("nan")
        mean_delta = float("nan")
    else:
        deltas = common["treated_volume"] - common["volume"]
        rmse = float(math.sqrt(float((deltas**2).mean())))
        mean_delta = float(deltas.mean())
    age100_tipsy = _value_at_age(tipsy_curve, 100, "treated_volume")
    age100_vdyp = _value_at_age(vdyp_curve, 100, "volume")
    max_ratio = tipsy_max / vdyp_max if vdyp_max > 0 else float("nan")
    age100_ratio = age100_tipsy / age100_vdyp if age100_vdyp > 0 else float("nan")
    if max_ratio > 1.35 or age100_ratio > 1.35:
        diagnostic_class = "tipsy_substantially_above_vdyp"
    elif max_ratio < 0.65 or age100_ratio < 0.65:
        diagnostic_class = "tipsy_substantially_below_vdyp"
    elif abs(max_ratio - 1.0) <= 0.15 and abs(age100_ratio - 1.0) <= 0.15:
        diagnostic_class = "tipsy_vdyp_close"
    else:
        diagnostic_class = "tipsy_vdyp_moderate_difference"
    return {
        "tipsy_max_volume": round(tipsy_max, 3),
        "vdyp_max_volume": round(vdyp_max, 3),
        "tipsy_to_vdyp_max_ratio": round(max_ratio, 3),
        "tipsy_age_at_max_volume": tipsy_age_at_max,
        "vdyp_age_at_max_volume": vdyp_age_at_max,
        "tipsy_volume_age_100": age100_tipsy,
        "vdyp_volume_age_100": age100_vdyp,
        "tipsy_to_vdyp_age_100_ratio": round(age100_ratio, 3),
        "common_age_rmse": round(rmse, 3),
        "common_age_mean_delta": round(mean_delta, 3),
        "diagnostic_class": diagnostic_class,
    }


def _plot_one(
    *,
    row: pd.Series,
    tipsy_curve: pd.DataFrame,
    vdyp_curve: pd.DataFrame,
    metrics: dict[str, float | int | str],
    output_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5), constrained_layout=True)
    ax.plot(
        vdyp_curve["age"],
        vdyp_curve["volume"],
        color="#3f3f46",
        linewidth=2.1,
        linestyle="--",
        label=f"VDYP natural: {row['canonical_au_id']}",
    )
    ax.plot(
        tipsy_curve["age"],
        tipsy_curve["treated_volume"],
        color="#0f766e",
        linewidth=2.2,
        marker="o",
        markersize=2.6,
        label=f"MP11 TIPSY managed: {row['mp11_au_code']}",
    )
    ymax = max(
        float(tipsy_curve["treated_volume"].max()),
        float(vdyp_curve["volume"].max()),
    )
    ax.set_xlim(0, 350)
    ax.set_ylim(0, max(100.0, math.ceil(ymax / 100.0) * 100.0))
    ax.set_title(
        "MP11 TIPSY vs public VDYP natural diagnostic: "
        f"{row['mp11_au_code']} -> {row['canonical_au_id']}\n"
        f"{metrics['diagnostic_class']} | "
        f"TIPSY/VDYP max {metrics['tipsy_to_vdyp_max_ratio']:.3f} | "
        f"age 100 {metrics['tipsy_to_vdyp_age_100_ratio']:.3f}",
        fontsize=11,
    )
    ax.set_xlabel("Age")
    ax.set_ylabel("Merch volume")
    ax.grid(True, color="#d7d7d7", linewidth=0.7, alpha=0.8)
    ax.legend(loc="best", fontsize=8)
    ax.text(
        0.01,
        0.02,
        (
            f"common-age RMSE {metrics['common_age_rmse']:.1f}; "
            f"mean delta {metrics['common_age_mean_delta']:+.1f}; "
            f"TIPSY review {row['review_status']}"
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
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def _build_vdyp_slice(
    *,
    comparison: pd.DataFrame,
    vdyp_curves: pd.DataFrame,
    vdyp_fit: pd.DataFrame,
    natural_diag: pd.DataFrame,
) -> pd.DataFrame:
    fit_by_au = vdyp_fit.set_index("au_id").to_dict(orient="index")
    diag_by_au = natural_diag.set_index("au_id").to_dict(orient="index")
    rows: list[dict[str, object]] = []
    for _, comp_row in comparison.sort_values(["mp11_au_code"]).iterrows():
        if pd.isna(comp_row.get("canonical_au_id")):
            continue
        _assert_same_bec(comp_row)
        vdyp_au_id = comp_row["canonical_au_id"]
        vdyp_curve = vdyp_curves[vdyp_curves["au_id"] == vdyp_au_id].sort_values("age")
        if vdyp_curve.empty:
            raise RuntimeError(f"Missing VDYP natural curve for {vdyp_au_id}")
        fit = fit_by_au.get(vdyp_au_id, {})
        diag = diag_by_au.get(vdyp_au_id, {})
        for _, curve_row in vdyp_curve.iterrows():
            rows.append(
                {
                    "mp11_au_code": comp_row["mp11_au_code"],
                    "mp11_feature_id": int(comp_row["mp11_feature_id"]),
                    "vdyp_au_id": vdyp_au_id,
                    "age": int(curve_row["age"]),
                    "vdyp_volume": round(float(curve_row["volume"]), 6),
                    "source_curve_table": VDYP_CURVES_PATH.relative_to(
                        INSTANCE_ROOT
                    ).as_posix(),
                    "source_vdyp_method": fit.get("selected_path", ""),
                    "source_vdyp_accepted": bool(fit.get("accepted", False)),
                    "source_stand_count": int(fit.get("source_stand_count", 0) or 0),
                    "natural_curve_status": diag.get("natural_curve_status", ""),
                    "review_status": VDYP_REVIEW_STATUS,
                    "model_input_status": MODEL_INPUT_STATUS,
                }
            )
    return (
        pd.DataFrame(rows).sort_values(["mp11_au_code", "age"]).reset_index(drop=True)
    )


def _build_manifest(
    *,
    comparison: pd.DataFrame,
    tipsy_curves: pd.DataFrame,
    vdyp_curves: pd.DataFrame,
    natural_diag: pd.DataFrame,
) -> pd.DataFrame:
    manifest_rows: list[dict[str, object]] = []
    tipsy_by_feature = {
        int(feature_id): group.sort_values("age")
        for feature_id, group in tipsy_curves.groupby("feature_id")
    }
    natural_by_au = {
        str(au_id): group.sort_values("age")
        for au_id, group in vdyp_curves.groupby("au_id")
    }
    diag_by_au = natural_diag.set_index("au_id").to_dict(orient="index")
    for _, row in comparison.sort_values(["mp11_au_code"]).iterrows():
        feature_id = int(row["mp11_feature_id"])
        tipsy_curve = tipsy_by_feature.get(feature_id)
        if tipsy_curve is None or tipsy_curve.empty:
            raise RuntimeError(f"Missing TIPSY curve for feature_id {feature_id}")
        if pd.isna(row.get("canonical_au_id")):
            manifest_rows.append(
                {
                    "mp11_au_code": row["mp11_au_code"],
                    "mp11_feature_id": feature_id,
                    "mp11_tipsy_review_status": row["review_status"],
                    "mp11_tipsy_comparison_class": row["comparison_class"],
                    "vdyp_au_id": "",
                    "vdyp_natural_curve_status": "not_available_same_bec",
                    "vdyp_selected_path": "",
                    "vdyp_source_stand_count": 0,
                    "tipsy_max_volume": round(
                        float(tipsy_curve["treated_volume"].max()), 3
                    ),
                    "vdyp_max_volume": float("nan"),
                    "tipsy_to_vdyp_max_ratio": float("nan"),
                    "tipsy_age_at_max_volume": int(
                        tipsy_curve.loc[tipsy_curve["treated_volume"].idxmax(), "age"]
                    ),
                    "vdyp_age_at_max_volume": -1,
                    "tipsy_volume_age_100": _value_at_age(
                        tipsy_curve, 100, "treated_volume"
                    ),
                    "vdyp_volume_age_100": float("nan"),
                    "tipsy_to_vdyp_age_100_ratio": float("nan"),
                    "common_age_rmse": float("nan"),
                    "common_age_mean_delta": float("nan"),
                    "diagnostic_class": BLOCKED_DIAGNOSTIC_CLASS,
                    "review_status": BLOCKED_REVIEW_STATUS,
                    "model_input_status": MODEL_INPUT_STATUS,
                    "plot_path": "",
                    "plot_exists": False,
                    "plot_size_bytes": 0,
                }
            )
            continue
        _assert_same_bec(row)
        vdyp_au_id = str(row["canonical_au_id"])
        vdyp_curve = natural_by_au.get(vdyp_au_id)
        if vdyp_curve is None or vdyp_curve.empty:
            raise RuntimeError(f"Missing VDYP natural curve for {vdyp_au_id}")
        metrics = _curve_comparison_metrics(tipsy_curve, vdyp_curve)
        filename = (
            f"mp11-{_clean_identifier(row['mp11_au_code'])}"
            f"_tipsy-vs-vdyp-{_clean_identifier(vdyp_au_id)}.png"
        )
        plot_path = PLOTS_DIR / filename
        _plot_one(
            row=row,
            tipsy_curve=tipsy_curve,
            vdyp_curve=vdyp_curve,
            metrics=metrics,
            output_path=plot_path,
        )
        natural_info = diag_by_au.get(vdyp_au_id, {})
        manifest_rows.append(
            {
                "mp11_au_code": row["mp11_au_code"],
                "mp11_feature_id": feature_id,
                "mp11_tipsy_review_status": row["review_status"],
                "mp11_tipsy_comparison_class": row["comparison_class"],
                "vdyp_au_id": vdyp_au_id,
                "vdyp_natural_curve_status": natural_info.get(
                    "natural_curve_status", ""
                ),
                "vdyp_selected_path": natural_info.get("selected_path", ""),
                "vdyp_source_stand_count": int(
                    natural_info.get("source_stand_count", 0) or 0
                ),
                **metrics,
                "review_status": REVIEW_STATUS,
                "model_input_status": MODEL_INPUT_STATUS,
                "plot_path": plot_path.relative_to(INSTANCE_ROOT).as_posix(),
                "plot_exists": plot_path.exists(),
                "plot_size_bytes": plot_path.stat().st_size,
            }
        )
    return (
        pd.DataFrame(manifest_rows).sort_values(["mp11_au_code"]).reset_index(drop=True)
    )


def _write_json_outputs(vdyp_slice: pd.DataFrame, manifest: pd.DataFrame) -> None:
    generated_at = datetime.now(UTC).isoformat(timespec="seconds")
    if vdyp_slice.empty:
        vdyp_index = pd.DataFrame()
    else:
        vdyp_index = (
            vdyp_slice.groupby(["vdyp_au_id"], as_index=False)
            .agg(
                mp11_candidate_count=("mp11_au_code", "nunique"),
                mp11_au_codes=(
                    "mp11_au_code",
                    lambda values: ";".join(sorted(set(values))),
                ),
                curve_point_count=("age", "count"),
                age_min=("age", "min"),
                age_max=("age", "max"),
                max_vdyp_volume=("vdyp_volume", "max"),
                source_vdyp_method=("source_vdyp_method", "first"),
                source_vdyp_accepted=("source_vdyp_accepted", "first"),
                source_stand_count=("source_stand_count", "first"),
                natural_curve_status=("natural_curve_status", "first"),
            )
            .sort_values(["vdyp_au_id"])
        )
    VDYP_SLICE_JSON_PATH.write_text(
        json.dumps(
            {
                "generated_at_utc": generated_at,
                "records_policy": (
                    "The full age-by-curve review slice is tracked in the CSV. "
                    "This JSON intentionally stores only the compact AU index."
                ),
                "source_vdyp_curve_table": VDYP_CURVES_PATH.relative_to(
                    INSTANCE_ROOT
                ).as_posix(),
                "source_comparison_table": MP11_COMPARISON_PATH.relative_to(
                    INSTANCE_ROOT
                ).as_posix(),
                "row_count": int(len(vdyp_slice)),
                "mp11_candidate_count": (
                    int(vdyp_slice["mp11_au_code"].nunique())
                    if not vdyp_slice.empty
                    else 0
                ),
                "vdyp_au_count": (
                    int(vdyp_slice["vdyp_au_id"].nunique())
                    if not vdyp_slice.empty
                    else 0
                ),
                "review_status_counts": vdyp_slice["review_status"]
                .value_counts()
                .sort_index()
                .to_dict(),
                "model_input_status_counts": vdyp_slice["model_input_status"]
                .value_counts()
                .sort_index()
                .to_dict(),
                "vdyp_au_index": vdyp_index.to_dict(orient="records"),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    MANIFEST_JSON_PATH.write_text(
        json.dumps(
            {
                "generated_at_utc": generated_at,
                "source_tipsy_curve_table": MP11_TIPSY_CURVES_PATH.relative_to(
                    INSTANCE_ROOT
                ).as_posix(),
                "source_vdyp_curve_table": VDYP_CURVES_PATH.relative_to(
                    INSTANCE_ROOT
                ).as_posix(),
                "plot_directory": PLOTS_DIR.relative_to(INSTANCE_ROOT).as_posix(),
                "row_count": int(len(manifest)),
                "diagnostic_class_counts": manifest["diagnostic_class"]
                .value_counts()
                .sort_index()
                .to_dict(),
                "review_status_counts": manifest["review_status"]
                .value_counts()
                .sort_index()
                .to_dict(),
                "model_input_status_counts": manifest["model_input_status"]
                .value_counts()
                .sort_index()
                .to_dict(),
                "records": manifest.to_dict(orient="records"),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_markdown(manifest: pd.DataFrame, vdyp_slice: pd.DataFrame) -> None:
    class_counts = (
        manifest.groupby("diagnostic_class")
        .size()
        .rename("row_count")
        .reset_index()
        .sort_values("diagnostic_class")
    )
    review_rows = manifest[
        [
            "mp11_au_code",
            "vdyp_au_id",
            "diagnostic_class",
            "tipsy_to_vdyp_max_ratio",
            "tipsy_to_vdyp_age_100_ratio",
            "common_age_rmse",
            "plot_path",
        ]
    ].copy()
    lines = [
        "# TFL 6 P10R MP11 TIPSY-vs-VDYP Diagnostic Manifest",
        "",
        "## Purpose",
        "",
        "This artifact builds AU-wise diagnostic overlays between the tentatively",
        "passed MP11 Table 57 TIPSY managed curves and the matching public VDYP",
        "natural curves from the existing FEMIC `smoothed_bin_pchip` first-growth",
        "curve table.",
        "",
        "The VDYP curves are a P10R review slice from the accepted public VDYP",
        "curve surface, not a model-input promotion. Every row remains",
        f"`{MODEL_INPUT_STATUS}`.",
        "",
        "## Summary",
        "",
        f"- diagnostic rows: `{len(manifest)}`",
        f"- plotted diagnostic rows: `{int(manifest['plot_exists'].sum())}`",
        f"- blocked no-same-BEC rows: `{int((manifest['review_status'] == BLOCKED_REVIEW_STATUS).sum())}`",
        f"- VDYP curve-slice rows: `{len(vdyp_slice)}`",
        f"- unique MP11 TIPSY candidates: `{manifest['mp11_au_code'].nunique()}`",
        f"- unique VDYP natural AUs: `{manifest['vdyp_au_id'].nunique()}`",
        f"- plot directory: `{PLOTS_DIR.relative_to(INSTANCE_ROOT).as_posix()}`",
        f"- review status: `{REVIEW_STATUS}`",
        f"- model-input status: `{MODEL_INPUT_STATUS}`",
        "",
        class_counts.to_markdown(index=False),
        "",
        "## Review Index",
        "",
        review_rows.to_markdown(index=False),
        "",
        "## Use Boundary",
        "",
        "- TIPSY-vs-VDYP differences are diagnostic evidence for review, not",
        "  automatic rejection or acceptance.",
        "- The MP11 TIPSY curves remain only tentatively passed for sequencing.",
        "- Phase 11 must explicitly promote curve surfaces before model-input or",
        "  ForestModel XML work consumes them.",
        "",
    ]
    MANIFEST_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    comparison = pd.read_csv(MP11_COMPARISON_PATH)
    tipsy_curves = pd.read_csv(MP11_TIPSY_CURVES_PATH)
    vdyp_curves = pd.read_csv(VDYP_CURVES_PATH)
    vdyp_fit = pd.read_csv(VDYP_FIT_PATH)
    natural_diag = pd.read_csv(VDYP_NATURAL_DIAGNOSTICS_PATH)
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    for path in PLOTS_DIR.glob("*.png"):
        path.unlink()
    vdyp_slice = _build_vdyp_slice(
        comparison=comparison,
        vdyp_curves=vdyp_curves,
        vdyp_fit=vdyp_fit,
        natural_diag=natural_diag,
    )
    manifest = _build_manifest(
        comparison=comparison,
        tipsy_curves=tipsy_curves,
        vdyp_curves=vdyp_curves,
        natural_diag=natural_diag,
    )
    if len(manifest) != len(comparison):
        raise RuntimeError(
            f"Expected {len(comparison)} manifest rows, got {len(manifest)}"
        )
    plotted = manifest[manifest["review_status"] != BLOCKED_REVIEW_STATUS]
    if not plotted["plot_exists"].all():
        raise RuntimeError("At least one expected diagnostic plot was not written")
    if (plotted["plot_size_bytes"] <= 0).any():
        raise RuntimeError("At least one diagnostic plot is empty")
    if not (manifest["model_input_status"] == MODEL_INPUT_STATUS).all():
        raise RuntimeError("Unexpected model-input promotion in diagnostic manifest")

    vdyp_slice.to_csv(VDYP_SLICE_CSV_PATH, index=False)
    manifest.to_csv(MANIFEST_CSV_PATH, index=False)
    _write_json_outputs(vdyp_slice, manifest)
    _write_markdown(manifest, vdyp_slice)
    print(
        "Generated P10R TIPSY-vs-VDYP diagnostics: "
        f"plots={int(manifest['plot_exists'].sum())} "
        f"blocked={int((manifest['review_status'] == BLOCKED_REVIEW_STATUS).sum())} "
        f"vdyp_slice_rows={len(vdyp_slice)}"
    )


if __name__ == "__main__":
    main()
