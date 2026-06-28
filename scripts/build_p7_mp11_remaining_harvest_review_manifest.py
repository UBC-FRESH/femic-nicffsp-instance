"""Build a review manifest for remaining MP11 harvest-scenario charts."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ReviewedRemainingHarvestFigure:
    """Reviewed status for one remaining MP11 harvest-scenario figure."""

    figure_id: str
    caption: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    series_count: int
    point_count: int
    min_series_point_count: int
    max_endpoint_abs_percent_error: float
    endpoint_error_threshold_percent: float
    endpoint_crosscheck_status: str
    overlay_review_status: str
    validation_strength: str
    model_input_status: str
    rows_csv_path: str
    overlay_path: str
    notes: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _write_csv(path: Path, rows: list[ReviewedRemainingHarvestFigure]) -> None:
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
    endpoint_error_threshold_percent: float,
    reviewer: str,
    reviewed_at_utc: str,
) -> list[ReviewedRemainingHarvestFigure]:
    rows: list[ReviewedRemainingHarvestFigure] = []
    for raw in _read_csv(extraction_summary_csv):
        max_error = float(raw["max_endpoint_abs_percent_error"])
        runtime_artifacts = [raw["rows_csv_path"], raw["overlay_path"]]
        artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
        passes_endpoint = max_error <= endpoint_error_threshold_percent
        review_status = (
            "accepted_for_comparison"
            if passes_endpoint and artifacts_exist
            else "needs_value_review"
        )
        rows.append(
            ReviewedRemainingHarvestFigure(
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
                    "deterministic colour-based harvest-line extraction; overlay inspection; "
                    "endpoint cross-check against visible MP11 table or narrative values"
                ),
                reviewer=reviewer,
                reviewed_at_utc=reviewed_at_utc,
                series_count=int(raw["series_count"]),
                point_count=int(raw["point_count"]),
                min_series_point_count=int(raw["min_series_point_count"]),
                max_endpoint_abs_percent_error=max_error,
                endpoint_error_threshold_percent=endpoint_error_threshold_percent,
                endpoint_crosscheck_status="passed" if passes_endpoint else "failed",
                overlay_review_status=(
                    "contact_sheet_passed" if artifacts_exist else "missing_runtime_artifact"
                ),
                validation_strength="endpoint_table_or_narrative_crosscheck",
                model_input_status="not_model_input",
                rows_csv_path=raw["rows_csv_path"],
                overlay_path=raw["overlay_path"],
                notes=(
                    "Accepted only for MP11 comparison planning. Endpoint values are "
                    "cross-checked against visible table or narrative values, but these "
                    "rows are not model input without later maintainer promotion."
                ),
            )
        )

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
        "endpoint_error_threshold_percent": endpoint_error_threshold_percent,
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


def _write_markdown(path: Path, rows: list[ReviewedRemainingHarvestFigure]) -> None:
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    status_counts_text = ", ".join(
        f"`{status}`: `{count}`" for status, count in status_counts.items()
    )
    accepted = [row for row in rows if row.review_status == "accepted_for_comparison"]
    lines = [
        "# TFL 6 MP11 Remaining Harvest Scenario Review Manifest",
        "",
        "## Purpose",
        "",
        "This note records the review decision for the remaining MP11",
        "harvest/scenario line-chart extraction batch. It promotes the batch to",
        "comparison-accepted evidence while keeping every row out of model-input",
        "surfaces.",
        "",
        "## Reviewed Inputs",
        "",
        "Raw extraction batch:",
        "",
        "- `planning/tfl6_mp11_remaining_harvest_extraction_summary.md`",
        "- `planning/tfl6_mp11_remaining_harvest_extraction_summary.csv`",
        "- `planning/tfl6_mp11_remaining_harvest_series_summary.csv`",
        "- `planning/tfl6_mp11_remaining_harvest_points.csv`",
        "",
        "Reviewed manifest:",
        "",
        "- `planning/tfl6_mp11_remaining_harvest_review_manifest.csv`",
        "- `planning/tfl6_mp11_remaining_harvest_review_manifest.json`",
        "",
        "Review helper:",
        "",
        "```bash",
        "python scripts/build_p7_mp11_remaining_harvest_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z",
        "```",
        "",
        "## Review Criteria",
        "",
        "The review used the following criteria:",
        "",
        "- deterministic extraction, not VLM-estimated values;",
        "- runtime per-figure CSV and overlay PNG artifacts exist;",
        "- overlay review confirms line sampling follows the intended plotted series;",
        "- endpoint values are cross-checked against visible table or narrative values;",
        "- maximum endpoint absolute percent error is below threshold; and",
        "- reviewed rows remain excluded from model-input surfaces.",
        "",
        "## Review Outcome",
        "",
        f"- Figures reviewed: `{len(rows)}`",
        f"- Status counts: {status_counts_text}",
        f"- Figures accepted for comparison: `{len(accepted)}`",
        "- Figures accepted for model input: `0`",
        "- Downstream use assigned: `phase6_mp11_comparison_only`",
        "- Model-input status assigned: `not_model_input`",
        "",
        "Accepted comparison figures:",
        "",
    ]
    for row in accepted:
        lines.append(
            f"- `{row.figure_id}`: {row.caption}; max endpoint error "
            f"`{row.max_endpoint_abs_percent_error:.2f}%`"
        )
    lines.extend(
        [
            "",
            "## Phase 6 Handoff",
            "",
            "These figures can support MP11 harvest-scenario comparison planning and",
            "sensitivity interpretation. They should not be copied into model-input",
            "bundles without explicit later review and promotion.",
            "",
            "They are relevant primarily to:",
            "",
            "- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;",
            "- `#46`: inventory, yield, operability, and harvest-system assumptions; and",
            "- `#47`: model behavior, sensitivities, AAC, and KPI comparison.",
            "",
            "## Remaining Work",
            "",
            "The review does not cover any lower-priority figures outside the Phase 7",
            "high-priority queue.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--extraction-summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_extraction_summary.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_review_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_review_manifest.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_remaining_harvest_review_manifest.md"),
    )
    parser.add_argument("--endpoint-error-threshold-percent", type=float, default=0.5)
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_and_endpoint_crosscheck_review",
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
        endpoint_error_threshold_percent=args.endpoint_error_threshold_percent,
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
    )
    _write_markdown(args.output_md, rows)
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    print(f"reviewed {len(rows)} remaining harvest figures")
    print(status_counts)
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
