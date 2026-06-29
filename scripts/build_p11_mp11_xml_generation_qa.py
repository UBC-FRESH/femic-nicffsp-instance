"""Record P11.4f QA for generated MP11 candidate ForestModel XML."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XML_PATH = (
    INSTANCE_ROOT / "output" / "patchworks_tfl6_mp11_candidate" / "forestmodel.xml"
)
DEFAULT_FRAGMENTS_PATH = (
    INSTANCE_ROOT
    / "output"
    / "patchworks_tfl6_mp11_candidate"
    / "fragments"
    / "fragments.shp"
)
DEFAULT_COMPAT_CURVE_TABLE = (
    INSTANCE_ROOT
    / "data"
    / "mp11_model_input_bundle"
    / "export_compat"
    / "curve_table.csv"
)
DEFAULT_OUTPUT_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_generation_qa.csv"
)
DEFAULT_OUTPUT_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_generation_qa.json"
)
DEFAULT_OUTPUT_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_forestmodel_xml_generation_qa.md"
)


def _repo_relative(path: Path) -> str:
    return path.relative_to(INSTANCE_ROOT).as_posix()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_xml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"ForestModel XML not found: {_repo_relative(path)}")
    root = ET.parse(path).getroot()
    tag_counts = Counter(element.tag for element in root.iter())
    return {
        "path": _repo_relative(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "root_tag": root.tag,
        "root_attributes": dict(root.attrib),
        "tag_counts": dict(sorted(tag_counts.items())),
    }


def _inspect_fragments(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Fragments shapefile not found: {_repo_relative(path)}"
        )
    fragments = gpd.read_file(path)
    return {
        "path": _repo_relative(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256(path),
        "rows": int(len(fragments)),
        "area_ha": float(fragments.geometry.area.sum() / 10000.0),
        "columns": list(fragments.columns),
    }


def _inspect_compat_curves(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Compatibility curve table not found: {_repo_relative(path)}"
        )
    curves = pd.read_csv(path)
    curve_id_strings = curves.get("curve_id_string", pd.Series(dtype=str)).astype(str)
    mp11_curve_mask = curve_id_strings.str.startswith("mp11_table57")
    return {
        "path": _repo_relative(path),
        "rows": int(len(curves)),
        "mp11_table57_curve_rows": int(mp11_curve_mask.sum()),
        "mp11_table57_curve_ids": sorted(curve_id_strings[mp11_curve_mask].tolist()),
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

    xml = payload["xml"]
    fragments = payload["fragments"]
    compat = payload["compat_curves"]
    lines = [
        "# P11.4f MP11 ForestModel XML Generation QA",
        "",
        "This QA record verifies the generated MP11 candidate ForestModel XML and "
        "fragments after P11.4e export.",
        "",
        "P11.4f does not run Matrix Builder or Patchworks runtime.",
        "",
        "## Summary",
        "",
    ]
    for key, value in payload["summary"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## XML",
            "",
            f"- Path: `{xml['path']}`",
            f"- SHA256: `{xml['sha256']}`",
            f"- Root: `{xml['root_tag']}`",
            f"- Year / horizon: `{xml['root_attributes'].get('year')}` / "
            f"`{xml['root_attributes'].get('horizon')}`",
            f"- XML curve nodes: `{xml['tag_counts'].get('curve', 0)}`",
            f"- XML select nodes: `{xml['tag_counts'].get('select', 0)}`",
            f"- XML treatment nodes: `{xml['tag_counts'].get('treatment', 0)}`",
            "",
            "## Fragments",
            "",
            f"- Path: `{fragments['path']}`",
            f"- SHA256: `{fragments['sha256']}`",
            f"- Rows: `{fragments['rows']}`",
            f"- Area ha: `{fragments['area_ha']:.6f}`",
            "",
            "## Candidate Curve Signal",
            "",
            f"- Compatibility curve rows: `{compat['rows']}`",
            f"- MP11 Table 57 candidate curve rows: `{compat['mp11_table57_curve_rows']}`",
            "",
            "## Boundary",
            "",
            "This is a candidate scaffold XML package. Matrix Builder, runtime "
            "assembly, scenario smoke, and release QA remain downstream work.",
            "",
        ]
    )
    output_md.write_text("\n".join(lines), encoding="utf-8")


def build_qa(
    *,
    xml_path: Path = DEFAULT_XML_PATH,
    fragments_path: Path = DEFAULT_FRAGMENTS_PATH,
    compat_curve_table: Path = DEFAULT_COMPAT_CURVE_TABLE,
    output_csv: Path = DEFAULT_OUTPUT_CSV,
    output_json: Path = DEFAULT_OUTPUT_JSON,
    output_md: Path = DEFAULT_OUTPUT_MD,
) -> dict[str, Any]:
    xml = _parse_xml(xml_path)
    fragments = _inspect_fragments(fragments_path)
    compat = _inspect_compat_curves(compat_curve_table)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "xml_path": xml["path"],
        "xml_bytes": xml["bytes"],
        "xml_root": xml["root_tag"],
        "xml_curve_nodes": xml["tag_counts"].get("curve", 0),
        "xml_select_nodes": xml["tag_counts"].get("select", 0),
        "xml_treatment_nodes": xml["tag_counts"].get("treatment", 0),
        "fragment_rows": fragments["rows"],
        "fragment_area_ha": round(fragments["area_ha"], 6),
        "compat_curve_rows": compat["rows"],
        "mp11_table57_curve_rows": compat["mp11_table57_curve_rows"],
        "matrix_builder": "not_performed",
        "runtime_bundle_generation": "not_performed",
    }
    payload = {
        "summary": summary,
        "xml": xml,
        "fragments": fragments,
        "compat_curves": compat,
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
    parser.add_argument("--xml-path", type=Path, default=DEFAULT_XML_PATH)
    parser.add_argument("--fragments-path", type=Path, default=DEFAULT_FRAGMENTS_PATH)
    parser.add_argument(
        "--compat-curve-table", type=Path, default=DEFAULT_COMPAT_CURVE_TABLE
    )
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    summary = build_qa(
        xml_path=args.xml_path,
        fragments_path=args.fragments_path,
        compat_curve_table=args.compat_curve_table,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
