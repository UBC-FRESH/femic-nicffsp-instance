# TFL 6 MP11 Phase 9 Public-Data THLB Diagnostic Rebuild

## Purpose

This P9.5 output records a compact diagnostic public-data THLB rebuild
from the P9.4 ordered scaffold. It writes summary tables only and does
not publish geospatial overlay intermediates or accepted model inputs.

## Files

- `planning/tfl6_mp11_phase9_thlb_rebuild_summary.md`
- `planning/tfl6_mp11_phase9_thlb_rebuild_summary.csv`
- `planning/tfl6_mp11_phase9_thlb_rebuild_summary.json`

## Summary

- Diagnostic current THLB: `24,762.768 ha`
- MP11 current THLB comparison target: `120,099.000 ha`
- Delta vs MP11 target: `-95,336.232 ha`
- Model-input status: `not_model_input`

## Ordered Results

| Order | Step | Rule | Gross ha | Ordered deduction ha | Cumulative ha | MP11 target ha | Delta ha | Residual class |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | `mp11_nd_000` Total land base / accounting universe | initial R1 accounting geometry | 217,042.719 |  | 217,042.719 | 217,197.000 | -154.281 | `public_match` |
| 10 | `mp11_nd_010` Non-forest and non-treed review candidates | bclcs_level_1 in {'N', 'U'} | 10,693.446 | 10,693.446 | 206,349.273 |  |  | `public_proxy_residual` |
| 20 | `mp11_nd_020` Existing roads | DRA all-road 5 m buffer full-stand intersection diagnostic | 4,339.761 | 94,381.292 | 111,967.981 |  |  | `public_proxy_residual` |
| 30 | `mp11_nd_030` Total forested checkpoint | checkpoint after non-forest and road diagnostics |  |  | 111,967.981 | 196,233.000 | -84,265.019 | `checkpoint_delta` |
| 40 | `mp11_nd_040` Non-productive and low-site candidates | explicit non-productive signal or site_index < 5 | 6,047.408 | 6,047.408 | 105,920.573 |  |  | `public_proxy_residual` |
| 50 | `mp11_nd_050` Productive forest / AFLB checkpoint | checkpoint after productivity diagnostics |  |  | 105,920.573 | 187,425.000 | -81,504.427 | `checkpoint_delta` |
| 60 | `mp11_nd_060` Legal/proposed OGMAs, WHAs, UWRs, and conservation candidates | current legal/non-legal OGMA plus approved WHA/UWR diagnostic union | 21,440.029 | 23,851.664 | 82,068.909 |  |  | `public_proxy_residual` |
| 70 | `mp11_nd_070` Additional values: research, PSPs, big trees, and karst | no public-safe geometry available |  | 0.000 | 82,068.909 |  |  | `unavailable_non_public` |
| 80 | `mp11_nd_080` Physical/economic operability proxy | public VRI low-height, low-volume, or hembal-height3 proxy | 39,516.610 | 39,516.610 | 42,552.299 | 156,305.000 | -113,752.701 | `public_proxy_residual` |
| 90 | `mp11_nd_090` Riparian management | FWA streams/lakes/wetlands 10 m buffer full-stand intersection diagnostic | 14,834.669 | 17,789.531 | 24,762.768 |  |  | `public_proxy_residual` |
| 100 | `mp11_nd_100` Terrain stability and LiDAR 90 percent slope | no public DEM/slope derivative available |  | 0.000 | 24,762.768 |  |  | `deferred_public_proxy` |
| 110 | `mp11_nd_110` Existing/future WTRAs and stand-level retention | no aspatial WTRA/retention deduction applied |  | 0.000 | 24,762.768 |  |  | `deferred_policy` |
| 120 | `mp11_nd_120` Current THLB checkpoint | current THLB diagnostic checkpoint |  |  | 24,762.768 | 120,099.000 | -95,336.232 | `checkpoint_delta` |

## Interpretation

- This is a diagnostic public-data rebuild, not an accepted replacement
  THLB surface.
- The run uses conservative public inventory candidates, full-stand
  intersection diagnostics for simple DRA road and FWA hydrology
  buffers, current public legal/reserve layers, and a high-uncertainty
  VRI operability proxy.
- Shoreline, DEM/slope, WFP LBB, WFP ITI/LEFI, proposed/local reserves,
  and WTRA/retention policy gaps remain unresolved or deferred.
- The MP11 current THLB target remains a comparison target only; this
  run does not force-fit to `120,099 ha`.

## Use Boundary

Rows in this summary are `not_model_input`. Later phases must explicitly
promote any accepted source-layer/THLB outputs through the Phase 8
evidence-promotion contract before model-input generation.
