"""Build P14.7 no-heli track variant from harvest-system candidate tracks."""

from __future__ import annotations

import csv
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "tfl6_patchworks_model_mp11_harvest_system_candidate"
TRACKS_ROOT = MODEL_ROOT / "tracks"
NO_HELI_ROOT = MODEL_ROOT / "tracks_no_heli"

OUT_CSV = ROOT / "planning" / "tfl6_mp11_phase14_no_heli_tracks.csv"
OUT_JSON = ROOT / "planning" / "tfl6_mp11_phase14_no_heli_tracks.json"
OUT_MD = ROOT / "planning" / "tfl6_mp11_phase14_no_heli_tracks.md"


def _repo(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _copy_tracks() -> None:
    if not TRACKS_ROOT.exists():
        raise FileNotFoundError(f"Track root missing: {_repo(TRACKS_ROOT)}")
    if NO_HELI_ROOT.exists():
        shutil.rmtree(NO_HELI_ROOT)
    shutil.copytree(TRACKS_ROOT, NO_HELI_ROOT)


def _filter_treatment_csv(path: Path, *, treatment_col: str = "TREATMENT") -> dict[str, Any]:
    frame = pd.read_csv(path)
    before = int(len(frame))
    removed = 0
    if treatment_col in frame.columns:
        keep = frame[treatment_col].astype(str) != "CC_HELI"
        removed = int((~keep).sum())
        frame = frame[keep].copy()
        frame.to_csv(path, index=False)
    return {"path": _repo(path), "rows_before": before, "rows_after": int(len(frame)), "removed": removed}


def _filter_account_csv(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(path)
    before = int(len(frame))
    keep = ~frame.astype(str).apply(
        lambda series: series.str.contains("CC_HELI", regex=False)
    ).any(axis=1)
    removed = int((~keep).sum())
    frame = frame[keep].copy()
    frame.to_csv(path, index=False)
    return {"path": _repo(path), "rows_before": before, "rows_after": int(len(frame)), "removed": removed}


def _inspect() -> dict[str, Any]:
    treatments = pd.read_csv(NO_HELI_ROOT / "treatments.csv")
    products = pd.read_csv(NO_HELI_ROOT / "products.csv")
    accounts = pd.read_csv(NO_HELI_ROOT / "accounts.csv")
    protoaccounts = pd.read_csv(NO_HELI_ROOT / "protoaccounts.csv")
    return {
        "treatments_rows": int(len(treatments)),
        "products_rows": int(len(products)),
        "accounts_rows": int(len(accounts)),
        "protoaccounts_rows": int(len(protoaccounts)),
        "accounts_proto_equal": bool(accounts.equals(protoaccounts)),
        "cc_heli_treatment_rows": int((treatments["TREATMENT"].astype(str) == "CC_HELI").sum()),
        "cc_heli_product_rows": int((products["TREATMENT"].astype(str) == "CC_HELI").sum()),
        "cc_heli_account_rows": int(
            accounts.astype(str)
            .apply(lambda series: series.str.contains("CC_HELI", regex=False))
            .any(axis=1)
            .sum()
        ),
        "cc_heli_protoaccount_rows": int(
            protoaccounts.astype(str)
            .apply(lambda series: series.str.contains("CC_HELI", regex=False))
            .any(axis=1)
            .sum()
        ),
        "aggregate_cc_product_rows": int(
            products.astype(str)
            .apply(
                lambda series: series.str.contains(
                    "product.HarvestedVolume.managed.Total.CC", regex=False
                )
            )
            .any(axis=1)
            .sum()
        ),
    }


def _write_outputs(payload: dict[str, Any]) -> None:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        for key, value in payload["summary"].items():
            writer.writerow({"metric": key, "value": value})
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    summary = payload["summary"]
    lines = [
        "# TFL 6 MP11 Phase 14 No-Heli Tracks",
        "",
        "This P14.7 helper builds a generated no-heli track variant by copying the "
        "P14.6 harvest-system Matrix Builder tracks and removing `CC_HELI` "
        "treatment/product rows. It does not change the all-system tracks.",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- The no-heli variant is a smoke-test track variant, not a new source model.",
            "- The all-system tracks remain under `tracks/`.",
            "- The no-heli tracks are generated under ignored `tracks_no_heli/`.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def build() -> dict[str, Any]:
    _copy_tracks()
    treatment_filter = _filter_treatment_csv(NO_HELI_ROOT / "treatments.csv")
    product_filter = _filter_treatment_csv(NO_HELI_ROOT / "products.csv")
    accounts_filter = _filter_account_csv(NO_HELI_ROOT / "accounts.csv")
    protoaccounts_filter = _filter_account_csv(NO_HELI_ROOT / "protoaccounts.csv")
    inspection = _inspect()
    summary = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "source_tracks_root": _repo(TRACKS_ROOT),
        "no_heli_tracks_root": _repo(NO_HELI_ROOT),
        "treatment_rows_removed": treatment_filter["removed"],
        "product_rows_removed": product_filter["removed"],
        "account_rows_removed": accounts_filter["removed"],
        "protoaccount_rows_removed": protoaccounts_filter["removed"],
        **inspection,
    }
    payload = {
        "summary": summary,
        "filters": {
            "treatments": treatment_filter,
            "products": product_filter,
            "accounts": accounts_filter,
            "protoaccounts": protoaccounts_filter,
        },
    }
    _write_outputs(payload)
    return payload


def main() -> None:
    payload = build()
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
