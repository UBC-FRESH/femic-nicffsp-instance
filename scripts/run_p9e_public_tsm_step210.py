"""Materialize public TSM terrain-stability data and test Step 210 rules."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd

from run_p9rf_mp11_table12_resultant_rebuild import _split_by_overlay


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
TFL6_BOUNDARY_PATH = INSTANCE_ROOT / "data/source/tfl_6/aoi/tfl_6_boundary.gpkg"
STEP200_GPKG = INSTANCE_ROOT / "planning/tfl6_mp11_p9rf_table12_step_200.gpkg"
OUTPUT_GPKG = INSTANCE_ROOT / "data/source/tfl_6/terrain/tsm_detailed_polygons_tfl6.gpkg"
SOURCE_PREFIX = INSTANCE_ROOT / "planning/tfl6_mp11_p9e_public_tsm_source_manifest"
SCENARIO_PREFIX = INSTANCE_ROOT / "planning/tfl6_mp11_p9e_step210_tsm_scenarios"
SERVICE_URL = (
    "https://delivery.maps.gov.bc.ca/arcgis/rest/services/whse/"
    "bcgw_pub_whse_terrestrial_ecology/MapServer/18/query"
)
LAYER_URL = (
    "https://delivery.maps.gov.bc.ca/arcgis/rest/services/whse/"
    "bcgw_pub_whse_terrestrial_ecology/MapServer/18"
)
CATALOGUE_URL = (
    "https://catalogue.data.gov.bc.ca/dataset/"
    "terrain-stability-mapping-tsm-detailed-polygons-with-short-attribute-table-spatial-view"
)
MP11_STEP210_TARGET_HA = 1_993.0
PAGE_SIZE = 1000
BC_ALBERS = "EPSG:3005"
OUT_FIELDS = [
    "OBJECTID",
    "TEIS_ID",
    "PROJECT_NAME",
    "PROJECT_TYPE",
    "PROJECT_MAP_SCALE",
    "SLOPE_STABILITY_CLASS_TXT",
    "SLOPE_STABILITY_CLASS_W_ROADS",
    "POLYGON_STABILITY_CLASS_TYPE",
    "FEATURE_AREA_SQM",
]


def main() -> None:
    """Materialize TSM and compare Step 210 candidate rules."""

    boundary = gpd.read_file(TFL6_BOUNDARY_PATH).to_crs(BC_ALBERS)
    raw = _fetch_tsm(boundary)
    clipped = _clip_to_tfl6(raw, boundary)
    OUTPUT_GPKG.parent.mkdir(parents=True, exist_ok=True)
    clipped.to_file(OUTPUT_GPKG, driver="GPKG")

    step200 = gpd.read_file(STEP200_GPKG, layer="active_fragments").to_crs(BC_ALBERS)
    scenarios = _scenario_table(step200, clipped)
    best = scenarios.iloc[0].to_dict()
    accepted = scenarios.loc[scenarios["scenario_id"].eq("roads_v")].iloc[0].to_dict()

    source_payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "catalogue_url": CATALOGUE_URL,
        "arcgis_layer_url": LAYER_URL,
        "arcgis_query_url": SERVICE_URL,
        "source_feature_class": "WHSE_TERRESTRIAL_ECOLOGY.STE_TER_STABILITY_POLYS_SVW",
        "output_gpkg": str(OUTPUT_GPKG.relative_to(INSTANCE_ROOT)),
        "raw_bbox_feature_count": int(len(raw)),
        "tfl6_clipped_feature_count": int(len(clipped)),
        "tfl6_clipped_area_ha": float(clipped.geometry.area.sum() / 10_000.0),
        "field_counts": _field_counts(clipped),
        "caveat": (
            "This public TSM layer is a provincial terrain-stability mapping "
            "source. It is not guaranteed to match WFP's private DTSM/Patchworks "
            "processing, but it is a real public candidate for MP11 Table 12 "
            "Step 210 and must not be treated as unavailable."
        ),
    }
    scenario_payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_gpkg": str(OUTPUT_GPKG.relative_to(INSTANCE_ROOT)),
        "step200_gpkg": str(STEP200_GPKG.relative_to(INSTANCE_ROOT)),
        "mp11_step210_target_ha": MP11_STEP210_TARGET_HA,
        "accepted_public_proxy_candidate": accepted,
        "best_candidate": best,
        "records": scenarios.to_dict(orient="records"),
        "recommended_rule": (
            "Use `roads_v` as the strict public TSM Class V proxy for MP11 "
            "Step 210. Broader `P/IV/V/U` and text-based unstable/potentially "
            "unstable combinations are retained as diagnostics but should not "
            "be used to inflate the deduction because they are still nowhere "
            "near the MP11 benchmark and are less semantically direct."
        ),
    }

    _write_source_outputs(source_payload, clipped)
    _write_scenario_outputs(scenario_payload, scenarios)

    print(f"Wrote {OUTPUT_GPKG}")
    print(f"Wrote {SOURCE_PREFIX.with_suffix('.md')}")
    print(f"Wrote {SCENARIO_PREFIX.with_suffix('.md')}")
    print(
        "Accepted candidate: "
        f"{accepted['scenario_id']} deduction={accepted['deduction_ha']:.3f} "
        f"delta={accepted['delta_to_mp11_ha']:.3f}"
    )


def _fetch_tsm(boundary: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    minx, miny, maxx, maxy = [float(value) for value in boundary.total_bounds]
    features: list[dict] = []
    offset = 0
    while True:
        params = {
            "f": "geojson",
            "where": "1=1",
            "outFields": ",".join(OUT_FIELDS),
            "returnGeometry": "true",
            "outSR": "3005",
            "geometry": f"{minx},{miny},{maxx},{maxy}",
            "geometryType": "esriGeometryEnvelope",
            "inSR": "3005",
            "spatialRel": "esriSpatialRelIntersects",
            "resultRecordCount": PAGE_SIZE,
            "resultOffset": offset,
        }
        url = f"{SERVICE_URL}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url, timeout=180) as response:
            payload = json.loads(response.read().decode("utf-8"))
        page_features = payload.get("features", [])
        features.extend(page_features)
        if len(page_features) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
    if not features:
        raise RuntimeError("No public TSM features were returned for the TFL6 bbox.")
    frame = gpd.GeoDataFrame.from_features(features, crs=BC_ALBERS)
    frame.columns = [str(col).lower() if col != "geometry" else col for col in frame.columns]
    return frame


def _clip_to_tfl6(raw: gpd.GeoDataFrame, boundary: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    clipped = gpd.overlay(raw.to_crs(BC_ALBERS), boundary[["geometry"]], how="intersection")
    clipped = clipped[clipped.geometry.notna() & ~clipped.geometry.is_empty].copy()
    clipped.geometry = clipped.geometry.make_valid()
    clipped = clipped.explode(index_parts=False, ignore_index=True)
    clipped["area_ha"] = clipped.geometry.area / 10_000.0
    return clipped[clipped["area_ha"] > 0].copy()


def _scenario_table(step200: gpd.GeoDataFrame, tsm: gpd.GeoDataFrame) -> pd.DataFrame:
    selectors = {
        "roads_v": tsm["slope_stability_class_w_roads"].isin(["V"]),
        "roads_u": tsm["slope_stability_class_w_roads"].isin(["U"]),
        "roads_p": tsm["slope_stability_class_w_roads"].isin(["P"]),
        "roads_v_or_u": tsm["slope_stability_class_w_roads"].isin(["V", "U"]),
        "roads_iv_v_u": tsm["slope_stability_class_w_roads"].isin(["IV", "V", "U"]),
        "roads_p_v_u": tsm["slope_stability_class_w_roads"].isin(["P", "V", "U"]),
        "roads_p_iv_v_u": tsm["slope_stability_class_w_roads"].isin(["P", "IV", "V", "U"]),
        "text_unstable": tsm["slope_stability_class_txt"].eq("Unstable"),
        "text_potentially_unstable": tsm["slope_stability_class_txt"].eq("Potentially unstable"),
        "text_unstable_or_potentially": tsm["slope_stability_class_txt"].isin(
            ["Unstable", "Potentially unstable"]
        ),
        "text_unstable_or_roads_v": tsm["slope_stability_class_txt"].eq("Unstable")
        | tsm["slope_stability_class_w_roads"].isin(["V"]),
        "text_unstable_or_roads_v_u": tsm["slope_stability_class_txt"].eq("Unstable")
        | tsm["slope_stability_class_w_roads"].isin(["V", "U"]),
    }
    rows = []
    for scenario_id, selector in selectors.items():
        overlay = tsm.loc[selector].copy()
        if overlay.empty:
            deduction_ha = 0.0
            retained_count = len(step200)
            deducted_count = 0
        else:
            retained, deducted = _split_by_overlay(
                step200,
                overlay[["geometry"]].copy(),
                "mp11_t12_210",
                f"diagnostic_{scenario_id}",
            )
            deduction_ha = float(deducted.geometry.area.sum() / 10_000.0)
            retained_count = int(len(retained))
            deducted_count = int(len(deducted))
        rows.append(
            {
                "scenario_id": scenario_id,
                "source_feature_count": int(selector.sum()),
                "source_overlay_area_ha": float(tsm.loc[selector].geometry.area.sum() / 10_000.0),
                "deduction_ha": deduction_ha,
                "delta_to_mp11_ha": deduction_ha - MP11_STEP210_TARGET_HA,
                "abs_delta_to_mp11_ha": abs(deduction_ha - MP11_STEP210_TARGET_HA),
                "delta_to_mp11_pct": (deduction_ha - MP11_STEP210_TARGET_HA)
                / MP11_STEP210_TARGET_HA
                * 100.0,
                "retained_fragment_count": retained_count,
                "deducted_fragment_count": deducted_count,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["abs_delta_to_mp11_ha", "scenario_id"],
    ).reset_index(drop=True)


def _field_counts(frame: gpd.GeoDataFrame) -> dict[str, dict[str, int]]:
    fields = [
        "slope_stability_class_txt",
        "slope_stability_class_w_roads",
        "polygon_stability_class_type",
        "project_name",
    ]
    counts = {}
    for field in fields:
        values = frame[field].fillna("NULL").astype(str).value_counts().to_dict()
        counts[field] = {key: int(value) for key, value in values.items()}
    return counts


def _write_source_outputs(payload: dict[str, object], clipped: gpd.GeoDataFrame) -> None:
    SOURCE_PREFIX.with_suffix(".json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    pd.DataFrame(
        [
            {"field": field, "value": value, "count": count}
            for field, value_counts in payload["field_counts"].items()
            for value, count in value_counts.items()
        ]
    ).to_csv(SOURCE_PREFIX.with_suffix(".csv"), index=False)
    lines = [
        "# TFL 6 MP11 P9E Public TSM Source Manifest",
        "",
        "## Source",
        "",
        f"- Catalogue URL: `{payload['catalogue_url']}`",
        f"- ArcGIS layer URL: `{payload['arcgis_layer_url']}`",
        f"- Feature class: `{payload['source_feature_class']}`",
        f"- Output GPKG: `{payload['output_gpkg']}`",
        "",
        "## Materialization",
        "",
        f"- Raw bbox features: `{payload['raw_bbox_feature_count']}`",
        f"- TFL6-clipped features: `{payload['tfl6_clipped_feature_count']}`",
        f"- TFL6-clipped area: `{payload['tfl6_clipped_area_ha']:.3f} ha`",
        "",
        "## Key Field Counts",
        "",
    ]
    for field, counts in payload["field_counts"].items():
        lines.extend([f"### `{field}`", ""])
        for value, count in counts.items():
            lines.append(f"- `{value}`: `{count}`")
        lines.append("")
    lines.extend(["## Caveat", "", str(payload["caveat"]), ""])
    SOURCE_PREFIX.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")


def _write_scenario_outputs(payload: dict[str, object], scenarios: pd.DataFrame) -> None:
    scenarios.to_csv(SCENARIO_PREFIX.with_suffix(".csv"), index=False)
    SCENARIO_PREFIX.with_suffix(".json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    accepted = payload["accepted_public_proxy_candidate"]
    best = payload["best_candidate"]
    lines = [
        "# TFL 6 MP11 P9E Step 210 Public TSM Scenarios",
        "",
        "## Benchmark",
        "",
        f"- MP11 Step 210 target: `{payload['mp11_step210_target_ha']:.3f} ha`",
        f"- Source GPKG: `{payload['source_gpkg']}`",
        f"- Step 200 surface: `{payload['step200_gpkg']}`",
        "",
        "## Accepted Public Proxy",
        "",
        f"- Scenario: `{accepted['scenario_id']}`",
        f"- Deduction: `{accepted['deduction_ha']:.3f} ha`",
        f"- Delta: `{accepted['delta_to_mp11_ha']:.3f} ha`",
        f"- Percent delta: `{accepted['delta_to_mp11_pct']:.3f}%`",
        "",
        "## Closest Numeric Diagnostic",
        "",
        f"- Scenario: `{best['scenario_id']}`",
        f"- Deduction: `{best['deduction_ha']:.3f} ha`",
        f"- Delta: `{best['delta_to_mp11_ha']:.3f} ha`",
        (
            "- Interpretation: retained for diagnostics only; it is broader "
            "than a strict Class V interpretation and still does not explain "
            "the MP11 Step 210 deduction."
        ),
        "",
        "## Scenario Table",
        "",
        "| Scenario | Source features | Overlay area | Deduction | Delta | Percent delta |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in scenarios.to_dict(orient="records"):
        lines.append(
            "| "
            f"`{row['scenario_id']}` | "
            f"`{row['source_feature_count']}` | "
            f"`{row['source_overlay_area_ha']:.3f}` | "
            f"`{row['deduction_ha']:.3f}` | "
            f"`{row['delta_to_mp11_ha']:.3f}` | "
            f"`{row['delta_to_mp11_pct']:.3f}%` |"
        )
    lines.extend(["", "## Recommendation", "", str(payload["recommended_rule"]), ""])
    SCENARIO_PREFIX.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
