"""Build P14.6 Matrix Builder/runtime package QA and launch surfaces."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "tfl6_patchworks_model_mp11_harvest_system_candidate"
SOURCE_MODEL_ROOT = ROOT / "models" / "tfl6_patchworks_model_mp11_candidate"
TRACKS_ROOT = MODEL_ROOT / "tracks"
BLOCKS_ROOT = MODEL_ROOT / "blocks"
RUN_ID = "tfl6_mp11_harvest_system_p14_6_matrix_build"
MATRIX_MANIFEST = ROOT / "runtime" / "logs" / f"patchworks_matrixbuilder_manifest-{RUN_ID}.json"
MATRIX_STDOUT = ROOT / "runtime" / "logs" / f"patchworks_matrixbuilder_stdout-{RUN_ID}.log"
MATRIX_STDERR = ROOT / "runtime" / "logs" / f"patchworks_matrixbuilder_stderr-{RUN_ID}.log"
P14_XML_QA = ROOT / "planning" / "tfl6_mp11_phase14_model_input_xml_build_summary.json"

OUT_CSV = ROOT / "planning" / "tfl6_mp11_phase14_matrix_runtime_qa.csv"
OUT_JSON = ROOT / "planning" / "tfl6_mp11_phase14_matrix_runtime_qa.json"
OUT_MD = ROOT / "planning" / "tfl6_mp11_phase14_matrix_runtime_qa.md"

TRACK_FILES = [
    "features.csv",
    "protoaccounts.csv",
    "accounts.csv",
    "products.csv",
    "curves.csv",
    "groups.csv",
    "strata.csv",
    "treatments.csv",
    "blocks.csv",
    "tracknames.csv",
    "packages.csv",
    "packageSequences.csv",
    "messages.csv",
]

TRACKED_PACKAGE_FILES = [
    "README.md",
    "lineage_registry.yaml",
    "analysis/base.pin",
    "analysis/base_variant_common.bsh",
    "analysis/headless_runtime_common.bsh",
    "scripts/targets/flowtargets.bsh",
]


def _repo(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required JSON missing: {_repo(path)}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _read_track(name: str) -> pd.DataFrame:
    path = TRACKS_ROOT / name
    if not path.exists():
        raise FileNotFoundError(f"Track file missing: {_repo(path)}")
    return pd.read_csv(path)


def _contains_rows(frame: pd.DataFrame, text: str) -> int:
    return int(
        frame.astype(str)
        .apply(lambda series: series.str.contains(text, regex=False))
        .any(axis=1)
        .sum()
    )


def _copy_launch_surfaces() -> None:
    mapping = {
        SOURCE_MODEL_ROOT / "analysis" / "base.pin": MODEL_ROOT / "analysis" / "base.pin",
        SOURCE_MODEL_ROOT / "analysis" / "base_variant_common.bsh": (
            MODEL_ROOT / "analysis" / "base_variant_common.bsh"
        ),
        SOURCE_MODEL_ROOT / "analysis" / "headless_runtime_common.bsh": (
            MODEL_ROOT / "analysis" / "headless_runtime_common.bsh"
        ),
        SOURCE_MODEL_ROOT / "scripts" / "targets" / "flowtargets.bsh": (
            MODEL_ROOT / "scripts" / "targets" / "flowtargets.bsh"
        ),
    }
    for source, target in mapping.items():
        if not source.exists():
            raise FileNotFoundError(f"Launch template missing: {_repo(source)}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _write_readme() -> None:
    text = """# TFL 6 MP11 Harvest-System Candidate Patchworks Runtime Package

This directory is the active Phase 14 harvest-system candidate Patchworks runtime-package root for the MP11 supplement.

Current scope:

- `tracks/` is the generated Matrix Builder track-table surface from P14.6.
- `blocks/` is the generated block/topology surface from P14.6.
- `analysis/` contains the candidate `base.pin` launch surface and shared headless helper scripts copied from the Phase 12 MP11 candidate runtime pattern.
- `lineage_registry.yaml` records package inputs, generation commands, validation status, caveats, and the Phase 14 handoff boundary.

Current modeling boundary:

