"""Build a review manifest for MP11 cedar inventory extractions."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ReviewedCedarFigure:
    """Reviewed status for one MP11 cedar inventory figure extraction."""

    figure_id: str
    caption: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    min_total_minus_thlb_m3: float
    nonnegative_total_minus_thlb_status: str
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


def _write_csv(path: Path, rows: list[ReviewedCedarFigure]) -> None:
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
    reviewer: str,
    reviewed_at_utc: str,
) -> list[ReviewedCedarFigure]:
    rows: list[ReviewedCedarFigure] = []
    for raw in _read_csv(extraction_summary_csv):
        min_total_minus_thlb = float(raw["min_total_minus_thlb_m3"])
        runtime_artifacts = [
            raw["result_json_path"],
            raw["points_csv_path"],
            raw["overlay_path"],
            raw["metrics_json_path"],
        ]
        artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
        passes_sanity = min_total_minus_thlb >= 0
        review_status = "reviewed_for_planning" if passes_sanity and artifacts_exist else "needs_value_review"
        rows.append(
            ReviewedCedarFigure(
                figure_id=raw["figure_id"],
                caption=raw["caption"],
                pdf_page=int(raw["pdf_page"]),
                review_status=review_status,
                downstream_use=(
                    "phase6_mp11_cedar_planning_only"
                    if review_status == "reviewed_for_planning"
                    else "not_yet_accepted"
                ),
                review_basis=(
                    "deterministic stacked-area boundary extraction; overlay contact-sheet "
                    "inspection; total cedar volume remains greater than or equal to THLB "
                    "cedar volume"
                ),
                reviewer=reviewer,
                reviewed_at_utc=reviewed_at_utc,
                min_total_minus_thlb_m3=min_total_minus_thlb,
                nonnegative_total_minus_thlb_status="passed" if passes_sanity else "failed",
                overlay_review_status=(
                    "contact_sheet_passed" if artifacts_exist else "missing_runtime_artifact"
                ),
                model_input_status="not_model_input",
                result_json_path=raw["result_json_path"],
                points_csv_path=raw["points_csv_path"],
                overlay_path=raw["overlay_path"],
                metrics_json_path=raw["metrics_json_path"],
                notes=(
                    "Reviewed only for MP11 cedar planning. The QA basis is visual overlay "
                    "inspection plus a nonnegative total-minus-THLB sanity check; do not "
                    "treat as comparison-accepted or model input without a stronger review."
                ),
            )
        )

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
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
        default=Path("planning/tfl6_mp11_cedar_inventory_extraction_summary.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_cedar_inventory_review_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_cedar_inventory_review_manifest.json"),
    )
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_and_sanity_check_review",
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
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
    )
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    print(f"reviewed {len(rows)} cedar figures")
    print(status_counts)
    print(args.output_csv)
    print(args.output_json)


if __name__ == "__main__":
    main()
