# TFL 6 MP11 Phase 14 Harvest-System Operability Plan

## Purpose

Phase 14 integrates MP11 harvest-system operability into the TFL 6 MP11
candidate runtime. The immediate goal is to replace the deferred
`unassigned_review_required` harvest-system placeholder with public-proxy
ground, cable, and heli assignments that can be exposed in model-input tables,
ForestModel XML, Matrix Builder tracks, runtime reports, and all-system/no-heli
scenario smoke tests.

This phase starts after Phase 13 selected `supplement_phase5`. Phase 5 remains
the accepted public teaching/runtime baseline. Phase 14 upgrades the MP11
candidate supplement; it does not replace Phase 5 by itself.

## Issue Tree

Parent issue:

- `#138`: Phase 14: integrate MP11 harvest-system operability into TFL6
  candidate runtime

Child issues:

- `#139`: P14.1: launch MP11 harvest-system operability execution plan
- `#140`: P14.2: mine MP11 and public-source evidence for harvest-system
  criteria
- `#141`: P14.3: build public proxy metrics for ground, cable, and heli
  assignment
- `#142`: P14.4: classify MP11 candidate stands by harvest system and QA
  against MP11 targets
- `#143`: P14.5: rebuild MP11 model-input tables and ForestModel XML with split
  CC lanes
- `#144`: P14.6: run Matrix Builder and assemble harvest-system candidate
  runtime
- `#145`: P14.7: smoke-test all-system and no-heli harvest scenarios
- `#146`: P14.8: document Phase 14 caveats, comparison results, and closeout
  status

## MP11 Evidence Basis

The MP11 package does not publish WFP's Land Base Blocking (LBB)
physical-operability GIS layer, and no queryable public LBB harvest-system
overlay has been identified. Phase 14 must therefore build public proxy
assignments and label them as such. The implementation must not claim WFP LBB
equivalence.

High-signal MP11 anchors:

- PDF page 257 / Information Package page 11: the base case uses conventional
  ground/cable and non-conventional helicopter harvesting methods, with harvest
  methods based on a spatially delineated physical-operability dataset from
  WFP's LBB process.
- PDF pages 265-267 / Information Package pages 19-21: LBB uses LiDAR bare
  earth hillshade, canopy height model, slope, streams, professional block and
  road planning, and post-harvest updates to assign harvest systems.
- PDF pages 297-298 / Information Package pages 51-52: physical operability
  classes are conventional, non-conventional, and inoperable; MP11 Table 20
  reports THLB area split as 57.3% ground, 39.6% cable, and 3.1%
  non-conventional.
- PDF pages 311-312 / Information Package pages 65-66: helicopter economic
  operability uses age, flight distance, minimum volume, and Cw+Fd+Yc component
  thresholds. Stands older than 80 years require 350 m3/ha and 15% Cw+Fd+Yc at
  0-499 m flight distance, 370 m3/ha and 25% at 500-999 m, and 400 m3/ha and
  30% at 1000 m or more.
- PDF page 400 / Information Package page 154: MP11 replaces older
  harvest-system DBH minimums with 95% CMAI plus a 350 m3/ha minimum volume
  rule, partly because ground and cable systems are often used together in the
  same operating area.
- PDF page 405 / Information Package page 159: MP11 Table 73 reports current
  THLB by harvest system: 68,845 ha and 19,216,294 m3 ground, 47,524 ha and
  14,563,331 m3 cable, and 3,730 ha and 2,223,221 m3 non-conventional.

## Implementation Boundary

P14.1 is planning and issue setup only. It must not generate model-input
tables, ForestModel XML, Matrix Builder outputs, Patchworks runtime artifacts,
or scenario outputs.

Later Phase 14 implementation should proceed in this order:

1. Mine and summarize MP11, historical MP9/MP10, and public-source evidence for
   harvest-system criteria.
2. Build public proxy metrics from accepted candidate stand tables, P9D public
   CDED slope statistics, inventory age/height/volume/species fields, and a
   reviewed road/access or flight-distance proxy if one is accepted.
3. Classify managed current THLB stands into `ground`, `cable`, `heli`,
   `not_applicable`, or `unclassified_review_required`, with source, confidence,
   and caveat fields.
4. Compare assigned area and volume against MP11 Table 20 and Table 73 targets
   without backfilling WFP percentages as stand-level truth.
5. Rebuild MP11 candidate model-input tables and ForestModel XML with split
   clearcut lanes for ground, cable, and heli.
6. Run Matrix Builder and inspect tracks for split treatment lanes, aggregate
   harvested-volume reporting, and per-system reporting.
7. Assemble a harvest-system candidate runtime and smoke-test all-system and
   no-heli scenarios.
8. Document the public-proxy caveats and decide whether the candidate remains a
   supplement, needs more repair, or is ready for a later publication lane.

## Generated Roots

Phase 14 generated artifacts should use new candidate roots rather than
overwriting the Phase 13 MP11 candidate:

- `data/mp11_harvest_system_model_input_bundle/`
- `output/patchworks_tfl6_mp11_harvest_system_candidate/`
- `models/tfl6_patchworks_model_mp11_harvest_system_candidate/`
- `runtime/mp11_harvest_system/`
- `plots/mp11_harvest_system/`

These roots are intended for generated candidate artifacts and should remain
ignored unless a later task explicitly promotes compact manifests or public-safe
release inputs.

## Non-Goals

- Do not claim WFP LBB reconstruction or WFP model equivalence.
- Do not treat MP11 as approved AAC.
- Do not publish private, sensitive, or proprietary source data.
- Do not replace the Phase 5 accepted public teaching/runtime baseline in this
  phase.
- Do not use MP11 aggregate harvest-system percentages as direct stand-level
  truth.
- Do not use the old MP10 ground/cable/heli DBH thresholds as current MP11 MHA
  criteria.
- Do not run Matrix Builder or Patchworks runtime work before classifier and
  model-input changes are explicitly promoted in later P14 tasks.

## Validation Expectations

P14.1 validation:

- `gh issue list --state open`
- `git diff --check`
- personal-path scan over changed roadmap, changelog, and planning files

Later implementation validation:

- classifier row counts and managed THLB coverage;
- area/volume residuals against MP11 Table 20 and Table 73;
- explicit counts for unclassified or missing-proxy rows;
- XML inspection showing split clearcut lanes;
- Matrix Builder tracks with per-system and aggregate harvest products;
- direct launch smoke;
- all-system scenario smoke;
- no-heli scenario smoke; and
- Sphinx warning-clean if docs are touched.
