from __future__ import annotations

from pathlib import Path
import shutil
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
INSTANCE_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))


def _upper_columns(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.copy()
    normalized.columns = [str(column).upper() for column in normalized.columns]
    return normalized


def _vdyp_table_to_rows(
    feature_id: int, table: pd.DataFrame
) -> list[dict[str, float | int]]:
    if table is None or table.empty:
        return []
    working = table.copy()
    working.columns = [str(column).upper() for column in working.columns]
    age_column = next(
        (
            column
            for column in ("PRJ_TOTAL_AGE", "TOTAL_AGE", "AGE")
            if column in working.columns
        ),
        None,
    )
    volume_column = next(
        (
            column
            for column in ("PRJ_VOL_DWB", "VOL_DWB", "VDWB", "DWB")
            if column in working.columns
        ),
        None,
    )
    year_column = next(
        (column for column in ("PRJ_YEAR", "YEAR") if column in working.columns), None
    )
    if age_column is None and working.index.name is not None:
        age_values = pd.to_numeric(
            pd.Series(working.index, index=working.index), errors="coerce"
        )
    elif age_column is not None:
        age_values = pd.to_numeric(working[age_column], errors="coerce")
    else:
        return []
    if volume_column is None:
        return []
    volume_values = pd.to_numeric(working[volume_column], errors="coerce")
    year_values = (
        pd.to_numeric(working[year_column], errors="coerce")
        if year_column is not None
        else pd.Series(-1, index=working.index)
    )
    rows: list[dict[str, float | int]] = []
    for age, volume, year in zip(age_values, volume_values, year_values, strict=False):
        if pd.isna(age) or pd.isna(volume):
            continue
        rows.append(
            {
                "FEATURE_ID": int(feature_id),
                "PRJ_TOTAL_AGE": int(float(age)),
                "PRJ_VOL_DWB": float(volume),
                "PRJ_YEAR": int(float(year))
                if year is not None and not pd.isna(year)
                else -1,
            }
        )
    return rows


def main() -> None:
    from femic.pipeline.mkrf_first_growth import build_mkrf_first_growth_curves
    from femic.pipeline.vdyp_stage import execute_vdyp_batch

    output_root = (
        INSTANCE_ROOT / "runtime" / "derived" / "p3_4_aflb_vdyp_first_growth_run2"
    )
    output_root.mkdir(parents=True, exist_ok=True)
    vdyp_io = output_root / "vdyp_io"
    vdyp_io.mkdir(parents=True, exist_ok=True)
    source_cfg = REPO_ROOT / "VDYP7" / "VDYP7" / "VDYP_CFG"
    source_ini = REPO_ROOT / "VDYP7" / "VDYP7" / "VDYP.INI"
    if source_cfg.is_dir():
        shutil.copytree(source_cfg, vdyp_io / "VDYP_CFG", dirs_exist_ok=True)
    if source_ini.is_file():
        shutil.copy2(source_ini, vdyp_io / "VDYP.INI")

    assignment_source = pd.read_csv(
        INSTANCE_ROOT / "planning" / "tfl6_stand_to_au_review.csv"
    )
    remap = pd.read_csv(
        INSTANCE_ROOT / "planning" / "tfl6_first_growth_au_remap_audit.csv"
    )
    remap_lookup = remap.set_index("source_au_id")["canonical_curve_au_id"].to_dict()
    assignment_source["source_stratum_bin_id"] = assignment_source["au_id"].astype(str)
    assignment_source["au_id"] = (
        assignment_source["source_stratum_bin_id"]
        .map(remap_lookup)
        .fillna(assignment_source["source_stratum_bin_id"])
    )
    selected_au = pd.read_csv(
        INSTANCE_ROOT / "planning" / "tfl6_static_au_universe.csv"
    )
    selected_au_ids = set(
        selected_au.loc[
            selected_au["selected_top_90_stratum"].astype(bool), "au_id"
        ].astype(str)
    )
    unexpected_au_ids = sorted(
        set(assignment_source["au_id"].astype(str)) - selected_au_ids
    )
    if unexpected_au_ids:
        raise RuntimeError(
            "Canonicalized assignment includes labels outside the top-N AU universe: "
            + ", ".join(unexpected_au_ids[:20])
        )
    feature_ids = sorted(
        {
            int(value)
            for value in pd.to_numeric(assignment_source["feature_id"], errors="coerce")
            .dropna()
            .tolist()
        }
    )
    vdyp_ply = _upper_columns(
        pd.read_parquet(
            INSTANCE_ROOT
            / "data"
            / "input"
            / "tfl_6"
            / "vdyp7_input_poly_2025_tfl6.parquet"
        )
    )
    vdyp_lyr = _upper_columns(
        pd.read_parquet(
            INSTANCE_ROOT
            / "data"
            / "input"
            / "tfl_6"
            / "vdyp7_input_layer_2025_tfl6.parquet"
        )
    )
    available_ids = set(
        pd.to_numeric(vdyp_ply["FEATURE_ID"], errors="coerce").dropna().astype(int)
    )
    feature_ids = [
        feature_id for feature_id in feature_ids if feature_id in available_ids
    ]

    vdyp_yield_path = output_root / "vdyp_yield_timeseries.parquet"
    if vdyp_yield_path.exists():
        print(f"reuse {vdyp_yield_path.relative_to(INSTANCE_ROOT)}", flush=True)
        vdyp_yields = pd.read_parquet(vdyp_yield_path)
    else:
        chunk_size = 250
        yield_chunks: list[pd.DataFrame] = []
        run_log = output_root / "vdyp_runs.jsonl"
        stdout_log = output_root / "vdyp_stdout.log"
        stderr_log = output_root / "vdyp_stderr.log"
        for chunk_index, start in enumerate(
            range(0, len(feature_ids), chunk_size), start=1
        ):
            chunk_ids = feature_ids[start : start + chunk_size]
            print(f"VDYP chunk {chunk_index}: {len(chunk_ids)} feature ids", flush=True)
            vdyp_out = execute_vdyp_batch(
                feature_ids=chunk_ids,
                vdyp_ply=vdyp_ply,
                vdyp_lyr=vdyp_lyr,
                vdyp_binpath="VDYP7/VDYP7/VDYP7Console.exe",
                vdyp_params_infile="vdyp_params-landp",
                vdyp_io_dirname=vdyp_io.relative_to(REPO_ROOT).as_posix(),
                vdyp_log_path=run_log,
                vdyp_stdout_log_path=stdout_log,
                vdyp_stderr_log_path=stderr_log,
                phase="aflb",
                timeout=1200,
                run_id="tfl6_p3_4_aflb_vdyp_first_growth",
                base_context={
                    "instance": "tfl6",
                    "phase": "p3.4",
                    "chunk_index": chunk_index,
                    "chunk_size": chunk_size,
                },
            )
            output_ids = {
                int(feature_id)
                for feature_id in vdyp_out.keys()
                if str(feature_id).strip().lstrip("-").isdigit()
            }
            chunk_id_set = set(chunk_ids)
            if output_ids and len(output_ids & chunk_id_set) < max(
                1, len(output_ids) // 2
            ):
                remapped_vdyp_out = {
                    int(feature_id): table
                    for feature_id, table in zip(
                        chunk_ids, vdyp_out.values(), strict=False
                    )
                }
            else:
                remapped_vdyp_out = {
                    int(feature_id): table for feature_id, table in vdyp_out.items()
                }
            rows: list[dict[str, float | int]] = []
            for feature_id, table in remapped_vdyp_out.items():
                rows.extend(_vdyp_table_to_rows(int(feature_id), table))
            chunk_frame = pd.DataFrame(
                rows, columns=["FEATURE_ID", "PRJ_TOTAL_AGE", "PRJ_VOL_DWB", "PRJ_YEAR"]
            )
            chunk_path = output_root / f"vdyp_yields_chunk_{chunk_index:05d}.parquet"
            chunk_frame.to_parquet(chunk_path, index=False)
            yield_chunks.append(chunk_frame)

        vdyp_yields = (
            pd.concat(yield_chunks, ignore_index=True)
            if yield_chunks
            else pd.DataFrame(
                columns=["FEATURE_ID", "PRJ_TOTAL_AGE", "PRJ_VOL_DWB", "PRJ_YEAR"]
            )
        )
        vdyp_yields = vdyp_yields.sort_values(
            ["FEATURE_ID", "PRJ_TOTAL_AGE"], kind="stable"
        )
        vdyp_yields.to_parquet(vdyp_yield_path, index=False)
        vdyp_yields.to_csv(output_root / "vdyp_yield_timeseries.csv", index=False)

    assignment = assignment_source.rename(
        columns={
            "feature_id": "forest_cover_id",
            "area_ha": "shape_area_ha",
        }
    )[["forest_cover_id", "au_id", "shape_area_ha"]].copy()
    assignment["res_key"] = assignment["forest_cover_id"].astype(str)
    curves, diagnostics = build_mkrf_first_growth_curves(
        vdyp_yields=vdyp_yields,
        assignment=assignment,
        source_table=None,
    )
    curves.to_csv(output_root / "first_growth_au_curves.csv", index=False)
    diagnostics.to_csv(output_root / "first_growth_au_fit_diagnostics.csv", index=False)

    print(
        "complete "
        f"features={len(feature_ids)} yield_rows={len(vdyp_yields)} "
        f"curve_aus={curves['au_id'].nunique() if not curves.empty else 0} "
        f"diagnostic_aus={len(diagnostics)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
