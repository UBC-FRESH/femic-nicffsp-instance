# TFL 6 MP11 Land Base And THLB Comparison Crosswalk

## Purpose

This P6.3 note normalizes the highest-priority MP11 land-base and THLB
values against the accepted Phase 5 benchmark and model-input-bundle
surfaces. It is comparison evidence only; it does not change model
inputs.

## Files

- `planning/tfl6_mp11_land_base_crosswalk.md`
- `planning/tfl6_mp11_land_base_crosswalk.csv`
- `planning/tfl6_mp11_land_base_crosswalk.json`

## Status

- Rows: `8`
- Review status: `reviewed_evidence`
- Downstream use: `phase6_land_base_comparison_only`
- Model-input status: `not_model_input`

## Comparison Table

| Metric | MP11 ha | Phase 5 reference | Phase 5 ha | Delta ha | Delta % |
| --- | ---: | --- | ---: | ---: | ---: |
| Total TFL area / total land base | 217,197.000 | P1.6 current FADM-derived TFL 6 AOI | 217,042.719 | 154.281 | 0.07% |
| Total forested | 196,233.000 | P2.4e smoke total forested | 196,833.177 | -600.177 | -0.30% |
| Productive forest / PFLB / AFLB-style checkpoint | 187,425.000 | Phase 5 accepted AFLB resultant-fragment area | 191,168.597 | -3,743.597 | -1.96% |
| Total operable | 156,305.000 | P2.4e smoke total operable | 174,768.947 | -18,463.947 | -10.56% |
| Current THLB | 120,099.000 | Phase 5 accepted weighted THLB area | 139,995.798 | -19,896.798 | -14.21% |
| NCLB / productive forest not available for harvesting | 67,326.000 | Phase 5 accepted NTHLB area | 51,172.799 | 16,153.201 | 31.57% |
| Long-term land base after future roads | 118,672.000 | Scaled MP10 long-term landbase benchmark | 134,598.870 | -15,926.870 | -11.83% |
| Current AAC-supporting THLB from previous MPs | 133,665.000 | Scaled MP10 current-THLB benchmark | 136,487.728 | -2,822.728 | -2.07% |

## Key Findings

- MP11 total land base is essentially aligned with the Phase 5 current
  FADM-derived AOI after rounding.
- MP11 productive forest and current THLB are lower than the accepted
  Phase 5 AFLB/THLB model-input surfaces.
- MP11 current THLB is `120,099 ha`, compared with the Phase 5 accepted
  weighted THLB of `139,995.798 ha`.
- MP11 reports the previous-MP aggregated current AAC-supporting THLB as
  `133,665 ha`, close to the earlier scaled MP10 benchmark of
  `136,487.728 ha`.
- The land-base delta is large enough that MP11-aligned implementation
  should plan a reviewed THLB/source-layer overhaul rather than treating
  the Phase 5 teaching THLB as already MP11-aligned.

## Use Boundary

Rows in this crosswalk are reviewed Phase 6 comparison evidence. They
are not accepted model inputs and should not be copied into bundle tables
without a later implementation issue, PR, and maintainer review.
