# TFL 6 Embedded NICF/K3Z Identity Contract

## Purpose

The TFL 6 teaching model must embed the original NICF/K3Z teaching area inside
the larger TFL 6 model while preserving distinct identities for:

- the broader TFL 6 model area;
- the K3Z/NICF core teaching AOI; and
- expansion candidate areas considered for NICF-style teaching scenarios.

This is a Phase 3 design contract for P3.2 / `#9`. It does not build geometry,
model-input tables, ForestModel XML, Matrix Builder outputs, or Patchworks
runtime files.

Related stakeholder framing is recorded in
`planning/tfl6_stakeholder_context.md`. The embedded identity contract should
support NICF-facing community/expansion reporting and WFP-facing
fibre-supply/value/cost comparison in the same runtime.

## Design Principle

NICF/K3Z and expansion identity must be represented as stand-level or
block-level grouping attributes, not as AU identity.

Reason:

- AUs define yield-curve families and should remain focused on stable
  ecological/species/SI strata.
- NICF/K3Z membership and expansion-candidate membership are planning/reporting
  identities and scenario groupings.
- Patchworks needs these identities for group accounts, matching targets, and
  reports, but they should not force duplicate AU families or duplicate yield
  curves.

## Required Identity Classes

The first reviewed contract should define at least these mutually auditable
classes:

| Identity | Meaning | Expected use |
| --- | --- | --- |
| `tfl6_base` | Area inside the accepted TFL 6 AOI, reported separately from the mostly external K3Z reference and any outside-AOI expansion source lands. | Whole-TFL accounting, comparison reports, broader teaching context. |
| `nicf_k3z_core` | Original K3Z/NICF teaching AOI identity from the K3Z tenure source; under the current TFL 6 AOI it is mostly an external/reference carve-out rather than a material current-AOI class. | Separate area/yield/account reporting where present, continuity with the K3Z teaching instance, and explicit carve-out audit. |
| `nicf_expansion_candidate` | Proximal or adjacent public forested land outside the accepted current TFL 6 AOI that is eligible for candidate expansion scenarios. | Scenario toggles, candidate pool accounting, AAC-uplift comparisons, matching targets. |
| `nicf_expansion_rejected` | Outside-AOI public forest land considered but screened out by productivity, THLB-equivalent eligibility, operability, tenure/public-land availability, proximity, constraint, or review criteria. | Audit trail, teaching comparison, rejected-pool reporting. |

The implementation can use a more compact coded field, but it must preserve
these distinctions in auditable form.

## P3.2b K3Z/NICF Core AOI Overlay Identity

P3.2b reviewed the original K3Z/NICF core source against the accepted current
TFL 6 AOI. The accepted K3Z/NICF core source remains the K3Z teaching-instance
tenure boundary:

| Surface | Path | Role |
| --- | --- | --- |
| K3Z/NICF core tenure | `external/femic-k3z-instance/data/bc/cfa/k3z/CFA K3Z Tenure.shp` | authoritative source for the original K3Z teaching AOI identity |
| Current TFL 6 AOI | `data/source/tfl_6/aoi/tfl_6_boundary.gpkg` | active model extraction boundary accepted under P1.6 |
| Pre-pivot FDU 1/2/3 FSP AOI | `data/source/nicf_fsp/aoi/nicf_fsp_aoi.shp` | historical NICF FSP planning context, not the K3Z tenure and not the active model boundary |

Non-mutating overlay diagnostics in EPSG:3005:

| Surface | Rows | Gross area | Area intersecting current TFL 6 AOI | Area outside current TFL 6 AOI |
| --- | ---: | ---: | ---: | ---: |
| K3Z/NICF core tenure | `3` | `2391.511 ha` | `0.072 ha` | `2391.440 ha` |
| Pre-pivot FDU 1/2/3 FSP AOI | `3` | `147798.392 ha` | `118617.247 ha` | `29181.145 ha` |
| Current TFL 6 AOI | `182` | `217042.719 ha` | `217042.719 ha` | `0.000 ha` |

Interpretation:

- The K3Z/NICF core tenure is the correct identity source for continuity with
  the original K3Z teaching instance.
- The current FADM-derived TFL 6 AOI appears to exclude essentially all of the
  K3Z community-forest tenure. This is consistent with the working hypothesis
  that K3Z/community-forest lands may have been carved out of TFL 6 before the
  current boundary vintage.