- This is an MP11 harvest-system candidate scaffold, not a final release model.
- WFP LBB geometry remains unavailable; `HVSYS` is a public-proxy field from P14.4.
- The runtime exposes split `CC_GROUND`, `CC_CABLE`, and `CC_HELI` treatment lanes.
- Aggregate `.CC` product labels are retained for all-system harvest-flow reporting.
- Matrix Builder and block/topology assembly passed in P14.6.
- Direct launch smoke, all-system scenario smoke, no-heli scenario smoke, documentation, and closeout remain downstream Phase 14 tasks.

Generated blocks, tracks, saved-stage outputs, logs, and package scratch files remain ignored in Git. Tracked planning manifests carry compact provenance and QA summaries.
"""
    (MODEL_ROOT / "README.md").write_text(text, encoding="utf-8")


def _write_lineage(payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    text = f"""schema_version: 1
model_id: tfl6_patchworks_model_mp11_harvest_system_candidate
model_root: models/tfl6_patchworks_model_mp11_harvest_system_candidate
runtime_config: config/patchworks.runtime.mp11_harvest_system_candidate.windows.yaml
phase: P14.6
status: {summary["runtime_package_status"]}

artifact_inventory:
  data:
    fragments_shapefile:
      path: output/patchworks_tfl6_mp11_harvest_system_candidate/fragments/fragments.shp
      qa_status: p14_5_split_lane_xml
      evidence:
        planning_note: planning/tfl6_mp11_phase14_model_input_xml_build_summary.md
        rows: {summary["fragment_rows"]}
        area_ha: {summary["fragment_area_ha"]}
        hvsys_field: HVSYS
  yield:
    forestmodel_xml:
      path: output/patchworks_tfl6_mp11_harvest_system_candidate/forestmodel.xml
      qa_status: p14_5_split_lane_xml
      evidence:
        xml_root: ForestModel
        split_treatment_nodes: {summary["split_treatment_nodes"]}
        split_product_selects: {summary["split_product_selects"]}
  tracks:
    matrix_outputs:
      path_glob: models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/*.csv
      qa_status: p14_6_matrix_builder_tracks_pass
      evidence:
        planning_note: planning/tfl6_mp11_phase14_matrix_runtime_qa.md
        run_id: {summary["matrix_run_id"]}
        track_file_count: {summary["track_file_count"]}
        features_rows: {summary["features_rows"]}
        accounts_rows: {summary["accounts_rows"]}
        products_rows: {summary["products_rows"]}
        treatments_rows: {summary["treatments_rows"]}
        messages_rows: {summary["messages_rows"]}
  blocks:
    blocks_shapefile:
      path: models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/blocks.shp
      qa_status: p14_6_runtime_blocks_pass
      evidence:
        rows: {summary["block_rows"]}
        crs: {summary["block_crs"]}
        geometry_valid: {str(summary["block_geometry_valid"]).lower()}
        area_ha: {summary["block_area_ha"]}
    topology_csv:
      path: models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/topology_blocks_200r.csv
      qa_status: p14_6_runtime_blocks_pass
      evidence:
        rows: {summary["topology_rows"]}

runtime_launch_surfaces:
  baseline_pin:
    path: models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/base.pin
    helper_scripts:
      - models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/base_variant_common.bsh
      - models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/headless_runtime_common.bsh
      - models/tfl6_patchworks_model_mp11_harvest_system_candidate/scripts/targets/flowtargets.bsh
    qa_status: p14_6_ready_for_launch_smoke

publication_policy:
  tracked_in_git:
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/README.md
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/lineage_registry.yaml
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/base.pin
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/base_variant_common.bsh
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/headless_runtime_common.bsh
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/scripts/targets/flowtargets.bsh
  regenerated_by_default:
    - data/mp11_harvest_system_model_input_bundle/
    - output/patchworks_tfl6_mp11_harvest_system_candidate/
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/tracks/
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/blocks/
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/patchworksLog.csv
  excluded_from_publication_until_p14_closeout:
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/p*/
    - models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/headless_runs/
    - runtime/

caveats:
  - WFP LBB remains unavailable; HVSYS is a public proxy.
  - Direct launch smoke and scenario smoke are downstream P14.7 work.
  - This package does not replace the Phase 5 accepted public teaching/runtime baseline.
