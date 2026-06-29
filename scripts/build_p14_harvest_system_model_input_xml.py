"""Build P14.5 harvest-system candidate bundle and split-lane XML."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd
from shapely import wkb


ROOT = Path(__file__).resolve().parents[1]
SOURCE_BUNDLE = ROOT / "data" / "mp11_model_input_bundle"
OUTPUT_BUNDLE = ROOT / "data" / "mp11_harvest_system_model_input_bundle"
OUTPUT_PATCHWORKS = ROOT / "output" / "patchworks_tfl6_mp11_harvest_system_candidate"
CLASSIFICATION_CSV = ROOT / "planning" / "tfl6_mp11_phase14_harvest_system_classification.csv"
QA_CSV = ROOT / "planning" / "tfl6_mp11_phase14_model_input_xml_build_summary.csv"
QA_JSON = ROOT / "planning" / "tfl6_mp11_phase14_model_input_xml_build_summary.json"
QA_MD = ROOT / "planning" / "tfl6_mp11_phase14_model_input_xml_build_summary.md"

SPLIT_SYSTEMS = ("ground", "cable", "heli")
SYSTEM_TREATMENT_LABELS = {
    "ground": "CC_GROUND",
    "cable": "CC_CABLE",
    "heli": "CC_HELI",
}
SYSTEM_EXPORT_VALUES = {
    "ground": "ground",
    "cable": "cable",
    "heli": "heli",
    "not_applicable": "not_applicable",
}
MIN_FRAGMENT_EXPORT_AREA_HA = 0.001


def _repo(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_replace_bundle() -> None:
    if not SOURCE_BUNDLE.exists():
        raise FileNotFoundError(f"Source bundle not found: {_repo(SOURCE_BUNDLE)}")
    expected = (ROOT / "data" / "mp11_harvest_system_model_input_bundle").resolve()
    if OUTPUT_BUNDLE.resolve() != expected:
        raise ValueError(f"Refusing to replace unexpected bundle root: {OUTPUT_BUNDLE}")
    if OUTPUT_BUNDLE.exists():
        shutil.rmtree(OUTPUT_BUNDLE)
    shutil.copytree(SOURCE_BUNDLE, OUTPUT_BUNDLE)


def _load_classification() -> pd.DataFrame:
    classification = pd.read_csv(CLASSIFICATION_CSV)
    required = {
        "stand_id",
        "harvest_system_candidate",
        "harvest_system_source",
        "harvest_system_confidence",
        "harvest_system_rule",
        "is_managed_current_thlb",
    }
    missing = required.difference(classification.columns)
    if missing:
        raise ValueError(f"Classification missing columns: {sorted(missing)}")
    classification["hvsys_export"] = classification["harvest_system_candidate"].map(
        SYSTEM_EXPORT_VALUES
    )
    if classification["hvsys_export"].isna().any():
        missing_values = sorted(
            classification.loc[
                classification["hvsys_export"].isna(),
                "harvest_system_candidate",
            ]
            .astype(str)
            .unique()
        )
        raise ValueError(f"Unsupported harvest-system classes: {missing_values}")
    return classification


def _merge_classification(table: pd.DataFrame, classification: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "stand_id",
        "harvest_system_candidate",
        "harvest_system_source",
        "harvest_system_confidence",
        "harvest_system_rule",
        "hvsys_export",
    ]
    merged = table.merge(classification[columns], on="stand_id", how="left", validate="1:1")
    missing = int(merged["harvest_system_candidate"].isna().sum())
    if missing:
        raise ValueError(f"{missing} table rows missing P14.4 harvest-system classification")
    return merged


def _update_stand_table(classification: pd.DataFrame) -> dict[str, Any]:
    path = OUTPUT_BUNDLE / "stand_table.csv"
    stand = pd.read_csv(path)
    stand = _merge_classification(stand, classification)
    stand["harvest_system"] = stand["hvsys_export"]
    stand["harvest_system_assignment_status"] = "p14_4_public_proxy_classification"
    stand["harvest_system_source"] = stand["harvest_system_source"]
    stand["harvest_system_confidence"] = stand["harvest_system_confidence"]
    stand["harvest_system_rule"] = stand["harvest_system_rule"]
    eligible = stand["harvest_system"].isin(SPLIT_SYSTEMS) & (
        stand["ifm"].astype(str) == "managed"
    )
    stand["operable_under_scenario"] = eligible
    stand["clearcut_and_plant_candidate"] = eligible
    stand["clearcut_and_plant_eligible"] = eligible
    stand["clearcut_blocker"] = pd.Series(
        ["none" if value else "not_managed_current_thlb_or_missing_harvest_system" for value in eligible],
        index=stand.index,
    )
    stand = stand.drop(columns=["harvest_system_candidate", "hvsys_export"])
    stand.to_csv(path, index=False)
    return {
        "stand_table_rows": int(len(stand)),
        "stand_clearcut_eligible_rows": int(eligible.sum()),
    }


def _update_harvest_system_table(classification: pd.DataFrame) -> dict[str, Any]:
    path = OUTPUT_BUNDLE / "harvest_system_table.csv"
    table = pd.read_csv(path)
    table = _merge_classification(table, classification)
    table["harvest_system"] = table["hvsys_export"]
    table["harvest_system_assignment_status"] = "p14_4_public_proxy_classification"
    table["harvest_system_source"] = table["harvest_system_source"]
    table["harvest_system_confidence"] = table["harvest_system_confidence"]
    table["harvest_system_rule"] = table["harvest_system_rule"]
    table["operable_under_scenario"] = table["harvest_system"].isin(SPLIT_SYSTEMS)
    table["clearcut_and_plant_candidate"] = table["operable_under_scenario"]
    table["clearcut_and_plant_eligible"] = table["operable_under_scenario"]
    table["clearcut_blocker"] = [
        "none" if value else "not_managed_current_thlb_or_missing_harvest_system"
        for value in table["operable_under_scenario"]
    ]
    table = table.drop(columns=["harvest_system_candidate", "hvsys_export"])
    table.to_csv(path, index=False)
    return {
        "harvest_system_table_rows": int(len(table)),
        "harvest_system_eligible_rows": int(table["clearcut_and_plant_eligible"].sum()),
    }


def _update_group_table(classification: pd.DataFrame) -> dict[str, Any]:
    path = OUTPUT_BUNDLE / "group_table.csv"
    group = pd.read_csv(path)
    area_cols = ["stand_id", "aflb_area_ha", "thlb_area_ha"]
    base_area = group[group["group_family"] == "area_class"][area_cols].drop_duplicates(
        subset=["stand_id"]
    )
    system = base_area.merge(
        classification[["stand_id", "hvsys_export"]],
        on="stand_id",
        how="left",
        validate="1:1",
    )
    system_rows = system.rename(columns={"hvsys_export": "group_id"})
    system_rows["group_family"] = "harvest_system_proxy"
    system_rows = system_rows[["stand_id", "group_family", "group_id", "aflb_area_ha", "thlb_area_ha"]]
    group = pd.concat([group, system_rows], ignore_index=True)
    group.to_csv(path, index=False)
    return {
        "group_table_rows": int(len(group)),
        "harvest_system_group_rows": int(len(system_rows)),
    }


def _update_treatment_and_transition_tables() -> dict[str, Any]:
    treatment_path = OUTPUT_BUNDLE / "treatment_table.csv"
    treatment = pd.read_csv(treatment_path)
    extra_treatments = pd.DataFrame(
        [
            {
                "treatment_id": "clearcut_and_plant_ground",
                "label": "Clearcut and plant - ground",
                "scheduled_action": True,
                "status": "p14_5_public_proxy_split_lane",
                "eligibility_summary": "managed THLB candidate assigned public-proxy ground system",
            },
            {
                "treatment_id": "clearcut_and_plant_cable",
                "label": "Clearcut and plant - cable",
                "scheduled_action": True,
                "status": "p14_5_public_proxy_split_lane",
                "eligibility_summary": "managed THLB candidate assigned public-proxy cable system",
            },
            {
                "treatment_id": "clearcut_and_plant_heli",
                "label": "Clearcut and plant - heli",
                "scheduled_action": True,
                "status": "p14_5_public_proxy_split_lane",
                "eligibility_summary": "managed THLB candidate assigned public-proxy heli system",
            },
        ]
    )
    treatment = treatment[
        ~treatment["treatment_id"].isin(extra_treatments["treatment_id"])
    ].copy()
    treatment = pd.concat([treatment, extra_treatments], ignore_index=True)
    treatment.to_csv(treatment_path, index=False)

    transition_path = OUTPUT_BUNDLE / "transition_table.csv"
    transition = pd.read_csv(transition_path)
    extra_transitions = pd.DataFrame(
        [
            {
                "transition_id": "tr_clearcut_plant_ground",
                "treatment_id": "clearcut_and_plant_ground",
                "source_state": "initial_managed_natural",
                "destination_state": "post_clearcut_planted",
                "status": "p14_5_public_proxy_split_lane",
            },
            {
                "transition_id": "tr_clearcut_plant_cable",
                "treatment_id": "clearcut_and_plant_cable",
                "source_state": "initial_managed_natural",
                "destination_state": "post_clearcut_planted",
                "status": "p14_5_public_proxy_split_lane",
            },
            {
                "transition_id": "tr_clearcut_plant_heli",
                "treatment_id": "clearcut_and_plant_heli",
                "source_state": "initial_managed_natural",
                "destination_state": "post_clearcut_planted",
                "status": "p14_5_public_proxy_split_lane",
            },
        ]
    )
    transition = transition[
        ~transition["transition_id"].isin(extra_transitions["transition_id"])
    ].copy()
    transition = pd.concat([transition, extra_transitions], ignore_index=True)
    transition.to_csv(transition_path, index=False)
    return {
        "treatment_table_rows": int(len(treatment)),
        "transition_table_rows": int(len(transition)),
    }


def _update_export_checkpoint(classification: pd.DataFrame) -> dict[str, Any]:
    path = OUTPUT_BUNDLE / "export_compat" / "aflb_current_export_compat.feather"
    checkpoint = pd.read_feather(path)
    checkpoint = _merge_classification(checkpoint, classification)
    checkpoint["harvest_system"] = checkpoint["hvsys_export"]
    checkpoint["harvest_system_assignment_status"] = "p14_4_public_proxy_classification"
    checkpoint["HVSYS"] = checkpoint["hvsys_export"].str.upper()
    checkpoint["clearcut_and_plant_eligible"] = checkpoint["hvsys_export"].isin(SPLIT_SYSTEMS)
    checkpoint["clearcut_blocker"] = [
        "none" if value else "not_managed_current_thlb_or_missing_harvest_system"
        for value in checkpoint["clearcut_and_plant_eligible"]
    ]
    checkpoint = checkpoint.drop(columns=["harvest_system_candidate", "hvsys_export"])
    checkpoint.to_feather(path)
    return {
        "checkpoint_rows": int(len(checkpoint)),
        "checkpoint_hvsys_counts": checkpoint["HVSYS"].value_counts().to_dict(),
    }


def _run_export() -> None:
    if OUTPUT_PATCHWORKS.exists():
        shutil.rmtree(OUTPUT_PATCHWORKS)
    command = [
        sys.executable,
        "-m",
        "femic",
        "export",
        "patchworks",
        "--instance-root",
        ".",
        "--tsa",
        "tfl6",
        "--bundle-dir",
        _repo(OUTPUT_BUNDLE / "export_compat"),
        "--checkpoint",
        _repo(OUTPUT_BUNDLE / "export_compat" / "aflb_current_export_compat.feather"),
        "--output-dir",
        _repo(OUTPUT_PATCHWORKS),
        "--silviculture-config",
        "config/silviculture.tfl6.yaml",
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def _filtered_checkpoint_for_fragments(checkpoint: pd.DataFrame) -> pd.DataFrame:
    au_table = pd.read_csv(OUTPUT_BUNDLE / "export_compat" / "au_table.csv")
    au_ids = set(pd.to_numeric(au_table["au_id"], errors="coerce").dropna().astype(int))
    scoped = checkpoint.copy()
    scoped = scoped[scoped["tsa_code"].astype(str).str.casefold() == "tfl6"].copy()
    scoped = scoped[scoped["au"].notna()].copy()
    scoped["au"] = pd.to_numeric(scoped["au"], errors="coerce")
    scoped = scoped[scoped["au"].isin(au_ids)].copy()
    scoped = scoped[scoped["geometry"].notna()].copy()
    geometry_area_ha = scoped["geometry"].map(_geometry_area_ha)
    scoped = scoped[geometry_area_ha > MIN_FRAGMENT_EXPORT_AREA_HA].copy()
    return scoped.reset_index(drop=True)


def _geometry_area_ha(geometry: Any) -> float:
    if isinstance(geometry, bytes):
        return float(wkb.loads(geometry).area / 10000.0)
    return float(geometry.area / 10000.0)


def _add_hvsys_to_fragments() -> dict[str, Any]:
    fragments_path = OUTPUT_PATCHWORKS / "fragments" / "fragments.shp"
    checkpoint_path = OUTPUT_BUNDLE / "export_compat" / "aflb_current_export_compat.feather"
    fragments = gpd.read_file(fragments_path)
    checkpoint = _filtered_checkpoint_for_fragments(pd.read_feather(checkpoint_path))
    if len(fragments) != len(checkpoint):
        raise ValueError(
            f"Fragment/checkpoint row mismatch: {len(fragments)} != {len(checkpoint)}"
        )
    fragments["HVSYS"] = checkpoint["HVSYS"].astype(str).to_numpy()
    fragments.to_file(fragments_path)
    return {
        "fragment_rows": int(len(fragments)),
        "fragment_area_ha": float(fragments.geometry.area.sum() / 10000.0),
        "fragment_hvsys_counts": fragments["HVSYS"].value_counts().to_dict(),
        "fragment_hvsys_area_ha": (
            fragments.assign(_area_ha=fragments.geometry.area / 10000.0)
            .groupby("HVSYS")["_area_ha"]
            .sum()
            .to_dict()
        ),
    }


def _has_cc_treatment(select: ET.Element) -> bool:
    track = select.find("track")
    if track is None:
        return False
    return any(treatment.get("label") == "CC" for treatment in track.findall("treatment"))


def _clone_for_system(select: ET.Element, system: str) -> ET.Element:
    clone = deepcopy(select)
    statement = clone.get("statement", "")
    clone.set("statement", f"{statement} and HVSYS eq '{system.upper()}'")
    treatment_label = SYSTEM_TREATMENT_LABELS[system]
    for treatment in clone.findall("./track/treatment"):
        if treatment.get("label") != "CC":
            continue
        treatment.set("label", treatment_label)
        for assign in treatment.findall("./produce/assign"):
            if assign.get("field") == "treatment" and assign.get("value") == "'CC'":
                assign.set("value", f"'{treatment_label}'")
    products = clone.find("products")
    if products is not None:
        original_attrs = list(products.findall("attribute"))
        existing_labels = {attr.get("label") for attr in original_attrs}
        for attr in original_attrs:
            label = attr.get("label")
            if not label or not label.endswith(".CC"):
                continue
            system_label = f"{label}_{system.upper()}"
            if system_label in existing_labels:
                continue
            duplicate = deepcopy(attr)
            duplicate.set("label", system_label)
            products.append(duplicate)
            existing_labels.add(system_label)
    return clone


def _postprocess_xml() -> dict[str, Any]:
    xml_path = OUTPUT_PATCHWORKS / "forestmodel.xml"
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(xml_path, parser=parser)
    root = tree.getroot()

    define_fields = {node.get("field") for node in root.findall("define")}
    if "HVSYS" not in define_fields:
        root.insert(0, ET.Element("define", {"field": "HVSYS", "column": "HVSYS"}))

    children = list(root)
    track_replacements = 0
    split_selects = 0
    for child in children:
        if child.tag != "select":
            continue
        statement = child.get("statement", "")
        if "IFM eq 'managed'" not in statement or not _has_cc_treatment(child):
            continue
        index = list(root).index(child)
        root.remove(child)
        for offset, system in enumerate(SPLIT_SYSTEMS):
            root.insert(index + offset, _clone_for_system(child, system))
            split_selects += 1
        track_replacements += 1

    children = list(root)
    product_replacements = 0
    split_product_selects = 0
    for child in children:
        if child.tag != "select":
            continue
        statement = child.get("statement", "")
        if "IFM eq 'managed'" not in statement or "treatment eq 'CC'" not in statement:
            continue
        if child.find("products") is None:
            continue
        index = list(root).index(child)
        root.remove(child)
        for offset, system in enumerate(SPLIT_SYSTEMS):
            clone = _clone_product_select_for_system(child, system)
            root.insert(index + offset, clone)
            split_product_selects += 1
        product_replacements += 1

    ET.indent(tree, space="  ")
    xml_text = ET.tostring(root, encoding="unicode")
    xml_path.write_text(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<?xml-model href=\"https://www.spatial.ca/ForestModel.xsd\"?>\n"
        f"{xml_text}\n",
        encoding="utf-8",
    )

    reparsed = ET.parse(xml_path).getroot()
    tag_counts = Counter(element.tag for element in reparsed.iter())
    treatment_labels = Counter(
        treatment.get("label")
        for treatment in reparsed.findall(".//treatment")
        if treatment.get("label")
    )
    hvsys_selects = sum(
        1
        for select in reparsed.findall("select")
        if "HVSYS eq" in str(select.get("statement", ""))
    )
    return {
        "xml_path": _repo(xml_path),
        "xml_sha256": _sha256(xml_path),
        "xml_root": reparsed.tag,
        "xml_tag_counts": dict(sorted(tag_counts.items())),
        "managed_cc_selects_replaced": track_replacements,
        "split_managed_selects": split_selects,
        "product_cc_selects_replaced": product_replacements,
        "split_product_selects": split_product_selects,
        "hvsys_selects": hvsys_selects,
        "treatment_label_counts": dict(sorted(treatment_labels.items())),
    }


def _clone_product_select_for_system(select: ET.Element, system: str) -> ET.Element:
    clone = deepcopy(select)
    treatment_label = SYSTEM_TREATMENT_LABELS[system]
    statement = str(clone.get("statement", ""))
    clone.set("statement", statement.replace("treatment eq 'CC'", f"treatment eq '{treatment_label}'"))
    products = clone.find("products")
    if products is None:
        return clone
    original_attrs = list(products.findall("attribute"))
    existing_labels = {attr.get("label") for attr in original_attrs}
    for attr in original_attrs:
        label = attr.get("label")
        if not label or not label.endswith(".CC"):
            continue
        system_label = f"{label}_{system.upper()}"
        if system_label in existing_labels:
            continue
        duplicate = deepcopy(attr)
        duplicate.set("label", system_label)
        products.append(duplicate)
        existing_labels.add(system_label)
    return clone


def _record_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for rel_path in [
        "stand_table.csv",
        "harvest_system_table.csv",
        "treatment_table.csv",
        "transition_table.csv",
        "group_table.csv",
        "export_compat/au_table.csv",
        "export_compat/curve_table.csv",
        "export_compat/curve_points_table.csv",
    ]:
        with (OUTPUT_BUNDLE / rel_path).open(newline="", encoding="utf-8") as handle:
            counts[rel_path] = sum(1 for _ in csv.DictReader(handle))
    return counts


def _write_outputs(payload: dict[str, Any]) -> None:
    rows = [
        {"metric": key, "value": value}
        for key, value in payload["summary"].items()
        if not isinstance(value, (dict, list))
    ]
    with QA_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(rows)
    QA_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    summary = payload["summary"]
    lines = [
        "# TFL 6 MP11 Phase 14 Model-Input And XML Build Summary",
        "",
        "This P14.5 output rebuilds an ignored MP11 harvest-system candidate "
        "model-input bundle and ForestModel XML/fragments package with public-proxy "
        "ground, cable, and heli clearcut lanes. It does not run Matrix Builder, "
        "assemble a Patchworks runtime, or run scenarios.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        if not isinstance(value, (dict, list)):
            lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Treatment Labels",
            "",
            "| Label | Count |",
            "| --- | ---: |",
        ]
    )
    for label, count in payload["xml"]["treatment_label_counts"].items():
        lines.append(f"| `{label}` | `{count}` |")
    lines.extend(
        [
            "",
            "## Fragment Harvest-System Counts",
            "",
            "| HVSYS | Rows | Area ha |",
            "| --- | ---: | ---: |",
        ]
    )
    fragment_counts = payload["fragments"]["fragment_hvsys_counts"]
    fragment_areas = payload["fragments"]["fragment_hvsys_area_ha"]
    for system, count in sorted(fragment_counts.items()):
        lines.append(f"| `{system}` | `{count}` | `{fragment_areas[system]:.3f}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- WFP LBB remains unavailable; `HVSYS` is a P14.4 public-proxy field.",
            "- XML split lanes expose `CC_GROUND`, `CC_CABLE`, and `CC_HELI` while "
            "retaining aggregate `.CC` product labels for all-system reporting.",
            "- Matrix Builder, runtime assembly, all-system smoke, no-heli smoke, and "
            "release QA remain downstream Phase 14 tasks.",
            "",
            "## Files",
            "",
            f"- `{_repo(OUTPUT_BUNDLE)}/`",
            f"- `{_repo(OUTPUT_PATCHWORKS / 'forestmodel.xml')}`",
            f"- `{_repo(OUTPUT_PATCHWORKS / 'fragments' / 'fragments.shp')}`",
            f"- `{_repo(QA_CSV)}`",
            f"- `{_repo(QA_JSON)}`",
            f"- `{_repo(QA_MD)}`",
            "",
        ]
    )
    QA_MD.write_text("\n".join(lines), encoding="utf-8")


def build() -> dict[str, Any]:
    _safe_replace_bundle()
    classification = _load_classification()
    summaries = {}
    summaries.update(_update_stand_table(classification))
    summaries.update(_update_harvest_system_table(classification))
    summaries.update(_update_group_table(classification))
    summaries.update(_update_treatment_and_transition_tables())
    summaries.update(_update_export_checkpoint(classification))
    _run_export()
    fragment_summary = _add_hvsys_to_fragments()
    xml_summary = _postprocess_xml()
    record_counts = _record_counts()
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "candidate_bundle_root": _repo(OUTPUT_BUNDLE),
        "patchworks_output_root": _repo(OUTPUT_PATCHWORKS),
        "forestmodel_xml": xml_summary["xml_path"],
        "fragments_path": _repo(OUTPUT_PATCHWORKS / "fragments" / "fragments.shp"),
        "stand_table_rows": summaries["stand_table_rows"],
        "stand_clearcut_eligible_rows": summaries["stand_clearcut_eligible_rows"],
        "harvest_system_eligible_rows": summaries["harvest_system_eligible_rows"],
        "harvest_system_group_rows": summaries["harvest_system_group_rows"],
        "checkpoint_rows": summaries["checkpoint_rows"],
        "fragment_rows": fragment_summary["fragment_rows"],
        "fragment_area_ha": round(fragment_summary["fragment_area_ha"], 6),
        "xml_root": xml_summary["xml_root"],
        "xml_select_nodes": xml_summary["xml_tag_counts"].get("select", 0),
        "xml_treatment_nodes": xml_summary["xml_tag_counts"].get("treatment", 0),
        "managed_cc_selects_replaced": xml_summary["managed_cc_selects_replaced"],
        "split_managed_selects": xml_summary["split_managed_selects"],
        "product_cc_selects_replaced": xml_summary["product_cc_selects_replaced"],
        "split_product_selects": xml_summary["split_product_selects"],
        "hvsys_selects": xml_summary["hvsys_selects"],
        "matrix_builder": "not_performed",
        "runtime_bundle_generation": "not_performed",
        "scenario_smoke": "not_performed",
    }
    payload = {
        "summary": summary,
        "bundle_updates": summaries,
        "record_counts": record_counts,
        "fragments": fragment_summary,
        "xml": xml_summary,
        "inputs": {
            "source_bundle": _repo(SOURCE_BUNDLE),
            "classification": _repo(CLASSIFICATION_CSV),
        },
        "outputs": {
            "candidate_bundle": _repo(OUTPUT_BUNDLE),
            "patchworks_output": _repo(OUTPUT_PATCHWORKS),
            "qa_csv": _repo(QA_CSV),
            "qa_json": _repo(QA_JSON),
            "qa_md": _repo(QA_MD),
        },
        "non_goals": [
            "No Matrix Builder run is performed in P14.5.",
            "No Patchworks runtime package is assembled in P14.5.",
            "No all-system or no-heli scenario smoke is run in P14.5.",
            "The split lanes are public-proxy harvest-system lanes, not WFP LBB reconstruction.",
        ],
    }
    _write_outputs(payload)
    return payload


def main() -> None:
    payload = build()
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
