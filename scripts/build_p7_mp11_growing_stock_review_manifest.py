"""Build a review manifest for MP11 growing-stock figure extractions."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ReviewedGrowingStockFigure:
    """Reviewed status for one MP11 growing-stock figure extraction."""

    figure_id: str
    caption: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    residual_metric: str
    residual_threshold_percent: float
    mean_abs_residual_percent: float
    max_abs_residual_percent: float
    internal_consistency_status: str
    overlay_review_status: str
    model_input_status: str
    result_json_path: str
    points_csv_path: str
    overlay_path: str
    metrics_json_path: str
    notes: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _write_csv(path: Path, rows: list[ReviewedGrowingStockFigure]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def build_review_manifest(
    extraction_summary_csv: Path,
    output_csv: Path,
    output_json: Path,
    residual_threshold_percent: float,
    reviewer: str,
    reviewed_at_utc: str,
) -> list[ReviewedGrowingStockFigure]:
    rows: list[ReviewedGrowingStockFigure] = []
    for raw in _read_csv(extraction_summary_csv):
        mean_residual = float(raw["component_sum_minus_total_mean_abs_percent"])
        max_residual = float(raw["component_sum_minus_total_max_abs_percent"])
        runtime_artifacts = [
            raw["result_json_path"],
            raw["points_csv_path"],
            raw["overlay_path"],
            raw["metrics_json_path"],
        ]
        artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
        passes_residual = max_residual <= residual_threshold_percent
        review_status = (
            "accepted_for_comparison"
            if passes_residual and artifacts_exist
            else "needs_value_review"
        )
        rows.append(
            ReviewedGrowingStockFigure(
                figure_id=raw["figure_id"],
                caption=raw["caption"],
                pdf_page=int(raw["pdf_page"]),
                review_status=review_status,
                downstream_use=(
                    "phase6_mp11_comparison_only"
                    if review_status == "accepted_for_comparison"
                    else "not_yet_accepted"
                ),
                review_basis=(
                    "deterministic extraction; overlay contact-sheet inspection; "
                    "component series sum to total growing-stock series within "
                    f"{residual_threshold_percent}%"
                ),
                reviewer=reviewer,
                reviewed_at_utc=reviewed_at_utc,
                residual_metric="abs((le_120_plus_gt_120) - total) / total * 100",
                residual_threshold_percent=residual_threshold_percent,
                mean_abs_residual_percent=mean_residual,
                max_abs_residual_percent=max_residual,
                internal_consistency_status="passed" if passes_residual else "failed",
                overlay_review_status=(
                    "contact_sheet_passed" if artifacts_exist else "missing_runtime_artifact"
                ),
                model_input_status="not_model_input",
                result_json_path=raw["result_json_path"],
                points_csv_path=raw["points_csv_path"],
                overlay_path=raw["overlay_path"],
                metrics_json_path=raw["metrics_json_path"],
                notes=(
                    "Accepted only for MP11 growing-stock comparison planning. "
                    "The QA basis is internal consistency, not an independent table "
                    "cross-check; do not use as model input without later promotion."
                ),
            )
        )

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
        "residual_threshold_percent": residual_threshold_percent,
        "figure_count": len(rows),
        "status_counts": {
            status: sum(row.review_status == status for row in rows)
            for status in sorted({row.review_status for row in rows})
        },
        "downstream_use_counts": {
            status: sum(row.downstream_use == status for row in rows)
            for status in sorted({row.downstream_use for row in rows})
        },
        "figures": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--extraction-summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_growing_stock_extraction_summary.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_growing_stock_review_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_growing_stock_review_manifest.json"),
    )
    parser.add_argument("--residual-threshold-percent", type=float, default=1.0)
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_and_internal_consistency_review",
    )
    parser.add_argument(
        "--reviewed-at-utc",
        default=datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    args = parser.parse_args()

    rows = build_review_manifest(
        extraction_summary_csv=args.extraction_summary_csv,
        output_csv=args.output_csv,
        output_json=args.output_json,
        residual_threshold_percent=args.residual_threshold_percent,
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
    )
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    print(f"reviewed {len(rows)} growing-stock figures")
    print(status_counts)
    print(args.output_csv)
    print(args.output_json)


if __name__ == "__main__":
    main()
