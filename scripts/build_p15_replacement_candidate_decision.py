"""Build Phase 15 MP11 replacement-candidate decision outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "planning" / "tfl6_mp11_phase15_replacement_candidate_decision.csv"
OUT_JSON = ROOT / "planning" / "tfl6_mp11_phase15_replacement_candidate_decision.json"
OUT_MD = ROOT / "planning" / "tfl6_mp11_phase15_replacement_candidate_decision.md"

ARCHIVE_QA = ROOT / "planning" / "tfl6_mp11_phase15_archive_publication_qa.json"
MATERIALIZATION_QA = ROOT / "planning" / "tfl6_mp11_phase15_materialization_qa.json"
SMOKE_QA = ROOT / "planning" / "tfl6_mp11_phase15_materialized_runtime_smoke_qa.json"

REQUIRED_FILES = {
    "planning_note": ROOT
    / "planning"
    / "tfl6_mp11_phase15_publication_replacement_candidate_plan.md",
    "archive_qa": ARCHIVE_QA,
    "archive_manifest": ROOT
    / "releases"
    / "tfl6_mp11_harvest_system_candidate_runtime_p15_2_manifest.yaml",
    "materialization_qa": MATERIALIZATION_QA,
    "materialized_runtime_smoke_qa": SMOKE_QA,
    "phase15_docs": ROOT / "docs" / "phase15-mp11-runtime-publication.rst",
}


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _required_file_rows() -> list[dict[str, str]]:
    return [
        {
            "gate": name,
            "status": "pass" if path.is_file() else "blocked",
            "evidence": path.relative_to(ROOT).as_posix(),
            "rationale": "required P15 evidence surface is present",
        }
        for name, path in REQUIRED_FILES.items()
    ]


def _hard_gate_rows(
    archive: dict[str, Any], materialization: dict[str, Any], smoke: dict[str, Any]
) -> list[dict[str, str]]:
    smoke_summary = smoke["summary"]
    return [
        {
            "gate": "archive_published",
            "status": "pass"
            if archive["publication_status"] == "published_materialization_pending"
            else "blocked",
            "evidence": "planning/tfl6_mp11_phase15_archive_publication_qa.json",
            "rationale": (
                "archive and manifest were annexed, copied to arbutus-s3, and "
                "verified before materialization"
            ),
        },
        {
            "gate": "archive_checksum",
            "status": "pass"
            if archive["archive_sha256"]
            == materialization["materialized_artifacts"]["archive_sha256"]
            == materialization["materialized_artifacts"]["manifest_archive_sha256"]
            else "blocked",
            "evidence": "planning/tfl6_mp11_phase15_materialization_qa.json",
            "rationale": "materialized archive SHA256 matches the tracked manifest",
        },
        {
            "gate": "public_no_credential_materialization",
            "status": "pass"
            if materialization["annex_remote"]["creds"] == "not available"
            and materialization["annex_remote"]["public"] == "yes"
            and materialization["materialized_artifacts"]["git_annex_get"]
            == "checksum_ok"
            and materialization["unpack"]["expected_files_present"] is True
            else "blocked",
            "evidence": "planning/tfl6_mp11_phase15_materialization_qa.json",
            "rationale": (
                "clean checkout fetched archive and manifest from arbutus-s3 with "
                "credentials cleared"
            ),
        },
        {
            "gate": "direct_launch_from_archive",
            "status": "pass"
            if smoke_summary["direct_launch_status"] == "pass"
            else "blocked",
            "evidence": "planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json",
            "rationale": "materialized archive direct launch returned success",
        },
        {
            "gate": "all_system_scenario_from_archive",
            "status": "pass"
            if smoke_summary["all_system_status"] == "pass"
            and smoke_summary["all_system_treatments"] == "CC_CABLE,CC_GROUND,CC_HELI"
            else "blocked",
            "evidence": "planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json",
            "rationale": "all-system 200k smoke scheduled cable, ground, and heli lanes",
        },
        {
            "gate": "no_heli_scenario_from_archive",
            "status": "pass"
            if smoke_summary["no_heli_status"] == "pass"
            and smoke_summary["no_heli_treatments"] == "CC_CABLE,CC_GROUND"
            and smoke_summary["no_heli_forbidden_present"] == "none"
            else "blocked",
            "evidence": "planning/tfl6_mp11_phase15_materialized_runtime_smoke_qa.json",
            "rationale": (
                "no-heli 200k smoke scheduled cable and ground lanes only and did "
                "not trip missing heli account startup errors"
            ),
        },
    ]


def _decision_rows(hard_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    all_pass = all(row["status"] == "pass" for row in hard_rows)
    decision = (
        "replacement_candidate_ready_for_review"
        if all_pass
        else "replacement_candidate_blocked"
    )
    return [
        {
            "gate": "phase15_decision",
            "status": decision,
            "evidence": "P15.1-P15.6 hard-gate evidence",
            "rationale": (
                "all publication, materialization, checksum, launch, scenario, and "
                "documentation hard gates pass"
                if all_pass
                else "one or more publication, materialization, checksum, launch, "
                "scenario, or documentation hard gates failed"
            ),
        },
        {
            "gate": "phase5_baseline",
            "status": "accepted_baseline_retained",
            "evidence": "Phase 5 release remains unchanged",
            "rationale": (
                "P15 creates a replacement candidate for review; it does not "
                "silently replace Phase 5"
            ),
        },
        {
            "gate": "wfp_model_equivalence",
            "status": "not_claimed",
            "evidence": "docs/phase15-mp11-runtime-publication.rst",
            "rationale": (
                "WFP LBB is unavailable and harvest-system lanes remain public "
                "proxy assignments"
            ),
        },
    ]


def _write_csv(rows: list[dict[str, str]]) -> None:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["gate", "status", "evidence", "rationale"]
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_json(rows: list[dict[str, str]]) -> None:
    decision = next(row for row in rows if row["gate"] == "phase15_decision")
    payload = {
        "decision": decision["status"],
        "phase5_baseline_status": "accepted_public_runtime_baseline_retained",
        "mp11_harvest_system_candidate_status": decision["status"],
        "replace_phase5": False,
        "wfp_model_equivalence": False,
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_md(rows: list[dict[str, str]]) -> None:
    decision = next(row for row in rows if row["gate"] == "phase15_decision")
    lines = [
        "# TFL 6 MP11 Phase 15 Replacement-Candidate Decision",
        "",
        "P15.7 records whether the published MP11 harvest-system candidate runtime "
        "is ready for replacement review.",
        "",
        "## Decision",
        "",
        f"- decision: `{decision['status']}`",
        "- phase5_baseline_status: `accepted_public_runtime_baseline_retained`",
        "- replace_phase5: `False`",
        "- wfp_model_equivalence: `False`",
        "",
        "The P15 runtime is ready for replacement review because archive "
        "publication, no-credential materialization, checksum validation, direct "
        "launch, all-system scenario smoke, no-heli scenario smoke, and "
        "publication documentation have passed. Phase 5 remains the accepted "
        "baseline until a later explicit replacement acceptance decision.",
        "",
        "## Gate Results",
        "",
        "| Gate | Status | Evidence | Rationale |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['gate']}` | `{row['status']}` | "
            f"{row['evidence']} | {row['rationale']} |"
        )
    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- WFP LBB remains unavailable and private.",
            "- Ground, cable, and heli assignments are public proxies.",
            "- The candidate is not WFP-model equivalent.",
            "- The candidate is not an approved AAC decision.",
            "- Phase 5 remains the accepted public teaching/runtime baseline until "
            "replacement is explicitly accepted.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    archive = _load_json(ARCHIVE_QA)
    materialization = _load_json(MATERIALIZATION_QA)
    smoke = _load_json(SMOKE_QA)

    required_rows = _required_file_rows()
    hard_rows = _hard_gate_rows(archive, materialization, smoke)
    rows = required_rows + hard_rows + _decision_rows(required_rows + hard_rows)
    _write_csv(rows)
    _write_json(rows)
    _write_md(rows)
    decision = next(row for row in rows if row["gate"] == "phase15_decision")
    print(f"wrote {OUT_MD.relative_to(ROOT).as_posix()} with {decision['status']}")


if __name__ == "__main__":
    main()
