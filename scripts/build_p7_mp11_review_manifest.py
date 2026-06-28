"""Build a compact review manifest for MP11 extracted figure evidence."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ReviewedFigure:
    """Reviewed status for one recovered MP11 figure."""

    figure_id: str
    caption: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    max_absolute_percent_error: float
    table_crosscheck_status: str
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


def _write_csv(path: Path, rows: list[ReviewedFigure]) -> None:
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
    max_error_threshold: float,
    reviewer: str,
    reviewed_at_utc: str,
) -> list[ReviewedFigure]:
    rows: list[ReviewedFigure] = []
    for raw in _read_csv(extraction_summary_csv):
        max_error = float(raw["max_absolute_percent_error"])
        runtime_artifacts = [
            raw["result_json_path"],
            raw["points_csv_path"],
            raw["overlay_path"],
            raw["metrics_json_path"],
        ]
        artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
        passes_error = max_error <= max_error_threshold
        review_status = (
            "accepted_for_comparison"
            if passes_error and artifacts_exist
            else "needs_value_review"
        )
        downstream_use = (
            "phase6_mp11_comparison_only"
            if review_status == "accepted_for_comparison"
            else "not_yet_accepted"
        )
        rows.append(
            ReviewedFigure(
                figure_id=raw["figure_id"],
                caption=raw["caption"],
                pdf_page=int(raw["pdf_page"]),
                review_status=review_status,
                downstream_use=downstream_use,
                review_basis=(
                    "deterministic extraction; overlay contact-sheet inspection; "
                    f"adjacent MP11 table cross-check <= {max_error_threshold}%"
                ),
                reviewer=reviewer,
                reviewed_at_utc=reviewed_at_utc,
                max_absolute_percent_error=max_error,
                table_crosscheck_status="passed" if passes_error else "failed",
                overlay_review_status=(
                    "contact_sheet_passed" if artifacts_exist else "missing_runtime_artifact"
                ),
                model_input_status="not_model_input",
                result_json_path=raw["result_json_path"],
                points_csv_path=raw["points_csv_path"],
                overlay_path=raw["overlay_path"],
                metrics_json_path=raw["metrics_json_path"],
                notes=(
                    "Accepted only for MP11 comparison planning. Do not use as model input "
                    "without a later maintainer review and explicit promotion."
                ),
            )
        )

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
        "max_error_threshold": max_error_threshold,
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
        default=Path("planning/tfl6_mp11_harvest_sensitivity_extraction_summary.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_reviewed_extraction_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_reviewed_extraction_manifest.json"),
    )
    parser.add_argument("--max-error-threshold", type=float, default=1.0)
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_and_table_crosscheck_review",
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
        max_error_threshold=args.max_error_threshold,
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
    )
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    print(f"reviewed {len(rows)} extracted figures")
    print(status_counts)
    print(args.output_csv)
    print(args.output_json)


if __name__ == "__main__":
    main()
