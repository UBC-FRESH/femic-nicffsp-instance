# TFL 6 Adjusted THLB Benchmarks

## Purpose

This note defines provisional current-AOI THLB validation targets by scaling
the 2011 Management Plan 10 Table 4 netdown values to the accepted P1.6
FADM-derived TFL 6 AOI.

Governing issue: `#7`.

These are approximate validation benchmarks only. They are not accepted
reconstructed THLB outputs and they do not replace spatial recipe execution.

## Scaling Contract

| Quantity | Area ha |
| --- | ---: |
| MP10 Table 4 historical GLB | `171,441` |
| P1.6 current FADM-derived TFL 6 AOI | `217,042.718950` |
| Scale factor | `1.265990742879474571426904883` |
| Instrument 101 labelled additions | `44,612 + 2,096 = 46,708` |

Instrument 101 explains most or all of the current-vs-MP10 AOI delta, so the
working benchmark strategy is to scale MP10 Table 4 to the accepted current
FADM AOI. The scale factor uses the accepted current AOI area rather than the
rounded Instrument 101 map-label addition total.

This is intentionally good-enough benchmark logic for a teaching and learning
instance. The remaining area mismatch may reflect smaller net-outs, parcel
cleanup, boundary-vintage differences, or other post-MP10 tenure changes. A
possible K3Z/community-forest carve-out is noted as an unverified candidate,
not as an accepted fact.

## Scaled Benchmarks

| Step ID | MP10 row / action | FEMIC stage | MP10 reduction ha | MP10 cumulative ha | Scaled reduction ha | Scaled cumulative ha |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| tfl6_nd_000 | Total landbase | reference_target / GLB | 0 | 171441 | 0.000 | 217042.719 |
| tfl6_nd_010 | Less non-forest | glb_to_aflb | 13483 | 157958 | 17069.353 | 199973.366 |
| tfl6_nd_020 | Less existing roads | glb_to_aflb | 3935 | 154023 | 4981.674 | 194991.692 |
| tfl6_nd_030 | Total forested | reference_target | 0 | 154023 | 0.000 | 194991.692 |
| tfl6_nd_040 | Less non-productive forest | glb_to_aflb | 6964 | 147059 | 8816.360 | 186175.333 |
| tfl6_nd_050 | Total productive forest | reference_target / AFLB | 0 | 147059 | 0.000 | 186175.333 |
| tfl6_nd_060 | Less inoperable, including uneconomic | aflb_to_lhlb | 12438 | 134621 | 15746.393 | 170428.940 |
| tfl6_nd_070 | Total operable | reference_target / LHLB | 0 | 134621 | 0.000 | 170428.940 |
| tfl6_nd_080 | Riparian management | lhlb_to_thlb | 10632 | 123989 | 13460.014 | 156968.926 |
| tfl6_nd_090 | Ungulate winter ranges | lhlb_to_thlb | 1313 | 122676 | 1662.246 | 155306.680 |
| tfl6_nd_100 | Established OGMAs | lhlb_to_thlb | 3750 | 118926 | 4747.465 | 150559.215 |
| tfl6_nd_110 | Draft OGMAs | lhlb_to_thlb | 3469 | 115457 | 4391.722 | 146167.493 |
| tfl6_nd_120 | Wildlife habitat areas | lhlb_to_thlb | 3 | 115454 | 3.798 | 146163.695 |
| tfl6_nd_130 | Recreation sites and trails | lhlb_to_thlb | 50 | 115404 | 63.300 | 146100.396 |
| tfl6_nd_140 | Deciduous-leading forest | lhlb_to_thlb | 1774 | 113630 | 2245.868 | 143854.528 |
| tfl6_nd_150 | Cultural heritage resources | lhlb_to_thlb | 132 | 113498 | 167.111 | 143687.417 |
| tfl6_nd_160 | Total operable reductions | reference_target | 21124 | 113497 | 26742.788 | 143686.151 |
| tfl6_nd_170 | Reduced landbase | reference_target | 0 | 113497 | 0.000 | 143686.151 |
| tfl6_nd_180 | Less allowance for stand-level retention | lhlb_to_thlb | 5686 | 107811 | 7198.423 | 136487.728 |
| tfl6_nd_190 | Current THLB | reference_target / THLB | 0 | 107811 | 0.000 | 136487.728 |
| tfl6_nd_200 | Less future roads | context / long_term_adjustment | 1491 | 106319 | 1887.592 | 134598.870 |
| tfl6_nd_210 | Long-term landbase | reference_target | 0 | 106319 | 0.000 | 134598.870 |

## Working Targets

- `Total productive forest`: `186175.333 ha`
- `Total operable`: `170428.940 ha`
- `Current THLB`: `136487.728 ha`
- `Long-term landbase`: `134598.870 ha`

## Caveats

- Uniform scaling assumes the 2015 addition areas have similar netdown
  proportions to the 2011 MP10 landbase.
- The targets are suitable for early validation tolerance bands, not for final
  accounting lock values.
- Current-AOI spatial recipe outputs should replace these scaled targets once
  source layers and recipe skeletons are reviewed.
- Keep the historical MP10 Table 4 values visible alongside these adjusted
  targets in reports.
- Do not use these scaled values as final lock values for legal/accounting
  reconciliation.

## P2.5 Tolerance Lock

P2.5 accepted the P2.4e current-THLB smoke result as close enough for the base
teaching lane:

- scaled current-AOI current-THLB benchmark: `136487.728 ha`;
- P2.4e reconstructed current-THLB result: `144203.485 ha`;
- difference: `+7715.757 ha`, or `+5.65%` relative to the scaled benchmark.

The accepted rationale is that the scaled benchmark depends on an unverifiable
assumption that the post-2011 extension area has the same mean THLB netdown rate
as the pre-extension MP10 landbase. That assumption is reasonable for a
teaching approximation but almost certainly not exactly true.

The detailed P2.5 lock is recorded in
`planning/tfl6_thlb_benchmark_tolerance.md`.
