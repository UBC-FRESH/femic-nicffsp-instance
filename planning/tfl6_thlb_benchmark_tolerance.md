# TFL 6 THLB Benchmark Tolerance Lock

## Purpose

This note records the P2.5 benchmark/tolerance decision for the first TFL 6
teaching-model THLB lane.

Governing issue: `#25`.

## Decision

The P2.4e final current-THLB smoke result is accepted for the base teaching
lane.

The accepted interpretation is:

- the official 2011 MP10 Table 4 current THLB remains the historical source
  benchmark: `107811 ha`;
- the scaled current-AOI benchmark remains an approximate validation target:
  `136487.728 ha`;
- the P2.4e reconstructed smoke result is `144203.485 ha`; and
- the `+7715.757 ha` / `+5.65%` final current-THLB gap is acceptable for this
  instance because the scaled target depends on an unverifiable assumption that
  the post-2011 extension area has the same mean THLB netdown rate as the
  pre-extension MP10 landbase.

This locks the base-lane THLB tolerance for teaching-model progression. It does
not claim that the extension-area scaling assumption is true, only that the
result is close enough to move from source-layer/THLB preparation into model
design and model-input work.

## Milestone Comparison

| Milestone | Scaled current-AOI benchmark ha | P2.4e smoke result ha | Delta ha | Delta percent |
| --- | ---: | ---: | ---: | ---: |
| Total landbase | `217042.719` | `217042.719` | `-0.000` | `-0.00%` |
| Total forested | `194991.692` | `196833.177` | `+1841.485` | `+0.94%` |
| Total productive forest | `186175.333` | `190515.340` | `+4340.007` | `+2.33%` |
| Total operable | `170428.940` | `174768.947` | `+4340.007` | `+2.55%` |
| Reduced landbase | `143686.151` | `151401.908` | `+7715.757` | `+5.37%` |
| Current THLB | `136487.728` | `144203.485` | `+7715.757` | `+5.65%` |

The long-term landbase row is not used for this P2.5 base-lane acceptance
decision because the P2.4e smoke lane does not execute the future-road
long-term adjustment. It remains a future scenario/reporting context row.

## Accepted Caveats

- The scaled current-AOI targets are approximate teaching validation targets,
  not legal/accounting lock values.
- The extension block almost certainly does not have exactly the same netdown
  proportions as the MP10 historical landbase.
- Spatially replacing aspatial fallback rows, especially operability,
  strategic RMZ/stand-level retention, draft OGMA, and cultural heritage proxy
  logic, remains valid future sensitivity or student challenge work.
- No additional THLB rerun is required before starting the next roadmap phase.

## Phase 2 Closeout Boundary

P2.5 closes the Phase 2 benchmark gate. The next roadmap work can move to Phase
3 model-design assumptions and then Phase 4 model-input generation once the
Phase 3 design contracts are accepted.