- The pre-pivot FDU 1/2/3 FSP AOI is a broader planning context and overlaps a
  large part of current TFL 6, but it is not the same thing as the K3Z tenure.
- Therefore the first TFL 6 model-input bundle cannot honestly label a large
  current-AOI area as `nicf_k3z_core` unless the maintainer explicitly chooses
  to expand the model boundary beyond the accepted current TFL 6 AOI or adds an
  external adjacent/community-forest overlay surface.

Accepted P3.2b identity behavior for the first bundle:

| Field / class | First behavior |
| --- | --- |
| `is_nicf_k3z_core` | `true` only for stands or fragments that materially intersect the accepted K3Z tenure source after the final bundle overlay; expected current-AOI area is effectively zero under the current TFL 6 boundary. |
| `embedded_area_class` | use `wfp_tfl6_remainder` or equivalent for current-AOI TFL 6 stands; use explicit outside-AOI expansion classes for reviewed external public-forest source lands; do not silently assign FDU 1/2/3 area to `nicf_k3z_core`. |
| `embedded_area_id` | preserve `k3z_tenure` as a source identity/provenance ID where the K3Z overlay is present; preserve FDU/LU IDs separately as planning context if used. |
| `nicf_k3z_core_external_reference` | recommended review flag for the K3Z tenure source when it is reported alongside, but mostly outside, the current TFL 6 AOI. |
| `core_overlay_status` | record `inside_current_tfl6`, `outside_current_tfl6`, or `tiny_boundary_overlap` during Phase 4 QA so the carve-out condition is auditable. |

Rejected P3.2b shortcuts:

- Do not use the pre-pivot FDU 1/2/3 FSP AOI as a synonym for
  `nicf_k3z_core`.
- Do not force the K3Z tenure into the current TFL 6 AOI by dissolving or
  snapping geometry.
- Do not create separate AU or yield-curve families for K3Z identity.
- Do not gate CT/fertilization across broad FDU 1/2/3 area as though it were
  the K3Z/NICF core.

Open design consequence for P3.2c/P3.2d:

- Expansion-candidate classes should be defined from proximal or adjacent
  public forested land outside the current TFL 6 AOI.
- If student scenarios need direct comparison with the original K3Z tenure,
  the first design should treat K3Z as an external/reference group or adjacent
  carve-out group, not as a large current-AOI embedded core.
- Group accounts and reports should preserve the distinction between K3Z
  tenure, FDU/LU planning context, expansion candidates, and the WFP/TFL 6
  remainder.

## P3.2c Expansion And Remainder Identity Classes

P3.2c defines the identity classes that Phase 4 must be able to carry, but it
does not materialize candidate geometry or execute screening logic. Candidate
status is a model-design/reporting identity, not an AU or yield-curve identity.

Accepted class vocabulary:

| `embedded_area_class` | Meaning | First-bundle behavior |
| --- | --- | --- |
| `wfp_tfl6_remainder` | Current-AOI TFL 6 stands that are not accepted K3Z core and are not adjacent/proximal expansion source land. | Default class for the active TFL 6 base geography. |
| `nicf_expansion_candidate` | Proximal or adjacent public forested land outside the accepted current TFL 6 AOI that passes the reviewed expansion screen and is available for NICF-style scenario toggles. | External expansion scenario/reporting class; does not alter TFL 6 base AU identity, curve family, or treatment eligibility by itself. |
| `nicf_expansion_rejected` | Proximal or adjacent public forested land considered by the expansion screen but rejected by productivity, THLB-equivalent eligibility, operability, reserve/retention, constraint, source-quality, tenure/public-land, proximity, or maintainer-review rules. | External rejected-pool audit/reporting class; keeps rejected-pool evidence visible. |
| `nicf_expansion_pool_unreviewed` | Proximal or adjacent public forested land inside the candidate search envelope before the P3.2d/P4 screen assigns accepted or rejected status. | Temporary planning/QA status only; should not be used as an active scenario class in the first runtime package. |
| `nicf_k3z_core_reference` | K3Z tenure identity carried as a provenance/external-reference group because the current TFL 6 AOI contains only a tiny boundary overlap. | Reference/reporting class only unless the maintainer later broadens model geography. |

Candidate-area pool semantics for the active TFL 6 AOI:

- Candidate areas come from proximal or adjacent public forested land outside
  the accepted current TFL 6 AOI.
