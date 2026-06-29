"""Build the Phase 11 MP11 model-input candidate manifest."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_READINESS_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_promotion_readiness.json"
)
DEFAULT_SCHEMA_BRIDGE_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_p11_2_candidate_schema_bridge.csv"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_manifest.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_manifest.json"
)
DEFAULT_OUTPUT_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_manifest.md"
)


@dataclass(frozen=True)
class RolePolicy:
    """Manifest policy for one candidate model-input table role."""

    source_artifacts: str
    candidate_output_path: str
    required_caveat_fields: str
    fallback_or_exclusion_policy: str
    downstream_status: str
    generation_eligibility: str


@dataclass(frozen=True)
class CandidateRecord:
    """P11.3 candidate manifest row."""

    table_role: str
    bridge_action: str
    p11_3_candidate_source: str
    source_artifacts: str
    candidate_output_path: str
    required_caveat_fields: str
    fallback_or_exclusion_policy: str
    downstream_status: str
    generation_eligibility: str
    candidate_output_policy: str


ROLE_POLICIES: dict[str, RolePolicy] = {
    "stand_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md; "
            "planning/tfl6_mp11_p9rf_table12_resultant_vs_p9r_comparison.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/stand_table.csv",
        required_caveat_fields=(
            "p9rf_step_status; p9rf_current_thlb_delta_ha; "
            "sensitive_source_exclusion; deferred_public_source"
        ),
        fallback_or_exclusion_policy=(
            "Use P9RF resultant-fragment source/THLB candidate only; preserve "
            "review-required and deferred step caveats."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "au_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_p11_2_candidate_schema_bridge.md; "
            "planning/tfl6_mp11_phase10r_curve_rebuild_closeout.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/au_table.csv",
        required_caveat_fields="phase10r_curve_handoff_status; table54_55_exclusion",
        fallback_or_exclusion_policy=(
            "Extend Phase 5 AU scaffold with accepted Phase 10R Table 57 "
            "curve-handoff targets; keep Tables 54/55 excluded."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "curve_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_phase10r_curve_rebuild_closeout.md; "
            "planning/tfl6_mp11_managed_curve_comparison.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/curve_table.csv",
        required_caveat_fields="phase10r_curve_status; not_model_input_until_generated",
        fallback_or_exclusion_policy=(
            "Use accepted 27 Phase 10R Table 57 managed curves and retained "
            "natural curves; exclude Tables 54/55."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "curve_points_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_managed_curves.json; "
            "planning/tfl6_mp11_natural_curve_diagnostics.json"
        ),
        candidate_output_path="data/mp11_model_input_bundle/curve_points_table.csv",
        required_caveat_fields="curve_source_family; phase10r_review_status",
        fallback_or_exclusion_policy=(
            "Use accepted Phase 10R managed curve points and retained natural "
            "curve points when generation is later authorized."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "stand_au_assignment": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_p11_2_candidate_schema_bridge.md; "
            "planning/tfl6_mp11_phase11_phase5_provenance_inventory.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/stand_au_assignment.csv",
        required_caveat_fields="phase5_assignment_source; mp11_candidate_provenance",
        fallback_or_exclusion_policy=(
            "Extend Phase 5 assignment scaffold and add MP11 candidate "
            "provenance fields."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "stand_origin_assignment": RolePolicy(
        source_artifacts="planning/tfl6_mp11_phase11_phase5_provenance_inventory.md",
        candidate_output_path="data/mp11_model_input_bundle/stand_origin_assignment.csv",
        required_caveat_fields="origin_source; replacement_review_status",
        fallback_or_exclusion_policy=(
            "Reuse Phase 5 origin scaffold until an MP11 source review replaces it."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "treatment_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md; "
            "planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/treatment_table.csv",
        required_caveat_fields="rule_status; mp11_rule_deferred_reason",
        fallback_or_exclusion_policy=(
            "Reuse Phase 5 treatment defaults; MP11 MHA, harvest-system, and "
            "scenario rules remain deferred metadata."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "transition_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md; "
            "planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/transition_table.csv",
        required_caveat_fields="transition_source; mp11_transition_deferred_reason",
        fallback_or_exclusion_policy=(
            "Reuse Phase 5 transition defaults until MP11 transitions are "
            "separately accepted."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "harvest_system_table": RolePolicy(
        source_artifacts="planning/tfl6_mp11_operability_harvest_mha_scenario_contract.md",
        candidate_output_path="",
        required_caveat_fields="harvest_system_status; unavailable_or_proxy_basis",
        fallback_or_exclusion_policy=(
            "Do not generate stand-level harvest-system assignments; aggregate "
            "MP11 percentages remain comparison targets only."
        ),
        downstream_status="deferred_not_model_input",
        generation_eligibility="deferred_not_eligible",
    ),
    "group_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_p11_2_candidate_scaffold_decisions.md; "
            "planning/tfl6_mp11_kpi_qa_reporting_contract.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/group_table.csv",
        required_caveat_fields="group_source; p9rf_caveat_group; kpi_role",
        fallback_or_exclusion_policy=(
            "Extend Phase 5 reporting groups with candidate caveat groups; "
            "runtime-only KPI reports defer to later phases."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "cedar_signal_table": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_kpi_qa_reporting_contract.md; "
            "planning/tfl6_mp11_baseline_and_promotion_contract.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/cedar_signal_table.csv",
        required_caveat_fields="cedar_signal_source; figure_evidence_status",
        fallback_or_exclusion_policy=(
            "Extend Phase 5 cedar-reporting scaffold with comparison/provenance "
            "fields only; planning-only figures stay out of model inputs."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "embedded_identity_table": RolePolicy(
        source_artifacts="planning/tfl6_mp11_phase11_phase5_provenance_inventory.md",
        candidate_output_path="data/mp11_model_input_bundle/embedded_identity_table.csv",
        required_caveat_fields="identity_source; preservation_status",
        fallback_or_exclusion_policy="Reuse Phase 5 embedded identity scaffold.",
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
    "export_compat_bridge": RolePolicy(
        source_artifacts=(
            "planning/tfl6_mp11_p11_2_candidate_schema_bridge.md; "
            "planning/tfl6_mp11_phase11_artifact_layout.md"
        ),
        candidate_output_path="data/mp11_model_input_bundle/export_compat/bridge_manifest.json",
        required_caveat_fields="bridge_action; phase5_baseline_protection",
        fallback_or_exclusion_policy=(
            "Replace Phase 5 export bridge only if P11.3 later authorizes "
            "generated candidate tables."
        ),
        downstream_status="candidate_manifest_only",
        generation_eligibility="eligible_for_later_generated_scaffold",
    ),
}


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_bridge(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def build_candidate_manifest(
    *,
    readiness_json: Path = DEFAULT_READINESS_JSON,
    schema_bridge_csv: Path = DEFAULT_SCHEMA_BRIDGE_CSV,
) -> tuple[list[CandidateRecord], dict[str, Any]]:
    readiness = _load_json(readiness_json)
    bridge_rows = _load_bridge(schema_bridge_csv)
    missing_policies = sorted(
        set(row["table_role"] for row in bridge_rows).difference(ROLE_POLICIES)
    )
    if missing_policies:
        raise RuntimeError(
            "Missing candidate manifest role policies: " + ", ".join(missing_policies)
        )
    records: list[CandidateRecord] = []
    blocked_hard = int(readiness["blocked_hard_gate_count"])
    for row in bridge_rows:
        policy = ROLE_POLICIES[row["table_role"]]
        generation_eligibility = policy.generation_eligibility
        downstream_status = policy.downstream_status
        if blocked_hard:
            generation_eligibility = "blocked_by_readiness"
            downstream_status = "blocked_stop_report"
        records.append(
            CandidateRecord(
                table_role=row["table_role"],
                bridge_action=row["bridge_action"],
                p11_3_candidate_source=row["p11_3_candidate_source"],
                source_artifacts=policy.source_artifacts,
                candidate_output_path=policy.candidate_output_path,
                required_caveat_fields=policy.required_caveat_fields,
                fallback_or_exclusion_policy=policy.fallback_or_exclusion_policy,
                downstream_status=downstream_status,
                generation_eligibility=generation_eligibility,
                candidate_output_policy=row["candidate_output_policy"],
            )
        )
    payload = {
        "schema_version": 1,
        "phase": "P11.3b",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "generator": _repo_relative(Path(__file__).resolve()),
        "readiness_json": _repo_relative(readiness_json),
        "schema_bridge_csv": _repo_relative(schema_bridge_csv),
        "readiness_unlock_status": readiness["p11_3_unlock_status"],
        "blocked_hard_gate_count": blocked_hard,
        "row_count": len(records),
        "generation_eligibility_counts": _counts(records, "generation_eligibility"),
        "bridge_action_counts": _counts(records, "bridge_action"),
        "candidate_manifest_status": "blocked_stop_report"
        if blocked_hard
        else "candidate_manifest_ready",
        "scope_boundary": (
            "This manifest records candidate table roles only. It does not write "
            "model-input bundle tables, ForestModel XML, Matrix Builder outputs, "
            "or Patchworks runtime artifacts."
        ),
        "records": [asdict(record) for record in records],
    }
    return records, payload


def _counts(records: list[CandidateRecord], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(getattr(record, field))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _write_csv(path: Path, records: list[CandidateRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def _markdown_table(records: list[CandidateRecord]) -> str:
    columns = [
        "table_role",
        "bridge_action",
        "generation_eligibility",
        "downstream_status",
        "candidate_output_path",
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
    path: Path, records: list[CandidateRecord], payload: dict[str, Any]
) -> None:
    lines = [
        "# TFL 6 MP11 Model-Input Candidate Manifest",
        "",
        "## Purpose",
        "",
        "This P11.3b manifest defines candidate model-input table roles, source",
        "artifacts, output paths, caveat fields, and fallback policies. It does",
        "not generate model-input tables, ForestModel XML, Matrix Builder outputs,",
        "or Patchworks runtime artifacts.",
        "",
        "## Summary",
        "",
        f"- Rows: `{payload['row_count']}`",
        f"- Status: `{payload['candidate_manifest_status']}`",
        f"- Readiness unlock status: `{payload['readiness_unlock_status']}`",
        f"- Blocked hard gates: `{payload['blocked_hard_gate_count']}`",
        "- Generation eligibility counts: "
        f"`{json.dumps(payload['generation_eligibility_counts'], sort_keys=True)}`",
        "",
        "## Candidate Table Roles",
        "",
        _markdown_table(records),
        "",
        "## Required Caveats",
        "",
        "- P9RF source/THLB is candidate-scaffold evidence only.",
        "- Tables 54/55 remain excluded without a public-safe AU-code mapping.",
        "- Figure-derived values remain excluded from model-input fields.",
        "- MP11 MHA, harvest-system assignment, helicopter economic operability,",
        "  and scenario policy remain deferred unless separately promoted.",
        "- WFP private dependencies remain unavailable, proxy-only,",
        "  sensitivity-only, or deferred.",
        "",
        "## Use Boundary",
        "",
        "- This manifest may support a later P11.3 generated scaffold decision.",
        "- It does not itself authorize generated model-input tables.",
        "- It does not authorize ForestModel XML generation.",
        "- Matrix Builder and Patchworks runtime remain out of scope.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_outputs(
    records: list[CandidateRecord],
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
    parser.add_argument("--readiness-json", type=Path, default=DEFAULT_READINESS_JSON)
    parser.add_argument(
        "--schema-bridge-csv", type=Path, default=DEFAULT_SCHEMA_BRIDGE_CSV
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build and print the summary without writing candidate manifest outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records, payload = build_candidate_manifest(
        readiness_json=args.readiness_json,
        schema_bridge_csv=args.schema_bridge_csv,
    )
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
