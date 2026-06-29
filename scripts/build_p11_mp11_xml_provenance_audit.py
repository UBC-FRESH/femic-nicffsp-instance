"""Audit Phase 5 ForestModel XML provenance for P11.4a."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE_REVIEW_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_model_input_candidate_provenance_review.csv"
)
DEFAULT_PHASE5_INVENTORY_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_phase5_provenance_inventory.csv"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_xml_provenance_audit.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_xml_provenance_audit.json"
)
DEFAULT_OUTPUT_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_xml_provenance_audit.md"
)
BASELINE_XML = (
    INSTANCE_ROOT / "output" / "patchworks_tfl6_validated" / "forestmodel.xml"
)
BASELINE_FRAGMENT_GLOB = (
    INSTANCE_ROOT / "output" / "patchworks_tfl6_validated" / "fragments" / "fragments.*"
)
PHASE5_BRIDGE_NOTE = (
    INSTANCE_ROOT / "planning" / "tfl6_forestmodel_xml_export_bridge.md"
)
PHASE5_BLOCKER_NOTE = (
    INSTANCE_ROOT / "planning" / "tfl6_forestmodel_xml_export_blocker.md"
)
ARTIFACT_LAYOUT_NOTE = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_artifact_layout.md"
)


@dataclass(frozen=True)
class XmlAuditRecord:
    """P11.4a audit row for one XML/component family."""

    component_family: str
    source_role: str
    phase5_surface: str
    mp11_candidate_source: str
    p11_4a_action: str
    baseline_artifacts: str
    required_p11_4b_check: str
    blocker_status: str
    notes: str


COMPONENT_POLICIES: tuple[XmlAuditRecord, ...] = (
    XmlAuditRecord(
        component_family="stand_universe_fragments",
        source_role="stand_table",
        phase5_surface="forestmodel_fragments",
        mp11_candidate_source="P9RF candidate stand/source/THLB scaffold",
        p11_4a_action="replace_after_readiness",
        baseline_artifacts="output/patchworks_tfl6_validated/fragments/fragments.*",
        required_p11_4b_check=(
            "Confirm candidate stand universe, THLB/NTHLB state, retained area, "
            "managed/unmanaged area, and group caveats before fragment export."
        ),
        blocker_status="p11_4b_required",
        notes="Phase 5 fragments remain protected until MP11 candidate export passes.",
    ),
    XmlAuditRecord(
        component_family="export_compat_bridge",
        source_role="export_compat_bridge",
        phase5_surface="export_bridge_manifest",
        mp11_candidate_source="MP11 candidate numeric/string bridge",
        p11_4a_action="replace_after_readiness",
        baseline_artifacts="data/model_input_bundle/export_compat/bridge_manifest.json",
        required_p11_4b_check=(
            "Require deterministic AU/curve ID bridge and accepted candidate "
            "bundle paths before XML generation."
        ),
        blocker_status="p11_4b_required",
        notes="The old P4.2 blocker proves the generic exporter needs a bridge.",
    ),
    XmlAuditRecord(
        component_family="curve_definitions",
        source_role="curve_table; curve_points_table",
        phase5_surface="forestmodel_xml",
        mp11_candidate_source="accepted Phase 10R Table 57 curves plus retained natural curves",
        p11_4a_action="replace_after_readiness",
        baseline_artifacts="output/patchworks_tfl6_validated/forestmodel.xml",
        required_p11_4b_check=(
            "Map every candidate curve ID to XML curve definitions and verify "
            "Tables 54/55 remain excluded."
        ),
        blocker_status="p11_4b_required",
        notes="Phase 10R curve handoff is accepted, but XML curve wiring still needs readiness.",
    ),
    XmlAuditRecord(
        component_family="au_selects_and_assignments",
        source_role="au_table; stand_au_assignment; stand_origin_assignment",
        phase5_surface="forestmodel_xml",
        mp11_candidate_source="Phase 5 scaffold with MP11 candidate AU/curve provenance",
        p11_4a_action="extend_or_reuse_after_readiness",
        baseline_artifacts="output/patchworks_tfl6_validated/forestmodel.xml",
        required_p11_4b_check=(
            "Verify candidate AU, origin, and stand-AU assignment fields can "
            "produce complete XML selects without unmapped stands."
        ),
        blocker_status="p11_4b_required",
        notes="Existing XML has Phase 5 select/assignment structure, not MP11 candidate truth.",
    ),
    XmlAuditRecord(
        component_family="treatments",
        source_role="treatment_table",
        phase5_surface="forestmodel_xml",
        mp11_candidate_source="Phase 5 generic treatment defaults with MP11 rule caveats",
        p11_4a_action="reuse_with_caveats",
        baseline_artifacts="output/patchworks_tfl6_validated/forestmodel.xml",
        required_p11_4b_check=(
            "Confirm generic treatment reuse is explicit and MP11 MHA, "
            "harvest-system, and scenario rules remain deferred metadata."
        ),
        blocker_status="p11_4b_required",
        notes="Generic CC treatment can be a candidate scaffold, not final MP11 equivalence.",
    ),
    XmlAuditRecord(
        component_family="transitions",
        source_role="transition_table",
        phase5_surface="forestmodel_xml",
        mp11_candidate_source="Phase 5 transition defaults with MP11 transition caveats",
        p11_4a_action="reuse_with_caveats",
        baseline_artifacts="output/patchworks_tfl6_validated/forestmodel.xml",
        required_p11_4b_check=(
            "Confirm transition reuse is explicit and any MP11 transition fields "
            "remain deferred unless separately promoted."
        ),
        blocker_status="p11_4b_required",
        notes="Transition defaults are scaffold rules only.",
    ),
    XmlAuditRecord(
        component_family="harvest_system_rules",
        source_role="harvest_system_table",
        phase5_surface="model_input_bundle",
        mp11_candidate_source="deferred comparison metadata",
        p11_4a_action="defer_not_xml_input",
        baseline_artifacts="data/model_input_bundle/harvest_system_table.csv",
        required_p11_4b_check=(
            "Verify no candidate XML treatment or report depends on stand-level "
            "harvest-system assignments."
        ),
        blocker_status="non_blocking_deferred",
        notes="P11.3c keeps harvest-system assignments out of generated model-input tables.",
    ),
    XmlAuditRecord(
        component_family="reporting_groups",
        source_role="group_table; cedar_signal_table; embedded_identity_table",
        phase5_surface="forestmodel_xml",
        mp11_candidate_source="Phase 5 reporting scaffold plus MP11 candidate caveat fields",
        p11_4a_action="extend_after_readiness",
        baseline_artifacts="output/patchworks_tfl6_validated/forestmodel.xml",
        required_p11_4b_check=(
            "Verify which reporting groups are XML-facing, which remain "
            "Matrix/QA-facing, and which MP11 cedar/caveat signals are metadata only."
        ),
        blocker_status="p11_4b_required",
        notes="Cedar and caveat signals must not become hidden model constraints.",
    ),
)


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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_xml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Baseline XML not found: {_repo_relative(path)}")
    root = ET.parse(path).getroot()
    tag_counts = Counter(element.tag for element in root.iter())
    return {
        "path": _repo_relative(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "root_tag": root.tag,
        "root_attributes": dict(root.attrib),
        "tag_counts": dict(sorted(tag_counts.items())),
    }


def _baseline_fragments() -> list[dict[str, Any]]:
    fragment_paths = sorted(
        BASELINE_FRAGMENT_GLOB.parent.glob(BASELINE_FRAGMENT_GLOB.name)
    )
    if not fragment_paths:
        raise FileNotFoundError("No Phase 5 baseline fragments found.")
    return [
        {
            "path": _repo_relative(path),
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in fragment_paths
    ]


def _required_notes() -> dict[str, bool]:
    paths = {
        "phase5_export_bridge_note": PHASE5_BRIDGE_NOTE,
        "phase5_export_blocker_note": PHASE5_BLOCKER_NOTE,
        "artifact_layout_note": ARTIFACT_LAYOUT_NOTE,
    }
    return {name: path.exists() for name, path in paths.items()}


def _candidate_review_summary(rows: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        decision = row.get("p11_3c_decision", "")
        counts[decision] = counts.get(decision, 0) + 1
    return counts


def _write_csv(path: Path, records: tuple[XmlAuditRecord, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_json(
    path: Path,
    *,
    records: tuple[XmlAuditRecord, ...],
    summary: dict[str, Any],
    baseline_xml: dict[str, Any],
    baseline_fragments: list[dict[str, Any]],
    phase5_inventory_rows: int,
    candidate_review_counts: dict[str, int],
    required_notes: dict[str, bool],
) -> None:
    payload = {
        "summary": summary,
        "inputs": {
            "candidate_review_csv": _repo_relative(DEFAULT_CANDIDATE_REVIEW_CSV),
            "phase5_inventory_csv": _repo_relative(DEFAULT_PHASE5_INVENTORY_CSV),
        },
        "required_notes": required_notes,
        "phase5_inventory_rows": phase5_inventory_rows,
        "candidate_review_counts": candidate_review_counts,
        "baseline_xml": baseline_xml,
        "baseline_fragments": baseline_fragments,
        "records": [asdict(record) for record in records],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_markdown(
    path: Path,
    *,
    output_csv: Path,
    output_json: Path,
    records: tuple[XmlAuditRecord, ...],
    summary: dict[str, Any],
    baseline_xml: dict[str, Any],
    baseline_fragments: list[dict[str, Any]],
    required_notes: dict[str, bool],
) -> None:
    lines = [
        "# P11.4a MP11 ForestModel XML Provenance Audit",
        "",
        "This audit records the Phase 5 ForestModel XML/fragments provenance and "
        "the MP11 candidate bridge treatment before P11.4b builds an XML "
        "readiness manifest or stop report.",
        "",
        "P11.4a does not generate model-input tables, ForestModel XML, Matrix "
        "Builder outputs, or Patchworks runtime artifacts.",
        "",
        "## Outputs",
        "",
        f"- Audit CSV: `{_repo_relative(output_csv)}`",
        f"- Audit JSON: `{_repo_relative(output_json)}`",
        "",
        "## Baseline XML Evidence",
        "",
        f"- Baseline XML: `{baseline_xml['path']}`",
        f"- SHA256: `{baseline_xml['sha256']}`",
        f"- Root: `{baseline_xml['root_tag']}`",
        f"- Year / horizon: `{baseline_xml['root_attributes'].get('year')}` / "
        f"`{baseline_xml['root_attributes'].get('horizon')}`",
        f"- Fragment sidecar files: `{len(baseline_fragments)}`",
        "",
        "## Required Notes",
        "",
        "| Note | Present |",
        "| --- | --- |",
    ]
    for name, present in required_notes.items():
        lines.append(f"| `{name}` | `{str(present).lower()}` |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- XML/component families audited: `{summary['component_count']}`",
            f"- P11.4b-required families: `{summary['p11_4b_required_count']}`",
            f"- Non-blocking deferred families: `{summary['non_blocking_deferred_count']}`",
            f"- P11.4a unlock status: `{summary['p11_4a_unlock_status']}`",
            "- Model-input generation: `not_performed`",
            "- ForestModel XML generation: `not_performed`",
            "- Matrix Builder: `not_performed`",
            "- Runtime bundle generation: `not_performed`",
            "",
            "## Component Audit",
            "",
            "| Component | Source role | Action | Blocker status | P11.4b check |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        lines.append(
            "| "
            f"`{record.component_family}` | "
            f"`{record.source_role}` | "
            f"`{record.p11_4a_action}` | "
            f"`{record.blocker_status}` | "
            f"{record.required_p11_4b_check} |"
        )

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "P11.4b may now build an XML readiness manifest from these audited "
            "component families. P11.4a itself does not authorize XML writes. "
            "Candidate XML generation remains reserved for P11.4c after P11.4b "
            "confirms the component readiness and generation contract.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def build_audit(
    *,
    candidate_review_csv: Path = DEFAULT_CANDIDATE_REVIEW_CSV,
    phase5_inventory_csv: Path = DEFAULT_PHASE5_INVENTORY_CSV,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    candidate_review = _read_csv(candidate_review_csv)
    phase5_inventory = _read_csv(phase5_inventory_csv)
    required_notes = _required_notes()
    baseline_xml = _parse_xml(BASELINE_XML)
    baseline_fragments = _baseline_fragments()
    records = COMPONENT_POLICIES
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "component_count": len(records),
        "p11_4b_required_count": sum(
            record.blocker_status == "p11_4b_required" for record in records
        ),
        "non_blocking_deferred_count": sum(
            record.blocker_status == "non_blocking_deferred" for record in records
        ),
        "missing_required_note_count": sum(
            not present for present in required_notes.values()
        ),
        "p11_4a_unlock_status": (
            "p11_4b_readiness_eligible"
            if all(required_notes.values())
            else "blocked_missing_phase5_notes"
        ),
        "model_input_generation": "not_performed",
        "xml_generation": "not_performed",
        "matrix_builder": "not_performed",
        "runtime_bundle_generation": "not_performed",
    }

    _write_csv(output_csv, records)
    _write_json(
        output_json,
        records=records,
        summary=summary,
        baseline_xml=baseline_xml,
        baseline_fragments=baseline_fragments,
        phase5_inventory_rows=len(phase5_inventory),
        candidate_review_counts=_candidate_review_summary(candidate_review),
        required_notes=required_notes,
    )
    _write_markdown(
        output_md,
        output_csv=output_csv,
        output_json=output_json,
        records=records,
        summary=summary,
        baseline_xml=baseline_xml,
        baseline_fragments=baseline_fragments,
        required_notes=required_notes,
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate-review-csv", type=Path, default=DEFAULT_CANDIDATE_REVIEW_CSV
    )
    parser.add_argument(
        "--phase5-inventory-csv", type=Path, default=DEFAULT_PHASE5_INVENTORY_CSV
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_audit(
        candidate_review_csv=args.candidate_review_csv,
        phase5_inventory_csv=args.phase5_inventory_csv,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
