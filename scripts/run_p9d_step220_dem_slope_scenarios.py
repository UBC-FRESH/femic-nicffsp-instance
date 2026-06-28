"""Compare public DEM steep-slope scenarios for MP11 Table 12 Step 220."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
ZONAL_CSV = INSTANCE_ROOT / "planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats.csv"
OUTPUT_PREFIX = INSTANCE_ROOT / "planning/tfl6_mp11_p9d_step220_dem_slope_scenarios"
MP11_STEP220_TARGET_HA = 1_820.0
THRESHOLDS = (60, 70, 80, 90)
MIN_PROPORTIONS = (0.25, 0.5, 0.75, 0.9, 1.0)


def main() -> None:
    """Run Step 220 whole-fragment and partial-area scenario comparisons."""

    zonal = pd.read_csv(ZONAL_CSV)
    step210_source_area_ha = float(zonal["source_fragment_area_ha"].sum())
    scenario_rows = []
    for threshold in THRESHOLDS:
        prop_col = f"prop_slope_ge_{threshold}pct"
        for min_prop in MIN_PROPORTIONS:
            mask = zonal[prop_col].fillna(0.0) >= min_prop
            whole_area = float(zonal.loc[mask, "source_fragment_area_ha"].sum())
            partial_area = float(
                (
                    zonal["source_fragment_area_ha"].fillna(0.0)
                    * zonal[prop_col].fillna(0.0)
                ).sum()
            )
            scenario_rows.append(
                _scenario_row(
                    threshold=threshold,
                    min_prop=min_prop,
                    accounting="whole_fragment",
                    deduction_ha=whole_area,
                    step210_source_area_ha=step210_source_area_ha,
                    fragment_count=int(mask.sum()),
                    valid_fragment_count=int((zonal["valid_pixel_count"] > 0).sum()),
                )
            )
            scenario_rows.append(
                _scenario_row(
                    threshold=threshold,
                    min_prop=min_prop,
                    accounting="partial_area_diagnostic",
                    deduction_ha=partial_area,
                    step210_source_area_ha=step210_source_area_ha,
                    fragment_count=int((zonal[prop_col].fillna(0.0) > 0.0).sum()),
                    valid_fragment_count=int((zonal["valid_pixel_count"] > 0).sum()),
                )
            )

    scenarios = pd.DataFrame(scenario_rows)
    scenarios = scenarios.sort_values(
        ["abs_delta_to_mp11_ha", "accounting", "threshold_pct", "min_steep_proportion"],
    ).reset_index(drop=True)
    best_whole = scenarios[scenarios["accounting"] == "whole_fragment"].iloc[0].to_dict()
    best_partial = scenarios[
        scenarios["accounting"] == "partial_area_diagnostic"
    ].iloc[0].to_dict()
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "zonal_stats": str(ZONAL_CSV.relative_to(INSTANCE_ROOT)),
        "mp11_step220_target_ha": MP11_STEP220_TARGET_HA,
        "step210_source_area_ha": step210_source_area_ha,
        "best_whole_fragment_candidate": best_whole,
        "best_partial_area_diagnostic": best_partial,
        "records": scenarios.to_dict(orient="records"),
        "recommended_review_focus": (
            "Prefer whole-fragment scenarios for the resultant-fragment netdown. "
            "The partial-area rows are diagnostics only because the production "
            "P9RF lane physically removes resultant fragments."
        ),
        "caveat": (
            "CDED-derived thresholds are public-data proxies. A lower CDED slope "
            "threshold may be defensible because coarse DEM smoothing suppresses "
            "local LiDAR-grade slopes, but this must be recorded as a proxy rule, "
            "not as WFP LiDAR equivalence."
        ),
    }

    scenarios.to_csv(OUTPUT_PREFIX.with_suffix(".csv"), index=False)
    OUTPUT_PREFIX.with_suffix(".json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    _write_markdown(payload, OUTPUT_PREFIX.with_suffix(".md"))

    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.csv')}")
    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.json')}")
    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.md')}")


def _scenario_row(
    *,
    threshold: int,
    min_prop: float,
    accounting: str,
    deduction_ha: float,
    step210_source_area_ha: float,
    fragment_count: int,
    valid_fragment_count: int,
) -> dict[str, float | int | str]:
    remaining_after_step220 = step210_source_area_ha - deduction_ha
    return {
        "scenario_id": f"slope_ge_{threshold}_prop_ge_{min_prop:g}_{accounting}",
        "threshold_pct": threshold,
        "min_steep_proportion": min_prop,
        "accounting": accounting,
        "fragment_count": fragment_count,
        "valid_fragment_count": valid_fragment_count,
        "deduction_ha": deduction_ha,
        "delta_to_mp11_ha": deduction_ha - MP11_STEP220_TARGET_HA,
        "abs_delta_to_mp11_ha": abs(deduction_ha - MP11_STEP220_TARGET_HA),
        "delta_to_mp11_pct": (
            (deduction_ha - MP11_STEP220_TARGET_HA) / MP11_STEP220_TARGET_HA * 100.0
        ),
        "remaining_after_step220_ha": remaining_after_step220,
    }


def _write_markdown(payload: dict[str, object], path: Path) -> None:
    records = payload["records"]
    if not isinstance(records, list):
        raise TypeError("Payload records must be a list.")
    whole = payload["best_whole_fragment_candidate"]
    partial = payload["best_partial_area_diagnostic"]
    if not isinstance(whole, dict) or not isinstance(partial, dict):
        raise TypeError("Candidate summaries must be dictionaries.")

    top_whole = [row for row in records if row["accounting"] == "whole_fragment"][:8]
    lines = [
        "# TFL 6 MP11 P9D Step 220 Public DEM Slope Scenarios",
        "",
        "## Purpose",
        "",
        (
            "Compare public CDED steep-slope rules against MP11 Table 12 Step "
            "220 before deciding whether a public DEM proxy can replace the "
            "current zero-deduction placeholder."
        ),
        "",
        "## Benchmark",
        "",
        f"- MP11 Step 220 target deduction: `{payload['mp11_step220_target_ha']:.3f} ha`",
        f"- Step 210 source area: `{payload['step210_source_area_ha']:.3f} ha`",
        "",
        "## Best Whole-Fragment Candidate",
        "",
        f"- Scenario: `{whole['scenario_id']}`",
        f"- Deduction: `{whole['deduction_ha']:.3f} ha`",
        f"- Delta to MP11 Step 220: `{whole['delta_to_mp11_ha']:.3f} ha`",
        f"- Percent delta: `{whole['delta_to_mp11_pct']:.3f}%`",
        "",
        "## Best Partial-Area Diagnostic",
        "",
        f"- Scenario: `{partial['scenario_id']}`",
        f"- Deduction: `{partial['deduction_ha']:.3f} ha`",
        f"- Delta to MP11 Step 220: `{partial['delta_to_mp11_ha']:.3f} ha`",
        "",
        "## Top Whole-Fragment Scenarios",
        "",
        "| Scenario | Deduction | Delta | Percent delta | Fragments |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in top_whole:
        lines.append(
            "| "
            f"`{row['scenario_id']}` | "
            f"`{row['deduction_ha']:.3f}` | "
            f"`{row['delta_to_mp11_ha']:.3f}` | "
            f"`{row['delta_to_mp11_pct']:.3f}%` | "
            f"`{row['fragment_count']}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            str(payload["recommended_review_focus"]),
            "",
            str(payload["caveat"]),
            "",
            (
                "Final Current THLB and Long-term Land Base deltas must come from "
                "rerunning the P9RF resultant-fragment netdown with the selected "
                "Step 220 rule physically applied."
            ),
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
