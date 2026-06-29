"""Build the P12.3 MP11 candidate runtime package manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_ROOT = INSTANCE_ROOT / "models" / "tfl6_patchworks_model_mp11_candidate"
DEFAULT_TRACK_QA_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_matrix_builder_tracks_qa.json"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_runtime_package_manifest.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_runtime_package_manifest.json"
)
DEFAULT_OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_runtime_package_manifest.md"

TRACKED_PACKAGE_FILES = [
    "README.md",
    "lineage_registry.yaml",
    "analysis/base.pin",
    "analysis/base_variant_common.bsh",
    "analysis/headless_runtime_common.bsh",
    "scripts/targets/flowtargets.bsh",
]

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

BLOCK_FILES = [
    "blocks.shp",
    "blocks.dbf",
    "blocks.shx",
    "blocks.prj",
    "blocks.cpg",
    "topology_blocks_200r.csv",
]


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_record(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Runtime package file missing: {_repo_relative(path)}")
    return {
        "path": _repo_relative(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required manifest input missing: {_repo_relative(path)}"
        )
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _inspect_blocks(model_root: Path) -> dict[str, Any]:
    blocks_path = model_root / "blocks" / "blocks.shp"
    topology_path = model_root / "blocks" / "topology_blocks_200r.csv"
    blocks = gpd.read_file(blocks_path)
    topology = pd.read_csv(topology_path)
    return {
        "blocks_path": _repo_relative(blocks_path),
        "block_rows": int(len(blocks)),
        "block_area_ha": float(blocks.geometry.area.sum() / 10000.0),
        "block_crs": str(blocks.crs),
        "block_geometry_valid": bool(blocks.geometry.is_valid.all()),
        "topology_path": _repo_relative(topology_path),
        "topology_rows": int(len(topology)),
        "topology_columns": list(topology.columns),
    }


def _write_outputs(
    *,
    payload: dict[str, Any],
    output_csv: Path,
    output_json: Path,
    output_md: Path,
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for key, value in payload["summary"].items():
            writer.writerow({"metric": key, "value": value})
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    lines = [
        "# P12.3 MP11 Runtime Package Manifest",
        "",
        "This manifest records the assembled MP11 candidate Patchworks runtime",
        "package after Matrix Builder tracks and block/topology surfaces were",
        "generated.",
        "",
        "P12.3 does not run direct Patchworks launch smoke, run scenarios, publish",
        "a release archive, or replace the accepted Phase 5 teaching/runtime",
        "baseline.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")

    lines.extend(
        [
            "",
            "## Tracked Package Files",
            "",
            "| Path | Bytes |",
            "| --- | ---: |",
        ]
    )
    for record in payload["tracked_package_files"]:
        lines.append(f"| `{record['path']}` | {record['bytes']} |")

    lines.extend(
        [
            "",
            "## Generated Runtime Inputs",
            "",
            "- Matrix Builder tracks remain under the ignored `tracks/` root.",
            "- Block/topology files remain under the ignored `blocks/` root.",
            "- Launch smoke and scenario smoke are still `not_performed`.",
            "",
            "## Boundary",
            "",
            "This is a candidate runtime package ready for P12.4 direct launch smoke.",
            "It is not a release package and does not supersede the accepted Phase 5",
            "teaching/runtime baseline.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_manifest(
    *,
    model_root: Path = DEFAULT_MODEL_ROOT,
    track_qa_json: Path = DEFAULT_TRACK_QA_JSON,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    track_qa = _load_json(track_qa_json)
    tracked_records = [
        _file_record(model_root / rel_path) for rel_path in TRACKED_PACKAGE_FILES
    ]
    track_records = [
        _file_record(model_root / "tracks" / rel_path) for rel_path in TRACK_FILES
    ]
    block_records = [
        _file_record(model_root / "blocks" / rel_path) for rel_path in BLOCK_FILES
    ]
    block_summary = _inspect_blocks(model_root)
    track_summary = track_qa["summary"]

    missing_launch = [
        rel_path
        for rel_path in TRACKED_PACKAGE_FILES
        if not (model_root / rel_path).exists()
    ]
    status = (
        "candidate_runtime_package_assembled_pending_launch_smoke"
        if not missing_launch
        and track_summary["qa_status"]
        == "matrix_builder_tracks_generated_inspection_pass"
        and block_summary["block_geometry_valid"]
        and block_summary["topology_rows"] > 0
        else "candidate_runtime_package_needs_review"
    )
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "runtime_package_status": status,
        "model_root": _repo_relative(model_root),
        "runtime_config": "config/patchworks.runtime.mp11_candidate.windows.yaml",
        "tracked_package_file_count": len(tracked_records),
        "track_file_count": len(track_records),
        "block_file_count": len(block_records),
        "block_rows": block_summary["block_rows"],
        "block_area_ha": round(block_summary["block_area_ha"], 6),
        "block_crs": block_summary["block_crs"],
        "block_geometry_valid": block_summary["block_geometry_valid"],
        "topology_rows": block_summary["topology_rows"],
        "tracks_qa_status": track_summary["qa_status"],
        "tracks_features_rows": track_summary["features_rows"],
        "tracks_accounts_rows": track_summary["accounts_rows"],
        "tracks_products_rows": track_summary["products_rows"],
        "tracks_messages_rows": track_summary["messages_rows"],
        "direct_launch_smoke": "not_performed",
        "scenario_smoke": "not_performed",
        "release_qa": "not_performed",
    }
    payload = {
        "summary": summary,
        "tracked_package_files": tracked_records,
        "generated_track_files": track_records,
        "generated_block_files": block_records,
        "block_summary": block_summary,
        "source_manifests": {
            "track_qa_json": _repo_relative(track_qa_json),
        },
        "caveats": [
            "This is an MP11 candidate scaffold, not a final release model.",
            "The Phase 5 stand universe and treatment/transition scaffold are reused.",
            "P9RF source/THLB caveats remain visible until a later source-layer rebuild.",
            "Tables 54/55 remain excluded until a public-safe AU-code mapping exists.",
            "Harvest-system assignment remains deferred comparison metadata.",
            "Direct launch smoke, scenario smoke, release QA, and publication remain downstream work.",
        ],
    }
    _write_outputs(
        payload=payload,
        output_csv=output_csv,
        output_json=output_json,
        output_md=output_md,
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-root", type=Path, default=DEFAULT_MODEL_ROOT)
    parser.add_argument("--track-qa-json", type=Path, default=DEFAULT_TRACK_QA_JSON)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_manifest(
        model_root=args.model_root,
        track_qa_json=args.track_qa_json,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
