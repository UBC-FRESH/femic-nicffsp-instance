"""Extract MP11 multi-series THLB growing-stock charts."""

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
class SeriesBand:
    """Colour and vertical-band filter for one growing-stock series."""

    name: str
    label: str
    color: str
    tolerance: float
    band_top_px: int
    band_bottom_px: int


@dataclass(frozen=True)
class FigureConfig:
    """Manual extraction configuration for one growing-stock figure."""

    figure_id: str
    caption: str
    pdf_page: int
    image_path: str
    plot_left: float
    plot_right: float
    plot_top: float
    plot_bottom: float
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    series_bands: list[SeriesBand]


@dataclass(frozen=True)
class SeriesSummary:
    """Compact summary of one recovered growing-stock series."""

    figure_id: str
    series_name: str
    label: str
    point_count: int
    x_min: float | None
    x_max: float | None
    y_min: float | None
    y_max: float | None
    y_mean: float | None


@dataclass(frozen=True)
class FigureSummary:
    """Compact summary of one recovered growing-stock figure."""

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
    plot_left: float
    plot_right: float
    plot_top: float
    plot_bottom: float
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    series_count: int
    point_count: int
    residual_point_count: int
    component_sum_minus_total_mean_abs_percent: float | None
    component_sum_minus_total_max_abs_percent: float | None
    review_status: str
    downstream_use: str
    notes: str


def _configs(runtime_root: Path) -> list[FigureConfig]:
    proposal_dir = runtime_root / "crops" / "priority_high_proposals"
    series_bands = [
        SeriesBand(
            name="thlb_gs_total",
            label="THLB GS total",
            color="#000000",
            tolerance=80,
            band_top_px=20,
            band_bottom_px=130,
        ),
        SeriesBand(
            name="thlb_gs_le_120_years",
            label="THLB GS <= 120 years",
            color="#4cff00",
            tolerance=90,
            band_top_px=50,
            band_bottom_px=260,
        ),
        SeriesBand(
            name="thlb_gs_gt_120_years",
            label="THLB GS > 120 years",
            color="#1c531f",
            tolerance=80,
            band_top_px=300,
            band_bottom_px=445,
        ),
    ]
    return [
        FigureConfig(
            figure_id="Figure 3",
            caption="Base Case THLB Growing Stock By 1-120 Years Old And 120+ Years Old Categories",
            pdf_page=83,
            image_path=str(proposal_dir / "figure-3-proposal.png"),
            plot_left=195,
            plot_right=991,
            plot_top=4,
            plot_bottom=458,
            x_min=0,
            x_max=300,
            y_min=0,
            y_max=45_000_000,
            series_bands=series_bands,
        ),
        FigureConfig(
            figure_id="Figure 40",
            caption="AAC Recommendation THLB Growing Stock By 1-120 Years Old Categories",
            pdf_page=143,
            image_path=str(proposal_dir / "figure-40-proposal.png"),
            plot_left=181,
            plot_right=977,
            plot_top=24,
            plot_bottom=488,
            x_min=0,
            x_max=300,
            y_min=0,
            y_max=45_000_000,
            series_bands=series_bands,
        ),
    ]


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)


def _sample_series(
    image: np.ndarray,
    config: FigureConfig,
    calibration: Calibration,
    band: SeriesBand,
    sample_every_px: int,
) -> SeriesResult:
    plot = image[
        int(config.plot_top) : int(config.plot_bottom) + 1,
        int(config.plot_left) : int(config.plot_right) + 1,
    ]
    target = np.array(_hex_to_rgb(band.color), dtype=float)
    points: list[DataPoint] = []
    previous_y: float | None = None
    for x_local in range(0, plot.shape[1], sample_every_px):
        column = plot[:, x_local, :].astype(float)
        distance = np.linalg.norm(column - target, axis=1)
        y_candidates = np.where(distance <= band.tolerance)[0]
        if len(y_candidates):
            y_candidates = y_candidates[
                (y_candidates >= band.band_top_px) & (y_candidates <= band.band_bottom_px)
            ]
        if not len(y_candidates):
            continue
        if previous_y is None:
            y_local = float(np.min(y_candidates)) if band.name != "thlb_gs_gt_120_years" else float(np.max(y_candidates))
        else:
            y_local = float(y_candidates[np.argmin(np.abs(y_candidates - previous_y))])
        previous_y = y_local
        y_pixel = y_local + config.plot_top
        x_pixel = float(x_local) + config.plot_left
        x_value, y_value = calibration.pixel_to_data(x_pixel, y_pixel)
        points.append(
            DataPoint(
                series=band.name,
                x=x_value,
                y=y_value,
                x_pixel=x_pixel,
                y_pixel=y_pixel,
                confidence=1.0,
            )
        )

    diagnostics = [
        Diagnostic(
            level="info",
            code="banded_colour_series_extracted",
            message="Extracted series using colour threshold and manual y-band filtering.",
            context={
                "series": band.name,
                "label": band.label,
                "tolerance": band.tolerance,
                "band_top_px": band.band_top_px,
                "band_bottom_px": band.band_bottom_px,
                "point_count": len(points),
            },
        )
    ]
    return SeriesResult(
        spec=SeriesSpec(
            name=band.name,
            color=band.color,
            mode="line",
            tolerance=band.tolerance,
            sample_every_px=sample_every_px,
            line_aggregation="median",
        ),
        points=points,
        diagnostics=diagnostics,
    )


