"""Compare P10R MP11 generated managed curves against Phase 5 fallback curves."""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
MP11_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.csv"
MP11_HANDOFF_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff.csv"
PHASE5_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_managed_curves.csv"
PHASE5_DIAGNOSTICS_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_diagnostics.csv"
)

OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.json"
OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.md"

BTC_SPECIES_TO_CANONICAL = {
    "BA": "BA",
    "CW": "CW",
    "YC": "YC",
    "CY": "YC",
    "FD": "FD",
    "FDC": "FD",
    "HW": "HW",
    "HM": "HM",
    "SS": "SS",
    "DR": "DR",
    "PL": "PL",
    "PLC": "PL",
}
SITE_INDEX_COLUMNS = {
    "BA": "ba_si",
    "CW": "cw_si",
    "YC": "yc_si",
    "FD": "fd_si",
    "HW": "hw_si",
    "HM": "hm_si",
    "SS": "ss_si",
    "DR": "dr_si",
    "PL": "pl_si",
}


def _clean_species(value: Any) -> str:
    text = str(value).strip().upper()
    return BTC_SPECIES_TO_CANONICAL.get(text, text)


def _float_or_nan(value: Any) -> float:
    try:
        if pd.isna(value):
            return float("nan")
        text = str(value).strip()
        if not text:
            return float("nan")
        return float(text)
    except (TypeError, ValueError):
        return float("nan")


def _candidate_species(row: pd.Series) -> tuple[list[str], float]:
    species: list[str] = []
    weighted_si = 0.0
    weight_sum = 0.0
    for index in range(1, 6):
        raw_species = row.get(f"planted_species{index}")
        if pd.isna(raw_species) or not str(raw_species).strip():
            continue
        code = _clean_species(raw_species)
        species.append(code)
        density = _float_or_nan(row.get(f"planted_density{index}"))
        si = _float_or_nan(row.get(SITE_INDEX_COLUMNS.get(code, "")))
        if not math.isnan(density) and density > 0 and not math.isnan(si) and si > 0:
            weighted_si += density * si
            weight_sum += density
    mean_si = weighted_si / weight_sum if weight_sum else float("nan")
    return species, mean_si


def _phase5_species_set(species_combo: Any) -> set[str]:
    return {
        _clean_species(part)
        for part in str(species_combo).replace("/", "+").split("+")
        if part.strip()
    }


def _value_at_age(curve: pd.DataFrame, age: int) -> float:
    subset = curve[curve["age"] == age]
    if subset.empty:
        return float("nan")
    return round(float(subset["treated_volume"].iloc[0]), 3)


def _curve_metrics(curve: pd.DataFrame) -> dict[str, float | int]:
    max_row = curve.loc[curve["treated_volume"].idxmax()]
    return {
        "max_volume": round(float(max_row["treated_volume"]), 3),
        "age_at_max_volume": int(max_row["age"]),
        "volume_age_40": _value_at_age(curve, 40),
        "volume_age_60": _value_at_age(curve, 60),
        "volume_age_80": _value_at_age(curve, 80),
        "volume_age_100": _value_at_age(curve, 100),
        "volume_age_350": _value_at_age(curve, 350),
    }


def _pct_delta(delta: float, reference: float) -> float:
    if math.isnan(delta) or math.isnan(reference) or reference == 0:
        return float("nan")
    return round(delta / reference * 100.0, 3)


def _delta(value: float, reference: float) -> float:
    if math.isnan(value) or math.isnan(reference):
        return float("nan")
    return round(value - reference, 3)


def _difference_class(max_pct_delta: float, age100_pct_delta: float) -> str:
    values = [abs(v) for v in [max_pct_delta, age100_pct_delta] if not math.isnan(v)]
    if not values:
        return "missing_comparison"
    largest = max(values)
    if largest > 25:
        return "large_difference_review_required"
    if largest > 10:
        return "moderate_difference_review_required"
    return "low_difference"


