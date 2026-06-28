"""Extract remaining MP11 harvest-scenario line charts.

This batch covers high-priority harvest/scenario charts that were not included
in the first accepted harvest-sensitivity tranche. It records raw deterministic
line extraction plus endpoint checks against visible table or narrative values
where those values are unambiguous.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"
SOURCE_URL = (
    "https://www.westernforest.com/wp-content/uploads/2026/06/"
    "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf"
)


@dataclass(frozen=True)
class SeriesConfig:
    """Series extraction settings for one harvest line."""

    series_name: str
    label: str
    rgb: tuple[int, int, int]
    tolerance: float
    expected_endpoint_m3_per_year: float | None
    expected_source: str


@dataclass(frozen=True)
class FigureConfig:
    """Manual plot bounds and expected values for one figure."""

    figure_id: str
    caption: str
    pdf_page: int
    image_path: str
    plot_left: int
    plot_top: int
    plot_right: int
    plot_bottom: int
    series: list[SeriesConfig]


@dataclass(frozen=True)
class HarvestPoint:
    """Recovered point from one harvest-scenario series."""

    figure_id: str
    series_name: str
    label: str
    year: float
    harvest_m3_per_year: float
    x_pixel: float
    y_pixel: float


@dataclass(frozen=True)
class HarvestSeriesSummary:
    """Compact summary of one recovered harvest series."""

    figure_id: str
    series_name: str
    label: str
    point_count: int
    year_min: float | None
    year_max: float | None
    harvest_min_m3_per_year: float | None
    harvest_max_m3_per_year: float | None
    harvest_mean_m3_per_year: float | None
    endpoint_m3_per_year: float | None
    expected_endpoint_m3_per_year: float | None
    endpoint_minus_expected_m3_per_year: float | None
    endpoint_abs_percent_error: float | None
    expected_source: str


@dataclass(frozen=True)
class HarvestFigureSummary:
    """Compact summary of one remaining harvest figure extraction."""

    figure_id: str
    caption: str
    pdf_page: int
    source_sha256: str
    source_url: str
    image_path: str
    rows_csv_path: str
    overlay_path: str
    series_count: int
    point_count: int
    min_series_point_count: int
    max_endpoint_abs_percent_error: float | None
    review_status: str
    downstream_use: str
    notes: str


BASE_CASE = SeriesConfig(
    series_name="base_case",
    label="MP11 Base Case",
    rgb=(76, 255, 0),
    tolerance=90,
    expected_endpoint_m3_per_year=1_061_600.0,
    expected_source="mp11_base_case_reference",
)

DARK = (29, 58, 42)
ORANGE = (220, 165, 0)


def _scenario(
    name: str,
    label: str,
    expected: float | None,
    source: str,
    rgb: tuple[int, int, int] = DARK,
) -> SeriesConfig:
    return SeriesConfig(
        series_name=name,
        label=label,
        rgb=rgb,
        tolerance=75 if rgb == DARK else 85,
        expected_endpoint_m3_per_year=expected,
        expected_source=source,
    )


def _configs(runtime_root: Path) -> list[FigureConfig]:
    proposal_dir = runtime_root / "crops" / "priority_high_proposals"
    return [
        FigureConfig(
            "Figure 21",
            "Harvest Levels Maintaining Current AAC",
            103,
            str(proposal_dir / "figure-21-proposal.png"),
            185,
            431,
            990,
            884,
            [
                BASE_CASE,
                _scenario(
                    "maintaining_current_aac",
                    "Maintaining Current AAC",
                    1_055_200.0,
                    "visible_table_final_70_300_year_row",
                ),
            ],
        ),
        FigureConfig(
            "Figure 22",
            "Harvest Levels Maximizing Short-Term Harvest",
            104,
            str(proposal_dir / "figure-22-proposal.png"),
            185,
            365,
            990,
            818,
            [
                BASE_CASE,
                _scenario(
                    "maximize_short_term",
                    "Maximum short-term",
                    1_095_500.0,
                    "visible_table_final_65_300_year_row",
                ),
            ],
        ),
        FigureConfig(
            "Figure 23",
            "Harvest Levels with Increased Natural Stand Yields",
            107,
            str(proposal_dir / "figure-23-proposal.png"),
            185,
            691,
            990,
            1144,
            [
                BASE_CASE,
                _scenario(
                    "increased_natural_stand_yields",
                    "Increased Natural Stand Yields",
                    1_075_300.0,
                    "narrative_difference_plus_13700",
                ),
            ],
        ),
        FigureConfig(
            "Figure 24",
            "Harvest Levels with Decreased Natural Stand Yields",
            109,
            str(proposal_dir / "figure-24-proposal.png"),
            185,
            601,
            990,
            1054,
            [
                BASE_CASE,
                _scenario(
                    "decreased_natural_stand_yields",
                    "Decreased Natural Stand Yields",
                    1_036_600.0,
                    "visible_table_single_row",
                ),
            ],
        ),
        FigureConfig(
            "Figure 25",
            "Harvest Levels with Increased Managed Stand Yields",
            110,
            str(proposal_dir / "figure-25-proposal.png"),
            185,
            813,
            990,
            1266,
            [
                BASE_CASE,
                _scenario(
                    "increased_managed_stand_yields",
                    "Increased Managed Stand Yields",
                    1_138_800.0,
                    "narrative_difference_plus_77200",
                ),
            ],
        ),
        FigureConfig(
            "Figure 26",
            "Harvest Levels with Decreased Managed Stand Yields",
            112,
            str(proposal_dir / "figure-26-proposal.png"),
            185,
            658,
            990,
            1111,
            [
                BASE_CASE,
                _scenario(
                    "decreased_managed_stand_yields",
                    "Decreased Managed Stand Yields",
                    970_900.0,
                    "narrative_difference_minus_90700",
                ),
            ],
        ),
        FigureConfig(
            "Figure 32",
            "Comparison of Harvest Scenarios: Base Case vs. Two Flows on ITI-Adjusted Volume with Reduced OAF1 Scenario",
            123,
            str(proposal_dir / "figure-32-proposal.png"),
            185,
            41,
            990,
            494,
            [
                BASE_CASE,
                _scenario(
                    "adjusted_iti_lidar_reduced_oaf1_even_flow",
                    "Adjusted ITI and LiDAR reduced OAF1 even flow",
                    1_150_300.0,
                    "visible_table_even_flow_endpoint",
                ),
                _scenario(
                    "adjusted_iti_lidar_reduced_oaf1_max_short_term",
                    "Adjusted ITI and LiDAR reduced OAF1 max short-term",
                    1_164_200.0,
                    "visible_table_max_short_term_final_row",
                    rgb=ORANGE,
                ),
            ],
        ),
        FigureConfig(
            "Figure 33",
            "Harvest Levels with No Genetic Gain",
            124,
            str(proposal_dir / "figure-33-proposal.png"),
            166,
            874,
            938,
            1308,
            [
                BASE_CASE,
                _scenario(
                    "no_genetic_gain",
                    "No Genetic Gain",
                    1_004_000.0,
                    "narrative_difference_minus_57600",
                ),
            ],
        ),
        FigureConfig(
            "Figure 34",
            "Harvest Levels with Full NSOG Order Targets",
            126,
            str(proposal_dir / "figure-34-proposal.png"),
            171,
            780,
            975,
            1233,
            [
                BASE_CASE,
                _scenario(
                    "full_nsog_order_targets",
                    "Full NSOG Order Targets",
                    1_049_400.0,
                    "narrative_difference_minus_12200",
                ),
            ],
        ),
        FigureConfig(
            "Figure 37",
            "Harvest Levels with Helicopter Operable Land Base Excluded",
            132,
            str(proposal_dir / "figure-37-proposal.png"),
            185,
            659,
            990,
            1112,
            [
                BASE_CASE,
                _scenario(
                    "helicopter_operable_land_base_excluded",
                    "Helicopter Operable Land Base Excluded",
                    1_021_900.0,
                    "visible_table_single_row",
                ),
            ],
        ),
        FigureConfig(
            "Figure 38",
            "Harvest Levels with 10% THLB Increases",
            133,
            str(proposal_dir / "figure-38-proposal.png"),
            185,
            749,
            990,
            1202,
            [
                BASE_CASE,
                _scenario(
                    "thlb_increased_by_10_percent",
                    "10% THLB Increases",
                    1_118_200.0,
                    "narrative_endpoint_1118200",
                ),
            ],
        ),
    ]


def _mask(plot: np.ndarray, series: SeriesConfig) -> np.ndarray:
    distance = np.linalg.norm(plot.astype(float) - np.array(series.rgb, dtype=float), axis=2)
    mask = distance <= series.tolerance
    # Exclude plot borders where possible.
    mask[:5, :] = False
    mask[-5:, :] = False
    mask[:, :5] = False
    mask[:, -5:] = False
    return mask


def _pixel_to_data(config: FigureConfig, x_pixel: float, y_pixel: float) -> tuple[float, float]:
    year = (x_pixel - config.plot_left) / (config.plot_right - config.plot_left) * 300.0
    harvest = (config.plot_bottom - y_pixel) / (config.plot_bottom - config.plot_top) * 1_400_000.0
    return year, harvest


def _sample_series(
    image: np.ndarray,
    config: FigureConfig,
    series: SeriesConfig,
    sample_every_px: int,
    half_window_px: int,
) -> list[HarvestPoint]:
    plot = image[
        config.plot_top : config.plot_bottom + 1,
        config.plot_left : config.plot_right + 1,
    ]
    mask = _mask(plot, series)
    # Legend swatches use the same series colours near the bottom of the plot.
    # All actual harvest lines in this MP11 batch sit above 600,000 m3/year, so
    # exclude lower pixels from sampling.
    min_harvest_for_series = 600_000.0
    max_y_local = int(
        round((1.0 - min_harvest_for_series / 1_400_000.0) * (config.plot_bottom - config.plot_top))
    )
    mask[max_y_local:, :] = False
    points: list[HarvestPoint] = []
    for x_local in range(8, plot.shape[1] - 8, sample_every_px):
        left = max(0, x_local - half_window_px)
        right = min(plot.shape[1], x_local + half_window_px + 1)
        y_hits = np.where(mask[:, left:right])[0]
        if not len(y_hits):
            continue
        y_local = float(np.median(y_hits))
        x_pixel = float(config.plot_left + x_local)
        y_pixel = float(config.plot_top + y_local)
        year, harvest = _pixel_to_data(config, x_pixel, y_pixel)
        points.append(
            HarvestPoint(
                figure_id=config.figure_id,
                series_name=series.series_name,
                label=series.label,
                year=year,
                harvest_m3_per_year=harvest,
                x_pixel=x_pixel,
                y_pixel=y_pixel,
            )
        )
    return points


def _endpoint(points: list[HarvestPoint]) -> float | None:
    if not points:
        return None
    tail = sorted(points, key=lambda point: point.year)[-max(3, len(points) // 10) :]
    return float(np.median([point.harvest_m3_per_year for point in tail]))


def _series_summary(
    figure_id: str,
    points: list[HarvestPoint],
    series: SeriesConfig,
) -> HarvestSeriesSummary:
    years = [point.year for point in points]
    values = [point.harvest_m3_per_year for point in points]
    endpoint = _endpoint(points)
    expected = series.expected_endpoint_m3_per_year
    delta = None if endpoint is None or expected is None else endpoint - expected
    pct = None if delta is None or expected == 0 else abs(delta) / expected * 100.0
    return HarvestSeriesSummary(
        figure_id=figure_id,
        series_name=series.series_name,
        label=series.label,
        point_count=len(points),
        year_min=min(years) if years else None,
        year_max=max(years) if years else None,
        harvest_min_m3_per_year=min(values) if values else None,
        harvest_max_m3_per_year=max(values) if values else None,
        harvest_mean_m3_per_year=sum(values) / len(values) if values else None,
        endpoint_m3_per_year=endpoint,
        expected_endpoint_m3_per_year=expected,
        endpoint_minus_expected_m3_per_year=delta,
        endpoint_abs_percent_error=pct,
        expected_source=series.expected_source,
    )


def _write_csv(path: Path, rows: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _draw_overlay(image: Image.Image, config: FigureConfig, points: list[HarvestPoint], output_path: Path) -> None:
    overlay = image.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    draw.rectangle(
        [config.plot_left, config.plot_top, config.plot_right, config.plot_bottom],
        outline=(220, 40, 40),
        width=2,
    )
    colours = {
        "base_case": (80, 235, 15),
        "adjusted_iti_lidar_reduced_oaf1_max_short_term": (220, 165, 0),
    }
    for point in points:
        colour = colours.get(point.series_name, (20, 65, 45))
        draw.ellipse(
            [point.x_pixel - 2, point.y_pixel - 2, point.x_pixel + 2, point.y_pixel + 2],
            fill=colour,
            outline=(255, 255, 255),
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(output_path)


def run_batch(
    runtime_root: Path,
    summary_csv: Path,
    series_summary_csv: Path,
    rows_csv: Path,
    summary_json: Path,
    sample_every_px: int,
    half_window_px: int,
) -> tuple[list[HarvestFigureSummary], list[HarvestSeriesSummary], list[HarvestPoint]]:
    table_dir = runtime_root / "recovered" / "remaining_harvest_batch"
    overlay_dir = runtime_root / "overlays" / "remaining_harvest_batch"
    table_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    figure_summaries: list[HarvestFigureSummary] = []
    series_summaries: list[HarvestSeriesSummary] = []
    all_points: list[HarvestPoint] = []
    for config in _configs(runtime_root):
        image_path = Path(config.image_path)
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)
        figure_points: list[HarvestPoint] = []
        figure_series_summaries: list[HarvestSeriesSummary] = []
        for series in config.series:
            points = _sample_series(
                image_array,
                config,
                series,
                sample_every_px=sample_every_px,
                half_window_px=half_window_px,
            )
            figure_points.extend(points)
            summary = _series_summary(config.figure_id, points, series)
            figure_series_summaries.append(summary)
            series_summaries.append(summary)
        figure_slug = config.figure_id.lower().replace(" ", "-")
        per_figure_csv = table_dir / f"{figure_slug}-remaining-harvest-points.csv"
        overlay_path = overlay_dir / f"{figure_slug}-overlay.png"
        _write_csv(per_figure_csv, figure_points)
        _draw_overlay(image, config, figure_points, overlay_path)
        counts = [summary.point_count for summary in figure_series_summaries]
        endpoint_errors = [
            summary.endpoint_abs_percent_error
            for summary in figure_series_summaries
            if summary.endpoint_abs_percent_error is not None
        ]
        figure_summaries.append(
            HarvestFigureSummary(
                figure_id=config.figure_id,
                caption=config.caption,
                pdf_page=config.pdf_page,
                source_sha256=SOURCE_SHA256,
                source_url=SOURCE_URL,
                image_path=image_path.as_posix(),
                rows_csv_path=per_figure_csv.as_posix(),
                overlay_path=overlay_path.as_posix(),
                series_count=len(config.series),
                point_count=len(figure_points),
                min_series_point_count=min(counts) if counts else 0,
                max_endpoint_abs_percent_error=max(endpoint_errors) if endpoint_errors else None,
                review_status="raw_extraction",
                downstream_use="needs_p7_5_review",
                notes=(
                    "Raw deterministic extraction for remaining harvest scenario charts. "
                    "Endpoint checks use visible table or narrative values where available; "
                    "stepped and multi-flow figures require review before promotion."
                ),
            )
        )
        all_points.extend(figure_points)

    _write_csv(summary_csv, figure_summaries)
    _write_csv(series_summary_csv, series_summaries)
    _write_csv(rows_csv, all_points)
    payload = {
        "summary_csv": summary_csv.as_posix(),
        "series_summary_csv": series_summary_csv.as_posix(),
        "rows_csv": rows_csv.as_posix(),
        "figure_count": len(figure_summaries),
        "series_count": len(series_summaries),
        "point_count": len(all_points),
        "figures": [asdict(summary) for summary in figure_summaries],
    }
    summary_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return figure_summaries, series_summaries, all_points


def _write_markdown(
    summary_md: Path,
    figure_summaries: list[HarvestFigureSummary],
    series_summaries: list[HarvestSeriesSummary],
) -> None:
    endpoint_lines = []
    for summary in series_summaries:
        if summary.expected_endpoint_m3_per_year is None:
            expected = "NA"
            error = "NA"
        else:
            expected = f"{summary.expected_endpoint_m3_per_year:,.0f}"
            error = (
                "NA"
                if summary.endpoint_abs_percent_error is None
                else f"{summary.endpoint_abs_percent_error:.2f}%"
            )
        endpoint = "NA" if summary.endpoint_m3_per_year is None else f"{summary.endpoint_m3_per_year:,.0f}"
        endpoint_lines.append(
            f"- `{summary.figure_id}` `{summary.label}` endpoint `{endpoint}`; "
            f"expected `{expected}`; absolute error `{error}`"
        )
    max_error = max(
        (
            summary.max_endpoint_abs_percent_error
            for summary in figure_summaries
            if summary.max_endpoint_abs_percent_error is not None
        ),
        default=None,
    )
    lines = [
        "# TFL 6 MP11 Remaining Harvest Scenario Extraction Summary",
        "",
        "## Purpose",
        "",
        "This note records the raw extraction batch for high-priority MP11",
        "harvest/scenario line charts that were not part of the first accepted",
        "harvest-sensitivity tranche.",
        "",
        "The batch extracts plotted lines and records endpoint checks against",
        "visible table or narrative values where those values are unambiguous.",
        "It remains raw until P7.5 overlay and value review.",
        "",
        "## Outputs",
        "",
        "- `planning/tfl6_mp11_remaining_harvest_extraction_summary.csv`",
        "- `planning/tfl6_mp11_remaining_harvest_extraction_summary.json`",
        "- `planning/tfl6_mp11_remaining_harvest_series_summary.csv`",
        "- `planning/tfl6_mp11_remaining_harvest_points.csv`",
        "",
        "Ignored runtime detail files are under:",
        "",
        "```text",
        "runtime/document_ingestion/tfl6-mp11-full-figures/recovered/remaining_harvest_batch/",
        "runtime/document_ingestion/tfl6-mp11-full-figures/overlays/remaining_harvest_batch/",
        "```",
        "",
        "## Current Status",
        "",
        f"- Figures extracted: `{len(figure_summaries)}`",
        f"- Series extracted: `{len(series_summaries)}`",
        f"- Recovered points: `{sum(row.point_count for row in figure_summaries)}`",
        "- Review status: `raw_extraction`",
        "- Downstream use: `needs_p7_5_review`",
        "- Model-input status: not accepted for model input",
        f"- Maximum endpoint absolute percent error: `{max_error:.2f}%`" if max_error is not None else "- Maximum endpoint absolute percent error: `NA`",
        "",
        "## Endpoint Snapshot",
        "",
        *endpoint_lines,
        "",
        "## Next Step",
        "",
        "P7.5 should inspect overlays and endpoint residuals. Simple flat-line",
        "figures with clean endpoint checks may be eligible for",
        "`accepted_for_comparison`; stepped and multi-flow figures may need",
        "planning-only handling unless the table rows are reviewed in more detail.",
        "",
    ]
    summary_md.write_text("\n".join(lines), encoding="utf-8")


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
        default=Path("planning/tfl6_mp11_remaining_harvest_extraction_summary.csv"),
    )
    parser.add_argument(
        "--series-summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_series_summary.csv"),
    )
    parser.add_argument(
        "--rows-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_points.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_extraction_summary.json"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_extraction_summary.md"),
    )
    parser.add_argument("--sample-every-px", type=int, default=4)
    parser.add_argument("--half-window-px", type=int, default=1)
    args = parser.parse_args()

    figure_summaries, series_summaries, points = run_batch(
        runtime_root=args.runtime_root,
        summary_csv=args.summary_csv,
        series_summary_csv=args.series_summary_csv,
        rows_csv=args.rows_csv,
        summary_json=args.summary_json,
        sample_every_px=args.sample_every_px,
        half_window_px=args.half_window_px,
    )
    _write_markdown(args.summary_md, figure_summaries, series_summaries)
    print(f"extracted {len(figure_summaries)} remaining harvest figures")
    print(f"wrote {len(series_summaries)} series summaries")
    print(f"wrote {len(points)} points")
    print(args.summary_csv)
    print(args.series_summary_csv)
    print(args.rows_csv)
    print(args.summary_json)
    print(args.summary_md)


if __name__ == "__main__":
    main()
