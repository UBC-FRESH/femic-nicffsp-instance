"""Build the P3.4e TFL 6 BatchTIPSY handoff from reviewed MP10 crosswalk rows."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
from femic.pipeline.tipsy import DEFAULT_BTC_MSYT_COLUMNS


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
CROSSWALK_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_parameter_crosswalk.csv"
PARAMETER_LIBRARY_PATH = (
    INSTANCE_ROOT / "planning" / "tfl6_mp10_tipsy_parameter_library.csv"
)
OUTPUT_CSV_PATH = INSTANCE_ROOT / "data" / "03_input-tfl6.csv"
MANIFEST_JSON_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_btc_handoff_manifest.json"
MANIFEST_MD_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_btc_handoff_manifest.md"
MAPPING_CSV_PATH = INSTANCE_ROOT / "planning" / "tfl6_tipsy_btc_curve_id_map.csv"

LANE_CODES = {
    "existing_managed_11_50": 1,
    "existing_managed_1_10": 2,
    "future_managed": 3,
}

SPECIES_COLUMNS = [
    ("ba", "Ba"),
    ("cw", "Cw"),
    ("cy", "Yc"),
    ("fd", "Fd"),
    ("hw", "Hw"),
    ("ss", "Ss"),
    ("other", "Dr"),
]

SITE_INDEX_COLUMNS = {
    "Ba": "ba_si",
    "Cw": "cw_si",
    "Yc": "yc_si",
    "Fd": "fd_si",
    "Hw": "hw_si",
    "Ss": "ss_si",
    "Dr": "dr_si",
}


def _bec_fields(bec_group: str) -> tuple[str, str]:
    match = re.match(r"^([A-Z]+)([a-z]+)", str(bec_group).strip())
    if not match:
        return str(bec_group).strip(), ""
    return match.group(1), match.group(2)


def _float_or_zero(value: object) -> float:
    try:
        if pd.isna(value):
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _oaf_factor(percent_reduction: object) -> float:
    return round(1.0 - (_float_or_zero(percent_reduction) / 100.0), 4)


def _regen_delay(value: object, *, lane: str) -> int:
    text = "" if pd.isna(value) else str(value).strip()
    if text:
        match = re.search(r"\d+", text)
        if match:
            return int(match.group(0))
    return 1 if lane == "future_managed" else 0


def _species_list(row: pd.Series) -> tuple[list[tuple[str, float]], float]:
    species: list[tuple[str, float]] = []
    other_pct = 0.0
    for source_code, btc_code in SPECIES_COLUMNS:
        pct = _float_or_zero(row.get(f"mp10_{source_code}_pct"))
        if pct <= 0:
            continue
        if source_code == "other":
            other_pct = pct
        species.append((btc_code, pct))
    species.sort(key=lambda item: (-item[1], item[0]))
    return species[:5], other_pct


def _site_index_for_species(
    *,
    btc_species: str,
    parameter_row: pd.Series,
    crosswalk_row: pd.Series,
) -> float:
    if btc_species == "Ba":
        value = parameter_row.get("ba_si")
    elif btc_species in {"Cw", "Yc"}:
        value = parameter_row.get("cw_cy_si")
    elif btc_species == "Fd":
        value = parameter_row.get("fd_si")
    elif btc_species == "Hw":
        value = parameter_row.get("hw_si")
    elif btc_species == "Ss":
        value = parameter_row.get("ss_si")
    else:
        value = crosswalk_row.get("mp10_weighted_si")
    site_index = _float_or_zero(value)
    if site_index <= 0:
        site_index = _float_or_zero(crosswalk_row.get("mp10_weighted_si"))
    if site_index <= 0:
        site_index = _float_or_zero(crosswalk_row.get("mean_si"))
    if site_index <= 0:
        site_index = _float_or_zero(crosswalk_row.get("median_si"))
    return round(site_index, 2)


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


def build_handoff() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    crosswalk = pd.read_csv(CROSSWALK_PATH)
    library = pd.read_csv(PARAMETER_LIBRARY_PATH, dtype={"legacy_au_code": str})
    library["legacy_au_code"] = library["legacy_au_code"].str.zfill(4)

    selected = crosswalk[crosswalk["selected_top_90_stratum"] == True].copy()  # noqa: E712
    selected = selected[selected["curve_lane"].isin(LANE_CODES)].copy()
    selected["matched_legacy_au_code"] = (
        selected["matched_legacy_au_code"].astype(str).str.zfill(4)
    )

    parameter_lookup = {
        (row.source_table, row.legacy_au_code): row
        for row in library.itertuples(index=False)
    }

    au_order = {
        au_id: index + 1
        for index, au_id in enumerate(
            selected[["au_id", "area_ha"]]
            .drop_duplicates()
            .sort_values(["area_ha", "au_id"], ascending=[False, True])["au_id"]
        )
    }

    rows: list[dict[str, object]] = []
    mappings: list[dict[str, object]] = []
    for _, crosswalk_row in selected.sort_values(["au_id", "curve_lane"]).iterrows():
        lookup_key = (
            crosswalk_row["source_table"],
            crosswalk_row["matched_legacy_au_code"],
        )
        parameter_tuple = parameter_lookup[lookup_key]
        parameter_row = pd.Series(parameter_tuple._asdict())
        lane = str(crosswalk_row["curve_lane"])
        feature_id = (
            600000 + au_order[str(crosswalk_row["au_id"])] * 10 + LANE_CODES[lane]
        )
        bec_zone, bec_subzone = _bec_fields(str(crosswalk_row["bec_group"]))
        species, other_pct = _species_list(crosswalk_row)
        density = _float_or_zero(crosswalk_row["initial_sph"])
        density_values = _density_split(density, species)

        btc_row = {column: "" for column in DEFAULT_BTC_MSYT_COLUMNS}
        btc_row.update(
            {
                "feature_id": feature_id,
                "bec_zone": bec_zone,
                "bec_subzone": bec_subzone,
                "planting_delay": _regen_delay(
                    crosswalk_row.get("regen_delay_years"), lane=lane
                ),
                "planted_percent": 100,
                "oaf1": _oaf_factor(crosswalk_row.get("oaf1_pct")),
                "oaf2": _oaf_factor(crosswalk_row.get("oaf2_pct")),
                "opening_id": feature_id,
                "vri_ref_age": 0,
                "vri_ref_sph": 0,
            }
        )
        for site_column in [
            column for column in DEFAULT_BTC_MSYT_COLUMNS if column.endswith("_si")
        ]:
            btc_row[site_column] = 0
        for index, ((btc_species, pct), density_value) in enumerate(
            zip(species, density_values, strict=True),
            start=1,
        ):
            btc_row[f"planted_species{index}"] = btc_species
            btc_row[f"planted_density{index}"] = density_value
            btc_row[f"genetic_worth{index}"] = _float_or_zero(
                crosswalk_row.get(f"genetic_worth_{btc_species.lower()}_pct")
            )
            btc_row[SITE_INDEX_COLUMNS[btc_species]] = _site_index_for_species(
                btc_species=btc_species,
                parameter_row=parameter_row,
                crosswalk_row=crosswalk_row,
            )

        rows.append(btc_row)
        mappings.append(
            {
                "feature_id": feature_id,
                "au_id": crosswalk_row["au_id"],
                "stratum_code": crosswalk_row["stratum_code"],
                "si_class": crosswalk_row["si_class"],
                "curve_lane": lane,
                "selected_top_90_stratum": True,
                "area_ha": round(float(crosswalk_row["area_ha"]), 6),
                "source_table": crosswalk_row["source_table"],
                "matched_legacy_au_code": crosswalk_row["matched_legacy_au_code"],
                "match_confidence": crosswalk_row["match_confidence"],
                "other_species_pct_encoded_as_dr": other_pct,
                "oaf1_factor": btc_row["oaf1"],
                "oaf2_factor": btc_row["oaf2"],
                "planting_delay": btc_row["planting_delay"],
                "planted_percent": btc_row["planted_percent"],
            }
        )

    handoff = pd.DataFrame(rows, columns=list(DEFAULT_BTC_MSYT_COLUMNS))
    mapping = pd.DataFrame(mappings)
    manifest = {
        "input_crosswalk": CROSSWALK_PATH.relative_to(INSTANCE_ROOT).as_posix(),
        "input_parameter_library": PARAMETER_LIBRARY_PATH.relative_to(
            INSTANCE_ROOT
        ).as_posix(),
        "output_btc_csv": OUTPUT_CSV_PATH.relative_to(INSTANCE_ROOT).as_posix(),
        "output_curve_id_map": MAPPING_CSV_PATH.relative_to(INSTANCE_ROOT).as_posix(),
        "selected_au_count": int(selected["au_id"].nunique()),
        "curve_lane_count": int(selected["curve_lane"].nunique()),
        "btc_row_count": int(len(handoff)),
        "feature_id_policy": "600000 + selected_AU_area_rank * 10 + lane_code",
        "lane_codes": LANE_CODES,
        "oaf_policy": "MP10 percent reductions are converted to BTC factors.",
        "regen_delay_policy": (
            "Use first numeric MP10 delay where present; otherwise existing-managed "
            "lanes use 0 and future-managed uses 1."
        ),
        "other_species_policy": (
            "MP10 other species share is encoded as Dr for this executable review "
            "handoff and flagged in the curve-id map. If the matched MP10 row has "
            "no deciduous/other site-index value, the static TFL 6 AU mean SI is "
            "used as the BTC Dr SI fallback."
        ),
        "planted_percent_policy": (
            "Rows are emitted as 100 percent planted/managed because the reviewed "
            "MP10 rows provide one managed species composition; the MP10 future "
            "row text is treated as delay context, not planted-area proportion."
        ),
        "confidence_counts": (
            mapping.groupby(["curve_lane", "match_confidence"])
            .size()
            .unstack(fill_value=0)
            .to_dict(orient="index")
        ),
        "rows_with_other_species_as_dr": int(
            (mapping["other_species_pct_encoded_as_dr"] > 0).sum()
        ),
    }
    return handoff, mapping, manifest


def write_markdown(mapping: pd.DataFrame, manifest: dict[str, object]) -> None:
    confidence = (
        mapping.groupby(["curve_lane", "match_confidence"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    largest = mapping.sort_values("area_ha", ascending=False).head(20)
    lines = [
        "# TFL 6 P3.4e BatchTIPSY Handoff Manifest",
        "",
        "## Purpose",
        "",
        "This P3.4e artifact converts the selected top-area TFL 6 AU/MP10 TIPSY",
        "crosswalk into the canonical BTC `03_input-tfl6.csv` handoff. It does",
        "not run `TIPSYbtc.exe`, parse `04_output`, write the model-input bundle,",
        "or emit Patchworks runtime files.",
        "",
        "## Outputs",
        "",
        f"- BTC input CSV: `{manifest['output_btc_csv']}`",
        f"- Curve ID map: `{manifest['output_curve_id_map']}`",
        f"- Rows: `{manifest['btc_row_count']}`",
        f"- Selected AUs: `{manifest['selected_au_count']}`",
        f"- Curve lanes per AU: `{manifest['curve_lane_count']}`",
        "",
        "## Translation Policies",
        "",
        f"- Feature IDs: {manifest['feature_id_policy']}.",
        f"- OAF: {manifest['oaf_policy']}",
        f"- Regen delay: {manifest['regen_delay_policy']}",
        f"- Other species: {manifest['other_species_policy']}",
        f"- Planted percent: {manifest['planted_percent_policy']}",
        "",
        "## Confidence Counts",
        "",
        confidence.to_markdown(index=False),
        "",
        "## Largest Handoff Rows",
        "",
        largest[
            [
                "feature_id",
                "au_id",
                "curve_lane",
                "area_ha",
                "matched_legacy_au_code",
                "match_confidence",
                "other_species_pct_encoded_as_dr",
            ]
        ].to_markdown(index=False),
        "",
        "## Review Boundary",
        "",
        "The handoff is executable input for BTC review, but it is not yet accepted",
        "treated-yield output. P3.4e still needs the BTC run, parsed output,",
        "TIPSY/VDYP overlay diagnostics, and row-level review of low-confidence or",
        "`other`-species rows before Phase 3 can move from curve construction to",
        "treatment-option design.",
        "",
    ]
    MANIFEST_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    handoff, mapping, manifest = build_handoff()
    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    handoff.to_csv(OUTPUT_CSV_PATH, index=False)
    mapping.to_csv(MAPPING_CSV_PATH, index=False)
    MANIFEST_JSON_PATH.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown(mapping, manifest)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
