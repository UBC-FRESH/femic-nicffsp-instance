"""Run a P9R resultant-fragment rebuild of MP11 Table 12 THLB steps."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
R1_PATH = INSTANCE_ROOT / "data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg"
STEP010B_JSON = INSTANCE_ROOT / "planning/tfl6_mp11_p9r_step_010b_nontreed_review.json"
ROADS_PATH = INSTANCE_ROOT / "data/source/tfl_6/roads/dra_roads_tfl6.gpkg"
STREAMS_PATH = INSTANCE_ROOT / "data/source/tfl_6/hydrology/fwa_stream_networks_tfl6.gpkg"
LAKES_PATH = INSTANCE_ROOT / "data/source/tfl_6/hydrology/fwa_lakes_tfl6.gpkg"
WETLANDS_PATH = INSTANCE_ROOT / "data/source/tfl_6/hydrology/fwa_wetlands_tfl6.gpkg"
UWR_PATH = INSTANCE_ROOT / "data/source/tfl_6/wildlife/uwr_approved_tfl6.gpkg"
OGMA_LEGAL_PATH = INSTANCE_ROOT / "data/source/tfl_6/ogma/ogma_legal_current_tfl6.gpkg"
WHA_LEGAL_PATH = INSTANCE_ROOT / "data/source/tfl_6/wildlife/wha_approved_tfl6.gpkg"
RECREATION_POLYGONS_PATH = INSTANCE_ROOT / "data/source/tfl_6/recreation/recreation_polygons_tfl6.gpkg"
PSP_ACTIVE_PUBLIC_PATH = INSTANCE_ROOT / "data/source/tfl_6/psp/psp_active_sites_public_tfl6.gpkg"
P9D_SLOPE_ZONAL_CSV = INSTANCE_ROOT / "planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.csv"
OUTPUT_PREFIX = INSTANCE_ROOT / "planning/tfl6_mp11_p9rf_table12"
COMPARISON_CSV = INSTANCE_ROOT / "planning/tfl6_mp11_p9rf_table12_resultant_vs_p9r_comparison.csv"
COMPARISON_JSON = INSTANCE_ROOT / "planning/tfl6_mp11_p9rf_table12_resultant_vs_p9r_comparison.json"
COMPARISON_MD = INSTANCE_ROOT / "planning/tfl6_mp11_p9rf_table12_resultant_vs_p9r_comparison.md"
AREA_TOLERANCE_HA = 0.001
ROAD_BUFFER_M = 5.0
RIPARIAN_STREAM_BUFFER_M = 10.0

KEY_COLUMNS = [
    "feature_id",
    "map_id",
    "polygon_id",
    "bclcs_level_1",
    "bclcs_level_2",
    "bclcs_level_3",
    "bclcs_level_4",
    "bclcs_level_5",
    "for_mgmt_land_base_ind",
    "non_productive_descriptor_cd",
    "non_productive_cd",
    "site_index",
    "species_cd_1",
    "species_pct_1",
    "proj_age_1",
    "proj_age_class_cd_1",
    "proj_height_class_cd_1",
    "live_stand_volume_125",
    "bec_zone_code",
    "bec_subzone",
    "bec_variant",
]

MP11_TARGETS = {
    "mp11_t12_000": 217_197.0,
    "mp11_t12_020": 5_021.0,
    "mp11_t12_030": 196_233.0,
    "mp11_t12_040": 8_808.0,
    "mp11_t12_050": 187_425.0,
    "mp11_t12_060": 9_927.0,
    "mp11_t12_070": 21_193.0,
    "mp11_t12_080": 156_305.0,
    "mp11_t12_090": 5_479.0,
    "mp11_t12_100": 1_619.0,
    "mp11_t12_110": 5_491.0,
    "mp11_t12_120": 5_317.0,
    "mp11_t12_130": 414.0,
    "mp11_t12_140": 17.0,
    "mp11_t12_150": 20.0,
    "mp11_t12_160": 1_576.0,
    "mp11_t12_170": 6.0,
    "mp11_t12_180": 527.0,
    "mp11_t12_190": 3_089.0,
    "mp11_t12_200": 13.0,
    "mp11_t12_210": 1_993.0,
    "mp11_t12_220": 1_820.0,
    "mp11_t12_230": 134.0,
    "mp11_t12_240": 42.0,
    "mp11_t12_250": 3_721.0,
    "mp11_t12_260": 453.0,
    "mp11_t12_270": 4_483.0,
    "mp11_t12_280": 36_216.0,
    "mp11_t12_290": 120_099.0,
    "mp11_t12_300": 1_427.0,
    "mp11_t12_310": 118_672.0,
}

DECIDUOUS_LEADING_CODES = {"DR", "AC", "MB"}
DECIDUOUS_LEADING_MIN_PCT = 90.0
STEP220_PUBLIC_DEM_SLOPE_THRESHOLD_PCT = 70.0
STEP220_PUBLIC_DEM_MIN_STEEP_PROPORTION = 0.75

OLD_P9R_SUMMARIES = {
    "mp11_t12_020": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_step_020_roads.json",
    "mp11_t12_050": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_step_050_aflb_checkpoint.json",
    "mp11_t12_060": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_table12_step_060_low_sites.json",
    "mp11_t12_070": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_table12_step_070_inoperable.json",
    "mp11_t12_080": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_table12_step_080_total_operable_checkpoint.json",
    "mp11_t12_090": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_table12_step_090_riparian.json",
    "mp11_t12_100": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_table12_step_100_uwr.json",
    "mp11_t12_110": INSTANCE_ROOT / "planning/tfl6_mp11_p9r_table12_step_110_legal_ogma.json",
}


@dataclass(frozen=True)
class StepSummary:
    """One resultant-fragment netdown step summary."""

    step_id: str
    label: str
    step_kind: str
    source_area_ha: float
    deducted_area_ha: float
    retained_area_ha: float
    mp11_target_ha: float | None
    delta_to_mp11_ha: float | None
    delta_to_mp11_pct: float | None
    input_fragment_count: int
    active_fragment_count: int
    deducted_fragment_count: int
    balance_error_ha: float
    checkpoint_status: str
    artifact_gpkg: str
    notes: str


def _component_key(frame: gpd.GeoDataFrame) -> pd.Series:
    cols = ["bclcs_level_3", "bclcs_level_4", "bclcs_level_5", "for_mgmt_land_base_ind"]
    return frame[cols].fillna("NULL").astype(str).agg("/".join, axis=1)


def _selected_components() -> set[str]:
    payload = json.loads(STEP010B_JSON.read_text(encoding="utf-8"))
    return set(payload["selected_components"])


def _make_valid(frame: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if frame.empty:
        return frame.copy()
    cleaned = frame.copy()
    cleaned.geometry = cleaned.geometry.make_valid()
    cleaned = cleaned[cleaned.geometry.notna() & ~cleaned.geometry.is_empty].copy()
    cleaned = cleaned.explode(index_parts=False, ignore_index=True)
    cleaned = cleaned[cleaned.geometry.notna() & ~cleaned.geometry.is_empty].copy()
    cleaned["area_ha"] = cleaned.geometry.area / 10_000.0
    return cleaned[cleaned["area_ha"] > 0].copy()


def _assign_fragment_ids(frame: gpd.GeoDataFrame, step_id: str) -> gpd.GeoDataFrame:
    out = frame.copy().reset_index(drop=True)
    out["parent_fragment_id"] = out.get("fragment_id", pd.Series([""] * len(out), index=out.index)).fillna("")
    out["fragment_id"] = [f"p9rf-{step_id}-{idx + 1:08d}" for idx in range(len(out))]
    out["step_id"] = step_id
    out["area_ha"] = out.geometry.area / 10_000.0
    return out


def _base_columns(frame: gpd.GeoDataFrame) -> list[str]:
    cols = [
        "fragment_id",
        "source_polygon_id",
        "parent_fragment_id",
        "step_id",
        "deduction_status",
        "area_ha",
        *KEY_COLUMNS,
        frame.geometry.name,
    ]
    return [col for col in cols if col in frame.columns]


def _load_initial_active() -> gpd.GeoDataFrame:
    r1 = gpd.read_file(R1_PATH)
    keep_cols = [col for col in KEY_COLUMNS if col in r1.columns]
    frame = r1[keep_cols + [r1.geometry.name]].copy()
    frame["source_polygon_id"] = (
        frame["feature_id"].fillna("").astype(str) + ":" + frame["map_id"].fillna("").astype(str) + ":" + frame["polygon_id"].fillna("").astype(str)
    )
    component = _component_key(frame)
    step010b_candidate = frame["bclcs_level_2"].isin(["N", "W"]) | frame["bclcs_level_2"].isna()
    removed = frame["bclcs_level_1"].isin(["N", "U"]) | (step010b_candidate & component.isin(_selected_components()))
    active = frame.loc[~removed].copy()
    active["fragment_id"] = [f"p9rf-source-{idx + 1:08d}" for idx in range(len(active))]
    active["parent_fragment_id"] = ""
    active["step_id"] = "mp11_t12_010b"
    active["deduction_status"] = "active_after_step010b"
    return _make_valid(active)


def _step_summary(
    step_id: str,
    label: str,
    step_kind: str,
    source_area: float,
    retained: gpd.GeoDataFrame,
    deducted: gpd.GeoDataFrame,
    checkpoint_status: str,
    notes: str,
) -> StepSummary:
    retained_area = float(retained.geometry.area.sum() / 10_000.0) if not retained.empty else 0.0
    deducted_area = float(deducted.geometry.area.sum() / 10_000.0) if not deducted.empty else 0.0
    target = MP11_TARGETS.get(step_id)
    delta = None if target is None else (retained_area if step_kind == "checkpoint" else deducted_area) - target
    delta_pct = None if target is None or target == 0 else delta / target * 100.0
    return StepSummary(
        step_id=step_id,
        label=label,
        step_kind=step_kind,
        source_area_ha=source_area,
        deducted_area_ha=deducted_area,
        retained_area_ha=retained_area,
        mp11_target_ha=target,
        delta_to_mp11_ha=delta,
        delta_to_mp11_pct=delta_pct,
        input_fragment_count=-1,
        active_fragment_count=int(len(retained)),
        deducted_fragment_count=int(len(deducted)),
        balance_error_ha=source_area - retained_area - deducted_area,
        checkpoint_status=checkpoint_status,
        artifact_gpkg=str(_step_gpkg(step_id).relative_to(INSTANCE_ROOT)),
        notes=notes,
    )


def _step_gpkg(step_id: str) -> Path:
    short = step_id.replace("mp11_t12_", "step_")
    return Path(f"{OUTPUT_PREFIX}_{short}.gpkg")


def _step_csv(step_id: str) -> Path:
    short = step_id.replace("mp11_t12_", "step_")
    return Path(f"{OUTPUT_PREFIX}_{short}.csv")


def _step_json(step_id: str) -> Path:
    short = step_id.replace("mp11_t12_", "step_")
    return Path(f"{OUTPUT_PREFIX}_{short}.json")


def _step_md(step_id: str) -> Path:
    short = step_id.replace("mp11_t12_", "step_")
    return Path(f"{OUTPUT_PREFIX}_{short}.md")


def _overlay_mask(geometries: gpd.GeoSeries, crs) -> gpd.GeoDataFrame:
    series = gpd.GeoSeries(geometries, crs=crs)
    series = series[series.notna() & ~series.is_empty]
    if series.empty:
        return gpd.GeoDataFrame(geometry=[], crs=crs)
    return gpd.GeoDataFrame(geometry=series, crs=crs).reset_index(drop=True)


def _rows_from_geometry(row: pd.Series, geometry, status: str, geometry_name: str) -> list[dict]:
    if geometry is None or geometry.is_empty:
        return []
    parts = gpd.GeoSeries([geometry], crs=None).make_valid().explode(index_parts=False)
    records: list[dict] = []
    for part in parts:
        if part is None or part.is_empty:
            continue
        record = row.drop(labels=[geometry_name]).to_dict()
        record[geometry_name] = part
        record["deduction_status"] = status
        records.append(record)
    return records


def _split_by_overlay(
    active: gpd.GeoDataFrame,
    overlay: gpd.GeoDataFrame,
    step_id: str,
    deduction_status: str,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    if active.empty or overlay.empty:
        retained = _assign_fragment_ids(active, step_id)
        retained["deduction_status"] = f"active_after_{step_id}"
        return retained, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs)

    active_cols = _base_columns(active)
    working = active[active_cols].copy()
    mask = _make_valid(overlay[[overlay.geometry.name]].copy())
    pairs = gpd.sjoin(
        working[[working.geometry.name]].set_geometry(working.geometry.name),
        mask[[mask.geometry.name]].set_geometry(mask.geometry.name),
        how="inner",
        predicate="intersects",
    )

    deducted_records: list[dict] = []
    matched = set(pairs.index.unique()) if not pairs.empty else set()
    retained_base = working.loc[~working.index.isin(matched)].copy()
    if not retained_base.empty:
        retained_base["deduction_status"] = f"active_after_{step_id}"
    retained_records: list[dict] = retained_base.to_dict(orient="records")

    for polygon_index, row in working.loc[list(matched)].iterrows():
        group = pairs.loc[[polygon_index]]
        local_mask = gpd.GeoSeries(
            [mask.geometry.iloc[int(overlay_index)] for overlay_index in group["index_right"].unique()],
            crs=working.crs,
        ).union_all()
        intersection = row.geometry.intersection(local_mask)
        difference = row.geometry.difference(local_mask)
        deducted_records.extend(_rows_from_geometry(row, intersection, deduction_status, working.geometry.name))
        retained_records.extend(_rows_from_geometry(row, difference, f"active_after_{step_id}", working.geometry.name))

    retained = gpd.GeoDataFrame(retained_records, geometry=working.geometry.name, crs=working.crs)
    deducted = gpd.GeoDataFrame(deducted_records, geometry=working.geometry.name, crs=working.crs)
    retained = _make_valid(retained)
    deducted = _make_valid(deducted)
    deducted = _assign_fragment_ids(deducted, step_id)
    retained = _assign_fragment_ids(retained, step_id)
    deducted["deduction_status"] = deduction_status
    retained["deduction_status"] = f"active_after_{step_id}"
    return retained, deducted


def _split_by_attribute(
    active: gpd.GeoDataFrame,
    selector: pd.Series,
    step_id: str,
    deduction_status: str,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    selected = selector.reindex(active.index).fillna(False).astype(bool)
    deducted = _assign_fragment_ids(active.loc[selected].copy(), step_id)
    retained = _assign_fragment_ids(active.loc[~selected].copy(), step_id)
    deducted["deduction_status"] = deduction_status
    retained["deduction_status"] = f"active_after_{step_id}"
    return retained, deducted


def _split_by_ranked_whole_fragments(
    active: gpd.GeoDataFrame,
    selected_index: pd.Index,
    step_id: str,
    deduction_status: str,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    selected = active.index.isin(selected_index)
    deducted = _assign_fragment_ids(active.loc[selected].copy(), step_id)
    retained = _assign_fragment_ids(active.loc[~selected].copy(), step_id)
    deducted["deduction_status"] = deduction_status
    retained["deduction_status"] = f"active_after_{step_id}"
    return retained, deducted


def _split_unavailable_source(
    active: gpd.GeoDataFrame,
    step_id: str,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    retained = _assign_fragment_ids(active.copy(), step_id)
    retained["deduction_status"] = f"active_after_{step_id}_source_unavailable"
    deducted = gpd.GeoDataFrame(columns=active.columns, geometry=active.geometry.name, crs=active.crs)
    return retained, deducted


def _old_seral_proxy_index(active: gpd.GeoDataFrame, target_ha: float) -> pd.Index:
    ranked = active.copy()
    ranked["rank_age"] = ranked["proj_age_1"].fillna(-1)
    ranked["rank_site"] = ranked["site_index"].fillna(-1)
    ranked = ranked.sort_values(
        ["rank_age", "rank_site", "area_ha", "source_polygon_id", "fragment_id"],
        ascending=[False, False, False, True, True],
    )
    cumulative = ranked["area_ha"].cumsum()
    before = ranked.index[cumulative <= target_ha]
    crossing = cumulative[cumulative > target_ha]
    if crossing.empty:
        return before
    crossing_index = crossing.index[0]
    before_area = float(ranked.loc[before, "area_ha"].sum()) if len(before) else 0.0
    with_crossing_area = before_area + float(ranked.loc[crossing_index, "area_ha"])
    if abs(with_crossing_area - target_ha) < abs(before_area - target_ha):
        return before.append(pd.Index([crossing_index]))
    return before


def _aspatial_area_proxy_index(active: gpd.GeoDataFrame, target_ha: float) -> pd.Index:
    ranked = active.copy()
    ranked = ranked.sort_values(
        ["area_ha", "source_polygon_id", "fragment_id"],
        ascending=[True, True, True],
    )
    cumulative = ranked["area_ha"].cumsum()
    before = ranked.index[cumulative <= target_ha]
    crossing = cumulative[cumulative > target_ha]
    if crossing.empty:
        return before
    crossing_index = crossing.index[0]
    before_area = float(ranked.loc[before, "area_ha"].sum()) if len(before) else 0.0
    with_crossing_area = before_area + float(ranked.loc[crossing_index, "area_ha"])
    if abs(with_crossing_area - target_ha) < abs(before_area - target_ha):
        return before.append(pd.Index([crossing_index]))
    return before


def _public_dem_step220_index(active: gpd.GeoDataFrame) -> pd.Index:
    zonal = pd.read_csv(P9D_SLOPE_ZONAL_CSV)
    prop_col = f"prop_slope_ge_{int(STEP220_PUBLIC_DEM_SLOPE_THRESHOLD_PCT)}pct"
    required = {"fragment_id", prop_col}
    missing = required.difference(zonal.columns)
    if missing:
        raise RuntimeError(
            "P9D Step 220 zonal statistics are missing required columns: "
            + ", ".join(sorted(missing))
        )
    selected_ids = set(
        zonal.loc[
            zonal[prop_col].fillna(0.0) >= STEP220_PUBLIC_DEM_MIN_STEEP_PROPORTION,
            "fragment_id",
        ].astype(str)
    )
    return active.index[active["fragment_id"].astype(str).isin(selected_ids)]


def _checkpoint_step(active: gpd.GeoDataFrame, step_id: str, label: str, target: float) -> tuple[gpd.GeoDataFrame, StepSummary]:
    retained = _assign_fragment_ids(active.copy(), step_id)
    retained["deduction_status"] = f"active_checkpoint_{step_id}"
    source_area = float(active.geometry.area.sum() / 10_000.0)
    summary = StepSummary(
        step_id=step_id,
        label=label,
        step_kind="checkpoint",
        source_area_ha=source_area,
        deducted_area_ha=0.0,
        retained_area_ha=source_area,
        mp11_target_ha=target,
        delta_to_mp11_ha=source_area - target,
        delta_to_mp11_pct=(source_area - target) / target * 100.0,
        input_fragment_count=int(len(active)),
        active_fragment_count=int(len(retained)),
        deducted_fragment_count=0,
        balance_error_ha=0.0,
        checkpoint_status="p9rf_resultant_checkpoint",
        artifact_gpkg=str(_step_gpkg(step_id).relative_to(INSTANCE_ROOT)),
        notes="Checkpoint only; no deduction at this Table 12 row.",
    )
    return retained, summary


def _total_deduction_from_operable(summaries: list[StepSummary]) -> float:
    operable_step_ids = {
        "mp11_t12_090",
        "mp11_t12_100",
        "mp11_t12_110",
        "mp11_t12_120",
        "mp11_t12_130",
        "mp11_t12_140",
        "mp11_t12_150",
        "mp11_t12_160",
        "mp11_t12_170",
        "mp11_t12_180",
        "mp11_t12_190",
        "mp11_t12_200",
        "mp11_t12_210",
        "mp11_t12_220",
        "mp11_t12_230",
        "mp11_t12_240",
        "mp11_t12_250",
        "mp11_t12_260",
        "mp11_t12_270",
    }
    return float(sum(summary.deducted_area_ha for summary in summaries if summary.step_id in operable_step_ids))


def _total_operable_reductions_checkpoint(
    active: gpd.GeoDataFrame,
    summaries: list[StepSummary],
) -> tuple[gpd.GeoDataFrame, StepSummary]:
    retained = _assign_fragment_ids(active.copy(), "mp11_t12_280")
    retained["deduction_status"] = "active_checkpoint_mp11_t12_280"
    retained_area = float(retained.geometry.area.sum() / 10_000.0)
    deducted_area = _total_deduction_from_operable(summaries)
    source_area = retained_area + deducted_area
    target = MP11_TARGETS["mp11_t12_280"]
    summary = StepSummary(
        step_id="mp11_t12_280",
        label="Total Operable Reductions",
        step_kind="checkpoint",
        source_area_ha=source_area,
        deducted_area_ha=deducted_area,
        retained_area_ha=retained_area,
        mp11_target_ha=target,
        delta_to_mp11_ha=deducted_area - target,
        delta_to_mp11_pct=(deducted_area - target) / target * 100.0,
        input_fragment_count=int(len(active)),
        active_fragment_count=int(len(retained)),
        deducted_fragment_count=0,
        balance_error_ha=source_area - retained_area - deducted_area,
        checkpoint_status="p9rf_total_operable_reductions_checkpoint",
        artifact_gpkg=str(_step_gpkg("mp11_t12_280").relative_to(INSTANCE_ROOT)),
        notes=(
            "Checkpoint only. Reports cumulative P9RF operable reductions from Step 090 through Step 270 "
            "against the MP11 total-operable-reductions target. This row validates the deduction total; "
            "the retained area is the same active surface used for the Current THLB checkpoint."
        ),
    )
    return retained, summary


def _write_step(summary: StepSummary, active: gpd.GeoDataFrame, deducted: gpd.GeoDataFrame) -> None:
    gpkg = _step_gpkg(summary.step_id)
    if gpkg.exists():
        gpkg.unlink()
    active[_base_columns(active)].to_file(gpkg, layer="active_fragments", driver="GPKG")
    if deducted.empty:
        empty = gpd.GeoDataFrame(columns=_base_columns(active), geometry="geometry", crs=active.crs)
        empty.to_file(gpkg, layer="deducted_fragments", driver="GPKG")
    else:
        deducted[_base_columns(deducted)].to_file(gpkg, layer="deducted_fragments", driver="GPKG")

    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "summary": asdict(summary),
        "area_balance_passed": abs(summary.balance_error_ha) <= AREA_TOLERANCE_HA,
        "layers": {
            "active_fragments": "retained resultant fragments after this step",
            "deducted_fragments": "fragments removed by this step",
        },
    }
    _step_json(summary.step_id).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    with _step_csv(summary.step_id).open("w", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(summary).keys()))
        writer.writeheader()
        writer.writerow(asdict(summary))
    _step_md(summary.step_id).write_text(_summary_markdown(summary), encoding="utf-8")


def _summary_markdown(summary: StepSummary) -> str:
    target = "" if summary.mp11_target_ha is None else f"{summary.mp11_target_ha:,.3f} ha"
    delta = "" if summary.delta_to_mp11_ha is None else f"{summary.delta_to_mp11_ha:,.3f} ha"
    delta_pct = "" if summary.delta_to_mp11_pct is None else f"{summary.delta_to_mp11_pct:.4f}%"
    return "\n".join(
        [
            f"# TFL 6 MP11 P9RF {summary.step_id} {summary.label}",
            "",
            "## Result",
            "",
            f"- Step kind: `{summary.step_kind}`",
            f"- Source area: `{summary.source_area_ha:,.3f} ha`",
            f"- Deducted area: `{summary.deducted_area_ha:,.3f} ha`",
            f"- Retained area: `{summary.retained_area_ha:,.3f} ha`",
            f"- MP11 comparison target: `{target}`",
            f"- Delta to MP11: `{delta}` (`{delta_pct}`)",
            f"- Input fragments: `{summary.input_fragment_count:,}`",
            f"- Active fragments: `{summary.active_fragment_count:,}`",
            f"- Deducted fragments: `{summary.deducted_fragment_count:,}`",
            f"- Balance error: `{summary.balance_error_ha:.9f} ha`",
            f"- Checkpoint status: `{summary.checkpoint_status}`",
            "",
            "## Notes",
            "",
            summary.notes,
            "",
            "## Artifact",
            "",
            f"- GeoPackage: `{summary.artifact_gpkg}`",
            "- Layers: `active_fragments`, `deducted_fragments`",
            "",
        ]
    )


def _assert_step(summary: StepSummary, active: gpd.GeoDataFrame, deducted: gpd.GeoDataFrame) -> None:
    if abs(summary.balance_error_ha) > AREA_TOLERANCE_HA:
        raise AssertionError(f"{summary.step_id} balance error {summary.balance_error_ha:.6f} ha")
    if active.empty:
        raise AssertionError(f"{summary.step_id} produced empty active fragments")
    if not active.is_valid.all():
        raise AssertionError(f"{summary.step_id} active fragments contain invalid geometries")
    if not deducted.empty and not deducted.is_valid.all():
        raise AssertionError(f"{summary.step_id} deducted fragments contain invalid geometries")
    if active["fragment_id"].duplicated().any():
        raise AssertionError(f"{summary.step_id} duplicate active fragment IDs")
    reported = float(active.geometry.area.sum() / 10_000.0)
    if abs(reported - summary.retained_area_ha) > AREA_TOLERANCE_HA:
        raise AssertionError(f"{summary.step_id} reported retained area mismatch")


def _run_deduction_step(
    active: gpd.GeoDataFrame,
    step_id: str,
    label: str,
    step_kind: str,
    split_func,
    checkpoint_status: str,
    notes: str,
) -> tuple[gpd.GeoDataFrame, StepSummary]:
    print(f"running {step_id}: {label}", flush=True)
    source_area = float(active.geometry.area.sum() / 10_000.0)
    retained, deducted = split_func(active)
    summary = _step_summary(step_id, label, step_kind, source_area, retained, deducted, checkpoint_status, notes)
    summary = StepSummary(**{**asdict(summary), "input_fragment_count": int(len(active))})
    _assert_step(summary, retained, deducted)
    _write_step(summary, retained, deducted)
    print(
        f"finished {step_id}: retained={summary.retained_area_ha:,.3f} ha "
        f"deducted={summary.deducted_area_ha:,.3f} ha fragments={summary.active_fragment_count:,}",
        flush=True,
    )
    return retained, summary


def _road_overlay(crs) -> gpd.GeoDataFrame:
    roads = gpd.read_file(ROADS_PATH).to_crs(crs)
    selected = roads[roads["FEATURE_TYPE"].isin(["Road", "Bridge"]) & ~roads["ROAD_CLASS"].isin(["trail", "water"])]
    buffers = selected.geometry.buffer(ROAD_BUFFER_M)
    return _overlay_mask(buffers, crs)


def _riparian_overlay(crs) -> gpd.GeoDataFrame:
    streams = gpd.read_file(STREAMS_PATH).to_crs(crs)
    lakes = gpd.read_file(LAKES_PATH).to_crs(crs)
    wetlands = gpd.read_file(WETLANDS_PATH).to_crs(crs)
    geoms = pd.concat(
        [
            streams.geometry.buffer(RIPARIAN_STREAM_BUFFER_M),
            lakes.geometry,
            wetlands.geometry,
        ],
        ignore_index=True,
    )
    return _overlay_mask(gpd.GeoSeries(geoms, crs=crs), crs)


def _public_overlay(path: Path, crs) -> gpd.GeoDataFrame:
    frame = gpd.read_file(path).to_crs(crs)
    return _overlay_mask(frame.geometry, crs)


def _recreation_overlay(crs) -> gpd.GeoDataFrame:
    polygons = gpd.read_file(RECREATION_POLYGONS_PATH).to_crs(crs)
    selected = polygons[
        polygons["LIFE_CYCLE_STATUS_CODE"].eq("ACTIVE")
        & polygons["RETIREMENT_DATE"].isna()
        & polygons["RECREATION_FEATURE_CODE"].eq("L5")
    ].copy()
    return _overlay_mask(selected.geometry, crs)


def _old_p9r_value(step_id: str) -> float | None:
    path = OLD_P9R_SUMMARIES.get(step_id)
    if path is None or not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if step_id == "mp11_t12_020":
        return payload["step"]["area_after_ha"]
    if step_id == "mp11_t12_050":
        return payload["summary"]["aflb_checkpoint_area_ha"]
    if step_id in {"mp11_t12_060", "mp11_t12_070"}:
        key = "area_after_step060_ha" if step_id == "mp11_t12_060" else "area_after_step070_ha"
        locked = payload["locked_scenario_id"]
        return {row["scenario_id"]: row for row in payload["scenarios"]}[locked][key]
    if step_id == "mp11_t12_080":
        return payload["summary"]["area_after_step070_ha"]
    if step_id == "mp11_t12_090":
        locked = payload["locked_scenario_id"]
        return {row["scenario_id"]: row for row in payload["scenarios"]}[locked]["area_after_step090_ha"]
    if step_id in {"mp11_t12_100", "mp11_t12_110"}:
        key = "area_after_step100_ha" if step_id == "mp11_t12_100" else "area_after_step110_ha"
        return payload["summary"][key]
    return None


def run_rebuild() -> list[StepSummary]:
    """Run the full P9RF resultant-fragment rebuild through Step 130."""

    active = _load_initial_active()
    summaries: list[StepSummary] = []

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_020",
        "Less Existing Roads & Powerlines",
        "deduction",
        lambda frame: _split_by_overlay(frame, _road_overlay(frame.crs), "mp11_t12_020", "deducted_existing_roads_5m"),
        "locked_p9rf_resultant_step020",
        "DRA Road/Bridge features, excluding trail/water ROAD_CLASS, buffered 5 m and physically erased from fragments.",
    )
    summaries.append(summary)

    active, summary = _checkpoint_step(active, "mp11_t12_030", "Total Forested", MP11_TARGETS["mp11_t12_030"])
    _assert_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    _write_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_040",
        "Less Non-productive",
        "deduction",
        lambda frame: _split_by_attribute(
            frame,
            frame["non_productive_descriptor_cd"].notna()
            | frame["non_productive_cd"].notna()
            | (frame["site_index"].notna() & (frame["site_index"] < 5))
            | frame["for_mgmt_land_base_ind"].eq("N"),
            "mp11_t12_040",
            "deducted_nonproductive_public_proxy",
        ),
        "locked_p9rf_resultant_step040",
        "Locked public-data non-productive proxy applied as whole-fragment attribute removal after road fragmentation.",
    )
    summaries.append(summary)

    active, summary = _checkpoint_step(active, "mp11_t12_050", "Total Productive", MP11_TARGETS["mp11_t12_050"])
    _assert_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    _write_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_060",
        "Low Sites",
        "deduction",
        lambda frame: _split_by_attribute(
            frame,
            frame["site_index"].notna() & (frame["site_index"] <= 9),
            "mp11_t12_060",
            "deducted_low_site_index_le_9",
        ),
        "locked_p9rf_resultant_step060",
        "Locked public-data low-sites proxy `site_index <= 9` applied to resultant fragments.",
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_070",
        "Less Inoperable",
        "deduction",
        lambda frame: _split_by_attribute(
            frame,
            frame["live_stand_volume_125"].notna() & (frame["live_stand_volume_125"] < 85),
            "mp11_t12_070",
            "deducted_inoperable_volume_lt_85",
        ),
        "locked_p9rf_resultant_step070",
        "Locked public-data inoperability proxy `live_stand_volume_125 < 85` applied to resultant fragments.",
    )
    summaries.append(summary)

    active, summary = _checkpoint_step(active, "mp11_t12_080", "Total Operable", MP11_TARGETS["mp11_t12_080"])
    _assert_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    _write_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_090",
        "Riparian Management",
        "deduction",
        lambda frame: _split_by_overlay(
            frame,
            _riparian_overlay(frame.crs),
            "mp11_t12_090",
            "deducted_fwa_riparian_proxy_10m_streams_waterbody_footprints",
        ),
        "locked_p9rf_resultant_step090",
        (
            "FWA streams buffered 10 m plus lakes/wetlands footprints, physically erased from Step 080 "
            "resultant fragments. Approved for the P9RF teaching/research public-data lane with documented "
            "non-equivalence to WFP LiDAR-classified riparian inputs."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_100",
        "Ungulate Winter Ranges",
        "deduction",
        lambda frame: _split_by_overlay(
            frame,
            _public_overlay(UWR_PATH, frame.crs),
            "mp11_t12_100",
            "deducted_approved_public_uwr",
        ),
        "locked_p9rf_resultant_step100",
        (
            "Approved public UWR polygons physically erased from Step 090 resultant fragments. Approved for "
            "the P9RF teaching/research public-data lane; gross source area is effectively identical to the "
            "published MP11 total UWR area."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_110",
        "Old Growth Management Areas",
        "deduction",
        lambda frame: _split_by_overlay(
            frame,
            _public_overlay(OGMA_LEGAL_PATH, frame.crs),
            "mp11_t12_110",
            "diagnostic_deducted_current_legal_ogma",
        ),
        "locked_p9rf_resultant_step110",
        (
            "Current legal public OGMA polygons physically erased from true Step 100 resultant fragments. "
            "Accepted for the P9RF teaching/research public-data lane because gross legal OGMA geometry "
            "closely matches MP11; the high ordered net deduction remains documented as a public-data versus "
            "private WFP upstream-overlap gap."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_120",
        "Old Growth Management Areas - Proposed",
        "deduction_proxy",
        lambda frame: _split_by_ranked_whole_fragments(
            frame,
            _old_seral_proxy_index(frame, MP11_TARGETS["mp11_t12_120"]),
            "mp11_t12_120",
            "deducted_old_seral_proposed_ogma_proxy",
        ),
        "locked_p9rf_resultant_step120",
        (
            "Proposed OGMA geometry is unavailable in public data. Current non-legal OGMA is only 0.687 ha "
            "inside TFL 6 and is not a direct MP11 proposed-OGMA source. This accepted proxy removes oldest "
            "remaining whole fragments until near the MP11 Step 120 net target as an old-seral teaching proxy; "
            "accepted for the P9RF teaching/research public-data lane because the net deduction is within 3 ha "
            "of MP11 while preserving the source-availability caveat."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_130",
        "Wildlife Habitat Areas - Legal",
        "deduction",
        lambda frame: _split_by_overlay(
            frame,
            _public_overlay(WHA_LEGAL_PATH, frame.crs),
            "mp11_t12_130",
            "deducted_approved_public_wha",
        ),
        "locked_p9rf_resultant_step130",
        (
            "Approved public WHA polygons physically erased from the true Step 120 resultant surface. "
            "Accepted for the P9RF teaching/research public-data lane as a defensible public legal-WHA overlay "
            "with an explicit current-vintage and private-upstream-overlap caveat; the high net delta is "
            "documented rather than tuned away."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_140",
        "Wildlife Habitat Areas - Proposed",
        "deduction_unavailable",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_140"),
        "review_required_p9rf_step140_proposed_wha_source_unavailable",
        (
            "No separate public proposed-WHA geometry is available in the current source stack. The row is "
            "carried forward as an explicit zero-deduction source-unavailable placeholder rather than an "
            "arbitrary benchmark-tuned proxy for the small MP11 17 ha net deduction."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_150",
        "Uneconomic",
        "deduction_unavailable",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_150"),
        "review_required_p9rf_step150_wfp_economic_operability_source_unavailable",
        (
            "MP11 Step 150 is a small uneconomic deduction tied to WFP LBB/ITI/LEFI/economic-operability "
            "evidence that is unavailable in the public source stack. The row is carried forward as an "
            "explicit zero-deduction source-unavailable placeholder rather than an arbitrary 20 ha proxy."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_160",
        "Deciduous-leading",
        "deduction",
        lambda frame: _split_by_attribute(
            frame,
            frame["species_cd_1"].isin(DECIDUOUS_LEADING_CODES)
            & frame["species_pct_1"].fillna(0).ge(DECIDUOUS_LEADING_MIN_PCT),
            "mp11_t12_160",
            "deducted_deciduous_leading_dr_ac_mb_pct90",
        ),
        "locked_p9rf_resultant_step160",
        (
            "Public inventory attribute rule removes whole resultant fragments where leading species is one "
            "of DR, AC, or MB and leading-species composition is at least 90%. This calibrated threshold "
            "keeps the rule tied to deciduous-dominant stands while avoiding blanket removal of mixed "
            "deciduous-leading fragments; it does not deduct deciduous secondary components in "
            "conifer-leading stands."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_170",
        "Recreation",
        "deduction",
        lambda frame: _split_by_overlay(
            frame,
            _recreation_overlay(frame.crs),
            "mp11_t12_170",
            "deducted_active_l5_recreation_polygon_proxy",
        ),
        "locked_p9rf_resultant_step170",
        (
            "Public recreation overlay uses active recreation polygon features with RECREATION_FEATURE_CODE "
            "L5. This subset is accepted for the P9RF teaching/research public-data lane as a defensible "
            "small recreation-feature proxy with gross area close to the MP11 Step 170 total area; broader "
            "active recreation polygons overstate the row and trails/points are retained as context unless "
            "separately accepted."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_180",
        "Known Archaeological Sites",
        "deduction_unavailable_sensitive",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_180"),
        "skipped_p9rf_step180_public_data_only_sensitive_source_excluded",
        (
            "Known archaeological-site geometry is sensitive/source-restricted and is not present in the "
            "public source stack. P9RF intentionally skips this Table 12 row because this unrestricted "
            "teaching and learning model instance uses only publicly available data. Do not infer or "
            "synthesize archaeological geometry from the published aggregate area."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_190",
        "Existing Stand-level Reserves",
        "deduction_proxy",
        lambda frame: _split_by_ranked_whole_fragments(
            frame,
            _old_seral_proxy_index(frame, MP11_TARGETS["mp11_t12_190"]),
            "mp11_t12_190",
            "deducted_old_seral_existing_wtra_proxy",
        ),
        "locked_p9rf_resultant_step190",
        (
            "Existing WTRA spatial inventory is not available in the public source stack. This candidate "
            "uses an oldest-remaining-whole-fragment proxy to approximate the MP11 Step 190 net target for "
            "the public teaching lane. Accepted as an ecologically interpretable old-seral reserve proxy, "
            "but it is not a reconstruction of WFP operational WTRA geometry."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_200",
        "Research Site",
        "deduction_unavailable_sensitive",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_200"),
        "skipped_p9rf_step200_public_data_only_sensitive_source_excluded",
        (
            "Research-site and PSP-style location geometry is sensitive or source-restricted and is not "
            "present in the public source stack. P9RF intentionally skips this Table 12 row because this "
            "unrestricted teaching and learning model instance uses only publicly available data. Do not "
            "infer or synthesize research-site geometry from the published aggregate area."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_210",
        "Terrain Stability - Class 5",
        "deduction_deferred_public_source",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_210"),
        "deferred_p9rf_step210_public_terrain_stability_source_needed",
        (
            "No accepted public DTSM terrain-stability Class 5 source is materialized in the current source "
            "stack. P9RF carries this row as a zero-deduction deferred public-source placeholder. A later "
            "public DEM/terrain materialization lane may replace this row, but no non-terrain proxy is used "
            "for the unrestricted teaching model."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_220",
        "Terrain Stability - LiDAR 90% + Slope",
        "deduction_proxy",
        lambda frame: _split_by_ranked_whole_fragments(
            frame,
            _public_dem_step220_index(frame),
            "mp11_t12_220",
            "deducted_public_cded_70pct_slope_75pct_fragment_proxy",
        ),
        "locked_p9rf_step220_public_cded_steep_slope_proxy",
        (
            "Accepted public CDED steep-slope proxy for MP11 Step 220. The rule deducts true Step 210 "
            "resultant fragments where at least 75% of valid CDED pixels are >=70% slope, based on "
            "`planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.csv` and scenario report "
            "`planning/tfl6_mp11_p9d_step220_dem_slope_scenarios.md`. CDED is coarser and smoother than "
            "LiDAR, so this is a public-data teaching/research proxy, not WFP LiDAR equivalence."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_230",
        "Permanent Sample Plots",
        "deduction",
        lambda frame: _split_by_overlay(
            frame,
            _public_overlay(PSP_ACTIVE_PUBLIC_PATH, frame.crs),
            "mp11_t12_230",
            "deducted_public_active_psp_all_buffers",
        ),
        "locked_p9rf_step230_public_active_psp_proxy",
        (
            "Public BC Data Catalogue active PSP polygons physically erased from the true Step 220 resultant "
            "surface. The locked public-data proxy uses all TFL6-clipped active PSP polygons from "
            "`WHSE_FOREST_VEGETATION.ISMC_PSP_ACTIVE_SITES_SP`, accepting the public geometry as-is rather "
            "than filtering lower-coordinate-confidence 300 m buffers. Accepted for the P9RF teaching/research "
            "public-data lane with an explicit non-equivalence caveat relative to WFP private Patchworks inputs."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_240",
        "Big Tree Reserves",
        "deduction_deferred_public_source",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_240"),
        "deferred_p9rf_step240_public_big_tree_source_needed",
        (
            "No accepted public big-tree reserve or registry-derived geometry is materialized in the current "
            "source stack. P9RF carries this small row as a zero-deduction deferred public-source placeholder "
            "until a reviewed public source exists."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_250",
        "Karst",
        "deduction_deferred_public_source",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_250"),
        "deferred_p9rf_step250_public_karst_source_needed",
        (
            "No accepted public karst likelihood, karst protection, or operational karst reserve geometry is "
            "materialized in the current source stack. P9RF carries this row as a zero-deduction deferred "
            "public-source placeholder until a reviewed karst source exists."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_260",
        "Unknown Cultural Features within Quatsino TUS Zone",
        "deduction_unavailable_sensitive",
        lambda frame: _split_unavailable_source(frame, "mp11_t12_260"),
        "skipped_p9rf_step260_public_data_only_sensitive_source_excluded",
        (
            "Unknown cultural-feature and TUS-zone geometry is sensitive or source-restricted and is not "
            "present in the public source stack. P9RF intentionally skips this Table 12 row because this "
            "unrestricted teaching and learning model instance uses only publicly available data. Do not "
            "infer or synthesize cultural/TUS geometry from the published aggregate area."
        ),
    )
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_270",
        "Future Stand-level Reserves",
        "deduction_proxy",
        lambda frame: _split_by_ranked_whole_fragments(
            frame,
            _old_seral_proxy_index(frame, MP11_TARGETS["mp11_t12_270"]),
            "mp11_t12_270",
            "deducted_old_seral_future_stand_level_reserve_proxy",
        ),
        "review_required_p9rf_step270_future_stand_reserve_old_seral_proxy_candidate",
        (
            "Future stand-level reserve geometry is a policy/model-time assumption rather than a public "
            "current-condition overlay. This candidate uses an oldest-remaining-whole-fragment proxy to "
            "approximate the MP11 Step 270 net target for the public teaching lane. It is an old-seral "
            "retention proxy, not a reconstruction of WFP Patchworks future WTRA placement."
        ),
    )
    summaries.append(summary)

    active, summary = _total_operable_reductions_checkpoint(active, summaries)
    _assert_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    _write_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    summaries.append(summary)

    active, summary = _checkpoint_step(active, "mp11_t12_290", "Current THLB", MP11_TARGETS["mp11_t12_290"])
    _assert_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    _write_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    summaries.append(summary)

    active, summary = _run_deduction_step(
        active,
        "mp11_t12_300",
        "Less future roads",
        "deduction_proxy",
        lambda frame: _split_by_ranked_whole_fragments(
            frame,
            _aspatial_area_proxy_index(frame, MP11_TARGETS["mp11_t12_300"]),
            "mp11_t12_300",
            "deducted_aspatial_future_roads_area_proxy",
        ),
        "locked_p9rf_step300_aspatial_future_roads_proxy",
        (
            "Future roads are long-term land-base context, not current THLB. Because future road alignments "
            "are unknown, P9RF implements this row as an aspatial area netdown proxy using smallest-current "
            "resultant fragments to approximate the MP11 net deduction. The deducted fragments are an area "
            "accounting placeholder and must not be interpreted as predicted future road locations."
        ),
    )
    summaries.append(summary)

    active, summary = _checkpoint_step(active, "mp11_t12_310", "Long-term Land Base", MP11_TARGETS["mp11_t12_310"])
    summary = StepSummary(
        **{
            **asdict(summary),
            "checkpoint_status": "p9rf_long_term_land_base_checkpoint_reached",
            "notes": (
                "Context checkpoint after future roads; keep separate from current THLB. Step 300 is "
                "implemented as an aspatial future-road area proxy, not mapped future-road geometry."
            ),
        }
    )
    _assert_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    _write_step(summary, active, gpd.GeoDataFrame(columns=active.columns, geometry="geometry", crs=active.crs))
    summaries.append(summary)

    _write_comparison(summaries)
    return summaries


def _write_comparison(summaries: list[StepSummary]) -> None:
    rows = []
    for summary in summaries:
        p9rf_area = summary.retained_area_ha
        old_area = _old_p9r_value(summary.step_id)
        rows.append(
            {
                "step_id": summary.step_id,
                "label": summary.label,
                "p9rf_retained_area_ha": p9rf_area,
                "p9rf_deducted_area_ha": summary.deducted_area_ha,
                "old_p9r_retained_area_ha": old_area,
                "p9rf_minus_old_p9r_area_ha": None if old_area is None else p9rf_area - old_area,
                "mp11_target_ha": summary.mp11_target_ha,
                "delta_to_mp11_ha": summary.delta_to_mp11_ha,
                "delta_to_mp11_pct": summary.delta_to_mp11_pct,
                "checkpoint_status": summary.checkpoint_status,
                "artifact_gpkg": summary.artifact_gpkg,
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(COMPARISON_CSV, index=False)
    COMPARISON_JSON.write_text(
        json.dumps({"generated_at_utc": datetime.now(UTC).isoformat(), "rows": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# TFL 6 MP11 P9RF Resultant-Fragment Comparison",
        "",
        "This table compares the new resultant-fragment lane against the prior",
        "partial-area-accounting P9R lane where a comparable retained area exists.",
        "",
        "| Step | Label | P9RF retained ha | P9RF deducted ha | Old P9R retained ha | P9RF - old ha | MP11 target ha | Delta to MP11 ha | Status |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        old = "" if row["old_p9r_retained_area_ha"] is None else f"{row['old_p9r_retained_area_ha']:,.3f}"
        old_delta = "" if row["p9rf_minus_old_p9r_area_ha"] is None else f"{row['p9rf_minus_old_p9r_area_ha']:,.3f}"
        target = "" if row["mp11_target_ha"] is None else f"{row['mp11_target_ha']:,.3f}"
        delta = "" if row["delta_to_mp11_ha"] is None else f"{row['delta_to_mp11_ha']:,.3f}"
        lines.append(
            f"| `{row['step_id']}` | {row['label']} | {row['p9rf_retained_area_ha']:,.3f} | "
            f"{row['p9rf_deducted_area_ha']:,.3f} | {old} | {old_delta} | {target} | {delta} | "
            f"`{row['checkpoint_status']}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The `p9rf` lane is the production candidate because its checkpoint geometry",
            "is the net area. The previous `p9r` lane remains audit/prototype evidence",
            "and should not be used as a downstream resultant-fragment model input.",
            "",
        ]
    )
    COMPARISON_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run the P9RF rebuild."""

    run_rebuild()


if __name__ == "__main__":
    main()
