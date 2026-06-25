# TFL 6 Recipe Adaptation Contract

## Purpose

This note classifies the TFL 6 MP10 THLB netdown backbone into reusable FEMIC
recipe patterns, TFL/general-FMU adaptation gaps, missing source-layer work,
aspatial fallback candidates, and reference-only benchmark rows.

Governing issue: `#7`.

This is a P1.7c planning contract. No recipe YAML is created here and no THLB
netdown execution is authorized.

## Classification Vocabulary

Use these classifications before drafting P1.7d recipe skeletons:

| Classification | Meaning | P1.7d implication |
| --- | --- | --- |
| `tsa29_carry_forward` | Existing TSA29 source-layer/netdown recipe concepts can guide this step directly. | Draft a TFL 6 skeleton using the established FEMIC pattern, with source paths left unresolved if needed. |
| `tfl_adaptation` | The step is conceptually executable, but TFL 6 needs a general-FMU or TFL-specific schema/rule adaptation. | Draft only if the needed schema/rule boundary can be expressed without pretending this is a TSA. |
| `missing_source_layer` | A spatial source is needed before a defensible executable recipe can run. | Record required source and candidate acquisition path; do not execute. |
| `aspatial_fallback_candidate` | A reviewed non-spatial or percent deduction is acceptable for teaching-tool validation if source geometry is unavailable. | Draft as a clearly marked fallback recipe or benchmark adjustment only. |
| `reference_target_only` | The row is a checkpoint, target, context row, or benchmark surface, not an executable deduction. | Include in reports/validation tables, not as a deduction recipe. |

## Global Contract Decisions

- Preserve MP10 Table 4 row order as the governing netdown order.
- Preserve MP10 source wording in planning notes; use FEMIC `GLB -> AFLB ->
  LHLB -> THLB` labels only as review metadata.
- Treat `planning/tfl6_adjusted_thlb_benchmarks.md` and
  `planning/tfl6_adjusted_thlb_benchmarks.json` as provisional validation
  targets for the current AOI, not as source data.
- Treat Instrument 101 as the working boundary-vintage explanation for the
  current-AOI scaling. The residual area mismatch remains unresolved and is not
  a blocker for this teaching instance.
- Do not execute netdown recipes until P1.7d skeletons are reviewed and an
  implementation issue explicitly accepts execution.

## Step Classification Matrix