- Candidate areas should be close enough to the K3Z/NICF context to support the
  community-forest expansion teaching question, but exact proximity thresholds
  remain a P3.2d/P4 review item.
- Candidate areas are outside the accepted K3Z tenure source unless the
  maintainer later decides to model K3Z as part of a broadened external
  geography. Under the current overlay, K3Z core is effectively external to
  the active TFL 6 AOI.
- Candidate areas must be separately identifiable from the WFP/TFL 6 remainder
  so scenario toggles can move or compare them without relabeling the whole
  TFL 6 model.
- Candidate status is not equivalent to TFL 6 THLB status. External expansion
  candidates need separate fields for source-pool membership, THLB-equivalent
  eligibility, treatment eligibility, public-land/tenure availability,
  operability, and scenario activation.
- Rejected candidates remain valuable teaching evidence; they explain why a
  plausible-looking area is not used for expansion scenarios.

Required source/provenance fields for the first candidate screen:

| Field family | Candidate field(s) | Purpose |
| --- | --- | --- |
| Stand key and area | `feature_id`, `map_id`, `polygon_id`, `area_ha` | trace candidate decisions to final bundle stands/fragments |
| Current AOI membership | `inside_tfl6_aoi` plus `outside_tfl6_aoi_expansion_source` | distinguish active TFL 6 base geography from external expansion source geography |
| K3Z reference overlay | `is_nicf_k3z_core`, `core_overlay_status`, `nicf_k3z_core_external_reference` | keep K3Z tenure continuity separate from expansion decisions |
| Expansion identity | `embedded_area_class`, `embedded_area_id`, `is_nicf_expansion_candidate`, `is_nicf_expansion_rejected` | carry candidate/rejected/remainder classes into Patchworks groups |
| Candidate set | `expansion_candidate_set`, `expansion_scenario_group` | support multiple future candidate-pool definitions or scenario toggles |
| Screen status | `expansion_screen_status`, `expansion_screen_reason` | explain accepted/rejected/unreviewed decisions |
| Tenure/public-land availability | public land / tenure source, candidate availability flag, exclusion reason | confirm the expansion source is public forested land suitable for consideration |
| THLB and eligibility | final Phase 4 TFL 6 THLB flag where applicable, external THLB-equivalent flag, `IFM`, `RETENTION`, reserve/non-THLB status | prevent candidate status from silently overriding land-base eligibility |
| Productivity | `site_index`, `est_site_index`, `estimated_site_index`, AU/SI class, VDYP curve availability | support productivity screening and AAC-uplift plausibility |
| Operability/cost | `HARVEST_SYSTEM`, operability/slope proxy fields, ground/cable/heli class | support delivered-cost proxy and operability screening |
| Constraints/context | UWR/WHA/OGMA/recreation/riparian/retention/context flags where carried by Phase 4 | keep constrained/rejected reasons auditable |
| Stakeholder grouping | `wfp_tfl6_remainder`, whole-TFL group, FDU/LU context where carried | support WFP-facing comparison and FDU/LU context reporting |

First screen-status vocabulary:

| `expansion_screen_status` | Meaning |
| --- | --- |
| `accepted_candidate` | external public-forest candidate passed the reviewed screen and may be toggled in expansion scenarios |
| `rejected_productivity` | failed the reviewed productivity/SI/yield screen |
| `rejected_non_thlb` | outside active TFL 6 THLB where applicable, outside external THLB-equivalent landbase, or otherwise not schedulable under the expansion land-base contract |
| `rejected_operability` | failed the reviewed operability/harvest-system/slope/cost screen |
| `rejected_constraint` | rejected by reserve, retention, UWR/WHA/OGMA, riparian, recreation, or other constraint context |
| `rejected_tenure_public_land` | failed public-land, tenure-availability, or adjacency/proximity requirements |
| `rejected_source_quality` | missing or ambiguous source fields prevent reliable classification |
| `rejected_review` | maintainer-reviewed rejection not covered by a more specific code |
| `unreviewed_pool` | inside the search envelope but not yet screened |
| `not_in_pool` | TFL 6 base area or external public forest land not considered for expansion |

P3.2c accepts only the identity/class vocabulary. P3.2d must define the
Patchworks group-account, matching-target, scenario-toggle, and report
requirements that consume these classes. Any executable screen or candidate
geometry materialization, including the external public-forest search envelope,
belongs to Phase 4 or a later explicitly scoped implementation lane.

