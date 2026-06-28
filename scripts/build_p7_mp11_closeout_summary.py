"""Build the Phase 7 MP11 figure-extraction closeout summary."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


ACCEPTED_REVIEW_FILES = [
    Path("planning/tfl6_mp11_figure2_review_manifest.csv"),
    Path("planning/tfl6_mp11_reviewed_extraction_manifest.csv"),
    Path("planning/tfl6_mp11_growing_stock_review_manifest.csv"),
    Path("planning/tfl6_mp11_impact_chart_review_manifest.csv"),
    Path("planning/tfl6_mp11_remaining_harvest_review_manifest.csv"),
]

PLANNING_REVIEW_FILES = [
    Path("planning/tfl6_mp11_cedar_inventory_review_manifest.csv"),
    Path("planning/tfl6_mp11_age_class_review_manifest.csv"),
    Path("planning/tfl6_mp11_old_seral_review_manifest.csv"),
]


@dataclass(frozen=True)
class FigureCloseoutRow:
    """Final Phase 7 status for one inventoried MP11 figure."""

    figure_id: str
    caption: str
    pdf_page: int
    chart_family: str
    extraction_priority: str
    phase7_status: str
    downstream_use: str
    model_input_status: str
    closeout_note: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _review_lookup(paths: list[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for path in paths:
        if not path.exists():
            continue
        for row in _read_csv(path):
            rows[row["figure_id"]] = row
    return rows


def _write_csv(path: Path, rows: list[FigureCloseoutRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def build_closeout(
    inventory_csv: Path,
    output_csv: Path,
    output_json: Path,
    output_md: Path,
    generated_at_utc: str,
) -> list[FigureCloseoutRow]:
    accepted = _review_lookup(ACCEPTED_REVIEW_FILES)
    planning = _review_lookup(PLANNING_REVIEW_FILES)
    inventory = _read_csv(inventory_csv)
    rows: list[FigureCloseoutRow] = []

    for raw in inventory:
        figure_id = raw["figure_id"]
        if figure_id in accepted:
            review = accepted[figure_id]
            phase7_status = "accepted_for_comparison"
            downstream_use = review.get("downstream_use", "phase6_mp11_comparison_only")
            model_input_status = review.get("model_input_status", "not_model_input")
            note = "Reviewed deterministic extraction; suitable for Phase 6 comparison planning only."
        elif figure_id in planning:
            review = planning[figure_id]
            phase7_status = "reviewed_for_planning"
            downstream_use = review.get("downstream_use", "phase6_mp11_planning_only")
            model_input_status = review.get("model_input_status", "not_model_input")
            note = "Reviewed deterministic extraction; useful as planning context but not comparison-accepted."
        elif raw["extraction_priority"] == "excluded_context":
            phase7_status = "inventory_context_only"
            downstream_use = "qualitative_context_only"
            model_input_status = "not_model_input"
            note = "Context map, diagram, or image; not a chart-to-table target in Phase 7."
        else:
            phase7_status = "deferred_not_extracted"
            downstream_use = "future_optional_review"
            model_input_status = "not_model_input"
            note = "Not extracted in the bounded Phase 7 test; mostly medium-priority stacked or mixed charts."

        rows.append(
            FigureCloseoutRow(
                figure_id=figure_id,
                caption=raw["caption"],
                pdf_page=int(raw["pdf_page"]),
                chart_family=raw["chart_family"],
                extraction_priority=raw["extraction_priority"],
                phase7_status=phase7_status,
                downstream_use=downstream_use,
                model_input_status=model_input_status,
                closeout_note=note,
            )
        )

    _write_csv(output_csv, rows)
    status_counts = Counter(row.phase7_status for row in rows)
    priority_counts = Counter(row.extraction_priority for row in rows)
    model_input_counts = Counter(row.model_input_status for row in rows)
    payload = {
        "generated_at_utc": generated_at_utc,
        "inventory_csv": inventory_csv.as_posix(),
        "closeout_csv": output_csv.as_posix(),
        "figure_count": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "priority_counts": dict(sorted(priority_counts.items())),
        "model_input_counts": dict(sorted(model_input_counts.items())),
        "figures": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, rows, payload)
    return rows


def _write_markdown(path: Path, rows: list[FigureCloseoutRow], payload: dict[str, object]) -> None:
    accepted = [row for row in rows if row.phase7_status == "accepted_for_comparison"]
    planning = [row for row in rows if row.phase7_status == "reviewed_for_planning"]
    deferred = [row for row in rows if row.phase7_status == "deferred_not_extracted"]
    context = [row for row in rows if row.phase7_status == "inventory_context_only"]
    priority_counts = payload["priority_counts"]
    model_input_counts = payload["model_input_counts"]

    def figure_list(items: list[FigureCloseoutRow]) -> str:
        return ", ".join(row.figure_id.replace("Figure ", "") for row in items)

    lines = [
        "# TFL 6 MP11 Figure Extraction Phase 7 Closeout",
        "",
        "## Purpose",
        "",
        "This note closes the bounded Phase 7 `figrecover` deployment test against",
        "the public TFL 6 Management Plan 11 PDF. It joins the full 61-row figure",
        "inventory to every reviewed extraction manifest and records what is ready",
        "for Phase 6 comparison planning, what remains planning-only, and what was",
        "deferred.",
        "",
        "## Source And Inventory",
        "",
        "- Source: public TFL 6 Management Plan 11 PDF",
        "- Source SHA256:",
        "  `44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b`",
        "- Inventory: `planning/tfl6_mp11_full_figure_inventory.csv`",
        f"- Inventory rows: `{len(rows)}`",
        f"- Priority counts: `{priority_counts}`",
        "",
        "## Closeout Files",
        "",
        "- `planning/tfl6_mp11_figure_extraction_closeout.md`",
        "- `planning/tfl6_mp11_figure_extraction_closeout.csv`",
        "- `planning/tfl6_mp11_figure_extraction_closeout.json`",
        "",
        "## Reviewed Evidence Surface",
        "",
        f"- Accepted for Phase 6 comparison planning: `{len(accepted)}` figures",
        f"- Reviewed for planning only: `{len(planning)}` figures",
        f"- Deferred after inventory/crop triage: `{len(deferred)}` figures",
        f"- Inventory context only: `{len(context)}` figures",
        f"- Model-input status counts: `{model_input_counts}`",
        "",
        "Accepted comparison figures:",
        "",
        f"- Figures `{figure_list(accepted)}`",
        "",
        "Planning-only reviewed figures:",
        "",
        f"- Figures `{figure_list(planning)}`",
        "",
        "Deferred figures:",
        "",
        f"- Figures `{figure_list(deferred)}`",
        "",
        "Context-only figures:",
        "",
        f"- Figures `{figure_list(context)}`",
        "",
        "## Interpretation",
        "",
        "Phase 7 completed the high-priority test target: all `36` high-priority",
        "figures now have explicit reviewed status. Of those, `22` are accepted",
        "for comparison planning and `14` are planning-only. No recovered figure",
        "table is accepted as model input.",
        "",
        "The `20` deferred figures are medium-priority stacked, grouped, mixed, or",
        "method-explanation charts. They are useful future stress tests for",
        "`figrecover`, but they are not required before Phase 6 can use the",
        "reviewed comparison evidence to plan the MP10-to-MP11 model-overhaul",
        "work.",
        "",
        "## Phase 6 Handoff",
        "",
        "Use comparison-accepted figures only for narrative and quantitative",
        "comparison planning in Phase 6. Treat planning-only figures as qualitative",
        "or approximate context unless a later task supplies stronger independent",
        "validation. Do not copy recovered rows into model-input bundles without a",
        "new maintainer review and explicit promotion to `accepted_for_model_input`.",
        "",
        "Primary Phase 6 consumers:",
        "",
        "- `#44`: MP11 extraction inventory and metadata;",
        "- `#46`: inventory, yield, operability, and harvest-system assumptions;",
        "- `#47`: model behavior, sensitivities, AAC, and KPI comparison; and",
        "- `#48`: MP11-aligned implementation roadmap.",
        "",
        "## Validation",
        "",
        "Final closeout validation should confirm:",
        "",
        "- reviewed manifests remain JSON/CSV readable;",
        "- runtime pages, crops, overlays, raw result JSON, and recovered point CSV",
        "  files remain ignored;",
        "- docs build if the Phase 7 Sphinx page is updated; and",
        "- GitHub issues and roadmap checkboxes match this closeout state.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_full_figure_inventory.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_figure_extraction_closeout.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_figure_extraction_closeout.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_figure_extraction_closeout.md"),
    )
    parser.add_argument(
        "--generated-at-utc",
        default=datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    args = parser.parse_args()
    rows = build_closeout(
        inventory_csv=args.inventory_csv,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
        generated_at_utc=args.generated_at_utc,
    )
    counts = Counter(row.phase7_status for row in rows)
    print(f"closed out {len(rows)} MP11 figures")
    print(dict(sorted(counts.items())))
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
