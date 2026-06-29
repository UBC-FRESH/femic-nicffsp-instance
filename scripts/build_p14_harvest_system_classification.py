"""Build P14.4 harvest-system proxy classifications and QA tables."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "planning"

METRICS_CSV = PLANNING / "tfl6_mp11_phase14_public_proxy_metrics.csv"

OUT_CLASS_CSV = PLANNING / "tfl6_mp11_phase14_harvest_system_classification.csv"
OUT_QA_CSV = PLANNING / "tfl6_mp11_phase14_harvest_system_classification_qa.csv"
OUT_JSON = PLANNING / "tfl6_mp11_phase14_harvest_system_classification.json"
OUT_MD = PLANNING / "tfl6_mp11_phase14_harvest_system_classification.md"

MP11_TARGETS = {
    "ground": {
        "mp11_label": "ground",
        "target_area_ha": 68845.0,
        "target_volume_m3": 19216294.0,
        "target_area_share_pct": 57.3,
        "target_volume_share_pct": 53.4,
    },
    "cable": {
        "mp11_label": "cable",
        "target_area_ha": 47524.0,
        "target_volume_m3": 14563331.0,
        "target_area_share_pct": 39.6,
        "target_volume_share_pct": 40.5,
    },
    "heli": {
        "mp11_label": "non_conventional_heli",
        "target_area_ha": 3730.0,
        "target_volume_m3": 2223221.0,
        "target_area_share_pct": 3.1,
        "target_volume_share_pct": 6.2,
    },
}

CLASS_COLUMNS = [
    "stand_id",
    "source_polygon_key",
    "is_managed_current_thlb",
    "thlb_area_ha",
    "volume_metric_m3_ha",
    "candidate_volume_m3",
    "harvest_system_candidate",
    "harvest_system_source",
    "harvest_system_confidence",
    "harvest_system_rule",
    "heli_economic_proxy_pass",
    "slope_mean_pct",
    "slope_p90_pct",
    "nearest_dra_road_m",
    "access_distance_proxy_bin",
    "cw_fd_yc_pct",
    "metric_missing_fields",
    "classification_caveat",
]


def _repo(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _num(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(frame[column], errors="coerce")


def _classify_row(row: pd.Series) -> tuple[str, str, str, str]:
    if not bool(row["is_managed_current_thlb"]):
        return (
            "not_applicable",
            "p14_4_non_current_managed_thlb",
            "not_applicable",
            "stand is outside managed current THLB",
        )

    slope_mean = row["slope_mean_pct"]
    slope_p90 = row["slope_p90_pct"]
    road_distance = row["nearest_dra_road_m"]
    heli_pass = bool(row["heli_economic_proxy_pass"])

    remote_or_steep = False
    if pd.notna(road_distance) and float(road_distance) >= 1000.0:
        remote_or_steep = True
    if pd.notna(slope_p90) and float(slope_p90) >= 80.0:
        remote_or_steep = True

    if heli_pass and remote_or_steep:
        return (
            "heli",
            "mp11_tables_27_29_public_proxy",
            "medium",
            "heli economic test passed and stand has remote or steep public-proxy context",
        )

    if pd.notna(slope_mean):
        if float(slope_mean) >= 30.0:
            return (
                "cable",
                "p9d_cded_slope_proxy",
                "medium",
                "public CDED mean slope >= 30 percent",
            )
        return (
            "ground",
            "p9d_cded_slope_proxy",
            "medium",
            "public CDED mean slope < 30 percent",
        )

    if pd.notna(road_distance) and float(road_distance) > 1500.0:
        return (
            "cable",
            "dra_road_distance_fallback",
            "low",
            "missing slope; nearest DRA road distance > 1500 m fallback",
        )

    return (
        "ground",
        "dra_road_distance_fallback",
        "low",
        "missing slope; nearest DRA road distance <= 1500 m fallback",
    )


def _build_classification() -> pd.DataFrame:
    metrics = pd.read_csv(METRICS_CSV)
    for column in [
        "thlb_area_ha",
        "volume_metric_m3_ha",
        "slope_mean_pct",
        "slope_p90_pct",
        "nearest_dra_road_m",
        "cw_fd_yc_pct",
    ]:
        metrics[column] = _num(metrics, column)
    metrics["candidate_volume_m3"] = metrics["thlb_area_ha"] * metrics["volume_metric_m3_ha"]

    classifications = metrics.apply(_classify_row, axis=1, result_type="expand")
    classifications.columns = [
        "harvest_system_candidate",
        "harvest_system_source",
        "harvest_system_confidence",
        "harvest_system_rule",
    ]
    output = pd.concat([metrics, classifications], axis=1)
    output["classification_caveat"] = (
        "Public proxy classification only; WFP LBB geometry is unavailable, "
        "CDED slope is not WFP LiDAR slope, and DRA road distance is not "
        "MP11 helicopter flight distance."
    )
    return output[CLASS_COLUMNS]


def _safe_sum(frame: pd.DataFrame, column: str) -> float:
    return float(pd.to_numeric(frame[column], errors="coerce").fillna(0).sum())


def _build_qa(classified: pd.DataFrame) -> pd.DataFrame:
    managed = classified[classified["is_managed_current_thlb"]].copy()
    candidate_area_total = _safe_sum(managed, "thlb_area_ha")
    candidate_volume_total = _safe_sum(managed, "candidate_volume_m3")

    rows: list[dict[str, Any]] = []
    for harvest_system, target in MP11_TARGETS.items():
        subset = managed[managed["harvest_system_candidate"] == harvest_system]
        candidate_area = _safe_sum(subset, "thlb_area_ha")
        candidate_volume = _safe_sum(subset, "candidate_volume_m3")
        candidate_area_share = candidate_area / candidate_area_total * 100.0
        candidate_volume_share = candidate_volume / candidate_volume_total * 100.0
        scaled_area_target = candidate_area_total * target["target_area_share_pct"] / 100.0
        scaled_volume_target = candidate_volume_total * target["target_volume_share_pct"] / 100.0
        rows.append(
            {
                "harvest_system": harvest_system,
                "mp11_label": target["mp11_label"],
                "candidate_rows": int(len(subset)),
                "candidate_area_ha": candidate_area,
                "candidate_volume_m3": candidate_volume,
                "candidate_area_share_pct": candidate_area_share,
                "candidate_volume_share_pct": candidate_volume_share,
                "mp11_table73_area_ha": target["target_area_ha"],
                "mp11_table73_volume_m3": target["target_volume_m3"],
                "mp11_area_share_pct": target["target_area_share_pct"],
                "mp11_volume_share_pct": target["target_volume_share_pct"],
                "direct_area_residual_ha": candidate_area - target["target_area_ha"],
                "direct_volume_residual_m3": candidate_volume - target["target_volume_m3"],
                "scaled_area_target_ha": scaled_area_target,
                "scaled_volume_target_m3": scaled_volume_target,
                "scaled_area_residual_ha": candidate_area - scaled_area_target,
                "scaled_volume_residual_m3": candidate_volume - scaled_volume_target,
                "area_share_residual_pct_points": (
                    candidate_area_share - target["target_area_share_pct"]
                ),
                "volume_share_residual_pct_points": (
                    candidate_volume_share - target["target_volume_share_pct"]
                ),
                "qa_caveat": (
                    "Candidate totals use the current public-proxy THLB scaffold and "
                    "public VRI volume proxies; direct residuals are not WFP LBB "
                    "stand-level errors."
                ),
            }
        )
    rows.append(
        {
            "harvest_system": "managed_current_thlb_total",
            "mp11_label": "table73_total",
            "candidate_rows": int(len(managed)),
            "candidate_area_ha": candidate_area_total,
            "candidate_volume_m3": candidate_volume_total,
            "candidate_area_share_pct": 100.0,
            "candidate_volume_share_pct": 100.0,
            "mp11_table73_area_ha": sum(v["target_area_ha"] for v in MP11_TARGETS.values()),
            "mp11_table73_volume_m3": sum(
                v["target_volume_m3"] for v in MP11_TARGETS.values()
            ),
            "mp11_area_share_pct": 100.0,
            "mp11_volume_share_pct": 100.0,
            "direct_area_residual_ha": (
                candidate_area_total
                - sum(v["target_area_ha"] for v in MP11_TARGETS.values())
            ),
            "direct_volume_residual_m3": (
                candidate_volume_total
                - sum(v["target_volume_m3"] for v in MP11_TARGETS.values())
            ),
            "scaled_area_target_ha": candidate_area_total,
            "scaled_volume_target_m3": candidate_volume_total,
            "scaled_area_residual_ha": 0.0,
            "scaled_volume_residual_m3": 0.0,
            "area_share_residual_pct_points": 0.0,
            "volume_share_residual_pct_points": 0.0,
            "qa_caveat": (
                "Total row shows the candidate scaffold total before later model-input "
                "promotion; Phase 14 does not change THLB truth by itself."
            ),
        }
    )
    return pd.DataFrame(rows)


def _write_csvs(classified: pd.DataFrame, qa: pd.DataFrame) -> None:
    OUT_CLASS_CSV.parent.mkdir(parents=True, exist_ok=True)
    classified.to_csv(OUT_CLASS_CSV, index=False, quoting=csv.QUOTE_MINIMAL)
    qa.to_csv(OUT_QA_CSV, index=False, quoting=csv.QUOTE_MINIMAL)


def _summary(classified: pd.DataFrame, qa: pd.DataFrame) -> dict[str, Any]:
    managed = classified[classified["is_managed_current_thlb"]].copy()
    by_system = (
        managed.groupby("harvest_system_candidate")
        .agg(
            rows=("stand_id", "count"),
            area_ha=("thlb_area_ha", "sum"),
            volume_m3=("candidate_volume_m3", "sum"),
        )
        .reset_index()
        .to_dict(orient="records")
    )
    by_confidence = (
        managed.groupby(["harvest_system_candidate", "harvest_system_confidence"])
        .agg(rows=("stand_id", "count"), area_ha=("thlb_area_ha", "sum"))
        .reset_index()
        .to_dict(orient="records")
    )
    return {
        "row_count": int(len(classified)),
        "managed_current_thlb_rows": int(len(managed)),
        "managed_current_thlb_area_ha": _safe_sum(managed, "thlb_area_ha"),
        "managed_current_thlb_volume_m3": _safe_sum(managed, "candidate_volume_m3"),
        "classification_counts": (
            classified["harvest_system_candidate"].value_counts().to_dict()
        ),
        "managed_classification_area_by_system": by_system,
        "managed_classification_area_by_confidence": by_confidence,
        "qa_rows": qa.to_dict(orient="records"),
    }


def _write_json(classified: pd.DataFrame, qa: pd.DataFrame) -> dict[str, Any]:
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "phase": "P14.4",
        "status": "harvest_system_proxy_classification_built",
        "inputs": {
            "public_proxy_metrics": _repo(METRICS_CSV),
        },
        "outputs": {
            "classification_csv": _repo(OUT_CLASS_CSV),
            "qa_csv": _repo(OUT_QA_CSV),
            "summary_json": _repo(OUT_JSON),
            "summary_md": _repo(OUT_MD),
        },
        "classification_rules": [
            "not_applicable for stands outside managed current THLB",
            (
                "heli when MP11 Tables 27-29 economic proxy passes and the stand "
                "has nearest-DRA-road distance >= 1000 m or P9D slope p90 >= 80%"
            ),
            "cable when public CDED mean slope >= 30%",
            "cable low-confidence fallback when slope is missing and DRA distance > 1500 m",
            "ground when public CDED mean slope < 30%",
            "ground low-confidence fallback when slope is missing and DRA distance <= 1500 m",
        ],
        "mp11_targets": MP11_TARGETS,
        "summary": _summary(classified, qa),
        "non_goals": [
            "No model-input tables are generated in P14.4.",
            "No ForestModel XML, Matrix Builder outputs, Patchworks runtime artifacts, or scenarios are generated.",
            "The classification is a public proxy and does not reconstruct WFP LBB.",
        ],
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def _write_md(payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# TFL 6 MP11 Phase 14 Harvest-System Classification",
        "",
        "This P14.4 output classifies the MP11 candidate stands into public-proxy "
        "harvest-system lanes and compares aggregate area/volume against MP11 "
        "Table 20/Table 73 targets. It does not generate model-input tables, "
        "ForestModel XML, Matrix Builder outputs, Patchworks runtime artifacts, "
        "or scenario outputs.",
        "",
        "## Summary",
        "",
        f"- status: `{payload['status']}`",
        f"- row_count: `{summary['row_count']}`",
        f"- managed_current_thlb_rows: `{summary['managed_current_thlb_rows']}`",
        f"- managed_current_thlb_area_ha: `{summary['managed_current_thlb_area_ha']:.3f}`",
        (
            "- managed_current_thlb_volume_m3: "
            f"`{summary['managed_current_thlb_volume_m3']:.3f}`"
        ),
        "",
        "## Managed Current THLB By Candidate System",
        "",
        "| System | Rows | Area ha | Volume m3 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in summary["managed_classification_area_by_system"]:
        lines.append(
            "| `{}` | `{}` | `{:.3f}` | `{:.3f}` |".format(
                row["harvest_system_candidate"],
                row["rows"],
                row["area_ha"],
                row["volume_m3"],
            )
        )
    lines.extend(
        [
            "",
            "## MP11 Table 73 QA",
            "",
            (
                "| System | Candidate area ha | MP11 area ha | Area share residual pp | "
                "Candidate volume m3 | MP11 volume m3 | Volume share residual pp |"
            ),
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in summary["qa_rows"]:
        if row["harvest_system"] == "managed_current_thlb_total":
            continue
        lines.append(
            "| `{}` | `{:.3f}` | `{:.3f}` | `{:.3f}` | `{:.3f}` | `{:.3f}` | `{:.3f}` |".format(
                row["harvest_system"],
                row["candidate_area_ha"],
                row["mp11_table73_area_ha"],
                row["area_share_residual_pct_points"],
                row["candidate_volume_m3"],
                row["mp11_table73_volume_m3"],
                row["volume_share_residual_pct_points"],
            )
        )
    lines.extend(
        [
            "",
            "## Classification Rules",
            "",
        ]
    )
    for rule in payload["classification_rules"]:
        lines.append(f"- {rule}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- WFP LBB geometry is unavailable; these are public proxy assignments.",
            "- CDED slope is not WFP LiDAR slope.",
            "- DRA road distance is not MP11 helicopter flight distance.",
            "- Public VRI volume is not WFP ITI volume.",
            "- P14.5 may use these classifications as candidate inputs only after "
            "reviewing the QA residuals and caveats.",
            "",
            "## Files",
            "",
            "- `planning/tfl6_mp11_phase14_harvest_system_classification.csv`",
            "- `planning/tfl6_mp11_phase14_harvest_system_classification_qa.csv`",
            "- `planning/tfl6_mp11_phase14_harvest_system_classification.json`",
            "- `planning/tfl6_mp11_phase14_harvest_system_classification.md`",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    classified = _build_classification()
    qa = _build_qa(classified)
    _write_csvs(classified, qa)
    payload = _write_json(classified, qa)
    _write_md(payload)
    print(f"wrote {_repo(OUT_CLASS_CSV)}")
    print(f"wrote {_repo(OUT_QA_CSV)}")
    print(f"wrote {_repo(OUT_JSON)}")
    print(f"wrote {_repo(OUT_MD)}")


if __name__ == "__main__":
    main()
