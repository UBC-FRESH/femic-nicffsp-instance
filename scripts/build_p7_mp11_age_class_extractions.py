"""Extract MP11 age-class distribution stacked bar charts."""

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
AGE_CLASSES = ["0-20", "21-40", "41-60", "61-80", "81-100", "101-120", "121-140", "141-250", "251+"]
PRODUCTIVE_FOREST_AREA_HA = 187_425.0


@dataclass(frozen=True)
class PanelConfig:
    """One age-class subplot."""

    year: int
    left: int
    top: int
    right: int
    bottom: int
    y_max_ha: float = 68_000.0
    top_exclusion_px: int = 8


@dataclass(frozen=True)
class FigureConfig:
    """Manual extraction configuration for one age-class figure."""

    figure_id: str
    caption: str
    pdf_page: int
    image_path: str
    panels: list[PanelConfig]


@dataclass(frozen=True)
class AgeClassRow:
    """Recovered stacked bar values for one panel and age class."""

    figure_id: str
    year: int
    age_class: str
    thlb_ha: float
    nclb_ha: float
    total_ha: float


@dataclass(frozen=True)
class FigureSummary:
    """Compact summary of one age-class figure."""

    figure_id: str
    caption: str
    pdf_page: int
    source_sha256: str
    source_url: str
    image_path: str
    table_csv_path: str
    overlay_path: str
    panel_count: int
    age_class_count: int
    row_count: int
    min_total_minus_thlb_ha: float
    max_total_ha: float
    min_panel_total_ha: float
    max_panel_total_ha: float
    max_abs_panel_total_deviation_percent: float
    review_status: str
    downstream_use: str
    notes: str


def _configs(runtime_root: Path) -> list[FigureConfig]:
    proposal_dir = runtime_root / "crops" / "priority_high_proposals"
    fig6_panels = [
        PanelConfig(2023, 235, 72, 520, 358, top_exclusion_px=70),
        PanelConfig(2073, 571, 72, 861, 365, top_exclusion_px=70),
        PanelConfig(2123, 235, 417, 520, 704),
        PanelConfig(2173, 571, 417, 861, 704),
        PanelConfig(2223, 235, 762, 520, 1049),
        PanelConfig(2273, 571, 762, 861, 1049),
    ]
    fig45_panels = [
        PanelConfig(2023, 250, 75, 521, 344, top_exclusion_px=70),
        PanelConfig(2073, 568, 75, 839, 348, top_exclusion_px=70),
        PanelConfig(2123, 250, 396, 521, 669),
        PanelConfig(2173, 568, 396, 839, 669),
        PanelConfig(2223, 250, 717, 521, 986),
        PanelConfig(2273, 568, 717, 839, 986),
    ]
    return [
        FigureConfig(
            figure_id="Figure 6",
            caption="Base Case Age Class Distribution of Productive Forest Area (187,425 ha)",
            pdf_page=88,
            image_path=str(proposal_dir / "figure-6-proposal.png"),
            panels=fig6_panels,
        ),
        FigureConfig(
            figure_id="Figure 45",
            caption="AAC Recommendation Age Class Distribution of Productive Forest Area (187,425 ha)",
            pdf_page=158,
            image_path=str(proposal_dir / "figure-45-proposal.png"),
            panels=fig45_panels,
        ),
    ]


def _mask(image: np.ndarray, colour: tuple[int, int, int], tolerance: float) -> np.ndarray:
    distance = np.linalg.norm(image.astype(float) - np.array(colour, dtype=float), axis=2)
    return distance <= tolerance


def _panel_values(image: np.ndarray, figure_id: str, panel: PanelConfig) -> list[AgeClassRow]:
    panel_image = image[panel.top : panel.bottom + 1, panel.left : panel.right + 1]
    green = _mask(panel_image, (76, 255, 0), 95)
    dark = _mask(panel_image, (29, 58, 42), 75)
    stacked = green | dark
    plot_width = panel.right - panel.left
    plot_height = panel.bottom - panel.top
    slot_width = plot_width / len(AGE_CLASSES)
    rows: list[AgeClassRow] = []
    for index, age_class in enumerate(AGE_CLASSES):
        slot_left = int(round(index * slot_width + slot_width * 0.18))
        slot_right = int(round((index + 1) * slot_width - slot_width * 0.18))
        slot_green = green[:, slot_left:slot_right]
        slot_stack = stacked[:, slot_left:slot_right]
        green_y = np.where(slot_green)[0]
        stack_y = np.where(slot_stack)[0]
        if len(green_y):
            green_y = green_y[green_y >= panel.top_exclusion_px]
        if len(stack_y):
            stack_y = stack_y[stack_y >= panel.top_exclusion_px]
        if len(green_y):
            green_top = float(np.min(green_y))
            thlb = (plot_height - green_top) / plot_height * panel.y_max_ha
        else:
            thlb = 0.0
        if len(stack_y):
            stack_top = float(np.min(stack_y))
            total = (plot_height - stack_top) / plot_height * panel.y_max_ha
        else:
            total = thlb
        rows.append(
            AgeClassRow(
                figure_id=figure_id,
                year=panel.year,
                age_class=age_class,
                thlb_ha=thlb,
                nclb_ha=max(0.0, total - thlb),
                total_ha=total,
            )
        )
    return rows