def _select_phase5_match(
    *,
    candidate: pd.Series,
    candidate_species: list[str],
    candidate_mean_si: float,
    phase5_future: pd.DataFrame,
) -> pd.Series | None:
    candidates = phase5_future[
        (phase5_future["bec_zone_code"] == candidate["bec_zone"])
        & (phase5_future["bec_subzone"] == candidate["bec_subzone"])
        & (phase5_future["phase5_comparison_curve_available"])
    ].copy()
    if candidates.empty:
        candidates = phase5_future[phase5_future["phase5_comparison_curve_available"]].copy()
    if candidates.empty:
        return None

    candidate_set = set(candidate_species)
    candidates["species_overlap_count"] = candidates["species_combo"].map(
        lambda combo: len(candidate_set.intersection(_phase5_species_set(combo)))
    )
    candidates["species_overlap_ratio"] = candidates["species_overlap_count"].map(
        lambda count: count / len(candidate_set) if candidate_set else 0.0
    )
    candidates["mean_si_abs_diff"] = candidates["mean_si"].map(
        lambda value: (
            abs(float(value) - candidate_mean_si)
            if not math.isnan(candidate_mean_si) and not pd.isna(value)
            else float("inf")
        )
    )
    return candidates.sort_values(
        [
            "species_overlap_count",
            "species_overlap_ratio",
            "mean_si_abs_diff",
            "selected_top_90_stratum",
            "area_ha",
        ],
        ascending=[False, False, True, False, False],
    ).iloc[0]


