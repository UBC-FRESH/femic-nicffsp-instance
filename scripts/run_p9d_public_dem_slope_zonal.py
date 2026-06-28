"""Derive public CDED slope and P9RF Step 220 candidate zonal statistics."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
DEM_PATH = INSTANCE_ROOT / "runtime/dem/p9d_public_dem/processed/tfl6_cded_dem.tif"
SLOPE_PATH = INSTANCE_ROOT / "runtime/dem/p9d_public_dem/processed/tfl6_cded_slope_pct.tif"
STEP210_GPKG = INSTANCE_ROOT / "planning/tfl6_mp11_p9rf_table12_step_210.gpkg"
OUTPUT_PREFIX = INSTANCE_ROOT / "planning/tfl6_mp11_p9d_public_dem_slope_zonal_stats"
THRESHOLDS = (60.0, 70.0, 80.0, 90.0)
NODATA = -9999.0


def main() -> None:
    """Build percent-slope raster and fragment-level zonal statistics."""

    slope, profile = _derive_slope_raster()
    _write_slope_raster(slope, profile)

    fragments = gpd.read_file(STEP210_GPKG, layer="active_fragments")
    fragments = fragments[fragments.geometry.notna() & ~fragments.geometry.is_empty].copy()
    fragments = fragments.to_crs(profile["crs"])
    zonal = _compute_zonal_stats(fragments, slope, profile)

    summary = _summarize(zonal)
    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "dem_path": str(DEM_PATH.relative_to(INSTANCE_ROOT)),
        "slope_path": str(SLOPE_PATH.relative_to(INSTANCE_ROOT)),
        "step210_active_gpkg": str(STEP210_GPKG.relative_to(INSTANCE_ROOT)),
        "records_csv": str(OUTPUT_PREFIX.with_suffix(".csv").relative_to(INSTANCE_ROOT)),
        "record_count": int(len(zonal)),
        "thresholds_pct": THRESHOLDS,
        "summary": summary,
        "caveat": (
            "Zonal statistics are derived from public CDED 1:250,000 DEM cells "
            "resampled to EPSG:3005. They are suitable as a public proxy test, "
            "not as a replacement for WFP LiDAR-derived terrain classes."
        ),
    }

    zonal.to_csv(OUTPUT_PREFIX.with_suffix(".csv"), index=False)
    OUTPUT_PREFIX.with_suffix(".json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    _write_markdown(payload, OUTPUT_PREFIX.with_suffix(".md"))

    print(f"Wrote {SLOPE_PATH}")
    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.csv')}")
    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.json')}")
    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.md')}")


def _derive_slope_raster() -> tuple[np.ndarray, dict[str, object]]:
    with rasterio.open(DEM_PATH) as src:
        dem = src.read(1).astype("float32")
        profile = src.profile.copy()
        nodata = src.nodata
    dem[dem == nodata] = np.nan
    xres = abs(float(profile["transform"].a))
    yres = abs(float(profile["transform"].e))
    grad_y = np.gradient(dem, yres, axis=0)
    grad_x = np.gradient(dem, xres, axis=1)
    slope = np.sqrt(np.square(grad_x) + np.square(grad_y)) * 100.0
    slope[~np.isfinite(dem)] = np.nan
    slope[~np.isfinite(slope)] = np.nan
    return slope.astype("float32"), profile


def _write_slope_raster(slope: np.ndarray, profile: dict[str, object]) -> None:
    slope_profile = profile.copy()
    slope_profile.update(
        {
            "dtype": "float32",
            "count": 1,
            "nodata": NODATA,
            "compress": "deflate",
            "tiled": True,
            "blockxsize": 256,
            "blockysize": 256,
        }
    )
    SLOPE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(SLOPE_PATH, "w", **slope_profile) as dst:
        dst.write(np.where(np.isfinite(slope), slope, NODATA).astype("float32"), 1)


def _compute_zonal_stats(
    fragments: gpd.GeoDataFrame,
    slope: np.ndarray,
    profile: dict[str, object],
) -> pd.DataFrame:
    frame = fragments.reset_index(drop=True).copy()
    frame["zone_id"] = np.arange(1, len(frame) + 1, dtype=np.int32)
    zones = rasterize(
        (
            (geometry, int(zone_id))
            for geometry, zone_id in zip(frame.geometry, frame["zone_id"], strict=False)
        ),
        out_shape=slope.shape,
        transform=profile["transform"],
        fill=0,
        all_touched=True,
        dtype="int32",
    )
    touched = zones > 0
    valid = touched & np.isfinite(slope)
    pixel_area_ha = (
        abs(float(profile["transform"].a)) * abs(float(profile["transform"].e)) / 10000.0
    )

    valid_df = pd.DataFrame(
        {
            "zone_id": zones[valid].astype("int32"),
            "slope_pct": slope[valid].astype("float32"),
        }
    )
    touched_counts = (
        pd.Series(zones[touched].astype("int32"))
        .value_counts(sort=False)
        .rename_axis("zone_id")
        .rename("touched_pixel_count")
    )
    valid_counts = (
        valid_df.groupby("zone_id", sort=False)
        .size()
        .rename("valid_pixel_count")
    )
    grouped = valid_df.groupby("zone_id", sort=False)["slope_pct"]
    stats = pd.DataFrame(
        {
            "slope_mean_pct": grouped.mean(),
            "slope_median_pct": grouped.median(),
            "slope_p90_pct": grouped.quantile(0.9),
            "slope_max_pct": grouped.max(),
        }
    )
    for threshold in THRESHOLDS:
        col = f"prop_slope_ge_{int(threshold)}pct"
        values = (
            valid_df.assign(is_steep=valid_df["slope_pct"] >= threshold)
            .groupby("zone_id", sort=False)["is_steep"]
            .mean()
        )
        stats[col] = values

    out = frame.drop(columns="geometry").merge(
        touched_counts,
        left_on="zone_id",
        right_index=True,
        how="left",
    )
    out = out.merge(valid_counts, left_on="zone_id", right_index=True, how="left")
    out = out.merge(stats, left_on="zone_id", right_index=True, how="left")
    out["touched_pixel_count"] = out["touched_pixel_count"].fillna(0).astype(int)
    out["valid_pixel_count"] = out["valid_pixel_count"].fillna(0).astype(int)
    out["nodata_pixel_count"] = out["touched_pixel_count"] - out["valid_pixel_count"]
    out["valid_pixel_area_ha"] = out["valid_pixel_count"] * pixel_area_ha
    out["source_fragment_area_ha"] = out["area_ha"].astype(float)
    keep_cols = [
        "fragment_id",
        "source_polygon_id",
        "parent_fragment_id",
        "step_id",
        "deduction_status",
        "source_fragment_area_ha",
        "zone_id",
        "touched_pixel_count",
        "valid_pixel_count",
        "nodata_pixel_count",
        "valid_pixel_area_ha",
        "slope_mean_pct",
        "slope_median_pct",
        "slope_p90_pct",
        "slope_max_pct",
        *[f"prop_slope_ge_{int(threshold)}pct" for threshold in THRESHOLDS],
    ]
    return out[keep_cols]


def _summarize(zonal: pd.DataFrame) -> dict[str, float | int | None]:
    valid = zonal[zonal["valid_pixel_count"] > 0].copy()
    total_area = float(zonal["source_fragment_area_ha"].sum())
    valid_area = float(valid["source_fragment_area_ha"].sum())
    summary: dict[str, float | int | None] = {
        "fragment_count": int(len(zonal)),
        "fragments_with_valid_pixels": int(len(valid)),
        "fragments_without_valid_pixels": int(len(zonal) - len(valid)),
        "source_area_ha": total_area,
        "source_area_with_valid_pixels_ha": valid_area,
        "source_area_without_valid_pixels_ha": total_area - valid_area,
        "mean_slope_pct_area_unweighted": (
            float(valid["slope_mean_pct"].mean()) if not valid.empty else None
        ),
        "median_slope_pct_area_unweighted": (
            float(valid["slope_median_pct"].median()) if not valid.empty else None
        ),
        "max_slope_pct": float(valid["slope_max_pct"].max()) if not valid.empty else None,
    }
    for threshold in THRESHOLDS:
        prop_col = f"prop_slope_ge_{int(threshold)}pct"
        any_area = valid.loc[valid[prop_col] > 0, "source_fragment_area_ha"].sum()
        majority_area = valid.loc[valid[prop_col] >= 0.5, "source_fragment_area_ha"].sum()
        summary[f"area_any_slope_ge_{int(threshold)}pct_ha"] = float(any_area)
        summary[f"area_majority_slope_ge_{int(threshold)}pct_ha"] = float(majority_area)
    return summary


def _write_markdown(payload: dict[str, object], path: Path) -> None:
    summary = payload["summary"]
    if not isinstance(summary, dict):
        raise TypeError("Payload summary must be a dict.")

    lines = [
        "# TFL 6 MP11 P9D Public DEM Slope Zonal Statistics",
        "",
        "## Inputs",
        "",
        f"- DEM: `{payload['dem_path']}`",
        f"- Slope raster: `{payload['slope_path']}`",
        f"- Step 210 active fragments: `{payload['step210_active_gpkg']}`",
        f"- Thresholds: `{', '.join(str(x) for x in payload['thresholds_pct'])}`",
        "",
        "## Summary",
        "",
        f"- Fragment count: `{summary['fragment_count']}`",
        f"- Fragments with valid DEM pixels: `{summary['fragments_with_valid_pixels']}`",
        f"- Fragments without valid DEM pixels: `{summary['fragments_without_valid_pixels']}`",
        f"- Source area: `{summary['source_area_ha']:.3f} ha`",
        (
            "- Source area with valid pixels: "
            f"`{summary['source_area_with_valid_pixels_ha']:.3f} ha`"
        ),
        (
            "- Source area without valid pixels: "
            f"`{summary['source_area_without_valid_pixels_ha']:.3f} ha`"
        ),
        f"- Maximum slope: `{summary['max_slope_pct']:.3f}%`",
        "",
        "## Threshold Diagnostics",
        "",
        "| Threshold | Area with any steep pixel | Area majority steep |",
        "| ---: | ---: | ---: |",
    ]
    for threshold in THRESHOLDS:
        lines.append(
            "| "
            f"`{int(threshold)}%` | "
            f"`{summary[f'area_any_slope_ge_{int(threshold)}pct_ha']:.3f} ha` | "
            f"`{summary[f'area_majority_slope_ge_{int(threshold)}pct_ha']:.3f} ha` |"
        )
    lines.extend(["", "## Caveat", "", str(payload["caveat"]), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