def _write_csv(path: Path, rows: list[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _draw_overlay(image: Image.Image, config: FigureConfig, rows: list[AgeClassRow], output_path: Path) -> None:
    overlay = image.convert("RGB")
    draw = ImageDraw.Draw(overlay)
    rows_by_panel = {(row.year, row.age_class): row for row in rows}
    for panel in config.panels:
        draw.rectangle([panel.left, panel.top, panel.right, panel.bottom], outline=(220, 40, 40), width=2)
        plot_height = panel.bottom - panel.top
        plot_width = panel.right - panel.left
        slot_width = plot_width / len(AGE_CLASSES)
        for index, age_class in enumerate(AGE_CLASSES):
            row = rows_by_panel[(panel.year, age_class)]
            x_mid = panel.left + int(round((index + 0.5) * slot_width))
            y_thlb = panel.bottom - row.thlb_ha / panel.y_max_ha * plot_height
            y_total = panel.bottom - row.total_ha / panel.y_max_ha * plot_height
            draw.ellipse([x_mid - 3, y_thlb - 3, x_mid + 3, y_thlb + 3], fill=(0, 255, 0), outline=(0, 0, 0))
            draw.ellipse([x_mid - 3, y_total - 3, x_mid + 3, y_total + 3], fill=(35, 70, 45), outline=(0, 0, 0))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(output_path)


def run_batch(
    runtime_root: Path,
    summary_csv: Path,
    rows_csv: Path,
    summary_json: Path,
) -> tuple[list[FigureSummary], list[AgeClassRow]]:
    table_dir = runtime_root / "recovered" / "age_class_batch"
    overlay_dir = runtime_root / "overlays" / "age_class_batch"
    table_dir.mkdir(parents=True, exist_ok=True)
    overlay_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[FigureSummary] = []
    all_rows: list[AgeClassRow] = []
    for config in _configs(runtime_root):
        image_path = Path(config.image_path)
        image = Image.open(image_path).convert("RGB")
        image_array = np.array(image)
        rows: list[AgeClassRow] = []
        for panel in config.panels:
            rows.extend(_panel_values(image_array, config.figure_id, panel))
        figure_slug = config.figure_id.lower().replace(" ", "-")
        table_path = table_dir / f"{figure_slug}-age-class.csv"
        overlay_path = overlay_dir / f"{figure_slug}-overlay.png"
        _write_csv(table_path, rows)
        _draw_overlay(image, config, rows, overlay_path)
        all_rows.extend(rows)
        min_total_minus_thlb = min(row.total_ha - row.thlb_ha for row in rows)
        max_total = max(row.total_ha for row in rows)
        panel_totals = [
            sum(row.total_ha for row in rows if row.year == panel.year)
            for panel in config.panels
        ]
        max_abs_panel_deviation = max(
            abs(total - PRODUCTIVE_FOREST_AREA_HA) / PRODUCTIVE_FOREST_AREA_HA * 100
            for total in panel_totals
        )
        summaries.append(
            FigureSummary(
                figure_id=config.figure_id,
                caption=config.caption,
                pdf_page=config.pdf_page,
                source_sha256=SOURCE_SHA256,
                source_url=SOURCE_URL,
                image_path=str(image_path),
                table_csv_path=str(table_path),
                overlay_path=str(overlay_path),
                panel_count=len(config.panels),
                age_class_count=len(AGE_CLASSES),
                row_count=len(rows),
                min_total_minus_thlb_ha=min_total_minus_thlb,
                max_total_ha=max_total,
                min_panel_total_ha=min(panel_totals),
                max_panel_total_ha=max(panel_totals),
                max_abs_panel_total_deviation_percent=max_abs_panel_deviation,
                review_status="raw_extraction",
                downstream_use="not_yet_accepted",
                notes=(
                    "Stacked bar extraction from fixed panel and age-class slots; "
                    "requires overlay review before planning or comparison use."
                ),
            )
        )
    _write_csv(summary_csv, summaries)
    _write_csv(rows_csv, all_rows)
    payload = {
            "batch": "age_class",
            "status": "raw_extraction",
        "productive_forest_area_ha": PRODUCTIVE_FOREST_AREA_HA,
        "figure_count": len(summaries),
        "row_count": len(all_rows),
        "runtime_root": str(runtime_root),
        "figure_summaries": [asdict(row) for row in summaries],
        "age_class_rows": [asdict(row) for row in all_rows],
    }
    summary_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return summaries, all_rows


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
        default=Path("planning/tfl6_mp11_age_class_extraction_summary.csv"),
    )
    parser.add_argument(
        "--rows-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_age_class_rows.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_age_class_extraction_summary.json"),
    )
    args = parser.parse_args()
    summaries, rows = run_batch(args.runtime_root, args.summary_csv, args.rows_csv, args.summary_json)
    for summary in summaries:
        print(
            summary.figure_id,
            "rows",
            summary.row_count,
            "min_total_minus_thlb_ha",
            f"{summary.min_total_minus_thlb_ha:.1f}",
            "max_total_ha",
            f"{summary.max_total_ha:.1f}",
        )
    print(f"extracted {len(summaries)} figures and {len(rows)} age-class rows")
    print(args.summary_csv)
    print(args.rows_csv)
    print(args.summary_json)


if __name__ == "__main__":
    main()
