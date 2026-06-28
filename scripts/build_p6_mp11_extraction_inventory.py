"""Build an initial MP11 extraction inventory with page/component anchors."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SOURCE_PACKAGE_ID = "tfl6_mp11_202606_public_pdf"
SOURCE_SHA256 = "44591c1024254e36d8989df45a2b489a624d5669c5ae01a6ebfd961b50a7321b"
HIGH_PRIORITY_TERMS = {
    "AAC": "aac",
    "allowable annual cut": "aac",
    "THLB": "land_base",
    "timber harvesting land base": "land_base",
    "productive forest": "land_base",
    "LiDAR": "inventory_yield",
    "Individual Tree Inventory": "inventory_yield",
    "ITI": "inventory_yield",
    "VRI": "inventory_yield",
    "operability": "inventory_yield",
    "minimum harvest age": "model_behavior",
    "base case": "model_behavior",
    "sensitivity": "model_behavior",
    "harvest level": "model_behavior",
    "cedar": "inventory_yield",
    "old seral": "inventory_yield",
}


@dataclass(frozen=True)
class ExtractionInventoryRow:
    """One raw P6.2 extraction-inventory row."""

    record_id: str
    source_package_id: str
    source_sha256: str
    document_component: str
    pdf_page: int
    reported_page_label: str
    section_path: str
    object_type: str
    object_id: str
    object_title: str
    claim_text: str
    normalized_value: str
    units: str
    comparison_topic: str
    extraction_method: str
    tool_versions: str
    source_artifact: str
    review_status: str
    downstream_use: str
    model_input_status: str
    reviewer: str
    reviewed_at_utc: str
    notes: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as src:
        return list(csv.DictReader(src))


def _component_for_page(components: list[dict[str, str]], pdf_page: int) -> str:
    for row in components:
        if int(row["pdf_page_start"]) <= pdf_page <= int(row["pdf_page_end"]):
            return row["component_id"]
    return "unknown_component"


def _reported_page_label(text: str) -> str:
    for pattern in [
        r"Page\s+[ivxlcdm]+\b",
        r"Page\s+\d+\s+of\s+\d+",
        r"Page\s+\d+\b",
    ]:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return ""


def _clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def _comparison_topic(text: str, default: str = "metadata") -> str:
    lowered = text.lower()
    for term, topic in HIGH_PRIORITY_TERMS.items():
        if term.lower() in lowered:
            return topic
    return default


def _is_heading(line: str) -> bool:
    if "..." in line or len(line) > 120:
        return False
    if re.match(r"^\d+(?:\.\d+){0,4}\s+[A-Z][A-Za-z0-9,()/#&' -]{3,}$", line):
        return True
    return line in {"Executive Summary", "Acknowledgements", "References", "Appendices"}


def _table_or_figure(line: str) -> tuple[str, str, str] | None:
    match = re.match(r"^(Table|Figure)\s+(\d+[A-Za-z]?)\s+(.+)$", line)
    if not match:
        return None
    kind, number, title = match.groups()
    return kind.lower(), f"{kind} {number}", title.strip()


def _priority_claim(line: str) -> bool:
    lowered = line.lower()
    if len(line) < 40 or len(line) > 360:
        return False
    if any(term.lower() in lowered for term in HIGH_PRIORITY_TERMS):
        return bool(re.search(r"\d", line)) or any(
            term in lowered for term in ["base case", "sensitivity", "cedar", "old seral"]
        )
    return False


def _dedupe(rows: list[ExtractionInventoryRow]) -> list[ExtractionInventoryRow]:
    seen: set[tuple[Any, ...]] = set()
    unique: list[ExtractionInventoryRow] = []
    for row in rows:
        key = (
            row.document_component,
            row.pdf_page,
            row.object_type,
            row.object_id,
            row.claim_text,
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return [
        ExtractionInventoryRow(
            **{
                **asdict(row),
                "record_id": f"mp11-{idx:04d}-{row.object_type}",
            }
        )
        for idx, row in enumerate(unique, start=1)
    ]


def build_inventory(
    source_pdf: Path,
    components_csv: Path,
    output_csv: Path,
    output_json: Path,
    output_md: Path,
    extracted_at_utc: str,
) -> list[ExtractionInventoryRow]:
    import fitz

    components = _read_csv(components_csv)
    doc = fitz.open(source_pdf)
    tool_versions = json.dumps({"pymupdf": fitz.version[0]}, sort_keys=True)
    rows: list[ExtractionInventoryRow] = []

    for page_index, page in enumerate(doc):
        pdf_page = page_index + 1
        text = page.get_text("text")
        component = _component_for_page(components, pdf_page)
        page_label = _reported_page_label(text)
        current_section = ""
        for raw_line in text.splitlines():
            line = _clean_line(raw_line)
            if not line:
                continue
            if _is_heading(line):
                current_section = line
                rows.append(
                    _row(
                        component=component,
                        pdf_page=pdf_page,
                        page_label=page_label,
                        section_path=current_section,
                        object_type="heading",
                        object_id="",
                        object_title=line,
                        claim_text=line,
                        comparison_topic=_comparison_topic(line),
                        tool_versions=tool_versions,
                        notes="Raw heading candidate from PDF text extraction.",
                    )
                )
                continue
            table_or_figure = _table_or_figure(line)
            if table_or_figure:
                object_type, object_id, title = table_or_figure
                rows.append(
                    _row(
                        component=component,
                        pdf_page=pdf_page,
                        page_label=page_label,
                        section_path=current_section,
                        object_type=object_type,
                        object_id=object_id,
                        object_title=title,
                        claim_text=f"{object_id} {title}",
                        comparison_topic=_comparison_topic(title),
                        tool_versions=tool_versions,
                        notes="Raw table/figure title candidate from PDF text extraction.",
                    )
                )
                continue
            if _priority_claim(line):
                rows.append(
                    _row(
                        component=component,
                        pdf_page=pdf_page,
                        page_label=page_label,
                        section_path=current_section,
                        object_type="claim_candidate",
                        object_id="",
                        object_title="",
                        claim_text=line,
                        comparison_topic=_comparison_topic(line),
                        tool_versions=tool_versions,
                        notes="Keyword-selected raw claim candidate; requires review before use.",
                    )
                )
    rows = _dedupe(rows)
    _write_csv(output_csv, [asdict(row) for row in rows])
    payload = {
        "source_package_id": SOURCE_PACKAGE_ID,
        "source_sha256": SOURCE_SHA256,
        "source_pdf": source_pdf.as_posix(),
        "extracted_at_utc": extracted_at_utc,
        "inventory_csv": output_csv.as_posix(),
        "row_count": len(rows),
        "object_type_counts": dict(sorted(Counter(row.object_type for row in rows).items())),
        "comparison_topic_counts": dict(
            sorted(Counter(row.comparison_topic for row in rows).items())
        ),
        "document_component_counts": dict(
            sorted(Counter(row.document_component for row in rows).items())
        ),
        "review_status_counts": dict(sorted(Counter(row.review_status for row in rows).items())),
        "model_input_status_counts": dict(
            sorted(Counter(row.model_input_status for row in rows).items())
        ),
    }
    output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _write_markdown(output_md, payload)
    return rows


def _row(
    *,
    component: str,
    pdf_page: int,
    page_label: str,
    section_path: str,
    object_type: str,
    object_id: str,
    object_title: str,
    claim_text: str,
    comparison_topic: str,
    tool_versions: str,
    notes: str,
) -> ExtractionInventoryRow:
    return ExtractionInventoryRow(
        record_id="",
        source_package_id=SOURCE_PACKAGE_ID,
        source_sha256=SOURCE_SHA256,
        document_component=component,
        pdf_page=pdf_page,
        reported_page_label=page_label,
        section_path=section_path,
        object_type=object_type,
        object_id=object_id,
        object_title=object_title,
        claim_text=claim_text,
        normalized_value="",
        units="",
        comparison_topic=comparison_topic,
        extraction_method="PyMuPDF text extraction with regex triage",
        tool_versions=tool_versions,
        source_artifact="",
        review_status="raw_extraction",
        downstream_use="phase6_inventory_triage_only",
        model_input_status="not_model_input",
        reviewer="",
        reviewed_at_utc="",
        notes=notes,
    )


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# TFL 6 MP11 Extraction Inventory",
        "",
        "## Purpose",
        "",
        "This P6.2 inventory is the first structured extraction pass over the MP11",
        "PDF. It records raw heading, table, figure, and high-priority claim",
        "candidates with source SHA256, document component, one-based PDF page,",
        "review status, downstream use, and model-input status.",
        "",
        "This is an inventory surface only. Rows are `raw_extraction`, downstream",
        "use is `phase6_inventory_triage_only`, and model-input status is",
        "`not_model_input`.",
        "",
        "## Files",
        "",
        f"- CSV: `{payload['inventory_csv']}`",
        "- JSON summary: `planning/tfl6_mp11_extraction_inventory_summary.json`",
        "- Markdown summary: `planning/tfl6_mp11_extraction_inventory_summary.md`",
        "",
        "## Counts",
        "",
        f"- Row count: `{payload['row_count']}`",
        f"- Object type counts: `{payload['object_type_counts']}`",
        f"- Comparison topic counts: `{payload['comparison_topic_counts']}`",
        f"- Document component counts: `{payload['document_component_counts']}`",
        f"- Review status counts: `{payload['review_status_counts']}`",
        f"- Model-input status counts: `{payload['model_input_status_counts']}`",
        "",
        "## Interpretation",
        "",
        "Use this file as the extraction queue for detailed P6.2 review. It is not",
        "a reviewed source of model assumptions. Phase 7 figure closeout evidence",
        "should be linked where relevant instead of duplicating recovered figure",
        "tables into this raw inventory.",
        "",
        "## Next Step",
        "",
        "Review and normalize the highest-priority table and claim rows into",
        "P6.3-P6.5 comparison crosswalks. Keep raw extraction separate from",
        "reviewed evidence and accepted model contracts.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_pdf", type=Path)
    parser.add_argument(
        "--components-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_document_components.csv"),
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("planning/tfl6_mp11_extraction_inventory.csv"),
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=Path("planning/tfl6_mp11_extraction_inventory_summary.json"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("planning/tfl6_mp11_extraction_inventory_summary.md"),
    )
    parser.add_argument(
        "--extracted-at-utc",
        default=datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    args = parser.parse_args()
    rows = build_inventory(
        source_pdf=args.source_pdf,
        components_csv=args.components_csv,
        output_csv=args.output_csv,
        output_json=args.output_json,
        output_md=args.output_md,
        extracted_at_utc=args.extracted_at_utc,
    )
    print(f"wrote {len(rows)} rows")
    print(args.output_csv)
    print(args.output_json)
    print(args.output_md)


if __name__ == "__main__":
    main()