def build_comparison() -> pd.DataFrame:
    mp11_curves = pd.read_csv(MP11_CURVES_PATH)
    handoff = pd.read_csv(MP11_HANDOFF_PATH)
    phase5_curves = pd.read_csv(PHASE5_CURVES_PATH)
    phase5_diag = pd.read_csv(PHASE5_DIAGNOSTICS_PATH)
    phase5_future = phase5_diag[
        (phase5_diag["curve_lane"] == "future_managed")
        & (phase5_diag["phase5_comparison_curve_available"])
    ].copy()

    phase5_curves_by_feature = {
        int(feature_id): group.copy()
        for feature_id, group in phase5_curves.groupby("feature_id")
    }
    mp11_by_feature = {
        int(feature_id): group.copy() for feature_id, group in mp11_curves.groupby("feature_id")
    }
    handoff_by_feature = {int(row["feature_id"]): row for _, row in handoff.iterrows()}

    rows: list[dict[str, object]] = []
    for feature_id, mp11_curve in sorted(mp11_by_feature.items()):
        metadata = mp11_curve.iloc[0]
        handoff_row = handoff_by_feature[feature_id]
        species, mean_si = _candidate_species(handoff_row)
        phase5_match = _select_phase5_match(
            candidate=metadata,
            candidate_species=species,
            candidate_mean_si=mean_si,
            phase5_future=phase5_future,
        )
        mp11_metrics = _curve_metrics(mp11_curve)
        if phase5_match is None:
            phase5_metrics: dict[str, float | int] = {
                "max_volume": float("nan"),
                "age_at_max_volume": -1,
                "volume_age_40": float("nan"),
                "volume_age_60": float("nan"),
                "volume_age_80": float("nan"),
                "volume_age_100": float("nan"),
                "volume_age_350": float("nan"),
            }
            phase5_feature_id = None
            age_rmse = float("nan")
            age_mean_delta = float("nan")
            overlap_ratio = float("nan")
            si_diff = float("nan")
        else:
            phase5_feature_id = int(phase5_match["feature_id"])
            phase5_curve = phase5_curves_by_feature[phase5_feature_id]
            phase5_metrics = _curve_metrics(phase5_curve)
            paired = mp11_curve[["age", "treated_volume"]].merge(
                phase5_curve[["age", "treated_volume"]],
                on="age",
                suffixes=("_mp11", "_phase5"),
            )
            paired["delta"] = paired["treated_volume_mp11"] - paired["treated_volume_phase5"]
            age_rmse = round(float((paired["delta"].pow(2).mean()) ** 0.5), 3)
            age_mean_delta = round(float(paired["delta"].mean()), 3)
            phase_species = _phase5_species_set(phase5_match["species_combo"])
            overlap_ratio = (
                round(len(set(species).intersection(phase_species)) / len(set(species)), 3)
                if species
                else float("nan")
            )
            si_diff = (
                round(abs(float(phase5_match["mean_si"]) - mean_si), 3)
                if not math.isnan(mean_si)
                else float("nan")
            )

        max_delta = _delta(
            float(mp11_metrics["max_volume"]),
            float(phase5_metrics["max_volume"]),
        )
        max_pct_delta = _pct_delta(max_delta, float(phase5_metrics["max_volume"]))
        age100_delta = _delta(
            float(mp11_metrics["volume_age_100"]),
            float(phase5_metrics["volume_age_100"]),
        )
        age100_pct_delta = _pct_delta(age100_delta, float(phase5_metrics["volume_age_100"]))
        rows.append(
            {
                "mp11_feature_id": feature_id,
                "mp11_au_code": metadata["mp11_au_code"],
                "mp11_curve_lane": metadata["curve_lane"],
                "mp11_thlb_area_ha": metadata["thlb_area_ha"],
                "mp11_bec_zone": metadata["bec_zone"],
                "mp11_bec_subzone": metadata["bec_subzone"],
                "mp11_species_combo": "+".join(species),
                "mp11_weighted_si": round(mean_si, 3) if not math.isnan(mean_si) else None,
                "phase5_au_id": None if phase5_match is None else phase5_match["au_id"],
                "phase5_feature_id": phase5_feature_id,
                "phase5_stratum_code": (
                    None if phase5_match is None else phase5_match["stratum_code"]
                ),
                "phase5_species_combo": (
                    None if phase5_match is None else phase5_match["species_combo"]
                ),
                "phase5_mean_si": None if phase5_match is None else phase5_match["mean_si"],
                "phase5_match_confidence": (
                    None if phase5_match is None else phase5_match["phase5_mp10_match_confidence"]
                ),
                "phase5_matched_legacy_au_code": (
                    None if phase5_match is None else phase5_match["matched_legacy_au_code"]
                ),
                "species_overlap_ratio": overlap_ratio,
                "mean_si_abs_diff": si_diff,
                "mp11_max_volume": mp11_metrics["max_volume"],
                "phase5_max_volume": phase5_metrics["max_volume"],
                "max_volume_delta": max_delta,
                "max_volume_pct_delta": max_pct_delta,
                "mp11_age_at_max_volume": mp11_metrics["age_at_max_volume"],
                "phase5_age_at_max_volume": phase5_metrics["age_at_max_volume"],
                "mp11_volume_age_40": mp11_metrics["volume_age_40"],
                "phase5_volume_age_40": phase5_metrics["volume_age_40"],
                "mp11_volume_age_60": mp11_metrics["volume_age_60"],
                "phase5_volume_age_60": phase5_metrics["volume_age_60"],
                "mp11_volume_age_80": mp11_metrics["volume_age_80"],
                "phase5_volume_age_80": phase5_metrics["volume_age_80"],
                "mp11_volume_age_100": mp11_metrics["volume_age_100"],
                "phase5_volume_age_100": phase5_metrics["volume_age_100"],
                "volume_age_100_delta": age100_delta,
                "volume_age_100_pct_delta": age100_pct_delta,
                "mp11_volume_age_350": mp11_metrics["volume_age_350"],
                "phase5_volume_age_350": phase5_metrics["volume_age_350"],
                "age_curve_mean_delta": age_mean_delta,
                "age_curve_rmse": age_rmse,
                "comparison_class": _difference_class(max_pct_delta, age100_pct_delta),
                "review_status": "p10r4e_comparison_review_required",
                "model_input_status": "not_model_input",
            }
        )
    return pd.DataFrame(rows).sort_values("mp11_feature_id").reset_index(drop=True)


