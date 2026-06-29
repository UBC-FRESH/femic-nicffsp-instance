"""Generate the TFL 6 Phase 3 AU/yield-curve Sphinx gallery page."""

from __future__ import annotations

from pathlib import Path


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = INSTANCE_ROOT / "docs" / "phase3-au-yield-curves.rst"
PLOTS_DIR = INSTANCE_ROOT / "plots"


def _figure_block(path: Path, caption: str, *, width: str = "95%") -> list[str]:
    rel_path = path.relative_to(INSTANCE_ROOT).as_posix()
    return [
        f".. figure:: ../{rel_path}",
        f"   :alt: {path.name}",
        f"   :width: {width}",
        "",
        f"   {caption}",
        "",
    ]


def _gallery_section(title: str, pattern: str, caption_prefix: str) -> list[str]:
    paths = sorted(PLOTS_DIR.glob(pattern))
    underline = "~" * len(title)
    lines = [title, underline, ""]
    for path in paths:
        stem = path.stem.removeprefix(pattern.replace("*.png", ""))
        lines.extend(_figure_block(path, f"{caption_prefix} ``{stem}``."))
    return lines


def build_page() -> str:
    lmh_count = len(list(PLOTS_DIR.glob("vdyp_lmh_tfl6-*.png")))
    fitdiag_count = len(list(PLOTS_DIR.glob("vdyp_fitdiag_tfl6-*.png")))
    tipsy_count = len(list(PLOTS_DIR.glob("tipsy_vdyp_tfl6-*.png")))

    lines: list[str] = [
        "Phase 3 Analysis Units and Yield Curves",
        "========================================",
        "",
        "Purpose",
        "-------",
        "",
        "This page is the student- and maintainer-facing gallery for the Phase 3",
        "TFL 6 analysis-unit and yield-curve work. It gathers the static AU",
        "definition, selected-strata plot, natural VDYP first-growth plots, and",
        "treated BatchTIPSY-vs-VDYP overlays in one place.",
        "",
        "The page is a documentation surface, not a model-input bundle. Phase 4",
        "still owns the final Patchworks-facing bundle, XML, Matrix Builder, and",
        "runtime package work.",
        "",
        "AU Definition Contract",
        "----------------------",
        "",
        "The accepted Phase 3 AU policy is static and K3Z-style:",
        "",
        "- BEC zone, subzone, variant, and phase where present;",
        "- top-two VDYP primary-layer species combination;",
        "- stratum-local low/medium/high site-index class; and",
        "- no age, THLB status, operability, treatment eligibility, cedar status,",
        "  NICF identity, or expansion status in the AU key.",
        "",
        "The current source review universe contains ``174`` static strata, ``26``",
        "selected top-area strata covering ``90.397%`` of the yieldable review",
        "area, ``384`` source stratum bins, and ``77`` canonical top-N L/M/H AUs.",
        "",
        "Canonical review files:",
        "",
        "- ``planning/tfl6_au_yield_curve_contract.md``",
        "- ``planning/tfl6_static_au_universe.{csv,json,md}``",
        "- ``planning/tfl6_source_stratum_bin_universe.{csv,json,md}``",
        "- ``planning/tfl6_static_au_top_strata.csv``",
        "- ``planning/tfl6_stand_to_au_review.csv``",
        "- ``planning/tfl6_tipsy_parameter_crosswalk.{csv,json,md}``",
        "",
        "Strata Diagnostic",
        "-----------------",
        "",
        "The strata diagnostic uses the same FEMIC plot specification as the",
        "other instance examples, widened to a ``0-55`` SI axis for the highly",
        "productive coastal rainforest setting.",
        "",
        *_figure_block(
            PLOTS_DIR / "strata-tfl6.png",
            "TFL 6 selected-strata area and site-index distribution plot.",
        ),
        "Yield Curve Artifacts",
        "---------------------",
        "",
        "Natural/untreated first-growth curves use the canonical top-N AU set",
        "and the shared FEMIC smoothing lane. Non-AU source stratum bins are imputed to",
        "selected curve families through the lexicographic remap audit.",
        "",
        "Treated/managed curves use the reviewed MP10 Tables 27-29 parameter",
        "crosswalk and the BTC/BatchTIPSY output generated from",
        "``data/03_input-tfl6.csv``.",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "",
        "   * - Artifact",
        "     - Path",
        "   * - Natural VDYP curves",
        "     - ``planning/tfl6_first_growth_au_curves.csv``",
        "   * - Natural VDYP fit diagnostics",
        "     - ``planning/tfl6_first_growth_shape_diagnostics.{csv,md}``",
        "   * - Non-AU source-bin remap audit",
        "     - ``planning/tfl6_first_growth_au_remap_audit.{csv,md}``",
        "   * - BTC handoff",
        "     - ``data/03_input-tfl6.csv``",
        "   * - BTC output",
        "     - ``data/04_output-tfl6.csv`` and ``data/04_error-tfl6.csv``",
        "   * - Parsed treated curves",
        "     - ``planning/tfl6_tipsy_managed_curves.csv``",
        "   * - Treated-curve diagnostics",
        "     - ``planning/tfl6_tipsy_managed_curve_diagnostics.{csv,md}``",
        "",
        "Gallery Counts",
        "--------------",
        "",
        f"- VDYP L/M/H comparison panels: ``{lmh_count}``",
        f"- VDYP fit-diagnostic panels: ``{fitdiag_count}``",
        f"- TIPSY-vs-VDYP treated overlay panels: ``{tipsy_count}``",
        "",
        "Review Caveats",
        "--------------",
        "",
        "- The selected natural VDYP curve set remains a review surface; smoothing,",
        "  tail constraints, and LMH order gates may be revisited before final",
        "  model-input bundle lock.",
        "- Small fallback ``CWHvm1_DR`` treated rows have high treated-to-natural",
        "  ratios. They remain visible in",
        "  ``planning/tfl6_tipsy_managed_curve_diagnostics.{csv,md}`` for later",
        "  bundle QA.",
        "- MP10 legacy AU codes are parameter provenance only. They are not",
        "  canonical Patchworks AU identities.",
        "",
        "VDYP L/M/H Comparison Gallery",
        "-----------------------------",
        "",
    ]
    lines.extend(
        _gallery_section(
            "Selected Strata L/M/H Panels",
            "vdyp_lmh_tfl6-*.png",
            "Natural VDYP L/M/H comparison panel for stratum",
        )
    )
    lines.extend(["VDYP Fit-Diagnostic Gallery", "---------------------------", ""])
    lines.extend(
        _gallery_section(
            "Selected AU Fit-Diagnostic Panels",
            "vdyp_fitdiag_tfl6-*.png",
            "Natural VDYP fit-diagnostic panel for AU",
        )
    )
    lines.extend(
        [
            "TIPSY-vs-VDYP Treated Overlay Gallery",
            "-------------------------------------",
            "",
        ]
    )
    lines.extend(
        _gallery_section(
            "Selected AU Treated Overlay Panels",
            "tipsy_vdyp_tfl6-*.png",
            "Treated BatchTIPSY-vs-natural VDYP overlay for AU",
        )
    )
    return "\n".join(lines)


def main() -> None:
    DOC_PATH.write_text(build_page(), encoding="utf-8")
    print(DOC_PATH.relative_to(INSTANCE_ROOT).as_posix())


if __name__ == "__main__":
    main()
