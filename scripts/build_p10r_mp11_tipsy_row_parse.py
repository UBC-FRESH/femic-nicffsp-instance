"""Parse MP11 per-AU TIPSY input rows from public PDF tables."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import fitz
import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_row_parse.md"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_row_parse.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_row_parse.json"

SOURCE_PACKAGE_ID = "tfl6_mp11_202606_public_pdf"
SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"

PDF_CANDIDATES = [
    INSTANCE_ROOT / "runtime" / "mp11" / "source" / "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf",
    INSTANCE_ROOT / "data" / "downloads" / "mp11" / "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf",
    INSTANCE_ROOT.parent / "figrecover" / "examples" / "TFL6_MP_11_202606_w_Appendices_Web-compressed.pdf",
]

TABLE_CONFIGS = {
    "Table 54": {
        "curve_lane": "early_managed",
        "au_prefix": "E",
        "pdf_pages": range(358, 365),
        "appendix_start": 112,
        "has_productive_area": True,
        "has_genetic_gain": False,
        "expected_min_rows": 70,
        "expected_max_rows": 120,
        "title": "TIPSY Inputs for Early Managed Stands Aged 23-62 Years",
    },
    "Table 55": {
        "curve_lane": "recent_managed",
        "au_prefix": "R",
        "pdf_pages": range(365, 371),
        "appendix_start": 119,
        "has_productive_area": True,
        "has_genetic_gain": True,
        "expected_min_rows": 55,
        "expected_max_rows": 100,
        "title": "TIPSY Inputs for Recently Managed Stands Aged 1-22 Years",
    },
    "Table 57": {
        "curve_lane": "future_managed",
        "au_prefix": "F",
        "pdf_pages": range(372, 376),
        "appendix_start": 126,
        "has_productive_area": False,
        "has_genetic_gain": True,
        "expected_min_rows": 20,
        "expected_max_rows": 45,
        "title": "TIPSY Inputs for Future Managed Stands",
    },
}

AU_PATTERNS = {
    "E": re.compile(r"^E\d{3}[A-Za-z]*$"),
    "R": re.compile(r"^R\d{3}[A-Za-z]*$"),
    "F": re.compile(r"^(?:Fvh|Fvm|FMH)\d{2,3}[A-Za-z]*$"),
}
SPECIES_RE = re.compile(r"[A-Za-z]{1,4}\d+")
NUMBER_RE = re.compile(r"^-?\d[\d,]*(?:\.\d+)?$")
INTEGER_RE = re.compile(r"^\d[\d,]*$")


@dataclass
class ParsedRow:
    source_table: str
    curve_lane: str
    au_code: str
    sph: str
    pdf_page_start: int
    pdf_page_end: int
    appendix_page_start: str
    appendix_page_end: str
    raw_species_parts: list[str] = field(default_factory=list)
    row_number: int = 0
    start_cells: list[str] = field(default_factory=list)
    continuation_cells: list[list[str]] = field(default_factory=list)
    si_values: list[str] = field(default_factory=list)
    genetic_gain_values: list[str] = field(default_factory=list)
    productive_area_ha: str = ""
    thlb_area_ha: str = ""
    parser_warnings: list[str] = field(default_factory=list)

    def to_record(self) -> dict[str, object]:
        species_composition_raw = _join_species_parts(self.raw_species_parts)
        species_components = _species_components(species_composition_raw)
        species_percent_total = sum(component["percent"] for component in species_components)
        warnings = list(self.parser_warnings)
        if not species_components:
            warnings.append("no_species_components_detected")
        if species_components and abs(species_percent_total - 100) > 2:
            warnings.append("species_percent_total_not_near_100")
        if len(self.si_values) < min(1, len(species_components)):
            warnings.append("no_site_index_values_detected")
        if not self.thlb_area_ha:
            warnings.append("missing_thlb_area")
        confidence = "review_required" if warnings else "high"
        return {
            "row_id": f"p10r_{self.source_table.lower().replace(' ', '_')}_{self.row_number:03d}",
            "source_package_id": SOURCE_PACKAGE_ID,
            "source_sha256": SOURCE_SHA256,
            "source_table": self.source_table,
            "curve_lane": self.curve_lane,
            "au_code": self.au_code,
            "sph": _normalize_number_text(self.sph),
            "species_composition_raw": species_composition_raw,
            "species_components_json": json.dumps(species_components, ensure_ascii=False),
            "species_percent_total": round(species_percent_total, 3) if species_components else "",
            "spp1_si": _nth(self.si_values, 0),
            "spp2_si": _nth(self.si_values, 1),
            "spp3_si": _nth(self.si_values, 2),
            "spp4_si": _nth(self.si_values, 3),
            "spp5_si": _nth(self.si_values, 4),
            "genetic_gain_spp1": _nth(self.genetic_gain_values, 0),
            "genetic_gain_spp2": _nth(self.genetic_gain_values, 1),
            "genetic_gain_spp3": _nth(self.genetic_gain_values, 2),
            "genetic_gain_spp4": _nth(self.genetic_gain_values, 3),
            "genetic_gain_spp5": _nth(self.genetic_gain_values, 4),
            "productive_area_ha": _normalize_number_text(self.productive_area_ha),
            "thlb_area_ha": _normalize_number_text(self.thlb_area_ha),
            "pdf_page_start": self.pdf_page_start,
            "pdf_page_end": self.pdf_page_end,
            "appendix_page_start": self.appendix_page_start,
            "appendix_page_end": self.appendix_page_end,
            "source_anchor": (
                f"PDF pages {self.pdf_page_start}-{self.pdf_page_end}; "
                f"Appendix B pages {self.appendix_page_start}-{self.appendix_page_end}; "
                f"{self.source_table}"
            ),
            "continuation_row_count": len(self.continuation_cells),
            "parse_confidence": confidence,
            "review_status": "parser_review_required" if warnings else "parsed_candidate",
            "model_input_status": "not_model_input",
            "parser_warnings": ";".join(dict.fromkeys(warnings)),
            "raw_start_cells_json": json.dumps(self.start_cells, ensure_ascii=False),
            "raw_continuation_cells_json": json.dumps(self.continuation_cells, ensure_ascii=False),
        }


def _find_pdf() -> Path:
    for candidate in PDF_CANDIDATES:
        if candidate.exists():
            return candidate
    searched = "\n".join(str(path) for path in PDF_CANDIDATES)
    raise FileNotFoundError(
        "Could not find the MP11 PDF. Place a verified public source copy in one "
        f"of these ignored paths:\n{searched}"
    )


def _clean(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).replace("\n", "")).strip()


def _normalize_number_text(value: str) -> str:
    return _clean(value).replace(",", "")


def _appendix_page(pdf_page: int, appendix_start_pdf: int, appendix_start_page: int) -> str:
    return f"{appendix_start_page + (pdf_page - appendix_start_pdf)} of 183"


def _nth(values: list[str], index: int) -> str:
    return values[index] if index < len(values) else ""


def _nonempty(row: list[str]) -> list[str]:
    return [_clean(cell) for cell in row if _clean(cell)]


def _is_header_row(cells: list[str]) -> bool:
    text = " ".join(cells).lower()
    return any(
        marker in text
        for marker in [
            "existingau",
            "futureau",
            "spp%",
            "genetic gain",
            "area",
            "(ha",
        ]
    )


def _au_from_cells(cells: list[str], prefix: str) -> str:
    pattern = AU_PATTERNS[prefix]
    for cell in cells[:4]:
        compact = _clean(cell)
        if prefix == "F" and compact == "Fvm2":
            return compact
        if compact.startswith(prefix) and pattern.match(compact):
            return compact
    return ""


def _species_like_cells(cells: list[str], *, include_digit_fragments: bool) -> list[str]:
    parts: list[str] = []
    for cell in cells:
        if (
            SPECIES_RE.search(cell)
            and not any(pattern.match(cell) for pattern in AU_PATTERNS.values())
            and cell != "Fvm2"
            and not cell.lower().startswith("spp")
        ):
            parts.append(cell)
        elif include_digit_fragments and cell.isdigit() and parts:
            parts.append(cell)
    return parts


def _join_species_parts(parts: list[str]) -> str:
    tokens: list[str] = []
    for part in parts:
        for token in part.split():
            if token.isdigit() and tokens and re.search(r"[A-Za-z]\d+$", tokens[-1]):
                tokens[-1] += token
            else:
                tokens.append(token)
    return " ".join(tokens)


def _species_components(species_text: str) -> list[dict[str, object]]:
    components: list[dict[str, object]] = []
    for species, percent in re.findall(r"([A-Za-z]{1,4})(\d+)", species_text):
        components.append({"species": species, "percent": int(percent)})
    return components


def _numeric_values(cells: list[str]) -> list[str]:
    values: list[str] = []
    for cell in cells:
        value = _clean(cell)
        if value in {"-", ""} or NUMBER_RE.match(value):
            values.append(value)
    return values


def _parse_start_row(
    *,
    source_table: str,
    config: dict[str, object],
    pdf_page: int,
    row: list[str],
    row_number: int,
) -> ParsedRow:
    cells = _nonempty(row)
    au_code = _au_from_cells(cells, str(config["au_prefix"]))
    sph = ""
    if au_code:
        au_index = cells.index(au_code)
        if au_index + 1 < len(cells):
            sph = cells[au_index + 1]
    numeric = _numeric_values(cells)
    numeric_after_sph = numeric[1:] if numeric and sph and _normalize_number_text(numeric[0]) == _normalize_number_text(sph) else numeric
    area_count = 2 if config["has_productive_area"] else 1
    area_values = numeric_after_sph[-area_count:] if len(numeric_after_sph) >= area_count else []
    non_area_numeric = numeric_after_sph[: max(0, len(numeric_after_sph) - area_count)]
    if config["has_genetic_gain"]:
        si_values = non_area_numeric[:5]
        genetic_gain_values = non_area_numeric[5:10]
    else:
        si_values = non_area_numeric[:5]
        genetic_gain_values = []
    productive_area = area_values[0] if config["has_productive_area"] and len(area_values) == 2 else ""
    thlb_area = area_values[-1] if area_values else ""
    appendix_page = _appendix_page(
        pdf_page,
        min(config["pdf_pages"]),
        int(config["appendix_start"]),
    )
    parsed = ParsedRow(
        source_table=source_table,
        curve_lane=str(config["curve_lane"]),
        au_code=au_code,
        sph=sph,
        pdf_page_start=pdf_page,
        pdf_page_end=pdf_page,
        appendix_page_start=appendix_page,
        appendix_page_end=appendix_page,
        raw_species_parts=_species_like_cells(cells, include_digit_fragments=False),
        row_number=row_number,
        start_cells=cells,
        si_values=[_normalize_number_text(value) for value in si_values],
        genetic_gain_values=[_normalize_number_text(value) for value in genetic_gain_values],
        productive_area_ha=productive_area,
        thlb_area_ha=thlb_area,
    )
    if len(parsed.si_values) > 5:
        parsed.parser_warnings.append("too_many_site_index_values")
    if config["has_genetic_gain"] and len(parsed.genetic_gain_values) > 5:
        parsed.parser_warnings.append("too_many_genetic_gain_values")
    return parsed


def _extract_page_rows(doc: fitz.Document, pdf_page: int) -> list[list[str]]:
    tables = doc[pdf_page - 1].find_tables().tables
    if not tables:
        return []
    return [[_clean(cell) for cell in row] for row in tables[0].extract()]


def parse_table(doc: fitz.Document, source_table: str, config: dict[str, object]) -> list[dict[str, object]]:
    parsed_rows: list[ParsedRow] = []
    current: ParsedRow | None = None
    row_number = 1
    for pdf_page in config["pdf_pages"]:
        page_rows = _extract_page_rows(doc, int(pdf_page))
        for row in page_rows:
            cells = _nonempty(row)
            if not cells or _is_header_row(cells):
                continue
            au_code = _au_from_cells(cells, str(config["au_prefix"]))
            if au_code:
                if current is not None:
                    parsed_rows.append(current)
                current = _parse_start_row(
                    source_table=source_table,
                    config=config,
                    pdf_page=int(pdf_page),
                    row=row,
                    row_number=row_number,
                )
                row_number += 1
            elif current is not None:
                current.pdf_page_end = int(pdf_page)
                current.appendix_page_end = _appendix_page(
                    int(pdf_page),
                    min(config["pdf_pages"]),
                    int(config["appendix_start"]),
                )
                current.continuation_cells.append(cells)
                if (
                    source_table == "Table 57"
                    and current.au_code == "Fvm2"
                    and len(cells) >= 3
                    and cells[0] == "05"
                ):
                    current.au_code = "Fvm205"
                    current.sph = f"{current.sph}{cells[1]}"
                    current.si_values = [
                        f"{value}0" if value.endswith(".") else value
                        for value in current.si_values
                    ]
                    current.genetic_gain_values = [
                        f"{value}0" if value.endswith(".") else value
                        for value in current.genetic_gain_values
                    ]
                    current.raw_species_parts.append(cells[2])
                    current.parser_warnings.append("repaired_known_pdf_page_split_fvm205")
                    continue
                if (
                    source_table == "Table 55"
                    and current.au_code == "R301"
                    and cells
                    and cells[0] == "y"
                ):
                    current.sph = "1,000"
                    current.raw_species_parts = ["yc60", "hw19", "ba13", "cw7", "fd1"]
                    current.si_values = ["20.0", "28.0", "25.7", "20.6", "31.3"]
                    current.genetic_gain_values = ["14.3", "", "", "17.0", "10.6"]
                    current.parser_warnings.append("repaired_known_pdf_page_split_r301")
                    continue
                if (
                    source_table == "Table 55"
                    and current.au_code == "R301"
                    and "repaired_known_pdf_page_split_r301" in current.parser_warnings
                ):
                    continue
                continuation_parts = _species_like_cells(cells, include_digit_fragments=False)
                if current.raw_species_parts:
                    continuation_parts.extend(cell for cell in cells if cell.isdigit())
                current.raw_species_parts.extend(continuation_parts)
    if current is not None:
        parsed_rows.append(current)
    return [row.to_record() for row in parsed_rows]


def build_rows() -> pd.DataFrame:
    pdf = _find_pdf()
    with fitz.open(pdf) as doc:
        records: list[dict[str, object]] = []
        for source_table, config in TABLE_CONFIGS.items():
            records.extend(parse_table(doc, source_table, config))
    return pd.DataFrame(records)


def _markdown_table(df: pd.DataFrame, columns: list[str], *, max_rows: int = 20) -> str:
    display = df[columns].head(max_rows)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for _, row in display.iterrows():
        values = []
        for column in columns:
            value = _clean(row[column]).replace("|", "\\|")
            values.append(value)
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows])


def write_outputs(df: pd.DataFrame) -> None:
    df.to_csv(OUTPUT_CSV, index=False)
    table_counts = df.groupby("source_table").size().to_dict()
    confidence_counts = df.groupby(["source_table", "parse_confidence"]).size().to_dict()
    warning_counts = (
        df.assign(parser_warnings=df["parser_warnings"].fillna(""))
        .query("parser_warnings != ''")
        .groupby("source_table")
        .size()
        .to_dict()
    )
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_package_id": SOURCE_PACKAGE_ID,
        "source_sha256": SOURCE_SHA256,
        "output_csv": str(OUTPUT_CSV.relative_to(INSTANCE_ROOT)),
        "row_count": int(len(df)),
        "table_counts": {str(key): int(value) for key, value in table_counts.items()},
        "confidence_counts": {str(key): int(value) for key, value in confidence_counts.items()},
        "warning_row_counts": {str(key): int(value) for key, value in warning_counts.items()},
        "table_configs": {
            table: {
                key: (
                    f"{min(value)}-{max(value)}"
                    if key == "pdf_pages"
                    else value
                )
                for key, value in config.items()
            }
            for table, config in TABLE_CONFIGS.items()
        },
        "use_boundary": (
            "Rows are parser candidates for P10R.2 QA. They are not model inputs "
            "until P10R.3/P10R.4 joins, curve generation, and review gates accept them."
        ),
    }
    OUTPUT_JSON.write_text(json.dumps({"summary": summary, "rows": df.to_dict(orient="records")}, indent=2))

    lines = [
        "# TFL 6 MP11 TIPSY Row Parse",
        "",
        "## Purpose",
        "",
        "This P10R.2 artifact parses the public MP11 per-AU TIPSY input tables ",
        "needed before managed-curve handoff work. It is a parser-candidate ",
        "surface only; rows remain `not_model_input` until later P10R gates ",
        "join them to AU/curve lanes and generate/review curves.",
        "",
        "## Source",
        "",
        f"- Source package: `{SOURCE_PACKAGE_ID}`",
        f"- Source SHA256: `{SOURCE_SHA256}`",
        "- Source tables: Table 54, Table 55, Table 57",
        "- Method: PyMuPDF `find_tables()` plus conservative continuation-row assembly",
        "",
        "## Summary",
        "",
        f"- Parsed rows: `{len(df)}`",
    ]
    for table, count in table_counts.items():
        config = TABLE_CONFIGS[str(table)]
        lines.append(
            f"- `{table}` ({config['curve_lane']}): `{count}` rows "
            f"from PDF pages `{min(config['pdf_pages'])}-{max(config['pdf_pages'])}`"
        )
    lines.extend(
        [
            "",
            "## QA Status",
            "",
            "Rows with `parse_confidence = review_required` need manual review before ",
            "BatchTIPSY/TIPSY handoff. Common causes are PDF line wrapping, split ",
            "species percentages, missing THLB area cells, or species percentages ",
            "that do not sum near 100 after reconstruction.",
            "",
            "### Confidence Counts",
            "",
            _markdown_table(
                (
                    df.groupby(["source_table", "parse_confidence"])
                    .size()
                    .reset_index(name="row_count")
                    .sort_values(["source_table", "parse_confidence"])
                ),
                ["source_table", "parse_confidence", "row_count"],
                max_rows=50,
            ),
            "",
            "### Representative Rows",
            "",
            _markdown_table(
                df,
                [
                    "source_table",
                    "au_code",
                    "sph",
                    "species_composition_raw",
                    "spp1_si",
                    "spp2_si",
                    "spp3_si",
                    "productive_area_ha",
                    "thlb_area_ha",
                    "parse_confidence",
                    "parser_warnings",
                ],
                max_rows=25,
            ),
            "",
            "## Use Boundary",
            "",
            "- Do not promote these rows directly to model inputs.",
            "- P10R.3 must join rows to the AU/curve-lane crosswalk and resolve ",
            "  parser warnings.",
            "- P10R.4 must capture the curve-generation toolchain before any ",
            "  generated curve can become an accepted candidate.",
        ]
    )
    OUTPUT_MD.write_text("\n".join(lines) + "\n")


def main() -> None:
    df = build_rows()
    write_outputs(df)
    print(f"Wrote {len(df)} parser rows to {OUTPUT_CSV.relative_to(INSTANCE_ROOT)}")


if __name__ == "__main__":
    main()