def _residuals(result: DigitizeResult) -> tuple[int, float | None, float | None]:
    by_series = {
        series.spec.name: {round(point.x, 3): point.y for point in series.points}
        for series in result.series
    }
    names = {"thlb_gs_total", "thlb_gs_le_120_years", "thlb_gs_gt_120_years"}
    if not names <= set(by_series):
        return 0, None, None
    common_x = set.intersection(*(set(by_series[name]) for name in names))
    residuals = []
    for x_value in common_x:
        total = by_series["thlb_gs_total"][x_value]
        if total == 0:
            continue
        component_sum = (
            by_series["thlb_gs_le_120_years"][x_value]
            + by_series["thlb_gs_gt_120_years"][x_value]
        )
        residuals.append(abs(component_sum - total) / total * 100)
    if not residuals:
        return 0, None, None
    return len(residuals), sum(residuals) / len(residuals), max(residuals)


def _series_summary(figure_id: str, result: DigitizeResult, labels: dict[str, str]) -> list[SeriesSummary]:
    summaries: list[SeriesSummary] = []
    for series in result.series:
        xs = [point.x for point in series.points]
        ys = [point.y for point in series.points]
        summaries.append(
            SeriesSummary(
                figure_id=figure_id,
                series_name=series.spec.name,
                label=labels[series.spec.name],
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
    recovered_dir = runtime_root / "recovered" / "growing_stock_batch"
    overlay_dir = runtime_root / "overlays" / "growing_stock_batch"
    recovered_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    figure_summaries: list[FigureSummary] = []
    series_summaries: list[SeriesSummary] = []

    for config in _configs(runtime_root):
        image_path = Path(config.image_path)
        figure_slug = config.figure_id.lower().replace(" ", "-")
        image = Image.open(image_path).convert("RGB")
        array = np.array(image)
        calibration = Calibration.from_plot_bounds(
            plot_left=config.plot_left,
            plot_right=config.plot_right,
            plot_top=config.plot_top,
            plot_bottom=config.plot_bottom,
            x_min=config.x_min,
            x_max=config.x_max,
            y_min=config.y_min,
            y_max=config.y_max,
            notes="Manual plot-frame estimate for growing-stock multi-series extraction.",
        )
        spec = DigitizeSpec(
            calibration=calibration,
            series=[
                SeriesSpec(
                    name=band.name,
                    color=band.color,
                    tolerance=band.tolerance,
                    mode="line",
                    sample_every_px=5,
                )
                for band in config.series_bands
            ],
            image_id=f"{figure_slug}-growing-stock",
            source_document_id="tfl6-mp11",
            source_figure_id=config.figure_id,
            figure_label=f"{config.figure_id} {config.caption}",
            source_page=config.pdf_page,
            extraction_tool_version="0.1.0a1",
            extraction_settings={
                "phase": "P7",
                "batch": "growing_stock",
                "status": "raw_extraction",
                "method": "banded_colour_line_sampling",
                "qa_basis": "component_sum_minus_total_residual",
            },
        )
        series_results = [
            _sample_series(array, config, calibration, band, sample_every_px=5)
            for band in config.series_bands
        ]
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

        residual_count, residual_mean, residual_max = _residuals(result)
        labels = {band.name: band.label for band in config.series_bands}
        figure_series_summaries = _series_summary(config.figure_id, result, labels)
        series_summaries.extend(figure_series_summaries)
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
                plot_left=config.plot_left,
                plot_right=config.plot_right,
                plot_top=config.plot_top,
                plot_bottom=config.plot_bottom,
                x_min=config.x_min,
                x_max=config.x_max,
                y_min=config.y_min,
                y_max=config.y_max,
                series_count=len(result.series),
                point_count=sum(len(series.points) for series in result.series),
                residual_point_count=residual_count,
                component_sum_minus_total_mean_abs_percent=residual_mean,
                component_sum_minus_total_max_abs_percent=residual_max,
                review_status="raw_extraction",
                downstream_use="not_yet_accepted",
                notes=(
                    "Internal component-sum QA looks useful, but max residual spikes "
                    "require value review before comparison acceptance."
                ),
            )
        )

    _write_csv(summary_csv, figure_summaries)
    _write_csv(series_csv, series_summaries)
    payload = {
        "batch": "growing_stock",
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
        default=Path("planning/tfl6_mp11_growing_stock_extraction_summary.csv"),
    )
    parser.add_argument(
        "--series-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_growing_stock_series_summary.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_growing_stock_extraction_summary.json"),
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
            "series",
            figure.series_count,
            "points",
            figure.point_count,
            "mean_abs_residual_percent",
            f"{figure.component_sum_minus_total_mean_abs_percent:.3f}",
            "max_abs_residual_percent",
            f"{figure.component_sum_minus_total_max_abs_percent:.3f}",
        )
    print(f"extracted {len(figures)} figures and {len(series)} series")
    print(args.summary_csv)
    print(args.series_csv)
    print(args.summary_json)


if __name__ == "__main__":
    main()
