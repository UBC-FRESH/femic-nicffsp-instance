"""Run a compact Phase 9 MP11 public-data THLB diagnostic rebuild."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
import yaml


@dataclass(frozen=True)
class ThlbStepResult:
    """Ordered THLB diagnostic result for one scaffold step."""

    step_id: str
    label: str
    order: int
    execution_class: str
    rule_applied: str
    gross_candidate_area_ha: float | None
    ordered_deduction_ha: float | None
    cumulative_area_ha: float
    mp11_target_ha: float | None
    delta_vs_mp11_ha: float | None
    residual_class: str
    model_input_status: str
    notes: str


def _load_recipe(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as src:
        data = yaml.safe_load(src)
    if not isinstance(data, dict):
        raise ValueError(f"Recipe did not parse as a mapping: {path}")
    return data


def _area_ha(frame: gpd.GeoDataFrame) -> float:
    if frame.empty:
        return 0.0
    return float(frame.geometry.area.sum() / 10_000.0)


def _candidate_area(frame: gpd.GeoDataFrame, mask) -> float:
    if frame.empty:
        return 0.0
    return float(frame.loc[mask, frame.geometry.name].area.sum() / 10_000.0)


def _drop_mask(frame: gpd.GeoDataFrame, mask) -> tuple[gpd.GeoDataFrame, float]:
    deduction = _candidate_area(frame, mask)
    kept = frame.loc[~mask].copy()
    return kept, deduction


def _spatial_intersection_mask(frame: gpd.GeoDataFrame, overlay: gpd.GeoDataFrame) -> Any:
    if frame.empty or overlay.empty:
        return frame.index[:0]
    joined = gpd.sjoin(
        frame[[frame.geometry.name]].set_geometry(frame.geometry.name),
        overlay[[overlay.geometry.name]].set_geometry(overlay.geometry.name),
        how="inner",
        predicate="intersects",
    )
    return joined.index.unique()


def _drop_intersecting_stands(
    frame: gpd.GeoDataFrame,
    overlay: gpd.GeoDataFrame,
) -> tuple[gpd.GeoDataFrame, float]:
    hit_index = _spatial_intersection_mask(frame, overlay)
    mask = frame.index.isin(hit_index)
    deduction = _candidate_area(frame, mask)
    return frame.loc[~mask].copy(), deduction


def _buffer_overlay(path: str, distance_m: float) -> gpd.GeoDataFrame:
    data = gpd.read_file(path)
    if data.empty:
        return data
    buffered = data.copy()
    buffered.geometry = data.geometry.buffer(distance_m)
    return buffered


def _polygon_overlay(paths: list[str]) -> gpd.GeoDataFrame:
    frames = []
    for path in paths:
        data = gpd.read_file(path)
        if not data.empty:
            frames.append(data[[data.geometry.name]].copy())
    if not frames:
        return gpd.GeoDataFrame(geometry=[], crs="EPSG:3005")
    return gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=frames[0].crs)


def _result(
    step: dict[str, Any],
    rule: str,
    gross: float | None,
    deduction: float | None,
    cumulative: float,
    residual_class: str,
    notes: str,
) -> ThlbStepResult:
    target = step.get("mp11_target_ha")
    delta = cumulative - float(target) if target is not None else None
    return ThlbStepResult(
        step_id=str(step["step_id"]),
        label=str(step["label"]),
        order=int(step["order"]),
        execution_class=str(step["execution_class"]),
        rule_applied=rule,
        gross_candidate_area_ha=gross,
        ordered_deduction_ha=deduction,
        cumulative_area_ha=cumulative,
        mp11_target_ha=target,
        delta_vs_mp11_ha=delta,
        residual_class=residual_class,
        model_input_status="not_model_input",
        notes=notes,
    )


def run_rebuild(recipe_path: Path, output_csv: Path, output_json: Path, output_md: Path) -> list[ThlbStepResult]:
    recipe = _load_recipe(recipe_path)
    steps = sorted(recipe["steps"], key=lambda row: int(row["order"]))
    remaining = gpd.read_file("data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg")
    results: list[ThlbStepResult] = []

    road_overlay = _buffer_overlay("data/source/tfl_6/roads/dra_roads_tfl6.gpkg", 5.0)
    reserve_overlay = _polygon_overlay(
        [
            "data/source/tfl_6/ogma/ogma_legal_current_tfl6.gpkg",
            "data/source/tfl_6/ogma/ogma_non_legal_current_tfl6.gpkg",
            "data/source/tfl_6/wildlife/wha_approved_tfl6.gpkg",
            "data/source/tfl_6/wildlife/uwr_approved_tfl6.gpkg",
        ]
    )
    riparian_overlay = gpd.GeoDataFrame(
        pd.concat(
            [
                _buffer_overlay("data/source/tfl_6/hydrology/fwa_stream_networks_tfl6.gpkg", 10.0),
                _buffer_overlay("data/source/tfl_6/hydrology/fwa_lakes_tfl6.gpkg", 10.0),
                _buffer_overlay("data/source/tfl_6/hydrology/fwa_wetlands_tfl6.gpkg", 10.0),
            ],
            ignore_index=True,
        ),
        crs=remaining.crs,
    )

    for step in steps:
        step_id = str(step["step_id"])
        if step_id == "mp11_nd_000":
            results.append(
                _result(
                    step,
                    "initial R1 accounting geometry",
                    _area_ha(remaining),
                    None,
                    _area_ha(remaining),
                    "public_match",
                    "Initial accounting area from R1 geometry.",
                )
            )
        elif step_id == "mp11_nd_010":
            mask = remaining["bclcs_level_1"].isin(["N", "U"])
            gross = _candidate_area(remaining, mask)
            remaining, deduction = _drop_mask(remaining, mask)
            results.append(
                _result(
                    step,
                    "bclcs_level_1 in {'N', 'U'}",
                    gross,
                    deduction,
                    _area_ha(remaining),
                    "public_proxy_residual",
                    "Conservative non-forest candidate; broader BCLCS level-2 envelope remains diagnostic.",
                )
            )
        elif step_id == "mp11_nd_020":
            gross = _area_ha(road_overlay)
            remaining, deduction = _drop_intersecting_stands(remaining, road_overlay)
            results.append(
                _result(
                    step,
                    "DRA all-road 5 m buffer full-stand intersection diagnostic",
                    gross,
                    deduction,
                    _area_ha(remaining),
                    "public_proxy_residual",
                    "Road class filters and widths are provisional; full-stand intersection overstates partial road area.",
                )
            )
        elif step_id == "mp11_nd_030":
            results.append(
                _result(
                    step,
                    "checkpoint after non-forest and road diagnostics",
                    None,
                    None,
                    _area_ha(remaining),
                    "checkpoint_delta",
                    "Forested checkpoint comparison only.",
                )
            )
        elif step_id == "mp11_nd_040":
            mask = (
                remaining["non_productive_descriptor_cd"].notna()
                | remaining["non_productive_cd"].notna()
                | (remaining["site_index"].notna() & (remaining["site_index"] < 5))
            )
            gross = _candidate_area(remaining, mask)
            remaining, deduction = _drop_mask(remaining, mask)
            results.append(
                _result(
                    step,
                    "explicit non-productive signal or site_index < 5",
                    gross,
                    deduction,
                    _area_ha(remaining),
                    "public_proxy_residual",
                    "Public inventory/productivity proxy; MP11 LiDAR/LEFI low-site gap remains.",
                )
            )
        elif step_id == "mp11_nd_050":
            results.append(
                _result(
                    step,
                    "checkpoint after productivity diagnostics",
                    None,
                    None,
                    _area_ha(remaining),
                    "checkpoint_delta",
                    "Productive forest checkpoint comparison only.",
                )
            )
        elif step_id == "mp11_nd_060":
            gross = _area_ha(reserve_overlay)
            remaining, deduction = _drop_intersecting_stands(remaining, reserve_overlay)
            results.append(
                _result(
                    step,
                    "current legal/non-legal OGMA plus approved WHA/UWR diagnostic union",
                    gross,
                    deduction,
                    _area_ha(remaining),
                    "public_proxy_residual",
                    "Current public layers are diagnostic; proposed/vintage equivalence remains unaccepted.",
                )
            )
        elif step_id == "mp11_nd_070":
            results.append(
                _result(
                    step,
                    "no public-safe geometry available",
                    None,
                    0.0,
                    _area_ha(remaining),
                    "unavailable_non_public",
                    "Research/PSP/big-tree/karst dependencies remain unavailable or deferred.",
                )
            )
        elif step_id == "mp11_nd_080":
            mask = (
                remaining["proj_height_class_cd_1"].isin(["0", "1", "2"])
                | (remaining["live_stand_volume_125"].notna() & (remaining["live_stand_volume_125"] < 100))
                | (remaining["species_cd_1"].isin(["HW", "HM", "BA"]) & remaining["proj_height_class_cd_1"].isin(["3"]))
            )
            gross = _candidate_area(remaining, mask)
            remaining, deduction = _drop_mask(remaining, mask)
            results.append(
                _result(
                    step,
                    "public VRI low-height, low-volume, or hembal-height3 proxy",
                    gross,
                    deduction,
                    _area_ha(remaining),
                    "public_proxy_residual",
                    "No DEM/slope or WFP LBB geometry; this is a high-uncertainty diagnostic proxy.",
                )
            )
        elif step_id == "mp11_nd_090":
            gross = _area_ha(riparian_overlay)
            remaining, deduction = _drop_intersecting_stands(remaining, riparian_overlay)
            results.append(
                _result(
                    step,
                    "FWA streams/lakes/wetlands 10 m buffer full-stand intersection diagnostic",
                    gross,
                    deduction,
                    _area_ha(remaining),
                    "public_proxy_residual",
                    "Hydrology classes, widths, and shoreline remain unresolved; full-stand intersection overstates partial riparian area.",
                )
            )
        elif step_id == "mp11_nd_100":
            results.append(
                _result(
                    step,
                    "no public DEM/slope derivative available",
                    None,
                    0.0,
                    _area_ha(remaining),
                    "deferred_public_proxy",
                    "Terrain stability and 90 percent slope remain deferred until public DEM/slope is materialized.",
                )
            )
        elif step_id == "mp11_nd_110":
            results.append(
                _result(
                    step,
                    "no aspatial WTRA/retention deduction applied",
                    None,
                    0.0,
                    _area_ha(remaining),
                    "deferred_policy",
                    "WTRA/stand-level retention policy remains a later reviewed aspatial rule.",
                )
            )
        elif step_id == "mp11_nd_120":
            results.append(
                _result(
                    step,
                    "current THLB diagnostic checkpoint",
                    None,
                    None,
                    _area_ha(remaining),
                    "checkpoint_delta",
                    "Current THLB is diagnostic public-data output only, not accepted model input.",
                )
            )
        else:
            raise ValueError(f"Unhandled scaffold step: {step_id}")

    _write_outputs(output_csv, output_json, output_md, results, recipe_path)
    return results


def _write_outputs(output_csv: Path, output_json: Path, output_md: Path, rows: list[ThlbStepResult], recipe_path: Path) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "recipe_path": recipe_path.as_posix(),
        "row_count": len(rows),
        "final_current_thlb_diagnostic_ha": rows[-1].cumulative_area_ha,
        "mp11_current_thlb_target_ha": rows[-1].mp11_target_ha,
        "delta_vs_mp11_current_thlb_ha": rows[-1].delta_vs_mp11_ha,
        "model_input_status": "not_model_input",
        "outputs": {
            "csv": output_csv.as_posix(),
            "json": output_json.as_posix(),
            "markdown": output_md.as_posix(),
        },
        "rows": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, payload, rows)


def _fmt(value: float | None) -> str:
    return "" if value is None else f"{value:,.3f}"


def _write_markdown(path: Path, payload: dict[str, Any], rows: list[ThlbStepResult]) -> None:
    lines = [
        "# TFL 6 MP11 Phase 9 Public-Data THLB Diagnostic Rebuild",
        "",
        "## Purpose",
        "",
        "This P9.5 output records a compact diagnostic public-data THLB rebuild",
        "from the P9.4 ordered scaffold. It writes summary tables only and does",
        "not publish geospatial overlay intermediates or accepted model inputs.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_phase9_thlb_rebuild_summary.md`",
        "- `planning/tfl6_mp11_phase9_thlb_rebuild_summary.csv`",
        "- `planning/tfl6_mp11_phase9_thlb_rebuild_summary.json`",
        "",
        "## Summary",
        "",
        f"- Diagnostic current THLB: `{payload['final_current_thlb_diagnostic_ha']:,.3f} ha`",
        f"- MP11 current THLB comparison target: `{payload['mp11_current_thlb_target_ha']:,.3f} ha`",
        f"- Delta vs MP11 target: `{payload['delta_vs_mp11_current_thlb_ha']:,.3f} ha`",
        "- Model-input status: `not_model_input`",
        "",
        "## Ordered Results",
        "",
        "| Order | Step | Rule | Gross ha | Ordered deduction ha | Cumulative ha | MP11 target ha | Delta ha | Residual class |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.order} | `{row.step_id}` {row.label} | {row.rule_applied} | "
            f"{_fmt(row.gross_candidate_area_ha)} | {_fmt(row.ordered_deduction_ha)} | "
            f"{_fmt(row.cumulative_area_ha)} | {_fmt(row.mp11_target_ha)} | "
            f"{_fmt(row.delta_vs_mp11_ha)} | `{row.residual_class}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a diagnostic public-data rebuild, not an accepted replacement",
            "  THLB surface.",
            "- The run uses conservative public inventory candidates, full-stand",
            "  intersection diagnostics for simple DRA road and FWA hydrology",
            "  buffers, current public legal/reserve layers, and a high-uncertainty",
            "  VRI operability proxy.",
            "- Shoreline, DEM/slope, WFP LBB, WFP ITI/LEFI, proposed/local reserves,",
            "  and WTRA/retention policy gaps remain unresolved or deferred.",
            "- The MP11 current THLB target remains a comparison target only; this",
            "  run does not force-fit to `120,099 ha`.",
            "",
            "## Use Boundary",
            "",
            "Rows in this summary are `not_model_input`. Later phases must explicitly",
            "promote any accepted source-layer/THLB outputs through the Phase 8",
            "evidence-promotion contract before model-input generation.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", type=Path, default=Path("config/tsr/mp11_thlb_rebuild.recipe.yaml"))
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_thlb_rebuild_summary.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_thlb_rebuild_summary.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_phase9_thlb_rebuild_summary.md"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_rebuild(args.recipe, args.output_csv, args.output_json, args.output_md)


if __name__ == "__main__":
    main()
