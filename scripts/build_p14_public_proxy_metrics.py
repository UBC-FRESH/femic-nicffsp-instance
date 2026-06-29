"""Build P14.3 public proxy metrics for harvest-system assignment."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "planning"

STAND_TABLE = ROOT / "data/mp11_model_input_bundle/stand_table.csv"
AFLB_FEATHER = ROOT / "data/mp11_model_input_bundle/input_geometry/aflb_current.feather"
P9D_SLOPE_STATS = PLANNING / "tfl6_mp11_p9d_public_dem_slope_zonal_stats.csv"
DRA_ROADS = ROOT / "data/source/tfl_6/roads/dra_roads_tfl6.gpkg"
EVIDENCE_JSON = PLANNING / "tfl6_mp11_phase14_harvest_system_evidence.json"

OUT_CSV = PLANNING / "tfl6_mp11_phase14_public_proxy_metrics.csv"
OUT_JSON = PLANNING / "tfl6_mp11_phase14_public_proxy_metrics.json"
OUT_MD = PLANNING / "tfl6_mp11_phase14_public_proxy_metrics.md"

SPECIES_GROUPS = {
    "cw": {"CW"},
    "fd": {"FD", "FDC", "FDI"},
    "yc": {"YC", "YCC", "YCY"},
    "hembal": {"HW", "HM", "BA", "BG"},
    "pine": {"PL", "PLC", "PLI", "PW"},
    "deciduous": {"AC", "ACT", "AT", "BP", "DR", "MB", "TW", "VB"},
}

SLOPE_WEIGHTED_COLS = [
    "slope_mean_pct",
    "slope_median_pct",
    "slope_p90_pct",
    "prop_slope_ge_60pct",
    "prop_slope_ge_70pct",
    "prop_slope_ge_80pct",
    "prop_slope_ge_90pct",
]

OUTPUT_COLUMNS = [
    "stand_id",
    "source_polygon_key",
    "source_feature_id",
    "map_id",
    "polygon_id",
    "aflb_area_ha",
    "thlb_area_ha",
    "managed_share",
    "ifm",
    "thlb_flag",
    "is_managed_current_thlb",
    "projected_age_years",
    "projected_height_m",
    "projected_height_class",
    "volume_metric_m3_ha",
    "volume_metric_source",
    "cw_pct",
    "fd_pct",
    "yc_pct",
    "cw_fd_yc_pct",
    "hembal_pct",
    "pine_pct",
    "deciduous_pct",
    "slope_metric_status",
    "slope_source_area_ha",
    "slope_mean_pct",
    "slope_median_pct",
    "slope_p90_pct",
    "slope_max_pct",
    "prop_slope_ge_60pct",
    "prop_slope_ge_70pct",
    "prop_slope_ge_80pct",
    "prop_slope_ge_90pct",
    "p9d_step220_high_steepness_context",
    "road_distance_status",
    "nearest_dra_road_m",
    "access_distance_proxy_bin",
    "heli_economic_metric_status",
    "heli_economic_proxy_pass",
    "metric_missing_fields",
    "metric_caveat",
]


def _repo(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _read_stands() -> pd.DataFrame:
    return pd.read_csv(STAND_TABLE)


def _read_aflb() -> gpd.GeoDataFrame:
    return gpd.read_feather(AFLB_FEATHER)


def _source_key(frame: pd.DataFrame, source_col: str, map_col: str, polygon_col: str) -> pd.Series:
    return (
        frame[source_col].astype("Int64").astype(str)
        + ":"
        + frame[map_col].astype(str)
        + ":"
        + frame[polygon_col].astype("Int64").astype(str)
    )


def _species_pct(row: pd.Series, codes: set[str]) -> float:
    total = 0.0
    for index in range(1, 7):
        species = row.get(f"species_cd_{index}")
        pct = row.get(f"species_pct_{index}")
        if pd.isna(species) or pd.isna(pct):
            continue
        if str(species).upper() in codes:
            total += float(pct)
    return total


def _species_metrics(aflb: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, row in aflb.iterrows():
        cw = _species_pct(row, SPECIES_GROUPS["cw"])
        fd = _species_pct(row, SPECIES_GROUPS["fd"])
        yc = _species_pct(row, SPECIES_GROUPS["yc"])
        rows.append(
            {
                "stand_id": row["aflb_fragment_id"],
                "cw_pct": cw,
                "fd_pct": fd,
                "yc_pct": yc,
                "cw_fd_yc_pct": cw + fd + yc,
                "hembal_pct": _species_pct(row, SPECIES_GROUPS["hembal"]),
                "pine_pct": _species_pct(row, SPECIES_GROUPS["pine"]),
                "deciduous_pct": _species_pct(row, SPECIES_GROUPS["deciduous"]),
            }
        )
    return pd.DataFrame(rows)


def _volume_metric(aflb: pd.DataFrame) -> pd.DataFrame:
    volume_125 = pd.to_numeric(aflb["live_stand_volume_125"], errors="coerce")
    volume_175 = pd.to_numeric(aflb["live_stand_volume_175"], errors="coerce")
    volume = volume_125.where(volume_125.notna(), volume_175)
    source = np.where(
        volume_125.notna(),
        "live_stand_volume_125",
        np.where(volume_175.notna(), "live_stand_volume_175", "missing"),
    )
    return pd.DataFrame(
        {
            "stand_id": aflb["aflb_fragment_id"],
            "projected_age_years": pd.to_numeric(aflb["proj_age_1"], errors="coerce"),
            "projected_height_m": pd.to_numeric(aflb["proj_height_1"], errors="coerce"),
            "projected_height_class": aflb["proj_height_class_cd_1"].astype("string"),
            "volume_metric_m3_ha": volume,
            "volume_metric_source": source,
        }
    )


def _weighted_average(group: pd.DataFrame, column: str) -> float | None:
    values = pd.to_numeric(group[column], errors="coerce")
    weights = pd.to_numeric(group["source_fragment_area_ha"], errors="coerce")
    valid = values.notna() & weights.notna() & (weights > 0)
    if not bool(valid.any()):
        return None
    return float(np.average(values[valid], weights=weights[valid]))


def _slope_metrics() -> pd.DataFrame:
    slope = pd.read_csv(P9D_SLOPE_STATS)
    records: list[dict[str, Any]] = []
    for source_key, group in slope.groupby("source_polygon_id", dropna=False):
        row: dict[str, Any] = {
            "source_polygon_key": str(source_key),
            "slope_source_area_ha": float(
                pd.to_numeric(group["source_fragment_area_ha"], errors="coerce").sum()
            ),
            "slope_max_pct": float(
                pd.to_numeric(group["slope_max_pct"], errors="coerce").max()
            ),
            "slope_fragment_count": int(len(group)),
        }
        for column in SLOPE_WEIGHTED_COLS:
            row[column] = _weighted_average(group, column)
        records.append(row)
    return pd.DataFrame(records)


def _road_distance(aflb: gpd.GeoDataFrame) -> pd.DataFrame:
    if not DRA_ROADS.exists():
        return pd.DataFrame(
            {
                "stand_id": aflb["aflb_fragment_id"],
                "nearest_dra_road_m": np.nan,
                "road_distance_status": "dra_roads_missing",
            }
        )
    roads = gpd.read_file(DRA_ROADS)
    roads = roads.to_crs(aflb.crs)
    centroids = gpd.GeoDataFrame(
        {"stand_id": aflb["aflb_fragment_id"]},
        geometry=aflb.geometry.representative_point(),
        crs=aflb.crs,
    )
    nearest = gpd.sjoin_nearest(
        centroids,
        roads[["geometry"]],
        how="left",
        distance_col="nearest_dra_road_m",
    )
    nearest = nearest.groupby("stand_id", as_index=False)["nearest_dra_road_m"].min()
    nearest["road_distance_status"] = np.where(
        nearest["nearest_dra_road_m"].notna(),
        "distance_to_dra_road_proxy",
        "nearest_road_missing",
    )
    return nearest


def _distance_bin(distance: float | None) -> str:
    if distance is None or pd.isna(distance):
        return "missing"
    if distance <= 499:
        return "0_499_m"
    if distance <= 999:
        return "500_999_m"
    return "1000_plus_m"


def _heli_pass(row: pd.Series) -> tuple[str, bool]:
    required = {
        "age": row["projected_age_years"],
        "volume": row["volume_metric_m3_ha"],
        "cw_fd_yc": row["cw_fd_yc_pct"],
        "distance": row["nearest_dra_road_m"],
    }
    missing = [name for name, value in required.items() if pd.isna(value)]
    if missing:
        return "missing_" + "_".join(missing), False
    if float(row["projected_age_years"]) <= 80:
        return "age_not_gt_80", False
    distance = float(row["nearest_dra_road_m"])
    volume = float(row["volume_metric_m3_ha"])
    component = float(row["cw_fd_yc_pct"])
    if distance <= 499:
        return "tested_0_499_m", volume >= 350 and component >= 15
    if distance <= 999:
        return "tested_500_999_m", volume >= 370 and component >= 25
    return "tested_1000_plus_m", volume >= 400 and component >= 30


def _missing_fields(row: pd.Series) -> str:
    fields = []
    for column, label in [
        ("projected_age_years", "age"),
        ("volume_metric_m3_ha", "volume"),
        ("cw_fd_yc_pct", "species_share"),
        ("slope_mean_pct", "slope"),
        ("nearest_dra_road_m", "road_distance"),
    ]:
        if pd.isna(row[column]):
            fields.append(label)
    return ";".join(fields) if fields else "none"


def _build_metrics() -> pd.DataFrame:
    stands = _read_stands()
    aflb = _read_aflb()
    aflb["source_polygon_key"] = _source_key(
        aflb,
        "SOURCE_FEATURE_ID",
        "MAP_ID",
        "polygon_id",
    )
    base = stands[
        [
            "stand_id",
            "source_feature_id",
            "map_id",
            "polygon_id",
            "aflb_area_ha",
            "thlb_area_ha",
            "managed_share",
            "ifm",
            "thlb_flag",
        ]
    ].copy()
    base["source_polygon_key"] = _source_key(
        base,
        "source_feature_id",
        "map_id",
        "polygon_id",
    )
    base["is_managed_current_thlb"] = (
        (base["ifm"].astype(str) == "managed")
        & (pd.to_numeric(base["thlb_area_ha"], errors="coerce") > 0)
        & (base["thlb_flag"].astype(str).str.lower() == "true")
    )

    metrics = base.merge(_volume_metric(aflb), on="stand_id", how="left")
    metrics = metrics.merge(_species_metrics(aflb), on="stand_id", how="left")
    metrics = metrics.merge(_slope_metrics(), on="source_polygon_key", how="left")
    metrics = metrics.merge(_road_distance(aflb), on="stand_id", how="left")

    metrics["slope_metric_status"] = np.where(
        metrics["slope_mean_pct"].notna(),
        "p9d_source_polygon_slope_proxy",
        "missing_p9d_slope_join",
    )
    metrics["access_distance_proxy_bin"] = metrics["nearest_dra_road_m"].map(_distance_bin)
    metrics["p9d_step220_high_steepness_context"] = (
        pd.to_numeric(metrics["prop_slope_ge_70pct"], errors="coerce") >= 0.75
    )
    heli_status: list[str] = []
    heli_pass: list[bool] = []
    for _, row in metrics.iterrows():
        status, passed = _heli_pass(row)
        heli_status.append(status)
        heli_pass.append(passed)
    metrics["heli_economic_metric_status"] = heli_status
    metrics["heli_economic_proxy_pass"] = heli_pass
    metrics["metric_missing_fields"] = metrics.apply(_missing_fields, axis=1)
    metrics["metric_caveat"] = (
        "Public proxy metrics only; road distance is not MP11 flight distance, "
        "CDED slope is not WFP LiDAR slope, and no WFP LBB geometry is used."
    )
    return metrics[OUTPUT_COLUMNS]


def _safe_sum(frame: pd.DataFrame, column: str) -> float:
    return float(pd.to_numeric(frame[column], errors="coerce").fillna(0).sum())


def _summary(metrics: pd.DataFrame) -> dict[str, Any]:
    managed = metrics[metrics["is_managed_current_thlb"]].copy()
    return {
        "row_count": int(len(metrics)),
        "managed_current_thlb_rows": int(len(managed)),
        "managed_current_thlb_area_ha": _safe_sum(managed, "thlb_area_ha"),
        "rows_with_age": int(metrics["projected_age_years"].notna().sum()),
        "rows_with_volume": int(metrics["volume_metric_m3_ha"].notna().sum()),
        "rows_with_slope": int(metrics["slope_mean_pct"].notna().sum()),
        "rows_with_road_distance": int(metrics["nearest_dra_road_m"].notna().sum()),
        "rows_with_cw_fd_yc": int(metrics["cw_fd_yc_pct"].notna().sum()),
        "managed_rows_with_all_core_metrics": int(
            (
                managed["projected_age_years"].notna()
                & managed["volume_metric_m3_ha"].notna()
                & managed["slope_mean_pct"].notna()
                & managed["nearest_dra_road_m"].notna()
                & managed["cw_fd_yc_pct"].notna()
            ).sum()
        ),
        "heli_proxy_pass_rows": int(metrics["heli_economic_proxy_pass"].sum()),
        "heli_proxy_pass_managed_area_ha": _safe_sum(
            managed[managed["heli_economic_proxy_pass"]],
            "thlb_area_ha",
        ),
        "high_steepness_context_rows": int(
            metrics["p9d_step220_high_steepness_context"].sum()
        ),
        "high_steepness_context_managed_area_ha": _safe_sum(
            managed[managed["p9d_step220_high_steepness_context"]],
            "thlb_area_ha",
        ),
        "missing_field_counts": metrics["metric_missing_fields"].value_counts().to_dict(),
        "access_distance_proxy_bin_counts": (
            metrics["access_distance_proxy_bin"].value_counts().to_dict()
        ),
        "heli_economic_metric_status_counts": (
            metrics["heli_economic_metric_status"].value_counts().to_dict()
        ),
    }


def _write_csv(metrics: pd.DataFrame) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUT_CSV, index=False, quoting=csv.QUOTE_MINIMAL)


def _write_json(metrics: pd.DataFrame) -> dict[str, Any]:
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "phase": "P14.3",
        "status": "public_proxy_metrics_built",
        "inputs": {
            "stand_table": _repo(STAND_TABLE),
            "aflb_geometry": _repo(AFLB_FEATHER),
            "p9d_slope_stats": _repo(P9D_SLOPE_STATS),
            "dra_roads": _repo(DRA_ROADS),
            "evidence_inventory": _repo(EVIDENCE_JSON),
        },
        "outputs": {
            "metrics_csv": _repo(OUT_CSV),
            "summary_json": _repo(OUT_JSON),
            "summary_md": _repo(OUT_MD),
        },
        "summary": _summary(metrics),
        "field_boundary": {
            "slope": "P9D public CDED source-polygon slope stats; not WFP LiDAR slope.",
            "access": "Nearest DRA road distance; not MP11 helicopter flight distance.",
            "species": "Public VRI species percentages; not WFP ITI/LiDAR species inference.",
            "volume": "Public VRI live stand volume proxy; not WFP ITI volume.",
        },
        "non_goals": [
            "No harvest-system classification is accepted in P14.3.",
            "No model-input tables are generated in P14.3.",
            "No ForestModel XML, Matrix Builder outputs, Patchworks runtime artifacts, or scenarios are generated.",
        ],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def _write_md(payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# TFL 6 MP11 Phase 14 Public Proxy Metrics",
        "",
        "This P14.3 output builds stand-level public proxy metrics for later "
        "ground, cable, and heli assignment. It does not classify stands and does "
        "not generate model-input tables, ForestModel XML, Matrix Builder outputs, "
        "Patchworks runtime artifacts, or scenario outputs.",
        "",
        "## Summary",
        "",
        f"- status: `{payload['status']}`",
        f"- row_count: `{summary['row_count']}`",
        f"- managed_current_thlb_rows: `{summary['managed_current_thlb_rows']}`",
        f"- managed_current_thlb_area_ha: `{summary['managed_current_thlb_area_ha']:.3f}`",
        f"- rows_with_age: `{summary['rows_with_age']}`",
        f"- rows_with_volume: `{summary['rows_with_volume']}`",
        f"- rows_with_slope: `{summary['rows_with_slope']}`",
        f"- rows_with_road_distance: `{summary['rows_with_road_distance']}`",
        f"- rows_with_cw_fd_yc: `{summary['rows_with_cw_fd_yc']}`",
        f"- managed_rows_with_all_core_metrics: `{summary['managed_rows_with_all_core_metrics']}`",
        f"- heli_proxy_pass_rows: `{summary['heli_proxy_pass_rows']}`",
        f"- heli_proxy_pass_managed_area_ha: `{summary['heli_proxy_pass_managed_area_ha']:.3f}`",
        f"- high_steepness_context_rows: `{summary['high_steepness_context_rows']}`",
        (
            "- high_steepness_context_managed_area_ha: "
            f"`{summary['high_steepness_context_managed_area_ha']:.3f}`"
        ),
        "",
        "## Access Distance Proxy Bins",
        "",
        "| Bin | Count |",
        "| --- | ---: |",
    ]
    for key, value in sorted(summary["access_distance_proxy_bin_counts"].items()):
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(["", "## Helicopter Economic Metric Status", "", "| Status | Count |", "| --- | ---: |"])
    for key, value in sorted(summary["heli_economic_metric_status_counts"].items()):
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Slope metrics use P9D public CDED source-polygon statistics and are not "
            "WFP LiDAR slope.",
            "- Access metrics use nearest DRA road distance and are not MP11 helicopter "
            "flight distance.",
            "- Species and volume metrics use public VRI attributes and are not WFP ITI "
            "or LBB attributes.",
            "- P14.4 must decide how to classify stands from these metrics and compare "
            "the result against MP11 Table 20 and Table 73 targets.",
            "",
            "## Files",
            "",
            "- `planning/tfl6_mp11_phase14_public_proxy_metrics.csv`",
            "- `planning/tfl6_mp11_phase14_public_proxy_metrics.json`",
            "- `planning/tfl6_mp11_phase14_public_proxy_metrics.md`",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    metrics = _build_metrics()
    _write_csv(metrics)
    payload = _write_json(metrics)
    _write_md(payload)
    print(f"wrote {_repo(OUT_CSV)}")
    print(f"wrote {_repo(OUT_JSON)}")
    print(f"wrote {_repo(OUT_MD)}")


if __name__ == "__main__":
    main()
