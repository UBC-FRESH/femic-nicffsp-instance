"""Extract MP11 timber-supply impact waterfall charts.

This script handles the two MP11 waterfall-style figures that summarize the
movement from MP10/current AAC assumptions to the MP11 base case and AAC
recommendation. It keeps detailed rows and overlays under ignored runtime
paths; tracked planning outputs are compact summaries only.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"
SOURCE_URL = (
    "https://www.westernforest.com/wp-content/uploads/2026/06/"
    "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf"
)


@dataclass(frozen=True)
class ImpactStepConfig:
    """One labelled component in a waterfall chart."""

    label: str
    kind: str
    printed_value_m3_per_year: float
    component_order: int


@dataclass(frozen=True)
class ImpactFigureConfig:
    """Manual extraction configuration for one impact chart."""

    figure_id: str
    caption: str
    pdf_page: int
    image_path: str
    plot_bottom_y: float
    calibration_anchor_component_order: int
    calibration_anchor_value_m3_per_year: float
    axis_bottom_value_m3_per_year: float
    steps: list[ImpactStepConfig]


@dataclass(frozen=True)
class ImpactStepRow:
    """Recovered label and geometry record for one waterfall component."""

    figure_id: str
    step_order: int
    step_label: str
    step_kind: str
    printed_value_m3_per_year: float
    component_left_px: int
    component_top_px: int
    component_right_px: int
    component_bottom_px: int
    geometry_high_m3_per_year: float
    geometry_low_m3_per_year: float
    geometry_delta_m3_per_year: float
    geometry_value_for_review_m3_per_year: float
    abs_geometry_minus_printed_m3_per_year: float
    abs_geometry_minus_printed_percent: float


@dataclass(frozen=True)
class ImpactFigureSummary:
    """Compact summary of one waterfall extraction."""

    figure_id: str
    caption: str
    pdf_page: int
    source_sha256: str
    source_url: str
    image_path: str
    rows_csv_path: str
    overlay_path: str
    step_count: int
    accepted_printed_total_m3_per_year: float
    max_abs_geometry_minus_printed_m3_per_year: float
    max_abs_geometry_minus_printed_percent: float
    arithmetic_residual_m3_per_year: float
    review_status: str
    downstream_use: str
    notes: str


def _configs(runtime_root: Path) -> list[ImpactFigureConfig]:
    proposal_dir = runtime_root / "crops" / "priority_high_proposals"
    return [
        ImpactFigureConfig(
            figure_id="Figure 20",
            caption="Timber Supply Impacts since MP #10 to Base Case",
            pdf_page=101,
            image_path=str(proposal_dir / "figure-20-proposal.png"),
            plot_bottom_y=656.0,
            calibration_anchor_component_order=1,
            calibration_anchor_value_m3_per_year=1_362_000.0,
            axis_bottom_value_m3_per_year=800_000.0,
            steps=[
                ImpactStepConfig("Current AAC", "absolute", 1_362_000.0, 1),
                ImpactStepConfig("MP 10 Forecast Decline", "delta", -95_400.0, 2),
                ImpactStepConfig("THLB and modelling changes", "delta", -118_900.0, 3),
                ImpactStepConfig("MP 11 max short-term flow", "absolute", 1_147_700.0, 4),
                ImpactStepConfig("Apply even-flow harvest", "delta", -86_100.0, 5),
                ImpactStepConfig("MP 11 Base Case", "absolute", 1_061_600.0, 6),
            ],
        ),
        ImpactFigureConfig(
            figure_id="Figure 57",
            caption="Updated Timber Supply Impacts Since MP #10",
            pdf_page=158,
            image_path=str(proposal_dir / "figure-57-proposal.png"),
            plot_bottom_y=573.0,
            calibration_anchor_component_order=1,
            calibration_anchor_value_m3_per_year=1_362_000.0,
            axis_bottom_value_m3_per_year=800_000.0,
            steps=[
                ImpactStepConfig("Current AAC", "absolute", 1_362_000.0, 1),
                ImpactStepConfig("MP 10 Forecast Decline", "delta", -95_400.0, 2),
                ImpactStepConfig("THLB and modelling changes", "delta", -118_900.0, 3),
                ImpactStepConfig("MP 11 max short-term flow", "absolute", 1_147_700.0, 4),
                ImpactStepConfig("Apply even-flow harvest", "delta", -86_100.0, 5),
                ImpactStepConfig("MP 11 Base Case", "absolute", 1_061_600.0, 6),
                ImpactStepConfig("LiDAR yield adjustments even-flow", "delta", 88_700.0, 7),
                ImpactStepConfig("LiDAR MHA adjustment max short-term flow", "delta", 102_400.0, 8),
                ImpactStepConfig("MP 11 AAC Recommendation", "absolute", 1_252_700.0, 9),
            ],
        ),
    ]


def _component_boxes(image: np.ndarray) -> list[tuple[int, int, int, int]]:
    rgb = image.astype(np.int16)
    channel_range = rgb.max(axis=2) - rgb.min(axis=2)
    brightness = rgb.sum(axis=2)
    y_indices = np.indices(channel_range.shape)[0]
    mask = (channel_range > 25) & (brightness < 720) & (y_indices < image.shape[0] - 80)
    labels_count, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    boxes: list[tuple[int, int, int, int]] = []
    for label in range(1, labels_count):
        left, top, width, height, area = stats[label]
        if area < 3_000:
            continue
        boxes.append((int(left), int(top), int(left + width - 1), int(top + height - 1)))
    return sorted(boxes, key=lambda box: box[0])


def _calibration_scale(
    boxes: list[tuple[int, int, int, int]],
    config: ImpactFigureConfig,
) -> float:
    anchor_box = boxes[config.calibration_anchor_component_order - 1]
    anchor_top = anchor_box[1]
    return (
        config.calibration_anchor_value_m3_per_year - config.axis_bottom_value_m3_per_year
    ) / (config.plot_bottom_y - anchor_top)


def _value_at_y(config: ImpactFigureConfig, scale: float, y: float) -> float:
    return config.axis_bottom_value_m3_per_year + (config.plot_bottom_y - y) * scale


def _step_rows(config: ImpactFigureConfig, boxes: list[tuple[int, int, int, int]]) -> list[ImpactStepRow]:
    scale = _calibration_scale(boxes, config)
    rows: list[ImpactStepRow] = []
    for step in config.steps:
        left, top, right, bottom = boxes[step.component_order - 1]
        high = _value_at_y(config, scale, float(top))
        low = _value_at_y(config, scale, float(bottom))
        geometry_delta = high - low
        if step.kind == "delta":
            sign = 1.0 if step.printed_value_m3_per_year >= 0 else -1.0
            geometry_for_review = sign * abs(geometry_delta)
        else:
            geometry_for_review = high
        residual = geometry_for_review - step.printed_value_m3_per_year
        residual_percent = (
            abs(residual) / abs(step.printed_value_m3_per_year) * 100.0
            if step.printed_value_m3_per_year
            else 0.0
        )
        rows.append(
            ImpactStepRow(
                figure_id=config.figure_id,
                step_order=step.component_order,
                step_label=step.label,
                step_kind=step.kind,
                printed_value_m3_per_year=step.printed_value_m3_per_year,
                component_left_px=left,
                component_top_px=top,
                component_right_px=right,
                component_bottom_px=bottom,
                geometry_high_m3_per_year=high,
                geometry_low_m3_per_year=low,
                geometry_delta_m3_per_year=geometry_delta,
                geometry_value_for_review_m3_per_year=geometry_for_review,
                abs_geometry_minus_printed_m3_per_year=abs(residual),
                abs_geometry_minus_printed_percent=residual_percent,
            )
        )
    return rows


def _arithmetic_residual(rows: list[ImpactStepRow]) -> float:
    if not rows:
        return 0.0
    running = rows[0].printed_value_m3_per_year
    for row in rows[1:-1]:
        if row.step_kind == "delta":
            running += row.printed_value_m3_per_year
        else:
            running = row.printed_value_m3_per_year
    return running - rows[-1].printed_value_m3_per_year


def _write_csv(path: Path, rows: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _draw_overlay(image: Image.Image, rows: list[ImpactStepRow], output_path: Path) -> None:
    overlay = image.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    for row in rows:
        colour = (25, 110, 40) if row.step_kind == "absolute" else (210, 65, 170)
        draw.rectangle(
            [
                row.component_left_px,
                row.component_top_px,
                row.component_right_px,
                row.component_bottom_px,
            ],
            outline=colour,
            width=3,
        )
        draw.text(
            (row.component_left_px, max(0, row.component_top_px - 16)),
            str(row.step_order),
            fill=(0, 0, 0),
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(output_path)


def run_batch(
    runtime_root: Path,
    summary_csv: Path,
    rows_csv: Path,
    summary_json: Path,
) -> tuple[list[ImpactFigureSummary], list[ImpactStepRow]]:
    table_dir = runtime_root / "recovered" / "impact_batch"
    overlay_dir = runtime_root / "overlays" / "impact_batch"
    table_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)

    summaries: list[ImpactFigureSummary] = []
    all_rows: list[ImpactStepRow] = []
    for config in _configs(runtime_root):
        image_path = Path(config.image_path)
        image = Image.open(image_path).convert("RGB")
        boxes = _component_boxes(np.array(image))
        if len(boxes) != len(config.steps):
            raise RuntimeError(
                f"{config.figure_id}: expected {len(config.steps)} components, found {len(boxes)}"
            )
        rows = _step_rows(config, boxes)
        figure_slug = config.figure_id.lower().replace(" ", "-")
        per_figure_csv = table_dir / f"{figure_slug}-impact-steps.csv"
        overlay_path = overlay_dir / f"{figure_slug}-overlay.png"
        _write_csv(per_figure_csv, rows)
        _draw_overlay(image, rows, overlay_path)
        max_residual_m3 = max(row.abs_geometry_minus_printed_m3_per_year for row in rows)
        max_residual_percent = max(row.abs_geometry_minus_printed_percent for row in rows)
        arithmetic_residual = _arithmetic_residual(rows)
        summaries.append(
            ImpactFigureSummary(
                figure_id=config.figure_id,
                caption=config.caption,
                pdf_page=config.pdf_page,
                source_sha256=SOURCE_SHA256,
                source_url=SOURCE_URL,
                image_path=image_path.as_posix(),
                rows_csv_path=per_figure_csv.as_posix(),
                overlay_path=overlay_path.as_posix(),
                step_count=len(rows),
                accepted_printed_total_m3_per_year=rows[-1].printed_value_m3_per_year,
                max_abs_geometry_minus_printed_m3_per_year=max_residual_m3,
                max_abs_geometry_minus_printed_percent=max_residual_percent,
                arithmetic_residual_m3_per_year=arithmetic_residual,
                review_status="raw_extraction",
                downstream_use="needs_p7_5_review",
                notes=(
                    "Waterfall step values are transcribed from printed chart labels and "
                    "checked against deterministic coloured-component geometry. Detailed "
                    "step rows and overlays remain under ignored runtime paths."
                ),
            )
        )
        all_rows.extend(rows)

    _write_csv(summary_csv, summaries)
    _write_csv(rows_csv, all_rows)
    payload = {
        "summary_csv": summary_csv.as_posix(),
        "rows_csv": rows_csv.as_posix(),
        "figure_count": len(summaries),
        "row_count": len(all_rows),
        "figures": [asdict(summary) for summary in summaries],
    }
    summary_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return summaries, all_rows


def _write_markdown(summary_md: Path, summaries: list[ImpactFigureSummary]) -> None:
    accepted_totals = ", ".join(
        f"{summary.figure_id}: {summary.accepted_printed_total_m3_per_year:,.0f}"
        for summary in summaries
    )
    max_residual = max(summary.max_abs_geometry_minus_printed_m3_per_year for summary in summaries)
    lines = [
        "# TFL 6 MP11 Timber-Supply Impact Extraction Summary",
        "",
        "## Purpose",
        "",
        "This note records the raw extraction batch for the MP11 waterfall-style",
        "timber-supply impact charts. The batch covers Figures `20` and `57`,",
        "which summarize the transition from MP10/current AAC assumptions to the",
        "MP11 base case and AAC recommendation.",
        "",
        "The extracted values are printed chart labels checked against",
        "deterministic coloured-component geometry. They are not model inputs.",
        "",
        "## Outputs",
        "",
        "- `planning/tfl6_mp11_impact_chart_extraction_summary.csv`",
        "- `planning/tfl6_mp11_impact_chart_extraction_summary.json`",
        "- `planning/tfl6_mp11_impact_chart_rows.csv`",
        "",
        "Ignored runtime detail files are under:",
        "",
        "```text",
        "runtime/document_ingestion/tfl6-mp11-full-figures/recovered/impact_batch/",
        "runtime/document_ingestion/tfl6-mp11-full-figures/overlays/impact_batch/",
        "```",
        "",
        "## Current Status",
        "",
        f"- Figures extracted: `{len(summaries)}`",
        "- Review status: `raw_extraction`",
        "- Downstream use: `needs_p7_5_review`",
        "- Model-input status: not accepted for model input",
        f"- Printed endpoint totals: {accepted_totals}",
        f"- Maximum geometry-vs-label residual: `{max_residual:,.0f} m3/year`",
        "",
        "## Next Step",
        "",
        "P7.5 should review the overlays and decide whether these figures can be",
        "promoted to `accepted_for_comparison` or should remain planning-only.",
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
        default=Path("planning/tfl6_mp11_impact_chart_extraction_summary.csv"),
    )
    parser.add_argument(
        "--rows-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_impact_chart_rows.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_impact_chart_extraction_summary.json"),
    )
    parser.add_argument(
        "--summary-md",
        type=Path,
        default=Path("planning/tfl6_mp11_impact_chart_extraction_summary.md"),
    )
    args = parser.parse_args()
    summaries, rows = run_batch(
        runtime_root=args.runtime_root,
        summary_csv=args.summary_csv,
        rows_csv=args.rows_csv,
        summary_json=args.summary_json,
    )
    _write_markdown(args.summary_md, summaries)
    print(f"extracted {len(summaries)} impact figures")
    print(f"wrote {len(rows)} step rows")
    print(args.summary_csv)
    print(args.rows_csv)
    print(args.summary_json)
    print(args.summary_md)


if __name__ == "__main__":
    main()
