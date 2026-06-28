"""Build the P6.3 MP11 land-base and THLB comparison crosswalk."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"


@dataclass(frozen=True)
class LandBaseComparison:
    """Reviewed comparison row for one MP11 land-base metric."""

    metric_id: str
    metric_label: str
    mp11_value_ha: float
    phase5_reference_label: str
    phase5_reference_ha: float | None
    delta_ha: float | None
    delta_percent_vs_phase5: float | None
    mp11_pdf_pages: str
    mp11_source_context: str
    phase5_source: str
    comparison_interpretation: str
    review_status: str
    downstream_use: str
    model_input_status: str
    notes: str


MP11_ROWS = [
    {
        "metric_id": "total_landbase",
        "metric_label": "Total TFL area / total land base",
        "mp11_value_ha": 217_197.0,
        "phase5_reference_label": "P1.6 current FADM-derived TFL 6 AOI",
        "phase5_reference_ha": 217_042.71895,
        "mp11_pdf_pages": "15, 19, 283, 284",
        "mp11_source_context": "Main document section 2.2; Appendix B Table 12",
        "phase5_source": "planning/tfl6_adjusted_thlb_benchmarks.json",
        "comparison_interpretation": (
            "Rounded MP11 land-base area is within 0.1% of the Phase 5 FADM-derived AOI; "
            "boundary area is effectively aligned for planning comparison."
        ),
    },
    {
        "metric_id": "total_forested",
        "metric_label": "Total forested",
        "mp11_value_ha": 196_233.0,
        "phase5_reference_label": "P2.4e smoke total forested",
        "phase5_reference_ha": 196_833.177,
        "mp11_pdf_pages": "284",
        "mp11_source_context": "Appendix B Table 12",
        "phase5_source": "planning/tfl6_thlb_benchmark_tolerance.md",
        "comparison_interpretation": (
            "MP11 total forested area is close to the Phase 2 smoke checkpoint; "
            "difference is small relative to total land base."
        ),
    },
    {
        "metric_id": "productive_forest",
        "metric_label": "Productive forest / PFLB / AFLB-style checkpoint",
        "mp11_value_ha": 187_425.0,
        "phase5_reference_label": "Phase 5 accepted AFLB resultant-fragment area",
        "phase5_reference_ha": 191_168.597386,
        "mp11_pdf_pages": "15, 54, 284",
        "mp11_source_context": "Main document section 2.2; Appendix B Table 12",
        "phase5_source": "planning/tfl6_model_input_bundle_qa.md",
        "comparison_interpretation": (
            "MP11 productive forest is lower than the accepted Phase 5 AFLB surface. "
            "This is a direct Phase 6 land-base delta requiring source-layer and netdown review."
        ),
    },
    {
        "metric_id": "total_operable",
        "metric_label": "Total operable",
        "mp11_value_ha": 156_305.0,
        "phase5_reference_label": "P2.4e smoke total operable",
        "phase5_reference_ha": 174_768.947,
        "mp11_pdf_pages": "284",
        "mp11_source_context": "Appendix B Table 12",
        "phase5_source": "planning/tfl6_thlb_benchmark_tolerance.md",
        "comparison_interpretation": (
            "MP11 total operable area is materially lower than the Phase 2 smoke checkpoint; "
            "operability and economic operability assumptions need dedicated P6.4 review."
        ),
    },
    {
        "metric_id": "current_thlb",
        "metric_label": "Current THLB",
        "mp11_value_ha": 120_099.0,
        "phase5_reference_label": "Phase 5 accepted weighted THLB area",
        "phase5_reference_ha": 139_995.798287,
        "mp11_pdf_pages": "15, 53, 75, 284, 285",
        "mp11_source_context": "Main document section 2.2; Appendix A Executive Summary; Appendix B Table 12",
        "phase5_source": "planning/tfl6_model_input_bundle_qa.md",
        "comparison_interpretation": (
            "MP11 current THLB is substantially lower than the accepted Phase 5 THLB surface. "
            "This is the central land-base delta for MP11 model-overhaul planning."
        ),
    },
    {
        "metric_id": "non_contributing_landbase",
        "metric_label": "NCLB / productive forest not available for harvesting",
        "mp11_value_ha": 67_326.0,
        "phase5_reference_label": "Phase 5 accepted NTHLB area",
        "phase5_reference_ha": 51_172.799099,
        "mp11_pdf_pages": "15",
        "mp11_source_context": "Main document section 2.2",
        "phase5_source": "planning/tfl6_model_input_bundle_qa.md",
        "comparison_interpretation": (
            "MP11 NCLB is higher than the Phase 5 NTHLB surface, consistent with the lower MP11 THLB."
        ),
    },
    {
        "metric_id": "long_term_landbase",
        "metric_label": "Long-term land base after future roads",
        "mp11_value_ha": 118_672.0,
        "phase5_reference_label": "Scaled MP10 long-term landbase benchmark",
        "phase5_reference_ha": 134_598.870,
        "mp11_pdf_pages": "54, 285",
        "mp11_source_context": "Appendix A Executive Summary; Appendix B Table 12",
        "phase5_source": "planning/tfl6_adjusted_thlb_benchmarks.md",
        "comparison_interpretation": (
            "MP11 long-term land base is materially lower than the prior scaled benchmark; "
            "Phase 5 did not implement future-road long-term adjustment as an active base-lane output."
        ),
    },
    {
        "metric_id": "current_aac_supporting_thlb",
        "metric_label": "Current AAC-supporting THLB from previous MPs",
        "mp11_value_ha": 133_665.0,
        "phase5_reference_label": "Scaled MP10 current-THLB benchmark",
        "phase5_reference_ha": 136_487.728,
        "mp11_pdf_pages": "53",
        "mp11_source_context": "Appendix A Executive Summary previous-MP aggregation statement",
        "phase5_source": "planning/tfl6_adjusted_thlb_benchmarks.md",
        "comparison_interpretation": (
            "MP11 reports a previous-MP aggregated THLB close to the Phase 5 scaled benchmark, "
            "supporting the earlier benchmark as a reasonable planning reference."
        ),
    },
]


def _comparison(row: dict[str, object]) -> LandBaseComparison:
    mp11_value = float(row["mp11_value_ha"])
    phase5_value = row["phase5_reference_ha"]
    phase5_float = float(phase5_value) if phase5_value is not None else None
    delta = mp11_value - phase5_float if phase5_float is not None else None
    delta_percent = (delta / phase5_float * 100.0) if phase5_float else None
    return LandBaseComparison(
        metric_id=str(row["metric_id"]),
        metric_label=str(row["metric_label"]),
        mp11_value_ha=mp11_value,
        phase5_reference_label=str(row["phase5_reference_label"]),
        phase5_reference_ha=phase5_float,
        delta_ha=delta,
        delta_percent_vs_phase5=delta_percent,
        mp11_pdf_pages=str(row["mp11_pdf_pages"]),
        mp11_source_context=str(row["mp11_source_context"]),
        phase5_source=str(row["phase5_source"]),
        comparison_interpretation=str(row["comparison_interpretation"]),
        review_status="reviewed_evidence",
        downstream_use="phase6_land_base_comparison_only",
        model_input_status="not_model_input",
        notes=(
            "Reviewed planning comparison row. Values are not accepted model inputs "
            "until a later implementation phase explicitly promotes them."
        ),
    )


def build_crosswalk(output_csv: Path, output_json: Path, output_md: Path, generated_at_utc: str) -> list[LandBaseComparison]:
    rows = [_comparison(row) for row in MP11_ROWS]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    payload = {
        "generated_at_utc": generated_at_utc,
        "source_sha256": SOURCE_SHA256,
        "crosswalk_csv": output_csv.as_posix(),
        "row_count": len(rows),
        "review_status_counts": {"reviewed_evidence": len(rows)},
        "model_input_status_counts": {"not_model_input": len(rows)},
        "rows": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, rows, payload)
    return rows


def _write_markdown(path: Path, rows: list[LandBaseComparison], payload: dict[str, object]) -> None:
    lines = [
        "# TFL 6 MP11 Land Base And THLB Comparison Crosswalk",
        "",
        "## Purpose",
        "",
        "This P6.3 note normalizes the highest-priority MP11 land-base and THLB",
        "values against the accepted Phase 5 benchmark and model-input-bundle",
        "surfaces. It is comparison evidence only; it does not change model",
        "inputs.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_land_base_crosswalk.md`",
        "- `planning/tfl6_mp11_land_base_crosswalk.csv`",
        "- `planning/tfl6_mp11_land_base_crosswalk.json`",
        "",
        "## Status",
        "",
        f"- Rows: `{payload['row_count']}`",
        "- Review status: `reviewed_evidence`",
        "- Downstream use: `phase6_land_base_comparison_only`",
        "- Model-input status: `not_model_input`",
        "",
        "## Comparison Table",
        "",
        "| Metric | MP11 ha | Phase 5 reference | Phase 5 ha | Delta ha | Delta % |",
        "| --- | ---: | --- | ---: | ---: | ---: |",
    ]
    for row in rows:
        delta = "" if row.delta_ha is None else f"{row.delta_ha:,.3f}"
        delta_pct = "" if row.delta_percent_vs_phase5 is None else f"{row.delta_percent_vs_phase5:.2f}%"
        phase5 = "" if row.phase5_reference_ha is None else f"{row.phase5_reference_ha:,.3f}"
        lines.append(
            f"| {row.metric_label} | {row.mp11_value_ha:,.3f} | "
            f"{row.phase5_reference_label} | {phase5} | {delta} | {delta_pct} |"
        )
    lines.extend(
        [
            "",
            "## Key Findings",
            "",
            "- MP11 total land base is essentially aligned with the Phase 5 current",
            "  FADM-derived AOI after rounding.",
            "- MP11 productive forest and current THLB are lower than the accepted",
            "  Phase 5 AFLB/THLB model-input surfaces.",
            "- MP11 current THLB is `120,099 ha`, compared with the Phase 5 accepted",
            "  weighted THLB of `139,995.798 ha`.",
            "- MP11 reports the previous-MP aggregated current AAC-supporting THLB as",
            "  `133,665 ha`, close to the earlier scaled MP10 benchmark of",
            "  `136,487.728 ha`.",
            "- The land-base delta is large enough that MP11-aligned implementation",
            "  should plan a reviewed THLB/source-layer overhaul rather than treating",
            "  the Phase 5 teaching THLB as already MP11-aligned.",
            "",
            "## Use Boundary",
            "",
            "Rows in this crosswalk are reviewed Phase 6 comparison evidence. They",
            "are not accepted model inputs and should not be copied into bundle tables",
            "without a later implementation issue, PR, and maintainer review.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_land_base_crosswalk.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_land_base_crosswalk.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_land_base_crosswalk.md"),
    )
    parser.add_argument(
        "--generated-at-utc",
        default=datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    args = parser.parse_args()
    rows = build_crosswalk(
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
        generated_at_utc=args.generated_at_utc,
    )
    print(f"wrote {len(rows)} land-base comparison rows")
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
