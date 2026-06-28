"""Record P10R managed-curve generation status and toolchain blockers."""

from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff.csv"
HANDOFF_MAP_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_handoff_map.csv"
OUTPUT_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.csv"
OUTPUT_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.json"
OUTPUT_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.md"

EXECUTABLE_CANDIDATES = [
    INSTANCE_ROOT / "runtime" / "mp11_yield" / "TIPSYbtc.exe",
    INSTANCE_ROOT / "runtime" / "mp11_yield" / "tipsy" / "TIPSYbtc.exe",
    INSTANCE_ROOT / "data" / "downloads" / "tipsy" / "TIPSYbtc.exe",
    INSTANCE_ROOT.parent / "femic" / "reference" / "tipsy" / "TIPSYbtc.exe",
    INSTANCE_ROOT.parent / "femic" / "tipsy_io" / "TIPSYbtc.exe",
]


def _existing_executables() -> list[str]:
    found: list[str] = []
    for candidate in EXECUTABLE_CANDIDATES:
        if candidate.exists():
            found.append(str(candidate))
    for name in ["TIPSYbtc.exe", "tipsybtc", "tipsy", "wine"]:
        resolved = shutil.which(name)
        if resolved:
            found.append(resolved)
    return sorted(set(found))


def build_blocker() -> tuple[pd.DataFrame, dict[str, object]]:
    handoff = pd.read_csv(HANDOFF_CSV)
    handoff_map = pd.read_csv(HANDOFF_MAP_CSV)
    found = _existing_executables()
    candidate_map = handoff_map[
        handoff_map["handoff_status"] == "candidate_for_curve_generation"
    ].copy()
    rows = []
    if found:
        status = "ready_for_manual_tool_execution_review"
        note = (
            "A possible executable/runtime command exists, but this script does "
            "not invoke it automatically. Review licensing, command syntax, and "
            "runtime isolation before running P10R.4 curve generation."
        )
    else:
        status = "blocked_missing_batchtipsy_executable"
        note = (
            "No accepted BatchTIPSY/TIPSY executable was found in configured "
            "public-safe local paths or PATH. Managed curve generation cannot "
            "be claimed until the executable/toolchain is supplied and command "
            "provenance is captured."
        )
    for _, row in candidate_map.iterrows():
        rows.append(
            {
                "feature_id": row["feature_id"],
                "mp11_au_code": row["mp11_au_code"],
                "source_table": row["source_table"],
                "curve_lane": row["curve_lane"],
                "handoff_status": row["handoff_status"],
                "curve_generation_status": status,
                "curve_generation_note": note,
                "output_curve_rows": 0,
                "model_input_status": "not_model_input",
            }
        )
    output = pd.DataFrame(rows)
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "input_handoff_csv": str(HANDOFF_CSV.relative_to(INSTANCE_ROOT)),
        "input_handoff_map_csv": str(HANDOFF_MAP_CSV.relative_to(INSTANCE_ROOT)),
        "handoff_candidate_count": int(len(handoff)),
        "blocked_or_review_rows": int(len(handoff_map) - len(handoff)),
        "searched_executable_candidates": [str(path) for path in EXECUTABLE_CANDIDATES],
        "found_executables_or_runners": found,
        "curve_generation_status": status,
        "curve_generation_note": note,
        "accepted_next_action": (
            "Supply an accepted local BatchTIPSY/TIPSY runtime under an ignored "
            "runtime or data/download path, document licensing and command "
            "syntax, then rerun P10R.4 on candidate rows."
        ),
        "use_boundary": (
            "This artifact is a blocker package. It does not contain generated "
            "curves and must not be treated as an MP11 managed-curve rebuild."
        ),
    }
    return output, summary


def _markdown_table(df: pd.DataFrame, columns: list[str], *, max_rows: int = 30) -> str:
    display = df[columns].head(max_rows)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for _, row in display.iterrows():
        values = []
        for column in columns:
            value = "" if pd.isna(row[column]) else str(row[column]).replace("|", "\\|")
            values.append(value)
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows])


def write_outputs(output: pd.DataFrame, summary: dict[str, object]) -> None:
    output.to_csv(OUTPUT_CSV, index=False)
    OUTPUT_JSON.write_text(
        json.dumps({"summary": summary, "rows": output.to_dict(orient="records")}, indent=2)
        + "\n",
        encoding="utf-8",
    )
    lines = [
        "# TFL 6 MP11 Managed Curve Rebuild Status",
        "",
        "## Purpose",
        "",
        "This P10R.4 artifact records whether MP11 managed curve generation can ",
        "run from the P10R.3 handoff candidates. It is a toolchain status and ",
        "blocker package, not a generated curve output.",
        "",
        "## Status",
        "",
        f"- Handoff candidate rows: `{summary['handoff_candidate_count']}`",
        f"- Blocked or review rows outside handoff: `{summary['blocked_or_review_rows']}`",
        f"- Curve-generation status: `{summary['curve_generation_status']}`",
        f"- Found executables/runners: `{len(summary['found_executables_or_runners'])}`",
        "",
        "## Toolchain Finding",
        "",
        str(summary["curve_generation_note"]),
        "",
        "## Searched Paths",
        "",
        *[f"- `{path}`" for path in summary["searched_executable_candidates"]],
        "",
        "## Candidate Row Status",
        "",
        _markdown_table(
            output,
            [
                "feature_id",
                "mp11_au_code",
                "curve_lane",
                "curve_generation_status",
                "output_curve_rows",
            ],
            max_rows=30,
        ),
        "",
        "## Required Next Action",
        "",
        str(summary["accepted_next_action"]),
        "",
        "## Use Boundary",
        "",
        str(summary["use_boundary"]),
    ]
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    output, summary = build_blocker()
    write_outputs(output, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
