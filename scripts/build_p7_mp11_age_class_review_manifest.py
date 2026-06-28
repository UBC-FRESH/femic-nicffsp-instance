"""Build a review manifest for MP11 age-class figure extractions."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ReviewedAgeClassFigure:
    """Reviewed status for one MP11 age-class figure extraction."""

    figure_id: str
    caption: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    max_panel_total_deviation_percent: float
    min_total_minus_thlb_ha: float
    panel_total_deviation_status: str
    nonnegative_total_minus_thlb_status: str
    overlay_review_status: str
    model_input_status: str
    table_csv_path: str
    overlay_path: str
    notes: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _write_csv(path: Path, rows: list[ReviewedAgeClassFigure]) -> None:
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
    panel_deviation_threshold_percent: float,
    reviewer: str,
    reviewed_at_utc: str,
) -> list[ReviewedAgeClassFigure]:
    rows: list[ReviewedAgeClassFigure] = []
    for raw in _read_csv(extraction_summary_csv):
        max_deviation = float(raw["max_abs_panel_total_deviation_percent"])
        min_total_minus_thlb = float(raw["min_total_minus_thlb_ha"])
        runtime_artifacts = [raw["table_csv_path"], raw["overlay_path"]]
        artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
        passes_nonnegative = min_total_minus_thlb >= 0
        passes_deviation = max_deviation <= panel_deviation_threshold_percent
        # Planning review allows known approximate error; comparison acceptance does not.
        review_status = (
            "reviewed_for_planning"
            if passes_nonnegative and artifacts_exist
            else "needs_value_review"
        )
        rows.append(
            ReviewedAgeClassFigure(
                figure_id=raw["figure_id"],
                caption=raw["caption"],
                pdf_page=int(raw["pdf_page"]),
                review_status=review_status,
                downstream_use=(
                    "phase6_mp11_age_class_planning_only"
                    if review_status == "reviewed_for_planning"
                    else "not_yet_accepted"
                ),
                review_basis=(
                    "deterministic fixed-slot stacked-bar extraction; overlay contact-sheet "
                    "inspection; nonnegative total-minus-THLB check; panel-total deviation "
                    "recorded against the stated 187,425 ha productive forest area"
                ),
                reviewer=reviewer,
                reviewed_at_utc=reviewed_at_utc,
                max_panel_total_deviation_percent=max_deviation,
                min_total_minus_thlb_ha=min_total_minus_thlb,
                panel_total_deviation_status="passed" if passes_deviation else "warning",
                nonnegative_total_minus_thlb_status="passed" if passes_nonnegative else "failed",
                overlay_review_status=(
                    "contact_sheet_passed" if artifacts_exist else "missing_runtime_artifact"
                ),
                model_input_status="not_model_input",
                table_csv_path=raw["table_csv_path"],
                overlay_path=raw["overlay_path"],
                notes=(
                    "Reviewed only for MP11 age-class planning. Panel-total deviation is "
                    f"{max_deviation:.2f}%, so this is not comparison-accepted and must not "
                    "be used as model input without a stronger manual review."
                ),
            )
        )

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
        "panel_deviation_threshold_percent": panel_deviation_threshold_percent,
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
        default=Path("planning/tfl6_mp11_age_class_extraction_summary.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_age_class_review_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_age_class_review_manifest.json"),
    )
    parser.add_argument("--panel-deviation-threshold-percent", type=float, default=5.0)
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_and_panel_total_review",
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
        panel_deviation_threshold_percent=args.panel_deviation_threshold_percent,
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
    )
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    print(f"reviewed {len(rows)} age-class figures")
    print(status_counts)
    print(args.output_csv)
    print(args.output_json)


if __name__ == "__main__":
    main()
