"""Build the P6.3 MP11 netdown/source-layer delta crosswalk."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class NetdownDelta:
    """Comparison row for one MP11 netdown or modelling-delta category."""

    category_id: str
    category_label: str
    mp11_pdf_pages: str
    source_table_or_section: str
    old_productive_area_ha: float | None
    mp11_productive_area_ha: float | None
    productive_area_delta_ha: float | None
    old_thlb_net_reduction_ha: float | None
    mp11_thlb_net_reduction_ha: float | None
    thlb_net_reduction_delta_ha: float | None
    source_reported_delta_percent: str
    reproducibility_class: str
    p6_followup_lane: str
    interpretation: str
    review_status: str
    downstream_use: str
    model_input_status: str


ROWS = [
    {
        "category_id": "ogma_wha_conservation",
        "category_label": "Legal/proposed OGMAs and WHAs",
        "mp11_pdf_pages": "76",
        "source_table_or_section": "Appendix A Table 6",
        "old_productive_area_ha": 20_632.0,
        "mp11_productive_area_ha": 27_966.0,
        "old_thlb_net_reduction_ha": None,
        "mp11_thlb_net_reduction_ha": None,
        "source_reported_delta_percent": "35.5% productive-area increase",
        "reproducibility_class": "partially_public_spatial_layer_rebuild",
        "p6_followup_lane": "P6.3/P6.4",
        "interpretation": (
            "MP11 adds 7,334 ha of conserved productive forest in legal/proposed OGMAs and WHAs. "
            "Legal designations may be public; proposed areas require careful source/version review."
        ),
    },
    {
        "category_id": "research_psp_big_tree_karst",
        "category_label": "Additional land-base values: research, PSPs, big trees, karst",
        "mp11_pdf_pages": "76-77",
        "source_table_or_section": "Appendix A Table 7",
        "old_productive_area_ha": 0.0,
        "mp11_productive_area_ha": 25_207.0,
        "old_thlb_net_reduction_ha": 0.0,
        "mp11_thlb_net_reduction_ha": 3_910.0,
        "source_reported_delta_percent": "new category in MP11",
        "reproducibility_class": "mixed_public_proxy_or_confidential",
        "p6_followup_lane": "P6.3/P6.4",
        "interpretation": (
            "MP11 explicitly adds THLB exclusions for values not specifically accounted for in previous MPs. "
            "Karst and big-tree evidence may be partly public/proxy; PSP/research-site details may not be fully public."
        ),
    },
    {
        "category_id": "nonproductive_low_sites",
        "category_label": "Non-productive and low sites",
        "mp11_pdf_pages": "77-78",
        "source_table_or_section": "Appendix A Table 8",
        "old_productive_area_ha": 14_703.0,
        "mp11_productive_area_ha": 35_423.0,
        "old_thlb_net_reduction_ha": 14_703.0,
        "mp11_thlb_net_reduction_ha": 18_735.0,
        "source_reported_delta_percent": "27.4% THLB-net-reduction increase",
        "reproducibility_class": "public_inventory_and_lidar_proxy",
        "p6_followup_lane": "P6.3/P6.4",
        "interpretation": (
            "MP11 increases non/low productivity net THLB reductions by 4,032 ha. "
            "This likely requires revisiting VRI productivity, LiDAR height/productivity proxies, and low-site rules."
        ),
    },
    {
        "category_id": "inoperable",
        "category_label": "Inoperable",
        "mp11_pdf_pages": "77-78",
        "source_table_or_section": "Appendix A Table 8",
        "old_productive_area_ha": 12_810.0,
        "mp11_productive_area_ha": 30_300.0,
        "old_thlb_net_reduction_ha": 12_810.0,
        "mp11_thlb_net_reduction_ha": 21_193.0,
        "source_reported_delta_percent": "65.4% THLB-net-reduction increase",
        "reproducibility_class": "public_dem_proxy_plus_wfp_operability_gap",
        "p6_followup_lane": "P6.4",
        "interpretation": (
            "MP11 materially increases inoperable net THLB reductions. "
            "A public DEM/slope proxy can be rebuilt, but WFP's land-base blocking and economic operability logic may not be fully public."
        ),
    },
    {
        "category_id": "riparian_management",
        "category_label": "Riparian management",
        "mp11_pdf_pages": "77-78",
        "source_table_or_section": "Appendix A Table 8",
        "old_productive_area_ha": 15_060.0,
        "mp11_productive_area_ha": 46_993.0,
        "old_thlb_net_reduction_ha": 13_956.0,
        "mp11_thlb_net_reduction_ha": 5_479.0,
        "source_reported_delta_percent": "-60.7% THLB-net-reduction decrease",
        "reproducibility_class": "public_hydrography_lidar_proxy",
        "p6_followup_lane": "P6.3/P6.4",
        "interpretation": (
            "MP11 reports much larger riparian productive area but lower net THLB reduction due to overlaps with earlier exclusions. "
            "This needs ordered-overlay reproduction, not independent category summation."
        ),
    },
    {
        "category_id": "terrain_stability_lidar_slope",
        "category_label": "Terrain stability and LiDAR 90%+ slope",
        "mp11_pdf_pages": "77-78",
        "source_table_or_section": "Appendix A Table 8",
        "old_productive_area_ha": 5_052.0,
        "mp11_productive_area_ha": 15_760.0,
        "old_thlb_net_reduction_ha": 1_304.0,
        "mp11_thlb_net_reduction_ha": 3_812.0,
        "source_reported_delta_percent": "N/A in source table",
        "reproducibility_class": "public_dem_proxy_plus_lidar_gap",
        "p6_followup_lane": "P6.4",
        "interpretation": (
            "MP11 adds LiDAR 90%+ slope logic and reports terrain/slope net reductions. "
            "Public DEM can approximate this, but source-specific LiDAR products may not be available."
        ),
    },
    {
        "category_id": "existing_future_wtra",
        "category_label": "Existing and future WTRAs",
        "mp11_pdf_pages": "79-80",
        "source_table_or_section": "Appendix A Table 9",
        "old_productive_area_ha": 0.0,
        "mp11_productive_area_ha": 7_287.0,
        "old_thlb_net_reduction_ha": 6_887.0,
        "mp11_thlb_net_reduction_ha": 7_577.0,
        "source_reported_delta_percent": "10.0% THLB-net-reduction increase",
        "reproducibility_class": "partly_aspatial_policy_parameter",
        "p6_followup_lane": "P6.3/P6.4",
        "interpretation": (
            "MP11 tracks existing WTRAs spatially and future stand-level reserves separately. "
            "Future WTRAs remain partly aspatial policy assumptions."
        ),
    },
    {
        "category_id": "mha_95_cmai",
        "category_label": "95% CMAI minimum harvest age plus 350 m3/ha minimum volume",
        "mp11_pdf_pages": "80",
        "source_table_or_section": "Appendix A section 2.2.3 item 3",
        "old_productive_area_ha": None,
        "mp11_productive_area_ha": None,
        "old_thlb_net_reduction_ha": None,
        "mp11_thlb_net_reduction_ha": None,
        "source_reported_delta_percent": "not a THLB area netdown",
        "reproducibility_class": "model_parameter_rebuild",
        "p6_followup_lane": "P6.4/P6.5",
        "interpretation": (
            "MP11 replaces harvest-system/DBH MHA logic with 95% CMAI and minimum volume criteria. "
            "This is a yield/treatment/model-behavior change rather than a land-base area deduction."
        ),
    },
    {
        "category_id": "vqo_eca_patchworks_spatial",
        "category_label": "VQO, ECA, adjacency/green-up, and Patchworks spatial modelling",
        "mp11_pdf_pages": "78-82",
        "source_table_or_section": "Appendix A sections 2.2.2-2.2.3 and 2.3",
        "old_productive_area_ha": None,
        "mp11_productive_area_ha": None,
        "old_thlb_net_reduction_ha": None,
        "mp11_thlb_net_reduction_ha": None,
        "source_reported_delta_percent": "not direct THLB area netdowns",
        "reproducibility_class": "model_constraint_rebuild",
        "p6_followup_lane": "P6.5/P6.6",
        "interpretation": (
            "Several MP11 changes limit harvest levels without directly reducing THLB. "
            "They need Patchworks constraint/scenario planning, not only source-layer netdown work."
        ),
    },
]


def _to_row(raw: dict[str, object]) -> NetdownDelta:
    old_prod = raw["old_productive_area_ha"]
    new_prod = raw["mp11_productive_area_ha"]
    old_thlb = raw["old_thlb_net_reduction_ha"]
    new_thlb = raw["mp11_thlb_net_reduction_ha"]
    return NetdownDelta(
        category_id=str(raw["category_id"]),
        category_label=str(raw["category_label"]),
        mp11_pdf_pages=str(raw["mp11_pdf_pages"]),
        source_table_or_section=str(raw["source_table_or_section"]),
        old_productive_area_ha=float(old_prod) if old_prod is not None else None,
        mp11_productive_area_ha=float(new_prod) if new_prod is not None else None,
        productive_area_delta_ha=(
            float(new_prod) - float(old_prod) if old_prod is not None and new_prod is not None else None
        ),
        old_thlb_net_reduction_ha=float(old_thlb) if old_thlb is not None else None,
        mp11_thlb_net_reduction_ha=float(new_thlb) if new_thlb is not None else None,
        thlb_net_reduction_delta_ha=(
            float(new_thlb) - float(old_thlb) if old_thlb is not None and new_thlb is not None else None
        ),
        source_reported_delta_percent=str(raw["source_reported_delta_percent"]),
        reproducibility_class=str(raw["reproducibility_class"]),
        p6_followup_lane=str(raw["p6_followup_lane"]),
        interpretation=str(raw["interpretation"]),
        review_status="reviewed_evidence",
        downstream_use="phase6_land_base_comparison_only",
        model_input_status="not_model_input",
    )


def build_crosswalk(output_csv: Path, output_json: Path, output_md: Path, generated_at_utc: str) -> list[NetdownDelta]:
    rows = [_to_row(row) for row in ROWS]
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    payload = {
        "generated_at_utc": generated_at_utc,
        "crosswalk_csv": output_csv.as_posix(),
        "row_count": len(rows),
        "reproducibility_class_counts": dict(
            sorted(Counter(row.reproducibility_class for row in rows).items())
        ),
        "followup_lane_counts": dict(sorted(Counter(row.p6_followup_lane for row in rows).items())),
        "review_status_counts": {"reviewed_evidence": len(rows)},
        "model_input_status_counts": {"not_model_input": len(rows)},
        "rows": [asdict(row) for row in rows],
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, rows, payload)
    return rows


def _fmt(value: float | None) -> str:
    return "" if value is None else f"{value:,.0f}"


def _write_markdown(path: Path, rows: list[NetdownDelta], payload: dict[str, object]) -> None:
    lines = [
        "# TFL 6 MP11 Netdown And Source-Layer Delta Crosswalk",
        "",
        "## Purpose",
        "",
        "This P6.3 note records the MP11 land-base/netdown categories that differ",
        "from the MP10-derived Phase 5 prototype basis and classifies whether each",
        "delta is likely reproducible from public layers, requires a proxy, or is",
        "better treated as a model-parameter/constraint rebuild.",
        "",
        "## Files",
        "",
        "- `planning/tfl6_mp11_netdown_delta_crosswalk.md`",
        "- `planning/tfl6_mp11_netdown_delta_crosswalk.csv`",
        "- `planning/tfl6_mp11_netdown_delta_crosswalk.json`",
        "",
        "## Status",
        "",
        f"- Rows: `{payload['row_count']}`",
        f"- Reproducibility classes: `{payload['reproducibility_class_counts']}`",
        "- Review status: `reviewed_evidence`",
        "- Downstream use: `phase6_land_base_comparison_only`",
        "- Model-input status: `not_model_input`",
        "",
        "## Delta Table",
        "",
        "| Category | PDF pages | Source | Old THLB net ha | MP11 THLB net ha | Delta ha | Reproducibility | Follow-up |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.category_label} | {row.mp11_pdf_pages} | {row.source_table_or_section} | "
            f"{_fmt(row.old_thlb_net_reduction_ha)} | {_fmt(row.mp11_thlb_net_reduction_ha)} | "
            f"{_fmt(row.thlb_net_reduction_delta_ha)} | `{row.reproducibility_class}` | `{row.p6_followup_lane}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- MP11's lower THLB is not explained by one category. It reflects a mix of",
            "  expanded conservation, new additional values, LiDAR-supported",
            "  productivity/operability/riparian/terrain interpretation, revised WTRA",
            "  treatment, and model constraints that do not directly reduce THLB.",
            "- Public-layer rebuilds are plausible for several categories, but some",
            "  MP11 assumptions rely on WFP-specific LiDAR/ITI, land-base blocking,",
            "  proposed conservation, research/PSP locations, or model policy choices.",
            "- Future implementation should split reproducible source-layer changes from",
            "  proxy/sensitivity lanes and model-constraint lanes.",
            "",
            "## Use Boundary",
            "",
            "These rows are reviewed comparison evidence only. They are not model input",
            "and do not authorize rerunning THLB or changing the Phase 5 teaching",
            "runtime package.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_netdown_delta_crosswalk.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_netdown_delta_crosswalk.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_netdown_delta_crosswalk.md"),
    )
    parser.add_argument(
        "--generated-at-utc",
        default=datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    args = parser.parse_args()
    rows = build_crosswalk(
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
        generated_at_utc=args.generated_at_utc,
    )
    print(f"wrote {len(rows)} netdown delta rows")
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
