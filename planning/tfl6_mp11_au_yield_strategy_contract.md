# TFL 6 MP11 AU/Yield And Managed-Stand Strategy Contract

## Purpose

This P8.3 contract decides how MP11 analysis-unit, site-productivity,
growth-and-yield, managed-stand, utilization, OAF/VRAF, and non-recoverable
loss assumptions should be represented before any curve regeneration. It keeps
the Phase 5 runtime intact while defining the model-contract boundary for a
future MP11-aligned yield rebuild.

This contract does not regenerate VDYP curves, run BatchTIPSY, modify the
model-input bundle, regenerate ForestModel XML, or promote MP11 assumptions to
accepted model inputs.

## Evidence Inputs

Primary P8.3 evidence inputs:

- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.md`;
- `planning/tfl6_mp11_inventory_yield_operability_crosswalk.csv`;
- `planning/tfl6_mp11_baseline_and_promotion_contract.md`;
- `planning/tfl6_mp11_source_layer_thlb_rebuild_contract.md`;
- `planning/tfl6_au_yield_curve_contract.md`;
- `planning/tfl6_tipsy_parameter_crosswalk.md`;
- `planning/tfl6_tipsy_parameter_crosswalk.csv`.

Relevant P6.4 reviewed rows:

- `analysis_unit_definition`;
- `growth_yield_software`;
- `site_index_sibec_tem_lefi`;
- `managed_stand_inputs_genetic_gain_fertilization_spacing`;
- `oaf_vraf_retention_yield_adjustment`;
- `utilization_standards`;
- `non_recoverable_losses`.

Every row remains `reviewed_evidence`, `phase6_assumption_comparison_only`,
and `not_model_input`.

## Strategy Decision

The future MP11 rebuild should preserve FEMIC's static canonical AU identity
and add MP11 AU-era, site-series, treatment, managed-stand, and productivity
fields as crosswalk and curve-parameter attributes.

MP11 AU identity should not fully replace the Phase 5 static AU architecture in
one step because MP11's published AU description mixes stand-family,
silvicultural-treatment, era, site-series, and managed-stand assumptions. Those
dimensions are important, but several are better represented as curve-lane,
treatment-eligibility, or reporting attributes than as immutable Patchworks AU
keys.

Canonical AU identity remains a stable stand-family key. MP11 attributes become
reviewed modifiers that can drive curve selection, parameter-library rows,
report groups, and QA comparisons.

## Accepted Canonical AU Boundary

Retain the Phase 5 AU identity principle:

- BEC/subzone/variant/phase grouping;
- ordered leading-species combination;
- selected static stand-family universe with explicit raw-to-canonical mapping
  if aggregation is needed;
- public SI/productivity class where supportable; and
- no age-at-time-zero, THLB status, treatment eligibility, harvest system,
  operability, retention, or scenario membership in the canonical AU key.

MP11 crosswalk fields should be added alongside canonical AU identity:

- MP11 AU era class: existing natural, existing managed, recent managed,
  future managed, or other reviewed class;
- BEC variant and site-series/source-productivity evidence where public-safe;
- leading species and managed-stand treatment markers;
- stand origin and curve-provenance class;
- site-index source class;
- managed-stand parameter row key;
- utilization rule key;
- OAF/VRAF rule key; and
- NRL/disturbance-loss rule key if accepted later.

This avoids changing AU identity when a stand moves between scenarios or when
treatment eligibility changes.

## Public And Non-Public Dependency Boundary

| Dependency | Base public-data treatment | Unavailable or sensitivity treatment |
| --- | --- | --- |
| Public VRI/R1/VDYP inventory | Refresh and profile as public base inventory where source version supports it. | Do not infer WFP LiDAR/ITI attributes from summaries. |
| VDYP natural curves | Regenerate only in a later curve phase using reviewed public inventory and visible diagnostics. | Document software-version mismatch where exact VDYP 7.33b reproduction is unavailable. |
| SIBEC/TEM site productivity | Use only if public source, schema, and site-series mapping are reviewed. | LEFI/LiDAR-derived SI remains sensitivity or unavailable. |
| RESULTS-derived existing managed SI | Use if public-safe linkage and attribute semantics are reviewed. | Do not invent stand-level managed SI from aggregate MP11 text. |
| BatchTIPSY/TIPSY managed curves | Rebuild only from reviewed parameter library and reproducible runner environment. | Document any TIPSY 4.6 version gap or local executable dependency. |
| MP11 ITI/LEFI/LiDAR heights | Not a base public-data input unless source is supplied and public-safe. | Represent as `unavailable_non_public` or explicit sensitivity. |

## Managed-Yield Parameter Library Requirements

A later curve-rebuild issue must extract MP11 managed-yield parameters into a
reviewed library before running BatchTIPSY. The library should include, at
minimum:

- source page, table, row, and extraction method;
- MP11 AU era or managed-stand class;
- BEC variant and site-series where available;
- leading species and species-percent assumptions;
- site-index value and site-index source;
- planting density: `900`, `1000`, `1200` sph, or reviewed exception;
- regeneration delay;
- genetic-gain assumption;
- fertilization marker and treatment timing where published;
- spacing marker and target density where published;
- OAF1/OAF2 rule key;
- VRAF rule key;
- utilization rule key;
- curve lane: existing managed, recent managed, future managed, natural, or
  sensitivity;
- public/private dependency flags; and
- reviewer and validation status.

MP11 Tables 54-57 are the first extraction target for managed-yield parameters.
Tables 47-60 and surrounding text should be treated as the broader extraction
scope if the first pass shows that managed-yield assumptions are distributed
across multiple tables and narrative sections.

## Yield-Adjustment Surfaces

The future MP11 curve phase should separate these parameter surfaces:

| Surface | P8.3 decision |
| --- | --- |
| OAF1/OAF2 | Create explicit rule keys. MP11's standard OAF1 `15%` and OAF2 `5%` may become implementation candidates after extraction and review. |
| VRAF | Create a separate VRAF rule surface for recent and future managed stands; do not hide it inside generic OAF until retention-zone logic is reviewed. |
| Utilization | Create age/stand-class utilization rule keys for `17.5 cm` mature DBH and `12.5 cm` immature/future managed DBH, with `30 cm` stump height, `10 cm` top DIB, and `50%` firmwood standard as reviewed parameters before curve generation. |
| Genetic gain | Store as species/era/stocking parameter rows, not as prose. |
| Fertilization and spacing | Store as treatment markers and curve-lane parameters, not as canonical AU identity. |
| NRL | Keep separate from curves until reviewed. Test whether it belongs as yield reduction, account/reporting adjustment, harvest-flow comparison factor, or scenario sensitivity. |

## Natural Curve Strategy

Natural and existing unmanaged curves should be regenerated only in a later
implementation phase after:

- public inventory version and stand universe are fixed;
- canonical AU/raw-to-canonical mapping is accepted;
- VDYP source and runner assumptions are documented;
- sparse-support diagnostics are defined; and
- MP11 comparison plots are scoped.

The current Phase 5 `smoothed_bin_pchip` first-growth method remains the
default FEMIC curve-construction method unless a later issue explicitly accepts
an MP11-specific override.

Natural stands older than `62` years are treated in MP11 as polygon-by-polygon
projection evidence. In FEMIC, that should be represented as a natural-curve
projection and QA rule, not as a reason to make age a canonical AU dimension.

## Managed Curve Strategy

Managed curves should be rebuilt only after the MP11 parameter library is
reviewed. The first curve-rebuild issue must:

- preserve separate curve lanes for existing managed, recent managed, and
  future managed where MP11 parameters differ;
- crosswalk canonical FEMIC AUs to MP11 parameter rows with confidence flags;
- keep MP10-derived parameter rows as legacy fallback evidence only;
- record every low-confidence or fallback row before curve generation;
- generate overlays comparing Phase 5, MP10-derived, and MP11-derived managed
  curves where possible; and
- fail loudly if a managed curve would otherwise be fabricated from an
  unreviewed private-data dependency.

## Acceptance Checks For Later Curve Rebuild

A later MP11 AU/yield implementation phase must define and pass these checks:

- every canonical AU has a stable ID independent of age, treatment,
  operability, and scenario membership;
- every curve has source, software, parameter-row, and QA provenance;
- every MP11 managed-yield table row used by a curve is in the reviewed
  parameter library;
- every public/private dependency is flagged;
- every unsupported AU/curve mapping is reported;
- natural and managed curve families have comparison plots;
- utilization, OAF/VRAF, and NRL surfaces are separately inspectable; and
- no private WFP curve, unpublished table, or proprietary LiDAR/ITI attribute
  is embedded in public model inputs.

## Handoff To P8.4 And P8.5

This P8.3 contract leaves these topics to later Phase 8 tasks:

- physical/economic operability, helicopter thresholds, harvest-system
  classifier, `95%` CMAI, and `350 m3/ha` MHA logic belong to P8.4;
- harvest-flow, AAC recommendation, sensitivity scenario interpretation, and
  KPI/reporting targets belong to P8.5;
- Patchworks objective weights, spatial harvest rules, VQO, ECA, adjacency,
  green-up, and block-size behavior belong to P8.4/P8.5 or later runtime
  rebuild phases.

## P8.3 Acceptance

P8.3 is complete when:

- this contract is tracked in `planning/`;
- `ROADMAP.md` marks P8.3 complete;
- `CHANGE_LOG.md` records the contract;
- issue `#61` is closed with validation evidence;
- no curve outputs are generated or tracked; and
- no MP11 AU/yield value has been promoted to model-input status.
