"""Build a review manifest for MP11 timber-supply impact chart extractions."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class ReviewedImpactFigure:
    """Reviewed status for one MP11 impact chart extraction."""

    figure_id: str
    caption: str
    pdf_page: int
    review_status: str
    downstream_use: str
    review_basis: str
    reviewer: str
    reviewed_at_utc: str
    step_count: int
    accepted_printed_total_m3_per_year: float
    max_abs_geometry_minus_printed_m3_per_year: float
    max_abs_geometry_minus_printed_percent: float
    arithmetic_residual_m3_per_year: float
    arithmetic_status: str
    geometry_check_status: str
    overlay_review_status: str
    model_input_status: str
    rows_csv_path: str
    overlay_path: str
    notes: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _write_csv(path: Path, rows: list[ReviewedImpactFigure]) -> None:
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
    arithmetic_threshold_m3_per_year: float,
    geometry_threshold_m3_per_year: float,
    reviewer: str,
    reviewed_at_utc: str,
) -> list[ReviewedImpactFigure]:
    rows: list[ReviewedImpactFigure] = []
    for raw in _read_csv(extraction_summary_csv):
        arithmetic_residual = abs(float(raw["arithmetic_residual_m3_per_year"]))
        geometry_residual = float(raw["max_abs_geometry_minus_printed_m3_per_year"])
        runtime_artifacts = [raw["rows_csv_path"], raw["overlay_path"]]
        artifacts_exist = all(Path(path).exists() for path in runtime_artifacts)
        passes_arithmetic = arithmetic_residual <= arithmetic_threshold_m3_per_year
        passes_geometry = geometry_residual <= geometry_threshold_m3_per_year
        review_status = (
            "accepted_for_comparison"
            if passes_arithmetic and passes_geometry and artifacts_exist
            else "needs_value_review"
        )
        rows.append(
            ReviewedImpactFigure(
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
                    "printed chart-label transcription; deterministic coloured-component "
                    "geometry check; zero waterfall arithmetic residual; overlay inspection"
                ),
                reviewer=reviewer,
                reviewed_at_utc=reviewed_at_utc,
                step_count=int(raw["step_count"]),
                accepted_printed_total_m3_per_year=float(
                    raw["accepted_printed_total_m3_per_year"]
                ),
                max_abs_geometry_minus_printed_m3_per_year=geometry_residual,
                max_abs_geometry_minus_printed_percent=float(
                    raw["max_abs_geometry_minus_printed_percent"]
                ),
                arithmetic_residual_m3_per_year=float(raw["arithmetic_residual_m3_per_year"]),
                arithmetic_status="passed" if passes_arithmetic else "failed",
                geometry_check_status="passed" if passes_geometry else "warning",
                overlay_review_status=(
                    "contact_sheet_passed" if artifacts_exist else "missing_runtime_artifact"
                ),
                model_input_status="not_model_input",
                rows_csv_path=raw["rows_csv_path"],
                overlay_path=raw["overlay_path"],
                notes=(
                    "Accepted only for MP10-to-MP11 comparison planning. The accepted "
                    "values are printed chart labels checked against bar geometry; do not "
                    "treat as model input without later maintainer promotion."
                ),
            )
        )

    _write_csv(output_csv, rows)
    payload = {
        "review_manifest": output_csv.as_posix(),
        "reviewed_at_utc": reviewed_at_utc,
        "reviewer": reviewer,
        "arithmetic_threshold_m3_per_year": arithmetic_threshold_m3_per_year,
        "geometry_threshold_m3_per_year": geometry_threshold_m3_per_year,
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


def _write_markdown(path: Path, rows: list[ReviewedImpactFigure]) -> None:
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    status_counts_text = ", ".join(
        f"`{status}`: `{count}`" for status, count in status_counts.items()
    )
    accepted = [row for row in rows if row.review_status == "accepted_for_comparison"]
    lines = [
        "# TFL 6 MP11 Impact Chart Review Manifest",
        "",
        "## Purpose",
        "",
        "This note records the review decision for the MP11 timber-supply impact",
        "waterfall chart extraction batch. It promotes Figures `20` and `57` to",
        "comparison-accepted evidence for MP10-to-MP11 planning, while keeping",
        "them out of model-input surfaces.",
        "",
        "## Reviewed Inputs",
        "",
        "Raw extraction batch:",
        "",
        "- `planning/tfl6_mp11_impact_chart_extraction_summary.md`",
        "- `planning/tfl6_mp11_impact_chart_extraction_summary.csv`",
        "- `planning/tfl6_mp11_impact_chart_rows.csv`",
        "",
        "Reviewed manifest:",
        "",
        "- `planning/tfl6_mp11_impact_chart_review_manifest.csv`",
        "- `planning/tfl6_mp11_impact_chart_review_manifest.json`",
        "",
        "Review helper:",
        "",
        "```bash",
        "python scripts/build_p7_mp11_impact_chart_review_manifest.py --reviewed-at-utc 2026-06-28T00:00:00Z",
        "```",
        "",
        "## Review Criteria",
        "",
        "The review used the following criteria:",
        "",
        "- extracted values are printed chart labels, not VLM estimates;",
        "- deterministic coloured-component geometry identifies the matching bars;",
        "- runtime per-figure step CSV and overlay PNG artifacts exist;",
        "- waterfall arithmetic residual is zero; and",
        "- maximum geometry-vs-label residual is below the review threshold.",
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
        lines.extend(
            [
                f"- `{row.figure_id}`: {row.caption}",
                f"  - accepted printed endpoint: `{row.accepted_printed_total_m3_per_year:,.0f} m3/year`",
                f"  - arithmetic residual: `{row.arithmetic_residual_m3_per_year:,.0f} m3/year`",
                f"  - maximum geometry-vs-label residual: `{row.max_abs_geometry_minus_printed_m3_per_year:,.0f} m3/year`",
            ]
        )
    lines.extend(
        [
            "",
            "## Phase 6 Handoff",
            "",
            "These figures can support MP10-to-MP11 comparison planning and narrative",
            "checks around the base-case and AAC-recommendation bridge. They should",
            "not be copied into model-input bundles without explicit later review.",
            "",
            "They are relevant primarily to:",
            "",
            "- `#44`: MP11 tables, figures, sections, assumptions, and metadata extraction;",
            "- `#46`: inventory, yield, operability, and harvest-system assumptions; and",
            "- `#47`: model behavior, sensitivities, AAC, and KPI comparison.",
            "",
            "## Remaining Work",
            "",
            "The review does not cover old-seral landscape-unit charts or remaining",
            "table-plus-chart hybrid figures.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--extraction-summary-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_impact_chart_extraction_summary.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_impact_chart_review_manifest.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_impact_chart_review_manifest.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_impact_chart_review_manifest.md"),
    )
    parser.add_argument("--arithmetic-threshold-m3-per-year", type=float, default=1.0)
    parser.add_argument("--geometry-threshold-m3-per-year", type=float, default=10_000.0)
    parser.add_argument(
        "--reviewer",
        default="codex_agent_overlay_arithmetic_and_geometry_review",
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
        arithmetic_threshold_m3_per_year=args.arithmetic_threshold_m3_per_year,
        geometry_threshold_m3_per_year=args.geometry_threshold_m3_per_year,
        reviewer=args.reviewer,
        reviewed_at_utc=args.reviewed_at_utc,
    )
    _write_markdown(args.output_md, rows)
    status_counts = {
        status: sum(row.review_status == status for row in rows)
        for status in sorted({row.review_status for row in rows})
    }
    print(f"reviewed {len(rows)} impact figures")
    print(status_counts)
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