"""
    (MODEL_ROOT / "lineage_registry.yaml").write_text(text, encoding="utf-8")


def _file_record(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Package file missing: {_repo(path)}")
    return {"path": _repo(path), "bytes": path.stat().st_size, "sha256": _sha256(path)}


def _log_scan(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    return {
        "path": _repo(path),
        "bytes": path.stat().st_size,
        "error_count": lowered.count("error"),
        "warning_count": lowered.count("warning"),
        "failed_count": lowered.count("failed"),
        "exception_count": lowered.count("exception"),
    }


def _inspect_tracks() -> dict[str, Any]:
    tracks = {name: _read_track(name) for name in TRACK_FILES}
    accounts_proto_equal = tracks["accounts.csv"].equals(tracks["protoaccounts.csv"])
    split_labels = {
        "CC_GROUND": _contains_rows(tracks["treatments.csv"], "CC_GROUND"),
        "CC_CABLE": _contains_rows(tracks["treatments.csv"], "CC_CABLE"),
        "CC_HELI": _contains_rows(tracks["treatments.csv"], "CC_HELI"),
    }
    product_split_labels = {
        "ground": _contains_rows(
            tracks["products.csv"], "product.HarvestedVolume.managed.Total.CC_GROUND"
        ),
        "cable": _contains_rows(
            tracks["products.csv"], "product.HarvestedVolume.managed.Total.CC_CABLE"
        ),
        "heli": _contains_rows(
            tracks["products.csv"], "product.HarvestedVolume.managed.Total.CC_HELI"
        ),
        "aggregate": _contains_rows(
            tracks["products.csv"], "product.HarvestedVolume.managed.Total.CC"
        ),
    }
    return {
        "row_counts": {name: int(len(frame)) for name, frame in tracks.items()},
        "accounts_proto_equal": bool(accounts_proto_equal),
        "split_treatment_rows": split_labels,
        "split_product_rows": product_split_labels,
        "track_file_count": len(TRACK_FILES),
    }


def _inspect_blocks() -> dict[str, Any]:
    blocks_path = BLOCKS_ROOT / "blocks.shp"
    topology_path = BLOCKS_ROOT / "topology_blocks_200r.csv"
    blocks = gpd.read_file(blocks_path)
    topology = pd.read_csv(topology_path)
    return {
        "block_rows": int(len(blocks)),
        "block_area_ha": float(blocks.geometry.area.sum() / 10000.0),
        "block_crs": str(blocks.crs),
        "block_geometry_valid": bool(blocks.geometry.is_valid.all()),
        "topology_rows": int(len(topology)),
        "topology_columns": list(topology.columns),
    }


def _write_outputs(payload: dict[str, Any]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for key, value in payload["summary"].items():
            writer.writerow({"metric": key, "value": value})
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    lines = [
        "# TFL 6 MP11 Phase 14 Matrix Runtime QA",
        "",
        "This P14.6 output records Matrix Builder and runtime package assembly for "
        "the MP11 harvest-system candidate. It does not run direct launch smoke "
        "or scenarios.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Split-Lane Track Evidence",
            "",
            "| Surface | Ground | Cable | Heli | Aggregate |",
            "| --- | ---: | ---: | ---: | ---: |",
            (
                "| Treatments | `{}` | `{}` | `{}` | `n/a` |".format(
                    payload["tracks"]["split_treatment_rows"]["CC_GROUND"],
                    payload["tracks"]["split_treatment_rows"]["CC_CABLE"],
                    payload["tracks"]["split_treatment_rows"]["CC_HELI"],
                )
            ),
            (
                "| Products | `{}` | `{}` | `{}` | `{}` |".format(
                    payload["tracks"]["split_product_rows"]["ground"],
                    payload["tracks"]["split_product_rows"]["cable"],
                    payload["tracks"]["split_product_rows"]["heli"],
                    payload["tracks"]["split_product_rows"]["aggregate"],
                )
            ),
            "",
            "## Boundary",
            "",
            "- Direct launch smoke remains P14.7.",
            "- All-system and no-heli scenario smoke remain P14.7.",
            "- WFP LBB remains unavailable; this runtime uses public-proxy `HVSYS` lanes.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def build_manifest() -> dict[str, Any]:
    _copy_launch_surfaces()
    p14_xml_qa = _read_json(P14_XML_QA)
    matrix_manifest = _read_json(MATRIX_MANIFEST)
    tracks = _inspect_tracks()
    blocks = _inspect_blocks()
    stdout_scan = _log_scan(MATRIX_STDOUT)
    stderr_scan = _log_scan(MATRIX_STDERR)

    hard_checks = {
        "matrix_returncode_zero": matrix_manifest.get("returncode") == 0,
        "track_files_present": all((TRACKS_ROOT / name).exists() for name in TRACK_FILES),
        "messages_header_only": tracks["row_counts"]["messages.csv"] == 0,
        "accounts_proto_equal": tracks["accounts_proto_equal"],
        "split_treatments_present": all(
            value > 0 for value in tracks["split_treatment_rows"].values()
        ),
        "split_products_present": all(
            value > 0 for value in tracks["split_product_rows"].values()
        ),
        "block_geometry_valid": blocks["block_geometry_valid"],
        "topology_present": blocks["topology_rows"] > 0,
        "no_manifest_failures": not matrix_manifest.get("failures"),
    }
    status = (
        "harvest_system_candidate_runtime_assembled_pending_smoke"
        if all(hard_checks.values())
        else "harvest_system_candidate_runtime_needs_review"
    )
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "runtime_package_status": status,
        "matrix_run_id": RUN_ID,
        "matrix_returncode": matrix_manifest.get("returncode"),
        "track_file_count": tracks["track_file_count"],
        "features_rows": tracks["row_counts"]["features.csv"],
        "accounts_rows": tracks["row_counts"]["accounts.csv"],
        "protoaccounts_rows": tracks["row_counts"]["protoaccounts.csv"],
        "products_rows": tracks["row_counts"]["products.csv"],
        "treatments_rows": tracks["row_counts"]["treatments.csv"],
        "messages_rows": tracks["row_counts"]["messages.csv"],
        "cc_ground_treatment_rows": tracks["split_treatment_rows"]["CC_GROUND"],
        "cc_cable_treatment_rows": tracks["split_treatment_rows"]["CC_CABLE"],
        "cc_heli_treatment_rows": tracks["split_treatment_rows"]["CC_HELI"],
        "cc_ground_product_rows": tracks["split_product_rows"]["ground"],
        "cc_cable_product_rows": tracks["split_product_rows"]["cable"],
        "cc_heli_product_rows": tracks["split_product_rows"]["heli"],
        "aggregate_cc_product_rows": tracks["split_product_rows"]["aggregate"],
        "block_rows": blocks["block_rows"],
        "block_area_ha": round(blocks["block_area_ha"], 6),
        "block_crs": blocks["block_crs"],
        "block_geometry_valid": blocks["block_geometry_valid"],
        "topology_rows": blocks["topology_rows"],
        "fragment_rows": p14_xml_qa["summary"]["fragment_rows"],
        "fragment_area_ha": p14_xml_qa["summary"]["fragment_area_ha"],
        "split_treatment_nodes": p14_xml_qa["summary"]["xml_treatment_nodes"],
        "split_product_selects": p14_xml_qa["summary"]["split_product_selects"],
        "direct_launch_smoke": "not_performed",
        "scenario_smoke": "not_performed",
    }
    partial_payload = {"summary": summary}
    _write_readme()
    _write_lineage(partial_payload)
    payload = {
        "summary": summary,
        "hard_checks": hard_checks,
        "tracks": tracks,
        "blocks": blocks,
        "matrix_manifest": {
            "path": _repo(MATRIX_MANIFEST),
            "warnings": matrix_manifest.get("warnings", []),
            "failures": matrix_manifest.get("failures", []),
        },
        "log_scan": {"stdout": stdout_scan, "stderr": stderr_scan},
        "tracked_package_files": [
            _file_record(MODEL_ROOT / rel_path) for rel_path in TRACKED_PACKAGE_FILES
        ],
        "generated_track_files": [
            _file_record(TRACKS_ROOT / rel_path) for rel_path in TRACK_FILES
        ],
        "generated_block_files": [
            _file_record(BLOCKS_ROOT / rel_path)
            for rel_path in [
                "blocks.shp",
                "blocks.dbf",
                "blocks.shx",
                "blocks.prj",
                "blocks.cpg",
                "topology_blocks_200r.csv",
            ]
        ],
    }
    payload["tracked_package_files"] = [
        _file_record(MODEL_ROOT / rel_path) for rel_path in TRACKED_PACKAGE_FILES
    ]
    _write_outputs(payload)
    return payload


def main() -> None:
    payload = build_manifest()
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
