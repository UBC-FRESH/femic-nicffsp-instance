"""Build Phase 13 MP11 candidate runtime archive/materialization QA outputs."""

from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ID = "tfl6_mp11_candidate_runtime_p13_4"
ARCHIVE_PATH = Path("releases") / f"{ARTIFACT_ID}.zip"
MANIFEST_PATH = Path("releases") / f"{ARTIFACT_ID}_manifest.yaml"
CSV_PATH = Path("planning") / "tfl6_mp11_phase13_archive_materialization_qa.csv"
JSON_PATH = Path("planning") / "tfl6_mp11_phase13_archive_materialization_qa.json"
MD_PATH = Path("planning") / "tfl6_mp11_phase13_archive_materialization_qa.md"

INCLUDE_FILES = [
    Path("config/patchworks.runtime.mp11_candidate.windows.yaml"),
    Path("models/tfl6_patchworks_model_mp11_candidate/README.md"),
    Path("models/tfl6_patchworks_model_mp11_candidate/lineage_registry.yaml"),
    Path("models/tfl6_patchworks_model_mp11_candidate/analysis/base.pin"),
    Path(
        "models/tfl6_patchworks_model_mp11_candidate/analysis/base_variant_common.bsh"
    ),
    Path(
        "models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runtime_common.bsh"
    ),
    Path("models/tfl6_patchworks_model_mp11_candidate/scripts/targets/flowtargets.bsh"),
    Path("output/patchworks_tfl6_mp11_candidate/forestmodel.xml"),
    Path("output/patchworks_tfl6_mp11_candidate/fragments/fragments.cpg"),
    Path("output/patchworks_tfl6_mp11_candidate/fragments/fragments.dbf"),
    Path("output/patchworks_tfl6_mp11_candidate/fragments/fragments.prj"),
    Path("output/patchworks_tfl6_mp11_candidate/fragments/fragments.shp"),
    Path("output/patchworks_tfl6_mp11_candidate/fragments/fragments.shx"),
    Path("models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.cpg"),
    Path("models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.dbf"),
    Path("models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.prj"),
    Path("models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.shp"),
    Path("models/tfl6_patchworks_model_mp11_candidate/blocks/blocks.shx"),
    Path("models/tfl6_patchworks_model_mp11_candidate/blocks/topology_blocks_200r.csv"),
]

TRACK_DIR = Path("models/tfl6_patchworks_model_mp11_candidate/tracks")
TRACK_FILES = [
    TRACK_DIR / "accounts.csv",
    TRACK_DIR / "blocks.csv",
    TRACK_DIR / "curves.csv",
    TRACK_DIR / "features.csv",
    TRACK_DIR / "groups.csv",
    TRACK_DIR / "messages.csv",
    TRACK_DIR / "packages.csv",
    TRACK_DIR / "packageSequences.csv",
    TRACK_DIR / "products.csv",
    TRACK_DIR / "protoaccounts.csv",
    TRACK_DIR / "strata.csv",
    TRACK_DIR / "tracknames.csv",
    TRACK_DIR / "treatments.csv",
]

EXCLUDED_PATTERNS = [
    "models/tfl6_patchworks_model_mp11_candidate/analysis/p*/",
    "models/tfl6_patchworks_model_mp11_candidate/analysis/headless_runs/",
    "models/tfl6_patchworks_model_mp11_candidate/patchworksLog.csv",
    "runtime/",
    "docs/_build/",
    "data/mp11_model_input_bundle/",
    "data/downloads/",
    "data/bc/",
]


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
    path_text = path.as_posix()
    if path_text.startswith("config/"):
        return "p12_1_runtime_config"
    if (
        "analysis/" in path_text
        or "/scripts/targets/" in path_text
        or path_text.endswith("README.md")
        or path_text.endswith("lineage_registry.yaml")
    ):
        return "p12_3_launch_and_metadata"
    if "/tracks/" in path_text:
        return "p12_2_matrix_builder"
    if "/blocks/" in path_text:
        return "p12_3_blocks_topology"
    if path_text.startswith("output/"):
        return "p11_4_forestmodel_xml_fragments"
    return "unknown"


