"""Extract MP11 old-seral landscape-unit projection charts.

This raw batch covers the old-seral LU line charts from the MP11 appendix.
The extractor is deliberately simple and auditable: it samples the uppermost
matching coloured line within each plot panel, which targets the projected
actual series and avoids the lower dashed/dotted target lines in this chart
family. Detailed rows and overlays remain under ignored runtime paths.
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
    """Colour and label configuration for one old-seral series."""

    series_name: str
    label: str
    rgb: tuple[int, int, int]
    tolerance: float


@dataclass(frozen=True)
class FigureConfig:
    """Manual plot bounds and series configuration for one figure."""

    figure_id: str
    caption: str
    landscape_unit: str
    scenario: str
    pdf_page: int
    image_path: str
    plot_left: int
    plot_top: int
    plot_right: int
    plot_bottom: int
    series: list[SeriesConfig]


@dataclass(frozen=True)
class OldSeralPoint:
    """Recovered point from one old-seral projected series."""

    figure_id: str
    landscape_unit: str
    scenario: str
    series_name: str
    label: str
    year: float
    old_seral_percent: float
    x_pixel: float
    y_pixel: float


@dataclass(frozen=True)
class OldSeralSeriesSummary:
    """Compact summary of one recovered old-seral series."""

    figure_id: str
    landscape_unit: str
    scenario: str
    series_name: str
    label: str
    point_count: int
    year_min: float | None
    year_max: float | None
    percent_min: float | None
    percent_max: float | None
    percent_mean: float | None
    final_percent: float | None


@dataclass(frozen=True)
class OldSeralFigureSummary:
    """Compact summary of one old-seral figure extraction."""

    figure_id: str
    caption: str
    landscape_unit: str
    scenario: str
    pdf_page: int
    source_sha256: str
    source_url: str
    image_path: str
    rows_csv_path: str
    overlay_path: str
    series_count: int
    point_count: int
    min_series_point_count: int
    max_series_point_count: int
    review_status: str
    downstream_use: str
    notes: str


def _series(include_tan: bool = True) -> list[SeriesConfig]:
    series: list[SeriesConfig] = []
    if include_tan:
        series.append(SeriesConfig("cwhvm1_in_gmz_or_cwhvh1", "CWHvm1 in GMZ/CWHvh1", (198, 184, 160), 55))
    series.extend(
        [
            SeriesConfig("cwhvm1_other", "Other CWHvm1/CWHvm1", (112, 18, 32), 55),
            SeriesConfig("cwhvm2", "CWHvm2", (65, 255, 0), 80),
            SeriesConfig("mhmm1", "MHmm1", (0, 0, 0), 70),
        ]
    )
    return series


def _configs(runtime_root: Path) -> list[FigureConfig]:
    proposal_dir = runtime_root / "crops" / "priority_high_proposals"
    return [
        FigureConfig(
            "Figure 16",
            "Projection of Old Seral Forest Proportions for Holberg LU",
            "Holberg",
            "base_case",
            98,
            str(proposal_dir / "figure-16-proposal.png"),
            139,
            63,
            776,
            490,
            _series(include_tan=True),
        ),
        FigureConfig(
            "Figure 17",
            "Projection of Old Seral Forest Proportions for Keogh LU",
            "Keogh",
            "base_case",
            99,
            str(proposal_dir / "figure-17-proposal.png"),
            139,
            63,
            691,
            490,
            _series(include_tan=True),
        ),
        FigureConfig(
            "Figure 18",
            "Projection of Old Seral Forest Proportions for Mahatta LU",
            "Mahatta",
            "base_case",
            99,
            str(proposal_dir / "figure-18-proposal.png"),
            139,
            793,
            776,
            1220,
            _series(include_tan=True),
        ),
        FigureConfig(
            "Figure 19",
            "Projection of Old Seral Forest Proportions for Neroutsos LU",
            "Neroutsos",
            "base_case",
            100,
            str(proposal_dir / "figure-19-proposal.png"),
            139,
            64,
            776,
            490,
            _series(include_tan=False),
        ),
        FigureConfig(
            "Figure 53",
            "AAC Recommendation Projection of Old Seral Forest Proportions for Holberg LU",
            "Holberg",
            "aac_recommendation",
            156,
            str(proposal_dir / "figure-53-proposal.png"),
            124,
            63,
            762,
            490,
            _series(include_tan=True),
        ),
        FigureConfig(
            "Figure 54",
            "AAC Recommendation Projection of Old Seral Forest Proportions for Keogh LU",
            "Keogh",
            "aac_recommendation",
            156,
            str(proposal_dir / "figure-53-proposal.png"),
            124,
            694,
            678,
            1120,
            _series(include_tan=True),
        ),
        FigureConfig(
            "Figure 55",
            "AAC Recommendation Projection of Old Seral Forest Proportions for Mahatta LU",
            "Mahatta",
            "aac_recommendation",
            157,
            str(proposal_dir / "figure-55-proposal.png"),
            124,
            63,
            762,
            490,
            _series(include_tan=True),
        ),
        FigureConfig(
            "Figure 56",
            "AAC Recommendation Projection of Old Seral Forest Proportions for Neroutsos LU",
            "Neroutsos",
            "aac_recommendation",
            157,
            str(proposal_dir / "figure-55-proposal.png"),
            124,
            694,
            762,
            1120,
            _series(include_tan=False),
        ),
    ]


def _mask(plot: np.ndarray, series: SeriesConfig) -> np.ndarray:
    distance = np.linalg.norm(plot.astype(float) - np.array(series.rgb, dtype=float), axis=2)
    mask = distance <= series.tolerance
    if series.series_name == "cwhvm1_in_gmz_or_cwhvh1":
        # The tan series is close to gray gridlines in RGB distance. Require
        # the warm channel ordering visible in the plotted tan line.
        red = plot[:, :, 0].astype(int)
        green = plot[:, :, 1].astype(int)
        blue = plot[:, :, 2].astype(int)
        mask &= (red > green + 4) & (green > blue + 8)
    return mask


def _pixel_to_data(config: FigureConfig, x_pixel: float, y_pixel: float) -> tuple[float, float]:
    year = (x_pixel - config.plot_left) / (config.plot_right - config.plot_left) * 300.0
    percent = (config.plot_bottom - y_pixel) / (config.plot_bottom - config.plot_top) * 100.0
    return year, percent


def _sample_series(
    image: np.ndarray,
    config: FigureConfig,
    series: SeriesConfig,
    sample_every_px: int,
    column_half_window_px: int,
) -> list[OldSeralPoint]:
    plot = image[
        config.plot_top : config.plot_bottom + 1,
        config.plot_left : config.plot_right + 1,
    ]
    mask = _mask(plot, series)
    # Remove axes and plot borders. The actual series never sit directly on
    # these borders in this chart family, but the black axes would otherwise
    # contaminate the MHmm1 series.
    mask[:8, :] = False
    mask[-5:, :] = False
    mask[:, :5] = False
    mask[:, -5:] = False

    points: list[OldSeralPoint] = []
    for x_local in range(8, plot.shape[1] - 8, sample_every_px):
        left = max(0, x_local - column_half_window_px)
        right = min(plot.shape[1], x_local + column_half_window_px + 1)
        y_hits = np.where(mask[:, left:right])[0]
        if not len(y_hits):
            continue
        # Old-seral target lines are lower than the actual projected lines.
        # Taking the uppermost coloured pixel therefore selects the actual
        # projected series in this figure family.
        y_local = float(np.min(y_hits))
        x_pixel = float(config.plot_left + x_local)
        y_pixel = float(config.plot_top + y_local)
        year, percent = _pixel_to_data(config, x_pixel, y_pixel)
        points.append(
            OldSeralPoint(
                figure_id=config.figure_id,
                landscape_unit=config.landscape_unit,
                scenario=config.scenario,
                series_name=series.series_name,
                label=series.label,
                year=year,
                old_seral_percent=percent,
                x_pixel=x_pixel,
                y_pixel=y_pixel,
            )
        )
    return points


def _series_summary(points: list[OldSeralPoint], config: FigureConfig, series: SeriesConfig) -> OldSeralSeriesSummary:
    years = [point.year for point in points]
    values = [point.old_seral_percent for point in points]
    final_percent = values[-1] if values else None
    return OldSeralSeriesSummary(
        figure_id=config.figure_id,
        landscape_unit=config.landscape_unit,
        scenario=config.scenario,
        series_name=series.series_name,
        label=series.label,
        point_count=len(points),
        year_min=min(years) if years else None,
        year_max=max(years) if years else None,
        percent_min=min(values) if values else None,
        percent_max=max(values) if values else None,
        percent_mean=sum(values) / len(values) if values else None,
        final_percent=final_percent,
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


def _draw_overlay(image: Image.Image, config: FigureConfig, points: list[OldSeralPoint], output_path: Path) -> None:
    overlay = image.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    draw.rectangle(
        [config.plot_left, config.plot_top, config.plot_right, config.plot_bottom],
        outline=(220, 40, 40),
        width=2,
    )
    colours = {
        "cwhvm1_in_gmz_or_cwhvh1": (185, 155, 110),
        "cwhvm1_other": (140, 25, 35),
        "cwhvm2": (60, 230, 20),
        "mhmm1": (0, 0, 0),
    }
    for point in points:
        colour = colours.get(point.series_name, (0, 80, 180))
        x = point.x_pixel
        y = point.y_pixel
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=colour, outline=(255, 255, 255))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(output_path)


def run_batch(
    runtime_root: Path,
    summary_csv: Path,
    series_summary_csv: Path,
    rows_csv: Path,
    summary_json: Path,
    sample_every_px: int,
    column_half_window_px: int,
) -> tuple[list[OldSeralFigureSummary], list[OldSeralSeriesSummary], list[OldSeralPoint]]:
    table_dir = runtime_root / "recovered" / "old_seral_batch"
    overlay_dir = runtime_root / "overlays" / "old_seral_batch"
    table_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    figure_summaries: list[OldSeralFigureSummary] = []
    series_summaries: list[OldSeralSeriesSummary] = []
    all_points: list[OldSeralPoint] = []
    for config in _configs(runtime_root):
        image_path = Path(config.image_path)
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)
        figure_points: list[OldSeralPoint] = []
        for series in config.series:
            points = _sample_series(
                image_array,
                config,
                series,
                sample_every_px=sample_every_px,
                column_half_window_px=column_half_window_px,
            )
            figure_points.extend(points)
            series_summaries.append(_series_summary(points, config, series))
        figure_slug = config.figure_id.lower().replace(" ", "-")
        per_figure_csv = table_dir / f"{figure_slug}-old-seral-points.csv"
        overlay_path = overlay_dir / f"{figure_slug}-overlay.png"
        _write_csv(per_figure_csv, figure_points)
        _draw_overlay(image, config, figure_points, overlay_path)
        counts = [sum(point.series_name == series.series_name for point in figure_points) for series in config.series]
        figure_summaries.append(
            OldSeralFigureSummary(
                figure_id=config.figure_id,
                caption=config.caption,
                landscape_unit=config.landscape_unit,
                scenario=config.scenario,
                pdf_page=config.pdf_page,
                source_sha256=SOURCE_SHA256,
                source_url=SOURCE_URL,
                image_path=image_path.as_posix(),
                rows_csv_path=per_figure_csv.as_posix(),
                overlay_path=overlay_path.as_posix(),
                series_count=len(config.series),
                point_count=len(figure_points),
                min_series_point_count=min(counts) if counts else 0,
                max_series_point_count=max(counts) if counts else 0,
                review_status="raw_extraction",
                downstream_use="needs_p7_5_review",
                notes=(
                    "Raw deterministic old-seral line extraction. The uppermost matching "
                    "coloured pixel is sampled to prefer projected actual series over lower "
                    "target lines. Requires overlay review before downstream use."
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
    figure_summaries: list[OldSeralFigureSummary],
    series_summaries: list[OldSeralSeriesSummary],
) -> None:
    final_lines = [
        f"- `{row.figure_id}` `{row.label}` final: "
        f"`{row.final_percent:.1f}%`" if row.final_percent is not None else f"- `{row.figure_id}` `{row.label}` final: `NA`"
        for row in series_summaries
    ]
    lines = [
        "# TFL 6 MP11 Old-Seral Extraction Summary",
        "",
        "## Purpose",
        "",
        "This note records the raw extraction batch for MP11 old-seral",
        "landscape-unit projection charts. The batch covers base-case Figures",
        "`16`-`19` and AAC recommendation Figures `53`-`56`.",
        "",
        "The extraction is deterministic and colour-based, but the outputs remain",
        "raw until overlay review confirms that projected actual series were",
        "sampled instead of target lines or axes.",
        "",
        "## Outputs",
        "",
        "- `planning/tfl6_mp11_old_seral_extraction_summary.csv`",
        "- `planning/tfl6_mp11_old_seral_extraction_summary.json`",
        "- `planning/tfl6_mp11_old_seral_series_summary.csv`",
        "- `planning/tfl6_mp11_old_seral_points.csv`",
        "",
        "Ignored runtime detail files are under:",
        "",
        "```text",
        "runtime/document_ingestion/tfl6-mp11-full-figures/recovered/old_seral_batch/",
        "runtime/document_ingestion/tfl6-mp11-full-figures/overlays/old_seral_batch/",
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
        "",
        "## Final-Point Snapshot",
        "",
        *final_lines,
        "",
        "## Next Step",
        "",
        "P7.5 should inspect per-figure overlays before promoting these outputs.",
        "Given the lack of adjacent source tables, the expected promotion ceiling is",
        "`reviewed_for_planning` unless a maintainer supplies a stronger validation",
        "basis.",
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
        default=Path("planning/tfl6_mp11_old_seral_extraction_summary.csv"),
    )
    parser.add_argument(
        "--series-summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_series_summary.csv"),
    )
    parser.add_argument(
        "--rows-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_points.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_extraction_summary.json"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_extraction_summary.md"),
    )
    parser.add_argument("--sample-every-px", type=int, default=5)
    parser.add_argument("--column-half-window-px", type=int, default=1)
    args = parser.parse_args()

    figure_summaries, series_summaries, points = run_batch(
        runtime_root=args.runtime_root,
        summary_csv=args.summary_csv,
        series_summary_csv=args.series_summary_csv,
        rows_csv=args.rows_csv,
        summary_json=args.summary_json,
        sample_every_px=args.sample_every_px,
        column_half_window_px=args.column_half_window_px,
    )
    _write_markdown(args.summary_md, figure_summaries, series_summaries)
    print(f"extracted {len(figure_summaries)} old-seral figures")
    print(f"wrote {len(series_summaries)} series summaries")
    print(f"wrote {len(points)} points")
    print(args.summary_csv)
    print(args.series_summary_csv)
    print(args.rows_csv)
    print(args.summary_json)
    print(args.summary_md)


if __name__ == "__main__":
    main()
