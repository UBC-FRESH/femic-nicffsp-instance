"""Build Phase 13 MP11 KPI and caveat comparison report."""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "planning"

SCENARIO_COMPARISON = PLANNING / "tfl6_mp11_phase13_scenario_comparison.json"
LAND_BASE = PLANNING / "tfl6_mp11_land_base_crosswalk.csv"
NETDOWN = PLANNING / "tfl6_mp11_netdown_delta_crosswalk.csv"
MODEL_BEHAVIOR = PLANNING / "tfl6_mp11_model_behavior_crosswalk.csv"
REVIEWED_FIGURES = PLANNING / "tfl6_mp11_reviewed_extraction_manifest.csv"
RUNTIME_CLOSEOUT = PLANNING / "tfl6_mp11_phase12_runtime_closeout.json"

OUT_CSV = PLANNING / "tfl6_mp11_phase13_kpi_caveat_report.csv"
OUT_JSON = PLANNING / "tfl6_mp11_phase13_kpi_caveat_report.json"
OUT_MD = PLANNING / "tfl6_mp11_phase13_kpi_caveat_report.md"


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _src(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _row(
    *,
    report_id: str,
    kpi_family: str,
    metric_label: str,
    mp11_anchor: str,
    candidate_anchor: str,
    evidence_strength: str,
    evidence_role: str,
    caveat: str,
    release_implication: str,
    blocker_status: str,
    source_file: str,
) -> dict[str, str]:
    return {
        "report_id": report_id,
        "kpi_family": kpi_family,
        "metric_label": metric_label,
        "mp11_anchor": mp11_anchor,
        "candidate_anchor": candidate_anchor,
        "evidence_strength": evidence_strength,
        "evidence_role": evidence_role,
        "caveat": caveat,
        "release_implication": release_implication,
        "blocker_status": blocker_status,
        "source_file": source_file,
    }


def _scenario_rows() -> list[dict[str, str]]:
    data = _read_json(SCENARIO_COMPARISON)
    rows: list[dict[str, str]] = []
    for item in data["summary_rows"]:
        rows.append(
            _row(
                report_id=f"scenario_{item['comparison_id']}",
                kpi_family="harvest_flow",
                metric_label=item["label"],
                mp11_anchor="MP11 Figure 2/Table 11 base-case context",
                candidate_anchor=f"{item['value_m3_per_year']:.2f} m3/year",
                evidence_strength=item["evidence_strength"],
                evidence_role=item["evidence_role"],
                caveat=item["caveat"],
                release_implication=item["release_implication"],
                blocker_status="not_blocking"
                if item["comparison_id"].startswith("mp11_")
                else "needs_reproducible_base_export"
                if item["evidence_strength"] == "maintainer_context"
                else "scenario_smoke_only",
                source_file=_src(SCENARIO_COMPARISON),
            )
        )
    summary = data["summary"]
    rows.append(
        _row(
            report_id="scenario_candidate_thlb_context",
            kpi_family="land_base",
            metric_label="Candidate P9RF current THLB versus MP11 declared THLB",
            mp11_anchor=f"{summary['mp11_declared_thlb_ha']} ha",
            candidate_anchor=(
                f"{summary['candidate_thlb_ha']} ha; "
                f"{summary['candidate_thlb_delta_pct']:.2f}% above MP11"
            ),
            evidence_strength="tracked_model_input",
            evidence_role="candidate_scaffold_context",
            caveat="P9RF is candidate scaffold THLB, not final release truth.",
            release_implication="Supports plausibility but requires Phase 13 release QA and caveat documentation.",
            blocker_status="caveated_not_blocking",
            source_file=_src(SCENARIO_COMPARISON),
        )
    )
    return rows


def _land_base_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in _read_csv(LAND_BASE):
        rows.append(
            _row(
                report_id=f"land_{item['metric_id']}",
                kpi_family="land_base",
                metric_label=item["metric_label"],
                mp11_anchor=(
                    f"{item['mp11_value_ha']} ha; pages {item['mp11_pdf_pages']}"
                ),
                candidate_anchor=(
                    f"{item['phase5_reference_label']}: "
                    f"{item['phase5_reference_ha']} ha"
                ),
                evidence_strength="tracked_mp11_table_or_text",
                evidence_role=item["downstream_use"],
                caveat=item["notes"],
                release_implication=item["comparison_interpretation"],
                blocker_status="comparison_context_only"
                if item["model_input_status"] == "not_model_input"
                else "needs_review",
                source_file=_src(LAND_BASE),
            )
        )
    return rows


def _netdown_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in _read_csv(NETDOWN):
        rows.append(
            _row(
                report_id=f"netdown_{item['category_id']}",
                kpi_family="source_thlb_constraints",
                metric_label=item["category_label"],
                mp11_anchor=(
                    f"productive delta {item['productive_area_delta_ha']} ha; "
                    f"THLB-net delta {item['thlb_net_reduction_delta_ha']} ha"
                ),
                candidate_anchor=item["reproducibility_class"],
                evidence_strength="tracked_mp11_table_or_text",
                evidence_role=item["downstream_use"],
                caveat=item["interpretation"],
                release_implication=(
                    f"Follow-up lane {item['p6_followup_lane']}; keep visible in Phase 13 caveats."
                ),
                blocker_status="release_caveat"
                if "gap" in item["reproducibility_class"]
                or "confidential" in item["reproducibility_class"]
                else "caveated_not_blocking",
                source_file=_src(NETDOWN),
            )
        )
    return rows


def _model_behavior_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in _read_csv(MODEL_BEHAVIOR):
        rows.append(
            _row(
                report_id=f"behavior_{item['behavior_id']}",
                kpi_family=item["evidence_family"],
                metric_label=item["behavior_id"],
                mp11_anchor=(
                    f"{item['mp11_summary']} Numeric anchor: {item['mp11_numeric_anchor']}"
                ),
                candidate_anchor=item["phase5_comparison"],
                evidence_strength="tracked_mp11_table_or_text",
                evidence_role=item["downstream_use"],
                caveat=item["notes"],
                release_implication=item["phase7_plus_followup"],
                blocker_status="release_caveat"
                if "gap" in item["comparison_class"]
                or "missing" in item["implementation_gap"]
                else "comparison_context_only",
                source_file=_src(MODEL_BEHAVIOR),
            )
        )
    return rows


def _reviewed_figure_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in _read_csv(REVIEWED_FIGURES):
        rows.append(
            _row(
                report_id=f"figure_{item['figure_id'].lower().replace(' ', '_')}",
                kpi_family="reviewed_figure_evidence",
                metric_label=item["caption"],
                mp11_anchor=f"{item['figure_id']} page {item['pdf_page']}",
                candidate_anchor=item["review_basis"],
                evidence_strength="reviewed_mp11_figure_extraction",
                evidence_role=item["downstream_use"],
                caveat=item["notes"],
                release_implication="Comparison evidence only; do not promote to model input in Phase 13.",
                blocker_status="not_blocking",
                source_file=_src(REVIEWED_FIGURES),
            )
        )
    return rows


def _runtime_rows() -> list[dict[str, str]]:
    data = _read_json(RUNTIME_CLOSEOUT)
    summary = data["summary"]
    return [
        _row(
            report_id="runtime_matrix_builder_tracks",
            kpi_family="runtime_build",
            metric_label="Matrix Builder track generation",
            mp11_anchor="Phase 11 candidate XML/fragments",
            candidate_anchor=(
                f"{summary['track_file_count']} track files; "
                f"{summary['features_rows']} feature rows; "
                f"{summary['accounts_rows']} account rows"
            ),
            evidence_strength="tracked_runtime_output",
            evidence_role="candidate_runtime_smoke",
            caveat="Generated tracks are ignored local runtime outputs summarized by tracked QA.",
            release_implication="Supports runtime buildability; archive/materialization QA remains P13.4.",
            blocker_status="needs_archive_materialization_qa",
            source_file=_src(RUNTIME_CLOSEOUT),
        ),
        _row(
            report_id="runtime_scenario_smoke",
            kpi_family="runtime_build",
            metric_label="Representative scenario smoke",
            mp11_anchor="MP11 comparison context only",
            candidate_anchor=(
                f"{summary['scenario_iterations']} iterations; "
                f"{summary['scenario_schedule_rows']} scheduled rows"
            ),
            evidence_strength="tracked_runtime_output",
            evidence_role="candidate_runtime_smoke",
            caveat="Scenario smoke is not release QA or WFP equivalence.",
            release_implication="Supports Phase 13 comparison; release decision remains P13.5.",
            blocker_status="not_blocking",
            source_file=_src(RUNTIME_CLOSEOUT),
        ),
    ]


def build_report() -> dict[str, Any]:
    rows = [
        *_scenario_rows(),
        *_land_base_rows(),
        *_netdown_rows(),
        *_model_behavior_rows(),
        *_reviewed_figure_rows(),
        *_runtime_rows(),
    ]
    blocker_counts = Counter(row["blocker_status"] for row in rows)
    family_counts = Counter(row["kpi_family"] for row in rows)
    return {
        "summary": {
            "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "phase": "P13.2",
            "parent_issue": "#70",
            "child_issue": "#128",
            "report_status": "kpi_caveat_report_built",
            "row_count": len(rows),
            "blocker_counts": dict(sorted(blocker_counts.items())),
            "family_counts": dict(sorted(family_counts.items())),
            "release_qa": "not_performed",
            "release_decision": "pending_p13_5",
        },
        "rows": rows,
        "source_files": [
            _src(SCENARIO_COMPARISON),
            _src(LAND_BASE),
            _src(NETDOWN),
            _src(MODEL_BEHAVIOR),
            _src(REVIEWED_FIGURES),
            _src(RUNTIME_CLOSEOUT),
        ],
    }


def write_csv(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(data: dict[str, Any]) -> None:
    with OUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def write_markdown(data: dict[str, Any]) -> None:
    summary = data["summary"]
    rows = data["rows"]
    lines = [
        "# TFL 6 MP11 Phase 13 KPI And Caveat Comparison Report",
        "",
        "This report broadens the Phase 13 comparison beyond harvest flow. It consolidates tracked MP11 evidence, candidate-runtime evidence, source/THLB caveats, reviewed figure evidence, and runtime build evidence into one release-decision surface.",
        "",
        "## Summary",
        "",
        f"- report_status: `{summary['report_status']}`",
        f"- row_count: `{summary['row_count']}`",
        f"- release_qa: `{summary['release_qa']}`",
        f"- release_decision: `{summary['release_decision']}`",
        "",
        "## Blocker And Caveat Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    lines.extend(
        f"| `{status}` | `{count}` |"
        for status, count in summary["blocker_counts"].items()
    )
    lines.extend(
        [
            "",
            "## KPI Family Counts",
            "",
            "| Family | Count |",
            "| --- | ---: |",
        ]
    )
    lines.extend(
        f"| `{family}` | `{count}` |"
        for family, count in summary["family_counts"].items()
    )
    lines.extend(
        [
            "",
            "## High-Signal Rows",
            "",
            "| ID | Family | Metric | Evidence | Blocker Status | Release Implication |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    priority_statuses = {
        "release_caveat",
        "needs_reproducible_base_export",
        "needs_archive_materialization_qa",
        "scenario_smoke_only",
    }
    for row in rows:
        if row["blocker_status"] in priority_statuses:
            lines.append(
                f"| `{row['report_id']}` | `{row['kpi_family']}` | "
                f"{row['metric_label']} | `{row['evidence_strength']}` | "
                f"`{row['blocker_status']}` | {row['release_implication']} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The candidate runtime has enough evidence to proceed with Phase 13 documentation and archive QA, but this report still carries release caveats. The strongest positive signals are the close candidate THLB context, the smoke-tested runtime package, and harvest-flow behavior in the right broad range. The main blockers or caveats are reproducible export of the maintainer basic scenario, unresolved WFP/private constraint surfaces, harvest-system/MHA/scenario-policy gaps, and public-safe archive/materialization decisions.",
            "",
            "This report does not decide release status. P13.5 must decide whether the MP11 candidate replaces Phase 5, supplements Phase 5, or remains experimental after docs and archive QA complete.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    data = build_report()
    write_csv(data["rows"])
    write_json(data)
    write_markdown(data)
    print(f"wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"report_status={data['summary']['report_status']}")


if __name__ == "__main__":
    main()