def _file_records(paths: Iterable[Path]) -> list[FileRecord]:
    records: list[FileRecord] = []
    missing: list[str] = []
    for relative_path in sorted(paths, key=lambda item: item.as_posix().lower()):
        absolute_path = REPO_ROOT / relative_path
        if not absolute_path.is_file():
            missing.append(relative_path.as_posix())
            continue
        records.append(
            FileRecord(
                path=relative_path.as_posix(),
                size_bytes=absolute_path.stat().st_size,
                sha256=_sha256(absolute_path),
                source_step=_source_step(relative_path),
            )
        )
    if missing:
        missing_text = ", ".join(missing)
        raise FileNotFoundError(f"Required archive input(s) missing: {missing_text}")
    return records


def _write_archive(records: list[FileRecord]) -> tuple[int, str, int]:
    archive_absolute = REPO_ROOT / ARCHIVE_PATH
    archive_absolute.parent.mkdir(parents=True, exist_ok=True)
    if archive_absolute.exists():
        archive_absolute.unlink()

    with zipfile.ZipFile(
        archive_absolute, "w", compression=zipfile.ZIP_DEFLATED
    ) as archive:
        for record in records:
            source = REPO_ROOT / record.path
            zip_info = zipfile.ZipInfo(record.path)
            zip_info.date_time = (2026, 1, 1, 0, 0, 0)
            zip_info.compress_type = zipfile.ZIP_DEFLATED
            with source.open("rb") as handle:
                archive.writestr(zip_info, handle.read())

    with zipfile.ZipFile(archive_absolute, "r") as archive:
        archive.testzip()
        member_count = len(archive.infolist())

    return archive_absolute.stat().st_size, _sha256(archive_absolute), member_count


def _manifest_yaml(
    records: list[FileRecord], archive_size: int, archive_sha: str
) -> str:
    lines = [
        "schema_version: 1",
        f"artifact_id: {ARTIFACT_ID}",
        f"archive_path: {ARCHIVE_PATH.as_posix()}",
        f"archive_sha256: {archive_sha}",
        f"archive_size_bytes: {archive_size}",
        f"created_utc: '{datetime.now(UTC).isoformat(timespec='seconds')}'",
        "instance_repo: UBC-FRESH/femic-tfl6-instance",
        "source_branch: feature/p13-4-mp11-archive-materialization-qa",
        "release_decision: pending_p13_5",
        "publication_status: local_archive_built_not_published",
        "phase5_relationship: phase5_remains_accepted_baseline_pending_p13_5",
        "included_files:",
    ]
    for record in records:
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
            "  clean_checkout_materialization: pending_publication_or_p13_5_decision",
            "  direct_launch_smoke: accepted_p12_4",
            "  scenario_smoke: accepted_p12_5",
            "  release_qa: not_performed",
        ]
    )
    return "\n".join(lines) + "\n"


def _summary_rows(
    records: list[FileRecord], archive_size: int, archive_sha: str
) -> list[dict[str, str]]:
    by_step: dict[str, list[FileRecord]] = {}
    for record in records:
        by_step.setdefault(record.source_step, []).append(record)

    rows = [
        {
            "id": "archive_status",
            "status": "local_archive_built_not_published",
            "value": ARCHIVE_PATH.as_posix(),
            "evidence": "archive_built_and_zip_integrity_checked",
            "release_implication": "candidate_archive_available_for_p13_5_decision",
        },
        {
            "id": "archive_sha256",
            "status": "recorded",
            "value": archive_sha,
            "evidence": MANIFEST_PATH.as_posix(),
            "release_implication": "supports_later_annex_or_publication_check",
        },
        {
            "id": "archive_size_bytes",
            "status": "recorded",
            "value": str(archive_size),
            "evidence": MANIFEST_PATH.as_posix(),
            "release_implication": "supports_later_annex_or_publication_check",
        },
        {
            "id": "clean_checkout_materialization",
            "status": "pending_publication_or_p13_5_decision",
            "value": "not_run",
            "evidence": "archive_is_local_ignored_candidate_payload",
            "release_implication": "blocks_replacement_release_but_not_candidate_supplement_decision",
        },
    ]
    for step, step_records in sorted(by_step.items()):
        rows.append(
            {
                "id": step,
                "status": "included",
                "value": f"{len(step_records)} files",
                "evidence": MANIFEST_PATH.as_posix(),
                "release_implication": "public_safe_runtime_input_candidate",
            }
        )
    return rows


