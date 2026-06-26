# TFL 6 Model-Input Contract

## Purpose

This P3.7 contract records what Phase 4 may consume when it builds the first
TFL 6 model-input bundle. It reconciles the accepted Phase 2/3 source-layer,
THLB, AU, yield-curve, treatment, transition, cedar, harvest-system, and
embedded NICF/K3Z identity decisions into one implementation handoff.

This note is not a generated model-input bundle. It does not write bundle
tables, materialize outside-AOI expansion geometry, emit ForestModel XML, run
Matrix Builder, or assemble a Patchworks runtime package.

Governing issue: `#32`.

## Accepted Input Artifacts

Phase 4 may consume these reviewed artifacts:

| Artifact family | Path | Role |
| --- | --- | --- |
| Run profile | `config/run_profile.tfl6.yaml` | active TFL 6 source/config entrypoint |
| THLB recipe | `config/tsr/thlb_netdown.recipe.yaml` | accepted Phase 2 THLB smoke/netdown recipe surface |
| THLB status | `config/tsr/thlb_reconstructed.status.md` | accepted Phase 2 THLB status and benchmark-tolerance record |
| Static AU contract | `planning/tfl6_au_yield_curve_contract.md` | accepted AU/yield/treatment-eligibility design |
| Static AU universe | `planning/tfl6_static_au_universe.{csv,json,md}` | reviewed AU bins and selected top-area flags |
| Selected strata | `planning/tfl6_static_au_top_strata.csv` | top-area stratum set used for curve compilation |
| Stand-to-AU review table | `planning/tfl6_stand_to_au_review.csv` | reviewed stand attribution source for Phase 3 diagnostics |
| Natural curves | `planning/tfl6_first_growth_au_curves.csv` | accepted natural/untreated VDYP curve table for selected AU families |
| Natural-curve diagnostics | `planning/tfl6_first_growth_shape_diagnostics.{csv,md}` | accepted shape diagnostics with revisit caveat |
| Non-selected AU remap | `planning/tfl6_first_growth_au_remap_audit.{csv,md}` | lexicographic remap audit for non-selected AU bins |
| TIPSY parameter library | `planning/tfl6_mp10_tipsy_parameter_library.{csv,json,md}` | MP10 Tables 27-29 parameter evidence |
| TIPSY crosswalk | `planning/tfl6_tipsy_parameter_crosswalk.{csv,json,md}` | selected-AU to MP10 row/fallback mapping |
| BTC handoff | `data/03_input-tfl6.csv` | selected-AU BatchTIPSY input |
| BTC output | `data/04_output-tfl6.csv` and `data/04_error-tfl6.csv` | reviewed BatchTIPSY output/error surfaces |
| Treated curves | `planning/tfl6_tipsy_managed_curves.csv` | parsed treated/managed curve table |
| Treated-curve diagnostics | `planning/tfl6_tipsy_managed_curve_diagnostics.{csv,md}` | treated curve QA and overlays |
| Treatment contract | `planning/tfl6_treatment_option_contract.md` and `config/silviculture.tfl6.yaml` | accepted treatment IDs, eligibility boundaries, and reporting hooks |
| Transition contract | `planning/tfl6_state_transition_contract.md` | accepted state and transition semantics |
| Cedar design | `planning/tfl6_cedar_signal_design.md` | accepted cedar signal/account/report handoff |
| Embedded identity design | `planning/tfl6_nicf_embedded_identity.md` | accepted K3Z/NICF reference and outside-AOI expansion handoff |

## Required Model-Input Field Families

Phase 4 bundle generation should produce or preserve these field families.
Exact final column names can be finalized in P4.1, but the semantic content
must be present and auditable.

