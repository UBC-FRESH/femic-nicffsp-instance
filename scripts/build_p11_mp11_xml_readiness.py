"""Build the P11.4b MP11 ForestModel XML readiness manifest or stop report."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XML_AUDIT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_xml_provenance_audit.csv"
)
DEFAULT_CANDIDATE_MANIFEST_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_manifest.csv"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_readiness.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_readiness.json"
)
DEFAULT_OUTPUT_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_readiness.md"
)


@dataclass(frozen=True)
class XmlReadinessRecord:
    """P11.4b readiness row for one XML/component family."""

    component_family: str
    source_role: str
    p11_4a_action: str
    required_candidate_roles: str
    missing_candidate_outputs: str
    deferred_roles: str
    readiness_status: str
    p11_4c_generation_decision: str
    required_followup: str


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {_repo_relative(path)}")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"Required input has no rows: {_repo_relative(path)}")
    return rows


def _split_roles(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def _candidate_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["table_role"]: row for row in rows}


def _review_component(
    audit_row: dict[str, str], candidate_rows: dict[str, dict[str, str]]
) -> XmlReadinessRecord:
    component_family = audit_row["component_family"]
    source_roles = _split_roles(audit_row.get("source_role", ""))
    blocker_status = audit_row.get("blocker_status", "")

    missing_outputs: list[str] = []
    deferred_roles: list[str] = []
    required_roles: list[str] = []

    for role in source_roles:
        candidate_row = candidate_rows.get(role)
        if candidate_row is None:
            missing_outputs.append(f"{role}:candidate_manifest_row_missing")
            continue
        eligibility = candidate_row.get("generation_eligibility", "")
        output_path = candidate_row.get("candidate_output_path", "")
        if eligibility == "deferred_not_eligible":
            deferred_roles.append(role)
            continue
        required_roles.append(role)
        if not output_path:
            missing_outputs.append(f"{role}:candidate_output_path_missing")
        elif not (INSTANCE_ROOT / output_path).exists():
            missing_outputs.append(output_path)

    if blocker_status == "non_blocking_deferred":
        readiness_status = "deferred_non_blocking"
        decision = "skip_generation_for_component"
        required_followup = (
            "Preserve as deferred comparison metadata; do not require this "
            "component for P11.4c."
        )
    elif missing_outputs:
        readiness_status = "blocked_missing_candidate_outputs"
        decision = "block_p11_4c_xml_generation"
        required_followup = (
            "Generate and QA the MP11 candidate model-input bundle/export bridge "
            "before XML generation."
        )
    else:
        readiness_status = "ready_for_p11_4c_generation"
        decision = "allow_p11_4c_component_generation"
        required_followup = (
            "Carry this component into P11.4c XML generation under the MP11 "
            "candidate output root."
        )

    return XmlReadinessRecord(
        component_family=component_family,
        source_role=audit_row.get("source_role", ""),
        p11_4a_action=audit_row.get("p11_4a_action", ""),
        required_candidate_roles="; ".join(required_roles),
        missing_candidate_outputs="; ".join(missing_outputs),
        deferred_roles="; ".join(deferred_roles),
        readiness_status=readiness_status,
        p11_4c_generation_decision=decision,
        required_followup=required_followup,
    )


def _summary(records: list[XmlReadinessRecord]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for record in records:
        status_counts[record.readiness_status] = (
            status_counts.get(record.readiness_status, 0) + 1
        )

    blocked_count = status_counts.get("blocked_missing_candidate_outputs", 0)
    ready_count = status_counts.get("ready_for_p11_4c_generation", 0)
    deferred_count = status_counts.get("deferred_non_blocking", 0)
    return {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "component_count": len(records),
        "ready_count": ready_count,
        "blocked_count": blocked_count,
        "deferred_non_blocking_count": deferred_count,
        "readiness_status_counts": status_counts,
        "p11_4b_result": "stop_report" if blocked_count else "readiness_manifest",
        "p11_4c_generation_status": (
            "blocked_missing_candidate_outputs" if blocked_count else "eligible"
        ),
        "model_input_generation": "not_performed",
        "xml_generation": "not_performed",
        "matrix_builder": "not_performed",
        "runtime_bundle_generation": "not_performed",
    }


def _write_csv(path: Path, records: list[XmlReadinessRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(
    path: Path,
    *,
    records: list[XmlReadinessRecord],
    summary: dict[str, Any],
    xml_audit_csv: Path,
    candidate_manifest_csv: Path,
) -> None:
    payload = {
        "inputs": {
            "xml_audit_csv": _repo_relative(xml_audit_csv),
            "candidate_manifest_csv": _repo_relative(candidate_manifest_csv),
        },
        "summary": summary,
        "records": [asdict(record) for record in records],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_markdown(
    path: Path,
    *,
    records: list[XmlReadinessRecord],
    summary: dict[str, Any],
    output_csv: Path,
    output_json: Path,
) -> None:
    result_label = (
        "Stop Report" if summary["p11_4b_result"] == "stop_report" else "Manifest"
    )
    lines = [
        f"# P11.4b MP11 ForestModel XML Readiness {result_label}",
        "",
        "This P11.4b output evaluates whether the audited XML/component "
        "families can proceed to P11.4c candidate ForestModel XML generation.",
        "",
        "P11.4b does not generate model-input tables, ForestModel XML, Matrix "
        "Builder outputs, or Patchworks runtime artifacts.",
        "",
        "## Outputs",
        "",
        f"- Readiness CSV: `{_repo_relative(output_csv)}`",
        f"- Readiness JSON: `{_repo_relative(output_json)}`",
        "",
        "## Summary",
        "",
        f"- Result: `{summary['p11_4b_result']}`",
        f"- XML/component families evaluated: `{summary['component_count']}`",
        f"- Ready families: `{summary['ready_count']}`",
        f"- Blocked families: `{summary['blocked_count']}`",
        f"- Non-blocking deferred families: `{summary['deferred_non_blocking_count']}`",
        f"- P11.4c generation status: `{summary['p11_4c_generation_status']}`",
        "- Model-input generation: `not_performed`",
        "- ForestModel XML generation: `not_performed`",
        "- Matrix Builder: `not_performed`",
        "- Runtime bundle generation: `not_performed`",
        "",
        "## Component Readiness",
        "",
        "| Component | Status | Missing candidate outputs | Follow-up |",
        "| --- | --- | --- | --- |",
    ]
    for record in records:
        missing = record.missing_candidate_outputs or "-"
        lines.append(
            "| "
            f"`{record.component_family}` | "
            f"`{record.readiness_status}` | "
            f"`{missing}` | "
            f"{record.required_followup} |"
        )

    if summary["blocked_count"]:
        lines.extend(
            [
                "",
                "## Stop Condition",
                "",
                "P11.4c must not generate candidate ForestModel XML yet. The "
                "P11.3 candidate manifest defines planned model-input and export "
                "bridge paths, but the required candidate output files do not "
                "exist. Running the exporter against the protected Phase 5 bundle "
                "would produce Phase 5 XML under a new path, not an MP11 "
                "candidate XML package.",
                "",
                "The next implementation task must generate and QA the MP11 "
                "candidate model-input bundle/export bridge, or explicitly revise "
                "the Phase 11 roadmap so that bundle generation happens before "
                "P11.4c.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Generation Boundary",
                "",
                "P11.4c may generate candidate XML only under "
                "`output/patchworks_tfl6_mp11_candidate/` and must preserve the "
                "Phase 5 baseline paths.",
                "",
            ]
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def build_readiness(
    *,
    xml_audit_csv: Path = DEFAULT_XML_AUDIT_CSV,
    candidate_manifest_csv: Path = DEFAULT_CANDIDATE_MANIFEST_CSV,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    audit_rows = _read_csv(xml_audit_csv)
    candidate_rows = _candidate_lookup(_read_csv(candidate_manifest_csv))
    records = [_review_component(row, candidate_rows) for row in audit_rows]
    summary = _summary(records)
    _write_csv(output_csv, records)
    _write_json(
        output_json,
        records=records,
        summary=summary,
        xml_audit_csv=xml_audit_csv,
        candidate_manifest_csv=candidate_manifest_csv,
    )
    _write_markdown(
        output_md,
        records=records,
        summary=summary,
        output_csv=output_csv,
        output_json=output_json,
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--xml-audit-csv", type=Path, default=DEFAULT_XML_AUDIT_CSV)
    parser.add_argument(
        "--candidate-manifest-csv", type=Path, default=DEFAULT_CANDIDATE_MANIFEST_CSV
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_readiness(
        xml_audit_csv=args.xml_audit_csv,
        candidate_manifest_csv=args.candidate_manifest_csv,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
