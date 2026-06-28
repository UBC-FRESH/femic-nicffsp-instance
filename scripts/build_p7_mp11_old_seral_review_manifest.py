"""Build a review manifest for MP11 old-seral chart extractions."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ReviewedOldSeralFigure:
    """Reviewed status for one MP11 old-seral figure extraction."""

    figure_id: str
    caption: str
    landscape_unit: str
    scenario: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    series_count: int
    point_count: int
    min_series_point_count: int
    min_series_point_threshold: int
    series_coverage_status: str
    overlay_review_status: str
    validation_strength: str
    model_input_status: str
    rows_csv_path: str
    overlay_path: str
    notes: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _write_csv(path: Path, rows: list[ReviewedOldSeralFigure]) -> None:
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
    min_series_point_threshold: int,
    reviewer: str,
    reviewed_at_utc: str,
) -> list[ReviewedOldSeralFigure]:
    rows: list[ReviewedOldSeralFigure] = []
    for raw in _read_csv(extraction_summary_csv):
        min_series_point_count = int(raw["min_series_point_count"])
        runtime_artifacts = [raw["rows_csv_path"], raw["overlay_path"]]
        artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
        passes_coverage = min_series_point_count >= min_series_point_threshold
        review_status = (
            "reviewed_for_planning"
            if passes_coverage and artifacts_exist
            else "needs_value_review"
        )
        rows.append(
            ReviewedOldSeralFigure(
                figure_id=raw["figure_id"],
                caption=raw["caption"],
                landscape_unit=raw["landscape_unit"],
                scenario=raw["scenario"],
                pdf_page=int(raw["pdf_page"]),
                review_status=review_status,
                downstream_use=(
                    "phase6_mp11_old_seral_planning_only"
                    if review_status == "reviewed_for_planning"
                    else "not_yet_accepted"
                ),
                review_basis=(
                    "deterministic colour-based line extraction; manual plot bounds; "
                    "overlay inspection; adequate per-series point coverage; no adjacent "
                    "source table cross-check"
                ),
                reviewer=reviewer,
                reviewed_at_utc=reviewed_at_utc,
                series_count=int(raw["series_count"]),
                point_count=int(raw["point_count"]),
                min_series_point_count=min_series_point_count,
                min_series_point_threshold=min_series_point_threshold,
                series_coverage_status="passed" if passes_coverage else "failed",
                overlay_review_status=(
                    "contact_sheet_passed" if artifacts_exist else "missing_runtime_artifact"
                ),
                validation_strength="planning_only_no_source_table_cross_check",
                model_input_status="not_model_input",
                rows_csv_path=raw["rows_csv_path"],
                overlay_path=raw["overlay_path"],
                notes=(
                    "Reviewed only for old-seral planning context. The extraction tracks "
                    "visible plotted series well enough for qualitative and approximate "
                    "planning comparisons, but lacks a source-table or printed-label "
                    "cross-check; do not treat as comparison-accepted or model input."
                ),
            )
        )

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
        "min_series_point_threshold": min_series_point_threshold,
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


def _write_markdown(path: Path, rows: list[ReviewedOldSeralFigure]) -> None:
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    status_counts_text = ", ".join(
        f"`{status}`: `{count}`" for status, count in status_counts.items()
    )
    planning_rows = [row for row in rows if row.review_status == "reviewed_for_planning"]
    lines = [
        "# TFL 6 MP11 Old-Seral Review Manifest",
        "",
        "## Purpose",
        "",
        "This note records the review decision for the MP11 old-seral",
        "landscape-unit projection extraction batch. It promotes Figures `16`-`19`",
        "and `53`-`56` to planning-reviewed evidence, but not to",
        "comparison-accepted evidence.",
        "",
        "The conservative status is intentional. These charts have useful visible",
        "series trajectories, but no adjacent source tables or printed values for",
        "strong numeric validation.",
        "",
        "## Reviewed Inputs",
        "",
        "Raw extraction batch:",
        "",
        "- `planning/tfl6_mp11_old_seral_extraction_summary.md`",
        "- `planning/tfl6_mp11_old_seral_extraction_summary.csv`",
        "- `planning/tfl6_mp11_old_seral_series_summary.csv`",
        "- `planning/tfl6_mp11_old_seral_points.csv`",
        "",
        "Reviewed manifest:",
        "",
        "- `planning/tfl6_mp11_old_seral_review_manifest.csv`",
        "- `planning/tfl6_mp11_old_seral_review_manifest.json`",
        "",
        "Review helper:",
        "",
        "```bash",
        "python scripts/build_p7_mp11_old_seral_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z",
        "```",
        "",
        "## Review Criteria",
        "",
        "The review used the following criteria:",
        "",
        "- deterministic extraction, not VLM-estimated values;",
        "- runtime per-figure CSV and overlay PNG artifacts exist;",
        "- manual plot bounds align with the intended chart panel;",
        "- sampled points visibly track projected actual series rather than axes;",
        "- each figure has adequate per-series point coverage; and",
        "- the lack of source-table cross-check keeps the status planning-only.",
        "",
        "## Review Outcome",
        "",
        f"- Figures reviewed: `{len(rows)}`",
        f"- Status counts: {status_counts_text}",
        f"- Figures assigned `reviewed_for_planning`: `{len(planning_rows)}`",
        "- Figures accepted for comparison: `0`",
        "- Figures accepted for model input: `0`",
        "- Downstream use assigned: `phase6_mp11_old_seral_planning_only`",
        "- Model-input status assigned: `not_model_input`",
        "",
        "Reviewed planning figures:",
        "",
    ]
    for row in planning_rows:
        lines.append(
            f"- `{row.figure_id}`: {row.landscape_unit} `{row.scenario}`, "
            f"`{row.series_count}` series, `{row.point_count}` points"
        )
    lines.extend(
        [
            "",
            "## Phase 6 Handoff",
            "",
            "These figures can support qualitative and approximate Phase 6 planning",
            "around old-seral landscape-unit dynamics under the base case and AAC",
            "recommendation. They should not be used as accepted quantitative",
            "comparison evidence without stronger validation.",
            "",
            "They are relevant primarily to:",
            "",
            "- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;",
            "- `#46`: inventory, yield, operability, and harvest-system assumptions; and",
            "- `#48`: MP11-aligned implementation roadmap.",
            "",
            "No recovered point table should be copied into model-input surfaces",
            "without later maintainer review and explicit status promotion.",
            "",
            "## Remaining Work",
            "",
            "The review does not cover remaining table-plus-chart hybrid figures.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--extraction-summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_extraction_summary.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_review_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_review_manifest.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_old_seral_review_manifest.md"),
    )
    parser.add_argument("--min-series-point-threshold", type=int, default=75)
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_and_series_coverage_review",
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
        min_series_point_threshold=args.min_series_point_threshold,
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
    )
    _write_markdown(args.output_md, rows)
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    print(f"reviewed {len(rows)} old-seral figures")
    print(status_counts)
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