| Field family | Required content |
| --- | --- |
| Stand identity | `feature_id`, `map_id`, `polygon_id`, stable fragment/block key, source layer, source vintage |
| Area accounting | `area_ha`, current-AOI membership, geometry/source QA flags |
| THLB / IFM | accepted THLB flag, `IFM`/managed treatment eligibility, unmanaged/retention/reserve context |
| Curve provenance | `ORIGIN`, natural/untreated curve ID, treated/managed curve ID, curve source, curve QA status |
| Static AU | `au_id`, stratum code, BEC zone/subzone/variant/phase, top-two species combo, L/M/H SI class, selected top-area flag |
| AU remap | selected curve family, non-selected AU remap target, remap confidence/reason |
| Yield curves | natural curve ID, treated curve ID, curve table key, curve diagnostics key |
| Treatment options | accepted base `clearcut_and_plant`, implicit `grow`, CT/fertilization hook flags, deferred treatment blockers |
| Transitions | initial state, managed/unmanaged state, retained/reserve state, regenerated state, deferred/special hook state |
| Harvest system | `HARVEST_SYSTEM` with ground-based, cable, and heli classes; operability/slope proxy fields where accepted |
| Cedar | `cedar_leading`, `western_redcedar_leading`, `yellow_cedar_leading`, `cedar_present`, `cedar_pct`, `old_cedar`, unresolved large/pole proxy fields |
| Cedar context | `cedar_cultural_reserve_context`, `cedar_harvest_candidate`, utility-pole unresolved warning |
| Embedded identity | `embedded_area_class`, `embedded_area_id`, `inside_tfl6_aoi`, `outside_tfl6_aoi_expansion_source` |
| K3Z reference | `is_nicf_k3z_core`, `nicf_k3z_core_external_reference`, `core_overlay_status` |
| Expansion | `is_nicf_expansion_candidate`, `is_nicf_expansion_rejected`, `expansion_candidate_set`, `expansion_screen_status`, `expansion_screen_reason`, `expansion_scenario_group` |
| Reporting groups | whole TFL 6, WFP TFL 6 remainder, K3Z reference, accepted expansion, rejected/unreviewed expansion, cedar signal, harvest system |

## Required Phase 4 QA Checks

Before P4.1 can hand the bundle to XML/Matrix Builder work, it must check:

- current-AOI TFL 6 area does not include outside-AOI expansion source lands;
- rejected and unreviewed expansion pools are report/audit surfaces only;
- embedded identity and cedar status are not AU keys or curve-family keys;
- managed/unmanaged treatment eligibility is separate from natural/treated
  curve provenance;
- natural and treated curve IDs are present for every schedulable AU family or
  have explicit fallback/missing rationale;
- non-selected AU bins map to selected curve families through the recorded
  lexicographic remap audit;
- CT and fertilization hooks remain group-gated to K3Z/NICF core/reference and
  accepted expansion groups;
- base scheduled treatment remains `clearcut_and_plant` for the whole TFL 6
  base case;
- harvest-system classes remain stand-level eligibility/account/report fields,
  not AU or curve identity; and
- cedar reporting fields recompute against the final bundle and explain any
  differences from P3.1 gross diagnostics.

## Rejected Or Deferred Assumptions

Do not implement these silently in Phase 4:

- no model-input bundle generation inside P3.7;
- no outside-AOI expansion geometry materialization or screening inside P3.7;
- no ForestModel XML, Matrix Builder, or runtime package work inside P3.7;
- no AU splits by cedar, K3Z/NICF, expansion, THLB, operability, treatment
  eligibility, or scenario state;
- no curve-family splits solely by cedar or embedded identity;
- no hidden THLB deduction for cedar cultural reserve or embedded identity;
- no schedulable rejected or unreviewed expansion pools;
- no CT/fertilization activation in the WFP/TFL 6 remainder;
- no cedar-specific base treatments, hard cedar reserve targets,
  utility-pole-grade price premium, or cedar-only curve family; and
- no claim that delivered-cost proxy accounts are real delivered-cost
  forecasts.

## P3.7 Acceptance

P3.7 is complete when this contract, `config/run_profile.tfl6.yaml`,
`config/tipsy/tfl6.yaml`, `ROADMAP.md`, `CHANGE_LOG.md`, and issue state all
point to the same Phase 4 entry boundary.

Validation status:

- YAML parsing passed for `config/run_profile.tfl6.yaml` and
  `config/tipsy/tfl6.yaml`.
- Sphinx documentation built with warnings treated as errors.
- `femic prep validate-case` parsed the run profile but could not complete in
  this shell because the linked public-data mirror requires Arbutus auth and
  DataLad/git-annex materialization/unlock recovery before FileGDB reads can
  proceed. Treat that as a local data-materialization/preflight blocker for
  Phase 4 setup, not as a P3.7 syntax failure.