## Candidate Stand Attributes

Phase 4 model-input generation should receive explicit fields such as:

- `embedded_area_class`;
- `embedded_area_id`;
- `is_nicf_k3z_core`;
- `is_nicf_expansion_candidate`;
- `is_nicf_expansion_rejected`;
- `expansion_candidate_set`;
- `expansion_screen_status`;
- `expansion_screen_reason`;
- `expansion_scenario_group`; and
- optional source geometry/provenance fields for K3Z/NICF and expansion
  overlays.

Exact field names can be finalized in P3.7 / the model-input contract, but the
identity content must be available before P4.1 starts.

## P3.2d Patchworks Accounts, Targets, Toggles, And Reports

P3.2d defines the Patchworks-facing contract that consumes the P3.2b/P3.2c
identity fields. It is still design-only: it does not create model-input
tables, ForestModel XML, Matrix Builder output, or Patchworks runtime files.

Required group dimensions:

| Dimension | Accepted values / examples | Purpose |
| --- | --- | --- |
| `embedded_area_class` | `wfp_tfl6_remainder`, `nicf_k3z_core_reference`, `nicf_expansion_candidate`, `nicf_expansion_rejected`, `nicf_expansion_pool_unreviewed` | primary group split for accounts, targets, and reports |
| `embedded_area_id` | `tfl6_current_aoi`, `k3z_tenure`, candidate-pool IDs, rejected-pool IDs | provenance and scenario-group traceability |
| `inside_tfl6_aoi` | `true` / `false` | separate active TFL 6 base geography from external source lands |
| `outside_tfl6_aoi_expansion_source` | `true` / `false` | prevent outside-AOI expansion lands from being hidden in whole-TFL totals |
| `expansion_candidate_set` | reviewed candidate-set name or `none` | support multiple candidate pools without changing AU identity |
| `expansion_scenario_group` | scenario group label or `none` | support Patchworks toggles and teaching comparisons |
| `expansion_screen_status` | P3.2c accepted/rejected/unreviewed status | preserve accepted/rejected-pool audit evidence |
| `core_overlay_status` | `inside_current_tfl6`, `outside_current_tfl6`, `tiny_boundary_overlap` | keep K3Z carve-out status visible |

Required account families:

| Account family | Split by | Base behavior |
| --- | --- | --- |
| Area | embedded area class, candidate set, screen status, TFL 6 AOI membership | report gross and schedulable area; do not merge outside-AOI expansion lands into base TFL 6 area |
| Managed / unmanaged area | embedded area class, `IFM`, retention, THLB/THLB-equivalent status | verify candidate status does not silently override treatment eligibility |
| Harvest area | embedded area class, harvest system, treatment, scenario group | compare where harvest pressure shifts under expansion scenarios |
| Harvest volume | embedded area class, AU, product group, harvest system | compare WFP-facing supply effects against NICF expansion gains |
| Residual inventory | embedded area class, AU, cedar signal, age class, harvest system | support post-scenario state comparison and teaching diagnostics |
| Delivered-cost proxy | embedded area class, harvest system, slope/operability class | expose ground/cable/heli cost tradeoffs without claiming real delivered cost |
| Cedar signal | embedded area class, cedar-leading/present/old-cedar flags | connect P3.1 cedar reporting to NICF and WFP comparison groups |
| Rejected-pool diagnostics | rejection reason, candidate set, source quality, tenure/public-land availability | show why plausible adjacent areas were not activated |

Required matching targets:

| Target / comparison | Purpose | Base status |
| --- | --- | --- |
| Whole TFL 6 vs WFP remainder | compare base TFL 6 outcomes with and without separately reported current-AOI remainder | report/comparison target only |
| K3Z reference vs expansion candidates | compare continuity with the original K3Z teaching AOI against outside-AOI candidate pools | report/comparison target only |
| Expansion accepted vs rejected | show the opportunity cost and evidence trail for candidate screening | report/comparison target only |
| Expansion scenario uplift | compare added area, THLB-equivalent area, harvest area, and harvest volume when accepted external candidates are activated | scenario target; no base hard constraint |
| WFP fibre supply impact | compare whole-TFL and WFP-remainder harvest volume/value proxies before and after expansion scenarios | scenario target; no base hard constraint |
| Delivered-cost proxy shift | compare ground/cable/heli mix under expansion scenarios | scenario target; proxy only |
| Cedar/community outcomes | compare cedar availability, scheduled cedar harvest, and residual old-cedar context by group | report/comparison target only |

