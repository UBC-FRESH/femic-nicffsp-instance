"""Build P15 MP11 harvest-system runtime archive/publication QA outputs."""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ID = "tfl6_mp11_harvest_system_candidate_runtime_p15_2"
ARCHIVE_PATH = Path("releases") / f"{ARTIFACT_ID}.zip"
MANIFEST_PATH = Path("releases") / f"{ARTIFACT_ID}_manifest.yaml"

OUT_CSV = Path("planning") / "tfl6_mp11_phase15_archive_publication_qa.csv"
OUT_JSON = Path("planning") / "tfl6_mp11_phase15_archive_publication_qa.json"
OUT_MD = Path("planning") / "tfl6_mp11_phase15_archive_publication_qa.md"

MODEL_ROOT = Path("models") / "tfl6_patchworks_model_mp11_harvest_system_candidate"
OUTPUT_ROOT = Path("output") / "patchworks_tfl6_mp11_harvest_system_candidate"
TRACK_ROOT = MODEL_ROOT / "tracks"
NO_HELI_TRACK_ROOT = MODEL_ROOT / "tracks_no_heli"

TRACK_FILE_NAMES = [
    "accounts.csv",
    "blocks.csv",
    "curves.csv",
    "features.csv",
    "groups.csv",
    "messages.csv",
    "packages.csv",
    "packageSequences.csv",
    "products.csv",
    "protoaccounts.csv",
    "strata.csv",
    "tracknames.csv",
    "treatments.csv",
]

INCLUDE_FILES = [
    Path("config/patchworks.runtime.mp11_harvest_system_candidate.windows.yaml"),
    OUTPUT_ROOT / "forestmodel.xml",
    OUTPUT_ROOT / "fragments" / "fragments.cpg",
    OUTPUT_ROOT / "fragments" / "fragments.dbf",
    OUTPUT_ROOT / "fragments" / "fragments.prj",
    OUTPUT_ROOT / "fragments" / "fragments.shp",
    OUTPUT_ROOT / "fragments" / "fragments.shx",
    MODEL_ROOT / "README.md",
    MODEL_ROOT / "lineage_registry.yaml",
    MODEL_ROOT / "analysis" / "base.pin",
    MODEL_ROOT / "analysis" / "base_variant_common.bsh",
    MODEL_ROOT / "analysis" / "headless_runtime_common.bsh",
    MODEL_ROOT / "analysis" / "no_heli.pin",
    MODEL_ROOT / "scripts" / "targets" / "flowtargets.bsh",
    MODEL_ROOT / "blocks" / "blocks.cpg",
    MODEL_ROOT / "blocks" / "blocks.dbf",
    MODEL_ROOT / "blocks" / "blocks.prj",
    MODEL_ROOT / "blocks" / "blocks.shp",
    MODEL_ROOT / "blocks" / "blocks.shx",
    MODEL_ROOT / "blocks" / "topology_blocks_200r.csv",
]

TRACK_FILES = [TRACK_ROOT / name for name in TRACK_FILE_NAMES]
NO_HELI_TRACK_FILES = [NO_HELI_TRACK_ROOT / name for name in TRACK_FILE_NAMES]

EXCLUDED_PATTERNS = [
    "models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/p*/",
    "models/tfl6_patchworks_model_mp11_harvest_system_candidate/analysis/headless_runs/",
    "models/tfl6_patchworks_model_mp11_harvest_system_candidate/patchworksLog.csv",
    "runtime/",
    "docs/_build/",
    "data/mp11_harvest_system_model_input_bundle/",
    "data/mp11_model_input_bundle/",
    "data/downloads/",
    "data/bc/",
]

ANNEX_REMOTE = {
    "name": "arbutus-s3",
    "bucket": "ubc-fresh-femic-tfl6-instance",
    "publicurl": "https://object-arbutus.cloud.computecanada.ca/ubc-fresh-femic-tfl6-instance",
    "uuid": "861b7dd7-fff0-4637-b0a2-b9b4668dca71",
}


@dataclass(frozen=True)
class FileRecord:
    path: str
    size_bytes: int
    sha256: str
    source_step: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_step(path: Path) -> str:
    text = path.as_posix()
    if text.startswith("config/"):
        return "p14_runtime_config"
    if text.startswith(OUTPUT_ROOT.as_posix()):
        return "p14_5_forestmodel_xml_fragments"
    if "/tracks_no_heli/" in text:
        return "p14_7_no_heli_tracks"
    if "/tracks/" in text:
        return "p14_6_matrix_builder_tracks"
    if "/blocks/" in text:
        return "p14_6_blocks_topology"
    if "/analysis/" in text or "/scripts/targets/" in text:
        return "p14_runtime_launch_surfaces"
    if text.endswith("README.md") or text.endswith("lineage_registry.yaml"):
        return "p14_runtime_metadata"
    return "unknown"