| Step ID | MP10 row / action | Primary classification | Secondary tags | P1.7d skeleton guidance |
| --- | --- | --- | --- | --- |
| `tfl6_nd_000` | Total landbase | `reference_target_only` | `boundary_context`, `scaled_validation_target` | Use accepted P1.6 current AOI as the active geometry context; keep MP10 GLB as historical benchmark only. |
| `tfl6_nd_010` | Less non-forest | `tsa29_carry_forward` | `tfl_adaptation`, `attribute_rule_review` | Draft an attribute-exclusion skeleton against clipped R1/VRI fields, but leave class mapping reviewed/unlocked. |
| `tfl6_nd_020` | Less existing roads | `missing_source_layer` | `tfl_adaptation`, `buffer_overlay` | Draft a source requirement and optional buffer-rule placeholder; do not claim executable readiness until road line/polygon sources are chosen. |
| `tfl6_nd_030` | Total forested | `reference_target_only` | `checkpoint` | Report-only checkpoint after non-forest and existing-road exclusions. |
| `tfl6_nd_040` | Less non-productive forest | `tsa29_carry_forward` | `tfl_adaptation`, `attribute_rule_review` | Draft an attribute/productivity exclusion skeleton; map CP/MH/MH1/S7/S8/PG5-style classes only after field review. |
| `tfl6_nd_050` | Total productive forest | `reference_target_only` | `aflb_checkpoint`, `scaled_validation_target` | Use as AFLB-style benchmark/checkpoint, including scaled current-AOI target. |
| `tfl6_nd_060` | Less inoperable, including uneconomic | `missing_source_layer` | `tfl_adaptation`, `operability_schema` | Do not draft executable logic until an operability source or reviewed proxy is accepted; record classes `I`, `Ocm`, and `Ohm` as target semantics. |
| `tfl6_nd_070` | Total operable | `reference_target_only` | `lhlb_checkpoint`, `scaled_validation_target` | Use as LHLB-style benchmark/checkpoint, including scaled current-AOI target. |
| `tfl6_nd_080` | Riparian management | `tfl_adaptation` | `missing_source_layer`, `buffer_overlay`, `aspatial_fallback_candidate` | Reuse TSA29 buffer/overlay concepts, but TFL 6 needs hydrology/wetland/shoreline source resolution and MP10-specific retention rules. Fallback percent deduction may be acceptable for teaching validation. |
| `tfl6_nd_090` | Ungulate winter ranges | `tsa29_carry_forward` | `missing_source_layer`, `spatial_overlay` | Draft a public-layer overlay skeleton after resolving UWR order polygons and IDs for `U-1-010` and the small `U-1-011` overlap. |
| `tfl6_nd_100` | Established OGMAs | `tsa29_carry_forward` | `missing_source_layer`, `vintage_risk` | Draft an OGMA overlay skeleton, but flag current legal layer vintage as potentially different from MP10 established OGMAs. |
| `tfl6_nd_110` | Draft OGMAs | `aspatial_fallback_candidate` | `missing_source_layer`, `vintage_risk`, `historical_local_source` | Do not depend on current public legal OGMAs for 2011 draft geometry. Draft as historical/local-source placeholder or reviewed aspatial deduction. |
| `tfl6_nd_120` | Wildlife habitat areas | `tsa29_carry_forward` | `missing_source_layer`, `spatial_overlay` | Draft a WHA overlay skeleton after resolving public WHA polygons and listed WHA IDs. |
| `tfl6_nd_130` | Recreation sites and trails | `tfl_adaptation` | `missing_source_layer`, `buffer_overlay` | Draft a recreation feature plus 10 m buffer placeholder only after source-layer decision. |
| `tfl6_nd_140` | Deciduous-leading forest | `tsa29_carry_forward` | `attribute_rule_review` | Draft an inventory attribute exclusion skeleton using R1/VDYP leading-species fields after reviewing the deciduous-leading definition. |
| `tfl6_nd_150` | Cultural heritage resources | `aspatial_fallback_candidate` | `sensitive_data`, `proxy_overlay` | Use reviewed proxy/aspatial deduction for teaching if TUS/CMT geometry is unavailable; do not represent sensitive local data as public source. |
| `tfl6_nd_160` | Total operable reductions | `reference_target_only` | `checkpoint`, `rounding_note` | Report-only check row; preserve the one-hectare rounding discrepancy noted in MP10 Table 4. |
| `tfl6_nd_170` | Reduced landbase | `reference_target_only` | `checkpoint` | Report-only pre-stand-level-retention checkpoint. |
| `tfl6_nd_180` | Less allowance for stand-level retention | `accepted_aspatial_fallback` | `tfl_adaptation`, `percent_by_stratum`, `teaching_base_case` | Implement the base teaching lane as an aspatial MP10 Table 16 deduction: `5686 ha` historical or `7198.423 ha` scaled current-AOI validation target. Strategic Resource Management Zone vector attribution is deferred to a later enhancement/sensitivity lane. |
| `tfl6_nd_190` | Current THLB | `reference_target_only` | `thlb_checkpoint`, `scaled_validation_target` | Use as final current-THLB validation checkpoint, including the scaled target; not an executable deduction. |
| `tfl6_nd_200` | Less future roads | `tfl_adaptation` | `context_row`, `aspatial_fallback_candidate`, `future_model_time` | Keep out of current THLB reconstruction unless explicitly modelling long-term landbase; draft only as context/future-road allowance. |
| `tfl6_nd_210` | Long-term landbase | `reference_target_only` | `long_term_checkpoint`, `scaled_validation_target` | Report-only long-term benchmark after future roads. |

## Source-Layer Priority

P1.7d should not try to solve all sources at once. Use this priority order:

| Priority | Source surface | Why it matters |
| --- | --- | --- |
| 1 | VRI/R1 attribute mapping for non-forest, non-productive, and deciduous-leading stands | These are the most direct carry-forward candidates and use accepted P1.6 inputs. |
| 2 | Operability source or reviewed proxy | This defines the productive-to-operable checkpoint and has a large area effect. |
| 3 | Roads and future-road treatment split | Existing roads affect early landbase; future roads are long-term/model-time context. |
| 4 | Hydrology/wetland/shoreline source and MP10 riparian RMA/RRZ/RMZ rules | Riparian is the largest LHLB-to-THLB reduction and needs TFL-specific operational buffer/retention rules. |
| 5 | UWR, WHA, and established OGMA public layers | These are likely public spatial overlays but need vintage/ID checks. |
| 6 | Draft OGMAs, cultural heritage, and stand-level retention | These likely need historical/local sources or reviewed fallback treatment. |

## Benchmark and Boundary Treatment

Use these benchmark surfaces in P1.7d:

| Surface | Treatment |
| --- | --- |
| MP10 Table 4 values in `planning/tfl6_thlb_netdown_steps.md` | Historical source benchmark. Keep visible in tables and validation reports. |
| Instrument 101 evidence in `planning/tfl6_instrument_boundary_reconciliation.md` | Boundary-vintage context explaining current-AOI scaling. Not recipe input. |
| Adjusted values in `planning/tfl6_adjusted_thlb_benchmarks.md` and `.json` | Approximate current-AOI validation targets. Not final lock values. |
| P1.6 input manifest | Active current-AOI input surface for future executable recipes. |

## P1.7d Handoff

P1.7d drafted the non-executable skeleton planning tables in
`planning/tfl6_recipe_skeletons.md` using this order:

1. Source-layer candidate skeleton for accepted current-AOI inventory fields.
2. THLB netdown skeleton table preserving MP10 order, with unresolved source
   placeholders for roads, operability, hydrology, and historical reserves.
3. Validation-target table carrying both MP10 historical values and scaled
   current-AOI targets.
4. Explicit blocked-execution notes for all missing-source and fallback rows.

P1.7d did not run recipes, materialize new source layers, or start Patchworks
runtime-package work.