Required scenario toggles:

| Toggle | Effect | Guardrail |
| --- | --- | --- |
| `base_tfl6_only` | use current-AOI TFL 6 stands and report K3Z as reference/provenance where available | default first-runtime behavior |
| `include_nicf_expansion_candidates` | activates reviewed outside-AOI `accepted_candidate` lands for scenario comparison | only accepted candidates; never unreviewed or rejected pools |
| `report_rejected_expansion_pool` | exposes rejected-pool area and rejection reasons | report-only; not schedulable |
| `k3z_reference_reporting` | reports K3Z tenure continuity alongside the TFL 6 model | report-only unless a later broadened-geometry lane explicitly activates it |
| `nicf_ct_fert_eligible_groups` | gates CT/fertilization hooks to K3Z core/reference and accepted expansion candidates | no CT/fert activation outside reviewed NICF groups |

Required reports:

| Report | Minimum splits | Interpretation |
| --- | --- | --- |
| Embedded landbase summary | embedded area class, AOI membership, candidate set, screen status | shows current TFL 6, K3Z reference, outside-AOI candidate, rejected, and unreviewed pools separately |
| Area and THLB-equivalent summary | embedded area class, `IFM`, retention, THLB/THLB-equivalent, harvest system | checks that expansion identity does not override landbase eligibility |
| Fibre-supply comparison | embedded area class, period, treatment, product group, AU | shows whole-TFL/WFP supply implications of NICF scenarios |
| Delivered-cost proxy comparison | embedded area class, period, harvest system, operability/slope class | lets students evaluate whether expansion shifts harvest into higher-cost systems |
| Cedar/community comparison | embedded area class, cedar signal, period, residual/scheduled status | connects P3.1 cedar interests to K3Z/NICF and WFP-facing tradeoffs |
| Expansion screen audit | candidate set, screen status, screen reason, source-quality and tenure/public-land fields | preserves why accepted and rejected candidate areas differ |
| K3Z continuity report | K3Z reference status, area, AU/SI/species context where present, comparison to accepted expansion candidates | links the TFL 6 teaching model back to the original K3Z instance |

The reporting design should make tradeoffs visible. Expansion candidates that
increase NICF opportunity may still affect WFP fibre supply, fibre value, or
delivered unit cost in the broader teaching model; those effects should be
reportable rather than hidden inside a single whole-model total.

Rejected P3.2d shortcuts:

- Do not place rejected or unreviewed expansion pools into schedulable base
  area.
- Do not let outside-AOI expansion lands inflate base current-AOI TFL 6 area
  accounts.
- Do not create separate AU or yield-curve families only because a stand is in
  a K3Z/NICF or expansion group.
- Do not create hard expansion or cedar targets in the base model; keep first
  targets as report/comparison surfaces unless a later scenario lane reviews a
  constraint.
- Do not treat delivered-cost proxy accounts as real delivered-cost forecasts.

## P3.2e Dependency Handoff To P3.7/P4.1

P3.2e locks what later contract and implementation lanes must carry forward.
This is still design-only. It does not materialize outside-AOI expansion
geometry, run candidate screening, generate the model-input bundle, emit XML,
run Matrix Builder, or assemble a Patchworks runtime package.

Required P3.7 run-profile/model-input contract fields:

| Field / family | Required handoff | P3.7/P4.1 expectation |
| --- | --- | --- |
| `embedded_area_class` | canonical group class from P3.2c | required field in the model-input contract |
| `embedded_area_id` | source/provenance ID for TFL 6, K3Z reference, or candidate pool | required field where source attribution exists |
| `inside_tfl6_aoi` | boolean AOI membership | required field; current-AOI TFL 6 base area must remain separable |
| `outside_tfl6_aoi_expansion_source` | boolean expansion-source membership | required field for any external candidate materialization lane |
| `is_nicf_k3z_core` | material intersection with accepted K3Z tenure source | required QA field; expected current-AOI area remains effectively zero |
| `nicf_k3z_core_external_reference` | K3Z tenure reported as external/reference identity | required if K3Z is reported beside current-AOI TFL 6 outputs |
| `core_overlay_status` | `inside_current_tfl6`, `outside_current_tfl6`, or `tiny_boundary_overlap` | required QA field if K3Z overlay is carried |
| `is_nicf_expansion_candidate` | accepted outside-AOI candidate flag | required only after a reviewed external candidate screen exists |
| `is_nicf_expansion_rejected` | rejected outside-AOI candidate flag | required only after a reviewed external candidate screen exists |
| `expansion_candidate_set` | candidate-pool identifier | required for any accepted, rejected, or unreviewed candidate pool |
| `expansion_screen_status` | P3.2c status code | required for candidate audit and rejected-pool reporting |
| `expansion_screen_reason` | human-readable or coded screen reason | required for rejected and reviewed candidates |
| `expansion_scenario_group` | scenario/toggle group label | required before activating expansion scenarios |

