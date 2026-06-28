"""Extract MP11 cedar inventory stacked-area charts."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from figrecover.calibration import Calibration
from figrecover.io import write_points_csv, write_result_json
from figrecover.models import DataPoint, Diagnostic, DigitizeResult, DigitizeSpec, SeriesResult, SeriesSpec
from figrecover.qa import compute_quality_metrics, render_overlay, write_quality_metrics
from PIL import Image


SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"
SOURCE_URL = (
    "https://www.westernforest.com/wp-content/uploads/2026/06/"
    "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf"
)


@dataclass(frozen=True)
class PanelConfig:
    """Manual panel bounds and axis calibration for one cedar chart panel."""

    panel_id: str
    label: str
    plot_left: float
    plot_right: float
    plot_top: float
    plot_bottom: float
    y_max: float
    total_band_top_px: int
    lower_band_top_px: int


@dataclass(frozen=True)
class FigureConfig:
    """Manual extraction configuration for one cedar figure."""

    figure_id: str
    caption: str
    pdf_page: int
    image_path: str
    panels: list[PanelConfig]


@dataclass(frozen=True)
class SeriesSummary:
    """Compact summary of one recovered cedar series."""

    figure_id: str
    panel_id: str
    species_group: str
    series_name: str
    point_count: int
    x_min: float | None
    x_max: float | None
    y_min: float | None
    y_max: float | None
    y_mean: float | None


@dataclass(frozen=True)
class FigureSummary:
    """Compact summary of one recovered cedar figure."""

    figure_id: str
    caption: str
    pdf_page: int
    source_sha256: str
    source_url: str
    image_path: str
    result_json_path: str
    points_csv_path: str
    overlay_path: str
    metrics_json_path: str
    panel_count: int
    series_count: int
    point_count: int
    min_total_minus_thlb_m3: float | None
    review_status: str
    downstream_use: str
    notes: str


def _configs(runtime_root: Path) -> list[FigureConfig]:
    proposal_dir = runtime_root / "crops" / "priority_high_proposals"
    two_panel = [
        PanelConfig(
            panel_id="yellow_cedar",
            label="Yellow cedar",
            plot_left=172,
            plot_right=516,
            plot_top=73,
            plot_bottom=505,
            y_max=27_000_000,
            total_band_top_px=300,
            lower_band_top_px=315,
        ),
        PanelConfig(
            panel_id="western_red_cedar",
            label="Western red cedar",
            plot_left=583,
            plot_right=927,
            plot_top=73,
            plot_bottom=505,
            y_max=27_000_000,
            total_band_top_px=35,
            lower_band_top_px=45,
        ),
    ]
    old_cedar_panel = [
        PanelConfig(
            panel_id="old_cedar",
            label="Old cedar > 250 years",
            plot_left=195,
            plot_right=991,
            plot_top=69,
            plot_bottom=521,
            y_max=14_000_000,
            total_band_top_px=135,
            lower_band_top_px=35,
        )
    ]
    old_cedar_panel_aac = [
        PanelConfig(
            panel_id="old_cedar",
            label="Old cedar > 250 years",
            plot_left=195,
            plot_right=991,
            plot_top=69,
            plot_bottom=521,
            y_max=14_000_000,
            total_band_top_px=135,
            lower_band_top_px=35,
        )
    ]
    return [
        FigureConfig(
            figure_id="Figure 14",
            caption="Base Case Cedar Inventory in Productive Forests",
            pdf_page=97,
            image_path=str(proposal_dir / "figure-14-proposal.png"),
            panels=two_panel,
        ),
        FigureConfig(
            figure_id="Figure 15",
            caption="Base Case Old Cedar Inventory in Productive Forests",
            pdf_page=98,
            image_path=str(proposal_dir / "figure-15-proposal.png"),
            panels=old_cedar_panel,
        ),
        FigureConfig(
            figure_id="Figure 51",
            caption="AAC Recommendation Cedar Inventory in Productive Forest",
            pdf_page=172,
            image_path=str(proposal_dir / "figure-51-proposal.png"),
            panels=two_panel,
        ),
        FigureConfig(
            figure_id="Figure 52",
            caption="AAC Recommendation Old Cedar Inventory in Productive Forest",
            pdf_page=173,
            image_path=str(proposal_dir / "figure-52-proposal.png"),
            panels=old_cedar_panel_aac,
        ),
    ]


def _colour_distance_mask(plot: np.ndarray, colour: tuple[int, int, int], tolerance: float) -> np.ndarray:
    distance = np.linalg.norm(plot.astype(float) - np.array(colour, dtype=float), axis=2)
    return distance <= tolerance


def _sample_panel(
    image: np.ndarray,
    figure_id: str,
    panel: PanelConfig,
    sample_every_px: int,
) -> list[SeriesResult]:
    calibration = Calibration.from_plot_bounds(
        plot_left=panel.plot_left,
        plot_right=panel.plot_right,
        plot_top=panel.plot_top,
        plot_bottom=panel.plot_bottom,
        x_min=0,
        x_max=300,
        y_min=0,
        y_max=panel.y_max,
        notes=f"Manual stacked-area calibration for {figure_id} {panel.panel_id}.",
    )
    plot = image[
        int(panel.plot_top) : int(panel.plot_bottom) + 1,
        int(panel.plot_left) : int(panel.plot_right) + 1,
    ]
    green_mask = _colour_distance_mask(plot, (76, 255, 0), 105)
    dark_mask = _colour_distance_mask(plot, (28, 66, 42), 75)
    stacked_mask = green_mask | dark_mask

    thlb_points: list[DataPoint] = []
    total_points: list[DataPoint] = []
    nclb_points: list[DataPoint] = []
    for x_local in range(0, plot.shape[1], sample_every_px):
        green_y = np.where(green_mask[:, x_local])[0]
        stack_y = np.where(stacked_mask[:, x_local])[0]
        if len(green_y):
            green_y = green_y[green_y >= panel.lower_band_top_px]
        if len(stack_y):
            stack_y = stack_y[stack_y >= panel.total_band_top_px]
        if not len(green_y) or not len(stack_y):
            continue

        thlb_y_pixel = float(np.min(green_y)) + panel.plot_top
        total_y_pixel = float(np.min(stack_y)) + panel.plot_top
        x_pixel = float(x_local) + panel.plot_left
        x_value, thlb_y = calibration.pixel_to_data(x_pixel, thlb_y_pixel)
        _, total_y = calibration.pixel_to_data(x_pixel, total_y_pixel)
        nclb_y = max(0.0, total_y - thlb_y)
        thlb_points.append(
            DataPoint(
                series=f"{panel.panel_id}_thlb",
                x=x_value,
                y=thlb_y,
                x_pixel=x_pixel,
                y_pixel=thlb_y_pixel,
            )
        )
        total_points.append(
            DataPoint(
                series=f"{panel.panel_id}_total",
                x=x_value,
                y=total_y,
                x_pixel=x_pixel,
                y_pixel=total_y_pixel,
            )
        )
        nclb_points.append(
            DataPoint(
                series=f"{panel.panel_id}_nclb_implied",
                x=x_value,
                y=nclb_y,
                x_pixel=x_pixel,
                y_pixel=total_y_pixel,
            )
        )

    diagnostics = [
        Diagnostic(
            level="info",
            code="stacked_area_boundaries_extracted",
            message="Extracted THLB and total boundaries from stacked cedar area fill.",
            context={
                "panel_id": panel.panel_id,
                "lower_band_top_px": panel.lower_band_top_px,
                "point_count": len(total_points),
            },
        )
    ]
    return [
        SeriesResult(
            spec=SeriesSpec(
                name=f"{panel.panel_id}_thlb",
                color="#4cff00",
                mode="line",
                tolerance=105,
                sample_every_px=sample_every_px,
            ),
            points=thlb_points,
            diagnostics=diagnostics,
        ),
        SeriesResult(
            spec=SeriesSpec(
                name=f"{panel.panel_id}_total",
                color="#1c422a",
                mode="line",
                tolerance=75,
                sample_every_px=sample_every_px,
            ),
            points=total_points,
            diagnostics=diagnostics,
        ),
        SeriesResult(
            spec=SeriesSpec(
                name=f"{panel.panel_id}_nclb_implied",
                color="#31563a",
                mode="line",
                tolerance=75,
                sample_every_px=sample_every_px,
            ),
            points=nclb_points,
            diagnostics=diagnostics,
        ),
    ]


def _series_summaries(figure_id: str, series_results: list[SeriesResult]) -> list[SeriesSummary]:
    summaries: list[SeriesSummary] = []
    for series in series_results:
        xs = [point.x for point in series.points]
        ys = [point.y for point in series.points]
        panel_id, _, suffix = series.spec.name.partition("_")
        if series.spec.name.startswith("western_red_cedar"):
            panel_id = "western_red_cedar"
        elif series.spec.name.startswith("yellow_cedar"):
            panel_id = "yellow_cedar"
        elif series.spec.name.startswith("old_cedar"):
            panel_id = "old_cedar"
        summaries.append(
            SeriesSummary(
                figure_id=figure_id,
                panel_id=panel_id,
                species_group=panel_id.replace("_", " "),
                series_name=series.spec.name,
                point_count=len(series.points),
                x_min=min(xs) if xs else None,
                x_max=max(xs) if xs else None,
                y_min=min(ys) if ys else None,
                y_max=max(ys) if ys else None,
                y_mean=sum(ys) / len(ys) if ys else None,
            )
        )
    return summaries


def _write_csv(path: Path, rows: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def run_batch(
    runtime_root: Path,
    summary_csv: Path,
    series_csv: Path,
    summary_json: Path,
) -> tuple[list[FigureSummary], list[SeriesSummary]]:
    recovered_dir = runtime_root / "recovered" / "cedar_inventory_batch"
    overlay_dir = runtime_root / "overlays" / "cedar_inventory_batch"
    recovered_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    figure_summaries: list[FigureSummary] = []
    series_summaries: list[SeriesSummary] = []
    for config in _configs(runtime_root):
        image_path = Path(config.image_path)
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)
        figure_slug = config.figure_id.lower().replace(" ", "-")
        series_results: list[SeriesResult] = []
        for panel in config.panels:
            series_results.extend(_sample_panel(image_array, config.figure_id, panel, sample_every_px=5))

        spec = DigitizeSpec(
            calibration=Calibration.from_plot_bounds(
                plot_left=min(panel.plot_left for panel in config.panels),
                plot_right=max(panel.plot_right for panel in config.panels),
                plot_top=min(panel.plot_top for panel in config.panels),
                plot_bottom=max(panel.plot_bottom for panel in config.panels),
                x_min=0,
                x_max=300,
                y_min=0,
                y_max=max(panel.y_max for panel in config.panels),
                notes="Composite calibration envelope; per-panel bounds are in extraction settings.",
            ),
            series=[series.spec for series in series_results],
            image_id=f"{figure_slug}-cedar-inventory",
            source_document_id="tfl6-mp11",
            source_figure_id=config.figure_id,
            figure_label=f"{config.figure_id} {config.caption}",
            source_page=config.pdf_page,
            extraction_tool_version="0.1.0a1",
            extraction_settings={
                "phase": "P7",
                "batch": "cedar_inventory",
                "status": "raw_extraction",
                "method": "stacked_area_boundary_sampling",
                "panels": [asdict(panel) for panel in config.panels],
            },
        )
        result = DigitizeResult(
            spec=spec,
            image_path=image_path,
            width=image.width,
            height=image.height,
            series=series_results,
        )
        result_path = recovered_dir / f"{figure_slug}-result.json"
        points_path = recovered_dir / f"{figure_slug}-points.csv"
        overlay_path = overlay_dir / f"{figure_slug}-overlay.png"
        metrics_path = overlay_dir / f"{figure_slug}-metrics.json"
        write_result_json(result, result_path)
        write_points_csv(result, points_path, include_provenance=True)
        render_overlay(result, overlay_path, source_image_path=image_path, point_radius=2)
        metrics = compute_quality_metrics(result)
        write_quality_metrics(metrics, metrics_path)

        summaries = _series_summaries(config.figure_id, series_results)
        series_summaries.extend(summaries)
        total_minus_thlb: list[float] = []
        grouped = {}
        for series in series_results:
            grouped[series.spec.name] = {round(point.x, 3): point.y for point in series.points}
        for panel in config.panels:
            total = grouped.get(f"{panel.panel_id}_total", {})
            thlb = grouped.get(f"{panel.panel_id}_thlb", {})
            for x_value in set(total) & set(thlb):
                total_minus_thlb.append(total[x_value] - thlb[x_value])

        figure_summaries.append(
            FigureSummary(
                figure_id=config.figure_id,
                caption=config.caption,
                pdf_page=config.pdf_page,
                source_sha256=SOURCE_SHA256,
                source_url=SOURCE_URL,
                image_path=str(image_path),
                result_json_path=str(result_path),
                points_csv_path=str(points_path),
                overlay_path=str(overlay_path),
                metrics_json_path=str(metrics_path),
                panel_count=len(config.panels),
                series_count=len(series_results),
                point_count=sum(len(series.points) for series in series_results),
                min_total_minus_thlb_m3=min(total_minus_thlb) if total_minus_thlb else None,
                review_status="raw_extraction",
                downstream_use="not_yet_accepted",
                notes=(
                    "Stacked-area boundary extraction; requires overlay review because no "
                    "adjacent table cross-check is available."
                ),
            )
        )

    _write_csv(summary_csv, figure_summaries)
    _write_csv(series_csv, series_summaries)
    payload = {
        "batch": "cedar_inventory",
        "status": "raw_extraction",
        "figure_count": len(figure_summaries),
        "series_count": len(series_summaries),
        "runtime_root": str(runtime_root),
        "figure_summaries": [asdict(row) for row in figure_summaries],
        "series_summaries": [asdict(row) for row in series_summaries],
    }
    summary_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return figure_summaries, series_summaries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--runtime-root",
        type=Path,
        default=Path("runtime/document_ingestion/tfl6-mp11-full-figures"),
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_cedar_inventory_extraction_summary.csv"),
    )
    parser.add_argument(
        "--series-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_cedar_inventory_series_summary.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_cedar_inventory_extraction_summary.json"),
    )
    args = parser.parse_args()
    figures, series = run_batch(
        runtime_root=args.runtime_root,
        summary_csv=args.summary_csv,
        series_csv=args.series_csv,
        summary_json=args.summary_json,
    )
    for figure in figures:
        print(
            figure.figure_id,
            "panels",
            figure.panel_count,
            "series",
            figure.series_count,
            "points",
            figure.point_count,
            "min_total_minus_thlb_m3",
            f"{figure.min_total_minus_thlb_m3:.1f}" if figure.min_total_minus_thlb_m3 is not None else "NA",
        )
    print(f"extracted {len(figures)} cedar figures and {len(series)} series")
    print(args.summary_csv)
    print(args.series_csv)
    print(args.summary_json)


if __name__ == "__main__":
    main()
