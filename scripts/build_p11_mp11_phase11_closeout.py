"""Build the P11.6 Phase 11 closeout package."""

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
DEFAULT_XML_QA_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_generation_qa.json"
)
DEFAULT_PHASE12_HANDOFF_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_phase12_runtime_handoff.json"
)
DEFAULT_OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_closeout.csv"
DEFAULT_OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_closeout.json"
DEFAULT_OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_phase11_closeout.md"

PHASE11_GENERATED_INPUTS = {
    "candidate_bundle_root": INSTANCE_ROOT / "data" / "mp11_model_input_bundle",
    "candidate_bridge_manifest": (
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

PHASE5_BASELINE_INPUTS = {
    "phase5_bridge_manifest": (
        INSTANCE_ROOT
        / "data"
        / "model_input_bundle"
        / "export_compat"
        / "bridge_manifest.json"
    ),
    "phase5_forestmodel_xml": (
        INSTANCE_ROOT / "output" / "patchworks_tfl6_validated" / "forestmodel.xml"
    ),
}

PHASE12_RUNTIME_OUTPUTS = {
    "matrix_builder_tracks": (
        INSTANCE_ROOT / "models" / "tfl6_patchworks_model_mp11_candidate" / "tracks"
    ),
    "runtime_blocks": (
        INSTANCE_ROOT / "models" / "tfl6_patchworks_model_mp11_candidate" / "blocks"
    ),
    "scenario_smoke": (
        INSTANCE_ROOT
        / "models"
        / "tfl6_patchworks_model_mp11_candidate"
        / "analysis"
        / "headless_runs"
    ),
}


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required closeout input missing: {_repo_relative(path)}"
        )
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _path_status(paths: dict[str, Path]) -> dict[str, dict[str, Any]]:
    status: dict[str, dict[str, Any]] = {}
    for key, path in paths.items():
        exists = path.exists()
        status[key] = {
            "path": _repo_relative(path),
            "exists": exists,
            "bytes": path.stat().st_size if exists and path.is_file() else None,
        }
    return status


def _closeout_rows() -> list[dict[str, str]]:
    return [
        {
            "closeout_item": "candidate_model_input_bundle",
            "status": "built",
            "path": "data/mp11_model_input_bundle/",
            "phase11_result": "Generated candidate scaffold and export bridge.",
            "next_owner": "P12.1-P12.2",
        },
        {
            "closeout_item": "candidate_forestmodel_xml",
            "status": "built",
            "path": "output/patchworks_tfl6_mp11_candidate/forestmodel.xml",
            "phase11_result": "Generated candidate ForestModel XML for Matrix Builder input.",
            "next_owner": "P12.2",
        },
        {
            "closeout_item": "candidate_fragments",
            "status": "built",
            "path": "output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp",
            "phase11_result": "Generated candidate fragments alongside XML.",
            "next_owner": "P12.2",
        },
        {
            "closeout_item": "phase5_baseline",
            "status": "preserved",
            "path": "data/model_input_bundle/ and output/patchworks_tfl6_validated/",
            "phase11_result": "Accepted teaching/runtime baseline was not overwritten.",
            "next_owner": "Phase 13 release decision",
        },
        {
            "closeout_item": "matrix_builder_tracks",
            "status": "not_performed",
            "path": "models/tfl6_patchworks_model_mp11_candidate/tracks/",
            "phase11_result": "Deliberately left for the runtime-build phase.",
            "next_owner": "P12.2",
        },
        {
            "closeout_item": "runtime_bundle",
            "status": "not_performed",
            "path": "models/tfl6_patchworks_model_mp11_candidate/",
            "phase11_result": "Patchworks runtime assembly is not a Phase 11 output.",
            "next_owner": "P12.3",
        },
        {
            "closeout_item": "scenario_smoke",
            "status": "not_performed",
            "path": "models/tfl6_patchworks_model_mp11_candidate/analysis/",
            "phase11_result": "Direct launch and scenario smoke wait for runtime assembly.",
            "next_owner": "P12.4-P12.5",
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
        "# P11.6 Phase 11 Closeout",
        "",
        "Phase 11 is closed as a model-input and ForestModel XML build phase.",
        "It built the MP11 candidate model-input bundle, export bridge,",
        "ForestModel XML, and fragments needed by Phase 12.",
        "",
        "Phase 11 did not run Matrix Builder, assemble a Patchworks runtime,",
        "run scenarios, publish a release archive, or replace the accepted",
        "Phase 5 teaching/runtime baseline.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            "",
            "## Closeout Items",
            "",
            "| Item | Status | Path | Phase 11 result | Next owner |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"`{row['closeout_item']}` | "
            f"`{row['status']}` | "
            f"`{row['path']}` | "
            f"{row['phase11_result']} | "
            f"`{row['next_owner']}` |"
        )

    lines.extend(
        [
            "",
            "## Caveats Carried Forward",
            "",
            "- This is an MP11 candidate scaffold, not a final release model.",
            "- The Phase 5 stand universe and treatment/transition scaffold are reused.",
            "- P9RF source/THLB exclusions and sensitive-source caveats remain visible.",
            "- The accepted 27 Phase 10R Table 57 rows materialize as 18 active MP11 "
            "candidate curves because duplicate rows map to canonical AU identities.",
            "- Tables 54/55 remain excluded until a public-safe AU-code mapping exists.",
            "- Harvest-system and MHA policy fields remain deferred comparison/QA metadata.",
            "",
            "## Phase 12 Start Point",
            "",
            "Phase 12 starts from these generated candidate inputs:",
            "",
            "- `output/patchworks_tfl6_mp11_candidate/forestmodel.xml`",
            "- `output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp`",
            "- `data/mp11_model_input_bundle/export_compat/bridge_manifest.json`",
            "",
            "The next build step is P12.2 Matrix Builder. It must write tracks under "
            "`models/tfl6_patchworks_model_mp11_candidate/tracks/`, then inspect "
            "accounts, protoaccounts, features, products, curves, blocks, and "
            "treatment/group signals before any runtime success claim.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_closeout(
    *,
    bundle_summary_json: Path = DEFAULT_BUNDLE_SUMMARY_JSON,
    xml_qa_json: Path = DEFAULT_XML_QA_JSON,
    phase12_handoff_json: Path = DEFAULT_PHASE12_HANDOFF_JSON,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    bundle_summary = _load_json(bundle_summary_json)
    xml_qa = _load_json(xml_qa_json)
    handoff = _load_json(phase12_handoff_json)

    phase11_inputs = _path_status(PHASE11_GENERATED_INPUTS)
    phase5_inputs = _path_status(PHASE5_BASELINE_INPUTS)
    phase12_outputs = _path_status(PHASE12_RUNTIME_OUTPUTS)

    missing_phase11 = [
        record["path"] for record in phase11_inputs.values() if not record["exists"]
    ]
    missing_phase5 = [
        record["path"] for record in phase5_inputs.values() if not record["exists"]
    ]
    premature_phase12 = [
        record["path"] for record in phase12_outputs.values() if record["exists"]
    ]
    if missing_phase11:
        raise FileNotFoundError(
            "Phase 11 generated inputs are missing: " + "; ".join(missing_phase11)
        )
    if missing_phase5:
        raise FileNotFoundError(
            "Phase 5 baseline inputs are missing: " + "; ".join(missing_phase5)
        )
    if premature_phase12:
        raise RuntimeError(
            "Phase 12 runtime outputs already exist: " + "; ".join(premature_phase12)
        )

    bundle = bundle_summary["summary"]
    qa = xml_qa["summary"]
    handoff_summary = handoff["summary"]
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "phase11_status": "complete_model_input_xml_handoff",
        "candidate_bundle_root": bundle["candidate_bundle_root"],
        "candidate_xml": qa["xml_path"],
        "candidate_fragments": "output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp",
        "active_mp11_curve_count": bundle["active_mp11_curve_count"],
        "duplicate_mp11_rows_deferred_by_canonical_au": bundle[
            "duplicate_mp11_rows_deferred_by_canonical_au"
        ],
        "xml_root": qa["xml_root"],
        "xml_curve_nodes": qa["xml_curve_nodes"],
        "fragment_rows": qa["fragment_rows"],
        "fragment_area_ha": qa["fragment_area_ha"],
        "matrix_builder": "not_performed",
        "runtime_bundle_generation": "not_performed",
        "phase12_handoff_status": handoff_summary["handoff_status"],
    }
    rows = _closeout_rows()
    payload = {
        "summary": summary,
        "closeout_rows": rows,
        "phase11_generated_inputs": phase11_inputs,
        "phase5_baseline_inputs": phase5_inputs,
        "phase12_runtime_outputs": phase12_outputs,
        "source_manifests": {
            "bundle_summary_json": _repo_relative(bundle_summary_json),
            "xml_qa_json": _repo_relative(xml_qa_json),
            "phase12_handoff_json": _repo_relative(phase12_handoff_json),
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
    parser.add_argument("--xml-qa-json", type=Path, default=DEFAULT_XML_QA_JSON)
    parser.add_argument(
        "--phase12-handoff-json", type=Path, default=DEFAULT_PHASE12_HANDOFF_JSON
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_closeout(
        bundle_summary_json=args.bundle_summary_json,
        xml_qa_json=args.xml_qa_json,
        phase12_handoff_json=args.phase12_handoff_json,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