def _records(paths: Iterable[Path]) -> list[FileRecord]:
    file_records: list[FileRecord] = []
    missing: list[str] = []
    for relative in sorted(paths, key=lambda item: item.as_posix().lower()):
        absolute = ROOT / relative
        if not absolute.is_file():
            missing.append(relative.as_posix())
            continue
        file_records.append(
            FileRecord(
                path=relative.as_posix(),
                size_bytes=absolute.stat().st_size,
                sha256=_sha256(absolute),
                source_step=_source_step(relative),
            )
        )
    if missing:
        raise FileNotFoundError("Required archive inputs missing: " + ", ".join(missing))
    return file_records


def _write_archive(file_records: list[FileRecord]) -> tuple[int, str, int]:
    archive_path = ROOT / ARCHIVE_PATH
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    if archive_path.exists():
        archive_path.unlink()
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for record in file_records:
            info = zipfile.ZipInfo(record.path)
            info.date_time = (2026, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            with (ROOT / record.path).open("rb") as handle:
                archive.writestr(info, handle.read())
    with zipfile.ZipFile(archive_path, "r") as archive:
        archive.testzip()
        member_count = len(archive.infolist())
    return archive_path.stat().st_size, _sha256(archive_path), member_count


def _manifest_yaml(file_records: list[FileRecord], archive_size: int, archive_sha: str) -> str:
    lines = [
        "schema_version: 1",
        f"artifact_id: {ARTIFACT_ID}",
        f"archive_path: {ARCHIVE_PATH.as_posix()}",
        f"archive_sha256: {archive_sha}",
        f"archive_size_bytes: {archive_size}",
        f"created_utc: '{datetime.now(UTC).isoformat(timespec='seconds')}'",
        "instance_repo: UBC-FRESH/femic-tfl6-instance",
        "source_branch: feature/tfl6-mp11-p15-runtime-publication",
        "source_runtime_phase: phase14_harvest_system_candidate",
        "release_decision: replacement_candidate_pending_p15_7",
        "publication_status: local_archive_built_not_published",
        "phase5_relationship: phase5_remains_accepted_baseline_pending_replacement_acceptance",
        "annex_remote:",
        f"  name: {ANNEX_REMOTE['name']}",
        f"  bucket: {ANNEX_REMOTE['bucket']}",
        f"  publicurl: {ANNEX_REMOTE['publicurl']}",
        f"  uuid: {ANNEX_REMOTE['uuid']}",
        "included_files:",
    ]
    for record in file_records:
        lines.extend(
            [
                f"- path: {record.path}",
                f"  size_bytes: {record.size_bytes}",
                f"  sha256: {record.sha256}",
                f"  source_step: {record.source_step}",
            ]
        )
    lines.append("excluded_patterns:")
    lines.extend(f"- {pattern}" for pattern in EXCLUDED_PATTERNS)
    lines.extend(
        [
            "validation:",
            "  local_archive_integrity: pass",
            "  zip_member_count_matches_manifest: true",
            "  publication_status: local_archive_built_not_published",
            "  clean_checkout_materialization: pending_p15_4",
            "  direct_launch_smoke_from_archive: pending_p15_5",
            "  all_system_scenario_smoke_from_archive: pending_p15_5",
            "  no_heli_scenario_smoke_from_archive: pending_p15_5",
            "  replacement_candidate_decision: pending_p15_7",
        ]
    )
    return "\n".join(lines) + "\n"


def _summary_rows(file_records: list[FileRecord], archive_size: int, archive_sha: str) -> list[dict[str, str]]:
    by_step: dict[str, int] = {}
    for record in file_records:
        by_step[record.source_step] = by_step.get(record.source_step, 0) + 1
    rows = [
        {
            "id": "archive_status",
            "status": "local_archive_built_not_published",
            "value": ARCHIVE_PATH.as_posix(),
            "evidence": "archive_built_and_zip_integrity_checked",
            "replacement_implication": "candidate_archive_ready_for_publication_step",
        },
        {
            "id": "archive_sha256",
            "status": "recorded",
            "value": archive_sha,
            "evidence": MANIFEST_PATH.as_posix(),
            "replacement_implication": "supports_publication_and_materialization_checks",
        },
        {
            "id": "archive_size_bytes",
            "status": "recorded",
            "value": str(archive_size),
            "evidence": MANIFEST_PATH.as_posix(),
            "replacement_implication": "supports_publication_and_materialization_checks",
        },
        {
            "id": "phase5_relationship",
            "status": "baseline_preserved",
            "value": "phase5_remains_accepted_baseline_pending_replacement_acceptance",
            "evidence": MANIFEST_PATH.as_posix(),
            "replacement_implication": "p15_is_replacement_candidate_review_not_silent_replacement",
        },
    ]
    for source_step, count in sorted(by_step.items()):
        rows.append(
            {
                "id": source_step,
                "status": "included",
                "value": f"{count} files",
                "evidence": MANIFEST_PATH.as_posix(),
                "replacement_implication": "public_safe_runtime_payload_candidate",
            }
        )
    return rows


def _write_outputs(file_records: list[FileRecord], archive_size: int, archive_sha: str) -> None:
    (ROOT / MANIFEST_PATH).write_text(
        _manifest_yaml(file_records, archive_size, archive_sha), encoding="utf-8"
    )
    rows = _summary_rows(file_records, archive_size, archive_sha)

    with (ROOT / OUT_CSV).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "status", "value", "evidence", "replacement_implication"],
        )
        writer.writeheader()
        writer.writerows(rows)

    payload = {
        "artifact_id": ARTIFACT_ID,
        "archive_path": ARCHIVE_PATH.as_posix(),
        "manifest_path": MANIFEST_PATH.as_posix(),
        "archive_size_bytes": archive_size,
        "archive_sha256": archive_sha,
        "publication_status": "local_archive_built_not_published",
        "source_runtime_phase": "phase14_harvest_system_candidate",
        "phase5_relationship": "phase5_remains_accepted_baseline_pending_replacement_acceptance",
        "included_file_count": len(file_records),
        "excluded_patterns": EXCLUDED_PATTERNS,
        "summary_rows": rows,
        "included_files": [record.__dict__ for record in file_records],
    }
    (ROOT / OUT_JSON).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# TFL 6 MP11 Phase 15 Archive Publication QA",
        "",
        "This P15.2 report records the local archive and manifest build for the Phase 14 MP11 harvest-system candidate runtime. It does not publish the archive or prove clean-checkout materialization.",
        "",
        "## Summary",
        "",
        "- archive_status: `local_archive_built_not_published`",
        f"- archive_path: `{ARCHIVE_PATH.as_posix()}`",
        f"- manifest_path: `{MANIFEST_PATH.as_posix()}`",
        f"- archive_size_bytes: `{archive_size}`",
        f"- archive_sha256: `{archive_sha}`",
        f"- included_file_count: `{len(file_records)}`",
        "- source_runtime_phase: `phase14_harvest_system_candidate`",
        "- phase5_relationship: `phase5_remains_accepted_baseline_pending_replacement_acceptance`",
        "",
        "## QA Rows",
        "",
        "| ID | Status | Value | Evidence | Replacement implication |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['id']}` | `{row['status']}` | `{row['value']}` | "
            f"`{row['evidence']}` | {row['replacement_implication']} |"
        )
    lines.extend(
        [
            "",
            "## Included Runtime Inputs",
            "",
            "| Path | Bytes | Source step | SHA256 |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for record in file_records:
        lines.append(
            f"| `{record.path}` | `{record.size_bytes}` | `{record.source_step}` | "
            f"`{record.sha256}` |"
        )
    lines.extend(["", "## Excluded Runtime Outputs", ""])
    lines.extend(f"- `{pattern}`" for pattern in EXCLUDED_PATTERNS)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- P15.2 builds the local archive and tracked manifest only.",
            "- Publication to `arbutus-s3` remains P15.3.",
            "- No-credential materialization remains P15.4.",
            "- Archive-derived launch and scenario smoke remain P15.5.",
            "- The archive is a replacement candidate input, not an automatic Phase 5 replacement.",
            "",
        ]
    )
    (ROOT / OUT_MD).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    file_records = _records([*INCLUDE_FILES, *TRACK_FILES, *NO_HELI_TRACK_FILES])
    archive_size, archive_sha, member_count = _write_archive(file_records)
    if member_count != len(file_records):
        raise RuntimeError(
            f"ZIP member count {member_count} does not match manifest count {len(file_records)}"
        )
    _write_outputs(file_records, archive_size, archive_sha)
    print(json.dumps({
        "artifact_id": ARTIFACT_ID,
        "archive_path": ARCHIVE_PATH.as_posix(),
        "manifest_path": MANIFEST_PATH.as_posix(),
        "archive_size_bytes": archive_size,
        "archive_sha256": archive_sha,
        "included_file_count": len(file_records),
        "publication_status": "local_archive_built_not_published",
    }, indent=2))


if __name__ == "__main__":
    main()
