"""Build the P10.3 MP11 AU and curve-lane crosswalk."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
STATIC_AU_PATH = INSTANCE_ROOT / "planning" / "tfl6_static_au_universe.csv"
NATURAL_CURVES_PATH = INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_curves.csv"
MP10_CROSSWALK_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_parameter_crosswalk.csv"
MP11_PARAMETER_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_yield_parameter_library.csv"

OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_au_curve_lane_crosswalk.md"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_au_curve_lane_crosswalk.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_au_curve_lane_crosswalk.json"


LANES = [
    {
        "curve_lane": "natural_unmanaged",
        "mp11_source_table": "VDYP 7.33b public natural-stand strategy",
        "mp11_curve_role": "natural_or_existing_unmanaged",
        "phase10_gate": "p10_4_natural_curve_diagnostics",
    },
    {
        "curve_lane": "early_managed",
        "mp11_source_table": "Table 54",
        "mp11_curve_role": "existing managed stands established 1961-2000",
        "phase10_gate": "p10_5_managed_parser_review",
    },
    {
        "curve_lane": "recent_managed",
        "mp11_source_table": "Table 55",
        "mp11_curve_role": "recent managed stands established 2001-2023",
        "phase10_gate": "p10_5_managed_parser_review",
    },
    {
        "curve_lane": "future_managed",
        "mp11_source_table": "Table 57",
        "mp11_curve_role": "future managed stands",
        "phase10_gate": "p10_5_managed_parser_review",
    },
]

MP10_LANE_MAP = {
    "early_managed": "existing_managed_11_50",
    "recent_managed": "existing_managed_1_10",
    "future_managed": "future_managed",
}


def _species_tokens(species_combo: str) -> set[str]:
    return {token.strip().upper() for token in str(species_combo).split("+") if token.strip()}


def _candidate_genetic_gain(species_combo: str, bec_group: str) -> str:
    species = _species_tokens(species_combo)
    gains: list[str] = []
    if "CW" in species:
        gains.append("Cw=21.0%")
    if "YC" in species or "CY" in species:
        gains.append("Yc=10.0%")
    if "FDC" in species or "FD" in species:
        gains.append("Fd low=16.0% / high=11.0%")
    if "HW" in species:
        if str(bec_group).upper().startswith(("CWHVH", "CWHVM1")):
            gains.append("Hw low-elevation restricted=1.7%")
        elif str(bec_group).upper().startswith(("CWHVM2", "MH")):
            gains.append("Hw high-elevation restricted=1.1%")
        else:
            gains.append("Hw restricted; elevation mapping required")
    if "DR" in species and str(bec_group).upper().startswith("CWHVM1"):
        gains.append("Dr CWHvm1=32.0%")
    return "; ".join(gains) if gains else "none_or_not_applicable"


def _managed_parameter_status(parameter_df: pd.DataFrame, source_table: str) -> str:
    subset = parameter_df[parameter_df["source_table"] == source_table]
    if subset.empty:
        return "missing_parameter_anchor"
    if (subset["review_status"] == "parser_review_required").any():
        return "parser_review_required"
    return "reviewed_parameter_candidate"


def build_crosswalk() -> pd.DataFrame:
    static_au = pd.read_csv(STATIC_AU_PATH)
    natural_curves = pd.read_csv(NATURAL_CURVES_PATH, usecols=["au_id"])
    natural_ids = set(natural_curves["au_id"].dropna().astype(str).unique())
    mp10 = pd.read_csv(MP10_CROSSWALK_PATH)
    parameters = pd.read_csv(MP11_PARAMETER_PATH)

    mp10_lookup: dict[tuple[str, str], dict[str, object]] = {}
    for _, row in mp10.iterrows():
        key = (str(row["au_id"]), str(row["curve_lane"]))
        mp10_lookup[key] = row.to_dict()

    rows: list[dict[str, object]] = []
    for _, au in static_au.sort_values(["selected_top_90_stratum", "area_ha"], ascending=[False, False]).iterrows():
        au_id = str(au["au_id"])
        species_combo = str(au["species_combo"])
        bec_group = str(au["bec_group"])
        selected_top = bool(au["selected_top_90_stratum"])
        natural_available = au_id in natural_ids
        for lane in LANES:
            curve_lane = lane["curve_lane"]
            if curve_lane == "natural_unmanaged":
                mp11_status = "public_vdyp_curve_available" if natural_available else "natural_curve_missing"
                mp10_status = "not_applicable"
                fallback_note = (
                    "Existing Phase 5 natural curve available for comparison."
                    if natural_available
                    else "No existing natural curve row found; P10.4 must diagnose support or fallback."
                )
                dependency_status = "public_vdyp"
                review_status = "p10_4_review_required"
                candidate_gain = "not_applicable"
            else:
                mp11_status = _managed_parameter_status(parameters, str(lane["mp11_source_table"]))
                mp10_lane = MP10_LANE_MAP[curve_lane]
                mp10_row = mp10_lookup.get((au_id, mp10_lane), {})
                mp10_status = str(mp10_row.get("match_confidence", "missing_mp10_fallback"))
                fallback_note = str(
                    mp10_row.get(
                        "fallback_or_review_note",
                        "No MP10 fallback row found for this AU/lane.",
                    )
                )
                dependency_status = (
                    "public_table_fragmented"
                    if mp11_status == "parser_review_required"
                    else "public_parameter_candidate"
                )
                review_status = "p10_5_parser_review_required"
                candidate_gain = (
                    _candidate_genetic_gain(species_combo, bec_group)
                    if curve_lane == "future_managed"
                    else "not_applicable"
                )
            rows.append(
                {
                    "au_id": au_id,
                    "stratum_code": au["stratum_code"],
                    "selected_top_90_stratum": selected_top,
                    "area_ha": round(float(au["area_ha"]), 6),
                    "stand_count": int(au["stand_count"]),
                    "bec_group": bec_group,
                    "bec_zone_code": au["bec_zone_code"],
                    "bec_subzone": au["bec_subzone"],
                    "bec_variant": au["bec_variant"],
                    "species_combo": species_combo,
                    "si_class": au["si_class"],
                    "mean_si": round(float(au["mean_si"]), 6),
                    "curve_lane": curve_lane,
                    "mp11_curve_role": lane["mp11_curve_role"],
                    "mp11_source_table": lane["mp11_source_table"],
                    "phase10_gate": lane["phase10_gate"],
                    "mp11_parameter_status": mp11_status,
                    "phase5_natural_curve_available": natural_available,
                    "mp10_fallback_confidence": mp10_status,
                    "candidate_future_genetic_gain": candidate_gain,
                    "dependency_status": dependency_status,
                    "review_status": review_status,
                    "fallback_or_review_note": fallback_note,
                    "downstream_use": "phase10_curve_lane_crosswalk_only",
                    "model_input_status": "not_model_input",
                }
            )
    return pd.DataFrame(rows)


def write_outputs(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_CSV, index=False)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "row_count": int(len(df)),
        "au_count": int(df["au_id"].nunique()),
        "curve_lane_counts": df["curve_lane"].value_counts().sort_index().to_dict(),
        "mp11_parameter_status_counts": df["mp11_parameter_status"].value_counts()
        .sort_index()
        .to_dict(),
        "review_status_counts": df["review_status"].value_counts().sort_index().to_dict(),
        "dependency_status_counts": df["dependency_status"].value_counts().sort_index().to_dict(),
        "selected_top_90_rows": int(df["selected_top_90_stratum"].sum()),
    }
    OUTPUT_JSON.write_text(
        json.dumps({**summary, "records": df.to_dict(orient="records")}, indent=2) + "\n",
        encoding="utf-8",
    )

    selected = df[df["selected_top_90_stratum"]]
    selected_summary = (
        selected.groupby(["curve_lane", "mp11_parameter_status"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values(["curve_lane", "mp11_parameter_status"])
    )
    lines = [
        "# TFL 6 MP11 AU And Curve-Lane Crosswalk",
        "",
        "## Purpose",
        "",
        "This P10.3 artifact maps the stable FEMIC canonical AU universe to MP11",
        "curve lanes and parameter gates. It preserves AU identity while making",
        "natural, early managed, recent managed, future managed, fallback, and",
        "parser-review status explicit.",
        "",
        "It does not generate curves or promote rows to model-input status.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_au_curve_lane_crosswalk.md`",
        "- `planning/tfl6_mp11_au_curve_lane_crosswalk.csv`",
        "- `planning/tfl6_mp11_au_curve_lane_crosswalk.json`",
        "",
        "## Status",
        "",
        f"- Crosswalk rows: `{summary['row_count']}`",
        f"- Canonical AU count: `{summary['au_count']}`",
        f"- Selected-top-90 row count: `{summary['selected_top_90_rows']}`",
        "- Model-input status: `not_model_input`",
        "",
        "## Curve Lane Counts",
        "",
    ]
    for key, value in summary["curve_lane_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## MP11 Parameter Status Counts", ""])
    for key, value in summary["mp11_parameter_status_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Selected Top-90 Lane Summary", ""])
    lines.append(
        "| curve_lane | mp11_parameter_status | rows |\n"
        "| --- | --- | ---: |"
    )
    for _, row in selected_summary.iterrows():
        lines.append(
            f"| `{row['curve_lane']}` | `{row['mp11_parameter_status']}` | {int(row['rows'])} |"
        )
    lines.extend(
        [
            "",
            "## Use Boundary",
            "",
            "- Natural lanes are handed to P10.4 for public VDYP curve diagnostics.",
            "- Managed lanes for Tables 54, 55, and 57 remain",
            "  `parser_review_required` until a reviewed per-AU row parser exists.",
            "- MP10 fallback confidence is retained as comparison/fallback evidence,",
            "  not as an MP11 replacement parameter.",
            "- Treatment, operability, THLB status, and scenario membership are not",
            "  canonical AU key dimensions.",
            "- All rows remain `not_model_input` until Phase 11 promotion review.",
            "",
            "## High-Area Selected Rows",
            "",
            "| au_id | curve_lane | area_ha | species_combo | si_class | mp11_parameter_status | mp10_fallback_confidence |",
            "| --- | --- | ---: | --- | --- | --- | --- |",
        ]
    )
    for _, row in selected.sort_values("area_ha", ascending=False).head(20).iterrows():
        lines.append(
            f"| `{row['au_id']}` | `{row['curve_lane']}` | {row['area_ha']:.3f} | "
            f"`{row['species_combo']}` | `{row['si_class']}` | "
            f"`{row['mp11_parameter_status']}` | `{row['mp10_fallback_confidence']}` |"
        )
    lines.append("")
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_outputs(build_crosswalk())


if __name__ == "__main__":
    main()