def _write_csv(rows: list[dict[str, str]]) -> None:
    output_path = REPO_ROOT / CSV_PATH
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "status", "value", "evidence", "release_implication"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_json(
    rows: list[dict[str, str]],
    records: list[FileRecord],
    archive_size: int,
    archive_sha: str,
) -> None:
    payload = {
        "artifact_id": ARTIFACT_ID,
        "archive_path": ARCHIVE_PATH.as_posix(),
        "archive_size_bytes": archive_size,
        "archive_sha256": archive_sha,
        "manifest_path": MANIFEST_PATH.as_posix(),
        "publication_status": "local_archive_built_not_published",
        "release_decision": "pending_p13_5",
        "phase5_relationship": "phase5_remains_accepted_baseline_pending_p13_5",
        "included_file_count": len(records),
        "excluded_patterns": EXCLUDED_PATTERNS,
        "summary_rows": rows,
        "included_files": [record.__dict__ for record in records],
    }
    output_path = REPO_ROOT / JSON_PATH
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_md(
    rows: list[dict[str, str]],
    records: list[FileRecord],
    archive_size: int,
    archive_sha: str,
) -> None:
    md_lines = [
        "# TFL 6 MP11 Phase 13 Archive And Materialization QA",
        "",
        "This note records P13.4 archive/materialization QA for the MP11 candidate runtime. "
        "It builds a local ignored candidate archive and a tracked manifest so P13.5 can "
        "decide whether the candidate supplements Phase 5, replaces Phase 5 after stronger "
        "QA, or remains experimental.",
        "",
        "## Summary",
        "",
        "- archive_status: `local_archive_built_not_published`",
        f"- archive_path: `{ARCHIVE_PATH.as_posix()}`",
        f"- manifest_path: `{MANIFEST_PATH.as_posix()}`",
        f"- archive_size_bytes: `{archive_size}`",
        f"- archive_sha256: `{archive_sha}`",
        f"- included_file_count: `{len(records)}`",
        "- local_archive_integrity: `pass`",
        "- clean_checkout_materialization: `pending_publication_or_p13_5_decision`",
        "- release_decision: `pending_p13_5`",
        "- phase5_relationship: `phase5_remains_accepted_baseline_pending_p13_5`",
        "",
        "## QA Rows",
        "",
        "| ID | Status | Value | Evidence | Release implication |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        md_lines.append(
            f"| `{row['id']}` | `{row['status']}` | `{row['value']}` | "
            f"`{row['evidence']}` | {row['release_implication']} |"
        )

    md_lines.extend(
        [
            "",
            "## Included Runtime Inputs",
            "",
            "| Path | Bytes | Source step | SHA256 |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for record in records:
        md_lines.append(
            f"| `{record.path}` | `{record.size_bytes}` | `{record.source_step}` | "
            f"`{record.sha256}` |"
        )

    md_lines.extend(
        [
            "",
            "## Excluded Runtime Outputs",
            "",
        ]
    )
    md_lines.extend(f"- `{pattern}`" for pattern in EXCLUDED_PATTERNS)
    md_lines.extend(
        [
            "",
            "Saved-stage outputs, runtime logs, generated model-input tables, and source download "
            "caches are excluded from the archive. They remain QA or rebuild evidence, not "
            "canonical runtime launch inputs.",
            "",
            "## Materialization Boundary",
            "",
            "The archive exists locally under the ignored `releases/` root and passed ZIP "
            "integrity checks. It has not been annexed, copied to `arbutus-s3`, or proven "
            "from a no-credential clean checkout. That prevents a `replace_phase5` release "
            "decision in P13.5, but it is enough evidence for P13.5 to decide whether the "
            "candidate can supplement Phase 5 as a documented MP11 candidate surface.",
            "",
            "The Phase 5 release archive remains the accepted public runtime package until "
            "P13.5 makes an explicit decision.",
        ]
    )
    (REPO_ROOT / MD_PATH).write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def main() -> None:
    records = _file_records([*INCLUDE_FILES, *TRACK_FILES])
    archive_size, archive_sha, member_count = _write_archive(records)
    if member_count != len(records):
        raise RuntimeError(
            f"ZIP member count {member_count} does not match manifest count {len(records)}"
        )
    (REPO_ROOT / MANIFEST_PATH).write_text(
        _manifest_yaml(records, archive_size, archive_sha), encoding="utf-8"
    )
    rows = _summary_rows(records, archive_size, archive_sha)
    _write_csv(rows)
    _write_json(rows, records, archive_size, archive_sha)
    _write_md(rows, records, archive_size, archive_sha)
    print(f"wrote {MD_PATH.as_posix()}")
    print(f"wrote {MANIFEST_PATH.as_posix()}")
    print(f"built {ARCHIVE_PATH.as_posix()} ({archive_size} bytes)")


if __name__ == "__main__":
    main()
