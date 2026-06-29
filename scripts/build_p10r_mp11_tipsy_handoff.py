"""Build P10R MP11 BatchTIPSY handoff candidates and blocker diagnostics."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
PARSED_ROWS_PATH = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_row_parse.csv"
BTC_SCHEMA_FALLBACK_PATH = INSTANCE_ROOT / "data" / "03_input-tfl6.csv"
CANONICAL_AU_PATH = INSTANCE_ROOT / "planning" / "tfl6_static_au_universe.csv"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff.csv"
OUTPUT_MAP_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff_map.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff.json"
OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff.md"


try:
    from femic.pipeline.tipsy import DEFAULT_BTC_MSYT_COLUMNS
except ModuleNotFoundError:
    DEFAULT_BTC_MSYT_COLUMNS = list(
        pd.read_csv(BTC_SCHEMA_FALLBACK_PATH, nrows=0).columns
    )

LANE_CODES = {
    "early_managed": 1,
    "recent_managed": 2,
    "future_managed": 3,
}

BTC_SPECIES = {
    "ba": "Ba",
    "cw": "Cw",
    "yc": "Yc",
    "cy": "Yc",
    "fd": "Fd",
    "fdc": "Fd",
    "hw": "Hw",
    "ss": "Ss",
    "dr": "Dr",
    "pl": "Pl",
    "plc": "Pl",
}

SITE_INDEX_COLUMNS = {
    "Ba": "ba_si",
    "Cw": "cw_si",
    "Yc": "yc_si",
    "Fd": "fd_si",
    "Hw": "hw_si",
    "Ss": "ss_si",
    "Dr": "dr_si",
    "Pl": "pl_si",
}


def _float_or_zero(value: Any) -> float:
    try:
        if pd.isna(value):
            return 0.0
        text = str(value).strip()
        if not text or text == "-":
            return 0.0
        return float(text)
    except (TypeError, ValueError):
        return 0.0


def _density_split(total_density: float, species: list[tuple[str, float]]) -> list[int]:
    exact = [(code, total_density * pct / 100.0) for code, pct in species]
    floored = [int(value) for _, value in exact]
    remainder = int(round(total_density)) - sum(floored)
    order = sorted(
        range(len(exact)),
        key=lambda index: (-(exact[index][1] - int(exact[index][1])), exact[index][0]),
    )
    for index in order[: max(0, remainder)]:
        floored[index] += 1
    return floored


def _species_components(row: pd.Series) -> list[dict[str, Any]]:
    try:
        value = json.loads(row["species_components_json"])
    except (TypeError, json.JSONDecodeError):
        return []
    return value if isinstance(value, list) else []


def _species_for_btc(row: pd.Series) -> list[tuple[str, float, float, float]]:
    components = _species_components(row)
    species: list[tuple[str, float, float, float]] = []
    for index, component in enumerate(components[:5], start=1):
        species_code = str(component.get("species", "")).lower()
        btc_species = BTC_SPECIES.get(species_code)
        if not btc_species:
            continue
        percent = _float_or_zero(component.get("percent"))
        si = _float_or_zero(row.get(f"spp{index}_si"))
        genetic_gain = _float_or_zero(row.get(f"genetic_gain_spp{index}"))
        species.append((btc_species, percent, si, genetic_gain))
    return species


def _canonical_species_set(species_combo: Any) -> set[str]:
    return {
        str(part).strip().upper()
        for part in str(species_combo).replace("/", "+").split("+")
        if str(part).strip()
    }


def _weighted_si(species: list[tuple[str, float, float, float]]) -> float:
    weighted = 0.0
    weight_sum = 0.0
    for _btc_species, percent, si, _genetic_gain in species:
        if percent > 0 and si > 0:
            weighted += percent * si
            weight_sum += percent
    return weighted / weight_sum if weight_sum else 0.0


def _bec_from_mp11_future_au(au_code: str) -> tuple[str, str, str]:
    if re.match(r"^Fvh\d+", au_code):
        return "CWH", "vh", "decoded_from_fvh_future_au_code"
    if re.match(r"^Fvm[12]\d+", au_code):
        return "CWH", "vm", "decoded_from_fvm_future_au_code"
    if re.match(r"^FMH\d+", au_code):
        return "MH", "mm", "decoded_from_fmh_future_au_code_review_required"
    return "", "", "missing_bec_decoder"


def _canonical_au_match(
    *,
    row: pd.Series,
    bec_zone: str,
    bec_subzone: str,
    canonical_au: pd.DataFrame,
) -> tuple[pd.Series | None, str]:
    species = _species_for_btc(row)
    species_set = {item[0].upper() for item in species}
    weighted_si = _weighted_si(species)
    candidates = canonical_au[
        (canonical_au["bec_zone_code"].astype(str).str.upper() == bec_zone)
        & (canonical_au["bec_subzone"].astype(str).str.lower() == bec_subzone.lower())
    ].copy()
    if candidates.empty:
        return None, "no_canonical_top_n_au_for_bec"
    candidates["species_overlap_count"] = candidates["species_combo"].map(
        lambda combo: len(species_set.intersection(_canonical_species_set(combo)))
    )
    candidates["species_overlap_ratio"] = candidates["species_overlap_count"].map(
        lambda count: count / len(species_set) if species_set else 0.0
    )
    candidates["median_si_abs_diff"] = candidates["median_si"].map(
        lambda value: (
            abs(float(value) - weighted_si) if weighted_si > 0 else float("inf")
        )
    )
    match = candidates.sort_values(
        [
            "species_overlap_count",
            "species_overlap_ratio",
            "median_si_abs_diff",
            "area_ha",
            "au_id",
        ],
        ascending=[False, False, True, False, True],
    ).iloc[0]
    if int(match["species_overlap_count"]) <= 0:
        return None, "no_canonical_top_n_au_species_overlap"
    return match, "canonical_top_n_au_match"


def _handoff_status(
    row: pd.Series, canonical_au: pd.DataFrame
) -> tuple[str, str, str, str, pd.Series | None, float]:
    species = _species_for_btc(row)
    weighted_si = _weighted_si(species)
    if row["parse_confidence"] != "high":
        return (
            "review_required_parser_warning",
            "",
            "",
            str(row.get("parser_warnings", "")),
            None,
            weighted_si,
        )
    if row["source_table"] != "Table 57":
        return (
            "blocked_missing_public_au_to_bec_mapping",
            "",
            "",
            "Tables 54/55 use MP11 existing AU codes that do not carry enough public BEC/site-series information for direct BatchTIPSY handoff.",
            None,
            weighted_si,
        )
    bec_zone, bec_subzone, source = _bec_from_mp11_future_au(str(row["au_code"]))
    if not bec_zone:
        return ("blocked_missing_bec_decoder", "", "", source, None, weighted_si)
    canonical_match, canonical_note = _canonical_au_match(
        row=row,
        bec_zone=bec_zone,
        bec_subzone=bec_subzone,
        canonical_au=canonical_au,
    )
    if canonical_match is None:
        return (
            f"blocked_{canonical_note}",
            bec_zone,
            bec_subzone,
            f"{source}; {canonical_note}",
            None,
            weighted_si,
        )
    return (
        "candidate_for_curve_generation",
        bec_zone,
        bec_subzone,
        f"{source}; {canonical_note}",
        canonical_match,
        weighted_si,
    )


def _btc_row(row: pd.Series, map_row: dict[str, Any]) -> dict[str, Any]:
    btc_row = {column: "" for column in DEFAULT_BTC_MSYT_COLUMNS}
    species = _species_for_btc(row)
    tipsy_input_si = _float_or_zero(map_row["tipsy_input_si"])
    if tipsy_input_si <= 0:
        raise RuntimeError(
            f"Missing canonical AU median SI for BTC feature {map_row['feature_id']}"
        )
    density_values = _density_split(
        _float_or_zero(row["sph"]), [(s[0], s[1]) for s in species]
    )
    feature_id = map_row["feature_id"]
    btc_row.update(
        {
            "feature_id": feature_id,
            "bec_zone": map_row["bec_zone"],
            "bec_subzone": map_row["bec_subzone"],
            "planting_delay": 1,
            "planted_percent": 100,
            "oaf1": 0.85,
            "oaf2": 0.95,
            "opening_id": feature_id,
            "vri_ref_age": 0,
            "vri_ref_sph": 0,
        }
    )
    for column in [
        column for column in DEFAULT_BTC_MSYT_COLUMNS if column.endswith("_si")
    ]:
        btc_row[column] = 0
    for index, (
        (btc_species, _percent, _parsed_si, genetic_gain),
        density,
    ) in enumerate(
        zip(species, density_values, strict=True),
        start=1,
    ):
        btc_row[f"planted_species{index}"] = btc_species
        btc_row[f"planted_density{index}"] = density
        btc_row[f"genetic_worth{index}"] = genetic_gain
        btc_row[SITE_INDEX_COLUMNS[btc_species]] = tipsy_input_si
    return btc_row


def build_handoff() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parsed = pd.read_csv(PARSED_ROWS_PATH)
    canonical_au = pd.read_csv(CANONICAL_AU_PATH)
    if (~canonical_au["selected_top_90_stratum"].astype(bool)).any():
        raise RuntimeError(
            "Canonical AU table contains non-top-N rows; refusing MP11 TIPSY handoff."
        )
    mapping_rows: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    for index, row in parsed.reset_index(drop=True).iterrows():
        status, bec_zone, bec_subzone, note, canonical_match, weighted_si = (
            _handoff_status(row, canonical_au)
        )
        feature_id = 610000 + (index + 1) * 10 + LANE_CODES[str(row["curve_lane"])]
        species = _species_for_btc(row)
        species_count = len(species)
        map_row = {
            "feature_id": feature_id,
            "row_id": row["row_id"],
            "source_table": row["source_table"],
            "curve_lane": row["curve_lane"],
            "mp11_au_code": row["au_code"],
            "bec_zone": bec_zone,
            "bec_subzone": bec_subzone,
            "canonical_au_id": ""
            if canonical_match is None
            else str(canonical_match["au_id"]),
            "canonical_stratum_code": ""
            if canonical_match is None
            else str(canonical_match["stratum_code"]),
            "canonical_species_combo": ""
            if canonical_match is None
            else str(canonical_match["species_combo"]),
            "canonical_mean_si": ""
            if canonical_match is None
            else round(float(canonical_match["mean_si"]), 3),
            "canonical_median_si": ""
            if canonical_match is None
            else round(float(canonical_match["median_si"]), 3),
            "mp11_parsed_weighted_si": round(weighted_si, 3) if weighted_si > 0 else "",
            "tipsy_input_si": ""
            if canonical_match is None
            else round(float(canonical_match["median_si"]), 3),
            "tipsy_input_si_source": ""
            if canonical_match is None
            else "canonical_top_n_au_vri_median_si",
            "mp11_weighted_si": round(weighted_si, 3) if weighted_si > 0 else "",
            "canonical_mean_si_abs_diff": ""
            if canonical_match is None or weighted_si <= 0
            else round(abs(float(canonical_match["mean_si"]) - weighted_si), 3),
            "canonical_median_si_abs_diff": ""
            if canonical_match is None or weighted_si <= 0
            else round(abs(float(canonical_match["median_si"]) - weighted_si), 3),
            "sph": row["sph"],
            "species_count": species_count,
            "species_percent_total": row["species_percent_total"],
            "thlb_area_ha": row["thlb_area_ha"],
            "parse_confidence": row["parse_confidence"],
            "handoff_status": status,
            "handoff_note": note,
            "model_input_status": "not_model_input",
            "source_anchor": row["source_anchor"],
        }
        mapping_rows.append(map_row)
        if status == "candidate_for_curve_generation":
            handoff_rows.append(_btc_row(row, map_row))
    handoff = pd.DataFrame(handoff_rows, columns=list(DEFAULT_BTC_MSYT_COLUMNS))
    mapping = pd.DataFrame(mapping_rows)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "input_rows": str(PARSED_ROWS_PATH.relative_to(INSTANCE_ROOT)),
        "output_handoff_csv": str(OUTPUT_CSV.relative_to(INSTANCE_ROOT)),
        "output_handoff_map_csv": str(OUTPUT_MAP_CSV.relative_to(INSTANCE_ROOT)),
        "parsed_row_count": int(len(parsed)),
        "handoff_candidate_count": int(len(handoff)),
        "status_counts": {
            str(key): int(value)
            for key, value in mapping["handoff_status"]
            .value_counts()
            .sort_index()
            .items()
        },
        "source_table_status_counts": {
            str(key): int(value)
            for key, value in mapping.groupby(["source_table", "handoff_status"])
            .size()
            .items()
        },
        "oaf_policy": "MP11 narrative OAF defaults: OAF1=15% and OAF2=5%, emitted as BTC factors 0.85 and 0.95.",
        "regen_delay_policy": "Future managed candidate rows use one-year regeneration delay from MP11 Section 8.2.7.1.",
        "site_index_policy": (
            "Candidate BTC rows use the matched canonical top-N AU VRI median SI "
            "as the TIPSY site-index input for every planted species SI column. "
            "Parsed MP11 per-species SI values are retained only as provenance."
        ),
        "join_boundary": (
            "Table 57 rows can produce standalone future-managed curve-generation candidates. "
            "They must first map to a canonical top-N FEMIC AU. Tables 54/55 remain "
            "blocked pending a public MP11 existing/recent AU-code to BEC/site-series "
            "mapping before BatchTIPSY handoff."
        ),
        "use_boundary": "Rows are handoff candidates only and remain not_model_input.",
    }
    return handoff, mapping, summary


def _markdown_table(df: pd.DataFrame, columns: list[str], *, max_rows: int = 25) -> str:
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


def write_outputs(
    handoff: pd.DataFrame, mapping: pd.DataFrame, summary: dict[str, Any]
) -> None:
    handoff.to_csv(OUTPUT_CSV, index=False)
    mapping.to_csv(OUTPUT_MAP_CSV, index=False)
    OUTPUT_JSON.write_text(
        json.dumps(
            {
                "summary": summary,
                "handoff_map": mapping.to_dict(orient="records"),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    status = (
        mapping.groupby(["source_table", "handoff_status"])
        .size()
        .reset_index(name="row_count")
        .sort_values(["source_table", "handoff_status"])
    )
    lines = [
        "# TFL 6 MP11 TIPSY Handoff Candidates",
        "",
        "## Purpose",
        "",
        "This P10R.3 artifact converts P10R.2 parser rows into conservative ",
        "BatchTIPSY handoff candidates and row-level blocker diagnostics. It does ",
        "not run curve-generation tools and does not promote any row to model input.",
        "",
        "## Summary",
        "",
        f"- Parsed input rows: `{summary['parsed_row_count']}`",
        f"- Handoff candidate rows: `{summary['handoff_candidate_count']}`",
        f"- Handoff CSV: `{summary['output_handoff_csv']}`",
        f"- Handoff map CSV: `{summary['output_handoff_map_csv']}`",
        "",
        "## Status Counts",
        "",
        _markdown_table(
            status, ["source_table", "handoff_status", "row_count"], max_rows=50
        ),
        "",
        "## Candidate Policy",
        "",
        f"- OAF: {summary['oaf_policy']}",
        f"- Regeneration delay: {summary['regen_delay_policy']}",
        f"- Site index: {summary['site_index_policy']}",
        f"- Join boundary: {summary['join_boundary']}",
        "",
        "## Candidate Rows",
        "",
        _markdown_table(
            mapping[mapping["handoff_status"] == "candidate_for_curve_generation"],
            [
                "feature_id",
                "mp11_au_code",
                "curve_lane",
                "bec_zone",
                "bec_subzone",
                "canonical_au_id",
                "canonical_median_si",
                "mp11_parsed_weighted_si",
                "tipsy_input_si",
                "canonical_median_si_abs_diff",
                "sph",
                "species_percent_total",
                "thlb_area_ha",
                "handoff_status",
            ],
            max_rows=30,
        ),
        "",
        "## Blocked Or Review-Required Rows",
        "",
        _markdown_table(
            mapping[mapping["handoff_status"] != "candidate_for_curve_generation"],
            [
                "mp11_au_code",
                "source_table",
                "curve_lane",
                "parse_confidence",
                "handoff_status",
                "handoff_note",
            ],
            max_rows=30,
        ),
        "",
        "## Use Boundary",
        "",
        "- All rows remain `not_model_input`.",
        "- P10R.4 may run only the candidate rows unless a maintainer accepts a ",
        "  repair or mapping for blocked rows.",
        "- Existing and recent managed rows require a public MP11 AU-code to ",
        "  BEC/site-series mapping before curve generation.",
    ]
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    handoff, mapping, summary = build_handoff()
    write_outputs(handoff, mapping, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
