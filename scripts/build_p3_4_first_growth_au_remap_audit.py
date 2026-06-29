from __future__ import annotations

from pathlib import Path

import distance
import pandas as pd

from femic.pipeline.tsa import build_stratum_lexmatch_alias_map


INSTANCE_ROOT = Path(__file__).resolve().parents[1]


def _build_f_table(static_au: pd.DataFrame) -> pd.DataFrame:
    table = static_au.copy()
    table.index = table["au_id"].astype(str)
    table.index.name = "stratum"
    table["stratum_lexmatch"] = table["au_id"].astype(str)
    total = float(table["area_ha"].sum())
    table["totalarea_p"] = table["area_ha"].astype(float) / total
    return table


def _write_markdown(audit: pd.DataFrame, output_path: Path) -> None:
    non_selected = audit.loc[~audit["selected_top_90_stratum"].astype(bool)].copy()
    alias_used = int(non_selected["lexmatch_alias_used"].sum())
    selected_count = int(audit["selected_top_90_stratum"].sum())
    all_count = len(audit)
    top_preview = non_selected.sort_values("area_ha", ascending=False).head(30)
    lines = [
        "# TFL 6 First-Growth AU Remap Audit",
        "",
        "## Purpose",
        "",
        "Record the P3.4 natural/untreated curve cardinality contract: build curves",
        "only for the selected top-area AU set, then remap non-AU source stratum bins onto",
        "that selected canonical curve universe using the established FEMIC",
        "lexicographic stratum-name matching pattern.",
        "",
        "## Counts",
        "",
        f"- Source stratum bins: `{all_count}`",
        f"- Canonical top-N AUs with curves: `{selected_count}`",
        f"- Non-AU source stratum bins requiring remap/imputation: `{len(non_selected)}`",
        f"- Non-AU source stratum bins with an alias different from source: `{alias_used}`",
        "",
        "## Contract",
        "",
        "- `canonical_curve_au_id` is the curve key to use for Phase 4 natural/",
        "  untreated curve lookup.",
        "- selected top-area AUs map to themselves.",
        "- non-AU source stratum bins map to the closest selected AU by the FEMIC",
        "  lexicographic alias rule, weighted by selected-area support when ties",
        "  occur.",
        "- non-AU source stratum bins are not published as separate canonical natural curve",
        "  families.",
        "",
        "## Largest Non-Selected Remaps",
        "",
    ]
    preview_cols = [
        "source_au_id",
        "canonical_curve_au_id",
        "source_stratum_code",
        "canonical_stratum_code",
        "area_ha",
        "lexmatch_alias_used",
    ]
    if top_preview.empty:
        lines.append("No non-AU source stratum bins require remap.")
    else:
        lines.append(top_preview[preview_cols].to_markdown(index=False))
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `planning/tfl6_first_growth_au_remap_audit.csv`",
            "- `planning/tfl6_first_growth_au_remap_audit.md`",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    static_au = pd.read_csv(
        INSTANCE_ROOT / "planning" / "tfl6_source_stratum_bin_universe.csv"
    )
    static_au["selected_top_90_stratum"] = static_au["selected_top_90_stratum"].astype(
        bool
    )
    selected_au_ids = (
        static_au.loc[static_au["selected_top_90_stratum"], "au_id"]
        .astype(str)
        .tolist()
    )
    f_table = _build_f_table(static_au)
    alias_map = build_stratum_lexmatch_alias_map(
        f_table=f_table,
        stratum_col="stratum",
        selected_strata_codes=selected_au_ids,
        levenshtein_fn=distance.levenshtein,
    )
    lookup = static_au.set_index(static_au["au_id"].astype(str), drop=False)
    rows = []
    for row in static_au.sort_values(["selected_top_90_stratum", "area_ha"]).itertuples(
        index=False
    ):
        source_au_id = str(row.au_id)
        canonical_au_id = (
            source_au_id
            if bool(row.selected_top_90_stratum)
            else alias_map.get(source_au_id, source_au_id)
        )
        canonical = lookup.loc[canonical_au_id]
        rows.append(
            {
                "source_au_id": source_au_id,
                "canonical_curve_au_id": canonical_au_id,
                "selected_top_90_stratum": bool(row.selected_top_90_stratum),
                "lexmatch_alias_used": canonical_au_id != source_au_id,
                "source_stratum_code": row.stratum_code,
                "canonical_stratum_code": canonical["stratum_code"],
                "source_si_class": row.si_class,
                "canonical_si_class": canonical["si_class"],
                "source_bec_group": row.bec_group,
                "canonical_bec_group": canonical["bec_group"],
                "source_species_combo": row.species_combo,
                "canonical_species_combo": canonical["species_combo"],
                "stand_count": int(row.stand_count),
                "area_ha": float(row.area_ha),
                "canonical_selected_area_ha": float(canonical["area_ha"]),
            }
        )
    audit = pd.DataFrame(rows).sort_values(
        ["selected_top_90_stratum", "area_ha", "source_au_id"],
        ascending=[False, False, True],
        kind="stable",
    )
    audit.to_csv(
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_remap_audit.csv",
        index=False,
    )
    _write_markdown(
        audit,
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_remap_audit.md",
    )
    print(
        {
            "source_stratum_bins": len(audit),
            "canonical_top_n_aus": int(audit["selected_top_90_stratum"].sum()),
            "non_au_source_bin_remaps": int((~audit["selected_top_90_stratum"]).sum()),
        }
    )


if __name__ == "__main__":
    main()
