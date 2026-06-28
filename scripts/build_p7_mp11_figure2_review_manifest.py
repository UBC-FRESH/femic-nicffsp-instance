"""Build a review manifest for the MP11 Figure 2 extraction pilot."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class Figure2Review:
    """Reviewed status for the MP11 Figure 2 extraction pilot."""

    figure_id: str
    caption: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    point_count: int
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    y_mean: float
    reference_value_m3_per_year: float
    mean_abs_percent_error: float
    validation_strength: str
    overlay_review_status: str
    model_input_status: str
    result_json_path: str
    points_csv_path: str
    overlay_path: str
    metrics_json_path: str
    notes: str


def _write_csv(path: Path, rows: list[Figure2Review]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def build_review_manifest(
    pilot_json: Path,
    output_csv: Path,
    output_json: Path,
    reviewer: str,
    reviewed_at_utc: str,
    reference_value_m3_per_year: float,
) -> list[Figure2Review]:
    pilot = json.loads(pilot_json.read_text(encoding="utf-8"))
    summary = pilot["result_summary"]
    artifacts = pilot["artifacts"]
    y_mean = float(summary["y_mean"])
    mean_abs_percent_error = abs(y_mean - reference_value_m3_per_year) / reference_value_m3_per_year * 100.0
    runtime_artifacts = [
        artifacts["raw_extraction_json"],
        artifacts["raw_points_csv"],
        artifacts["qa_overlay"],
        artifacts["qa_metrics"],
    ]
    artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
    review_status = "accepted_for_comparison" if artifacts_exist else "needs_value_review"
    rows = [
        Figure2Review(
            figure_id=pilot["figure_id"],
            caption=pilot["caption"],
            pdf_page=int(pilot["pdf_page"]),
            review_status=review_status,
            downstream_use=(
                "phase6_mp11_comparison_only"
                if review_status == "accepted_for_comparison"
                else "not_yet_accepted"
            ),
            review_basis=(
                "deterministic top-edge extraction; overlay inspection; "
                "mean harvest level cross-check against MP11 base-case reference value"
            ),
            reviewer=reviewer,
            reviewed_at_utc=reviewed_at_utc,
            point_count=int(summary["point_count"]),
            x_min=float(summary["x_min"]),
            x_max=float(summary["x_max"]),
            y_min=float(summary["y_min"]),
            y_max=float(summary["y_max"]),
            y_mean=y_mean,
            reference_value_m3_per_year=reference_value_m3_per_year,
            mean_abs_percent_error=mean_abs_percent_error,
            validation_strength="overlay_plus_base_case_reference_crosscheck",
            overlay_review_status=(
                "overlay_passed" if artifacts_exist else "missing_runtime_artifact"
            ),
            model_input_status="not_model_input",
            result_json_path=artifacts["raw_extraction_json"],
            points_csv_path=artifacts["raw_points_csv"],
            overlay_path=artifacts["qa_overlay"],
            metrics_json_path=artifacts["qa_metrics"],
            notes=(
                "Accepted only for MP11 comparison planning. This flat base-case "
                "harvest trajectory is useful for comparison context, but it is not "
                "model input without later maintainer promotion."
            ),
        )
    ]

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
        "reference_value_m3_per_year": reference_value_m3_per_year,
        "figure_count": len(rows),
        "status_counts": {
            status: sum(row.review_status == status for row in rows)
            for status in sorted({row.review_status for row in rows})
        },
        "figures": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return rows


def _write_markdown(path: Path, rows: list[Figure2Review]) -> None:
    row = rows[0]
    lines = [
        "# TFL 6 MP11 Figure 2 Review Manifest",
        "",
        "## Purpose",
        "",
        "This note records the review decision for the MP11 Figure 2 base-case",
        "harvest-level extraction pilot. It promotes the pilot to",
        "`accepted_for_comparison` while keeping it out of model-input surfaces.",
        "",
        "## Reviewed Inputs",
        "",
        "Raw pilot:",
        "",
        "- `planning/tfl6_mp11_figure2_extraction_pilot.md`",
        "- `planning/tfl6_mp11_figure2_extraction_pilot.json`",
        "",
        "Reviewed manifest:",
        "",
        "- `planning/tfl6_mp11_figure2_review_manifest.csv`",
        "- `planning/tfl6_mp11_figure2_review_manifest.json`",
        "",
        "Review helper:",
        "",
        "```bash",
        "python scripts/build_p7_mp11_figure2_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z",
        "```",
        "",
        "## Review Criteria",
        "",
        "The review used the following criteria:",
        "",
        "- deterministic extraction, not VLM-estimated values;",
        "- runtime point CSV, extraction JSON, overlay PNG, and metrics JSON exist;",
        "- overlay review confirms extracted points track the flat top edge of the",
        "  plotted harvest-level series;",
        "- mean recovered harvest level is cross-checked against the MP11 base-case",
        "  reference value; and",
        "- reviewed rows remain excluded from model-input surfaces.",
        "",
        "## Review Outcome",
        "",
        "- Figures reviewed: `1`",
        "- Status counts: `accepted_for_comparison`: `1`",
        "- Figures accepted for comparison: `1`",
        "- Figures accepted for model input: `0`",
        "- Downstream use assigned: `phase6_mp11_comparison_only`",
        "- Model-input status assigned: `not_model_input`",
        "",
        "Accepted comparison figure:",
        "",
        f"- `{row.figure_id}`: {row.caption}",
        f"  - point count: `{row.point_count}`",
        f"  - mean recovered value: `{row.y_mean:,.0f} m3/year`",
        f"  - reference value: `{row.reference_value_m3_per_year:,.0f} m3/year`",
        f"  - mean absolute percent error: `{row.mean_abs_percent_error:.2f}%`",
        "",
        "## Phase 6 Handoff",
        "",
        "Figure 2 can support MP11 base-case comparison context and should be",
        "handled with the other comparison-only harvest-flow evidence. It should",
        "not be copied into model-input bundles without explicit later review and",
        "promotion.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pilot-json",
        type=Path,
        default=Path("planning/tfl6_mp11_figure2_extraction_pilot.json"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_figure2_review_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_figure2_review_manifest.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_figure2_review_manifest.md"),
    )
    parser.add_argument(
        "--reference-value-m3-per-year",
        type=float,
        default=1_061_600.0,
    )
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_and_base_case_crosscheck_review",
    )
    parser.add_argument(
        "--reviewed-at-utc",
        default=datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    args = parser.parse_args()

    rows = build_review_manifest(
        pilot_json=args.pilot_json,
        output_csv=args.output_csv,
        output_json=args.output_json,
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
        reference_value_m3_per_year=args.reference_value_m3_per_year,
    )
    _write_markdown(args.output_md, rows)
    print(f"reviewed {len(rows)} figure-2 pilot row")
    print({row.review_status: sum(r.review_status == row.review_status for r in rows) for row in rows})
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