def write_outputs(comparison: pd.DataFrame) -> None:
    comparison.to_csv(OUTPUT_CSV, index=False)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "row_count": int(len(comparison)),
        "mp11_feature_count": int(comparison["mp11_feature_id"].nunique()),
        "phase5_match_count": int(comparison["phase5_feature_id"].notna().sum()),
        "comparison_class_counts": comparison["comparison_class"]
        .value_counts()
        .sort_index()
        .to_dict(),
        "model_input_status_counts": comparison["model_input_status"]
        .value_counts()
        .sort_index()
        .to_dict(),
        "method": (
            "Nearest Phase 5 future-managed comparison row selected by matching BEC "
            "zone/subzone first, then maximizing species overlap and minimizing "
            "weighted site-index difference."
        ),
    }
    OUTPUT_JSON.write_text(
        json.dumps({**summary, "records": comparison.to_dict(orient="records")}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    largest = comparison.sort_values(
        ["comparison_class", "max_volume_pct_delta"],
        ascending=[True, False],
    ).head(15)
    top_delta = comparison.reindex(
        comparison["max_volume_pct_delta"].abs().sort_values(ascending=False).index
    ).head(15)
    lines = [
        "# TFL 6 MP11 Managed Curve Phase 5 Comparison",
        "",
        "## Purpose",
        "",
        "This P10R.4e artifact compares the generated MP11 Table 57 future-managed",
        "candidate curves against the nearest available Phase 5 future-managed",
        "fallback curves. It is a review surface only and does not promote any",
        "curve to model input.",
        "",
        "## Status",
        "",
        f"- MP11 candidate rows compared: `{summary['row_count']}`",
        f"- Phase 5 comparison matches: `{summary['phase5_match_count']}`",
        "- Model-input status: `not_model_input`",
        "",
        "## Method",
        "",
        str(summary["method"]),
        "",
        "## Comparison Classes",
        "",
    ]
    for key, value in summary["comparison_class_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Largest Absolute Max-Volume Differences",
            "",
            top_delta[
                [
                    "mp11_au_code",
                    "mp11_species_combo",
                    "phase5_au_id",
                    "phase5_species_combo",
                    "species_overlap_ratio",
                    "mean_si_abs_diff",
                    "mp11_max_volume",
                    "phase5_max_volume",
                    "max_volume_pct_delta",
                    "comparison_class",
                ]
            ].to_markdown(index=False),
            "",
            "## Review Rows",
            "",
            largest[
                [
                    "mp11_au_code",
                    "phase5_au_id",
                    "phase5_match_confidence",
                    "max_volume_delta",
                    "max_volume_pct_delta",
                    "volume_age_100_delta",
                    "volume_age_100_pct_delta",
                    "age_curve_rmse",
                    "comparison_class",
                ]
            ].to_markdown(index=False),
            "",
            "## Use Boundary",
            "",
            "- Phase 5 curves are comparison/fallback evidence, not MP11-equivalent",
            "  curves.",
            "- Generated MP11 curves remain `not_model_input` until reviewed and",
            "  explicitly accepted.",
            "- Downstream plots, model-input tables, ForestModel XML, and Patchworks",
            "  packages must not consume these rows without a later promotion step.",
            "",
        ]
    )
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    comparison = build_comparison()
    write_outputs(comparison)
    print(
        json.dumps(
            {
                "row_count": int(len(comparison)),
                "phase5_match_count": int(comparison["phase5_feature_id"].notna().sum()),
                "comparison_class_counts": comparison["comparison_class"]
                .value_counts()
                .sort_index()
                .to_dict(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
