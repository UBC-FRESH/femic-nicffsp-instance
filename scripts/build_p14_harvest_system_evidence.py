"""Build the P14.2 harvest-system operability evidence inventory."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "planning"

OUT_CSV = PLANNING / "tfl6_mp11_phase14_harvest_system_evidence.csv"
OUT_JSON = PLANNING / "tfl6_mp11_phase14_harvest_system_evidence.json"
OUT_MD = PLANNING / "tfl6_mp11_phase14_harvest_system_evidence.md"


@dataclass(frozen=True)
class EvidenceRow:
    """One reviewed evidence row for Phase 14 classifier planning."""

    evidence_id: str
    evidence_family: str
    evidence_role: str
    source_anchor: str
    source_detail: str
    extracted_clue: str
    public_proxy_use: str
    queryable_or_local_artifact: str
    p14_decision: str
    p14_followup: str
    caveat: str


ROWS = [
    EvidenceRow(
        evidence_id="mp11_lbb_private_operability_source",
        evidence_family="physical_operability",
        evidence_role="unavailable_private_source",
        source_anchor="PDF p257 / IP p11; PDF p265-267 / IP p19-21; PDF p297 / IP p51",
        source_detail=(
            "MP11 says ground, cable, and helicopter harvest methods come from "
            "WFP's spatial LBB physical-operability dataset."
        ),
        extracted_clue=(
            "LBB uses LiDAR bare-earth hillshade, canopy height model, slope, "
            "streams, professional block/road planning, and post-harvest updates."
        ),
        public_proxy_use="Do not use as a queryable source; record as private benchmark context.",
        queryable_or_local_artifact="No public FEMIC-readable LBB layer identified.",
        p14_decision="unavailable_private_source",
        p14_followup="Build public proxy assignments and label them as non-equivalent to WFP LBB.",
        caveat="Aggregate MP11 LBB summaries cannot be reverse-engineered into stand truth.",
    ),
    EvidenceRow(
        evidence_id="mp11_physical_operability_classes",
        evidence_family="physical_operability",
        evidence_role="classification_target",
        source_anchor="PDF p297-298 / IP p51-52",
        source_detail="MP11 Section 6.8 and Tables 18-20.",
        extracted_clue=(
            "MP11 physical classes are conventional, non-conventional, and "
            "inoperable; only inoperable is removed from THLB."
        ),
        public_proxy_use="Use class vocabulary and inoperable/non-conventional distinction.",
        queryable_or_local_artifact="planning/tfl6_mp11_inventory_yield_operability_crosswalk.md",
        p14_decision="adopt_vocabulary_not_geometry",
        p14_followup="Map public proxy rows to ground, cable, heli, not_applicable, or review-required.",
        caveat="MP11 class vocabulary is public; the LBB polygons are not.",
    ),
    EvidenceRow(
        evidence_id="mp11_table20_thlb_area_distribution",
        evidence_family="comparison_target",
        evidence_role="aggregate_target",
        source_anchor="PDF p298 / IP p52",
        source_detail="MP11 Table 20.",
        extracted_clue="THLB area distribution is 57.3% ground, 39.6% cable, 3.1% non-conventional.",
        public_proxy_use="Use as aggregate QA target only.",
        queryable_or_local_artifact="planning/tfl6_mp11_inventory_yield_operability_crosswalk.md",
        p14_decision="comparison_target_only",
        p14_followup="Report assigned-area residuals after public proxy classification.",
        caveat="Do not force individual stands to match percentages without public evidence.",
    ),
    EvidenceRow(
        evidence_id="mp11_table73_area_volume_distribution",
        evidence_family="comparison_target",
        evidence_role="aggregate_target",
        source_anchor="PDF p405 / IP p159",
        source_detail="MP11 Table 73.",
        extracted_clue=(
            "Current THLB is 68,845 ha and 19,216,294 m3 ground; 47,524 ha and "
            "14,563,331 m3 cable; 3,730 ha and 2,223,221 m3 non-conventional."
        ),
        public_proxy_use="Use as area and volume QA target.",
        queryable_or_local_artifact="planning/tfl6_mp11_phase14_harvest_system_operability_plan.md",
        p14_decision="comparison_target_only",
        p14_followup="Compare proxy area and candidate inventory volume by harvest system.",
        caveat="Candidate THLB is larger than MP11; residuals must be area-normalized.",
    ),
    EvidenceRow(
        evidence_id="mp11_helicopter_economic_thresholds_near",
        evidence_family="economic_operability",
        evidence_role="explicit_rule_candidate",
        source_anchor="PDF p311-312 / IP p65-66",
        source_detail="MP11 Table 27.",
        extracted_clue=(
            "For age >80 years and 0-499 m flight distance: minimum 350 m3/ha "
            "and minimum 15% Cw+Fd+Yc."
        ),
        public_proxy_use="Use if age, volume, species share, and flight/access proxy exist.",
        queryable_or_local_artifact="data/mp11_model_input_bundle/input_geometry/aflb_current.feather",
        p14_decision="candidate_rule_after_metric_build",
        p14_followup="P14.3 must build species-share, volume, age, and access-distance proxy fields.",
        caveat="Flight distance is not yet a reviewed public metric.",
    ),
    EvidenceRow(
        evidence_id="mp11_helicopter_economic_thresholds_mid",
        evidence_family="economic_operability",
        evidence_role="explicit_rule_candidate",
        source_anchor="PDF p311-312 / IP p65-66",
        source_detail="MP11 Table 27.",
        extracted_clue=(
            "For age >80 years and 500-999 m flight distance: minimum 370 m3/ha "
            "and minimum 25% Cw+Fd+Yc."
        ),
        public_proxy_use="Use if age, volume, species share, and flight/access proxy exist.",
        queryable_or_local_artifact="data/mp11_model_input_bundle/input_geometry/aflb_current.feather",
        p14_decision="candidate_rule_after_metric_build",
        p14_followup="P14.3 must build species-share, volume, age, and access-distance proxy fields.",
        caveat="Flight distance is not yet a reviewed public metric.",
    ),
    EvidenceRow(
        evidence_id="mp11_helicopter_economic_thresholds_far",
        evidence_family="economic_operability",
        evidence_role="explicit_rule_candidate",
        source_anchor="PDF p311-312 / IP p65-66",
        source_detail="MP11 Table 27.",
        extracted_clue=(
            "For age >80 years and 1000+ m flight distance: minimum 400 m3/ha "
            "and minimum 30% Cw+Fd+Yc."
        ),
        public_proxy_use="Use if age, volume, species share, and flight/access proxy exist.",
        queryable_or_local_artifact="data/mp11_model_input_bundle/input_geometry/aflb_current.feather",
        p14_decision="candidate_rule_after_metric_build",
        p14_followup="P14.3 must build species-share, volume, age, and access-distance proxy fields.",
        caveat="Flight distance is not yet a reviewed public metric.",
    ),
    EvidenceRow(
        evidence_id="mp11_conventional_economic_assumption",
        evidence_family="economic_operability",
        evidence_role="rule_boundary",
        source_anchor="PDF p311-312 / IP p65-66",
        source_detail="MP11 Section 6.13 and Tables 28-29.",
        extracted_clue=(
            "MP11 assumes all conventionally operable areas become economically "
            "viable at some market point; only 20 ha of non-conventional uneconomic "
            "area are netted from THLB."
        ),
        public_proxy_use="Do not add a broad conventional uneconomic exclusion in Phase 14.",
        queryable_or_local_artifact="planning/tfl6_mp11_inventory_yield_operability_crosswalk.md",
        p14_decision="boundary_condition",
        p14_followup="Limit economic-operability rule work to heli/non-conventional sensitivity.",
        caveat="Conventional economics are not a public cost model.",
    ),
    EvidenceRow(
        evidence_id="mp11_no_current_system_dbh_mha",
        evidence_family="rule_rejection",
        evidence_role="do_not_use",
        source_anchor="PDF p400 / IP p154",
        source_detail="MP11 Section 10.4.1.",
        extracted_clue=(
            "MP11 replaces prior ground/cable/helicopter DBH thresholds with "
            "95% CMAI plus 350 m3/ha minimum volume."
        ),
        public_proxy_use="Do not use MP10 30/37/42 cm DBH rules as current MP11 criteria.",
        queryable_or_local_artifact="planning/tfl6_mp11_phase14_harvest_system_operability_plan.md",
        p14_decision="reject_as_current_mp11_rule",
        p14_followup="Keep MHA implementation separate from harvest-system classifier.",
        caveat="Historical DBH thresholds can be context only.",
    ),
    EvidenceRow(
        evidence_id="mp10_slope_30_ground_cable_context",
        evidence_family="historical_context",
        evidence_role="proxy_clue",
        source_anchor="planning/tfl6_operability_netdown_proxy.md",
        source_detail="MP10 evidence summarized from local extracted text.",
        extracted_clue=(
            "MP10 assigned conventionally operable 0-30% slopes to ground-based "
            "systems and steeper conventional slopes to cable."
        ),
        public_proxy_use="Use as a candidate proxy threshold to test, not as MP11 truth.",
        queryable_or_local_artifact="planning/tfl6_operability_netdown_proxy.md",
        p14_decision="candidate_proxy_clue",
        p14_followup="P14.3 should compute slope-threshold sensitivity metrics including 30%.",
        caveat="MP11 says ground and cable may be used together within operating areas.",
    ),
    EvidenceRow(
        evidence_id="p9d_public_cded_slope_stats",
        evidence_family="public_proxy_input",
        evidence_role="slope_metric",
        source_anchor="planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.md",
        source_detail="P9D public DEM percent-slope zonal statistics.",
        extracted_clue=(
            "CDED-derived slope stats exist for Step 210 active P9RF fragments "
            "with 60/70/80/90% thresholds."
        ),
        public_proxy_use="Use as coarse public slope evidence for first classifier pass.",
        queryable_or_local_artifact="planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.csv",
        p14_decision="accepted_public_proxy_input",
        p14_followup="P14.3 must join or aggregate slope metrics onto candidate stands.",
        caveat="CDED is coarse and not WFP LiDAR slope.",
    ),
    EvidenceRow(
        evidence_id="p9d_step220_steep_slope_rule",
        evidence_family="public_proxy_input",
        evidence_role="slope_rule_context",
        source_anchor="planning/tfl6_mp11_p9d_step220_dem_slope_scenarios.md",
        source_detail="P9D selected Step 220 steep-slope public proxy.",
        extracted_clue=(
            "Best whole-fragment candidate was slope_ge_70_prop_ge_0.75, "
            "deducting 1,801.705 ha against MP11 target 1,820 ha."
        ),
        public_proxy_use="Use as high-steepness context for inoperable/high-cost flags.",
        queryable_or_local_artifact="planning/tfl6_mp11_p9d_step220_dem_slope_scenarios.csv",
        p14_decision="accepted_public_proxy_context",
        p14_followup="Do not double-count Step 220 removed fragments as heli candidates.",
        caveat="This is a netdown proxy, not a yarding-system rule.",
    ),
    EvidenceRow(
        evidence_id="p9e_public_tsm_class_v",
        evidence_family="public_proxy_input",
        evidence_role="terrain_stability_context",
        source_anchor="planning/tfl6_mp11_p9e_step210_tsm_scenarios.md",
        source_detail="P9E public TSM Class V proxy for MP11 Step 210.",
        extracted_clue=(
            "Strict public TSM Class V source exists but deducts far less area "
            "than MP11, leaving a WFP DTSM/LiDAR semantic gap."
        ),
        public_proxy_use="Use as terrain-stability caveat/context, not direct harvest-system class.",
        queryable_or_local_artifact="planning/tfl6_mp11_p9e_step210_tsm_scenarios.csv",
        p14_decision="context_only_public_proxy",
        p14_followup="Carry terrain-stability status into classifier confidence/caveat fields.",
        caveat="Low coverage prevents treating TSM as WFP terrain model equivalent.",
    ),
    EvidenceRow(
        evidence_id="phase9_vri_inventory_metrics",
        evidence_family="public_proxy_input",
        evidence_role="inventory_metric",
        source_anchor="planning/tfl6_mp11_phase9_input_proxy_profile.md",
        source_detail="P9.3 inventory and proxy field profile.",
        extracted_clue=(
            "R1/VRI contains candidate low-height, low-volume, hembal-height3, "
            "age, species, volume, and stand-attribute fields."
        ),
        public_proxy_use="Use for volume/ha, age, height, and species-share classifier metrics.",
        queryable_or_local_artifact="data/mp11_model_input_bundle/input_geometry/aflb_current.feather",
        p14_decision="accepted_public_proxy_input",
        p14_followup="P14.3 must build Cw+Fd+Yc share and volume/age fields from candidate geometry.",
        caveat="Inventory fields are public proxies and may not match WFP LiDAR/ITI values.",
    ),
    EvidenceRow(
        evidence_id="phase9_dra_roads",
        evidence_family="public_proxy_input",
        evidence_role="access_metric_candidate",
        source_anchor="planning/tfl6_mp11_phase9_source_layer_manifest.md",
        source_detail="P9.2 source-layer manifest.",
        extracted_clue="DRA roads for TFL 6 are present and readable: 10,706 features, 4,255.863 km.",
        public_proxy_use="Candidate access-distance input for heli economic proxy.",
        queryable_or_local_artifact="data/source/tfl_6/roads",
        p14_decision="candidate_metric_after_review",
        p14_followup="P14.3 should compute a distance-to-road/access proxy only after source path review.",
        caveat="Road distance is not the same as MP11 helicopter flight distance.",
    ),
    EvidenceRow(
        evidence_id="phase9_wfp_lbb_iti_lefi_manifest_gap",
        evidence_family="private_gap",
        evidence_role="do_not_materialize",
        source_anchor="planning/tfl6_mp11_phase9_source_layer_manifest.md",
        source_detail="P9.2 source-layer manifest private dependency row.",
        extracted_clue="WFP LBB, ITI, and LEFI are marked unavailable_non_public.",
        public_proxy_use="Use only as a documented gap.",
        queryable_or_local_artifact="none",
        p14_decision="private_gap",
        p14_followup="Keep private dependency gap visible in classifier QA and docs.",
        caveat="Do not invent or publish proprietary source values.",
    ),
]


def _write_csv(rows: list[EvidenceRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def _summary(rows: list[EvidenceRow]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "evidence_family_counts": dict(Counter(row.evidence_family for row in rows)),
        "evidence_role_counts": dict(Counter(row.evidence_role for row in rows)),
        "p14_decision_counts": dict(Counter(row.p14_decision for row in rows)),
        "ready_public_proxy_input_rows": sum(
            row.p14_decision == "accepted_public_proxy_input" for row in rows
        ),
        "comparison_target_rows": sum(
            row.p14_decision == "comparison_target_only" for row in rows
        ),
        "candidate_rule_rows": sum(
            row.p14_decision == "candidate_rule_after_metric_build" for row in rows
        ),
        "private_gap_rows": sum(
            row.p14_decision in {"unavailable_private_source", "private_gap"}
            for row in rows
        ),
    }


def _write_json(rows: list[EvidenceRow], path: Path) -> dict[str, Any]:
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "phase": "P14.2",
        "status": "harvest_system_evidence_inventory_built",
        "summary": _summary(rows),
        "rows": [asdict(row) for row in rows],
        "boundary": (
            "This inventory mines evidence and public proxy candidates only. It does not "
            "generate classifier metrics, model-input tables, XML, Matrix Builder outputs, "
            "Patchworks runtime artifacts, or scenario outputs."
        ),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def _write_md(rows: list[EvidenceRow], payload: dict[str, Any], path: Path) -> None:
    summary = payload["summary"]
    lines = [
        "# TFL 6 MP11 Phase 14 Harvest-System Evidence Inventory",
        "",
        "This P14.2 inventory records MP11, historical, and public-source clues for "
        "the harvest-system operability classifier. It is evidence mining only: no "
        "classifier metrics, model-input tables, ForestModel XML, Matrix Builder "
        "outputs, Patchworks runtime artifacts, or scenario outputs are generated.",
        "",
        "## Summary",
        "",
        f"- status: `{payload['status']}`",
        f"- row_count: `{summary['row_count']}`",
        f"- accepted public proxy input rows: `{summary['ready_public_proxy_input_rows']}`",
        f"- comparison target rows: `{summary['comparison_target_rows']}`",
        f"- candidate rule rows: `{summary['candidate_rule_rows']}`",
        f"- private gap rows: `{summary['private_gap_rows']}`",
        "",
        "## Decision Counts",
        "",
        "| P14 decision | Count |",
        "| --- | ---: |",
    ]
    for decision, count in sorted(summary["p14_decision_counts"].items()):
        lines.append(f"| `{decision}` | `{count}` |")
    lines.extend(
        [
            "",
            "## Evidence Rows",
            "",
            "| Evidence | Family | Role | Decision | Public/proxy use | Follow-up |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"`{row.evidence_id}` | `{row.evidence_family}` | `{row.evidence_role}` | "
            f"`{row.p14_decision}` | {row.public_proxy_use} | {row.p14_followup} |"
        )
    lines.extend(
        [
            "",
            "## Key Interpretation",
            "",
            "- WFP LBB is the governing MP11 source for harvest-system assignment, but it "
            "is not public/queryable in the current package.",
            "- Public FEMIC work should use transparent proxy assignments with source, "
            "confidence, and caveat fields rather than claiming WFP LBB equivalence.",
            "- MP11 Table 20 and Table 73 distributions are aggregate QA targets only.",
            "- Helicopter economic-operability thresholds are explicit enough to become "
            "candidate rules after P14.3 builds age, volume, species-share, and "
            "access/flight-distance proxy metrics.",
            "- The old MP10 DBH-by-harvest-system criteria are not current MP11 MHA "
            "rules and must not be used as Phase 14 classifier acceptance criteria.",
            "",
            "## Files",
            "",
            "- `planning/tfl6_mp11_phase14_harvest_system_evidence.csv`",
            "- `planning/tfl6_mp11_phase14_harvest_system_evidence.json`",
            "- `planning/tfl6_mp11_phase14_harvest_system_evidence.md`",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = list(ROWS)
    _write_csv(rows, OUT_CSV)
    payload = _write_json(rows, OUT_JSON)
    _write_md(rows, payload, OUT_MD)
    print(f"wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
