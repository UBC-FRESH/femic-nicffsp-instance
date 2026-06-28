"""Record maintainer review of P10R TIPSY-vs-VDYP diagnostic plots."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
FAILED_AU_CODES = {"FMH01", "FMH22", "Fvh103"}
PASSED_STATUS = "passed_tipsy_vdyp_sanity_review"
FAILED_STATUS = "failed_tipsy_below_vdyp_sanity_review"
MODEL_INPUT_STATUS = "not_model_input"
FAILED_NOTE = (
    "Maintainer plot review rejected this generated TIPSY curve because "
    "plantation yield should meet or beat the matched natural VDYP curve; "
    "observed TIPSY is substantially below VDYP."
)
PASSED_NOTE = (
    "Maintainer plot review found no TIPSY-vs-VDYP sanity objection for this "
    "diagnostic plot."
)

CURVES_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.csv"
CURVES_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curves.json"
COMPARISON_CSV = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.csv"
COMPARISON_JSON = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.json"
COMPARISON_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_comparison.md"
PLOT_MANIFEST_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.csv"
)
PLOT_MANIFEST_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.json"
)
PLOT_MANIFEST_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_plot_manifest.md"
)
TIPSY_VDYP_MANIFEST_CSV = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_vdyp_diagnostic_manifest.csv"
)
TIPSY_VDYP_MANIFEST_JSON = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_vdyp_diagnostic_manifest.json"
)
TIPSY_VDYP_MANIFEST_MD = (
    INSTANCE_ROOT / "planning" / "tfl6_mp11_tipsy_vdyp_diagnostic_manifest.md"
)
REBUILD_MD = INSTANCE_ROOT / "planning" / "tfl6_mp11_managed_curve_rebuild.md"


def _review_status_for(code: object) -> str:
    return FAILED_STATUS if str(code) in FAILED_AU_CODES else PASSED_STATUS


def _review_note_for(code: object) -> str:
    return FAILED_NOTE if str(code) in FAILED_AU_CODES else PASSED_NOTE


def _mark_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["review_status"] = df["mp11_au_code"].map(_review_status_for)
    df["plot_review_note"] = df["mp11_au_code"].map(_review_note_for)
    df["model_input_status"] = MODEL_INPUT_STATUS
    df.to_csv(path, index=False)
    return df


def _mark_json(path: Path, rows_key: str) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload[rows_key]
    for row in rows:
        code = row["mp11_au_code"]
        row["review_status"] = _review_status_for(code)
        row["plot_review_note"] = _review_note_for(code)
        row["model_input_status"] = MODEL_INPUT_STATUS
    counts = pd.Series([row["review_status"] for row in rows]).value_counts().to_dict()
    if "summary" in payload:
        payload["summary"]["review_status_counts"] = counts
        payload["summary"]["failed_plot_review_au_codes"] = sorted(FAILED_AU_CODES)
    else:
        payload["review_status_counts"] = counts
        payload["failed_plot_review_au_codes"] = sorted(FAILED_AU_CODES)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def _insert_or_replace_section(path: Path, lines: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    heading = lines[0]
    next_heading = "\n## "
    if heading in text:
        start = text.index(heading)
        next_start = text.find(next_heading, start + len(heading))
        replacement = "\n".join(lines)
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + replacement + "\n"
        else:
            text = (
                text[:start].rstrip() + "\n\n" + replacement + "\n" + text[next_start:]
            )
    else:
        insert_at = text.find("## Use Boundary")
        replacement = "\n".join(lines)
        if insert_at == -1:
            text = text.rstrip() + "\n\n" + replacement + "\n"
        else:
            text = (
                text[:insert_at].rstrip()
                + "\n\n"
                + replacement
                + "\n\n"
                + text[insert_at:]
            )
    path.write_text(text, encoding="utf-8")


def _review_section(title: str) -> list[str]:
    timestamp = datetime.now(UTC).isoformat(timespec="seconds")
    failed = ", ".join(f"`{code}`" for code in sorted(FAILED_AU_CODES))
    return [
        title,
        "",
        f"- Passed TIPSY-vs-VDYP sanity rows: `{27 - len(FAILED_AU_CODES)}`",
        f"- Failed TIPSY-vs-VDYP sanity rows: `{len(FAILED_AU_CODES)}`",
        f"- Failed AU codes: {failed}",
        f"- Failed review status: `{FAILED_STATUS}`",
        f"- Passed review status: `{PASSED_STATUS}`",
        f"- Model-input status: `{MODEL_INPUT_STATUS}`",
        f"- Review timestamp UTC: `{timestamp}`",
        f"- Failed-row rationale: {FAILED_NOTE}",
    ]


def _update_markdown() -> None:
    section = _review_section("## Maintainer Plot Review")
    for path in [COMPARISON_MD, PLOT_MANIFEST_MD, TIPSY_VDYP_MANIFEST_MD]:
        _insert_or_replace_section(path, section)

    text = REBUILD_MD.read_text(encoding="utf-8")
    replacement = (
        "- Review status: `passed_tipsy_vdyp_sanity_review` for `24` candidate "
        "curves; `failed_tipsy_below_vdyp_sanity_review` for `3` candidate "
        "curves (`FMH01`, `FMH22`, `Fvh103`).\n"
        f"- Model-input status: `{MODEL_INPUT_STATUS}`"
    )
    if "- Review status:" in text:
        lines = text.splitlines()
        updated: list[str] = []
        skip_next_model_status = False
        for line in lines:
            if line.startswith("- Review status:"):
                updated.extend(replacement.splitlines())
                skip_next_model_status = True
                continue
            if skip_next_model_status and line.startswith("- Model-input status:"):
                skip_next_model_status = False
                continue
            skip_next_model_status = False
            updated.append(line)
        text = "\n".join(updated) + "\n"
    REBUILD_MD.write_text(text, encoding="utf-8")


def main() -> None:
    curve_df = _mark_csv(CURVES_CSV)
    comparison_df = _mark_csv(COMPARISON_CSV)
    plot_df = _mark_csv(PLOT_MANIFEST_CSV)
    diagnostic_df = _mark_csv(TIPSY_VDYP_MANIFEST_CSV)

    _mark_json(CURVES_JSON, "rows")
    _mark_json(COMPARISON_JSON, "records")
    _mark_json(PLOT_MANIFEST_JSON, "records")
    _mark_json(TIPSY_VDYP_MANIFEST_JSON, "records")
    _update_markdown()

    print(
        "Recorded P10R TIPSY-vs-VDYP plot review: "
        f"curve_rows={len(curve_df)}, comparison_rows={len(comparison_df)}, "
        f"managed_plot_rows={len(plot_df)}, diagnostic_rows={len(diagnostic_df)}, "
        f"failed_aus={','.join(sorted(FAILED_AU_CODES))}"
    )


if __name__ == "__main__":
    main()