Required P4.1 model-input behavior:

- Carry current-AOI TFL 6 base stands as `wfp_tfl6_remainder` unless a later
  reviewed overlay assigns a more specific current-AOI reporting class.
- Keep original K3Z tenure identity as external/reference provenance unless a
  later broadened-geometry lane explicitly activates it.
- Treat outside-AOI expansion candidates as external source geography. They
  must not inflate base current-AOI TFL 6 area accounts.
- Carry rejected and unreviewed expansion pools as report/audit surfaces only.
  They are not schedulable and must not contribute to active expansion scenario
  area.
- Keep embedded-area fields out of AU keys, curve-family keys, and base THLB
  netdown rules.
- Join embedded-area fields to treatment eligibility, harvest-system, cedar,
  and THLB/THLB-equivalent fields only as reporting, account, target, or
  scenario-filter dimensions.

Dependency boundaries:

| Lane | Handoff from P3.2 | Boundary |
| --- | --- | --- |
| P3.3 AU contract | embedded identity is explicitly not an AU key | no AU rebuild solely for K3Z/NICF or expansion status |
| P3.4 yield curves | embedded identity may split reports, not curve families | no duplicate curve families solely for embedded groups |
| P3.5 treatments | CT/fertilization hooks can be gated to K3Z/NICF and accepted expansion groups | no activation outside reviewed NICF groups |
| P3.6 transitions | preserve embedded fields through grow, retention, harvest, and scenario hooks | no base transition changes caused only by embedded identity |
| P3.1 cedar design | cedar reports split by embedded group | no cedar hard target or cedar-only treatment created by P3.2 |
| P2 THLB/source layers | use accepted TFL 6 THLB for current-AOI stands and THLB-equivalent fields for external candidates | no new THLB source-layer work in P3.2 |
| P3.7 run profile | name and require the fields above | no runtime build |
| P4.1 model-input bundle | implement field generation and QA from reviewed sources | first implementation lane for bundle tables |
| Phase 4 Patchworks build | consume generated fields for accounts, targets, toggles, and reports | no Matrix Builder or runtime package in P3.2 |

P3.2 is complete when this handoff is recorded, roadmap and issue state are
synchronized, and the governing issue is closed with an explicit closeout
comment.

## Dependencies

- P3.3 / `#28` owns AU identity and curve-lane semantics; P3.2 fields are not
  AU keys.
- P3.4 / `#29` owns actual yield-curve build and QA; P3.2 fields are report
  splits, not curve-family keys.
- P3.5 / `#30` owns treatment options; P3.2 provides group gates for
  NICF-specific CT/fertilization hooks.
- P3.6 / `#31` owns base state-transition logic; P3.2 fields must be preserved
  through transitions without changing base state semantics.
- P3.1 / `#8` owns cedar signals; P3.2 provides embedded group splits for
  cedar reports and stakeholder comparisons.
- P3.2 / `#9` owns the embedded NICF/K3Z and expansion-candidate identity
  design, and hands implementation naming to P3.7/P4.1.
- P3.7 owns final run-profile/model-input field naming before Phase 4 starts.
- P4.1 owns executable field generation and QA in the model-input bundle.

## Acceptance Checks

- The K3Z/NICF core tenure source can be overlaid against the current TFL 6
  AOI, and the near-zero current-AOI intersection is reported rather than
  hidden.
- A stand in an expansion-candidate pool can be identified separately from the
  K3Z/NICF core and from the TFL 6 remainder.
- Group-account, matching-target, and report requirements are listed before
  P4.1 starts.
- Embedded identity fields do not change AU assignment or curve family.
- Expansion scenarios can change inclusion/eligibility/reporting without
  redefining AUs.
- P3.7/P4.1 handoff fields and dependency boundaries are explicit before P3.2
  closes.
