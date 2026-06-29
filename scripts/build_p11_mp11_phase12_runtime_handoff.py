"""Build the P11.5 Phase 12 runtime handoff package."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE_SUMMARY_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_candidate_bundle_build_summary.json"
)
DEFAULT_XML_READINESS_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_readiness.json"
)
DEFAULT_XML_QA_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_generation_qa.json"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase12_runtime_handoff.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase12_runtime_handoff.json"
)
DEFAULT_OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_phase12_runtime_handoff.md"

GENERATED_INPUTS = {
    "candidate_bundle_root": INSTANCE_ROOT / "data" / "mp11_model_input_bundle",
    "candidate_export_bridge": (
        INSTANCE_ROOT / "data" / "mp11_model_input_bundle" / "export_compat"
    ),
    "candidate_export_bridge_manifest": (
        INSTANCE_ROOT
        / "data"
        / "mp11_model_input_bundle"
        / "export_compat"
        / "bridge_manifest.json"
    ),
    "candidate_export_checkpoint": (
        INSTANCE_ROOT
        / "data"
        / "mp11_model_input_bundle"
        / "export_compat"
        / "aflb_current_export_compat.feather"
    ),
    "candidate_forestmodel_xml": (
        INSTANCE_ROOT / "output" / "patchworks_tfl6_mp11_candidate" / "forestmodel.xml"
    ),
    "candidate_fragments": (
        INSTANCE_ROOT
        / "output"
        / "patchworks_tfl6_mp11_candidate"
        / "fragments"
        / "fragments.shp"
    ),
}


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required handoff input not found: {_repo_relative(path)}"
        )
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _generated_input_status() -> dict[str, dict[str, Any]]:
    status: dict[str, dict[str, Any]] = {}
    for key, path in GENERATED_INPUTS.items():
        exists = path.exists()
        status[key] = {
            "path": _repo_relative(path),
            "exists": exists,
            "bytes": path.stat().st_size if exists and path.is_file() else None,
        }
    return status


def _handoff_rows() -> list[dict[str, str]]:
    return [
        {
            "handoff_item": "matrix_builder_input_xml",
            "path": "output/patchworks_tfl6_mp11_candidate/forestmodel.xml",
            "phase12_owner": "P12.2",
            "status": "ready_for_matrix_builder_candidate",
            "caveat": "Candidate scaffold XML; not final MP11 release truth.",
        },
        {
            "handoff_item": "matrix_builder_fragments",
            "path": "output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp",
            "phase12_owner": "P12.2",
            "status": "ready_for_matrix_builder_candidate",
            "caveat": "Fragments inherit Phase 5 stand universe and P9RF/source caveats.",
        },
        {
            "handoff_item": "candidate_bundle",
            "path": "data/mp11_model_input_bundle/",
            "phase12_owner": "P12.1",
            "status": "generated_candidate_scaffold",
            "caveat": "Generated and ignored; tracked summaries carry compact provenance.",
        },
        {
            "handoff_item": "candidate_export_bridge",
            "path": "data/mp11_model_input_bundle/export_compat/",
            "phase12_owner": "P12.2",
            "status": "ready_for_exporter_runtime_bridge",
            "caveat": "Bridge is deterministic numeric compatibility surface for FEMIC exporter.",
        },
        {
            "handoff_item": "matrix_builder_tracks_root",
            "path": "models/tfl6_patchworks_model_mp11_candidate/tracks/",
            "phase12_owner": "P12.2",
            "status": "not_started_phase12",
            "caveat": "Do not create until Matrix Builder runs in Phase 12.",
        },
        {
            "handoff_item": "runtime_package_root",
            "path": "models/tfl6_patchworks_model_mp11_candidate/",
            "phase12_owner": "P12.3",
            "status": "not_started_phase12",
            "caveat": "Runtime assembly, launch surfaces, and topology are Phase 12 work.",
        },
        {
            "handoff_item": "scenario_smoke",
            "path": "models/tfl6_patchworks_model_mp11_candidate/analysis/",
            "phase12_owner": "P12.4-P12.5",
            "status": "not_started_phase12",
            "caveat": "Direct launch and scenario smoke must follow Matrix Builder/runtime assembly.",
        },
    ]


def _write_outputs(
    *,
    payload: dict[str, Any],
    rows: list[dict[str, str]],
    output_csv: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    lines = [
        "# P11.5 Phase 12 Runtime Handoff",
        "",
        "This handoff packages the generated MP11 candidate model-input/XML "
        "surfaces for Phase 12 Matrix Builder and runtime smoke work.",
        "",
        "P11.5 does not run Matrix Builder, assemble a Patchworks runtime, run "
        "scenario smoke, or publish a release archive.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            "",
            "## Phase 12 Inputs",
            "",
            "| Item | Path | Phase 12 owner | Status | Caveat |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"`{row['handoff_item']}` | "
            f"`{row['path']}` | "
            f"`{row['phase12_owner']}` | "
            f"`{row['status']}` | "
            f"{row['caveat']} |"
        )

    lines.extend(
        [
            "",
            "## Required Phase 12 Sequence",
            "",
            "1. Launch P12.1 with child issues for Matrix Builder, runtime assembly, "
            "direct launch smoke, scenario smoke, and closeout.",
            "2. Run Matrix Builder from "
            "`output/patchworks_tfl6_mp11_candidate/forestmodel.xml` and "
            "`output/patchworks_tfl6_mp11_candidate/fragments/`.",
            "3. Inspect generated tracks before runtime claims: accounts, "
            "protoaccounts, features, products, curves, blocks, and treatment/group "
            "signals.",
            "4. Assemble the candidate runtime under "
            "`models/tfl6_patchworks_model_mp11_candidate/`.",
            "5. Run direct launch smoke and representative scenario smoke before any "
            "Phase 13 release/docs QA claim.",
            "",
            "## Candidate Caveats",
            "",
            "- This is a candidate scaffold, not a final MP11 release model.",
            "- The Phase 5 stand universe and treatment/transition scaffold are reused.",
            "- P9RF source/THLB caveats remain visible until a later source-layer "
            "rebuild replaces the scaffold.",
            "- The accepted 27 Phase 10R Table 57 rows materialize as 18 active MP11 "
            "candidate curves because duplicate rows map to already-selected "
            "canonical AU identities.",
            "- Tables 54/55 remain excluded until a public-safe AU-code mapping exists.",
            "- Harvest-system assignment remains deferred comparison metadata, not a "
            "stand-level treatment classifier.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_handoff(
    *,
    bundle_summary_json: Path = DEFAULT_BUNDLE_SUMMARY_JSON,
    xml_readiness_json: Path = DEFAULT_XML_READINESS_JSON,
    xml_qa_json: Path = DEFAULT_XML_QA_JSON,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    bundle_summary = _load_json(bundle_summary_json)
    xml_readiness = _load_json(xml_readiness_json)
    xml_qa = _load_json(xml_qa_json)
    generated_inputs = _generated_input_status()
    missing_inputs = [
        record["path"] for record in generated_inputs.values() if not record["exists"]
    ]
    if missing_inputs:
        raise FileNotFoundError(
            "Phase 12 handoff inputs are missing: " + "; ".join(missing_inputs)
        )

    bundle = bundle_summary["summary"]
    readiness = xml_readiness["summary"]
    qa = xml_qa["summary"]
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "handoff_status": "phase12_runtime_handoff_ready",
        "candidate_bundle_root": bundle["candidate_bundle_root"],
        "active_mp11_curve_count": bundle["active_mp11_curve_count"],
        "duplicate_mp11_rows_deferred_by_canonical_au": bundle[
            "duplicate_mp11_rows_deferred_by_canonical_au"
        ],
        "xml_readiness_ready_count": readiness["ready_count"],
        "xml_readiness_blocked_count": readiness["blocked_count"],
        "xml_path": qa["xml_path"],
        "xml_curve_nodes": qa["xml_curve_nodes"],
        "fragment_rows": qa["fragment_rows"],
        "fragment_area_ha": qa["fragment_area_ha"],
        "matrix_builder": "not_performed",
        "runtime_bundle_generation": "not_performed",
        "scenario_smoke": "not_performed",
        "release_qa": "not_performed",
    }
    rows = _handoff_rows()
    payload = {
        "summary": summary,
        "generated_inputs": generated_inputs,
        "handoff_rows": rows,
        "source_manifests": {
            "bundle_summary_json": _repo_relative(bundle_summary_json),
            "xml_readiness_json": _repo_relative(xml_readiness_json),
            "xml_qa_json": _repo_relative(xml_qa_json),
        },
    }
    _write_outputs(
        payload=payload,
        rows=rows,
        output_csv=output_csv,
        output_json=output_json,
        output_md=output_md,
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-summary-json", type=Path, default=DEFAULT_BUNDLE_SUMMARY_JSON
    )
    parser.add_argument(
        "--xml-readiness-json", type=Path, default=DEFAULT_XML_READINESS_JSON
    )
    parser.add_argument("--xml-qa-json", type=Path, default=DEFAULT_XML_QA_JSON)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_handoff(
        bundle_summary_json=args.bundle_summary_json,
        xml_readiness_json=args.xml_readiness_json,
        xml_qa_json=args.xml_qa_json,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
