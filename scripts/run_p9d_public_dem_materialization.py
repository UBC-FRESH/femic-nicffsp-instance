"""Materialize public CDED DEM evidence for the TFL 6 Step 220 repair lane."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.request
import zipfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd
import rasterio
from rasterio.enums import Resampling
from rasterio.merge import merge
from rasterio.vrt import WarpedVRT


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
VRI_PATH = INSTANCE_ROOT / "data/input/tfl_6/vri_2025_r1_poly_tfl6.gpkg"
TFL6_BOUNDARY_PATH = INSTANCE_ROOT / "data/source/tfl_6/aoi/tfl_6_boundary.gpkg"
SOURCE_ROOT = INSTANCE_ROOT / "runtime/dem/p9d_public_dem/source"
PROCESSED_ROOT = INSTANCE_ROOT / "runtime/dem/p9d_public_dem/processed"
OUTPUT_PREFIX = INSTANCE_ROOT / "planning/tfl6_mp11_p9d_public_dem_source_manifest"

CDED_DATASET_TITLE = "Digital Elevation Model for British Columbia - CDED - 1:250,000"
CDED_DATASET_URL = (
    "https://catalogue.data.gov.bc.ca/dataset/"
    "digital-elevation-model-for-british-columbia-cded-1-250-000"
)
CDED_RESOURCE_ROOT = "https://pub.data.gov.bc.ca/datasets/175624/"
CDED_LICENSE = "Open Government Licence - British Columbia"
BC_ALBERS = "EPSG:3005"
MOSAIC_PATH = PROCESSED_ROOT / "tfl6_cded_dem.tif"


@dataclass(frozen=True)
class DemArchiveRecord:
    """One public CDED archive materialization record."""

    letterblock: str
    archive_name: str
    archive_url: str
    listed_size_text: str
    listed_size_bytes: int | None
    md5_expected: str | None
    md5_actual: str | None
    md5_matches: bool | None
    sha256: str | None
    archive_path: str
    archive_size_bytes: int | None
    dem_path: str | None
    extracted: bool
    raster_readable: bool
    raster_driver: str | None
    raster_crs: str | None
    raster_width: int | None
    raster_height: int | None
    raster_count: int | None
    raster_nodata: float | None
    raster_bounds: tuple[float, float, float, float] | None
    error: str | None


def main() -> None:
    """Run DEM source materialization and write audit manifests."""

    SOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)

    vri = gpd.read_file(VRI_PATH, columns=["map_id"])
    letterblocks = _required_letterblocks(vri)
    archive_rows: list[dict[str, str | int | None]] = []
    records: list[DemArchiveRecord] = []

    for letterblock in letterblocks:
        archive_rows.extend(_list_archives(letterblock))

    for row in archive_rows:
        records.append(_materialize_archive(row))

    readable_paths = [
        Path(record.dem_path)
        for record in records
        if record.dem_path and record.raster_readable
    ]
    mosaic_record = _build_tfl6_mosaic(readable_paths)

    payload = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "dataset_title": CDED_DATASET_TITLE,
        "dataset_url": CDED_DATASET_URL,
        "resource_root_url": CDED_RESOURCE_ROOT,
        "license": CDED_LICENSE,
        "vri_source": str(VRI_PATH.relative_to(INSTANCE_ROOT)),
        "tfl6_boundary_source": str(TFL6_BOUNDARY_PATH.relative_to(INSTANCE_ROOT)),
        "letterblocks": letterblocks,
        "archive_count": len(records),
        "readable_dem_count": len(readable_paths),
        "mosaic": mosaic_record,
        "records": [asdict(record) for record in records],
        "caveat": (
            "CDED 1:250,000 is a coarse public DEM smoke-test source. It is not "
            "equivalent to WFP's LiDAR-derived terrain and 90% slope analysis."
        ),
    }

    _write_json(payload, OUTPUT_PREFIX.with_suffix(".json"))
    _write_csv(records, OUTPUT_PREFIX.with_suffix(".csv"))
    _write_markdown(payload, OUTPUT_PREFIX.with_suffix(".md"))

    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.json')}")
    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.csv')}")
    print(f"Wrote {OUTPUT_PREFIX.with_suffix('.md')}")
    if mosaic_record["created"]:
        print(f"Wrote {MOSAIC_PATH}")


def _required_letterblocks(vri: gpd.GeoDataFrame) -> list[str]:
    values = {
        str(value).strip()[:4].upper()
        for value in vri["map_id"].dropna()
        if str(value).strip()
    }
    if not values:
        raise RuntimeError("VRI input did not contain any usable map_id values.")
    return sorted(values)


def _list_archives(letterblock: str) -> list[dict[str, str | int | None]]:
    directory = letterblock[1:] if letterblock.startswith("0") else letterblock
    index_url = f"{CDED_RESOURCE_ROOT}{directory}/"
    html = urllib.request.urlopen(index_url, timeout=120).read().decode(
        "utf-8",
        errors="ignore",
    )
    rows: list[dict[str, str | int | None]] = []
    pattern = re.compile(
        r'<a href="(?P<name>[0-9a-z]+_[ew]\.dem\.zip)">(?P=name)</a>\s+'
        r'(?P<modified>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s+'
        r'(?P<size>[0-9.]+[KMG]?)',
        flags=re.IGNORECASE,
    )
    for match in pattern.finditer(html):
        archive_name = match.group("name")
        rows.append(
            {
                "letterblock": letterblock,
                "archive_name": archive_name,
                "archive_url": f"{index_url}{archive_name}",
                "listed_size_text": match.group("size"),
                "listed_size_bytes": _parse_size(match.group("size")),
            }
        )
    if not rows:
        raise RuntimeError(f"No CDED DEM archives found at {index_url}")
    return sorted(rows, key=lambda item: str(item["archive_name"]))


def _parse_size(size_text: str) -> int | None:
    match = re.fullmatch(r"(?P<value>[0-9.]+)(?P<unit>[KMG]?)", size_text.strip())
    if not match:
        return None
    value = float(match.group("value"))
    unit = match.group("unit").upper()
    multiplier = {"": 1, "K": 1024, "M": 1024**2, "G": 1024**3}[unit]
    return int(value * multiplier)


def _materialize_archive(row: dict[str, str | int | None]) -> DemArchiveRecord:
    letterblock = str(row["letterblock"])
    archive_name = str(row["archive_name"])
    archive_url = str(row["archive_url"])
    archive_path = SOURCE_ROOT / letterblock / archive_name
    dem_path = archive_path.with_suffix("")
    md5_expected: str | None = None
    md5_actual: str | None = None
    sha256: str | None = None
    error: str | None = None

    try:
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        md5_expected = _read_remote_md5(f"{archive_url}.md5")
        if not archive_path.exists():
            _download(archive_url, archive_path)
        md5_actual = _hash_file(archive_path, "md5")
        sha256 = _hash_file(archive_path, "sha256")
        if not dem_path.exists():
            _extract_dem(archive_path, dem_path)
        metadata = _read_raster_metadata(dem_path)
    except Exception as exc:  # noqa: BLE001 - report per-archive failure.
        error = f"{type(exc).__name__}: {exc}"
        metadata = {
            "raster_readable": False,
            "raster_driver": None,
            "raster_crs": None,
            "raster_width": None,
            "raster_height": None,
            "raster_count": None,
            "raster_nodata": None,
            "raster_bounds": None,
        }

    md5_matches = None
    if md5_expected and md5_actual:
        md5_matches = md5_expected.lower() == md5_actual.lower()

    return DemArchiveRecord(
        letterblock=letterblock,
        archive_name=archive_name,
        archive_url=archive_url,
        listed_size_text=str(row["listed_size_text"]),
        listed_size_bytes=(
            int(row["listed_size_bytes"])
            if row["listed_size_bytes"] is not None
            else None
        ),
        md5_expected=md5_expected,
        md5_actual=md5_actual,
        md5_matches=md5_matches,
        sha256=sha256,
        archive_path=str(archive_path.relative_to(INSTANCE_ROOT)),
        archive_size_bytes=archive_path.stat().st_size if archive_path.exists() else None,
        dem_path=str(dem_path.relative_to(INSTANCE_ROOT)) if dem_path.exists() else None,
        extracted=dem_path.exists(),
        error=error,
        **metadata,
    )


def _read_remote_md5(url: str) -> str | None:
    try:
        text = urllib.request.urlopen(url, timeout=120).read().decode(
            "utf-8",
            errors="ignore",
        )
    except Exception:  # noqa: BLE001 - absent remote MD5 is non-fatal.
        return None
    match = re.search(r"[a-fA-F0-9]{32}", text)
    return match.group(0) if match else None


def _download(url: str, destination: Path) -> None:
    with urllib.request.urlopen(url, timeout=300) as response:
        destination.write_bytes(response.read())


def _hash_file(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _extract_dem(archive_path: Path, dem_path: Path) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        members = [name for name in archive.namelist() if name.lower().endswith(".dem")]
        if not members:
            raise RuntimeError(f"Archive does not contain a .dem member: {archive_path}")
        member = members[0]
        extracted_path = archive_path.parent / member
        archive.extract(member, path=archive_path.parent)
    if extracted_path != dem_path:
        extracted_path.rename(dem_path)


def _read_raster_metadata(path: Path) -> dict[str, object]:
    with rasterio.open(path) as src:
        bounds = src.bounds
        return {
            "raster_readable": True,
            "raster_driver": src.driver,
            "raster_crs": str(src.crs) if src.crs else None,
            "raster_width": src.width,
            "raster_height": src.height,
            "raster_count": src.count,
            "raster_nodata": src.nodata,
            "raster_bounds": (
                float(bounds.left),
                float(bounds.bottom),
                float(bounds.right),
                float(bounds.top),
            ),
        }


def _build_tfl6_mosaic(dem_paths: list[Path]) -> dict[str, object]:
    if not dem_paths:
        return {"created": False, "error": "No readable DEM paths were available."}

    boundary = gpd.read_file(TFL6_BOUNDARY_PATH).to_crs(BC_ALBERS)
    minx, miny, maxx, maxy = [float(value) for value in boundary.total_bounds]
    bounds = (minx, miny, maxx, maxy)
    sources = []
    vrts = []
    try:
        for path in dem_paths:
            src = rasterio.open(path)
            sources.append(src)
            vrts.append(
                WarpedVRT(
                    src,
                    crs=BC_ALBERS,
                    resampling=Resampling.bilinear,
                )
            )
        mosaic, transform = merge(vrts, bounds=bounds, masked=True)
        dem = mosaic[0].filled(-9999).astype("float32")
        profile = {
            "driver": "GTiff",
            "height": dem.shape[0],
            "width": dem.shape[1],
            "count": 1,
            "dtype": "float32",
            "crs": BC_ALBERS,
            "transform": transform,
            "nodata": -9999.0,
            "compress": "deflate",
            "tiled": True,
            "blockxsize": 256,
            "blockysize": 256,
        }
        MOSAIC_PATH.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(MOSAIC_PATH, "w", **profile) as dst:
            dst.write(dem, 1)
    finally:
        for vrt in vrts:
            vrt.close()
        for src in sources:
            src.close()

    with rasterio.open(MOSAIC_PATH) as src:
        array = src.read(1, masked=True)
        valid = array.compressed()
        return {
            "created": True,
            "path": str(MOSAIC_PATH.relative_to(INSTANCE_ROOT)),
            "crs": str(src.crs),
            "width": src.width,
            "height": src.height,
            "pixel_width_m": abs(float(src.transform.a)),
            "pixel_height_m": abs(float(src.transform.e)),
            "bounds": tuple(float(value) for value in src.bounds),
            "valid_pixel_count": int(valid.size),
            "nodata_pixel_count": int(array.mask.sum()) if hasattr(array.mask, "sum") else 0,
            "min_elevation_m": float(valid.min()) if valid.size else None,
            "mean_elevation_m": float(valid.mean()) if valid.size else None,
            "max_elevation_m": float(valid.max()) if valid.size else None,
        }


def _write_json(payload: dict[str, object], path: Path) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_csv(records: list[DemArchiveRecord], path: Path) -> None:
    pd.DataFrame([asdict(record) for record in records]).to_csv(path, index=False)


def _write_markdown(payload: dict[str, object], path: Path) -> None:
    records = payload["records"]
    if not isinstance(records, list):
        raise TypeError("Manifest payload records must be a list.")
    mosaic = payload["mosaic"]
    if not isinstance(mosaic, dict):
        raise TypeError("Manifest payload mosaic must be a dict.")

    readable = sum(1 for record in records if record["raster_readable"])
    md5_ok = sum(1 for record in records if record["md5_matches"] is True)
    md5_bad = sum(1 for record in records if record["md5_matches"] is False)
    extracted = sum(1 for record in records if record["extracted"])

    lines = [
        "# TFL 6 MP11 P9D Public DEM Source Manifest",
        "",
        "## Source",
        "",
        f"- Dataset: `{payload['dataset_title']}`",
        f"- Catalogue URL: `{payload['dataset_url']}`",
        f"- Direct root: `{payload['resource_root_url']}`",
        f"- Licence: `{payload['license']}`",
        f"- Letterblocks: `{', '.join(payload['letterblocks'])}`",
        "",
        "## Materialization Summary",
        "",
        f"- Archive count: `{payload['archive_count']}`",
        f"- Extracted DEM count: `{extracted}`",
        f"- Readable DEM count: `{readable}`",
        f"- Matching remote MD5 count: `{md5_ok}`",
        f"- Failed remote MD5 count: `{md5_bad}`",
        "",
        "## TFL 6 Mosaic",
        "",
    ]
    if mosaic.get("created"):
        lines.extend(
            [
                f"- Path: `{mosaic['path']}`",
                f"- CRS: `{mosaic['crs']}`",
                f"- Dimensions: `{mosaic['width']} x {mosaic['height']}` pixels",
                (
                    f"- Pixel size: `{mosaic['pixel_width_m']:.2f} m x "
                    f"{mosaic['pixel_height_m']:.2f} m`"
                ),
                f"- Valid pixels: `{mosaic['valid_pixel_count']}`",
                f"- Nodata pixels: `{mosaic['nodata_pixel_count']}`",
                f"- Min elevation: `{mosaic['min_elevation_m']:.2f} m`",
                f"- Mean elevation: `{mosaic['mean_elevation_m']:.2f} m`",
                f"- Max elevation: `{mosaic['max_elevation_m']:.2f} m`",
            ]
        )
    else:
        lines.append(f"- Not created: `{mosaic.get('error')}`")

    lines.extend(
        [
            "",
            "## Caveat",
            "",
            str(payload["caveat"]),
            "",
            "## Archive Readback",
            "",
            "| Letterblock | Archive | Size | MD5 | Raster | DEM path |",
            "| --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for record in records:
        md5_status = "ok" if record["md5_matches"] else "missing/fail"
        raster_status = "readable" if record["raster_readable"] else "failed"
        lines.append(
            "| "
            f"`{record['letterblock']}` | "
            f"`{record['archive_name']}` | "
            f"`{record['archive_size_bytes']}` | "
            f"`{md5_status}` | "
            f"`{raster_status}` | "
            f"`{record['dem_path']}` |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
