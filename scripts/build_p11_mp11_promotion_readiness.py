"""Build the Phase 11 MP11 model-input promotion-readiness audit."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATES_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_promotion_gates.csv"
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_promotion_readiness.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_promotion_readiness.json"
)
DEFAULT_OUTPUT_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_promotion_readiness.md"
)


@dataclass(frozen=True)
class GateSpec:
    """P11.2 readiness decision template for one P11.1 promotion gate."""

    gate_id: str
    source_artifact_path: str
    required_promotion_state: str
    actual_promotion_state: str
    required_qa_evidence: str
    decision: str
    blocker_or_caveat: str
    next_action_owner: str


@dataclass(frozen=True)
class ReadinessRecord:
    """Generated row for one P11.2 promotion-readiness gate."""

    gate_id: str
    gate_type: str
    target_role: str
    source_artifact_path: str
    source_exists: bool
    required_promotion_state: str
    actual_promotion_state: str
    required_qa_evidence: str
    decision: str
    blocker_or_caveat: str
    next_action_owner: str


GATE_SPECS: dict[str, GateSpec] = {
    "p11_gate_01_baseline_protection": GateSpec(
        gate_id="p11_gate_01_baseline_protection",
        source_artifact_path="planning/tfl6_mp11_phase11_artifact_layout.json",
        required_promotion_state="accepted_model_contract",
        actual_promotion_state="accepted_model_contract",
        required_qa_evidence=(
            "Candidate roots use MP11 namespace and Phase 5 accepted baseline "
            "paths are explicitly protected."
        ),
        decision="pass",
        blocker_or_caveat=(
            "P11.3+ must continue to write only MP11 candidate paths until a "
            "replacement runtime passes later QA."
        ),
        next_action_owner="P11.3 candidate manifest",
    ),
    "p11_gate_02_source_thlb": GateSpec(
        gate_id="p11_gate_02_source_thlb",
        source_artifact_path="planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md",
        required_promotion_state="accepted_candidate_scaffold_contract",
        actual_promotion_state="accepted_candidate_scaffold_contract_with_caveats",
        required_qa_evidence=(
            "P9RF resultant-fragment THLB is assigned to candidate scaffold roles "
            "for stand universe, THLB/NTHLB state, retained area, "
            "managed/unmanaged area, and group-field source, with explicit "
            "caveats for review-required, deferred, and sensitive-source steps."
        ),
        decision="pass",
        blocker_or_caveat=(
            "P9RF may support P11.3 candidate-manifest work only; proposed WHA, "
            "uneconomic, archaeology, research-site, big-tree, karst, TUS, and "
            "future stand-level reserve caveats remain visible and do not imply "
            "runtime or release acceptance."
        ),
        next_action_owner="P11.3 candidate manifest source/THLB caveat fields",
    ),
    "p11_gate_03_curve_handoff": GateSpec(
        gate_id="p11_gate_03_curve_handoff",
        source_artifact_path="planning/tfl6_mp11_phase10r_curve_rebuild_closeout.md",
        required_promotion_state="accepted_model_contract",
        actual_promotion_state="accepted_phase11_curve_handoff_not_model_input",
        required_qa_evidence=(
            "All 27 Table 57 managed curves are accounted for, including 25 BTC "
            "generated rows and 2 canonical AU curve-reuse rows."
        ),
        decision="pass",
        blocker_or_caveat=(
            "Curves remain not_model_input until P11.3 materializes explicit "
            "model-input curve tables."
        ),
        next_action_owner="P11.3 curve table candidate manifest",
    ),
    "p11_gate_04_deferred_tables_54_55": GateSpec(
        gate_id="p11_gate_04_deferred_tables_54_55",
        source_artifact_path="planning/tfl6_mp11_phase10r_curve_rebuild_closeout.md",
        required_promotion_state="deferred",
        actual_promotion_state="deferred_missing_public_safe_au_mapping",
        required_qa_evidence=(
            "Tables 54/55 existing and recent managed rows remain excluded unless "
            "a public-safe AU-code mapping is reviewed and accepted."
        ),
        decision="pass",
        blocker_or_caveat=(
            "This gate passes only as an exclusion rule; P11.3 must not consume "
            "Tables 54/55 directly."
        ),
        next_action_owner="Future public-safe AU mapping issue",
    ),
    "p11_gate_05_figure_evidence": GateSpec(
        gate_id="p11_gate_05_figure_evidence",
        source_artifact_path="planning/tfl6_mp11_baseline_and_promotion_contract.md",
        required_promotion_state="accepted_model_contract_or_excluded",
        actual_promotion_state="excluded_from_model_input",
        required_qa_evidence=(
            "Figure-derived values are limited to comparison/planning roles "
            "unless separately promoted through a model-contract decision."
        ),
        decision="pass",
        blocker_or_caveat=(
            "P11.3 must not use comparison-only or planning-only figure values as "
            "model-input fields."
        ),
        next_action_owner="P11.3 field-source filter",
    ),
    "p11_gate_06_rule_contracts": GateSpec(
        gate_id="p11_gate_06_rule_contracts",
        source_artifact_path="planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md",
        required_promotion_state="accepted_candidate_scaffold_contract",
        actual_promotion_state="accepted_candidate_scaffold_with_deferred_rule_fields",
        required_qa_evidence=(
            "Treatment and transition defaults reuse Phase 5 scaffold behavior; "
            "MP11 MHA, helicopter economic operability, harvest-system assignment, "
            "and scenario-policy fields are excluded from accepted model input "
            "unless separately promoted."
        ),
        decision="pass",
        blocker_or_caveat=(
            "Rule fields may appear in P11.3 only as null, deferred, comparison, "
            "proxy, QA, or unavailable metadata; this is not MP11 runtime-rule "
            "acceptance."
        ),
        next_action_owner="P11.3 candidate manifest rule-status fields",
    ),
    "p11_gate_07_schema_bridge": GateSpec(
        gate_id="p11_gate_07_schema_bridge",
        source_artifact_path="planning/tfl6_mp11_p11_2_candidate_schema_bridge.md",
        required_promotion_state="accepted_candidate_schema_bridge",
        actual_promotion_state="accepted_candidate_schema_bridge_manifest_only",
        required_qa_evidence=(
            "P11.2 names candidate table roles and whether they reuse, replace, "
            "extend, or defer the Phase 5 schema/export bridge."
        ),
        decision="pass",
        blocker_or_caveat=(
            "P11.3 may build a candidate manifest from the bridge, but generated "
            "tables still require explicit P11.3 authorization and MP11 candidate "
            "paths."
        ),
        next_action_owner="P11.3 candidate model-input manifest",
    ),
    "p11_gate_08_private_data": GateSpec(
        gate_id="p11_gate_08_private_data",
        source_artifact_path="planning/tfl6_mp11_baseline_and_promotion_contract.md",
        required_promotion_state="unavailable_non_public_or_public_proxy",
        actual_promotion_state="unavailable_non_public_or_proxy_only",
        required_qa_evidence=(
            "WFP LBB, ITI, LEFI, objective weights, and unpublished model internals "
            "are explicitly marked unavailable, proxy-only, sensitivity-only, or "
            "deferred."
        ),
        decision="pass",
        blocker_or_caveat=(
            "P11.3 must not infer private stand-level data from aggregate public "
            "MP11 summaries."
        ),
        next_action_owner="P11.3 private-data exclusion check",
    ),
    "p11_gate_09_kpi_reporting": GateSpec(
        gate_id="p11_gate_09_kpi_reporting",
        source_artifact_path="planning/tfl6_mp11_kpi_qa_reporting_contract.md",
        required_promotion_state="classified_by_downstream_role",
        actual_promotion_state="comparison_and_reporting_contract_only",
        required_qa_evidence=(
            "KPI/reporting targets must be separated into model-input, XML/report, "
            "runtime, docs, or comparison-only roles."
        ),
        decision="deferred",
        blocker_or_caveat=(
            "Runtime-only and docs-only reporting can defer to Phases 12/13 if "
            "P11.3 records that candidate table generation does not require them."
        ),
        next_action_owner="P11.3 candidate manifest non-blocking KPI deferral",
    ),
    "p11_gate_10_xml_readiness": GateSpec(
        gate_id="p11_gate_10_xml_readiness",
        source_artifact_path="planning/tfl6_mp11_phase11_artifact_layout.json",
        required_promotion_state="candidate_manifest_required_before_xml",
        actual_promotion_state="deferred_until_p11_3_candidate_manifest",
        required_qa_evidence=(
            "P11.4 XML readiness depends on P11.3 candidate model-input manifest "
            "or an explicit stop report."
        ),
        decision="deferred",
        blocker_or_caveat=(
            "XML readiness cannot be decided until P11.3 either writes the "
            "candidate manifest or remains blocked."
        ),
        next_action_owner="P11.4 XML readiness manifest",
    ),
    "p11_gate_11_runtime_boundary": GateSpec(
        gate_id="p11_gate_11_runtime_boundary",
        source_artifact_path="planning/tfl6_mp11_phase11_artifact_layout.json",
        required_promotion_state="phase12_or_later",
        actual_promotion_state="phase12_or_later",
        required_qa_evidence=(
            "Matrix Builder and Patchworks runtime checks are assigned to Phase 12 "
            "unless P11.4 defines a parse-only XML check."
        ),
        decision="pass",
        blocker_or_caveat=(
            "P11.2/P11.3 must not run Matrix Builder or Patchworks runtime."
        ),
        next_action_owner="Phase 12 runtime handoff",
    ),
}


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _load_gate_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def build_readiness_records(
    gates_csv: Path = DEFAULT_GATES_CSV,
) -> tuple[list[ReadinessRecord], dict[str, Any]]:
    gate_rows = _load_gate_rows(gates_csv)
    records: list[ReadinessRecord] = []
    missing_specs = sorted(
        set(row["gate_id"] for row in gate_rows).difference(GATE_SPECS)
    )
    if missing_specs:
        raise RuntimeError(f"Missing P11.2 gate specs: {', '.join(missing_specs)}")
    for row in gate_rows:
        spec = GATE_SPECS[row["gate_id"]]
        source_path = INSTANCE_ROOT / spec.source_artifact_path
        records.append(
            ReadinessRecord(
                gate_id=spec.gate_id,
                gate_type=row["gate_type"],
                target_role=row["target_role"],
                source_artifact_path=spec.source_artifact_path,
                source_exists=source_path.exists(),
                required_promotion_state=spec.required_promotion_state,
                actual_promotion_state=spec.actual_promotion_state,
                required_qa_evidence=spec.required_qa_evidence,
                decision=spec.decision,
                blocker_or_caveat=spec.blocker_or_caveat,
                next_action_owner=spec.next_action_owner,
            )
        )
    decision_counts = _counts(records, "decision")
    gate_type_counts = _counts(records, "gate_type")
    payload = {
        "schema_version": 1,
        "phase": "P11.2",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "generator": _repo_relative(Path(__file__).resolve()),
        "input_gates_csv": _repo_relative(gates_csv),
        "row_count": len(records),
        "decision_counts": decision_counts,
        "gate_type_counts": gate_type_counts,
        "blocked_hard_gate_count": sum(
            record.gate_type == "hard" and record.decision == "blocked"
            for record in records
        ),
        "source_missing_count": sum(not record.source_exists for record in records),
        "p11_3_unlock_status": "blocked"
        if any(
            record.gate_type == "hard" and record.decision == "blocked"
            for record in records
        )
        else "candidate_manifest_eligible",
        "scope_boundary": (
            "This audit writes planning readiness records only. It does not "
            "generate model-input tables, ForestModel XML, Matrix Builder "
            "outputs, or Patchworks runtime artifacts."
        ),
        "records": [asdict(record) for record in records],
    }
    return records, payload


def _counts(records: list[ReadinessRecord], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(getattr(record, field))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _write_csv(path: Path, records: list[ReadinessRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def _markdown_table(records: list[ReadinessRecord]) -> str:
    columns = [
        "gate_id",
        "gate_type",
        "target_role",
        "actual_promotion_state",
        "decision",
        "next_action_owner",
    ]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for record in records:
        row = asdict(record)
        values = [str(row[column]).replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _write_markdown(
    path: Path, records: list[ReadinessRecord], payload: dict[str, Any]
) -> None:
    blocked = [
        record
        for record in records
        if record.gate_type == "hard" and record.decision == "blocked"
    ]
    lines = [
        "# TFL 6 MP11 Model-Input Promotion Readiness",
        "",
        "## Purpose",
        "",
        "This P11.2 audit classifies whether MP11 source, THLB, curve, rule,",
        "schema, reporting, private-data, XML, and runtime boundaries are ready",
        "for model-input promotion. It is a planning manifest only.",
        "",
        "## Summary",
        "",
        f"- Rows: `{payload['row_count']}`",
        f"- Decision counts: `{json.dumps(payload['decision_counts'], sort_keys=True)}`",
        f"- Blocked hard gates: `{payload['blocked_hard_gate_count']}`",
        f"- P11.3 unlock status: `{payload['p11_3_unlock_status']}`",
        "",
        "## Gate Decisions",
        "",
        _markdown_table(records),
        "",
        "## Blocked Hard Gates",
        "",
    ]
    if blocked:
        for record in blocked:
            lines.extend(
                [
                    f"### `{record.gate_id}`",
                    "",
                    f"- Target role: {record.target_role}",
                    f"- Source: `{record.source_artifact_path}`",
                    f"- Actual state: `{record.actual_promotion_state}`",
                    f"- Blocker: {record.blocker_or_caveat}",
                    f"- Next action: {record.next_action_owner}",
                    "",
                ]
            )
    else:
        lines.append("- No hard gates are blocked.")
        lines.append("")
    lines.extend(
        [
            "## Use Boundary",
            "",
            "- This manifest does not generate model-input bundle tables.",
            "- This manifest does not generate ForestModel XML.",
            "- This manifest does not run Matrix Builder or Patchworks runtime.",
            "- P11.3 may start only if all hard gates pass after maintainer review.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_outputs(
    records: list[ReadinessRecord],
    payload: dict[str, Any],
    *,
    output_csv: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    _write_csv(output_csv, records)
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, records, payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gates-csv", type=Path, default=DEFAULT_GATES_CSV)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build and print the summary without writing readiness outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records, payload = build_readiness_records(args.gates_csv)
    if not args.dry_run:
        write_outputs(
            records,
            payload,
            output_csv=args.output_csv,
            output_json=args.output_json,
            output_md=args.output_md,
        )
    print(
        json.dumps({key: payload[key] for key in payload if key != "records"}, indent=2)
    )


if __name__ == "__main__":
    main()
