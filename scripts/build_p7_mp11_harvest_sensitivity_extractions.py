"""Extract first-batch MP11 harvest-sensitivity line charts.

The batch is intentionally conservative: it covers simple two-series,
flat-line harvest-level charts with visible MP11 summary table values that can
be used as a first QA target. Detailed recovered tables and overlays remain in
ignored runtime paths; tracked outputs are compact summaries only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np
from figrecover.calibration import Calibration
from figrecover.digitize import DigitizeSpec
from figrecover.io import write_points_csv, write_result_json
from figrecover.models import DataPoint, Diagnostic, DigitizeResult, SeriesResult, SeriesSpec
from figrecover.qa import compute_quality_metrics, render_overlay, write_quality_metrics
from PIL import Image


SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"
SOURCE_URL = (
    "https://www.westernforest.com/wp-content/uploads/2026/06/"
    "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf"
)


@dataclass(frozen=True)
class FigureBatchConfig:
    """Manual configuration for one first-batch sensitivity chart."""

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
    scenario_series_name: str
    table_base_case_m3_per_year: float
    table_scenario_m3_per_year: float
    table_difference_m3_per_year: float
    table_percent_difference: float


@dataclass(frozen=True)
class SeriesSummary:
    """Compact summary of one extracted series."""

    figure_id: str
    series_name: str
    point_count: int
    x_min: float | None
    x_max: float | None
    y_min: float | None
    y_max: float | None
    y_mean: float | None
    expected_table_value: float | None
    mean_minus_table: float | None
    absolute_percent_error: float | None


@dataclass(frozen=True)
class FigureSummary:
    """Compact summary of one extracted figure."""

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
    base_case_table_value: float
    scenario_table_value: float
    table_difference: float
    table_percent_difference: float
    point_count: int
    max_absolute_percent_error: float | None
    review_status: str
    downstream_use: str
    notes: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for block in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _configs(runtime_root: Path) -> list[FigureBatchConfig]:
    proposal_dir = runtime_root / "crops" / "priority_high_proposals"
    common = {
        "plot_left": 184.0,
        "plot_right": 989.0,
        "plot_bottom": 439.0,
        "x_min": 0.0,
        "x_max": 300.0,
        "y_min": 0.0,
        "y_max": 1_400_000.0,
    }
    return [
        FigureBatchConfig(
            figure_id="Figure 29",
            caption="Harvest Levels with Adjusted ITI Stand Yields",
            pdf_page=129,
            image_path=str(proposal_dir / "figure-29-proposal.png"),
            plot_top=-18.7,
            scenario_series_name="adjusted_iti_volume",
            table_base_case_m3_per_year=1_061_600,
            table_scenario_m3_per_year=1_079_000,
            table_difference_m3_per_year=17_400,
            table_percent_difference=1.6,
            **common,
        ),
        FigureBatchConfig(
            figure_id="Figure 30",
            caption="Harvest Levels with ITI adjusted volumes and LiDAR-derived Height and Site Index",
            pdf_page=131,
            image_path=str(proposal_dir / "figure-30-proposal.png"),
            plot_top=-12.1,
            scenario_series_name="adjusted_iti_volume_lidar_height_site_index",
            table_base_case_m3_per_year=1_061_600,
            table_scenario_m3_per_year=1_095_200,
            table_difference_m3_per_year=33_600,
            table_percent_difference=3.2,
            **common,
        ),
        FigureBatchConfig(
            figure_id="Figure 31",
            caption=(
                "Harvest Levels with ITI adjusted volumes, LiDAR-derived Height and Site Index, "
                "and reduced OAF1"
            ),
            pdf_page=132,
            image_path=str(proposal_dir / "figure-31-proposal.png"),
            plot_left=184.0,
            plot_right=989.0,
            plot_top=7.0,
            plot_bottom=459.0,
            x_min=0.0,
            x_max=300.0,
            y_min=0.0,
            y_max=1_400_000.0,
            scenario_series_name="lidar_adjusted_yields_reduced_oaf1",
            table_base_case_m3_per_year=1_061_600,
            table_scenario_m3_per_year=1_150_300,
            table_difference_m3_per_year=88_700,
            table_percent_difference=8.4,
        ),
        FigureBatchConfig(
            figure_id="Figure 35",
            caption="Harvest Levels with MHA Increased by 10 Years",
            pdf_page=144,
            image_path=str(proposal_dir / "figure-35-proposal.png"),
            plot_top=-20.0,
            scenario_series_name="mha_increased_by_10_years",
            table_base_case_m3_per_year=1_061_600,
            table_scenario_m3_per_year=956_000,
            table_difference_m3_per_year=-105_600,
            table_percent_difference=-10.0,
            **common,
        ),
        FigureBatchConfig(
            figure_id="Figure 36",
            caption="Harvest Levels with MHA Decreased by 10 Years",
            pdf_page=145,
            image_path=str(proposal_dir / "figure-36-proposal.png"),
            plot_top=-18.7,
            scenario_series_name="mha_decreased_by_10_years",
            table_base_case_m3_per_year=1_061_600,
            table_scenario_m3_per_year=1_074_300,
            table_difference_m3_per_year=12_300,
            table_percent_difference=1.2,
            **common,
        ),
        FigureBatchConfig(
            figure_id="Figure 39",
            caption="Harvest Levels with 10% THLB Decreases",
            pdf_page=148,
            image_path=str(proposal_dir / "figure-39-proposal.png"),
            plot_top=-20.0,
            scenario_series_name="thlb_decreased_by_10_percent",
            table_base_case_m3_per_year=1_061_600,
            table_scenario_m3_per_year=953_500,
            table_difference_m3_per_year=-108_100,
            table_percent_difference=-10.2,
            **common,
        ),
    ]


def _series_summaries(
    figure_id: str,
    result,
    expected_values: dict[str, float],
) -> list[SeriesSummary]:
    summaries: list[SeriesSummary] = []
    for series in result.series:
        ys = [point.y for point in series.points]
        xs = [point.x for point in series.points]
        expected = expected_values.get(series.spec.name)
        y_mean = sum(ys) / len(ys) if ys else None
        mean_minus_table = None if y_mean is None or expected is None else y_mean - expected
        absolute_percent_error = (
            None
            if mean_minus_table is None or expected in (None, 0)
            else abs(mean_minus_table) / expected * 100.0
        )
        summaries.append(
            SeriesSummary(
                figure_id=figure_id,
                series_name=series.spec.name,
                point_count=len(series.points),
                x_min=min(xs) if xs else None,
                x_max=max(xs) if xs else None,
                y_min=min(ys) if ys else None,
                y_max=max(ys) if ys else None,
                y_mean=y_mean,
                expected_table_value=expected,
                mean_minus_table=mean_minus_table,
                absolute_percent_error=absolute_percent_error,
            )
        )
    return summaries


def _write_csv(path: Path, rows: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def run_batch(
    runtime_root: Path,
    summary_csv: Path,
    series_csv: Path,
    summary_json: Path,
) -> tuple[list[FigureSummary], list[SeriesSummary]]:
    recovered_dir = runtime_root / "recovered" / "harvest_sensitivity_batch"
    overlay_dir = runtime_root / "overlays" / "harvest_sensitivity_batch"
    recovered_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    figure_summaries: list[FigureSummary] = []
    series_summaries: list[SeriesSummary] = []

    for config in _configs(runtime_root):
        figure_slug = config.figure_id.lower().replace(" ", "-")
        image_path = Path(config.image_path)
        result_path = recovered_dir / f"{figure_slug}-result.json"
        points_path = recovered_dir / f"{figure_slug}-points.csv"
        overlay_path = overlay_dir / f"{figure_slug}-overlay.png"
        metrics_path = overlay_dir / f"{figure_slug}-metrics.json"

        calibration = Calibration.from_plot_bounds(
            plot_left=config.plot_left,
            plot_right=config.plot_right,
            plot_top=config.plot_top,
            plot_bottom=config.plot_bottom,
            x_min=config.x_min,
            x_max=config.x_max,
            y_min=config.y_min,
            y_max=config.y_max,
            notes="Manual first-batch plot-frame estimate from proposal crop.",
        )
        spec = DigitizeSpec(
            calibration=calibration,
            series=[
                SeriesSpec(
                    name="base_case",
                    color="#4cff00",
                    mode="line",
                    tolerance=65,
                    sample_every_px=5,
                    line_aggregation="median",
                ),
                SeriesSpec(
                    name=config.scenario_series_name,
                    color="#243a32",
                    mode="line",
                    tolerance=55,
                    sample_every_px=5,
                    line_aggregation="median",
                ),
            ],
            image_id=f"{figure_slug}-harvest-sensitivity",
            source_document_id="tfl6-mp11",
            source_figure_id=config.figure_id,
            figure_label=f"{config.figure_id} {config.caption}",
            source_page=config.pdf_page,
            extraction_tool_version="0.1.0a1",
            extraction_settings={
                "phase": "P7",
                "batch": "harvest_sensitivity",
                "status": "raw_extraction",
                "method": "long_colour_component_line_sampling",
                "long_component_min_width_fraction": 0.60,
                "post_component_y_pixel_window": 10,
                "proposal_crop_sha256": _sha256(image_path),
            },
        )

        result = _digitize_long_components(image_path, spec)
        write_result_json(result, result_path)
        write_points_csv(result, points_path, include_provenance=True)
        render_overlay(result, overlay_path, source_image_path=image_path, point_radius=2)
        metrics = compute_quality_metrics(result)
        write_quality_metrics(metrics, metrics_path)

        expected_values = {
            "base_case": config.table_base_case_m3_per_year,
            config.scenario_series_name: config.table_scenario_m3_per_year,
        }
        figure_series_summaries = _series_summaries(config.figure_id, result, expected_values)
        series_summaries.extend(figure_series_summaries)
        errors = [
            summary.absolute_percent_error
            for summary in figure_series_summaries
            if summary.absolute_percent_error is not None
        ]
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
                base_case_table_value=config.table_base_case_m3_per_year,
                scenario_table_value=config.table_scenario_m3_per_year,
                table_difference=config.table_difference_m3_per_year,
                table_percent_difference=config.table_percent_difference,
                point_count=sum(summary.point_count for summary in figure_series_summaries),
                max_absolute_percent_error=max(errors) if errors else None,
                review_status="raw_extraction",
                downstream_use="not_yet_accepted",
                notes="First-batch deterministic line extraction; requires overlay/value review.",
            )
        )

    _write_csv(summary_csv, figure_summaries)
    _write_csv(series_csv, series_summaries)
    payload = {
        "batch": "harvest_sensitivity",
        "status": "raw_extraction",
        "figure_count": len(figure_summaries),
        "series_count": len(series_summaries),
        "runtime_root": str(runtime_root),
        "figure_summaries": [asdict(row) for row in figure_summaries],
        "series_summaries": [asdict(row) for row in series_summaries],
    }
    summary_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return figure_summaries, series_summaries


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    if len(text) != 6:
        raise ValueError(f"expected #RRGGBB colour, got {value!r}")
    return int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16)


def _digitize_long_components(path: Path, spec: DigitizeSpec) -> DigitizeResult:
    """Digitize flat line charts by sampling long colour components only."""

    image = Image.open(path).convert("RGB")
    array = np.array(image)
    assert spec.calibration.plot_left is not None
    assert spec.calibration.plot_right is not None
    assert spec.calibration.plot_top is not None
    assert spec.calibration.plot_bottom is not None

    left = int(round(spec.calibration.plot_left))
    right = int(round(spec.calibration.plot_right))
    top = int(np.floor(spec.calibration.plot_top))
    bottom = int(round(spec.calibration.plot_bottom))
    crop_top = max(0, top)
    plot = array[crop_top : bottom + 1, left : right + 1]
    min_width = int((right - left) * 0.60)

    series_results: list[SeriesResult] = []
    diagnostics: list[Diagnostic] = []
    for series_spec in spec.series:
        target = np.array(_hex_to_rgb(series_spec.color), dtype=float)
        distance = np.linalg.norm(plot.astype(float) - target, axis=2)
        mask = (distance <= series_spec.tolerance).astype(np.uint8)
        component_count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
        candidates: list[tuple[int, int, int, int, int]] = []
        for label in range(1, component_count):
            _, _, width, height, area = stats[label]
            if width >= min_width and area >= 500:
                candidates.append((int(width), int(area), int(height), int(label), len(candidates)))

        points: list[DataPoint] = []
        series_diagnostics: list[Diagnostic] = []
        if not candidates:
            series_diagnostics.append(
                Diagnostic(
                    level="warning",
                    code="no_long_colour_component",
                    message="No long colour component passed the harvest-sensitivity filters.",
                    context={"series": series_spec.name, "min_width_px": min_width},
                )
            )
        else:
            candidates.sort(reverse=True)
            selected_label = candidates[0][3]
            raw_samples: list[tuple[int, float]] = []
            for x_local in range(0, plot.shape[1], series_spec.sample_every_px):
                column = np.where(labels[:, x_local] == selected_label)[0]
                if len(column):
                    raw_samples.append((x_local, float(np.median(column)) + crop_top))

            if raw_samples:
                median_y = float(np.median([sample[1] for sample in raw_samples]))
                filtered = [
                    sample
                    for sample in raw_samples
                    if abs(sample[1] - median_y) <= 10
                ]
                for x_local, y_pixel in filtered:
                    x_pixel = x_local + left
                    x_value, y_value = spec.calibration.pixel_to_data(x_pixel, y_pixel)
                    points.append(
                        DataPoint(
                            series=series_spec.name,
                            x=x_value,
                            y=y_value,
                            x_pixel=x_pixel,
                            y_pixel=y_pixel,
                            confidence=1.0,
                        )
                    )
                series_diagnostics.append(
                    Diagnostic(
                        level="info",
                        code="long_colour_component_extracted",
                        message="Sampled the dominant long colour component after median-y filtering.",
                        context={
                            "series": series_spec.name,
                            "candidate_count": len(candidates),
                            "raw_sample_count": len(raw_samples),
                            "retained_sample_count": len(filtered),
                            "median_y_pixel": median_y,
                        },
                    )
                )
        series_results.append(
            SeriesResult(spec=series_spec, points=points, diagnostics=series_diagnostics)
        )

    return DigitizeResult(
        spec=spec,
        image_path=path,
        width=image.width,
        height=image.height,
        series=series_results,
        diagnostics=diagnostics,
    )


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
        default=Path("planning/tfl6_mp11_harvest_sensitivity_extraction_summary.csv"),
    )
    parser.add_argument(
        "--series-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_harvest_sensitivity_series_summary.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_harvest_sensitivity_extraction_summary.json"),
    )
    args = parser.parse_args()

    figure_summaries, series_summaries = run_batch(
        runtime_root=args.runtime_root,
        summary_csv=args.summary_csv,
        series_csv=args.series_csv,
        summary_json=args.summary_json,
    )
    max_error = max(
        row.max_absolute_percent_error or 0.0 for row in figure_summaries
    )
    print(f"extracted {len(figure_summaries)} figures and {len(series_summaries)} series")
    print(f"maximum absolute percent error against table values: {max_error:.3f}%")
    print(args.summary_csv)
    print(args.series_csv)
    print(args.summary_json)


if __name__ == "__main__":
    main()
