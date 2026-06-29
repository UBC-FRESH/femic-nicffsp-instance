"""Review P11.3 MP11 candidate manifest provenance and fallback policy."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_manifest.csv"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_provenance_review.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT
    / "planning"
    / "tfl6_mp11_model_input_candidate_provenance_review.json"
)
DEFAULT_OUTPUT_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_provenance_review.md"
)


@dataclass(frozen=True)
class ProvenanceReviewRecord:
    """P11.3c review row for one candidate table role."""

    table_role: str
    bridge_action: str
    generation_eligibility: str
    downstream_status: str
    source_artifact_count: int
    missing_source_artifact_count: int
    missing_source_artifacts: str
    fallback_policy_present: bool
    caveat_fields_present: bool
    candidate_output_path: str
    review_status: str
    p11_3c_decision: str
    p11_4a_requirement: str


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _read_manifest(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Candidate manifest not found: {_repo_relative(path)}")

    with path.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))

    if not records:
        raise ValueError(f"Candidate manifest contains no rows: {_repo_relative(path)}")
    return records


def _split_sources(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def _review_record(row: dict[str, str]) -> ProvenanceReviewRecord:
    table_role = row["table_role"]
    sources = _split_sources(row.get("source_artifacts", ""))
    missing_sources = [
        source for source in sources if not (INSTANCE_ROOT / source).exists()
    ]
    fallback_present = bool(row.get("fallback_or_exclusion_policy", "").strip())
    caveats_present = bool(row.get("required_caveat_fields", "").strip())
    eligibility = row.get("generation_eligibility", "")
    downstream_status = row.get("downstream_status", "")

    if missing_sources or not fallback_present or not caveats_present:
        review_status = "blocked_missing_source_or_policy"
        decision = "blocked"
        p11_4a_requirement = "Resolve missing source, fallback, or caveat fields first."
    elif eligibility == "deferred_not_eligible":
        review_status = "deferred_not_model_input"
        decision = "deferred_non_blocking"
        p11_4a_requirement = (
            "Carry as deferred comparison metadata only; do not generate a table."
        )
    else:
        review_status = "reviewed_for_candidate_manifest"
        decision = "pass_candidate_scaffold"
        p11_4a_requirement = (
            "Verify candidate output role during P11.4a XML provenance audit."
        )

    return ProvenanceReviewRecord(
        table_role=table_role,
        bridge_action=row.get("bridge_action", ""),
        generation_eligibility=eligibility,
        downstream_status=downstream_status,
        source_artifact_count=len(sources),
        missing_source_artifact_count=len(missing_sources),
        missing_source_artifacts="; ".join(missing_sources),
        fallback_policy_present=fallback_present,
        caveat_fields_present=caveats_present,
        candidate_output_path=row.get("candidate_output_path", ""),
        review_status=review_status,
        p11_3c_decision=decision,
        p11_4a_requirement=p11_4a_requirement,
    )


def _summary(records: list[ProvenanceReviewRecord]) -> dict[str, Any]:
    decisions: dict[str, int] = {}
    statuses: dict[str, int] = {}
    for record in records:
        decisions[record.p11_3c_decision] = decisions.get(record.p11_3c_decision, 0) + 1
        statuses[record.review_status] = statuses.get(record.review_status, 0) + 1

    blocked_count = decisions.get("blocked", 0)
    return {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "record_count": len(records),
        "review_status_counts": statuses,
        "decision_counts": decisions,
        "blocked_count": blocked_count,
        "p11_3c_unlock_status": (
            "p11_4a_audit_eligible" if blocked_count == 0 else "blocked"
        ),
        "model_input_generation": "not_performed",
        "xml_generation": "not_performed",
        "matrix_builder": "not_performed",
        "runtime_bundle_generation": "not_performed",
    }


def _write_csv(path: Path, records: list[ProvenanceReviewRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(
    path: Path,
    *,
    input_csv: Path,
    records: list[ProvenanceReviewRecord],
    summary: dict[str, Any],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "input_csv": _repo_relative(input_csv),
        "summary": summary,
        "records": [asdict(record) for record in records],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_markdown(
    path: Path,
    *,
    input_csv: Path,
    output_csv: Path,
    output_json: Path,
    records: list[ProvenanceReviewRecord],
    summary: dict[str, Any],
) -> None:
    lines = [
        "# P11.3c MP11 Candidate Provenance Review",
        "",
        "This review locks the provenance and fallback-policy status for each "
        "P11.3 model-input candidate table role before P11.4 begins XML "
        "provenance audit work.",
        "",
        "P11.3c does not generate model-input tables, ForestModel XML, Matrix "
        "Builder outputs, or Patchworks runtime artifacts.",
        "",
        "## Inputs And Outputs",
        "",
        f"- Input manifest: `{_repo_relative(input_csv)}`",
        f"- Review CSV: `{_repo_relative(output_csv)}`",
        f"- Review JSON: `{_repo_relative(output_json)}`",
        "",
        "## Summary",
        "",
        f"- Candidate table roles reviewed: `{summary['record_count']}`",
        f"- Blocked roles: `{summary['blocked_count']}`",
        f"- P11.3c unlock status: `{summary['p11_3c_unlock_status']}`",
        "- Model-input generation: `not_performed`",
        "- ForestModel XML generation: `not_performed`",
        "- Matrix Builder: `not_performed`",
        "- Runtime bundle generation: `not_performed`",
        "",
        "## Decision Counts",
        "",
        "| Decision | Count |",
        "| --- | ---: |",
    ]
    for decision, count in sorted(summary["decision_counts"].items()):
        lines.append(f"| `{decision}` | {count} |")

    lines.extend(
        [
            "",
            "## Table-Role Review",
            "",
            "| Table role | Action | Sources | Missing | Decision | P11.4a requirement |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for record in records:
        lines.append(
            "| "
            f"`{record.table_role}` | "
            f"`{record.bridge_action}` | "
            f"{record.source_artifact_count} | "
            f"{record.missing_source_artifact_count} | "
            f"`{record.p11_3c_decision}` | "
            f"{record.p11_4a_requirement} |"
        )

    lines.extend(
        [
            "",
            "## Candidate Boundary",
            "",
            "All passing roles remain candidate-scaffold roles only. The single "
            "deferred role, `harvest_system_table`, remains comparison metadata "
            "and must not become a generated model-input table unless a later "
            "phase separately promotes stand-level harvest-system logic.",
            "",
            "P11.4a may audit candidate XML provenance against this review, but "
            "P11.4a must still avoid writing ForestModel XML. XML generation is "
            "reserved for P11.4c after the P11.4a/P11.4b audit and generation "
            "contract checks pass.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def build_review(
    *,
    input_csv: Path = DEFAULT_INPUT_CSV,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    manifest_records = _read_manifest(input_csv)
    records = [_review_record(row) for row in manifest_records]
    summary = _summary(records)
    _write_csv(output_csv, records)
    _write_json(output_json, input_csv=input_csv, records=records, summary=summary)
    _write_markdown(
        output_md,
        input_csv=input_csv,
        output_csv=output_csv,
        output_json=output_json,
        records=records,
        summary=summary,
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", type=Path, default=DEFAULT_INPUT_CSV)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_review(
        input_csv=args.input_csv,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
