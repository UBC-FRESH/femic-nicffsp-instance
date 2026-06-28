"""Build first-pass crop proposals for MP11 high-priority figures.

This script is intentionally instance-local. It consumes the Phase 7
high-priority crop queue, detects coloured chart marks in the preliminary
full-page crops, and writes proposed chart crops plus a compact public-safe
summary. The proposals are review aids, not accepted extraction crops.
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
from PIL import Image


@dataclass(frozen=True)
class CropProposal:
    """One proposed chart crop generated from a preliminary full-page crop."""

    figure_id: str
    caption: str
    chart_family: str
    extraction_priority: str
    preliminary_crop_path: str
    proposal_path: str
    bbox_left: int | None
    bbox_top: int | None
    bbox_right: int | None
    bbox_bottom: int | None
    width_px: int | None
    height_px: int | None
    crop_sha256: str | None
    proposal_status: str
    review_status: str
    detection_note: str


def _figure_number(figure_id: str) -> int:
    return int(figure_id.lower().replace("figure", "").strip())


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for block in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _chart_colour_mask(image: np.ndarray) -> np.ndarray:
    """Return a mask for saturated chart marks while suppressing black text."""

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hue = hsv[:, :, 0]
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    saturated = (saturation >= 45) & (value >= 45) & (value <= 245)
    green = (hue >= 35) & (hue <= 95) & (saturation >= 35) & (value >= 35)
    magenta = ((hue <= 10) | (hue >= 145)) & (saturation >= 35) & (value >= 80)

    return (saturated | green | magenta).astype(np.uint8) * 255


def _proposal_bbox(image: Image.Image, padding: int, min_area: int) -> tuple[int, int, int, int, str] | None:
    rgb = np.array(image.convert("RGB"))
    mask = _chart_colour_mask(rgb)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 17))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.dilate(mask, kernel, iterations=2)

    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    boxes: list[tuple[int, int, int, int, int]] = []
    image_area = image.width * image.height
    for label in range(1, component_count):
        x, y, w, h, area = stats[label]
        if area < min_area:
            continue
        if area > image_area * 0.40:
            continue
        if w < 40 or h < 25:
            continue
        boxes.append((int(x), int(y), int(x + w), int(y + h), int(area)))

    if not boxes:
        return None

    left = max(0, min(box[0] for box in boxes) - padding)
    top = max(0, min(box[1] for box in boxes) - padding)
    right = min(image.width, max(box[2] for box in boxes) + padding)
    bottom = min(image.height, max(box[3] for box in boxes) + padding)
    note = f"{len(boxes)} colour components after filtering"
    return left, top, right, bottom, note


def _read_queue(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _write_csv(path: Path, rows: list[CropProposal]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys()) if rows else list(CropProposal.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def _write_json(path: Path, rows: list[CropProposal]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "proposal_count": len(rows),
        "status_counts": {
            status: sum(row.proposal_status == status for row in rows)
            for status in sorted({row.proposal_status for row in rows})
        },
        "review_status_counts": {
            status: sum(row.review_status == status for row in rows)
            for status in sorted({row.review_status for row in rows})
        },
        "proposals": [asdict(row) for row in rows],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_proposals(
    queue_path: Path,
    preliminary_crop_dir: Path,
    proposal_dir: Path,
    summary_csv: Path,
    summary_json: Path,
    padding: int,
    min_area: int,
) -> list[CropProposal]:
    rows: list[CropProposal] = []
    proposal_dir.mkdir(parents=True, exist_ok=True)

    for queue_row in sorted(_read_queue(queue_path), key=lambda row: _figure_number(row["figure_id"])):
        figure_id = queue_row["figure_id"]
        figure_slug = figure_id.lower().replace(" ", "-")
        crop_path = preliminary_crop_dir / f"{figure_slug}.png"
        proposal_path = proposal_dir / f"{figure_slug}-proposal.png"

        if not crop_path.exists():
            rows.append(
                CropProposal(
                    figure_id=figure_id,
                    caption=queue_row["caption"],
                    chart_family=queue_row["chart_family"],
                    extraction_priority=queue_row["extraction_priority"],
                    preliminary_crop_path=str(crop_path),
                    proposal_path=str(proposal_path),
                    bbox_left=None,
                    bbox_top=None,
                    bbox_right=None,
                    bbox_bottom=None,
                    width_px=None,
                    height_px=None,
                    crop_sha256=None,
                    proposal_status="missing_preliminary_crop",
                    review_status="not_reviewed",
                    detection_note="preliminary crop was not found",
                )
            )
            continue

        image = Image.open(crop_path).convert("RGB")
        bbox = _proposal_bbox(image, padding=padding, min_area=min_area)
        if bbox is None:
            rows.append(
                CropProposal(
                    figure_id=figure_id,
                    caption=queue_row["caption"],
                    chart_family=queue_row["chart_family"],
                    extraction_priority=queue_row["extraction_priority"],
                    preliminary_crop_path=str(crop_path),
                    proposal_path=str(proposal_path),
                    bbox_left=None,
                    bbox_top=None,
                    bbox_right=None,
                    bbox_bottom=None,
                    width_px=None,
                    height_px=None,
                    crop_sha256=None,
                    proposal_status="no_colour_bbox",
                    review_status="not_reviewed",
                    detection_note="no saturated chart-colour component passed filters",
                )
            )
            continue

        left, top, right, bottom, note = bbox
        proposal = image.crop((left, top, right, bottom))
        proposal.save(proposal_path)
        rows.append(
            CropProposal(
                figure_id=figure_id,
                caption=queue_row["caption"],
                chart_family=queue_row["chart_family"],
                extraction_priority=queue_row["extraction_priority"],
                preliminary_crop_path=str(crop_path),
                proposal_path=str(proposal_path),
                bbox_left=left,
                bbox_top=top,
                bbox_right=right,
                bbox_bottom=bottom,
                width_px=proposal.width,
                height_px=proposal.height,
                crop_sha256=_sha256(proposal_path),
                proposal_status="proposed",
                review_status="needs_manual_crop_review",
                detection_note=note,
            )
        )

    _write_csv(summary_csv, rows)
    _write_json(summary_json, rows)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--queue",
        type=Path,
        default=Path("planning/tfl6_mp11_priority_figure_crop_queue.csv"),
    )
    parser.add_argument(
        "--preliminary-crop-dir",
        type=Path,
        default=Path(
            "runtime/document_ingestion/tfl6-mp11-full-figures/crops/"
            "priority_high_preliminary"
        ),
    )
    parser.add_argument(
        "--proposal-dir",
        type=Path,
        default=Path(
            "runtime/document_ingestion/tfl6-mp11-full-figures/crops/"
            "priority_high_proposals"
        ),
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_priority_crop_proposals.csv"),
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=Path("planning/tfl6_mp11_priority_crop_proposals.json"),
    )
    parser.add_argument("--padding", type=int, default=70)
    parser.add_argument("--min-area", type=int, default=900)
    args = parser.parse_args()

    rows = build_proposals(
        queue_path=args.queue,
        preliminary_crop_dir=args.preliminary_crop_dir,
        proposal_dir=args.proposal_dir,
        summary_csv=args.summary_csv,
        summary_json=args.summary_json,
        padding=args.padding,
        min_area=args.min_area,
    )
    proposed = sum(row.proposal_status == "proposed" for row in rows)
    print(f"wrote {proposed} crop proposals from {len(rows)} priority rows")
    print(args.summary_csv)
    print(args.summary_json)


if __name__ == "__main__":
    main()
