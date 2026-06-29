"""Build the P11.4c MP11 candidate model-input bundle scaffold."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
PHASE5_BUNDLE_ROOT = INSTANCE_ROOT / "data" / "model_input_bundle"
DEFAULT_OUTPUT_ROOT = INSTANCE_ROOT / "data" / "mp11_model_input_bundle"
MANAGED_CURVES_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.csv"
MANAGED_COMPARISON_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.csv"
)
DEFAULT_SUMMARY_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_candidate_bundle_build_summary.csv"
)
DEFAULT_SUMMARY_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_candidate_bundle_build_summary.json"
)
DEFAULT_SUMMARY_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_candidate_bundle_build_summary.md"
)

TSA_CODE = "tfl6"
NUMERIC_AU_START = 6_000_001
NUMERIC_CURVE_START = 610_000_001


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {_repo_relative(path)}")


def _safe_replace_bundle_root(source_root: Path, output_root: Path) -> None:
    resolved = output_root.resolve()
    expected = (INSTANCE_ROOT / "data" / "mp11_model_input_bundle").resolve()
    if resolved != expected:
        raise ValueError(f"Refusing to replace unexpected output root: {output_root}")
    if output_root.exists():
        shutil.rmtree(output_root)
    shutil.copytree(source_root, output_root)


def _load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    _require_file(MANAGED_CURVES_CSV)
    _require_file(MANAGED_COMPARISON_CSV)
    managed = pd.read_csv(MANAGED_CURVES_CSV)
    comparison = pd.read_csv(MANAGED_COMPARISON_CSV)
    required_managed = {"feature_id", "canonical_au_id", "age", "treated_volume"}
    missing_managed = required_managed.difference(managed.columns)
    if missing_managed:
        raise ValueError(f"Managed curves missing columns: {sorted(missing_managed)}")
    required_comparison = {
        "mp11_feature_id",
        "canonical_au_id",
        "mp11_thlb_area_ha",
        "review_status",
    }
    missing_comparison = required_comparison.difference(comparison.columns)
    if missing_comparison:
        raise ValueError(
            f"Managed comparison missing columns: {sorted(missing_comparison)}"
        )
    return managed, comparison


def _select_active_mp11_curves(comparison: pd.DataFrame) -> pd.DataFrame:
    accepted = comparison[
        comparison["review_status"].astype(str) == "accepted_for_phase11_curve_handoff"
    ].copy()
    if accepted.empty:
        raise ValueError("No accepted Phase 10R curve-handoff rows found.")
    accepted["mp11_thlb_area_ha_numeric"] = pd.to_numeric(
        accepted["mp11_thlb_area_ha"], errors="coerce"
    ).fillna(0.0)
    accepted["mp11_feature_id"] = pd.to_numeric(
        accepted["mp11_feature_id"], errors="raise"
    ).astype(int)
    accepted = accepted.sort_values(
        ["canonical_au_id", "mp11_thlb_area_ha_numeric", "mp11_feature_id"],
        ascending=[True, False, True],
    )
    selected = accepted.drop_duplicates(subset=["canonical_au_id"], keep="first").copy()
    selected["candidate_curve_id"] = "mp11_table57_future_managed_" + selected[
        "canonical_au_id"
    ].astype(str)
    return selected


def _inject_mp11_managed_curves(
    *,
    bundle_root: Path,
    managed_curves: pd.DataFrame,
    selected_curves: pd.DataFrame,
) -> dict[str, Any]:
    curve_table_path = bundle_root / "curve_table.csv"
    curve_points_path = bundle_root / "curve_points_table.csv"
    au_table_path = bundle_root / "au_table.csv"
    stand_table_path = bundle_root / "stand_table.csv"
    stand_au_assignment_path = bundle_root / "stand_au_assignment.csv"
    stand_origin_assignment_path = bundle_root / "stand_origin_assignment.csv"

    curve_table = pd.read_csv(curve_table_path)
    curve_points = pd.read_csv(curve_points_path)
    au_table = pd.read_csv(au_table_path)
    stand_table = pd.read_csv(stand_table_path)
    stand_au_assignment = pd.read_csv(stand_au_assignment_path)
    stand_origin_assignment = pd.read_csv(stand_origin_assignment_path)

    active_by_feature = selected_curves.set_index("mp11_feature_id")
    active_feature_ids = set(active_by_feature.index.astype(int))
    managed_curves = managed_curves.copy()
    managed_curves["feature_id"] = pd.to_numeric(
        managed_curves["feature_id"], errors="raise"
    ).astype(int)
    active_points = managed_curves[
        managed_curves["feature_id"].isin(active_feature_ids)
    ].copy()

    selected_curve_ids = set(selected_curves["candidate_curve_id"].astype(str))
    curve_table = curve_table[
        ~curve_table["curve_id"].astype(str).isin(selected_curve_ids)
    ].copy()
    curve_points = curve_points[
        ~curve_points["curve_id"].astype(str).isin(selected_curve_ids)
    ].copy()

    curve_rows: list[dict[str, Any]] = []
    for row in selected_curves.itertuples(index=False):
        curve_rows.append(
            {
                "curve_id": row.candidate_curve_id,
                "au_id": row.canonical_au_id,
                "curve_family": "future_managed_tipsy_mp11_table57",
                "curve_lane": "future_managed_mp11_table57",
                "source_table": "planning/tfl6_mp11_managed_curves.csv",
                "tipsy_feature_id": int(row.mp11_feature_id),
                "match_confidence": "accepted_phase10r_handoff",
            }
        )

    selected_lookup = selected_curves.set_index("mp11_feature_id")[
        ["candidate_curve_id", "canonical_au_id"]
    ].to_dict("index")
    point_rows: list[dict[str, Any]] = []
    for row in active_points.itertuples(index=False):
        selected = selected_lookup[int(row.feature_id)]
        point_rows.append(
            {
                "curve_id": selected["candidate_curve_id"],
                "au_id": selected["canonical_au_id"],
                "curve_family": "future_managed_tipsy_mp11_table57",
                "age": int(row.age),
                "volume_m3_per_ha": float(row.treated_volume),
            }
        )

    curve_table = pd.concat([curve_table, pd.DataFrame(curve_rows)], ignore_index=True)
    curve_points = pd.concat(
        [curve_points, pd.DataFrame(point_rows)], ignore_index=True
    )

    active_curve_by_au = dict(
        zip(
            selected_curves["canonical_au_id"].astype(str),
            selected_curves["candidate_curve_id"].astype(str),
            strict=True,
        )
    )
    active_aus = set(active_curve_by_au)

    def _candidate_curve_for_au(au_id: Any, original_curve: Any) -> Any:
        return active_curve_by_au.get(str(au_id), original_curve)

    au_table["treated_curve_id"] = [
        _candidate_curve_for_au(au_id, curve_id)
        for au_id, curve_id in zip(
            au_table["canonical_curve_au_id"], au_table["treated_curve_id"], strict=True
        )
    ]
    stand_table["treated_curve_id"] = [
        _candidate_curve_for_au(au_id, curve_id)
        for au_id, curve_id in zip(
            stand_table["canonical_curve_au_id"],
            stand_table["treated_curve_id"],
            strict=True,
        )
    ]
    stand_au_assignment["treated_curve_id"] = [
        _candidate_curve_for_au(au_id, curve_id)
        for au_id, curve_id in zip(
            stand_au_assignment["canonical_curve_au_id"],
            stand_au_assignment["treated_curve_id"],
            strict=True,
        )
    ]
    stand_origin_assignment["treated_curve_id"] = [
        active_curve_by_au.get(str(stand_au), curve_id)
        for stand_au, curve_id in zip(
            stand_table["canonical_curve_au_id"],
            stand_origin_assignment["treated_curve_id"],
            strict=True,
        )
    ]

    curve_table.to_csv(curve_table_path, index=False)
    curve_points.to_csv(curve_points_path, index=False)
    au_table.to_csv(au_table_path, index=False)
    stand_table.to_csv(stand_table_path, index=False)
    stand_au_assignment.to_csv(stand_au_assignment_path, index=False)
    stand_origin_assignment.to_csv(stand_origin_assignment_path, index=False)

    affected_stands = int(
        stand_table["canonical_curve_au_id"].astype(str).isin(active_aus).sum()
    )
    return {
        "active_mp11_curve_count": int(len(selected_curves)),
        "active_mp11_curve_point_rows": int(len(point_rows)),
        "affected_stand_rows": affected_stands,
        "affected_au_rows": int(
            au_table["canonical_curve_au_id"].astype(str).isin(active_aus).sum()
        ),
    }


def _build_export_compat(bundle_root: Path) -> dict[str, Any]:
    compat_root = bundle_root / "export_compat"
    compat_root.mkdir(parents=True, exist_ok=True)

    au_table = pd.read_csv(bundle_root / "au_table.csv")
    curve_table = pd.read_csv(bundle_root / "curve_table.csv")
    curve_points = pd.read_csv(bundle_root / "curve_points_table.csv")
    checkpoint = pd.read_feather(compat_root / "aflb_current_export_compat.feather")

    au_values = sorted(au_table["au_id"].astype(str).unique())
    au_map = {au_id: NUMERIC_AU_START + idx for idx, au_id in enumerate(au_values)}

    referenced_curves = sorted(
        set(au_table["natural_curve_id"].astype(str))
        | set(au_table["treated_curve_id"].astype(str))
    )
    curve_map = {
        curve_id: NUMERIC_CURVE_START + idx
        for idx, curve_id in enumerate(referenced_curves)
    }

    export_au = au_table.copy()
    if "si_level" not in export_au.columns:
        if "si_class" not in export_au.columns:
            raise ValueError("Candidate AU table missing `si_level`/`si_class`.")
        export_au["si_level"] = export_au["si_class"]
    export_au["tsa"] = TSA_CODE
    export_au["source_local_au_id"] = export_au["au_id"].astype(str).map(au_map)
    export_au["source_managed_local_au_id"] = export_au["source_local_au_id"]
    export_au["source_unmanaged_local_au_id"] = export_au["source_local_au_id"]
    export_au["untreated_curve_id"] = (
        export_au["natural_curve_id"].astype(str).map(curve_map)
    )
    export_au["treated_curve_id"] = (
        export_au["treated_curve_id"].astype(str).map(curve_map)
    )
    export_au["unmanaged_curve_id"] = export_au["untreated_curve_id"]
    export_au["managed_curve_id"] = export_au["treated_curve_id"]
    export_au["au_id_string"] = export_au["au_id"].astype(str)
    export_au["au_id"] = export_au["au_id_string"].map(au_map)
    export_au = export_au[
        [
            "au_id",
            "tsa",
            "stratum_code",
            "si_level",
            "source_local_au_id",
            "source_managed_local_au_id",
            "source_unmanaged_local_au_id",
            "untreated_curve_id",
            "treated_curve_id",
            "unmanaged_curve_id",
            "managed_curve_id",
            "au_id_string",
            "canonical_curve_au_id",
        ]
    ]

    missing_curve_rows = sorted(
        set(referenced_curves) - set(curve_table["curve_id"].astype(str))
    )
    if missing_curve_rows:
        raise ValueError(
            f"Missing curve_table rows for referenced curves: {missing_curve_rows[:10]}"
        )

    curve_subset = curve_table[
        curve_table["curve_id"].astype(str).isin(referenced_curves)
    ].copy()
    curve_subset["curve_id_string"] = curve_subset["curve_id"].astype(str)
    curve_subset["curve_id"] = curve_subset["curve_id_string"].map(curve_map)
    curve_subset["curve_type"] = [
        "untreated" if str(curve_id).startswith("nat_") else "treated"
        for curve_id in curve_subset["curve_id_string"]
    ]
    export_curve = curve_subset[
        [
            "curve_id",
            "curve_type",
            "curve_id_string",
            "au_id",
            "curve_family",
            "curve_lane",
        ]
    ].copy()

    points_subset = curve_points[
        curve_points["curve_id"].astype(str).isin(referenced_curves)
    ].copy()
    points_subset["curve_id_string"] = points_subset["curve_id"].astype(str)
    points_subset["curve_id"] = points_subset["curve_id_string"].map(curve_map)
    points_subset["x"] = pd.to_numeric(points_subset["age"], errors="raise").astype(int)
    points_subset["y"] = pd.to_numeric(
        points_subset["volume_m3_per_ha"], errors="raise"
    ).astype(float)
    export_points = points_subset[
        ["curve_id", "x", "y", "curve_id_string", "au_id", "curve_family"]
    ].copy()

    checkpoint = checkpoint.copy()
    checkpoint["bundle_au_id"] = checkpoint["bundle_au_id"].astype(str)
    checkpoint["au"] = checkpoint["bundle_au_id"].map(au_map)
    missing_checkpoint_au_rows = int(checkpoint["au"].isna().sum())
    if missing_checkpoint_au_rows:
        raise ValueError(
            f"Compatibility checkpoint has {missing_checkpoint_au_rows} unmapped AU rows."
        )
    checkpoint["au"] = checkpoint["au"].astype(int)
    checkpoint["thlb_fact"] = pd.to_numeric(
        checkpoint["managed_share"], errors="coerce"
    ).fillna(0.0)

    id_rows = [
        {"id_family": "au", "string_id": string_id, "numeric_id": numeric_id}
        for string_id, numeric_id in au_map.items()
    ] + [
        {"id_family": "curve", "string_id": string_id, "numeric_id": numeric_id}
        for string_id, numeric_id in curve_map.items()
    ]

    export_au.to_csv(compat_root / "au_table.csv", index=False)
    export_curve.to_csv(compat_root / "curve_table.csv", index=False)
    export_points.to_csv(compat_root / "curve_points_table.csv", index=False)
    pd.DataFrame(id_rows).to_csv(compat_root / "id_crosswalk.csv", index=False)
    checkpoint.to_feather(compat_root / "aflb_current_export_compat.feather")

    manifest = {
        "generated_for": "P11.4c MP11 candidate ForestModel exporter compatibility bridge",
        "compat_dir": _repo_relative(compat_root),
        "au_rows": int(len(export_au)),
        "curve_rows": int(len(export_curve)),
        "curve_point_rows": int(len(export_points)),
        "checkpoint_rows": int(len(checkpoint)),
        "au_id_start": NUMERIC_AU_START,
        "curve_id_start": NUMERIC_CURVE_START,
        "missing_checkpoint_au_rows": missing_checkpoint_au_rows,
        "missing_unmanaged_curve_rows": int(
            export_au["unmanaged_curve_id"].isna().sum()
        ),
        "missing_managed_curve_rows": int(export_au["managed_curve_id"].isna().sum()),
        "managed_share_min": float(checkpoint["managed_share"].min()),
        "managed_share_max": float(checkpoint["managed_share"].max()),
        "age_zero_rows": int((export_points["x"] == 0).sum()),
    }
    (compat_root / "bridge_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def _record_counts(bundle_root: Path) -> dict[str, int]:
    paths = [
        "au_table.csv",
        "curve_table.csv",
        "curve_points_table.csv",
        "stand_table.csv",
        "stand_au_assignment.csv",
        "stand_origin_assignment.csv",
        "treatment_table.csv",
        "transition_table.csv",
        "group_table.csv",
        "cedar_signal_table.csv",
        "embedded_identity_table.csv",
        "export_compat/au_table.csv",
        "export_compat/curve_table.csv",
        "export_compat/curve_points_table.csv",
        "export_compat/id_crosswalk.csv",
    ]
    counts: dict[str, int] = {}
    for rel_path in paths:
        path = bundle_root / rel_path
        if path.suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as handle:
                counts[rel_path] = sum(1 for _ in csv.DictReader(handle))
    return counts


def _checksums(bundle_root: Path) -> dict[str, str]:
    rel_paths = [
        "au_table.csv",
        "curve_table.csv",
        "curve_points_table.csv",
        "stand_table.csv",
        "stand_au_assignment.csv",
        "stand_origin_assignment.csv",
        "export_compat/au_table.csv",
        "export_compat/curve_table.csv",
        "export_compat/curve_points_table.csv",
        "export_compat/bridge_manifest.json",
        "export_compat/aflb_current_export_compat.feather",
    ]
    return {rel_path: _sha256(bundle_root / rel_path) for rel_path in rel_paths}


def _write_summary(
    *,
    output_root: Path,
    output_csv: Path,
    output_json: Path,
    output_md: Path,
    payload: dict[str, Any],
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    summary_rows = [
        {"metric": key, "value": value}
        for key, value in payload["summary"].items()
        if not isinstance(value, (dict, list))
    ]
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(summary_rows)

    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# P11.4c MP11 Candidate Bundle Build Summary",
        "",
        "This build materializes the generated MP11 candidate model-input bundle "
        "and export compatibility bridge under the ignored candidate root.",
        "",
        "It does not generate ForestModel XML, Matrix Builder outputs, or "
        "Patchworks runtime artifacts.",
        "",
        "## Generated Root",
        "",
        f"- Candidate bundle root: `{_repo_relative(output_root)}`",
        f"- Export compatibility bridge: `{_repo_relative(output_root / 'export_compat')}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in payload["summary"].items():
        if not isinstance(value, (dict, list)):
            lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Record Counts",
            "",
            "| Surface | Rows |",
            "| --- | ---: |",
        ]
    )
    for surface, count in payload["record_counts"].items():
        lines.append(f"| `{surface}` | {count} |")
    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- This is an MP11 candidate scaffold, not a final MP11 release model.",
            "- The Phase 5 stand universe and treatment/transition scaffold are reused.",
            "- Accepted Phase 10R Table 57 managed curves are injected where they map "
            "deterministically to canonical AU identities.",
            "- Duplicate MP11 Table 57 rows mapping to the same canonical AU are not "
            "split into new stand AUs in this scaffold; the active row is selected "
            "by largest MP11 THLB area.",
            "- P9RF source/THLB caveats remain model-contract caveats until a later "
            "source-layer rebuild replaces the scaffold.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_candidate_bundle(
    *,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
    summary_csv: Path = DEFAULT_SUMMARY_CSV,
    summary_json: Path = DEFAULT_SUMMARY_JSON,
    summary_md: Path = DEFAULT_SUMMARY_MD,
) -> dict[str, Any]:
    if not PHASE5_BUNDLE_ROOT.exists():
        raise FileNotFoundError(
            f"Phase 5 bundle root not found: {_repo_relative(PHASE5_BUNDLE_ROOT)}"
        )

    managed_curves, comparison = _load_inputs()
    selected_curves = _select_active_mp11_curves(comparison)

    _safe_replace_bundle_root(PHASE5_BUNDLE_ROOT, output_root)
    injection_summary = _inject_mp11_managed_curves(
        bundle_root=output_root,
        managed_curves=managed_curves,
        selected_curves=selected_curves,
    )
    bridge_manifest = _build_export_compat(output_root)
    record_counts = _record_counts(output_root)
    checksums = _checksums(output_root)

    duplicate_curve_rows = int(
        comparison[
            comparison["review_status"].astype(str)
            == "accepted_for_phase11_curve_handoff"
        ].shape[0]
        - len(selected_curves)
    )
    payload = {
        "summary": {
            "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "candidate_bundle_root": _repo_relative(output_root),
            "active_mp11_curve_count": injection_summary["active_mp11_curve_count"],
            "accepted_phase10r_curve_rows": int(
                comparison[
                    comparison["review_status"].astype(str)
                    == "accepted_for_phase11_curve_handoff"
                ].shape[0]
            ),
            "duplicate_mp11_rows_deferred_by_canonical_au": duplicate_curve_rows,
            "active_mp11_curve_point_rows": injection_summary[
                "active_mp11_curve_point_rows"
            ],
            "affected_stand_rows": injection_summary["affected_stand_rows"],
            "affected_au_rows": injection_summary["affected_au_rows"],
            "export_compat_curve_rows": bridge_manifest["curve_rows"],
            "export_compat_curve_point_rows": bridge_manifest["curve_point_rows"],
            "model_input_generation": "performed_candidate_scaffold",
            "xml_generation": "not_performed",
            "matrix_builder": "not_performed",
            "runtime_bundle_generation": "not_performed",
        },
        "selected_curves": selected_curves[
            [
                "mp11_feature_id",
                "canonical_au_id",
                "candidate_curve_id",
                "mp11_thlb_area_ha",
                "review_status",
            ]
        ].to_dict(orient="records"),
        "bridge_manifest": bridge_manifest,
        "record_counts": record_counts,
        "checksums_sha256": checksums,
    }
    _write_summary(
        output_root=output_root,
        output_csv=summary_csv,
        output_json=summary_json,
        output_md=summary_md,
        payload=payload,
    )
    return payload["summary"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--summary-csv", type=Path, default=DEFAULT_SUMMARY_CSV)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY_JSON)
    parser.add_argument("--summary-md", type=Path, default=DEFAULT_SUMMARY_MD)
    args = parser.parse_args()

    summary = build_candidate_bundle(
        output_root=args.output_root,
        summary_csv=args.summary_csv,
        summary_json=args.summary_json,
        summary_md=args.summary_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
